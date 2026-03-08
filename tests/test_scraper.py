import pytest
from unittest.mock import patch, MagicMock
from scraper import fetch_website_links, fetch_website_contents


# --- Helpers ---

def make_response(html: str, status_code: int = 200) -> MagicMock:
    mock = MagicMock()
    mock.text = html
    mock.status_code = status_code
    mock.raise_for_status = MagicMock()
    return mock


# --- fetch_website_links ---

class TestFetchWebsiteLinks:

    @patch("scraper.requests.get")
    def test_returns_absolute_links(self, mock_get):
        html = '<a href="/about">About</a><a href="https://other.com">Other</a>'
        mock_get.return_value = make_response(html)

        links = fetch_website_links("https://example.com")

        assert "https://example.com/about" in links
        assert "https://other.com" in links

    @patch("scraper.requests.get")
    def test_filters_anchor_links(self, mock_get):
        html = '<a href="#section">Jump</a>'
        mock_get.return_value = make_response(html)

        links = fetch_website_links("https://example.com")

        assert links == []

    @patch("scraper.requests.get")
    def test_filters_mailto_links(self, mock_get):
        html = '<a href="mailto:hi@example.com">Email</a>'
        mock_get.return_value = make_response(html)

        links = fetch_website_links("https://example.com")

        assert links == []

    @patch("scraper.requests.get")
    def test_filters_tel_links(self, mock_get):
        html = '<a href="tel:+1234567890">Call</a>'
        mock_get.return_value = make_response(html)

        links = fetch_website_links("https://example.com")

        assert links == []

    @patch("scraper.requests.get")
    def test_no_duplicate_links(self, mock_get):
        html = '<a href="/page">P</a><a href="/page">P again</a>'
        mock_get.return_value = make_response(html)

        links = fetch_website_links("https://example.com")

        assert links.count("https://example.com/page") == 1

    @patch("scraper.requests.get")
    def test_empty_page_returns_empty_list(self, mock_get):
        mock_get.return_value = make_response("<html><body></body></html>")

        links = fetch_website_links("https://example.com")

        assert links == []

    @patch("scraper.requests.get")
    def test_raises_on_bad_status(self, mock_get):
        mock_get.return_value = make_response("", 404)
        mock_get.return_value.raise_for_status.side_effect = Exception("404")

        with pytest.raises(Exception):
            fetch_website_links("https://example.com/missing")


# --- fetch_website_contents ---

class TestFetchWebsiteContents:

    @patch("scraper.requests.get")
    def test_returns_visible_text(self, mock_get):
        html = "<html><body><p>Hello world</p></body></html>"
        mock_get.return_value = make_response(html)

        content = fetch_website_contents("https://example.com")

        assert "Hello world" in content

    @patch("scraper.requests.get")
    def test_strips_script_tags(self, mock_get):
        html = "<html><body><script>alert('xss')</script><p>Clean</p></body></html>"
        mock_get.return_value = make_response(html)

        content = fetch_website_contents("https://example.com")

        assert "alert" not in content
        assert "Clean" in content

    @patch("scraper.requests.get")
    def test_strips_style_tags(self, mock_get):
        html = "<html><body><style>body{color:red}</style><p>Text</p></body></html>"
        mock_get.return_value = make_response(html)

        content = fetch_website_contents("https://example.com")

        assert "color" not in content
        assert "Text" in content

    @patch("scraper.requests.get")
    def test_no_blank_lines(self, mock_get):
        html = "<html><body><p>Line one</p><p>Line two</p></body></html>"
        mock_get.return_value = make_response(html)

        content = fetch_website_contents("https://example.com")
        lines = content.splitlines()

        assert all(line.strip() != "" for line in lines)

    @patch("scraper.requests.get")
    def test_returns_at_most_300_lines(self, mock_get):
        many_lines = "".join(f"<p>Line {i}</p>" for i in range(500))
        html = f"<html><body>{many_lines}</body></html>"
        mock_get.return_value = make_response(html)

        content = fetch_website_contents("https://example.com")

        assert len(content.splitlines()) <= 300

    @patch("scraper.requests.get")
    def test_raises_on_bad_status(self, mock_get):
        mock_get.return_value = make_response("", 500)
        mock_get.return_value.raise_for_status.side_effect = Exception("500")

        with pytest.raises(Exception):
            fetch_website_contents("https://example.com/error")
