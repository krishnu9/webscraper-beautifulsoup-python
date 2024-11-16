from pathlib import Path
import httpx

class FileSystemSavingStrategy:
    pass

class ImageFetcher:
    def __init__(self, script_dir: Path, storage_strategy: str):
        self.script_dir = script_dir
        self.storage_strategy = storage_strategy

    async def fetch_image_and_save_to_fs(self, url: str):
        file_name = url.split('/')[-1]
        file_path = self.script_dir / 'images' / file_name
        response = httpx.get(url)
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(response.content)
            return file_path
        else:
            print(f"Failed to download image: {url}")
            return None