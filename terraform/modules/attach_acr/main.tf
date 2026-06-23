data "azurerm_kubernetes_cluster" "aks" {

  name                = var.aks_name
  resource_group_name = var.aks_resource_group
}

data "azurerm_container_registry" "acr" {

  name                = var.acr_name
  resource_group_name = var.acr_resource_group
}

resource "azurerm_role_assignment" "acr_pull" {

  principal_id = data.azurerm_kubernetes_cluster.aks.kubelet_identity[0].object_id

  role_definition_name = "AcrPull"

  scope = data.azurerm_container_registry.acr.id
}