import os
import csv
import tkinter as tk
from random import choice
from gtts import gTTS
import pygame

# 

def load_flashcards():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    cards_dir = os.path.join(script_dir, 'cards')

    flashcard_sets = {}
    for file_name in os.listdir(cards_dir):
        if not file_name.endswith('.csv'):
            continue

        csv_path = os.path.join(cards_dir, file_name)
        flashcard_set = {}

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            primary_key = reader.fieldnames[0]
            for row in reader:
                flashcard_set[row[primary_key]] = row

        key = os.path.splitext(file_name)[0]
        flashcard_sets[key] = flashcard_set

    return flashcard_sets

def play_sound(word):
    try:
        tts = gTTS(text=word, lang='nl')  # 'nl' is the language code for Dutch
        tts.save("temp_audio.mp3")
        pygame.mixer.music.load("temp_audio.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        os.remove("temp_audio.mp3")
    except Exception as e:
        print(f"Error playing sound: {e}")

def create_flashcard_app():
    pygame.mixer.init()
    flashcard_sets = load_flashcards()
    flashcard_set_names = list(flashcard_sets.keys())
    flashcards = flashcard_sets[flashcard_set_names[0]]

    def choose_flashcard():
        word, details = choice(list(flashcards.items()))
        flashcard_button.config(text=word)
        details_text.config(state='normal')
        details_text.delete(1.0, tk.END)

        # Display all details dynamically based on available columns
        for key, value in details.items():
            if key != 'word':
                details_text.insert(tk.END, f"{key.capitalize()}: {value}\n")
        
        details_text.config(state='disabled')

    def choose_flashcard_set(event):
        nonlocal flashcards
        chosen_set = flashcard_set_var.get()
        flashcards = flashcard_sets[chosen_set]

    root = tk.Tk()
    root.title("Dutch Flashcard Application with Sound (gTTS and Pygame)")

    flashcard_set_var = tk.StringVar(root)
    flashcard_set_var.set(flashcard_set_names[0])
    flashcard_set_menu = tk.OptionMenu(root, flashcard_set_var, *flashcard_set_names, command=choose_flashcard_set)
    flashcard_set_menu.pack()

    flashcard_button = tk.Button(root, text="Click for a flashcard", command=choose_flashcard)
    flashcard_button.pack(fill=tk.BOTH, expand=True)

    sound_button = tk.Button(root, text="Play Sound", command=lambda: play_sound(flashcard_button.cget("text")))
    sound_button.pack(fill=tk.BOTH, expand=True)

    details_text = tk.Text(root, height=4, state='disabled')
    details_text.pack(fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    create_flashcard_app()
