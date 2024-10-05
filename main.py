from md_parse import get_list_of_users
from vector.chroma_handler import ChromaHandler
import faiss
from bertopic import BERTopic
from umap import UMAP


path = "pkms"

all_users = get_list_of_users(path)
all_vectors = []

for user in all_users:
    chunks = user.all_chunks
    db_handler = ChromaHandler(f"../vector_tings4", "test-strings-1")
    texts = [str(chunk[1]) for chunk in chunks]
    ids = [str(chunk[0]) for chunk in chunks]
    if not texts or ids:
        continue
    """
    db_handler.add_docs_with_embeddings(
        texts,
        ids
    )
    """
    all_vectors.extend(db_handler.get_text_embeddings(texts))


