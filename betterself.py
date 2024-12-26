import tkinter as tk
import random
import pickle
from datetime import datetime
import webbrowser

affirmations = [
    "You are enough.",
    "You are stronger than you think.",
    "This too shall pass.",
    "Take a deep breath, you’ve got this.",
    "Believe in yourself, you're amazing.",
    "Your strength is an inspiration for many.",
    "You are strong enough to weather any storm, for better days are just ahead,"  
    "Your resilience shines brighter than any challenge that comes your way,"  
    "Trust in the quiet power of healing; growth is already unfolding within you,"  
    "You are not defined by your setbacks, but by the strength with which you rise,"  
    "Your emotions are sacred, and it is okay to honor them with compassion,"  
    "You have faced storms before, and each time, you have emerged stronger,"  
    "Amid the clouds, you find the light, always choosing to focus on the good,"  
    "Peace and happiness are your birthright, and they flow effortlessly to you,"  
    "Every setback is but a chapter in the epic of your life, and the story is far from over,"  
    "Your heart has the power to heal, and your soul is your guide,"  
    "It is okay to pause, to rest; the world will wait as you find your peace,"  
    "Love and support surround you, for you are worthy of every ounce of both,"  
    "Each new day brings a fresh canvas, ready for the joy you create,"  
    "Believe that everything unfolds as it should, with purpose and grace,"  
    "Within you lies the peace you seek, waiting to be embraced,"  
    "Every obstacle is a lesson, shaping you into the wisdom you are becoming,"  
    "You hold the power to transform any moment into one of peace,"  
    "Strength flows from you in ways you may not yet see, but they are there,"  
    "Tomorrow is filled with endless possibilities, and you are ready to meet them,"  
    "You are enough, always have been, and always will be, exactly as you are."  
]

moods = {
    "joyful": "Yay! I'm glad you're feeling happy!",
    "calm": "You're calm. Enjoy the peace.",
    "lonely": "I understand you're feeling sad. I'm here for you.",
    "disappointed": "It's okay to feel down. Let's make it better."
}

diary_entries = {}

users = {}
current_user = None

def load_data():
    global users
    try:
        with open('users_data.pkl', 'rb') as file:
            users = pickle.load(file)
            print("Users Data Loaded.")  
    except FileNotFoundError:
        users = {}
        print("No previous user data found.") 

def save_data():
    with open('users_data.pkl', 'wb') as file:
        pickle.dump(users, file)
        print("Users Data Saved.")  

