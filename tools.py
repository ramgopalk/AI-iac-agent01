import json

from azure_services.discovery import AzureDiscovery
from agent.executor import TerraformExecutor


# =====================================
# INITIALIZE SERVICES
# =====================================

discovery = AzureDiscovery()
executor = TerraformExecutor()


# =====================================
# TOOL DEFINITIONS
# =====================================

TOOLS = [

    # =====================================
    # RESOURCE GROUPS
    # =====================================

    {
        "type": "function",
        "function": {
            "name": "list_resource_groups",
            "description": "List all Azure resource groups",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "create_resource_group",
            "description": "Create a new Azure Resource Group using Terraform",
            "parameters": {
                "type": "object",
                "properties": {

                    "resource_group_name": {
                        "type": "string",
                        "description": "Name of the resource group"
                    },

                    "location": {
                        "type": "string",
                        "description": "Azure region"
                    }
                },

                "required": [
                    "resource_group_name",
                    "location"
                ]
            }
        }
    },

    # =====================================
    # ACR
    # =====================================

    {
        "type": "function",
        "function": {
            "name": "list_acr_registries",
            "description": "List all Azure Container Registries",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "create_acr",
            "description": "Create Azure Container Registry using Terraform",
            "parameters": {
                "type": "object",
                "properties": {

                    "acr_name": {
                        "type": "string",
                        "description": "Globally unique Azure Container Registry name"
                    },

                    "resource_group_name": {
                        "type": "string",
                        "description": "Existing Azure resource group"
                    },

                    "location": {
                        "type": "string",
                        "description": "Azure region"
                    },

                    "sku": {
                        "type": "string",
                        "description": "ACR SKU: Basic, Standard, Premium"
                    },

                    "admin_enabled": {
                        "type": "boolean",
                        "description": "Enable admin user for ACR"
                    }
                },

                "required": [
                    "acr_name",
                    "resource_group_name",
                    "location"
                ]
            }
        }
    },

    # =====================================
    # AKS
    # =====================================

    {
        "type": "function",
        "function": {
            "name": "list_aks_clusters",
            "description": "List all Azure Kubernetes Service clusters",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "create_aks",
            "description": "Create Azure Kubernetes Service cluster using Terraform",
            "parameters": {
                "type": "object",
                "properties": {

                    "aks_name": {
                        "type": "string",
                        "description": "AKS cluster name"
                    },

                    "resource_group_name": {
                        "type": "string",
                        "description": "Existing Azure resource group"
                    },

                    "location": {
                        "type": "string",
                        "description": "Azure region"
                    },

                    "dns_prefix": {
                        "type": "string",
                        "description": "Optional DNS prefix for AKS"
                    },

                    "node_count": {
                        "type": "integer",
                        "description": "Initial node count"
                    },

                    "vm_size": {
                        "type": "string",
                        "description": "Azure VM size"
                    },

                    "kubernetes_version": {
                        "type": "string",
                        "description": "Optional Kubernetes version"
                    }
                },

                "required": [
                    "aks_name",
                    "resource_group_name",
                    "location"
                ]
            }
        }
    },

    # =====================================
    # ACR ↔ AKS ATTACHMENT
    # =====================================

    {
        "type": "function",
        "function": {
            "name": "attach_acr_to_aks",
            "description": "Attach Azure Container Registry to AKS using AcrPull role assignment",

            "parameters": {
                "type": "object",

                "properties": {

                    "aks_name": {
                        "type": "string",
                        "description": "AKS cluster name"
                    },

                    "aks_resource_group": {
                        "type": "string",
                        "description": "AKS resource group"
                    },

                    "acr_name": {
                        "type": "string",
                        "description": "Azure Container Registry name"
                    },

                    "acr_resource_group": {
                        "type": "string",
                        "description": "ACR resource group"
                    }
                },

                "required": [
                    "aks_name",
                    "aks_resource_group",
                    "acr_name",
                    "acr_resource_group"
                ]
            }
        }
    }

]


# =====================================
# TOOL EXECUTOR
# =====================================

def execute_tool(tool_name, arguments):

    arguments = json.loads(arguments)

    # =====================================
    # RESOURCE GROUPS
    # =====================================

    if tool_name == "list_resource_groups":

        return discovery.list_resource_groups()

    elif tool_name == "create_resource_group":

        return executor.apply(
            module_name="rg",
            variables={
                "resource_group_name": arguments["resource_group_name"],
                "location": arguments["location"]
            }
        )

    # =====================================
    # ACR
    # =====================================

    elif tool_name == "list_acr_registries":

        return discovery.list_acr_registries()

    elif tool_name == "create_acr":

        return executor.apply(
            module_name="acr",
            variables={
                "acr_name": arguments["acr_name"],
                "resource_group_name": arguments["resource_group_name"],
                "location": arguments["location"],
                "sku": arguments.get("sku", "Basic"),
                "admin_enabled": arguments.get(
                    "admin_enabled",
                    True
                )
            }
        )

    # =====================================
    # AKS
    # =====================================

    elif tool_name == "list_aks_clusters":

        return discovery.list_aks_clusters()

    elif tool_name == "create_aks":

        return executor.apply(
            module_name="aks",
            variables={

                "aks_name": arguments["aks_name"],

                "resource_group_name": arguments[
                    "resource_group_name"
                ],

                "location": arguments["location"],

                # Auto-generate DNS prefix
                "dns_prefix": arguments.get(
                    "dns_prefix",
                    arguments["aks_name"]
                ),

                "node_count": arguments.get(
                    "node_count",
                    1
                ),

                "vm_size": arguments.get(
                    "vm_size",
                    "Standard_B2s"
                ),

                # Prevent empty string issue
                "kubernetes_version": (
                    arguments.get("kubernetes_version")
                    or None
                )
            }
        )

    # =====================================
    # ATTACH ACR TO AKS
    # =====================================

    elif tool_name == "attach_acr_to_aks":

        return executor.apply(
            module_name="attach_acr",
            variables={

                "aks_name": arguments["aks_name"],

                "aks_resource_group": arguments[
                    "aks_resource_group"
                ],

                "acr_name": arguments["acr_name"],

                "acr_resource_group": arguments[
                    "acr_resource_group"
                ]
            }
        )

    # =====================================
    # UNKNOWN TOOL
    # =====================================

    return {
        "error": f"Unknown tool: {tool_name}"
    }