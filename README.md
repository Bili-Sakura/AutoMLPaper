# AutoMLPaper
Write Machine Learning Paper Automatically with Agents

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