class MoodHandler:
    def __init__(self, root):
        global current_user
        self.root = root
        self.root.title("Better Self - Mood Tracker")
        self.root.geometry("600x700")
        self.root.config(bg="#f4e1d2")
        self.current_mood = None 
        load_data() 
        current_user = None  

        self.font_style = ("Times New Roman", 14)
        self.show_login_screen()

    def show_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Welcome to Better Self!", font=(
            "Times New Roman", 16), bg="#f4e1d2", fg="#5c4033").pack(pady=20)
        tk.Button(self.root, text="Login", font=self.font_style, bg="#A67C52", fg="white",
                  relief="solid", borderwidth=2, width=20, height=2, command=self.login).pack(pady=10)
        tk.Button(self.root, text="Sign Up", font=self.font_style, bg="#A67C52", fg="white",
                  relief="solid", borderwidth=2, width=20, height=2, command=self.signup).pack(pady=10)

    def login(self):
        self.clear_screen()
        tk.Label(self.root, text="Enter your username and password",
                 font=self.font_style, bg="#f4e1d2", fg="#5c4033").pack(pady=20)
        self.username_entry = tk.Entry(
            self.root, font=self.font_style, width=30)
        self.username_entry.pack(pady=10)
        self.password_entry = tk.Entry(
            self.root, font=self.font_style, width=30, show="*")
        self.password_entry.pack(pady=10)
        tk.Button(self.root, text="Login", font=self.font_style, bg="#A67C52", fg="white",
                  relief="solid", borderwidth=2, command=self.process_login).pack(pady=20)
        tk.Button(self.root, text="Back", font=self.font_style, bg="#D39B86", fg="white",
                  relief="solid", borderwidth=2, command=self.show_login_screen).pack(pady=10)

    def signup(self):
        self.clear_screen()
        tk.Label(self.root, text="Create a new account",
                 font=self.font_style, bg="#f4e1d2", fg="#5c4033").pack(pady=20)
        self.username_entry = tk.Entry(
            self.root, font=self.font_style, width=30)
        self.username_entry.pack(pady=10)
        self.password_entry = tk.Entry(
            self.root, font=self.font_style, width=30, show="*")
        self.password_entry.pack(pady=10)
        tk.Button(self.root, text="Sign Up", font=self.font_style, bg="#A67C52", fg="white",
                  relief="solid", borderwidth=2, command=self.process_signup).pack(pady=20)
        tk.Button(self.root, text="Back", font=self.font_style, bg="#D39B86", fg="white",
                  relief="solid", borderwidth=2, command=self.show_login_screen).pack(pady=10)

    def process_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in users and users[username]['password'] == password:
            global current_user
            current_user = username
            self.ask_mood()
        else:
            tk.Label(self.root, text="Invalid credentials!",
                     font=self.font_style, bg="#f4e1d2", fg="red").pack(pady=10)

    def process_signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in users:
            tk.Label(self.root, text="Username already exists!",
                     font=self.font_style, bg="#f4e1d2", fg="red").pack(pady=10)
        elif len(users) >= 50:
            tk.Label(self.root, text="User limit reached!",
                     font=self.font_style, bg="#f4e1d2", fg="red").pack(pady=10)
        else:
            users[username] = {'password': password, 'entries': {}}
            save_data()
            tk.Label(self.root, text="Account created successfully!",
                     font=self.font_style, bg="#f4e1d2", fg="green").pack(pady=10)

    def ask_mood(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Welcome, {current_user}! How are you feeling today?", font=(
            "Times New Roman", 16), bg="#f4e1d2", fg="#5c4033").pack(pady=20)

        for mood in moods.keys():
            btn = tk.Button(self.root, text=mood.capitalize(), font=self.font_style, bg="#D39B86", fg="white",
                            relief="solid", borderwidth=2, width=20, height=2, command=lambda m=mood: self.handle_mood(m))
            btn.pack(pady=10, fill='x', padx=40)

        tk.Button(self.root, text="Read All Entries", font=self.font_style, bg="#A67C52", fg="white",
                  relief="solid", borderwidth=2, width=20, height=2, command=self.read_all_entries).pack(pady=20)

    def handle_mood(self, mood):
        self.current_mood = mood  # Store the current mood
        self.clear_screen()

        self.display_message(moods[mood])

        if mood in ["joyful", "calm"]:
            self.happy_response()
        elif mood in ["lonely", "disappointed"]:
            self.sad_response()
        if mood == "disappointed":
            self.add_affirmation_button()
            self.add_comfortingplaylist_button()
            self.add_back_button()
        elif mood == "lonely":
            self.add_activity_button()
            self.add_relaxingmusic_button()
            self.add_back_button()
        elif mood == "joyful":
            self.add_happymusic_button()
            self.add_back_button()
        elif mood == "calm":
            self.add_motivatingpodcast_button()
            self.add_back_button()
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def display_message(self, message):
        tk.Label(self.root, text=message, font=self.font_style,
                 bg="#f4e1d2", fg="#5c4033", wraplength=500).pack(pady=20)

    def happy_response(self):
        self.display_message("Let's record this memory! Write a diary entry.")
        tk.Button(self.root, text="Write Diary Entry", font=self.font_style, bg="#A67C52", fg="white",
                  relief="solid", borderwidth=2, width=20, height=2, command=self.open_diary).pack(pady=20)

    def sad_response(self):
        self.display_message(
            "How would the Moon shine if there was no darkness. \nRelive the happy moments.")
        tk.Button(self.root, text="Read a happy diary entry", font=self.font_style, bg="#A67C52", fg="white",
                  relief="solid", borderwidth=2, width=20, height=2, command=self.read_random_entry).pack(pady=20)

    def add_affirmation_button(self):
        tk.Button(self.root, text="Read Random Affirmation", font=self.font_style, bg="#A67C52", fg="white",
              relief="solid", borderwidth=2, width=20, height=2, command=self.display_random_affirmation).pack(pady=20)

    def display_random_affirmation(self):
         affirmation = random.choice(affirmations)
         self.display_message(affirmation)

    def add_activity_button(self):
        tk.Button(self.root, text="Suggest an Activity", font=self.font_style, bg="#A67C52", fg="white",
              relief="solid", borderwidth=2, width=20, height=2, command=self.suggest_activity).pack(pady=20)
    
    def suggest_activity(self):
        activity = random.choice([
        "Take a walk in the park.",
        "Call a friend to chat.",
        "Try a new hobby or craft.",
        "Watch a feel-good movie."
    ])
        self.display_message(f"How about trying this activity? \n{activity}")
    def play_comforting_podcast(self):
        # Link to the Spotify playlist or podcast
        podcast_url = "https://open.spotify.com/playlist/5uCDuvkZqjMPUR7j6TniRW"
        webbrowser.open(podcast_url)
    def  add_comfortingplaylist_button(self):
        tk.Button(self.root, text="Listen to Comforting Podcast", font=self.font_style, bg="#8B4C4A", fg="white",
          relief="solid", borderwidth=2, width=28, height=2, command=self.play_comforting_podcast).pack(pady=20)
    def play_soft_music(self):
        # Link to the Spotify playlist or podcast
        podcast_url ="https://open.spotify.com/playlist/43PQ5XylpPN2qT0oRQizDM"
        webbrowser.open(podcast_url)
    def  add_relaxingmusic_button(self):
        tk.Button(self.root, text="Listen to relaxing music", font=self.font_style, bg="#8B4C4A", fg="white",
          relief="solid", borderwidth=2, width=28, height=2, command=self.play_soft_music).pack(pady=20)
    def play_happy_music(self):
        # Link to the Spotify playlist or podcast
        podcast_url = "https://open.spotify.com/playlist/2soK85vhEYcTnQ2PXtfG2p"
        webbrowser.open(podcast_url)
    def  add_happymusic_button(self):
        tk.Button(self.root, text="Vibe to the music", font=self.font_style, bg="#8B4C4A", fg="white",
          relief="solid", borderwidth=2, width=25, height=2, command=self.play_happy_music).pack(pady=20)
    def play_motivating_podcast(self):
        # Link to the Spotify playlist or podcast
        podcast_url = "https://open.spotify.com/playlist/4cSR30YpH1lnn2VnG5V5kF"
        webbrowser.open(podcast_url)
    def  add_motivatingpodcast_button(self):
        tk.Button(self.root, text="Listen to motivating podcasts", font=self.font_style, bg="#8B4C4A", fg="white",
          relief="solid", borderwidth=2, width=30, height=2, command=self.play_motivating_podcast).pack(pady=20)
    def open_diary(self):
        self.clear_screen()
        self.display_message("Write your thoughts below:")

        self.text_area = tk.Text(self.root, height=10, width=40, font=self.font_style,
                                 wrap="word", bd=2, relief="solid", padx=10, pady=10)
        self.text_area.pack(pady=20)

        tk.Button(self.root, text="Save Diary Entry", font=self.font_style, bg="#A67C52", fg="white",
                  relief="solid", borderwidth=2, width=20, height=2, command=self.save_diary_entry).pack(pady=20)
        self.add_back_button()

    def save_diary_entry(self):
        global current_user
        entry = self.text_area.get("1.0", "end-1c")  # Retrieve the text
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if entry.strip() and self.current_mood and current_user:  # Ensure mood and user are set
            if self.current_mood not in users[current_user]['entries']:
                users[current_user]['entries'][self.current_mood] = []
            users[current_user]['entries'][self.current_mood].append(
                {"entry": entry.strip(), "timestamp": timestamp})
            save_data()  # Save diary entries after adding new ones
            self.clear_screen()
            self.display_message("Your diary entry has been saved. Take care!")
            self.add_back_button()

    def read_random_entry(self):
        global current_user
        entries = [item for mood_entries in users[current_user]
                   ['entries'].values() for item in mood_entries]
        if entries:
            random_entry = random.choice(entries)
            self.display_message(f"Happy Entry from {random_entry['timestamp']}:\n\n{random_entry['entry']}")

        else:
            self.display_message("No entries available yet.")

    def read_all_entries(self):
        global current_user
        self.clear_screen()

        # Create a container frame for the scrollable content
        container = tk.Frame(self.root, bg="#f4e1d2")
        container.pack(fill="both", expand=True)

        # Add a canvas to enable scrolling
        canvas = tk.Canvas(container, bg="#f4e1d2", highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="nsew")

        # Add a vertical scrollbar
        scrollbar = tk.Scrollbar(
            container, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Configure the container to resize dynamically
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        # Configure the canvas for scrolling
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))

        # Create a frame inside the canvas for content
        content_frame = tk.Frame(canvas, bg="#f4e1d2")
        canvas.create_window((0, 0), window=content_frame, anchor="n")

        # Display user's diary entries
        tk.Label(content_frame, text="Your Diary Entries", font=("Times New Roman", 18), bg="#f4e1d2",
                 fg="#5c4033").pack(pady=20)

        for mood, mood_entries in users[current_user]['entries'].items():
            mood_frame = tk.LabelFrame(content_frame, text=f"{mood.capitalize()} Entries:",
                                       font=("Times New Roman", 16), bg="#f4e1d2", fg="#988558")
            mood_frame.pack(pady=10, fill='x', padx=20)
            for entry in sorted(mood_entries, key=lambda x: x['timestamp']):
                tk.Label(mood_frame, text=f"{entry['timestamp']}:\n {entry['entry']}",
                         font=self.font_style, bg="#f4e1d2", fg="#5c4033", wraplength=500).pack(pady=5)

        # Add a back button at the end of the scrollable area
        tk.Button(content_frame, text="Back to Main Menu", font=self.font_style, bg="#D39B86",
                  fg="white", relief="solid", borderwidth=2, width=20, height=2, command=self.ask_mood).pack(pady=20)

        # Ensure the container resizes dynamically
        container.bind("<Configure>", lambda e: self.center_content(
            e, content_frame, canvas))

    def center_content(self, event, content_frame, canvas):
        canvas_width = event.width
        content_width = content_frame.winfo_reqwidth()
        x_offset = max((canvas_width - content_width) // 2, 0)
        canvas.itemconfig(canvas.create_window(
            (x_offset, 0), window=content_frame, anchor="n"))

    def add_back_button(self):
        tk.Button(self.root, text="Back to Main Menu", font=self.font_style, bg="#D39B86", fg="white",
                  relief="solid", borderwidth=2, width=20, height=2, command=self.ask_mood).pack(pady=20)


# Initialize the GUI
root = tk.Tk()
app = MoodHandler(root)

# Start the app
root.mainloop()
