variable "image" {
  default = "asia-northeast3-docker.pkg.dev/model-sphere-399315/spot/spot_test"
}

variable "machine_type" {
  default = "e2-standard-4"
}

variable "service_account" {
  default = "terraform-infra@model-sphere-399315.iam.gserviceaccount.com"
}

variable "resume" {
  default = false
}

variable "api_host" {}