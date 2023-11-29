terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.17.0"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region                   = var.region
  profile                  = "demo-user"
  shared_credentials_files = ["../.credentials/aws-credentials"]
}

module "aws_spot" {
  source = "./modules/ec2"
}