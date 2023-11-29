terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.84.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials)

  project = var.project
  region  = var.region
  zone    = var.zone
}

module "gce_spot" {
  source = "./modules/gce_spot"
  api_host = var.api_host
}