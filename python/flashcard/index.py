import tkinter as tk
from random import choice

# Dutch word dictionary as provided before
dutch_word_dict = dutch_flashcards = {
    "Hallo daar": {
        "meaning": "A greeting, similar to 'hello there'",
        "example": "Hallo daar! Hoe gaat het met je?",
        "translation": "Hello there! How are you?",
        "type": "phrase"
    },
    "Intellectuele dorst": {
        "meaning": "Intellectual thirst or desire for knowledge",
        "example": "Hij heeft een grote intellectuele dorst.",
        "translation": "He has a great intellectual thirst.",
        "type": "noun"
    },
    "Noem maar op": {
        "meaning": "And so forth, and so on",
        "example": "Appels, peren, bananen, noem maar op.",
        "translation": "Apples, pears, bananas, and so on.",
        "type": "phrase"
    },
    "Muziek is mijn medicijn": {
        "meaning": "Music is my medicine or music is my cure",
        "example": "Als ik me slecht voel, muziek is mijn medicijn.",
        "translation": "When I'm feeling down, music is my medicine.",
        "type": "phrase"
    },
    "Foodie in hart en nieren": {
        "meaning": "A real food lover or enthusiast",
        "example": "Ze is een foodie in hart en nieren.",
        "translation": "She's a foodie through and through.",
        "type": "phrase"
    },
    "Kers op de taart": {
        "meaning": "The icing on the cake, something that makes a good situation even better",
        "example": "Dat was echt de kers op de taart!",
        "translation": "That was really the icing on the cake!",
        "type": "phrase"
    },
    "Je ne sais quoi": {
        "meaning": "An indescribable quality that makes something distinctive or attractive",
        "example": "Ze heeft een bepaalde je ne sais quoi.",
        "translation": "She has a certain je ne sais quoi.",
        "type": "phrase"
    }
}


# Dutch verb dictionary as provided before
dutch_verb_dict = dutch_verb_dict = {
    "ben": {  #zijn (to be)
        "infinitive": "zijn",
        "present": "ben",
        "past": "was",
        "perfect": "is geweest"
    },
    "woon": {  #wonen (to live)
        "infinitive": "wonen",
        "present": "woon",
        "past": "woonde",
        "perfect": "heeft gewoond"
    },
    "werk": {  #werken (to work)
        "infinitive": "werken",
        "present": "werk",
        "past": "werkte",
        "perfect": "heeft gewerkt"
    },
    "geniet": {  #genieten (to enjoy)
        "infinitive": "genieten",
        "present": "geniet",
        "past": "genoot",
        "perfect": "heeft genoten"
    },
    "probeer": {  #proberen (to try)
        "infinitive": "proberen",
        "present": "probeer",
        "past": "probeerde",
        "perfect": "heeft geprobeerd"
    },
    "ontwikkel": {  #ontwikkelen (to develop)
        "infinitive": "ontwikkelen",
        "present": "ontwikkel",
        "past": "ontwikkelde",
        "perfect": "heeft ontwikkeld"
    },
    "doe": {  #doen (to do)
        "infinitive": "doen",
        "present": "doe",
        "past": "deed",
        "perfect": "heeft gedaan"
    },
    "zing": {  #zingen (to sing)
        "infinitive": "zingen",
        "present": "zing",
        "past": "zong",
        "perfect": "heeft gezongen"
    },
    "speel": {  #spelen (to play)
        "infinitive": "spelen",
        "present": "speel",
        "past": "speelde",
        "perfect": "heeft gespeeld"
    },
    "maak": {  #maken (to make)
        "infinitive": "maken",
        "present": "maak",
        "past": "maakte",
        "perfect": "heeft gemaakt"
    },
    "sta": {  #staan (to stand)
        "infinitive": "staan",
        "present": "sta",
        "past": "stond",
        "perfect": "heeft gestaan"
    },
    "leef": {  #leven (to live)
        "infinitive": "leven",
        "present": "leef",
        "past": "leefde",
        "perfect": "heeft geleefd"
    },
    "ga": {  #gaan (to go)
        "infinitive": "gaan",
        "present": "ga",
        "past": "ging",
        "perfect": "is gegaan"
    },
    "neem": {  #nemen (to take)
        "infinitive": "nemen",
        "present": "neem",
        "past": "nam",
        "perfect": "heeft genomen"
    },
}

# Combine both dictionaries
# Combine dictionaries in a way that integrates verb forms into the general words dictionary
flashcards = {**dutch_word_dict}
for verb, details in dutch_verb_dict.items():
    if verb in flashcards:
        flashcards[verb].update(details)
    else:
        flashcards[verb] = details

# Function to select a random flashcard
def choose_flashcard():
    word, details = choice(list(flashcards.items()))
    flashcard_button.config(text=word)
    details_text.config(state='normal')
    details_text.delete(1.0, tk.END)
    
    # Check if keys exist before accessing
    english = details.get('english', 'N/A')
    word_type = details.get('type', 'N/A')
    example = details.get('example', 'N/A')

    # If the word is a verb, also display verb forms
    verb_forms = ''
    if word_type == 'verb':
        verb_forms = f"Present: {details.get('present', 'N/A')}\nPast: {details.get('past', 'N/A')}\nFuture: {details.get('future', 'N/A')}"

    details_text.insert(tk.END, f"English: {english}\nType: {word_type}\nExample: {example}\n{verb_forms}")
    details_text.config(state='disabled')



# Function to create a flashcard application window
def create_flashcard_app():
    global flashcard_button, details_text

    root = tk.Tk()
    root.title("Dutch Flashcard Application")

    flashcard_button = tk.Button(root, text="Click for a flashcard", command=choose_flashcard)
    flashcard_button.pack(fill=tk.BOTH, expand=True)

    details_text = tk.Text(root, height=4, state='disabled')
    details_text.pack(fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    create_flashcard_app()
