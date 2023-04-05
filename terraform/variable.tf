variable "hcloud_token" {
  default = "<token>"
}

variable "location" {
  default = "hel1"
}

variable "instances" {
  default = "1"
}

variable "server_type" {
  default = "cx21"
}

variable "os_type" {
  default = "ubuntu-22.04"
}

variable "disk_size" {
  default = "20"
} 

variable "ip_range" {
  default = "10.0.1.0/24"
}