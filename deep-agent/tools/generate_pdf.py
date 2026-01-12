"""PDF generation tool."""
from langchain_core.tools import tool
from fpdf import FPDF




@tool
def generate_pdf(content: str, filename: str = "output.pdf") -> str:
    """Generates a PDF file from text content."""
    safe_text = content.encode("latin-1", "replace").decode("latin-1")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, safe_text)
    pdf.output(filename)
    return f"PDF saved: {filename}"
