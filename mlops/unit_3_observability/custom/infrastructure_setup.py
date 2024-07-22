import os

from mlops.utils.deploy.terraform.env_vars import set_environment_variables
from mlops.utils.deploy.terraform.setup import download_terraform_configurations, setup_configurations

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom

import os

def switch_gitconfig():
    home_dir = "/home/codespace/nilarte"
    gitconfig_path = os.path.join(home_dir, ".gitconfig")
    gitconfig_dir_path = os.path.join(home_dir, ".gitconfig-dir")
    gitconfig_file_path = os.path.join(home_dir, ".gitconfig-file")

    print(gitconfig_path)
    print(gitconfig_dir_path)
    print(gitconfig_file_path)

    # Rename .gitconfig to .gitconfig-dir
    if os.path.exists(gitconfig_path):
        os.rename(gitconfig_path, gitconfig_dir_path)
        print(f"Renamed {gitconfig_path} to {gitconfig_dir_path}")

    # Rename .gitconfig-file to .gitconfig
    if os.path.exists(gitconfig_file_path):
        os.rename(gitconfig_file_path, gitconfig_path)
        print(f"Renamed {gitconfig_file_path} to {gitconfig_path}")

@custom
def setup(*args, **kwargs):
    """
    Downloads the base configurations for Terraform maintained and provided by Mage
    https://github.com/mage-ai/mage-ai-terraform-templates
    """
    switch_gitconfig()
    download_terraform_configurations()

    """
    1. Updates variables in the Terraform variables file.
    2. Adds variables into the main.tf template env_vars.
    3. Adds environment variables to env_vars.json.

    prevent_destroy_ecr:
        True
    project_name:
        "mlops"
    """
    setup_configurations(
        prevent_destroy_ecr=kwargs.get('prevent_destroy_ecr'),
        project_name=kwargs.get('project_name'),
    )

    """
    Use the current environment variables as the environment variables in production.
    Change this if you want different values.
    In a real world environment, we’d have different values but this is here for 
    demonstration purposes and for convenience.
    """
    set_environment_variables(
        password=kwargs.get('password', os.getenv('POSTGRES_PASSWORD')),
        username=kwargs.get('username', os.getenv('POSTGRES_USER')),
        smtp_email=kwargs.get('smtp_email', os.getenv('SMTP_EMAIL')),
        smtp_password=kwargs.get('smtp_password', os.getenv('SMTP_PASSWORD')),
    )