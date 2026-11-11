import json
import requests
from pathlib import Path

def download_file(url: str, destination: str):
    with requests.get(url, stream=True, timeout=(10, 60)) as response:
        response.raise_for_status()

        total = int(response.headers.get("content-length", 0))
        downloaded = 0

        with open(destination, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if not chunk:
                    continue

                file.write(chunk)
                downloaded += len(chunk)

                if total:
                    percent = downloaded / total * 100
                    print(f"\rDownloading: {percent:.1f}%", end="")

def install_external_dependencies():
    with open('external_dependencies.json', 'r') as f:
        data = json.load(f)

    print(f"Found {len(data['mods'])} external mods.")

    Path("game_files/mods").mkdir(parents=True, exist_ok=True)

    for mod in data["mods"]:
        print(f"\nInstalling {mod['name']} {mod['version']}")
        download_file(mod["url"], "game_files/mods/" + mod["filename"])
    print("")

    print("\nAll external dependencies have been installed successfully.")

if __name__ == "__main__":
    install_external_dependencies()