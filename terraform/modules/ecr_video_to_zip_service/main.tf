resource "aws_ecr_repository" "ecr_video_to_zip_service" {
  name                 = "ecr_video_to_zip_service"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }
}
