resource "kubernetes_deployment" "video_to_zip_service_api" {
  metadata {
    name = "video-to-zip-service-api"
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "video-to-zip-service-api"
      }
    }
    template {
      metadata {
        labels = {
          app = "video-to-zip-service-api"
        }
      }
      spec {
        container {
          image             = "${var.api_image}:latest"
          name              = "video-to-zip-service-api-container"
          command           = ["sh", "-c", "./scripts/api.sh"]
          image_pull_policy = "Always"


          resources {
            limits = {
              cpu    = "1500m"
              memory = "512Mi"
            }
            requests = {
              cpu    = "1m"
              memory = "256Mi"
            }
          }

          port {
            container_port = 80
          }
          env {
            name  = "API_PORT"
            value = "80"
          }
          env {
            name  = "SECRET_KEY"
            value = "your-secret-key"
          }
          env {
            name  = "ALGORITHM"
            value = "HS256"
          }
          env {
            name  = "ACCESS_TOKEN_EXPIRE_MINUTES"
            value = "60"
          }
          env {
            name  = "POSTGRES_HOST"
            value = var.db_url
          }
          env {
            name  = "POSTGRES_USER"
            value = jsondecode(data.aws_secretsmanager_secret_version.db.secret_string)["db-username"]
          }
          env {
            name  = "POSTGRES_PASSWORD"
            value = jsondecode(data.aws_secretsmanager_secret_version.db.secret_string)["db-password"]
          }
          env {
            name  = "POSTGRES_DB"
            value = var.db_db_name
          }
          env {
            name  = "AWS_BUCKET_NAME" // Updated environment variable for S3 bucket name
            value = var.bucket_name   // Use the variable passed from the module
          }
          env {
            name  = "AWS_ACCESS_KEY_ID"
            value = var.aws_access_key_id
          }
          env {
            name  = "AWS_SECRET_ACCESS_KEY"
            value = var.aws_secret_access_key
          }
          env {
            name  = "AWS_REGION"
            value = var.aws_region
          }
          env {
            name  = "AWS_SESSION_TOKEN"
            value = var.aws_session_token
          }
          env {
            name  = "AWS_ACCOUNT_ID"
            value = var.aws_account_id
          }
        }
      }
    }
  }
}



resource "kubernetes_horizontal_pod_autoscaler" "video_to_zip_service" {
  metadata {
    name = "video-to-zip-service-hpa"
  }

  spec {
    max_replicas                      = 3
    min_replicas                      = 1
    target_cpu_utilization_percentage = 80

    scale_target_ref {
      api_version = "apps/v1"
      kind        = "Deployment"
      name        = kubernetes_deployment.video_to_zip_service_api.metadata[0].name
    }
  }
}
