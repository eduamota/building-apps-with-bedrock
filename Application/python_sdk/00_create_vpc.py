# create_vpc_script.py
import boto3
import json
import time
import argparse
import sys
from botocore.exceptions import ClientError

def create_vpc(region, vpc_name="bedrock-poc-vpc"):
    """Creates VPC, subnets, IGW, NAT GW, route tables.

    Args:
        region (str): The AWS region to create resources in.
        vpc_name (str): The base name for the VPC and related resources.

    Returns:
        dict: A dictionary containing details of the created VPC resources.

    Raises:
        Exception: If any critical step fails.
    """
    print(f"--- Starting VPC Creation in {region} ---", file=sys.stderr)
    session = boto3.Session(region_name=region)
    ec2 = session.client('ec2')

    # Store results
    vpc_info = {}

    try:
        # Create VPC
        print(f"Creating VPC '{vpc_name}'...", file=sys.stderr)
        vpc_response = ec2.create_vpc(
            CidrBlock='10.0.0.0/16',
            TagSpecifications=[{'ResourceType': 'vpc', 'Tags': [{'Key': 'Name', 'Value': vpc_name}]}]
        )
        vpc_id = vpc_response['Vpc']['VpcId']
        vpc_info['vpc_id'] = vpc_id
        print(f"  VPC ID: {vpc_id}", file=sys.stderr)
        vpc_waiter = ec2.get_waiter('vpc_available')
        vpc_waiter.wait(VpcIds=[vpc_id])
        print("  VPC Available.", file=sys.stderr)

        # Enable DNS attributes
        ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={'Value': True})
        ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsSupport={'Value': True})
        print("  Enabled DNS Hostnames and Support.", file=sys.stderr)

        # Internet Gateway
        print("Creating Internet Gateway...", file=sys.stderr)
        igw_response = ec2.create_internet_gateway(
            TagSpecifications=[{'ResourceType': 'internet-gateway', 'Tags': [{'Key': 'Name', 'Value': f"{vpc_name}-igw"}]}]
        )
        igw_id = igw_response['InternetGateway']['InternetGatewayId']
        vpc_info['igw_id'] = igw_id
        ec2.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
        print(f"  Internet Gateway ID: {igw_id} (attached)", file=sys.stderr)

        # Subnets
        availability_zones = [f'{region}a', f'{region}b', f'{region}c'] # Simple AZ naming
        private_subnet_cidrs = ['10.0.1.0/24', '10.0.2.0/24', '10.0.3.0/24']
        public_subnet_cidrs = ['10.0.101.0/24', '10.0.102.0/24', '10.0.103.0/24']
        private_subnet_ids = []
        public_subnet_ids = []

        print("Creating private subnets...", file=sys.stderr)
        for i, (az, cidr) in enumerate(zip(availability_zones, private_subnet_cidrs)):
            try:
                response = ec2.create_subnet(
                    VpcId=vpc_id, CidrBlock=cidr, AvailabilityZone=az,
                    TagSpecifications=[{'ResourceType': 'subnet', 'Tags': [{'Key': 'Name', 'Value': f"{vpc_name}-private-{i+1}"}]}]
                )
                subnet_id = response['Subnet']['SubnetId']
                private_subnet_ids.append(subnet_id)
                print(f"    Private subnet {i+1}: {subnet_id} in {az}", file=sys.stderr)
            except ClientError as e:
                print(f"    Warning: Could not create private subnet in {az}: {e}. Skipping AZ.", file=sys.stderr)

        print("Creating public subnets...", file=sys.stderr)
        for i, (az, cidr) in enumerate(zip(availability_zones, public_subnet_cidrs)):
            try:
                response = ec2.create_subnet(
                    VpcId=vpc_id, CidrBlock=cidr, AvailabilityZone=az,
                    TagSpecifications=[{'ResourceType': 'subnet', 'Tags': [{'Key': 'Name', 'Value': f"{vpc_name}-public-{i+1}"}]}]
                )
                subnet_id = response['Subnet']['SubnetId']
                public_subnet_ids.append(subnet_id)
                print(f"    Public subnet {i+1}: {subnet_id} in {az}", file=sys.stderr)
            except ClientError as e:
                print(f"    Warning: Could not create public subnet in {az}: {e}. Skipping AZ.", file=sys.stderr)

        vpc_info['private_subnet_ids'] = private_subnet_ids
        vpc_info['public_subnet_ids'] = public_subnet_ids

        if not public_subnet_ids:
            raise Exception("CRITICAL: No public subnets were created. Cannot proceed with NAT Gateway.")
        if not private_subnet_ids:
             print("Warning: No private subnets were created. NAT Gateway route table association will be skipped.", file=sys.stderr)


        print("Waiting for subnets...", file=sys.stderr)
        subnet_waiter = ec2.get_waiter('subnet_available')
        if public_subnet_ids: subnet_waiter.wait(SubnetIds=public_subnet_ids)
        if private_subnet_ids: subnet_waiter.wait(SubnetIds=private_subnet_ids)
        print("  Subnets available.", file=sys.stderr)


        # Public Route Table
        print("Creating Public Route Table...", file=sys.stderr)
        public_rt_response = ec2.create_route_table(
            VpcId=vpc_id,
            TagSpecifications=[{'ResourceType': 'route-table', 'Tags': [{'Key': 'Name', 'Value': f"{vpc_name}-public-rt"}]}]
        )
        public_rt_id = public_rt_response['RouteTable']['RouteTableId']
        vpc_info['public_rt_id'] = public_rt_id
        ec2.create_route(RouteTableId=public_rt_id, DestinationCidrBlock='0.0.0.0/0', GatewayId=igw_id)
        print(f"  Public Route Table ID: {public_rt_id} (route to IGW added)", file=sys.stderr)
        print("  Associating public subnets...", file=sys.stderr)
        for subnet_id in public_subnet_ids:
            ec2.associate_route_table(RouteTableId=public_rt_id, SubnetId=subnet_id)

        # NAT Gateway (requires EIP)
        print("Creating NAT Gateway...", file=sys.stderr)
        eip_response = ec2.allocate_address(Domain='vpc')
        allocation_id = eip_response['AllocationId']
        public_ip = eip_response.get('PublicIp', 'N/A')
        vpc_info['nat_eip_allocation_id'] = allocation_id
        vpc_info['nat_eip_public_ip'] = public_ip
        print(f"    Allocated Elastic IP: {public_ip} ({allocation_id})", file=sys.stderr)

        nat_gateway_id = None
        try:
            nat_response = ec2.create_nat_gateway(
                AllocationId=allocation_id, SubnetId=public_subnet_ids[0], # Place in first public subnet
                TagSpecifications=[{'ResourceType': 'natgateway', 'Tags': [{'Key': 'Name', 'Value': f"{vpc_name}-nat"}]}]
            )
            nat_gateway_id = nat_response['NatGateway']['NatGatewayId']
            vpc_info['nat_gateway_id'] = nat_gateway_id
            print(f"    NAT Gateway ID: {nat_gateway_id}. Waiting...", file=sys.stderr)
            nat_waiter = ec2.get_waiter('nat_gateway_available')
            nat_waiter.wait(NatGatewayIds=[nat_gateway_id])
            print("    NAT Gateway Available.", file=sys.stderr)
        except Exception as nat_err:
             print(f"ERROR Creating NAT Gateway: {nat_err}. Releasing EIP {allocation_id}.", file=sys.stderr)
             ec2.release_address(AllocationId=allocation_id) # Clean up EIP
             vpc_info['nat_gateway_id'] = None # Ensure it's marked as failed
             vpc_info['nat_eip_allocation_id'] = None
             vpc_info['nat_eip_public_ip'] = None
             raise nat_err # Propagate error

        # Private Route Table (only if private subnets exist and NAT GW succeeded)
        private_rt_id = None
        if private_subnet_ids and nat_gateway_id:
            print("Creating Private Route Table...", file=sys.stderr)
            private_rt_response = ec2.create_route_table(
                VpcId=vpc_id,
                TagSpecifications=[{'ResourceType': 'route-table', 'Tags': [{'Key': 'Name', 'Value': f"{vpc_name}-private-rt"}]}]
            )
            private_rt_id = private_rt_response['RouteTable']['RouteTableId']
            vpc_info['private_rt_id'] = private_rt_id
            ec2.create_route(RouteTableId=private_rt_id, DestinationCidrBlock='0.0.0.0/0', NatGatewayId=nat_gateway_id)
            print(f"  Private Route Table ID: {private_rt_id} (route to NAT GW added)", file=sys.stderr)
            print("  Associating private subnets...", file=sys.stderr)
            for subnet_id in private_subnet_ids:
                ec2.associate_route_table(RouteTableId=private_rt_id, SubnetId=subnet_id)
        elif not private_subnet_ids:
            print("Skipping Private Route Table (no private subnets).", file=sys.stderr)
            vpc_info['private_rt_id'] = None
        else: # Private subnets exist, but NAT GW failed
            print("Skipping Private Route Table (NAT Gateway creation failed).", file=sys.stderr)
            vpc_info['private_rt_id'] = None


        print("--- VPC Creation Complete ---", file=sys.stderr)
        return vpc_info

    except Exception as e:
        # Basic cleanup attempt - could be more sophisticated
        print(f"\n--- ERROR during VPC Creation: {e} ---", file=sys.stderr)
        print("Attempting basic cleanup of created resources...", file=sys.stderr)
        if 'nat_gateway_id' in vpc_info and vpc_info['nat_gateway_id']:
             try:
                 print(f"  Deleting NAT Gateway {vpc_info['nat_gateway_id']}...", file=sys.stderr)
                 ec2.delete_nat_gateway(NatGatewayId=vpc_info['nat_gateway_id'])
                 # Add wait for deletion if needed
             except ClientError as del_e: print(f"    Error deleting NAT GW: {del_e}", file=sys.stderr)
        if 'nat_eip_allocation_id' in vpc_info and vpc_info['nat_eip_allocation_id']:
             try:
                 print(f"  Releasing EIP {vpc_info['nat_eip_allocation_id']}...", file=sys.stderr)
                 ec2.release_address(AllocationId=vpc_info['nat_eip_allocation_id'])
             except ClientError as del_e: print(f"    Error releasing EIP: {del_e}", file=sys.stderr)
        if 'igw_id' in vpc_info and 'vpc_id' in vpc_info:
             try:
                 print(f"  Detaching/Deleting IGW {vpc_info['igw_id']}...", file=sys.stderr)
                 ec2.detach_internet_gateway(InternetGatewayId=vpc_info['igw_id'], VpcId=vpc_info['vpc_id'])
                 ec2.delete_internet_gateway(InternetGatewayId=vpc_info['igw_id'])
             except ClientError as del_e: print(f"    Error deleting IGW: {del_e}", file=sys.stderr)
        # Add subnet/route table/VPC deletion if needed, handle dependencies carefully

        raise Exception(f"VPC Creation Failed: {e}") # Re-raise after cleanup attempt


def main():
    parser = argparse.ArgumentParser(description="Create AWS VPC infrastructure for Bedrock RAG.")
    parser.add_argument("--region", required=True, help="AWS region for resource creation (e.g., us-west-2)")
    parser.add_argument("--vpc-name", default="bedrock-poc-vpc", help="Base name for VPC resources")
    args = parser.parse_args()

    try:
        vpc_details = create_vpc(args.region, args.vpc_name)
        # --- IMPORTANT ---
        # Print *only* the JSON output to stdout on success
        # All status/error messages go to stderr using file=sys.stderr
        print(json.dumps(vpc_details, indent=2))
        sys.exit(0) # Explicit success exit code
    except Exception as e:
        # Error message already printed to stderr in create_vpc or here
        print(f"Script failed: {e}", file=sys.stderr)
        sys.exit(1) # Explicit failure exit code

if __name__ == "__main__":
    main()