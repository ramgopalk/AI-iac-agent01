variable "vm_name" {
  type = string
}

variable "resource_group_name" {
  type = string
}

variable "location" {
  type = string
}

variable "vm_size" {
  type    = string
  default = "Standard_B1s"
}

variable "admin_username" {
  type = string
}

variable "ssh_public_key" {
  type = string
}

variable "subnet_id" {
  type = string
}

variable "image_publisher" {
  type        = string
  description = "Image publisher"
#   default     = "Canonical"
}

variable "image_offer" {
  type        = string
  description = "Image offer"
#   default     = "0001-com-ubuntu-server-jammy"
}

variable "image_sku" {
  type        = string
  description = "Image SKU"
#   default     = "22_04-lts"
}

variable "image_version" {
  type        = string
  description = "Image version"
#   default     = "latest"
}

variable "resource_group_name_vnet" {
  type = string
}

variable "vnet_name" {
  type = string
}

variable "subnet_name" {
  type = string
}