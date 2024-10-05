from md_parse import get_list_of_users
from bertopic import BERTopic
from umap import UMAP
from mistralai import Mistral
import os
from hdbscan import HDBSCAN
from vector.chroma_handler import ChromaHandler



path = "pkms"

all_users = get_list_of_users(path)
all_vectors = []
all_texts = []

mistral = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
)

def query(text, model, max_tokens=10000):
    return mistral.chat.complete(model=model, 
        max_tokens=max_tokens,
        messages=[
        {
            "content": text,
            "role": "system",
        },
    ]).choices[0].message.content


def get_text_embeddings(sentences):
    embeddings_resp = mistral.embeddings.create(
        model="mistral-embed", inputs=sentences
    )
    embeddings = [
        string_embedding.embedding for string_embedding in embeddings_resp.data
    ]
    return embeddings

db_handler = ChromaHandler(f"../vector_tings4", "test-strings-2")

for user in all_users:
    chunks = user.all_chunks
    texts = [str(chunk[1]) for chunk in chunks]

    for i in range(0, len(texts)):
        texts[i] = texts[i].replace("<chunk>", "").replace("</chunk>", "").replace("<info>", "").replace("</info>", "")

    ids = [str(chunk[0]) for chunk in chunks]

    if not texts or not ids:
        continue
    all_tags = []

    for text in texts:
        classification_prompt = f"""
        We are trying to tag the following markdown content from our notebase according to the following tags. Each content can have one or more tags.
        
        The tags are described as follows:
        Task Management Notes
        Task Management Notes are markdown files containing information on actions that the author has taken in the past, is currently undertaking and/or will take in the future. Task Management Notes can take on many different styles such as:

        a devlog where the author describes what they have done in a journaling writing style which includes self reflections on their work
        a checklist where the author determines what they have to do and check off items when completed
        a table containing tasks on each row along with metadata on the team member responsible, the task priority, expected deadline and/or task priority
        Project Documentation Notes
        Project Documentation Notes are markdown files containing information on the project deliverable itself. These notes usually focus on a specific part of the project. They could focus on software aspect by describing the architecture of a software module, outlining the code structure of a class or function or listing the dependencies of a codebase. Project documentation could also discuss machine learning processes such as results of model training, provide reasons for how learning models are architected or comment on the performance of a model during evaluation.

        Knowledge Database Notes
        Knowledge Database Notes are markdown files containing information that is meant to educate on the problem space. These are more independent from the project's development and are meant to assist the author in better understanding the problem they are trying to solve. The hope is that some of this knowledge can come in handy when justifying current approaches in the project and/or offer solutions to future potential problems.

        Please output the tag(s) as follows: tags: [tag1, tag2, tag3] where the tag options are task, project, knowledge. Each piece of content has one or more tags.

        Example Output:
        tags: [task, project]

        Input Content for Classification: {text}
        """
        tags_txt = query(classification_prompt, "mistral-large-latest", 100)
        tags = {"task": False, "project": False, "knowledge": False}

        if "task" in tags_txt:
            tags["task"] = True
        if "project" in tags_txt:
            tags["project"] = True
        if "knowledge" in tags_txt:
            tags["knowledge"] = True

        all_tags.append(tags)
    
    db_handler.add_docs_with_embeddings(
        texts,
        ids, 
        all_tags
    )
    all_vectors.extend(db_handler.get_text_embeddings(texts))
    all_texts.extend(texts)

import IPython
IPython.embed()

umap_model = UMAP(n_neighbors=3, n_components=5, min_dist=0.0, metric='cosine')
hdbscan_model = HDBSCAN(min_samples=3, gen_min_span_tree=True, prediction_data=True, min_cluster_size=3)
topic_model = BERTopic(umap_model=umap_model, hdbscan_model=hdbscan_model)
matrix, _ = topic_model.fit_transform(all_texts)

for topic in topic_model.get_topics():
    print("Topic: ", topic)
    for i in range(len(matrix)):
        if matrix[i] == topic:
            print(all_texts[i])
