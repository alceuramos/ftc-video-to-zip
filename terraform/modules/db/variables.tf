variable "aws_region" {
  type = string
}

variable "db_username" {
  description = "Username for the RDS instance"
  type        = string
  default     = "user_fiap"
}

variable "db_name" {
  description = "Name of the database"
  type        = string
  default     = "database_video_to_zip_service"
}

variable "security_group_id" {
  description = "ID of the security group"
  type        = string
}

