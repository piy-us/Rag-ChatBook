from flask import Flask, request, jsonify, render_template
from data_loader import load_documents
from embeddings import generate_embeddings
from search import build_vector_store, build_index

from chat_engine import create_chat_engine, get_chat_response
from flask import Flask, render_template, request, jsonify, redirect, url_for
import os  # For file path manipulation
import OCR_with_mouse_drag
# pdfpath="D:/OCR-on-Image-ROI-with-Tesseract/ocr6/uploads/"
# textpath='D:/Chatebook/chatbotcopy4/textpdf/'
# summarypath="D:/OCR-on-Image-ROI-with-Tesseract/ocr6/summarypath/"
# output_folder = "D:/OCR-on-Image-ROI-with-Tesseract/ocr6/static/converted_images/"
pageno=0
filen=''
book_name=''
author_name=''

app = Flask(__name__)

# Load documents and prepare chat engine once at the start
file_path = "D://Rag ChatBook//_OceanofPDF.com_The_Alchemist.pdf"
documents = load_documents(file_path)
nodes = generate_embeddings(documents)
vector_store = build_vector_store(nodes)
index = build_index(vector_store,1)
chat_engine = create_chat_engine(index)



@app.route('/')
def home():
    return render_template('page_two.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    query = data.get('message')
    response = get_chat_response(chat_engine, query)

    # Convert the response to a JSON-serializable format
    response_text = response.response  # Assuming 'response' has a 'response' attribute with the text

    return jsonify({'answer': response_text})

@app.post("/coordinate")
def getocr():
    try:
        coordinates = request.get_json()
        print(coordinates)
    except Exception as e:
        return jsonify({"error": f"Invalid request format: {e}"}), 400
    try:
        response = OCR_with_mouse_drag.get_coor(*coordinates)  # Unpack coordinates
        print(response)
    except Exception as e:
        return jsonify({"error": f"Error during OCR processing: {e}"}), 500

  # Return OCR text in JSON response
    return jsonify({"answer": response})

@app.get("/<int:page_number>")
def get_page_num(page_number):
    # Construct the file path based on the page number
    #file_path = os.path.join(text_files_dir, f"page{page_number}.txt")
    print(f'Current page received: {page_number}')
    index = build_index(vector_store,page_number)
    chat_engine = create_chat_engine(index)

    #file_path = os.path.join(textpath, f"{filen}{page_number}.txt")
    #file_path = os.path.join(summarypath, f"{page_number}.txt")
    #print(file_path)
    #summar=summariser.summary(file_path)
    #print(file_path)
    return jsonify({"answer": "received"})

if __name__ == "__main__":
    app.run(debug=True)
