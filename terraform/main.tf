terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials)

  project = var.project
  region  = var.region
  zone    = var.zone
}

module "gce-container" {
  source = "./gce-spot"
  gcs_path = var.gcs_path
}