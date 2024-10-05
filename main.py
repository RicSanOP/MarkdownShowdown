from md_parse import get_list_of_users
from vector.chroma_handler import ChromaHandler

path = "pkms"

all_users = get_list_of_users(path)

for user in all_users:
    chunks = user.all_chunks
    db_handler = ChromaHandler(f"", "test-strings-2")
    db_handler.add_docs_with_embeddings(
        [chunk[1] for chunk in chunks],
        [chunk[0] for chunk in chunks]        
    )

