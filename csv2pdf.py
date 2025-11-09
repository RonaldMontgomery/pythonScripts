import pandas as pd
import pdfkit
from pathlib import Path

# --- Inputs/outputs ---
csv_path = Path("Weekly Report (794506) 20250922.csv").resolve()
html_path = csv_path.with_suffix(".html")          # e.g., ...\Weekly Report ... .html
pdf_path  = csv_path.with_name("FinalOutput.pdf")  # write PDF next to CSV

# --- Make HTML from CSV ---
df = pd.read_csv(csv_path)
df.to_html(html_path, index=False)  # drop the index column in output

# --- wkhtmltopdf configuration ---
# If wkhtmltopdf is on PATH, you can set config=None and skip this.
path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# Optional rendering options (page size, orientation, margins, etc.)
options = {
    "page-size": "Letter",
    "orientation": "Portrait",
    "encoding": "UTF-8",
    "margin-top": "10mm",
    "margin-right": "10mm",
    "margin-bottom": "10mm",
    "margin-left": "10mm",
}

# --- Convert local HTML -> PDF (use from_file, not from_url) ---
pdfkit.from_file(str(html_path), str(pdf_path), configuration=config, options=options)
print(f"Wrote PDF to: {pdf_path}")
