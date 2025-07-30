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

