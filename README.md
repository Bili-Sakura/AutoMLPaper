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

## Automatic Manuscript Generation

The `write_manuscript.py` script orchestrates the full workflow from searching
for papers to producing a LaTeX manuscript. It performs the following steps:

1. Search for related papers using the OpenAI API.
2. Group and rank the results.
3. Download each PDF and convert it to LaTeX with Mineru.
4. Extract Markdown notes from the LaTeX sources.
5. Ask the OpenAI API to draft a new LaTeX manuscript from the notes.

### Usage

```bash
export OPENAI_API_KEY=your_openai_key
export API_KEY=your_mineru_token
python write_manuscript.py "neural architecture search" -n 3 --manuscript output.tex
```

The generated manuscript will be saved to `output.tex`.


## arXiv LaTeX Template

A minimal template for writing an arXiv preprint is available in
`arxiv_template/main.tex`. To compile the example document, run:

```bash
cd arxiv_template
pdflatex main.tex
```

The template includes a simple bibliography file `references.bib` and uses
`unsrt` style references.

## Development

Refer to [AGENTS.md](AGENTS.md) for repository guidelines and contribution notes.

