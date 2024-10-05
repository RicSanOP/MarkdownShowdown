
import os
import obsidiantools.api as otools
import pathlib
from bs4 import BeautifulSoup
from mistralai import Mistral
import os

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

class Note:
    markdown: str
    vault_path: str
    rel_path: str
    forward_links: list
    backward_links: list
    title: str
    user: str

    NUM_CHARS_PER_CHUNK = 800
    
    def generate_vector_db_inputs(self):
        # generate a list of inputs for the vector db by prompting an LLM and then splitting greedily where needed
        prompt = f"""
        We are trying to split the following markdown content into distinct chunks of markdown that are each less than {Note.NUM_CHARS_PER_CHUNK} characters long.
        Each chunk should be a complete idea and we want to split it as best as possible.
        Please output chunks using the <chunk> and </chunk> tags and leave the content as unchanged as possible.
        
        At the top of each chunk you must always include a <info> </info> tag with a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk. Answer only with the succinct context and nothing else. 

        The input document is: {self.markdown}

        Remember to include an <info> tag at the top of each chunk.

        For example: 
        <chunk> <info> </info> </chunk>
        """
        chunked_doc = query(prompt, "mistral-large-latest", 120000)
        soup = BeautifulSoup(chunked_doc)

        # create list of chunks by splitting using the <chunk> and </chunk> tags
        chunks = soup.find_all("chunk")

        for chunk in chunks:
            print("Processing chunk # ", chunks.index(chunk))
            info_chunk = chunk.find("info")
            if info_chunk is None:
                info_chunk = soup.new_tag("info")
                chunk.insert(0, info_chunk)
            if not info_chunk.string:
                info_chunk.string = ""

            nl = "\n"
            links_text = ""
            if self.forward_links or self.backward_links:
                link_prompt = f"""We are dealing with the following chunk: {chunk}
                Please output a maximum of 3 forward links and 3 back links that are relevant to this chunk in the following format:
                <forward_links> </forward_links>
                <backlinks> </backlinks>
                Do not output anything else and if there are no relevant links, output an empty string in the tags.

                Forward Links to consider: {nl.join(self.forward_links)}
                Backward Links to consider: {nl.join(self.backward_links)}"""
                links_text = query(link_prompt, "mistral-large-latest", 150)
                print("LINKS: ", links_text)
            if links_text:
                print("LINKS: ", links_text)
                info_chunk.string += links_text 
            info_chunk.string += "\nAuthor: " + self.user
            info_chunk.string += "\nRelative Path: " + str(self.rel_path)

        # iterate through chunks and prompt for a succinct context if it is greater than 1000 characters
        for chunk in chunks:
            if len(chunk) > 1000:
                prompt = f"""The following chunk is too long: {chunk}
                Please shorten it to less characters and output the shortened version.
                """
                shortened_chunk = query(prompt, "mistral-large-latest", max_tokens=300)
                chunk.string = shortened_chunk.find("chunk").string[0:1000]
        
        output_tuples = []

        for chunk_id, chunk in enumerate(chunks):
            chunk_text = chunk  
            uid = f"{str(self.rel_path)}_{str(chunk_id)}"
            output_tuples.append((uid, chunk_text))

        return output_tuples

    def __init__(self, title, rel_path, markdown, vault_path, forward_links, back_links, user):
        self.title = title
        self.vault_path = vault_path
        self.user = user
        self.markdown = markdown
        self.rel_path = rel_path
        self.forward_links = forward_links
        self.backward_links = back_links
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
            back_links = vault.get_backlinks(note_title)
            forward_links = vault.get_wikilinks(note_title)
            markdown = vault.get_source_text(note_title)
            print("Procesing note: ", note_title)
            created_note = Note(note_title, rel_path, markdown, self.vault_path, forward_links, back_links, self.user)
            self.notes.append(created_note)
            self.all_chunks.extend(created_note.vector_db_inputs)
            

    def __init__(self, user, vault_path):
        self.vault_path = vault_path
        self.user = user
        self.notes = []
        self.load_notes()


def get_list_of_users(team_path):
    users = []
    for user_path in os.listdir(team_path):
        user_vault = Vault(user_path, os.path.join(team_path, user_path))
        users.append(user_vault)
    return users



