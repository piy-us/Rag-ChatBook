# import fitz

# pdffile = "D:\OCR-on-Image-ROI-with-Tesseract\extmoti.pdf"
# zoom = 5  # Adjust zoom level as needed (higher = sharper)
# mat = fitz.Matrix(zoom, zoom)

# doc = fitz.open(pdffile)
# page = doc.load_page(0)  # number of page

# # Render page at specified zoom level
# pix = page.get_pixmap(matrix=mat)
# output = "outfile.png"
# pix.save(output)
# doc.close()
import fitz
import os

def convert_pdf_to_images(pdf_path, output_folder,zoom=5):
  """
  Converts all pages in a PDF to images and saves them with sequential names.

  Args:
      pdf_path (str): Path to the PDF file.
      output_folder (str): Path to the folder where images will be saved.
      zoom (int, optional): Zoom level for the images (higher = sharper). Defaults to 5.
  """

  doc = fitz.open(pdf_path)
  num_pages = doc.page_count

  # Create output folder if it doesn't exist
  os.makedirs(output_folder, exist_ok=True)

  for page_number in range(num_pages):
    page = doc.load_page(page_number)
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
    output_filename = f"page{page_number + 1}.png"  # Start numbering from 1
    output_path = os.path.join(output_folder, output_filename)
    pix.save(output_path)

  doc.close()


  print(f"Converted {num_pages} pages from {pdf_path} to images in {output_folder}")
  #return num_pages

# Example Usage
pdf_path = "D://Rag ChatBook//_OceanofPDF.com_The_Alchemist.pdf"
output_folder = "static/converted_images"
convert_pdf_to_images(pdf_path, output_folder)
