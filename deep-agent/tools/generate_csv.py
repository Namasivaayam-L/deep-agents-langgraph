"""CSV generation tool."""
from langchain_core.tools import tool




@tool
def generate_csv(content: str, filename: str = "output.csv") -> str:
    """Generates a CSV file from CSV-formatted string."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return f"CSV saved: {filename}"
