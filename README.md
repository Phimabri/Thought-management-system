# Thought Manager

This project is a **Thought Management System** that allows users to **store, search, and delete their personal thoughts** using machine learning models. The project leverages **Faiss** for vector similarity search, **Sentence Transformers** for text embeddings, and a **Tkinter GUI** for user interaction.

## Features

1. **Add Thoughts**: 
   - Users can input their thoughts via a simple dialog box.
   - Thoughts are embedded using the `CamemBERT` model from the `sentence-transformers` library.
   - The embeddings are stored in a Faiss index to enable fast and efficient similarity search.
   - The actual text of the thoughts is stored in a `JSON` file (`thoughts_texts.json`).

2. **Delete Thoughts**:
   - Users can view all stored thoughts in a scrollable window.
   - Thoughts can be deleted by entering their corresponding number.
   - The system automatically updates both the Faiss index and the `JSON` file to reflect the deletion.

3. **Retrieve Thoughts**:
   - Users can retrieve the thoughts most similar to a given question or topic.
   - The retrieval is based on the vector similarity between the query and stored thoughts using Faiss.
