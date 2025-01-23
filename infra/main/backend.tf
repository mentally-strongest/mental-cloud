terraform {
  required_version = ">= 1.0.0"
  backend "s3" {
    bucket         = "mental-cloud-tf-state-bucket"  # same name from the bootstrap
    key            = "mental-cloud/terraform.tfstate"
    region         = "eu-central-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"          # same name from the bootstrap
  }
}