import os
import json
import requests
import openai


def search_papers(topic: str, n: int = 5):
    """Use OpenAI API to search for papers related to a topic.

    Returns a list of dictionaries with keys 'title' and 'pdf_url'.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    openai.api_key = api_key

    system_msg = {
        "role": "system",
        "content": (
            "You are a helpful assistant that provides a list of academic papers "
            "with direct links to their PDFs."
        ),
    }
    user_msg = {
        "role": "user",
        "content": (
            f"Provide a JSON list of {n} notable academic papers about '{topic}'. "
            "Each list item should have 'title' and 'pdf_url'."
        ),
    }

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[system_msg, user_msg],
    )
    content = response["choices"][0]["message"]["content"]
    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError("OpenAI response is not valid JSON") from exc
    return data


def download_pdf(url: str, output_dir: str) -> str:
    """Download a PDF from URL to the output directory."""
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.basename(url.split("?")[0]) or "download.pdf"
    path = os.path.join(output_dir, filename)
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    with open(path, "wb") as fh:
        fh.write(resp.content)
    return path


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Search for papers using OpenAI and download their PDFs"
    )
    parser.add_argument("topic", help="Topic to search for")
    parser.add_argument(
        "-n", "--num", type=int, default=5, help="Number of papers to retrieve"
    )
    parser.add_argument(
        "-o", "--output", default="papers", help="Directory to save PDFs"
    )
    args = parser.parse_args()

    papers = search_papers(args.topic, args.num)
    for paper in papers:
        title = paper.get("title")
        url = paper.get("pdf_url")
        if not url:
            print(f"No URL for '{title}', skipping")
            continue
        print(f"Downloading '{title}' from {url}")
        try:
            path = download_pdf(url, args.output)
            print(f"Saved to {path}")
        except Exception as exc:
            print(f"Failed to download {url}: {exc}")


if __name__ == "__main__":
    main()
