import pymupdf
import pdfplumber

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

# if __name__=="__main__":
#     sample_pdf = "C:/Users/arman/Downloads/Arman_Bhattacharjee_Resume.pdf"
#     extracted_text = extract_text(sample_pdf)
#     print(extracted_text[:])