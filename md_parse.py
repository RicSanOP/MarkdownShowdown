import base64
import os
import pathlib
import re

import obsidiantools.api as otools
from bs4 import BeautifulSoup
from mistralai import Mistral
from openai import OpenAI


mistral = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
)

openai = OpenAI()


class ImageProcessor:

    @staticmethod
    def encode_image(image_path):
        """Encode the image to base64."""
        try:
            with open(image_path, "rb") as image_file:
                img_file = image_file.read()
                return base64.b64encode(img_file).decode("utf-8")
        except FileNotFoundError:
            print(f"Error: The file {image_path} was not found.")
            return None
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_image_description(image_path):

        base64_image = ImageProcessor.encode_image(image_path)
        # model = "pixtral-12b-2409"

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe this image",  # TODO: prompt engineer this
                    },
                    {
                        "type": "image_url",
                        "image_url": f"data:image/png;base64,{base64_image}",
                    },
                ],
            }
        ]
        
        return image_path
        
        chat_response = mistral.chat.complete(
            model="pixtral-12b-2409", messages=messages, max_tokens=200
        )

        return chat_response.choices[0].message.content

    @staticmethod
    def replace_images_with_desc(markdown_string, vault_path):
        # regex pattern to match ![[name]] where "name" is the image name
        pattern = r"!\[\[([^\]]+)\]\]"

        image_names = re.findall(pattern, markdown_string)

        # Replace each instance of ![[name]] with its description
        for image_name in image_names:
            image_path = f"{vault_path}/attachments/{image_name}"
            description = ImageProcessor.get_image_description(image_path)
            markdown_string = markdown_string.replace(
                f"![[{image_name}]]", f"IMAGE:{image_path}- {description}"
            )

        return markdown_string

def query_openai(text, model, max_tokens=10000):
    return openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": text}
        ]
    ).choices[0].message.content

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


class Note:
    markdown: str
    vault_path: str
    rel_path: str
    title: str
    user: str

    NUM_CHARS_PER_CHUNK = 800

    def generate_vector_db_inputs(self):
        # generate a list of inputs for the vector db by prompting an LLM and then splitting greedily where needed
        prompt = f"""
        We are trying to split the following markdown content into distinct chunks of markdown that are each less than {Note.NUM_CHARS_PER_CHUNK} characters long.
        Each chunk should be a complete idea and we want to split it as best as possible.
        Please output chunks using the <chunk> and </chunk> tags and leave the content as unchanged as possible. Make sure each image is in it's own chunk.

        At the top of each chunk you must always include a <info> </info> tag with a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk. Answer only with the succinct context and nothing else. 

        The input document is: {self.markdown}

        Remember to include an <info> tag at the top of each chunk.

        For example: 
        <chunk> <info> </info> </chunk>
        """
        # print(prompt)
        chunked_doc = query_openai(prompt, "mistral-large-latest", 120000)
        soup = BeautifulSoup(chunked_doc)
        # print(chunked_doc)

        # create list of chunks by splitting using the <chunk> and </chunk> tags
        chunks = soup.find_all("chunk")
        # print(chunks)

        for chunk in chunks:
            info_chunk = chunk.find("info")
            if info_chunk is None:
                info_chunk = soup.new_tag("info")
                chunk.insert(0, info_chunk)
            if not info_chunk.string:
                info_chunk.string = ""

            info_chunk.string += (
                "\nNote Path: " + str(self.rel_path) + "\nAuthor: " + str(self.user)
            )

            # iterate through chunks and prompt for a succinct context if it is greater than 1000 characters
            # for chunk in chunks:
            if len(chunk) > 1000:
                prompt = f"""The following chunk is too long: {chunk}
                Please shorten it to less characters and output the shortened version.
                """
                shortened_chunk = query_openai(prompt, "mistral-small-latest", max_tokens=300)
                chunk.string = shortened_chunk.find("chunk").string[0:1000]
            chunk.string = ImageProcessor.replace_images_with_desc(
                str(chunk), self.vault_path
            )

        output_tuples = []

        for chunk_id, chunk in enumerate(chunks):
            chunk_text = chunk
            uid = f"{str(self.rel_path)}_{str(chunk_id)}"
            output_tuples.append((uid, chunk_text))

        return output_tuples

    def __init__(self, title, rel_path, markdown, vault_path, user):
        self.title = title
        self.vault_path = vault_path
        self.user = user
        self.markdown = markdown
        self.rel_path = rel_path
        self.vector_db_inputs = self.generate_vector_db_inputs()


class Vault:
    vault_path: str
    notes: list
    user: str
    all_chunks: list

    def load_notes(self):
        path = pathlib.Path(self.vault_path)
        vault = otools.Vault(path).connect().gather()
        notes_list = vault.md_file_index
        for note_title, rel_path in notes_list.items():
            if not rel_path:
                continue
            markdown = vault.get_source_text(note_title)
            print("Procesing note: ", note_title)
            created_note = Note(
                note_title,
                rel_path,
                markdown,
                self.vault_path,
                self.user,
            )
            self.notes.append(created_note)
            self.all_chunks.extend(created_note.vector_db_inputs)

    def __init__(self, user, vault_path):
        self.vault_path = vault_path
        self.all_chunks = []
        self.user = user
        self.notes = []
        self.all_chunks = []
        self.load_notes()


def get_list_of_users(team_path):
    users = []
    for user_path in os.listdir(team_path):
        user_vault = Vault(user_path, os.path.join(team_path, user_path))
        users.append(user_vault)
    return users
