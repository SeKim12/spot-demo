variable "credentials" {
  default = "../.credentials/gcp-credentials.json"
}

variable "project" {
  default = "model-sphere-399315"
}

variable "region" {
  default = "asia-northeast3"
}

variable "zone" {
  default = "asia-northeast3-a"
}

variable "gcs_path" {
  default = "gs://mdl-ckpts"
}
