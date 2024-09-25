import json
import nltk
import wikipediaapi
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Ensure NLTK looks in the correct data directory
nltk.data.path.append('/home/sammy/nltk_data')

class AICharacter:
    def __init__(self):
        # Initialize Wikipedia API
        self.wiki_wiki = wikipediaapi.Wikipedia(
            language='en',
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent='PersonAI/0.1'
        )
        self.personas = {}
        self.current_persona = None
        self.load_personas()

    def format_title(self, name):
        return name.replace(" ", "_")  # Keep the original capitalization

    def fetch_persona_data(self, name):
        formatted_name = self.format_title(name)  # Format the name for Wikipedia
        page = self.wiki_wiki.page(formatted_name)
        if page.exists():
            return page.text
        else:
            print(f"No Wikipedia page found for {name}. Trying original capitalization.")
            original_name = name.strip().title()  # Capitalize each word
            page = self.wiki_wiki.page(original_name)
            if page.exists():
                return page.text
            else:
                print(f"No Wikipedia page found for {original_name}.")
                return None

    def add_persona(self, name):
        if name in self.personas:
            print(f"{name} already exists. Please choose a different name.")
            return
        if len(self.personas) >= 3:
            print("You can only have 3 personas. Please delete one to add a new one.")
            return
        
        description = self.fetch_persona_data(name)
        if description:
            self.personas[name] = description
            self.save_personas()
            print(f"{name} has been successfully created.")
            if self.ask_for_confirmation():
                self.current_persona = name
                self.save_adopted_persona()
                print(f"You have adopted the persona of {name}.")
                self.run_as_persona(name)

    def run_as_persona(self, name):
        print(f"You have now adopted the persona of {name}.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print("Exiting persona mode. Returning to main menu...")
                break
            else:
                print(f"AI: I'm not sure how to respond to that. But I'm {name}.")

    def list_personas(self):
        if not self.personas:
            print("No personas available.")
        else:
            print("Available personas:")
            for name in self.personas.keys():
                print(f"- {name}")

    def delete_persona(self):
        self.list_personas()  # Show available personas before deleting
        name = input("Enter the name of the persona to delete: ")
        if name in self.personas:
            del self.personas[name]
            self.save_personas()
            print(f"{name} has been deleted.")
        else:
            print(f"{name} does not exist.")

    def ask_for_confirmation(self):
        return input("Do you want to adopt this persona? (yes/no): ").lower() == "yes"

    def show_menu(self):
        print("Welcome to personAI!")
        while True:
            print("\nMain Menu:")
            print("1. Add new persona")
            print("2. Load existing persona")
            print("3. List personas")
            print("4. Delete persona")
            print("5. Exit personAI")
            
            choice = input("Choose an option: ")
            if choice == '1':
                name = input("Enter the character's name: ")
                self.add_persona(name)
            elif choice == '2':
                if self.current_persona:
                    print(f"You are currently adopting {self.current_persona}.")
                    change = input("Do you want to change to a different persona? (yes/no): ").lower()
                    if change == "yes":
                        available_personas = list(self.personas.keys())
                        if available_personas:
                            print("Available personas to load:")
                            for persona in available_personas:
                                print(f"- {persona}")
                            name = input("Enter the character's name to adopt: ")
                            if name in self.personas:
                                self.current_persona = name
                                self.save_adopted_persona()
                                self.run_as_persona(name)
                            else:
                                print("That persona does not exist.")
                        else:
                            print("No available personas to load.")
                    else:
                        print(f"Continuing with the current persona: {self.current_persona}.")
                        self.run_as_persona(self.current_persona)
                else:
                    available_personas = list(self.personas.keys())
                    if available_personas:
                        print("Available personas to load:")
                        for persona in available_personas:
                            print(f"- {persona}")
                        name = input("Enter the character's name to adopt: ")
                        if name in self.personas:
                            self.current_persona = name
                            self.save_adopted_persona()
                            self.run_as_persona(name)
                        else:
                            print("That persona does not exist.")
                    else:
                        print("You have not adopted any persona.")
            elif choice == '3':
                self.list_personas()
            elif choice == '4':
                self.delete_persona()  # Call the method without passing name
            elif choice == '5':
                print("Exiting personAI.")
                break
            else:
                print("Invalid option. Please try again.")

    def save_personas(self):
        with open('personas.json', 'w') as f:
            json.dump(self.personas, f, indent=4)

    def load_personas(self):
        try:
            with open('personas.json', 'r') as f:
                self.personas = json.load(f)
        except FileNotFoundError:
            self.personas = {}

    def save_adopted_persona(self):
        with open('adopted_persona.json', 'w') as f:
            json.dump({"current_persona": self.current_persona}, f, indent=4)

# In your main code
if __name__ == "__main__":
    ai = AICharacter()
    ai.show_menu()
