import json
import os


def load_config(config_path):
    """Loads a config file.

    Args:
        config_path (str): The path to the config file. Must be json.

    Raises:
        FileNotFoundError: If the config file does not exist.

    Returns:
        json: The loaded config file.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file {config_path} not found.")

    with open(config_path, "r") as f:
        config = json.load(f)

    return config


def load_garment_configs(config_path, garments):
    garment_configs = {}
    for filename in os.listdir(config_path):
        if filename.endswith(".json"):
            garment_type = filename.split(".")[0].lower()
            garment_configs[garment_type] = load_config(
                os.path.join(config_path, filename)
            )

    if garments:
        garments_lower = {garment.lower() for garment in garments}
        garment_configs = {
            name: config
            for name, config in garment_configs.items()
            if name in garments_lower
        }

    return garment_configs
