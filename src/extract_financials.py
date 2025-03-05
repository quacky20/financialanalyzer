import pymupdf
import pdfplumber
import pandas as pd
import os
import re

KEYWORDS = [
    # 🏦 Balance Sheet Related
    r"balance\s*sheets?", r"statement\s*of\s*financial\s*position",
    r"total\s*assets?", r"current\s*assets?", r"non-current\s*assets?",
    r"liabilities?", r"current\s*liabilities?", r"non-current\s*liabilities?",
    r"shareholders?\s*equity", r"total\s*equity", r"retained\s*earnings?",
    r"working\s*capital", r"goodwill", r"intangible\s*assets?", r"fixed\s*assets?",
    r"long\s*term\s*debt", r"short\s*term\s*debt", r"deferred\s*tax",

    # 📊 Income Statement Related
    r"income\s*statements?", r"statement\s*of\s*operations", r"statement\s*of\s*earnings",
    r"profit\s*&?\s*loss", r"revenue", r"total\s*revenue", r"gross\s*profit",
    r"operating\s*income", r"net\s*income", r"cost\s*of\s*goods\s*sold", r"cogs",
    r"earnings\s*before\s*interest\s*&?\s*taxes?", r"ebit", r"ebitda",
    r"interest\s*expense", r"net\s*profit", r"selling\s*&?\s*administrative\s*expenses?",

    # 💵 Cash Flow Statement Related
    r"cash\s*flow", r"statement\s*of\s*cash\s*flows",
    r"operating\s*activities", r"investing\s*activities", r"financing\s*activities",
    r"net\s*cash\s*flow", r"free\s*cash\s*flow", r"capital\s*expenditures?",

    # 📈 Financial Ratios & Metrics
    r"return\s*on\s*assets?", r"return\s*on\s*equity", r"return\s*on\s*investment",
    r"price\s*to\s*earnings", r"p\/e\s*ratio", r"earnings\s*per\s*share",
    r"gross\s*margins?", r"operating\s*margins?", r"profit\s*margins?",
    r"dividends?", r"payout\s*ratio", r"book\s*value", r"market\s*capitalization",
    r"debt\s*to\s*equity", r"liquidity\s*ratio", r"quick\s*ratio", r"current\s*ratio",
]

def extract_text_and_match_terms(pdf_path, output_dir="data/raw_reports"):
    os.makedirs(output_dir, exist_ok=True)
    matched_pages_file = os.path.join(output_dir, "matched_pages.txt")

    matched_pages = []

    with pymupdf.open(pdf_path) as doc:
        for page_num, page in enumerate(doc):
            text = page.get_text()
            if any(re.search(pattern, text, re.IGNORECASE) for pattern in KEYWORDS):
                matched_pages.append(f"Page {page_num + 1}:\n{text}\n" + "-"*50 + "\n")

    # Save matched pages to a file
    if matched_pages:
        with open(matched_pages_file, "w", encoding="utf-8") as f:
            f.writelines(matched_pages)
        print(f"Matched pages saved.")
    else:
        print("No matching financial terms found in the PDF.")

def extract_tables(pdf_path, output_dir="."):
    os.makedirs(output_dir, exist_ok=True)
    table_file_path = os.path.join(output_dir, "table.csv")
    
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted_tables = page.extract_tables()
            if extracted_tables:  # Check if any table exists
                for table in extracted_tables:
                    if table is not None:  # Ensure it's not an empty table
                        tables.append(pd.DataFrame(table))

    if tables:
        final_df = pd.concat(tables, ignore_index=True)
        final_df.to_csv(table_file_path, index=False, header=False)
        print(f"Tables extracted and saved.")
    else:
        print("No tables found in the PDF.")


if __name__=="__main__":
    sample_pdf = "C:/Users/arman/Downloads/NASDAQ_PZZA_2023.pdf"
    extract_text_and_match_terms(sample_pdf)
    extract_tables(sample_pdf)