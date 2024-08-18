from llama_index.core.memory import ChatMemoryBuffer
from search import build_index

memory = ChatMemoryBuffer.from_defaults(token_limit=4000)

def create_chat_engine(index):
    #memory = ChatMemoryBuffer.from_defaults(token_limit=4000)
    global memory
    chat_engine = index.as_chat_engine(
        chat_mode="condense_plus_context",
        memory=memory,
        context_prompt=(
            "You are a chatbot integrated with an ebook reader, able to have normal interactions on any topic, as well as talk about the book. "
            "Your primary task is to assist the user based on the content of the book they have read up to this point. "
            "Do not provide any information, plot points, or details beyond the pages the user has already read. "
            "if user is asking something beyond the scope of the book, then you can provide the information."
            "Use concepts, quotes, and details strictly from the provided context and avoid relying on your pre-trained knowledge base. "
            "Here are the relevant documents for the context:\n"
            "{context_str}"
            "\nInstruction: Use the previous chat history or the context above to interact and help the user. "
            "Do not reference or infer any content that is beyond the scope of the provided documents. "
            "Always include direct quotes from the book where relevant."
        ),
        verbose=False
    )
    return chat_engine

def get_chat_response(chat_engine, query):
    response = chat_engine.chat(query)
    return response

