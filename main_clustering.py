import itertools
import json
import os
import re
from collections import defaultdict

from bertopic import BERTopic
from hdbscan import HDBSCAN
from mistralai import Mistral
from umap import UMAP

from md_parse import get_list_of_users
from openai import OpenAI

import sys

#path = "pkms"
path = "toy/inputs"

all_vectors = []
all_texts = []
all_tags = []


mistral = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
)

openai = OpenAI()


def query(text, model, max_tokens=10000):
    return (
        mistral.chat.complete(
            model=model,
            max_tokens=max_tokens,
            messages=[
                {
                    "content": text,
                    "role": "system",
                },
            ],
        )
        .choices[0]
        .message.content
    )
    
def query_openai(text, model, max_tokens=10000):
    return openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": text}
        ]
    ).choices[0].message.content


def query_json(text, model, max_tokens=10000):
    return (
        mistral.chat.complete(
            model=model,
            max_tokens=max_tokens,
            messages=[
                {
                    "content": text,
                    "role": "system",
                }
            ],
            response_format={"type": "json_object"},
        )
        .choices[0]
        .message.content
    )

def query_json_openai(text, model, max_tokens=10000):
    return openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": text}
        ],
        response_format={"type": "json_object"}
    ).choices[0].message.content
    
def query_json_openai_mini(text, model, max_tokens=10000):
    return openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": text}
        ],
        response_format={"type": "json_object"}
    ).choices[0].message.content

def get_text_embeddings(sentences):
    embeddings_resp = mistral.embeddings.create(model="mistral-embed", inputs=sentences)
    embeddings = [
        string_embedding.embedding for string_embedding in embeddings_resp.data
    ]
    return embeddings


def extract_img_path(text):
    pattern = r"IMAGE:([^-\n]+)-"
    match = re.search(pattern, text)
    # NOTE: expects "IMAGE:path/subpath- some more text"

    if match:
        path = match.group(1).strip()
        return path


# add system arg for speed mode

if sys.argv and len(sys.argv) > 1 and sys.argv[1] == "speed":
    all_texts = json.load(open("texts.json"))
    all_tags = json.load(open("tags.json"))
else:
    all_users = get_list_of_users(path)

    for user in all_users:
        chunks = user.all_chunks
        texts = [str(chunk[1]) for chunk in chunks]

        for i in range(0, len(texts)):
            texts[i] = (
                texts[i]
                .replace("<chunk>", "")
                .replace("</chunk>", "")
                .replace("<info>", "")
                .replace("</info>", "")
            )

        ids = [str(chunk[0]) for chunk in chunks]

        if not texts or not ids:
            continue
        tags_list = []

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
            tags_txt = query_openai(classification_prompt, "mistral-large-latest", 100)
            tags = {"task": False, "project": False, "knowledge": False}

            if "task" in tags_txt:
                tags["task"] = True
            if "project" in tags_txt:
                tags["project"] = True
            if "knowledge" in tags_txt:
                tags["knowledge"] = True
            img_path = extract_img_path(text)
            if img_path:
                tags["image"] = img_path
            tags_list.append(tags)
        
        """db_handler.add_docs_with_embeddings(
            texts,
            ids, 
            tags_list
        )
        all_vectors.extend(db_handler.get_text_embeddings(texts))"""
        all_texts.extend(texts)
        all_tags.extend(tags_list)


