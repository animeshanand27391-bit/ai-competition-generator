# 🤖 AI-Based Competition Generator

An intelligent agent that scrapes competitor websites and uses AI to generate competitive intelligence reports — automatically.

---

## What It Does

Give it a URL, and it will:

- Crawl the competitor's website and extract all relevant links
- Read and clean page content
- Feed it to an AI model to generate structured competitive insights
- Save the output report to the `outputs/` folder

---

## Tech Stack

- **Python 3.10+**
- **[Requests](https://docs.python-requests.org/)** — HTTP calls
- **[BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)** — HTML parsing & content extraction
- **Claude API (Anthropic)** — AI-generated competitive analysis

---

## Project Structure

```
├── main.py           # Entry point — orchestrates the full pipeline
├── prompts.py        # Prompt templates sent to the AI model
├── scraper.py        # Fetches links and cleans page text from URLs
├── utils.py          # Shared helper functions
├── requirements.txt  # Python dependencies
└── outputs/          # Generated reports saved here
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/ai-competition-generator.git
cd ai-competition-generator
```

### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your API key

Create a `.env` file in the root:

```
ANTHROPIC_API_KEY=your_api_key_here
```

---

## Usage

```bash
python main.py
```

Reports are saved to the `outputs/` directory.

---

## How the Scraper Works

Two core functions in `scraper.py`:

| Function | Description |
|---|---|
| `fetch_website_links(url)` | Extracts all absolute links from a page, filtering out anchors, mailto, and tel links |
| `fetch_website_contents(url)` | Fetches and cleans page text — strips scripts, styles, and blank lines, returns the first 300 lines |

---

## Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to change.

---

## License

[MIT](LICENSE)
