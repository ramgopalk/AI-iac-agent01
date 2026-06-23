import json
import os
import shutil
import subprocess
from pathlib import Path


class TerraformExecutor:

    def __init__(self):

        self.temp_dir = Path("terraform/temp")

        self.temp_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    # =====================================
    # CREATE TERRAFORM VARS FILE
    # =====================================

    def create_tfvars(self, variables):

        tfvars_path = self.temp_dir / "terraform.tfvars.json"

        with open(tfvars_path, "w") as f:
            json.dump(variables, f, indent=2)

        return tfvars_path

    # =====================================
    # COPY MODULE FILES
    # =====================================

    def prepare_module(self, module_name):

        module_path = Path(f"terraform/modules/{module_name}")

        if not module_path.exists():
            raise Exception(
                f"Module not found: {module_name}"
            )

        # clean temp dir
        for item in self.temp_dir.iterdir():

            if item.is_dir():
                shutil.rmtree(item)

            else:
                item.unlink()

        # copy module files
        for item in module_path.iterdir():

            target = self.temp_dir / item.name

            if item.is_dir():
                shutil.copytree(item, target)

            else:
                shutil.copy2(item, target)

    # =====================================
    # RUN TERRAFORM COMMAND
    # =====================================

    def run_command(self, command):

        result = subprocess.run(
            command,
            cwd=self.temp_dir,
            capture_output=True,
            text=True,
            shell=True
        )

        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    # =====================================
    # EXECUTE TERRAFORM
    # =====================================

    def apply(self, module_name, variables):

        self.prepare_module(module_name)

        self.create_tfvars(variables)

        results = {}

        # terraform init
        results["init"] = self.run_command(
            "terraform init"
        )

        if results["init"]["returncode"] != 0:
            return results

        # terraform plan
        results["plan"] = self.run_command(
            "terraform plan"
        )

        if results["plan"]["returncode"] != 0:
            return results

        # terraform apply
        results["apply"] = self.run_command(
            "terraform apply -auto-approve"
        )

        return results