TAG_PROMPTS = {
    "task": """Task Management Notes
Task Management Notes are markdown files containing information on actions that the author has taken in the past, is currently undertaking and/or will take in the future. Task Management Notes can take on many different styles such as:
a devlog where the author describes what they have done in a journaling writing style which includes self reflections on their work
a checklist where the author determines what they have to do and check off items when completed
a table containing tasks on each row along with metadata on the team member responsible, the task priority, expected deadline and/or task priority""",
    "project": """Project Documentation Notes
Project Documentation Notes are markdown files containing information on the project deliverable itself. These notes usually focus on a specific part of the project. They could focus on software aspect by describing the architecture of a software module, outlining the code structure of a class or function or listing the dependencies of a codebase. Project documentation could also discuss machine learning processes such as results of model training, provide reasons for how learning models are architected or comment on the performance of a model during evaluation.""",
    "knowledge": """
    Knowledge Database Notes
    Knowledge Database Notes are markdown files containing information that is meant to educate on the problem space. These are more independent from the project's development and are meant to assist the author in better understanding the problem they are trying to solve. The hope is that some of this knowledge can come in handy when justifying current approaches in the project and/or offer solutions to future potential problems.
    """,
    "general": """
    We are a team working on an AI project together. As is common, we take notes to manage information pertaining to our jobs. Each team member is maintains their own notebase of markdown files which use wikilinks to link to each other. Various markdown editors leverage linking in markdown such as: - Obsidian - Dendron - LogSeq

    The fact that each team member has their own personal notebase has some advantages and disadvantages. While a team member has the freedom to draft markdown notes and structure the notebase in whichever way they see fit, they miss out on the potentially valuable information that exists within the notebases of their teammates. This means that a given team member can comfortably manage their tasks, draft project documentation and develop their personal knowledge database without concern for how they structure their writing and organize their markdown files, which may not suit the preferences of their teammates. However, there is a lack of a centralized notebase structure where the team can productively share and compare notes on project tasks, project documentation and knowledge on the problem domain.

    Therefore we need your help! You will help us merge our individual notebases into a unified, centralized and structured notebase. In general, here are the steps you will take:

    process our markdown files
    break them down into chunks
    tag our files and chunks based on their function
    cluster the tagged chunks and markdown files into new potential markdown file candidates
    suggest wikilink style links to connect the note files semantically
    draft the new notes taking into consideration the relevant markdown file contents
    """,
}

PROPER_TAG_NAMES = {
    "task": "Task Management Notes",
    "project": "Project Documentation Notes",
    "knowledge": "Knowledge Database Notes",
}


def get_note_blurb_json(chunks, tag_name):
    prompt = TAG_PROMPTS["general"]
    prompt += TAG_PROMPTS[tag_name]
    prompt += (
        f"""
    You are going to help us come up with a title for a new markdown note. When generating a title, strike a balance between suggesting a simple title and one that encompasses the information provided. We are going to provide you with a collection of markdown files and chunks that have tagged with the {PROPER_TAG_NAMES[tag_name]} note type and share a strong semantic similarity. Imagine that you are about to draft a new note containing all the information found in the provided markdown files and chunks. Please generate the following:

    - suggest a title for this new markdown note
    - justify why you have decided to go with this title
    - provide a one paragraph summary of its contents
    - mark down its type as {PROPER_TAG_NAMES[tag_name]} Feel free to provide references to the provided markdown files and chunks in your justification. Also make sure the summary covers as much information from the markdown files and chunks as possible. Please provide your answer in the following JSON format:
    """
        + """
    { title: "", justification: "", summary: "", type: "" }
    """
        + f"""
    You MUST only return the following JSON format and nothing else.
    
    Use the following chunks provided in a JSON list format:
    {json.dumps(chunks)}
    """
    )
    output_json = query_json_openai(prompt, "mistral-large-latest", 10000)
    output_json = json.loads(output_json)
    return output_json


all_notes_json_blurbs = {}

import IPython
IPython.embed()

for tag_name in ["task", "project", "knowledge"]:
    print("Clustering for tag: " + tag_name)
    tagged_texts = []
    for i in range(len(all_tags)):
        if all_tags[i][tag_name]:
            tagged_texts.append(all_texts[i])
    umap_model = UMAP(n_neighbors=5, n_components=5, min_dist=0.0, metric="cosine")
    hdbscan_model = HDBSCAN(
        min_samples=5, gen_min_span_tree=True, prediction_data=True, min_cluster_size=5
    )
    topic_model = BERTopic(umap_model=umap_model, hdbscan_model=hdbscan_model)
    matrix, _ = topic_model.fit_transform(all_texts)

    clusters = defaultdict(lambda: defaultdict(list))

    for i in range(len(matrix)):
        if "image" in all_tags[i]:
            clusters[matrix[i]]['image'].append({"description": all_tags[i]['image'], "path": all_tags[i]['image']})
        else:
            clusters[matrix[i]]['text'].append(all_texts[i])

    all_notes_json_blurbs[tag_name] = []

    for cluster in clusters:
        cluster_json = get_note_blurb_json(clusters[cluster]['text'], tag_name)
        cluster_json["chunks"] = clusters[cluster]['text']
        cluster_json["images"] = clusters[cluster]['image']
        all_notes_json_blurbs[tag_name].append(cluster_json)


