from flask import render_template, Response
import logging
import pdfkit
import os
import platform

# Import your HTML renderers
from .html_renderer import render_html_resume
from .cv_renderer import cv_render

logger = logging.getLogger(__name__)


if platform.system() == 'Windows':
    path_wkhtmltopdf = r'D:\software installations data\wkhtmltopdf\bin\wkhtmltopdf.exe' # Adjust if needed
else:
    path_wkhtmltopdf = os.path.join(os.getcwd(), 'bin', 'wkhtmltopdf') # For Render/Linux

if not os.path.exists(path_wkhtmltopdf):
    print(f"ERROR: wkhtmltopdf executable not found at: {path_wkhtmltopdf}")
    config = None
else:
    print(f"Using wkhtmltopdf at: {path_wkhtmltopdf}")
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)



def download_pdf_document(mongo, doc_type, username, template):
    """
    Generates and serves a resume or CV as a PDF file using pdfkit.

    Args:
        mongo: The Flask-PyMongo instance.
        doc_type (str): The type of document ('resume' or 'cv').
        username (str): The username of the user.
        template (str): The HTML template file to use.

    Returns:
        Flask Response object with PDF data or an error tuple.
    """
    if config is None:
        logger.error("wkhtmltopdf configuration error: Executable not found or path incorrect.")
        return ("<h1>Configuration Error</h1>"
                "<p>wkhtmltopdf path configured does not exist or is incorrect. PDF generation unavailable.</p>"), 500

    try:
        # 1. Render the appropriate HTML based on doc_type
        html_string_or_error = None
        if doc_type == 'resume':
            html_string_or_error = render_html_resume(mongo, username=username, template=template)
        elif doc_type == 'cv':
            html_string_or_error = cv_render(mongo, username=username, template=template)
        else:
            return f"Invalid document type: {doc_type}. Use 'resume' or 'cv'.", 400

        # Check if the renderer returned an error (like user not found)
        if isinstance(html_string_or_error, tuple):
            # Propagate the error message and status code from the renderer
            return html_string_or_error
        elif not isinstance(html_string_or_error, str):
             # Should be a string if successful
             logger.error(f"HTML renderer for {doc_type} did not return a string.")
             return "<h1>Internal Server Error</h1><p>Failed to render HTML content.</p>", 500

        html_string = html_string_or_error # It's a valid HTML string now

        # 2. Define PDF generation options
        options = {
            'page-size': 'Letter',
            'margin-top': '0.5in',
            'margin-right': '0.5in',
            'margin-bottom': '0.5in',
            'margin-left': '0.5in',
            'encoding': "UTF-8",
            'enable-local-file-access': None, # Important if CSS/images are local
            'no-outline': None
        }

        # 3. Generate PDF bytes using pdfkit
        pdf_bytes = pdfkit.from_string(
            html_string,
            output_path=False,  # Generate in memory
            options=options,
            configuration=config
        )

        # 4. Create the Flask Response
        response = Response(pdf_bytes)
        response.headers['Content-Type'] = 'application/pdf'
        # Make filename dynamic
        safe_username = "".join(c if c.isalnum() else "_" for c in username) # Basic sanitization
        filename = f"{safe_username}_{doc_type}.pdf"
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response

    except FileNotFoundError as e:
        # Specific error if wkhtmltopdf execution fails (e.g., permissions)
        logger.error(f"wkhtmltopdf execution error: {e}")
        # Check if the error message points to wkhtmltopdf specifically
        if 'wkhtmltopdf' in str(e):
             return (f"<h1>Error Generating PDF</h1>"
                     f"<p>Failed to execute wkhtmltopdf. Please check server logs and configuration.</p>"
                     f"<p>Details: {str(e)}</p>"), 500
        else:
             # Handle other potential FileNotFoundError during rendering (less likely here)
             return (f"<h1>Error Generating PDF</h1><p>A required file was not found: {str(e)}</p>"), 500
    except Exception as e:
        # Catch other potential errors during PDF generation
        logger.exception(f"Unexpected PDF generation error for {doc_type} ({username}): {e}") # Use logger.exception to include traceback
        return (f"<h1>Error Generating PDF</h1><p>An unexpected error occurred: {str(e)}</p>"), 500