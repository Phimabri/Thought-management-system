import json
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

# Function to add a thought
def add_thought():
    text = simpledialog.askstring("Input", "Veuillez entrer votre pensée:")
    if text is None or text.strip() == "":
        messagebox.showwarning("Input Error", "No thought entered!")
        return

    # Load the model
    model = SentenceTransformer("dangvantuan/sentence-camembert-large")

    # Encode the text
    embeddings = model.encode(text)
    size = embeddings.shape

    # Load the Faiss index
    index = faiss.read_index("./thoughts.index")

    # Add the embeddings to the index
    index.add(embeddings.reshape(1, size[0]))

    # Save the Faiss index
    faiss.write_index(index, "./thoughts.index")

    # Load the existing thoughts or initialize a new list if not present
    try:
        with open("thoughts_texts.json", "r", encoding="utf-8") as f:
            thoughts_texts = json.load(f)
    except FileNotFoundError:
        thoughts_texts = []

    # Append the new thought text to the list
    thoughts_texts.append(text)

    # Save the updated thoughts list
    with open("thoughts_texts.json", "w", encoding="utf-8") as f:
        json.dump(thoughts_texts, f, ensure_ascii=False, indent=4)

    messagebox.showinfo("Success", "Thought added successfully.")

# Function to delete a thought
def delete_thought():
    # Load the existing thoughts
    try:
        with open("thoughts_texts.json", "r", encoding="utf-8") as f:
            thoughts_texts = json.load(f)
    except FileNotFoundError:
        messagebox.showwarning("No Thoughts", "No thoughts found.")
        return

    # Create a window to display thoughts
    delete_window = tk.Toplevel()
    delete_window.title("Delete a Thought")
    delete_window.geometry("600x400")

    text_area = scrolledtext.ScrolledText(delete_window, wrap=tk.WORD, width=60, height=20, font=("Arial", 12))
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    for i, thought in enumerate(thoughts_texts):
        text_area.insert(tk.END, f"{i + 1}: {thought}\n\n")

    text_area.config(state=tk.DISABLED)

    def confirm_delete():
        try:
            num = int(entry.get()) - 1
            if num < 0 or num >= len(thoughts_texts):
                raise IndexError
        except (ValueError, IndexError):
            messagebox.showwarning("Input Error", "Invalid number.")
            return

        # Remove the thought from the list
        del thoughts_texts[num]

        # Save the updated thoughts list
        with open("thoughts_texts.json", "w", encoding="utf-8") as f:
            json.dump(thoughts_texts, f, ensure_ascii=False, indent=4)

        # Load the Faiss index
        index = faiss.read_index("./thoughts.index")

        # Create a new index without the removed embedding
        new_index = faiss.IndexFlatL2(index.d)

        # Get all embeddings from the current index
        embeddings = index.reconstruct_n(0, index.ntotal)

        # Remove the corresponding embedding
        embeddings = np.delete(embeddings, num, axis=0)

        # Add the remaining embeddings to the new index
        new_index.add(embeddings)

        # Save the updated Faiss index
        faiss.write_index(new_index, "./thoughts.index")

        messagebox.showinfo("Success", "Thought deleted successfully.")
        delete_window.destroy()

    entry_frame = tk.Frame(delete_window)
    entry_frame.pack(pady=10)

    tk.Label(entry_frame, text="Enter the number of the thought to delete:").pack(side=tk.LEFT, padx=10)
    entry = tk.Entry(entry_frame)
    entry.pack(side=tk.LEFT, padx=10)

    tk.Button(delete_window, text="Confirm Delete", command=confirm_delete).pack(pady=10)

# Main GUI
def main():
    root = tk.Tk()
    root.title("Thought Manager")
    root.geometry("300x200")

    tk.Button(root, text="Add Thought", command=add_thought, width=20).pack(pady=10)
    tk.Button(root, text="Delete Thought", command=delete_thought, width=20).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
