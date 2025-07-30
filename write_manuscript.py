import os
import json
import re
from pathlib import Path
from typing import List, Dict

import openai

from search_and_download import search_papers, download_pdf
from convert_to_latex import convert_pdf_to_latex


def group_and_rank_papers(
    topic: str, papers: List[Dict[str, str]]
) -> List[Dict[str, List[Dict[str, str]]]]:
    """Use OpenAI to group and rank papers by relevance."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    openai.api_key = api_key
    system_msg = {
        "role": "system",
        "content": (
            "You group academic papers about a topic and rank them by relevance."
        ),
    }
    prompt = (
        "Group the following papers related to '{topic}' and rank them by "
        "relevance in JSON format as {{'groups': [{{'name': str, 'papers': "
        "[{{'title': str, 'pdf_url': str}}]}}]}}:".format(topic=topic)
    )
    user_msg = {"role": "user", "content": prompt + json.dumps(papers)}
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[system_msg, user_msg]
    )
    data = json.loads(response["choices"][0]["message"]["content"])
    return data.get("groups", [])


def _latex_to_markdown(text: str) -> str:
    """Very naive LaTeX to Markdown converter."""
    text = re.sub(r"\\cite\{[^}]*\}", "", text)
    text = re.sub(r"\\ref\{[^}]*\}", "", text)
    text = re.sub(r"\\[a-zA-Z]+\*?\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\[a-zA-Z]+\*?", "", text)
    return text


def write_manuscript(topic: str, markdown_notes: str, output: Path) -> None:
    """Use OpenAI to write a LaTeX manuscript from notes."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    openai.api_key = api_key
    system_msg = {
        "role": "system",
        "content": (
            "You are an academic writing agent that produces LaTeX manuscripts."
        ),
    }
    user_msg = {
        "role": "user",
        "content": (
            f"Write a full LaTeX manuscript about '{topic}' using the following "
            f"notes:\n{markdown_notes}"
        ),
    }
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[system_msg, user_msg]
    )
    latex = response["choices"][0]["message"]["content"]
    output.write_text(latex)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate a manuscript from searched papers"
    )
    parser.add_argument("topic", help="Topic to research")
    parser.add_argument("-n", "--num", type=int, default=5, help="Number of papers")
    parser.add_argument(
        "-o", "--output", default="papers", help="Directory for downloaded papers"
    )
    parser.add_argument(
        "--manuscript", default="manuscript.tex", help="Output LaTeX file"
    )
    args = parser.parse_args()

    papers = search_papers(args.topic, args.num)
    groups = group_and_rank_papers(args.topic, papers)

    markdown_notes = []
    for group in groups:
        gname = group.get("name", "group")
        for paper in group.get("papers", []):
            url = paper.get("pdf_url")
            if not url:
                continue
            path = download_pdf(url, os.path.join(args.output, gname))
            latex_dir = convert_pdf_to_latex(Path(path).as_uri())
            for tex_file in Path(latex_dir).rglob("*.tex"):
                text = tex_file.read_text(errors="ignore")
                markdown_notes.append(_latex_to_markdown(text))

    notes = "\n".join(markdown_notes)
    write_manuscript(args.topic, notes, Path(args.manuscript))


if __name__ == "__main__":
    main()
