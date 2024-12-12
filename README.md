# PDF to JSON with Generative AI

This application processes PDF files, extracts text (from both text-based and image-based PDFs), and converts the extracted content into JSON format using a Generative AI model (Gemini-1.5-flash).

## Features

- Detects whether a PDF is text-based or image-based.
- Extracts text using PyPDF2 for text-based PDFs and EasyOCR for image-based PDFs.
- Formats the extracted text into a JSON structure using Generative AI.
- Provides a downloadable JSON output.

## Prerequisites

- Python 3.8 or higher

## Installation

1. Clone the repository or download the source code.

   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Install the required dependencies.
   ```bash
   pip install -r requirements.txt
   ```

## Required Libraries

The application requires the following Python libraries:

- Streamlit
- PyPDF2
- pdf2image
- easyocr
- google-generativeai
- pillow
- json

Install these dependencies using:

```bash
pip install streamlit PyPDF2 pdf2image easyocr google-generativeai pillow
```

## Configuration

### Getting a Gemini API Key

1. Sign up or log in to the Generative AI provider's platform.
2. Navigate to the API section and create a new API key.
3. Copy the API key for use in the application.

### Additional Setup

- For image-based PDF processing, `poppler-utils` must be installed on your system.
  - On Ubuntu/Debian:
    ```bash
    sudo apt-get install poppler-utils
    ```
  - On MacOS (with Homebrew):
    ```bash
    brew install poppler
    ```

## Running the Application Locally

1. Start the Streamlit application.
   ```bash
   streamlit run app.py
   ```
2. Open the displayed local URL (e.g., `http://localhost:8501`) in your browser.

## Usage Instructions

1. Enter your Gemini AI API Key in the input field.
2. Upload a PDF file.
3. Wait while the application processes the file.
4. View the extracted JSON output in the app.
5. Download the JSON file using the "Download JSON" button.

## Notes

- The application processes up to one page by default (customizable with the `MAX` variable).
- Ensure the API key has sufficient permissions to call the Generative AI service.
- For large or complex PDFs, processing time may vary.

## Contributing

Feel free to submit issues or feature requests via GitHub. Contributions are welcome!

## License

This project is licensed under the MIT License.
