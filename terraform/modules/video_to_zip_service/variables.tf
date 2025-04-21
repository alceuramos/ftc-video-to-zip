variable "api_image" {
  description = "The Docker image for the video-to-zip service"
  type        = string
}

variable "db_url" {
  description = "The database URL"
  type        = string
}

variable "db_db_name" {
  description = "The database name"
  type        = string
}

variable "secret-name" {
  description = "The name of the secret containing database credentials"
  type        = string
}

variable "bucket_name" {
  description = "The name of the S3 bucket"
  type        = string
}

variable "aws_access_key_id" {
  description = "AWS access key ID"
  type        = string
}

variable "aws_secret_access_key" {
  description = "AWS secret access key"
  type        = string
}

variable "aws_region" {
  description = "AWS region"
  type        = string
}

variable "aws_session_token" {
  description = "AWS session token"
  type        = string
}

variable "aws_account_id" {
  description = "AWS account ID"
  type        = string
}
