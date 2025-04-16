terraform {
  backend "s3" {
    bucket = "ftc-video-to-zip"
    key    = "ftc-video-to-zip/terraform.tfstate"
    region = "us-east-1"
  }


}
provider "aws" {
  region = var.region_default
}


provider "kubernetes" {
  host                   = module.eks.endpoint
  cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority)
  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    command     = "aws"
    # Specify cluster name dynamically
    args = ["eks", "get-token", "--cluster-name", module.eks.cluster_name]
  }
}
