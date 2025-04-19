variable "region_default" {
  default = "us-east-1"
}

variable "eks_name" {
  default = "eks-fiap-tech"
}

variable "node_group_name" {
  default = "eks-fiap-tech-node"
}

variable "node_instance_type" {
  default = "t3a.medium"
}

variable "project_name" {
  default = "fiap-tech-challenge"
}

variable "security_groupe_name" {
  default = "eks-sg"
}

variable "policy_arn" {
  default = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"
}

variable "access_config" {
  default = "API_AND_CONFIG_MAP"
}

variable "vpc_cidr" {
  default = "172.31.0.0/16"
}

variable "account_id" {
  type    = string
  default = "767397802435"
}

variable "aws_access_key_id" {
  type = string
}
variable "aws_secret_access_key" {
  type = string
}
variable "aws_session_token" {
  type = string
}
