
import fitz


def extract_text_from_pdf(uploaded_file):
    """Extract text from an uploaded PDF CV."""

    try:
        pdf_bytes = uploaded_file.getvalue()

        with fitz.open(stream=pdf_bytes, filetype="pdf") as pdf:
            extracted_text = []

            for page in pdf:
                extracted_text.append(page.get_text())

        text = "\n".join(extracted_text).strip()

        if not text:
            return None, (
                "No readable text found. "
                "This PDF may be scanned and require OCR."
            )

        return text, None

    except Exception:
        return None, (
            "Could not read this PDF. "
            "Please upload a valid PDF CV."
        )
