import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
    AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
    AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
    AZURE_SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")

    TERRAFORM_DIR = "terraform/temp"


def validate_config():
    required_vars = [
        "GROQ_API_KEY",
        "AZURE_CLIENT_ID",
        "AZURE_CLIENT_SECRET",
        "AZURE_TENANT_ID",
        "AZURE_SUBSCRIPTION_ID"
    ]

    missing = []

    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)

    if missing:
        raise Exception(
            f"Missing environment variables: {', '.join(missing)}"
        )