import os
import csv
import tkinter as tk
from random import choice, shuffle

CARD_DIR = 'cards'
COMPLETION_FILE = 'completion.csv'

def load_flashcards():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    cards_dir = os.path.join(script_dir, CARD_DIR)

    flashcard_sets = {}
    for file_name in os.listdir(cards_dir):
        if not file_name.endswith('.csv'):
            continue

        csv_path = os.path.join(cards_dir, file_name)
        flashcard_set = []

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                flashcard_set.append(row)

        key = os.path.splitext(file_name)[0]
        flashcard_sets[key] = flashcard_set

    return flashcard_sets

def load_completion():
    if not os.path.exists(COMPLETION_FILE):
        create_completion_file()
    with open(COMPLETION_FILE, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        completion_data = {row['card_set']: int(row['completed']) for row in reader}
    return completion_data

def create_completion_file():
    flashcard_sets = load_flashcards()
    with open(COMPLETION_FILE, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['card_set', 'completed', 'total'])
        writer.writeheader()
        for card_set, cards in flashcard_sets.items():
            writer.writerow({'card_set': card_set, 'completed': 0, 'total': len(cards)})

def update_completion_data(card_set_name, new_completed):
    completion_data = load_completion()
    completion_data[card_set_name] = new_completed
    with open(COMPLETION_FILE, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['card_set', 'completed', 'total'])
        writer.writeheader()
        for card_set, completed in completion_data.items():
            total_cards = len(load_flashcards()[card_set])
            writer.writerow({'card_set': card_set, 'completed': completed, 'total': total_cards})

class FlashcardApp:
    def __init__(self):
        self.flashcards = load_flashcards()
        self.current_set = None
        self.current_card = None
        self.cards = []

        self.root = tk.Tk()
        self.root.title("Dutch Flashcard Application")

        self.flashcard_button = tk.Button(self.root, text="Click for a flashcard", command=self.choose_flashcard)
        self.flashcard_button.pack(fill=tk.BOTH, expand=True)

        self.details_text = tk.Text(self.root, height=4, state='disabled')
        self.details_text.pack(fill=tk.BOTH, expand=True)

        self.understand_button = tk.Button(self.root, text="Got It!", command=self.mark_understood)
        self.understand_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.practice_button = tk.Button(self.root, text="Practice More", command=self.mark_practice)
        self.practice_button.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        self.choose_flashcard_set()

    def choose_flashcard_set(self):
        self.flashcard_set_var = tk.StringVar(self.root)
        self.flashcard_set_var.set(list(self.flashcards.keys())[0])
        self.flashcard_set_menu = tk.OptionMenu(self.root, self.flashcard_set_var, *self.flashcards.keys(), command=self.load_flashcard_set)
        self.flashcard_set_menu.pack()

    def load_flashcard_set(self, event=None):
        self.current_set = self.flashcard_set_var.get()
        self.cards = shuffle(self.flashcards[self.current_set].copy())
        self.choose_flashcard()

    def choose_flashcard(self):
        if not self.cards:
            return  # End of the set
        self.current_card = self.cards.pop()
        self.flashcard_button.config(text=self.current_card['word'])
        self.details_text.config(state='normal')
        self.details_text.delete(1.0, tk.END)
        self.details_text.config(state='disabled')

    def mark_understood(self):
        completion_data = load_completion()
        completion_data[self.current_set] += 1
        update_completion_data(self.current_set, completion_data[self.current_set])
        self.choose_flashcard()

    def mark_practice(self):
        if self.current_card:
            self.cards.insert(0, self.current_card)  # Add back to the front of the queue
            self.choose_flashcard()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FlashcardApp()
    app.run()
