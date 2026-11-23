"""Minimal repro: markitdown 0.1.1 DOCX extraction path (mammoth, CVE-2025-11849).

Usage:
    python repro.py                 # converts a generated benign sample.docx
    python repro.py path/to/file.docx
"""
import sys
import zipfile
from io import BytesIO
from pathlib import Path

from markitdown import MarkItDown, StreamInfo

DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


class DocumentExtractor:
    def _extract_markdown_from_msoffice(self, file_content: bytes, mime_type: str) -> str:
        file = BytesIO(file_content)
        converter = MarkItDown(enable_plugins=False)
        result = converter.convert(file, stream_info=StreamInfo(mimetype=mime_type))
        return result.markdown


def build_sample_docx(path: Path) -> None:
    """Write a minimal, benign .docx so the repro needs no extra dependencies."""
    ct = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" ContentType="application/'
        'vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>'
    )
    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/'
        '2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'
    )
    doc = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:body><w:p><w:r><w:t>Hello from the CVE-2025-11849 repro</w:t></w:r></w:p></w:body>'
        '</w:document>'
    )
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/document.xml", doc)


def main() -> None:
    if len(sys.argv) > 1:
        docx_path = Path(sys.argv[1])
    else:
        docx_path = Path("sample.docx")
        build_sample_docx(docx_path)

    markdown = DocumentExtractor()._extract_markdown_from_msoffice(
        docx_path.read_bytes(), DOCX_MIME
    )
    print(markdown)


if __name__ == "__main__":
    main()
