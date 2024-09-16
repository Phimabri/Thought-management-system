import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
import os
import json

import tkinter as tk
from tkinter import simpledialog, messagebox

# Function to retrieve a thought based on the vector
def get_thought(question, k):
    # Get the Faiss index
    faiss_index = faiss.read_index("./thoughts.index")

    # Search the index
    D, I = faiss_index.search(question, k)

    # Load the text list
    with open("thoughts_texts.json", "r", encoding="utf-8") as f:
        thoughts_texts = json.load(f)

    # Retrieve the corresponding text
    thought_list = []
    for i in range(k):
        thought_list.append(thoughts_texts[I[0][i]-1])
    return thought_list

def read_thoughts():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Get user input for the topic
    text = simpledialog.askstring("Input", "Veuillez entrer votre sujet:")
    if text is None:
        return  # User cancelled

    # Get user input for the number of thoughts
    k = simpledialog.askinteger("Input", "À combien de pensées souhaitez-vous accéder?", minvalue=1)
    if k is None:
        return  # User cancelled

    # Load the Faiss index
    index = faiss.read_index("./thoughts.index")

    # Initialize the Sentence Transformer model
    model = SentenceTransformer("dangvantuan/sentence-camembert-large")

    # Encode the question
    question_embedding = model.encode(text).reshape(1, -1)

    # Get the thoughts
    message_thought = get_thought(question_embedding, k)

    # Display the thoughts in a message box
    thoughts_message = "\n\n".join(message_thought)
    messagebox.showinfo("Thoughts", thoughts_message)

if __name__ == "__main__":
    read_thoughts()



read_thoughts()
