"""
Competitive Intelligence Analyzer
==================================
Analyzes competitor websites and generates structured intelligence briefs
using Claude AI. Fetches relevant pages, extracts insights, and produces
formatted reports saved to the outputs/ directory.

Usage:
    python main.py "Hugging Face" https://huggingface.co
"""

import os
import re
import json
import logging
import argparse

import anthropic
from dotenv import load_dotenv

from scraper import fetch_website_links, fetch_website_contents
from prompts import (
    LINK_SELECTOR_SYSTEM_PROMPT,
    BRIEF_SYSTEM_PROMPT,
    build_link_selection_prompt,
    build_brochure_prompt,
)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

MODEL = "claude-sonnet-4-6"
OUTPUT_DIR = "outputs"

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ---------------------------------------------------------------------------
# Link Selection
# ---------------------------------------------------------------------------

def select_relevant_links(url: str) -> list[str]:
    """Ask Claude to pick the most relevant pages from a website for intel gathering."""
    logger.info("Selecting relevant links for: %s", url)

    links = fetch_website_links(url)
    response = client.messages.create(
        model=MODEL,
        max_tokens=1_000,
        system=LINK_SELECTOR_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_link_selection_prompt(url, links)}],
    )

    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]
    if raw.endswith("```"):
        raw = raw.rsplit("```", 1)[0]

    selected = json.loads(raw)["relevant_links"]
    logger.info("Found %d relevant links", len(selected))
    return selected

# ---------------------------------------------------------------------------
# Content Fetching
# ---------------------------------------------------------------------------

def fetch_all_relevant_content(url: str) -> str:
    """Fetch the landing page content plus all relevant sub-pages."""
    landing_content = fetch_website_contents(url)
    relevant_links = select_relevant_links(url)

    sections = [f"## Landing Page\n\n{landing_content}\n\n## Relevant Pages"]
    for link in relevant_links:
        page_content = fetch_website_contents(link)
        sections.append(f"### {link}\n\n{page_content}")

    return "\n\n".join(sections)

# ---------------------------------------------------------------------------
# Brief Generation
# ---------------------------------------------------------------------------

def create_brochure(company_name: str, url: str) -> None:
    """Generate and save a competitive intelligence brief for a given company."""
    logger.info("Generating competitive intelligence brief for: %s (%s)", company_name, url)

    content = fetch_all_relevant_content(url)
    response = client.messages.create(
        model=MODEL,
        max_tokens=2_000,
        system=BRIEF_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_brochure_prompt(company_name, content)}],
    )

    brief = response.content[0].text

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    slug = re.sub(r"[^\w]+", "_", company_name.lower()).strip("_")
    output_path = os.path.join(OUTPUT_DIR, f"{slug}.md")

    with open(output_path, "w") as f:
        f.write(brief)

    logger.info("Brief saved to %s", output_path)
    print(brief)

# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate a competitive intelligence brief.")
    parser.add_argument("company", help="Company name (e.g. 'Hugging Face')")
    parser.add_argument("url", help="Company website URL (e.g. https://huggingface.co)")
    args = parser.parse_args()

    create_brochure(args.company, args.url)


if __name__ == "__main__":
    main()
