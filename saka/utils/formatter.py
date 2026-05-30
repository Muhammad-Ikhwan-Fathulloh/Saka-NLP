import json
import csv
import io
import re
from typing import List, Dict, Any, Union

class OutputFormatter:
    """
    Utility class to format LLM outputs into various formats locally.
    This helps in saving tokens by avoiding complex formatting requests to the LLM.
    """

    @staticmethod
    def to_markdown(data: Any) -> str:
        """Converts data (list of dicts or dict) to Markdown."""
        if isinstance(data, list):
            if not data:
                return ""
            if isinstance(data[0], dict):
                # Convert list of dicts to Markdown Table
                headers = data[0].keys()
                md = "| " + " | ".join(headers) + " |\n"
                md += "| " + " | ".join(["---"] * len(headers)) + " |\n"
                for row in data:
                    md += "| " + " | ".join(str(row.get(h, "")) for h in headers) + " |\n"
                return md
            else:
                # Convert list of strings to Markdown List
                return "\n".join(f"- {item}" for item in data)
        elif isinstance(data, dict):
            md = ""
            for k, v in data.items():
                md += f"**{k}**: {v}\n"
            return md
        return str(data)

    @staticmethod
    def to_html(text: str) -> str:
        """
        Converts Markdown-like text to basic HTML.
        Custom implementation to avoid heavy dependencies.
        """
        html = text
        # Bold
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        # Italic
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
        # Headers
        html = re.sub(r'^### (.*)$', r'<h3>\1</h3>', html, flags=re.M)
        html = re.sub(r'^## (.*)$', r'<h2>\1</h2>', html, flags=re.M)
        html = re.sub(r'^# (.*)$', r'<h1>\1</h1>', html, flags=re.M)
        # Lists
        html = re.sub(r'^- (.*)$', r'<li>\1</li>', html, flags=re.M)
        html = re.sub(r'(<li>.*</li>)', r'<ul>\1</ul>', html, flags=re.S)
        # Tables (basic)
        if "|" in html and "---" in html:
            rows = html.strip().split('\n')
            table_html = '<table border="1">'
            for i, row in enumerate(rows):
                if '---' in row: continue
                cells = [c.strip() for c in row.split('|') if c.strip()]
                tag = 'th' if i == 0 else 'td'
                table_html += '<tr>' + "".join(f'<{tag}>{c}</{tag}>' for c in cells) + '</tr>'
            table_html += '</table>'
            # Replace the whole table block
            # This is a bit naive, but works for simple cases
            html = table_html
        else:
            # Paragraphs
            html = html.replace('\n', '<br>')
        
        return html

    @staticmethod
    def to_table(data: List[Dict[str, Any]]) -> str:
        """Converts list of dicts to a plain text table summary."""
        if not data or not isinstance(data, list):
            return ""
        headers = data[0].keys()
        # Simple string-based table
        res = " | ".join(headers) + "\n"
        res += "-" * len(res) + "\n"
        for row in data:
            res += " | ".join(str(row.get(h, "")) for h in headers) + "\n"
        return res

    @staticmethod
    def to_csv(data: List[Dict[str, Any]]) -> str:
        """Converts list of dicts to CSV string."""
        if not data or not isinstance(data, list):
            return ""
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()

    @staticmethod
    def to_text(data: Any) -> str:
        """Converts data to clean plain text."""
        if isinstance(data, (list, dict)):
            return json.dumps(data, indent=2)
        return str(data)

    @staticmethod
    def to_json(data: Any) -> str:
        """Converts data to JSON string."""
        return json.dumps(data, indent=2, ensure_ascii=False)

    @classmethod
    def format(cls, data: Any, format_type: str = "markdown") -> str:
        """Main entry point for formatting."""
        fmt = format_type.lower()
        if fmt == "html":
            # If data is not string, convert to md first
            md = cls.to_markdown(data) if not isinstance(data, str) else data
            return cls.to_html(md)
        elif fmt == "markdown":
            return cls.to_markdown(data)
        elif fmt == "table":
            return cls.to_table(data)
        elif fmt == "csv":
            return cls.to_csv(data)
        elif fmt == "json":
            return cls.to_json(data)
        elif fmt == "text":
            return cls.to_text(data)
        return str(data)
