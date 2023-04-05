resource "hcloud_ssh_key" "default" {
  name       = "ssh_key"
  public_key = file("~/.ssh/id_rsa.pub")
}