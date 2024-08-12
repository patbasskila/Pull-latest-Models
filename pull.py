import os
import requests
import json

def get_latest_release_info(model_name):
    """
    Get the latest release information of the model using Ollama's API.
    """
    url = f"https://api.ollama.com/v1/models/{model_name}/latest"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch the latest release info: {response.status_code}")

def is_latest_version_installed(model_name, latest_version, save_dir):
    """
    Check if the latest version of the model is already installed.
    """
    version_file = os.path.join(save_dir, f"{model_name}_version.txt")
    if os.path.exists(version_file):
        with open(version_file, 'r') as f:
            installed_version = f.read().strip()
        return installed_version == latest_version
    return False

def download_model(model_name, version, save_dir):
    """
    Download the model and save it to the specified directory.
    """
    url = f"https://api.ollama.com/v1/models/{model_name}/download?version={version}"
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        model_path = os.path.join(save_dir, f"{model_name}_{version}.bin")
        with open(model_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return model_path
    else:
        raise Exception(f"Failed to download the model: {response.status_code}")

def save_version_info(model_name, version, save_dir):
    """
    Save the version information after downloading the model.
    """
    version_file = os.path.join(save_dir, f"{model_name}_version.txt")
    with open(version_file, 'w') as f:
        f.write(version)

def main():
    model_name = "mistral"
    save_dir = "D:/Models"

    # Ensure the save directory exists
    os.makedirs(save_dir, exist_ok=True)

    try:
        # Get the latest release information
        release_info = get_latest_release_info(model_name)
        latest_version = release_info['version']

        # Check if the latest version is already installed
        if is_latest_version_installed(model_name, latest_version, save_dir):
            print(f"The latest version {latest_version} of {model_name} is already installed.")
        else:
            # Download the latest version of the model
            print(f"Downloading {model_name} version {latest_version}...")
            model_path = download_model(model_name, latest_version, save_dir)
            print(f"Model downloaded and saved to {model_path}.")

            # Save the version information
            save_version_info(model_name, latest_version, save_dir)
            print(f"Version information saved.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
