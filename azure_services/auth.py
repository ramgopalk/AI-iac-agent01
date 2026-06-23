from azure.identity import ClientSecretCredential

from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.containerregistry import ContainerRegistryManagementClient
from azure.mgmt.containerservice import ContainerServiceClient

from config import Config


class AzureAuth:

    def __init__(self):
        self.credential = ClientSecretCredential(
            tenant_id=Config.AZURE_TENANT_ID,
            client_id=Config.AZURE_CLIENT_ID,
            client_secret=Config.AZURE_CLIENT_SECRET
        )

        self.subscription_id = Config.AZURE_SUBSCRIPTION_ID

    def get_resource_client(self):
        return ResourceManagementClient(
            self.credential,
            self.subscription_id
        )

    def get_acr_client(self):
        return ContainerRegistryManagementClient(
            self.credential,
            self.subscription_id
        )

    def get_aks_client(self):
        return ContainerServiceClient(
            self.credential,
            self.subscription_id
        )