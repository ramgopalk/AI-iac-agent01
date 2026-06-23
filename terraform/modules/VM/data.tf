data "azurerm_virtual_network" "existing_vnet" {

  name                = var.vnet_name
  resource_group_name = var.resource_group_name_vnet

}

data "azurerm_subnet" "existing_subnet" {

  name                 = var.subnet_name

  virtual_network_name = data.azurerm_virtual_network.existing_vnet.name

  resource_group_name  = var.resource_group_name_vnet

}