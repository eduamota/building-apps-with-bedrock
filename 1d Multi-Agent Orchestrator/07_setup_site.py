"""
07_setup_site.py — Deploy the static chat website to S3 (website hosting).

Creates a public-read bucket with static website hosting, injects the API endpoint into
index.html, and uploads it. Prints the website URL.

Note: S3 website hosting serves over HTTP. For HTTPS, front it with CloudFront (noted in README).
"""

import json
import common as c

BUCKET = f"{c.SITE_BUCKET_PREFIX}-{c.ACCOUNT_ID}"


def main():
    s3 = c.boto3.client("s3", region_name=c.REGION)
    api = json.load(open(".api.json"))
    endpoint = api["endpoint"]

    # 1. Create bucket (region-aware)
    try:
        if c.REGION == "us-east-1":
            s3.create_bucket(Bucket=BUCKET)
        else:
            s3.create_bucket(Bucket=BUCKET,
                             CreateBucketConfiguration={"LocationConstraint": c.REGION})
        print(f"OK Created bucket {BUCKET}")
    except s3.exceptions.BucketAlreadyOwnedByYou:
        print(f"OK Bucket {BUCKET} exists")

    # 2. Disable Block Public Access (needed for website hosting with a public policy)
    s3.put_public_access_block(
        Bucket=BUCKET,
        PublicAccessBlockConfiguration={
            "BlockPublicAcls": False, "IgnorePublicAcls": False,
            "BlockPublicPolicy": False, "RestrictPublicBuckets": False,
        },
    )

    # 3. Public-read bucket policy
    policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "PublicReadForWebsite", "Effect": "Allow", "Principal": "*",
            "Action": "s3:GetObject", "Resource": f"arn:aws:s3:::{BUCKET}/*",
        }],
    }
    s3.put_bucket_policy(Bucket=BUCKET, Policy=json.dumps(policy))

    # 4. Enable static website hosting
    s3.put_bucket_website(
        Bucket=BUCKET,
        WebsiteConfiguration={
            "IndexDocument": {"Suffix": "index.html"},
            "ErrorDocument": {"Key": "index.html"},
        },
    )

    # 5. Inject the API endpoint into the HTML and upload
    with open("site/index.html") as f:
        html = f.read()
    html = html.replace("__API_ENDPOINT__", endpoint)
    s3.put_object(Bucket=BUCKET, Key="index.html", Body=html.encode(),
                  ContentType="text/html", CacheControl="no-cache")
    print("OK Uploaded index.html (API endpoint injected)")

    website_url = f"http://{BUCKET}.s3-website-{c.REGION}.amazonaws.com"
    with open(".site.json", "w") as f:
        json.dump({"bucket": BUCKET, "websiteUrl": website_url}, f, indent=2)

    print("\n" + "=" * 60)
    print("WEBSITE READY")
    print("=" * 60)
    print(f"URL: {website_url}")
    print(f"API: {endpoint}")
    print("=" * 60)
    return website_url


if __name__ == "__main__":
    main()
