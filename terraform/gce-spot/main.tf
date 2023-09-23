module "gce-container" {
  # https://github.com/terraform-google-modules/terraform-google-container-vm
  source = "terraform-google-modules/container-vm/google"
  version = "~> 2.0"

  container = {
    image = var.image
    volumeMounts = [
      {
        mountPath = "/vol/"
        name = "ckpt"
        readOnly = false
      }
    ]
  }

  volumes = [
    {
      name = "ckpt"
      hostPath = {
        path = "/home/seungwoo_simon_kim/"
      }
    }
  ]

  restart_policy = "Always"
}

resource "google_compute_instance" "default" {
  name         = "test"
  machine_type = var.machine_type

  boot_disk {
    initialize_params {
      image = module.gce-container.source_image
    }
  }

  network_interface {
    network = "default"

    access_config {
      // Ephemeral public IP
    }
  }

  metadata = {
    gce-container-declaration = module.gce-container.metadata_value
    shutdown-script = file("${path.module}/../../scripts/vm_shutdown.sh")
  }

  metadata_startup_script = "echo ${var.gcs_path} >> /etc/profile; toolbox gsutil"
  # "echo GCS_PATH=${var.gcs_path} >> /etc/profile"

  labels = {
    container-vm = module.gce-container.vm_container_label
  }
  
  scheduling {
    preemptible = true
    automatic_restart = false 
    provisioning_model = "SPOT"
  }


  service_account {
    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    email  = "terraform-infra@model-sphere-399315.iam.gserviceaccount.com"
    scopes = ["cloud-platform"]
  }
}