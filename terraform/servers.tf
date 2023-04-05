resource "hcloud_server" "app" {
  count       = var.instances
  name        = "app-server-${count.index}"
  image       = var.os_type
  server_type = var.server_type
  location    = var.location
  ssh_keys    = [hcloud_ssh_key.default.id]
  labels = {
    type = "application"
  }
  user_data = file("config.yml")
}