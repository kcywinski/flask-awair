import os
import yaml

def load_secrets():
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the full path to the secrets.yml file
    secrets_path = os.path.join(base_dir, 'secrets.yaml')

    # Load URL from secrets.yml
    with open(secrets_path, 'r') as file:
        secrets = yaml.safe_load(file)
        return secrets