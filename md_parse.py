
import os
import mistletoe
import obsidiantools.api as otools
import pathlib
from bs4 import BeautifulSoup
from mistralai import Mistral
import os

mistral = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
)


def query(text, max_tokens=10000):
    return mistral.chat.complete(model="mistral-large-latest", 
        max_tokens=max_tokens,
        messages=[
        {
            "content": text,
            "role": "system",
        },
    ])

class Note:
    markdown: str
    vault_path: str
    links: list
    title: str
    user: str

    NUM_CHARS_PER_CHUNK = 800
    
    def generate_vector_db_inputs(self):
        # generate a list of inputs for the vector db by prompting an LLM and then splitting greedily where needed
        prompt = f"""
        We are trying to split the following note into distinct chunks of text that are each less than {Note.NUM_CHARS_PER_CHUNK} characters long.
        Each chunk should be a complete idea and we want to split it as best as possible.
        Please output chunks using the <chunk> and </chunk> tags.
        At the top of each chunk include a <info> </info> tag with a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk. Answer only with the succinct context and nothing else. 
        The input document is: {self.markdown}
        """
        chunked_doc = query(prompt, 120000)
        soup = BeautifulSoup(chunked_doc)

        # create list of chunks by splitting using the <chunk> and </chunk> tags
        chunks = chunked_doc.find_all("chunk")

        for chunk in chunks:
            info_chunk = chunk.find("<info>")
            link_prompt = f"""Use the following document as context:  {self.markdown}
            We are dealing with the following chunk: {chunk}
            Please output a maximum of 3 forward links and 3 backward links that are relevant to this chunk in the following format:
            <forward_links> </forward_links>
            <backward_links> </backward_links>
            Do not output anything else and if there are no relevant links, output an empty string in the tags.
            """
            links = query(link_prompt, 150)
            info_chunk.string += links

        # iterate through chunks and prompt for a succinct context if it is greater than 1000 characters
        for chunk in chunks:
            if len(chunk) > 1000:
                prompt = f"""The following chunk is too long: {chunk}
                Please shorten it to less characters and output the shortened version.
                """
                shortened_chunk = query(prompt, max_tokens=300)
                chunk.string = shortened_chunk.find("chunk").string[0:1000]
        return chunks

class Vault:
    vault_path: str
    notes: list
    user: str

    def load_notes(self):
        path = pathlib.Path(self.vault_path)
        vault = otools.Vault(path).connect().gather()
        notes_list = vault.md_file_index
        for note_title, rel_path in notes_list.items():
            back_links = vault.get_backlinks(note_title)
            forward_links = vault.get_md_links(note_title)
            self.notes.append(Note(note_title, rel_path, self.vault_path, forward_links, back_links))

    def __init__(self, vault_path):
        self.vault_path = vault_path
        self.notes = []
        self.load_notes()


def get_list_of_users(team_path):
    users = []
    for user in os.listdir(team_path):
        users.append(user)
    return users



