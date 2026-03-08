MAX_RELEVANT_LINKS = 5

LINK_SELECTOR_SYSTEM_PROMPT = """
You are a competitive intelligence analyst helping product managers and founders
understand competitor companies.

Your job is to analyze website content and identify the most useful pages for research.

Return ONLY valid JSON — no markdown, no code fences, no explanations.

Expected format:
{
  "relevant_links": [
    "https://example.com",
    "https://example.com/pricing"
  ]
}
""".strip()

BRIEF_SYSTEM_PROMPT = """
You are a competitive intelligence analyst preparing a briefing for product leaders.

Your task is to analyze website content and produce a structured competitive intelligence brief.

Rules:
- Use ONLY information present in the provided content.
- Do NOT invent facts. Label uncertainties as inferences.
- Prefer bullet points over long paragraphs.

Focus areas:
• What the company does and the problems it solves
• Products or services offered
• Target customer segments
• Key value propositions
• Messaging and positioning themes
• Trust signals (testimonials, logos, certifications, partnerships)
• Pricing or business model signals

Output format:

------------------------------------------------
COMPETITIVE INTELLIGENCE BRIEF

Company Overview
[2–3 sentence summary]

Target Customers
[Bullet points]

Key Products or Services
[Bullet points]

Core Value Propositions
[Bullet points]

Messaging and Positioning
[How the company frames itself]

Trust Signals
[Evidence of credibility]

Business Model or Pricing Signals
[Subscription, enterprise, consulting clues]

Strategic Observations
[Insights for a product team]

Potential Opportunities or Gaps
[Possible weaknesses or differentiation angles]
------------------------------------------------
""".strip()


def build_link_selection_prompt(url: str, links: list[str]) -> str:
    prompt = f"""
You are analyzing a company website to identify the most useful pages for competitive intelligence.

Website URL: {url}

Select up to {MAX_RELEVANT_LINKS} links most useful for understanding:
- What the company does
- Products or features
- Pricing or plans
- Company background

Prefer: homepage, product, features, pricing, about, solutions
Avoid: Terms of Service, Privacy Policy, Careers, Blog posts, Login/Signup, Contact

Return only the most relevant links as full https URLs in JSON format.

Links found:
""".strip()

    prompt += "\n" + "\n".join(links)
    return prompt


def build_brochure_prompt(company_name: str, content: str, max_chars: int = 5_000) -> str:
    prompt = f"""
You are analyzing: {company_name}

Below is content from the company's website. Use it to produce a competitive
intelligence brief in markdown (no code blocks).

---

{content}
""".strip()

    return prompt[:max_chars]
