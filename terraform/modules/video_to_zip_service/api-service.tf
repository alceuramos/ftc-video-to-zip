resource "kubernetes_service" "video_to_zip_service_lb" {
  metadata {
    name = "video-to-zip-service-lb"
  }

  spec {
    selector = {
      app = "video-to-zip-service-api"
    }

    port {
      port        = 80
      target_port = 80
    }

    type = "LoadBalancer"
  }
}

output "url" {
  value = kubernetes_service.video_to_zip_service_lb.status.0.load_balancer.0.ingress.0.hostname
}
