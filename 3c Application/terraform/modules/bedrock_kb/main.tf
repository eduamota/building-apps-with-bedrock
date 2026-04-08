

resource "aws_iam_role" "bedrock_kb_role" {
  name = "${var.knowledge_base_name}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "bedrock.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "bedrock_kb_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonBedrockFullAccess"
  role       = aws_iam_role.bedrock_kb_role.name
}

# New IAM policy for RDS Data API access
resource "aws_iam_policy" "rds_data_api_policy" {
  name        = "${var.knowledge_base_name}-rds-data-api-policy"
  path        = "/"
  description = "IAM policy for RDS Data API access"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "rds-data:ExecuteStatement",
          "rds-data:BatchExecuteStatement",
          "rds-data:BeginTransaction",
          "rds-data:CommitTransaction",
          "rds-data:RollbackTransaction",
        ]
        Resource = var.aurora_arn
      },
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = var.aurora_secret_arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "rds_data_api_policy_attachment" {
  policy_arn = aws_iam_policy.rds_data_api_policy.arn
  role       = aws_iam_role.bedrock_kb_role.name
}

resource "aws_iam_policy" "bedrock_kb_rds_access" {
  name        = "bedrock_kb_rds_access"
  path        = "/"
  description = "IAM policy for Bedrock Knowledge Base to access RDS"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "rds:DescribeDBClusters",
          "rds:DescribeDBInstances",
          "rds:DescribeDBSubnetGroups",
          "rds:ListTagsForResource",
          "s3:ListBucket",
          "s3:GetObject"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ]
        Resource = var.aurora_secret_arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "rds_policy_attachment" {
  policy_arn = aws_iam_policy.bedrock_kb_rds_access.arn
  role       = aws_iam_role.bedrock_kb_role.name
}

resource "time_sleep" "wait_10_seconds" {
  depends_on = [aws_iam_role_policy_attachment.bedrock_kb_policy]

  create_duration = "10s"
}

resource "aws_bedrockagent_knowledge_base" "main" {
  name = var.knowledge_base_name
  role_arn = aws_iam_role.bedrock_kb_role.arn
  knowledge_base_configuration {
    vector_knowledge_base_configuration {
      embedding_model_arn = "arn:aws:bedrock:us-west-2::foundation-model/amazon.titan-embed-text-v1"
    }
    type = "VECTOR"
  }
  storage_configuration {
    type = "RDS"
    rds_configuration {
      credentials_secret_arn = var.aurora_secret_arn
      database_name = var.aurora_db_name
      resource_arn = var.aurora_arn
      table_name = var.aurora_table_name
      field_mapping {
        primary_key_field = var.aurora_primary_key_field
        vector_field   = var.aurora_verctor_field
        text_field     = var.aurora_text_field
        metadata_field = var.aurora_metadata_field
      }

    }
  }
  depends_on = [ time_sleep.wait_10_seconds ]
}

data "aws_caller_identity" "current" {}

locals {
  bucket_name = "bedrock-kb-${data.aws_caller_identity.current.account_id}"
}

resource "aws_bedrockagent_data_source" "s3_bedrock_bucket" {
  knowledge_base_id = aws_bedrockagent_knowledge_base.main.id
  name              = "s3_bedrock_bucket"
  data_source_configuration {
    type = "S3"
    s3_configuration {
      bucket_arn = var.s3_bucket_arn
    }
  }
  depends_on = [ aws_bedrockagent_knowledge_base.main ]
}