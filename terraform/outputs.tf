output "servers_status" {
  value = {
    for server in hcloud_server.app :
    server.name => server.status
  }
}

output "servers_ips" {
  value = {
    for server in hcloud_server.app :
    server.name => server.ipv4_address
  }
}