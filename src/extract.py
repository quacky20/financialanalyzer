import pymupdf
import pdfplumber
from store import store_documents

def extract_text_pymupdf(file_path):
    doc = pymupdf.open(file_path)
    text = "\n".join([page.get_text("text") for page in doc])
    return text.strip()

def extract_text_pdfplumber(file_path):
    text = ""
    with pdfplumber.open(file_path) as file:
        for page in file.pages:
            text += page.extract_text() or ""
    return text.strip()

def extract_text(file_path):
    text = extract_text_pymupdf(file_path)

    if not text:
        print("Failed using Pymupdf! Trying using pdfplumber!")
        text = extract_text_pdfplumber(file_path)

    return text

def get_pdf_metadata(file_path):
    try:
        doc = pymupdf.open(file_path)
        metadata = doc.metadata
        doc.close()
        return metadata
    except Exception as e:
        print(f"Error extracting metadata: {e}")
        return {}

def process_pdf(file_path, doc_id):
    text = extract_text(file_path)
    metadata = get_pdf_metadata(file_path)

    metadata["doc_id"] = doc_id
    metadata.setdefault("source", file_path)

    if text:
        store_documents(text, metadata)
        print("PDF stored")
    else:
        print("ERROR: PDF could not be stored")

if __name__=="__main__":
    sample_pdf = "C:/Users/arman/Downloads/Arman_Bhattacharjee_Resume.pdf"
    # extracted_text = extract_text(sample_pdf)
    # print(extracted_text[:])
    process_pdf(sample_pdf, doc_id="123")