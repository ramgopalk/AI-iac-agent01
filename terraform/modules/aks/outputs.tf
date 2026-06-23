output "aks_name" {
  value = azurerm_kubernetes_cluster.aks.name
}

output "aks_id" {
  value = azurerm_kubernetes_cluster.aks.id
}

output "kube_config" {
  sensitive = true

  value = azurerm_kubernetes_cluster.aks.kube_config_raw
}