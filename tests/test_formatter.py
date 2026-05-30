import pytest
from saka.utils.formatter import OutputFormatter

def test_to_markdown_list():
    data = ["Apple", "Banana", "Cherry"]
    md = OutputFormatter.to_markdown(data)
    assert "- Apple" in md
    assert "- Banana" in md
    assert "- Cherry" in md

def test_to_markdown_table():
    data = [
        {"Name": "Alice", "Age": 30},
        {"Name": "Bob", "Age": 25}
    ]
    md = OutputFormatter.to_markdown(data)
    assert "| Name | Age |" in md
    assert "| Alice | 30 |" in md
    assert "| Bob | 25 |" in md

def test_to_html_basic():
    md = "# Title\nThis is **bold** and *italic*."
    html = OutputFormatter.to_html(md)
    assert "<h1>Title</h1>" in html
    assert "<strong>bold</strong>" in html
    assert "<em>italic</em>" in html

def test_to_html_table():
    md = "| Header 1 | Header 2 |\n| --- | --- |\n| Cell 1 | Cell 2 |"
    html = OutputFormatter.to_html(md)
    assert '<table border="1">' in html
    assert "<th>Header 1</th>" in html
    assert "<td>Cell 1</td>" in html

def test_to_csv():
    data = [{"ID": 1, "Val": "A"}, {"ID": 2, "Val": "B"}]
    csv_str = OutputFormatter.to_csv(data)
    assert "ID,Val" in csv_str
    assert "1,A" in csv_str
    assert "2,B" in csv_str

def test_to_table_plain():
    data = [{"X": 10, "Y": 20}]
    table = OutputFormatter.to_table(data)
    assert "X | Y" in table
    assert "10 | 20" in table

def test_format_dispatcher():
    data = {"key": "value"}
    res = OutputFormatter.format(data, "markdown")
    assert "**key**: value" in res
    
    res_html = OutputFormatter.format(data, "html")
    assert "<strong>key</strong>: value" in res_html

def test_to_json():
    data = {"name": "Saka", "type": "NLP"}
    res_json = OutputFormatter.to_json(data)
    assert '"name": "Saka"' in res_json
    assert '"type": "NLP"' in res_json
