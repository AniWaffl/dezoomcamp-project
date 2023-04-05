resource "hcloud_volume" "server_volume" {
  count    = var.instances
  name     = "volume-${count.index}"
  size     = var.disk_size
  location = var.location
  format   = "xfs"
}

resource "hcloud_volume_attachment" "vol_attachment" {
  count     = var.instances
  volume_id = hcloud_volume.server_volume[count.index].id
  server_id = hcloud_server.app[count.index].id
  automount = true
}