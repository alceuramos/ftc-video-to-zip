module "eks" {
  source             = "./modules/eks"
  eks_name           = var.eks_name
  node_group_name    = var.node_grou_name
  node_instance_type = var.node_instance_type
  subnet_ids         = [for subnet in data.aws_subnet.subnet : subnet.id if subnet.availability_zone != "${var.region_default}e"]
  security_group_id  = module.security_group.security_group_id
  access_config      = var.access_config
  region             = var.region_default
  account_id         = var.account_id
  policy_arn         = var.policy_arn
  role_arn           = data.aws_iam_role.name.arn

  depends_on = [module.security_group, module.db]
}

module "security_group" {
  source              = "./modules/security_group"
  security_group_name = var.security_groupe_name
  vpc_id              = data.aws_vpc.vpc.id
}

module "video_to_zip_service_api" {
  source      = "./modules/video_to_zip_service"
  api_image   = module.ecr_video_to_zip_service.user_ecr_repository_url
  db_url      = module.db.url
  db_db_name  = module.db.db-name
  secret-name = module.db.secret-name

  depends_on = [module.eks, module.security_group, module.db, module.ecr_video_to_zip_service]
}



module "db" {
  source            = "./modules/db"
  security_group_id = module.security_group.security_group_id
  aws_region        = var.region_default
}

module "ecr_video_to_zip_service" {
  source = "./modules/ecr_video_to_zip_service"
}
