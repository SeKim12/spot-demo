resource "google_compute_instance" "gce_spot" {
  name         = "test-spot"
  machine_type = var.machine_type

  boot_disk {
    initialize_params {
      image = "ubuntu-os-pro-cloud/ubuntu-pro-1604-lts" # ubuntu-2204-lts"
    }
  }

  network_interface {
    network = "default"

    access_config {
      // Ephemeral public IP
    }
  }

  metadata = {
    serial-port-logging-enable = "TRUE"
    startup-script = templatefile("${path.module}/startup.sh", {
      resume = var.resume
    })
    shutdown-script = templatefile("${path.module}/shutdown.sh", {
      api_host = var.api_host
    })
  }

  scheduling {
    preemptible        = true
    automatic_restart  = false
    provisioning_model = "SPOT"
  }


  service_account {
    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    email  = var.service_account
    scopes = ["cloud-platform"]
  }
}