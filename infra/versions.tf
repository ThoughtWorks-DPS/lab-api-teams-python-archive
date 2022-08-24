terraform {
  required_version = "~> 1.2"
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }

  # backend "remote" {
  #   hostname     = "app.terraform.io"
  #   organization = "twdps"
  #   workspaces {
  #     prefix = "lab-api-teams-"
  #   }
  # }
}

provider "aws" {
  region = var.aws_region
}
