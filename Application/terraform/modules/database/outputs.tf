output "cluster_endpoint" {
  description = "The cluster endpoint"
  value       = aws_rds_cluster.aurora_serverless.endpoint
}

output "cluster_reader_endpoint" {
  description = "The cluster reader endpoint"
  value       = aws_rds_cluster.aurora_serverless.reader_endpoint
}

output "cluster_id" {
  description = "The cluster identifier"
  value       = aws_rds_cluster.aurora_serverless.id
}

output "master_password" {
  description = "Master password"
  value = aws_rds_cluster.aurora_serverless.master_password
}

output "database_name" {
  description = "Database name"
  value = aws_rds_cluster.aurora_serverless.database_name
}

output "database_arn" {
  description = "Database arn"
  value = aws_rds_cluster.aurora_serverless.arn
}

output "database_master_username" {
  description = "Database master username"
  value = aws_rds_cluster.aurora_serverless.master_username
}

output "database_secretsmanager_secret_arn" {
  description = "Secret with all the connection detaals"
  value = aws_secretsmanager_secret_version.aurora_secret_version.arn
}