import streamlit as st
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import easyocr
import os
import google.generativeai as genai
import json

# Maximum number of pages to process
MAX = -1

def is_pdf_text_based(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            if page.extract_text():  # Check if text can be extracted
                return True
        return False
    except Exception as e:
        st.error(f"Error processing PDF: {e}")
        return False

def extract_text_from_text_based_pdf(pdf_path):
    pages = []
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        page_text = page.extract_text()
        pages.append(page_text)
    return pages

def extract_text_from_image_based_pdf(pdf_path, output_dir="output_images"):
    pages = []
    os.makedirs(output_dir, exist_ok=True)

    # Convert PDF pages to images
    pages = convert_from_path(pdf_path, dpi=300, first_page=8, last_page=10)
    reader = easyocr.Reader(['vi'])  # Initialize EasyOCR reader

    for page_number, page in enumerate(pages, start=1):
        st.write(f"Processing page {page_number}...")
        image_path = os.path.join(output_dir, f"page_{page_number}.jpg")
        page.save(image_path, "JPEG")  # Save image for debugging (optional)

        # Perform OCR
        ocr_result = reader.readtext(image_path)
        page_text = "\n".join([text[1] for text in ocr_result])
        pages.append(page_text)

    return pages

def extract_text_from_pdf(pdf_path):
    if is_pdf_text_based(pdf_path):
        st.write("The PDF is text-based. Extracting text...")
        return extract_text_from_text_based_pdf(pdf_path)
    else:
        st.write("The PDF is image-based. Performing OCR...")
        return extract_text_from_image_based_pdf(pdf_path)

def convert_text_to_json(pages_arr, model):
    pages = []
    for page_number, text in enumerate(pages_arr, start=1):
        if page_number< 0 or page_number > MAX:
            break
        table_row = """{ROLL.:0001,COLOR: 11, LENGTH: 82, +L: , CYL: 053/001, NET: 14.76,GROSS: 15.56}"""
        response = model.generate_content(f"format text to JSON file. Rolls array: {table_row} :{text}")
        result = response.text
        if result.startswith("```json"):
            start_index = result.find("```json") + 7
            end_index = result.rfind("```")
            json_text = json.loads(result[start_index:end_index])
        else:
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            json_text = {"lines": lines}
        pages.append(json_text)
    json_array = json.dumps({"pages": pages}, indent=4, ensure_ascii=False)
    return json_array

# Streamlit App
st.title("PDF to JSON with Generative AI")

# Input field for API key
api_key = st.text_input("Enter your Generative AI API Key", type="password")

if api_key:
    try:
        # Configure Generative AI
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

        if uploaded_file is not None:
            # Save the uploaded file temporarily
            temp_pdf_path = "uploaded_file.pdf"
            with open(temp_pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.write("Processing the uploaded PDF...")

            # Extract text from the PDF
            pages_arr = extract_text_from_pdf(temp_pdf_path)

            # Generate JSON from extracted text using Generative AI
            st.write("Generating JSON format...")
            json_text = convert_text_to_json(pages_arr, model)

            # Display the JSON response
            st.subheader("Generated JSON Response")
            # Provide a download option for the JSON
            st.download_button(
                label="Download JSON",
                data=json_text,
                file_name="output.json",
                mime="application/json"
            )
            st.code(json_text, language="json")

          
    except Exception as e:
        st.error(f"Error configuring Generative AI: {e}")
else:
    st.warning("Please enter your API key to continue.")
