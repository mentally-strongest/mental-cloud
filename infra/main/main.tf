provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  type    = string
  default = "eu-central-1"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "team" {
  type    = string
  default = "platform"
}

locals {
  common_tags = {
    Environment = var.environment
    Team        = var.team
    Project     = "mental-cloud"
  }
}

# Example resource: Another S3 bucket for your application data
resource "aws_s3_bucket" "app_data" {
  bucket = "my-mental-cloud-app-bucket-1488"  # must be globally unique
  tags   = local.common_tags
}

# Enable versioning
resource "aws_s3_bucket_versioning" "app_data_versioning" {
  bucket = aws_s3_bucket.app_data.id
  versioning_configuration {
    status = "Enabled"
  }
}

output "app_data_bucket_name" {
  value = aws_s3_bucket.app_data.bucket
}
