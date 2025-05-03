variable "cluster_identifier" {
  description = "The cluster identifier"
  type        = string
}

variable "engine_version" {
  description = "The engine version to use"
  type        = string
  default     = "15.4"
}

variable "database_name" {
  description = "The name of the database to create when the cluster is created"
  type        = string
  default     = "mydb"
}

variable "master_username" {
  description = "Username for the master DB user"
  type        = string
  default     = "admin"
}

variable "backup_retention_period" {
  description = "The days to retain backups for"
  type        = number
  default     = 0
}

variable "preferred_backup_window" {
  description = "The daily time range during which automated backups are created"
  type        = string
  default     = "02:00-03:00"
}

variable "auto_pause" {
  description = "Whether to enable auto pause"
  type        = bool
  default     = true
}

variable "max_capacity" {
  description = "The maximum capacity units for the cluster"
  type        = number
  default     = 4
}

variable "min_capacity" {
  description = "The minimum capacity units for the cluster"
  type        = number
  default     = 2
}

variable "seconds_until_auto_pause" {
  description = "The time in seconds before the cluster is paused"
  type        = number
  default     = 300
}

variable "timeout_action" {
  description = "The action to take when the timeout is reached"
  type        = string
  default     = "ForceApplyCapacityChange"
}

variable "vpc_id" {
  description = "The VPC ID where the cluster and security group will be created"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs to use for the Aurora cluster"
  type        = list(string)
}

variable "allowed_cidr_blocks" {
  description = "The CIDR blocks allowed to access the cluster"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}
