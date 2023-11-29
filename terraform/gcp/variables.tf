variable "credentials" {
  default = "../.credentials/gcp-credentials.json"
}

variable "project" {
  default = "model-sphere-399315"
}

variable "region" {
  default = "us-west2"
}

variable "zone" {
  default = "us-west2-b"
}

variable "gcs_path" {
  default = "gs://mdl-ckpts"
}

variable "api_host" {}
