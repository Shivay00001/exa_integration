from pypdf import PdfReader

def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

if __name__ == "__main__":
    # Test the extractor
    text = extract_text_from_pdf("my_cv.pdf")
    if text:
        print("Successfully extracted text from CV:")
        print(text[:500] + "...") # Print first 500 chars
    else:
        print("Failed to extract text.")
