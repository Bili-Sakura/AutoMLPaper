import os
import time
import json
import requests
from pathlib import Path
from zipfile import ZipFile


API_URL = "https://mineru.net/api/v4"


def load_api_key():
    """Load API key from environment or .env file."""
    api_key = os.getenv("API_KEY")
    if api_key:
        return api_key
    env_path = Path(".env")
    if env_path.exists():
        with env_path.open() as f:
            for line in f:
                if line.startswith("API_KEY="):
                    return line.strip().split("=", 1)[1]
    raise RuntimeError("API_KEY not found in environment or .env file")


def create_task(api_key: str, pdf_url: str) -> str:
    url = f"{API_URL}/extract/task"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {
        "url": pdf_url,
        "extra_formats": ["latex"],
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    if result.get("code") != 0:
        raise RuntimeError(f"Failed to create task: {result}")
    return result["data"]["task_id"]


def poll_task(api_key: str, task_id: str, interval: int = 5) -> dict:
    url = f"{API_URL}/extract/task/{task_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    while True:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        result = res.json()
        if result.get("code") != 0:
            raise RuntimeError(f"Failed to get task result: {result}")
        data = result["data"]
        state = data.get("state")
        if state == "done":
            return data
        elif state == "failed":
            raise RuntimeError(f"Task failed: {data.get('err_msg')}")
        time.sleep(interval)


def download_and_extract(zip_url: str, output_dir: Path) -> Path:
    response = requests.get(zip_url, stream=True)
    response.raise_for_status()
    output_dir.mkdir(parents=True, exist_ok=True)
    zip_path = output_dir / "result.zip"
    with open(zip_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)
    return output_dir


def convert_pdf_to_latex(pdf_url: str, output_dir: str = "output") -> Path:
    api_key = load_api_key()
    task_id = create_task(api_key, pdf_url)
    result = poll_task(api_key, task_id)
    zip_url = result.get("full_zip_url")
    if not zip_url:
        raise RuntimeError("No result url found")
    return download_and_extract(zip_url, Path(output_dir))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert PDF to LaTeX using Mineru API")
    parser.add_argument("pdf_url", help="URL of the PDF file to convert")
    parser.add_argument("--out", default="output", help="Directory to save LaTeX files")

    args = parser.parse_args()
    output_dir = convert_pdf_to_latex(args.pdf_url, args.out)
    print(f"LaTeX files saved to: {output_dir}")
