from data_loader import load_documents
from embeddings import generate_embeddings
from search import build_vector_store, build_index, query_index
from chat_engine import create_chat_engine, get_chat_response

def main():
    file_path = "D://Rag ChatBook//_OceanofPDF.com_The_Alchemist.pdf"
    documents = load_documents(file_path)
    nodes = generate_embeddings(documents)
    vector_store = build_vector_store(nodes)
    index = build_index(vector_store)
    chat_engine = create_chat_engine(index)
    
    query = "What is the name and profession of the boy?"
    response = get_chat_response(chat_engine, query)
    print(response)
    while True:
        query = input("User: ")
        if query.lower() == "exit":
            break
        response = get_chat_response(chat_engine, query)
        print(f"Agent: {response}")

if __name__ == "__main__":
    main()
