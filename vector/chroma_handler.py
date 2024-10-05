import chromadb


class ChromaHandler:

    def __init__(self, db_path, collection_name):
        self.client = chromadb.PersistentClient(path=db_path)
        self.change_collection(collection_name)

    def change_collection(self, collection_name):
        # self.collection = self.client.get_collection(name=collection_name)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_docs(self, documents, ids):
        self.collection.upsert(
            documents=documents,
            ids=ids,
        )

    def query_collection(self, query_texts, n):
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
    db_handler = ChromaHandler("../../vector_collections", "test-strings")
    result = db_handler.query_collection(["some query"], 2)
    print(result)