def get_cluster_links(json_blurbs):
    from copy import deepcopy
    json_blurbs_copy = deepcopy(json_blurbs)
    # remove the chunks field from the json_blurbs_copy
    for tag_name in json_blurbs_copy:
        for note in json_blurbs_copy[tag_name]:
            note.pop("chunks", None)
    prompt = TAG_PROMPTS["general"]

    prompt += """
    You are going to help us find links between suggested markdown file candidates. Links show that there are unidirectional semantic connections between 2 notes. They can represent a multitude of things like:

    A parent-child relation where one note contains another
    A similarity relation between 2 notes
    An sibling relation where both notes link to each other
    We are going to provide you with a collection of candidates in the form of a JSON list. An example of the input JSON list can be found below (imagine that the empty strings below have been filled):

    [ { title: "A", justification: "", summary: "", type: "" }, { title: "B", justification: "", summary: "", type: "" }, { title: "C", justification: "", summary: "", type: "" } ]

    Please suggest semantic links between these notes in the form of a JSON list which identifies links as combinations of 2 titles. An example of the output JSON list can be found below:

    [ { title_from: "A", title_to: "B" }, { title_from: "A", title_to: "C" }, { title_from: "B", title_to: "C" }, ]}
    """

    prompt += f"""
    Use the following notes provided in a JSON list format:
    {json.dumps(list(itertools.chain(*(json_blurbs.values()))))}
    \n
    """

    prompt += """
    Please provide the links in the following JSON format:
    { [ { title_from: "", title_to: "" }, { title_from: "", title_to: "" }, { title_from: "", title_to: "" } ] }
    """

    output_json = query_json_openai_mini(prompt, "mistral-large-latest", 10000)
    output_json = json.loads(output_json)
    return output_json


def build_final_markdown(note_json, tag_name):
    prompt = TAG_PROMPTS["general"]
    prompt += "\n\n"
    prompt += TAG_PROMPTS[tag_name]
    prompt += (
        f"""
    You are going to draft a new markdown note within the parameters we provide. The new note will be a {PROPER_TAG_NAMES[tag_name]}. We are going to provide you with a JSON object containing the following format:
    """
        + """
    { title: "", chunks: [], links: [], summary: "", justification: "", images: [], }

    Here are some details on each field of the JSON object:

    title: the title and filename of the new markdown note which should be added to the top of the file using # header markdown syntax
    chunks: a list of chunks with content that can be revised into the new markdown note
    links: a list of titles to other markdown notes that must be included in the new markdown note (paste the provided title within sets of double square brackets [[ ]])
    summary: a summary of the new markdown note's contents which could add some further useful context
    justification: a justification for the content curation of the new markdown note which could add some further useful context
    images: a list of image filenames that must be embedded into the new note using the embed syntax ![[ ]] where the filename is inserted within the double square brackets
    """
        + f"""
    Here is the JSON object you will be working with for this note:
    f{json.dumps(note_json)}
    
    Remember that the output is markdown so please respect the syntax of the format.
    
    Do not include the justification in the output markdown and keep the note as organic as possible and similar to the style(s) of the input chunks.
    """
    )

    output_markdown = query_openai(prompt, "mistral-large-latest", 10000)
    return output_markdown


links = get_cluster_links(all_notes_json_blurbs)
all_notes_jsons = itertools.chain(*all_notes_json_blurbs.values())

if 'links' in links:
    links = links['links']
    
for link_data in links:
    for note in all_notes_jsons:
        if note["title"] == link_data["title_from"]:
            if "links" not in note:
                note["links"] = []
            note["links"].append(link_data["title_to"])

TAG_NAME_TO_FOLDER = {"task": "tasks", "project": "docs", "knowledge": "notes"}

from datetime import datetime

time_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

for tag_name in all_notes_json_blurbs:
    os.makedirs(
        "../outputs-" + time_str + f"/{TAG_NAME_TO_FOLDER[tag_name]}", exist_ok=True
    )
    for note_json in all_notes_json_blurbs[tag_name]:
        final_markdown = build_final_markdown(note_json, tag_name)
        with open(
            "../outputs-"
            + time_str
            + f"/{TAG_NAME_TO_FOLDER[tag_name]}/{note_json['title']}.md",
            "w",
        ) as f:
            f.write(final_markdown)
