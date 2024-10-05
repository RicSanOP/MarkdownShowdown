import chromadb
import os
from mistralai import Mistral


class ChromaHandler:

    def __init__(self, db_path, collection_name):
        self.mistral_client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
        self.client = chromadb.PersistentClient(path=db_path)
        self.change_collection(collection_name)
        # self.collection = self.client.get_collection(name=collection_name)

    def change_collection(self, collection_name):
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
        )

    def add_docs_default(self, documents, ids):
        self.collection.upsert(
            documents=documents,
            ids=ids,
        )

    def get_text_embeddings(self, sentences):
        embeddings_resp = self.mistral_client.embeddings.create(
            model="mistral-embed", inputs=sentences
        )
        embeddings = [
            string_embedding.embedding for string_embedding in embeddings_resp.data
        ]
        return embeddings

    def add_docs_with_embeddings(self, docs, ids):
        embeddings = self.get_text_embeddings(docs)
        self.collection.add(
            documents=docs, embeddings=embeddings, ids=ids
        )  # chroma will not embed this

    def query_collection(self, query_texts, n, use_mistral=True):
        if use_mistral:
            embeddings = self.get_text_embeddings(query_texts)
            query_response = self.collection.query(
                query_embeddings=embeddings,
                n_results=n,
            )
        else:
            query_response = self.collection.query(
                query_texts=query_texts,  # chroma will embed this
                n_results=n,
            )

        # taking out embeddings, metadata etc
        response = {
            "docs": query_response["documents"][0],
            "ids": query_response["ids"][0],
        }  # these are 2d for some reason
        return response


if __name__ == "__main__":
    db_handler = ChromaHandler("../../vector_collections", "test-strings-2")
    db_handler.add_docs_with_embeddings(
        ["some good text", "some bad text"], ["id1", "id2"]
    )
    print(db_handler.query_collection("good text", 1))
