# Building Apps with Amazon Bedrock - Heavy Machinery Assistant

A GenAI application demonstrating Amazon Bedrock Knowledge Base (RAG) and Agents for heavy machinery information retrieval using Amazon Nova models.

## Architecture

- **VPC**: Multi-AZ setup with public/private subnets
- **Database**: Aurora Serverless v2 PostgreSQL 15.14 with pgvector
- **Storage**: S3 bucket for document storage (spec sheets)
- **GenAI**: Bedrock Knowledge Base with Titan embeddings + RDS vector store
- **Models**: Amazon Nova (Micro, Lite, Pro) for inference and validation
- **Apps**: Streamlit-based RAG and Agent interfaces

## Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform >= 1.0
- Python 3.9+
- Access to Amazon Bedrock (Nova models and Titan embeddings)

## Deployment Steps

### Step 1: Deploy Storage Stack

```bash
cd terraform/01_storage_stack
terraform init
terraform plan
terraform apply
```

**Outputs:**
- `aurora_arn`: Aurora cluster ARN
- `aurora_endpoint`: Database endpoint
- `rds_secret_arn`: Secrets Manager ARN for DB credentials
- `s3_bucket_name`: S3 bucket ARN
- `vpc_id`: VPC ID

### Step 2: Initialize Database

Connect to Aurora and create the pgvector schema:

```bash
# Get database credentials from Secrets Manager
aws secretsmanager get-secret-value \
  --secret-id my-aurora-serverless \
  --region us-west-2 \
  --query SecretString \
  --output text | jq -r

# Connect using psql or Data API
# Run the SQL files in order:
# 1. pre-requisites/postgres_data/00_create_tables.sql
# 2. pre-requisites/postgres_data/01_insert_machines.sql
# 3. pre-requisites/postgres_data/02-16_insert_*_data.sql
```

**Create Bedrock Integration Schema:**

```sql
CREATE SCHEMA bedrock_integration;

CREATE TABLE bedrock_integration.bedrock_kb (
    id UUID PRIMARY KEY,
    embedding vector(1536),
    chunks TEXT,
    metadata JSON
);
```

### Step 3: Upload Documents to S3

```bash
cd pre-requisites/documents

# Update ACCOUNT_ID in upload_S3.py if needed
python upload_S3.py
```

This uploads spec sheets for:
- BD850 Bulldozer
- DT1000 Dump Truck
- LE950 Excavator
- FL250 Forklift
- MC750 Mobile Crane

### Step 4: Update and Deploy Bedrock Stack

Update `terraform/02_bedrock_rag_stack/main.tf` with outputs from Step 1:

```hcl
module "bedrock_kb" {
  source = "../modules/bedrock_kb"

  knowledge_base_name        = "my-bedrock-kb"
  knowledge_base_description = "Knowledge base for heavy machinery"

  # Update these with Stack 1 outputs
  aurora_arn        = "arn:aws:rds:us-west-2:058264544288:cluster:my-aurora-serverless"
  aurora_db_name    = "myapp"
  aurora_endpoint   = "my-aurora-serverless.cluster-c9micoqmu13m.us-west-2.rds.amazonaws.com"
  aurora_table_name = "bedrock_integration.bedrock_kb"
  aurora_primary_key_field = "id"
  aurora_metadata_field = "metadata"
  aurora_text_field = "chunks"
  aurora_verctor_field = "embedding"
  aurora_username   = "dbadmin"
  aurora_secret_arn = "arn:aws:secretsmanager:us-west-2:058264544288:secret:my-aurora-serverless-S5ixH2"
  s3_bucket_arn = "arn:aws:s3:::bedrock-kb-058264544288"
}
```

Deploy:

```bash
cd terraform/02_bedrock_rag_stack
terraform init
terraform plan
terraform apply
```

**Outputs:**
- `bedrock_knowledge_base_id`: Knowledge Base ID
- `bedrock_knowledge_base_arn`: Knowledge Base ARN

### Step 5: Sync Knowledge Base

After deployment, sync the Knowledge Base to ingest documents:

```bash
# Via AWS Console: Bedrock > Knowledge Bases > Select KB > Sync
# Or via CLI:
aws bedrock-agent start-ingestion-job \
  --knowledge-base-id <KB_ID> \
  --data-source-id <DATA_SOURCE_ID> \
  --region us-west-2
```

### Step 6: Run Applications

#### RAG Application

```bash
cd rag_app

# Update app.py with your Knowledge Base ID
# Line 13: kb_id = st.sidebar.text_input("Knowledge Base ID", "YOUR_KB_ID")

streamlit run app.py
```

**Features:**
- Nova model selection (Micro, Lite, Pro)
- Knowledge Base retrieval (3 results)
- Prompt validation (heavy machinery topics only)
- Temperature and Top_P controls

#### Agent Application

```bash
cd agent_app

# Update app.py with your Agent ID and Alias
# Line 99: agent_id = st.sidebar.text_input("Agent ID", "YOUR_AGENT_ID")
# Line 100: agent_alias_id = st.sidebar.text_input("Agent Alias ID", "YOUR_ALIAS_ID")

streamlit run app.py
```

**Features:**
- Session-based conversations
- Nova model validation
- Agent invocation with action groups
- Supports 5 machine types

## Model Configuration

Both apps use **Amazon Nova models**:
- `us.amazon.nova-micro-v1:0` - Fast, cost-effective
- `us.amazon.nova-lite-v1:0` - Balanced performance
- `us.amazon.nova-pro-v1:0` - Highest quality

## Prompt Validation

Both apps validate prompts to ensure queries are about heavy machinery:
- **Category A**: Model architecture questions (rejected)
- **Category B**: Profanity/toxic content (rejected)
- **Category C**: Off-topic subjects (rejected)
- **Category D**: System instructions (rejected)
- **Category E**: Heavy machinery topics (accepted)

## Available Equipment

- **BD850** - Large Bulldozer
- **DT1000** - Large Mining Dump Truck
- **LE950** - Large Excavator
- **FL250** - Heavy-Duty Industrial Forklift
- **MC750** - Large Mobile Crane

## Cleanup

```bash
# Delete Bedrock stack
cd terraform/02_bedrock_rag_stack
terraform destroy

# Delete storage stack
cd ../01_storage_stack
terraform destroy

# Note: S3 bucket has force_destroy=true, so it will be deleted with contents
```

## Troubleshooting

**Aurora Connection Issues:**
- Ensure you're connecting from within the VPC or use RDS Data API
- Check security group allows port 5432 from your CIDR

**Knowledge Base Sync Fails:**
- Verify S3 bucket has documents in `spec-sheets/` prefix
- Check IAM role has permissions to read S3 and write to RDS
- Ensure pgvector extension is installed: `CREATE EXTENSION vector;`

**App Shows "Unable to answer":**
- Verify prompt is about heavy machinery
- Check Knowledge Base ID is correct
- Ensure Knowledge Base sync completed successfully

## Cost Considerations

- **Aurora Serverless v2**: Scales 0.5-1 ACU (~$0.12/hr when active)
- **Bedrock Knowledge Base**: Pay per query
- **Nova Models**: Pay per token (Micro < Lite < Pro)
- **S3**: Minimal storage costs
- **NAT Gateway**: ~$0.045/hr + data transfer

Estimated monthly cost for development: **$50-100**

## Security Notes

- Database credentials stored in Secrets Manager
- S3 bucket blocks public access
- VPC uses private subnets for database
- IAM roles follow least privilege principle
- All data encrypted at rest (AES256)
