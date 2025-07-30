# AutoMLPaper
Write Machine Learning Paper Automatically with Agents

## Searching and Downloading Papers

The `search_and_download.py` script uses the OpenAI API to suggest relevant
papers for a given topic and attempts to download the provided PDF links.

### Usage

Install requirements:

```bash
pip install -r requirements.txt
```

Run the script with an OpenAI API key in the environment:

```bash
export OPENAI_API_KEY=your_key_here
python search_and_download.py "neural architecture search" -n 3 -o downloads
```

Downloaded PDFs will be saved in the specified output directory.

## Mineru Conversion Utility

This repository includes `convert_to_latex.py` which demonstrates how to
convert a PDF paper to LaTeX using the [Mineru API](https://mineru.net/).
The API key must be provided via the `API_KEY` environment variable or in a
local `.env` file with the line:

```bash
API_KEY=your_mineru_token
```

### Usage

```bash
python convert_to_latex.py <PDF_URL> --out output_directory
```

The script submits a conversion task, waits for completion and downloads the
resulting ZIP archive containing the LaTeX files into `output_directory`.

## Development

Refer to [AGENTS.md](AGENTS.md) for repository guidelines and contribution notes.
