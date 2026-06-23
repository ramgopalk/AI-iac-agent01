from azure_services.auth import AzureAuth


class AzureDiscovery:

    def __init__(self):
        auth = AzureAuth()

        self.resource_client = auth.get_resource_client()
        self.acr_client = auth.get_acr_client()
        self.aks_client = auth.get_aks_client()

    # -----------------------------------
    # RESOURCE GROUPS
    # -----------------------------------

    def list_resource_groups(self):

        groups = self.resource_client.resource_groups.list()

        results = []

        for group in groups:
            results.append({
                "name": group.name,
                "location": group.location
            })

        return results

    # -----------------------------------
    # ACR
    # -----------------------------------

    def list_acr_registries(self):

        registries = self.acr_client.registries.list()

        results = []

        for registry in registries:
            results.append({
                "name": registry.name,
                "location": registry.location,
                "resource_group": self.extract_resource_group(
                    registry.id
                )
            })

        return results

    # -----------------------------------
    # AKS
    # -----------------------------------

    def list_aks_clusters(self):

        clusters = self.aks_client.managed_clusters.list()

        results = []

        for cluster in clusters:
            results.append({
                "name": cluster.name,
                "location": cluster.location,
                "resource_group": self.extract_resource_group(
                    cluster.id
                )
            })

        return results

    # -----------------------------------
    # HELPERS
    # -----------------------------------

    def extract_resource_group(self, resource_id):

        parts = resource_id.split("/")

        if "resourceGroups" in parts:
            index = parts.index("resourceGroups")
            return parts[index + 1]

        return None