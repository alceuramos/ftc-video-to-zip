resource "aws_db_instance" "rds_postgresql" {
  identifier                          = "rds-postgresql"
  allocated_storage                   = 20
  max_allocated_storage               = 25
  engine                              = "postgres"
  engine_version                      = "16.3"
  instance_class                      = "db.t3.micro"
  username                            = jsondecode(aws_secretsmanager_secret_version.db-secret-version.secret_string)["db-username"]
  password                            = jsondecode(aws_secretsmanager_secret_version.db-secret-version.secret_string)["db-password"]
  parameter_group_name                = "default.postgres16"
  skip_final_snapshot                 = true
  publicly_accessible                 = true
  backup_retention_period             = 7
  db_name                             = var.db_name
  vpc_security_group_ids              = [var.security_group_id]
  iam_database_authentication_enabled = true



  tags = {
    Name        = "ftc-video-to-zip"
    Repository  = "https://github.com/alceuramos/ftc-video-to-zip"
    Environment = "Prod"
    ManagedBy   = "Terraform"
  }

  timeouts {
    create = "15m"
    update = "15m"
    delete = "15m"
  }

}



resource "random_password" "example" {
  length  = 16
  special = false
}

resource "random_uuid" "uui" {
}
resource "aws_secretsmanager_secret" "db-secret" {
  name        = "fiap-tech-challenge-db-secret-${random_uuid.uui.result}"
  description = "Secret for the RDS instance"
}
resource "aws_secretsmanager_secret_version" "db-secret-version" {
  secret_id = aws_secretsmanager_secret.db-secret.id
  secret_string = jsonencode({
    db-username = var.db_username
    db-password = random_password.example.result
  })
}

output "db-name" {
  value = aws_db_instance.rds_postgresql.db_name
}

output "url" {
  value = aws_db_instance.rds_postgresql.endpoint
}

output "secret-name" {
  value = aws_secretsmanager_secret.db-secret.name
}

