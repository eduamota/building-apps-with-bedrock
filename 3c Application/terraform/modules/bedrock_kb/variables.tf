variable "knowledge_base_name" {
  description = "The name of the Bedrock knowledge base"
  type        = string
}

variable "knowledge_base_description" {
  description = "The description of the Bedrock knowledge base"
  type        = string
}

variable "aurora_arn" {
  description = "The ARN of the Aurora database"
  type = string
}

variable "aurora_db_name" {
  description = "The name of the Aurora database"
  type        = string
}

variable "aurora_endpoint" {
  description = "The endpoint of the Aurora database"
  type        = string
}

variable "aurora_table_name" {
  description = "The name of the table in the Aurora database"
  type        = string
}

variable "aurora_username" {
  description = "The username for the Aurora database"
  type        = string
}

variable "aurora_secret_arn" {
  description = "The ARN of the secret containing the Aurora database password"
  type        = string
}

variable "aurora_verctor_field" {
  description = "The column name for the vector values"
  type = string  
}

variable "aurora_text_field" {
  description = "The column name for the text values"
  type = string
}

variable "aurora_metadata_field" {
  description = "The column name for the metadata values"
  type = string
}

variable "aurora_primary_key_field" {
  description = "The column name for the primary key field"
  type = string
}

variable "s3_bucket_arn" {
  description = "The ARN for the S3 bucket where the data is"
  type = string
}