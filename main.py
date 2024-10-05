from md_parse import get_list_of_users
from vector.chroma_handler import ChromaHandler
import faiss
from bertopic import BERTopic
from umap import UMAP


db_handler = ChromaHandler(f"../vector_tings5", "test-strings-1")
# db_handler.add_docs_with_embeddings(["ligma1", "more ligma"], ["id1", "id2"])


if True:
    path = "pkms"
    all_users = get_list_of_users(path)

    for user in all_users:
        chunks = user.all_chunks
        # print(chunks)
        # exit()

        texts = [str(chunk[1]) for chunk in chunks]
        ids = [str(chunk[0]) for chunk in chunks]
        if not texts or not ids:
            continue
        db_handler.add_docs_with_embeddings(texts, ids)
else:
    print(db_handler.collection.peek())
    print(db_handler.query_collection(["project"], 5))

# print(db_handler.collection.peek())
# print(db_handler.query_collection(["project"], 5))
