variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "expiration_days" {
  description = "Number of days after which objects should be deleted"
  type        = number
  default     = 30
} 
