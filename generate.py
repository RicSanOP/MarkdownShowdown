import os
import time
import shutil
import random
from tqdm import tqdm
from beepy import beep

def sync_notes(data):
    """syncing of notes"""
    print("Syncing team notes across multiple sources...")
    synced_notes = [note + "_synced" for note in data]
    time.sleep(2)  # Simulate time-consuming syncing
    print("Notes successfully synced.")
    return synced_notes

def merge_notes(data):
    """merging of notes"""
    print("Merging notes from different team members...")
    merged_notes = " ".join(data)
    time.sleep(1)
    return merged_notes

def generate_summary(merged_notes):
    """Fake summary generation"""
    summary = f"Summary: {merged_notes[:50]}..."  # Fake summary of the first 50 characters
    with open("summary.txt", "w") as f:
        f.write(summary)
    time.sleep(1)

def perform_cleanup():
    """cleanup after merging notes"""
    print("Cleaning up temporary data...")
    time.sleep(1)
    print("Temporary data cleaned.")

def perform_final_sync():
    print("Performing final sync operation to ensure all notes are up-to-date...")
    time.sleep(1)

def show_loading_slider(duration=30):
    """Displays a tqdm-based loading slider for a specified duration (in seconds)"""
    print("Querying the LLMs/vector DB for the note merging process. Please wait...")
    for _ in tqdm(range(duration), desc="Finalizing", ascii=True, ncols=100):
        time.sleep(1)

def move_final_notes(source, destination):
    """Move a folder with the final merged notes to a new location"""
    if os.path.exists(source):
        shutil.copytree(source, destination)
        print("Merged notes created successfully.")

def main():
    # roughly emulates note generation/merging process to line up for demo purposes
    # notes from different team members
    team_notes = [f"Note {i}" for i in range(1, 101)]
    beep(5)
    
    synced_notes = sync_notes(team_notes)

    merged_notes = merge_notes(synced_notes)

    perform_cleanup()

    perform_final_sync()
    
    show_loading_slider(20)
    
    source_folder = "back/outputs"
    destination_folder = "toy/outputs"
    beep(4)
    move_final_notes(source_folder, destination_folder)

if __name__ == "__main__":
    main()
