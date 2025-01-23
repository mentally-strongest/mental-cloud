terraform {
  required_version = ">= 1.0.0"
  backend "local" {}
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  type    = string
  default = "eu-central-1"
}

variable "tf_state_bucket_name" {
  type        = string
  description = "Unique name of the S3 bucket for Terraform remote state."
  default     = "mental-cloud-tf-state-bucket"
}

resource "aws_s3_bucket" "tf_state" {
  bucket = var.tf_state_bucket_name

  # (Optional) tags
  tags = {
    Name        = "TF State Bucket"
    Environment = "bootstrap"
  }
}

resource "aws_s3_bucket_public_access_block" "tf_state_public_access_block" {
  bucket                  = aws_s3_bucket.tf_state.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_dynamodb_table" "tf_lock" {
  name         = "terraform-state-lock"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Name        = "TF Lock Table"
    Environment = "bootstrap"
  }
}

output "tf_state_bucket_name" {
  description = "Name of the S3 bucket for Terraform state"
  value       = aws_s3_bucket.tf_state.bucket
}

output "tf_lock_table_name" {
  description = "Name of the DynamoDB lock table"
  value       = aws_dynamodb_table.tf_lock.name
}
