# DutchFlashcardWithSoundPygame.py

import os
import csv
import tkinter as tk
from random import choice
from gtts import gTTS
import pygame

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
            for row in reader:
                flashcard_set[row['word']] = row

        key = os.path.splitext(file_name)[0]
        flashcard_sets[key] = flashcard_set

    return flashcard_sets

def play_sound(word):
    try:
        tts = gTTS(text=word, lang='nl')  # 'nl' is the language code for Dutch
        tts.save("temp_audio.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load("temp_audio.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        os.remove("temp_audio.mp3")
    except Exception as e:
        print(f"Error playing sound: {e}")

def create_flashcard_app():
    flashcard_sets = load_flashcards()
    flashcard_set_names = list(flashcard_sets.keys())
    flashcards = flashcard_sets[flashcard_set_names[0]]

    def choose_flashcard():
        word, details = choice(list(flashcards.items()))
        flashcard_button.config(text=word)
        details_text.config(state='normal')
        details_text.delete(1.0, tk.END)
        
        english = details.get('english', 'N/A')
        word_type = details.get('type', 'N/A')
        example = details.get('example', 'N/A')
        
        verb_forms = ''
        if word_type == 'verb':
            verb_forms = f"Present: {details.get('present', 'N/A')}\nPast: {details.get('past', 'N/A')}\nFuture: {details.get('future', 'N/A')}"

        details_text.insert(tk.END, f"English: {english}\nType: {word_type}\nExample: {example}\n{verb_forms}")
        details_text.config(state='disabled')

        sound_button = tk.Button(root, text="🔊", command=lambda: play_sound(word))
        sound_button.pack(pady=5)

    def choose_flashcard_set(event):
        nonlocal flashcards
        chosen_set = flashcard_set_var.get()
        flashcards = flashcard_sets[chosen_set]

    root = tk.Tk()
    root.title("Dutch Flashcard Application with Sound (Pygame)")

    flashcard_set_var = tk.StringVar(root)
    flashcard_set_var.set(flashcard_set_names[0])  # default value
    flashcard_set_menu = tk.OptionMenu(root, flashcard_set_var, *flashcard_set_names, command=choose_flashcard_set)
    flashcard_set_menu.pack()

    flashcard_button = tk.Button(root, text="Click for a flashcard", command=choose_flashcard)
    flashcard_button.pack(fill=tk.BOTH, expand=True)

    details_text = tk.Text(root, height=4, state='disabled')
    details_text.pack(fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    create_flashcard_app()
