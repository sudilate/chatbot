import random
import json

import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Lib-Bot"
print("Let's chat! (type 'quit' to exit)")
while True:
    # sentence = "do you use credit cards?"
    sentence = input("You: ")
    if sentence == "quit":
        break

    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                print(f"{bot_name}: {random.choice(intent['responses'])}")
    else:
        print(f"{bot_name}: I do not understand...")

import tkinter as tk
from tkinter import scrolledtext
import random
import json
import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load intents and model
with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Lib-Bot"

# Function to handle sending message and getting bot response
def send():
    msg = entry.get()
    entry.delete(0, tk.END)
    if msg.strip() != "":
        chat.config(state=tk.NORMAL)
        chat.insert(tk.END, f"You: {msg}\n")
        chat.config(state=tk.DISABLED)

        sentence = tokenize(msg)
        X = bag_of_words(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)

        output = model(X)
        _, predicted = torch.max(output, dim=1)

        tag = tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        if prob.item() > 0.75:
            for intent in intents['intents']:
                if tag == intent["tag"]:
                    response = random.choice(intent['responses'])
                    chat.config(state=tk.NORMAL)
                    chat.insert(tk.END, f"{bot_name}: {response}\n")
                    chat.config(state=tk.DISABLED)
                    break
        else:
            chat.config(state=tk.NORMAL)
            chat.insert(tk.END, f"{bot_name}: I do not understand...\n")
            chat.config(state=tk.DISABLED)

# Set up GUI
root = tk.Tk()
root.title("ChatBot")

# Background image
bg_image = tk.PhotoImage(file="/Users/amitsarang/Desktop/my_chatenv/background_image.gif")
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Frame for chat history and scroll bar
frame = tk.Frame(root)
frame.pack()

# Chat history
chat = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=40, height=10)
chat.pack(side=tk.LEFT)

# Scroll bar
scroll = tk.Scrollbar(frame, command=chat.yview)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
chat.config(yscrollcommand=scroll.set)

# Entry for user input
entry = tk.Entry(root, width=40)
entry.pack()

# Send button
button = tk.Button(root, text="Send", command=send, bg="#32de97", activebackground="#3c9d9b")
button.pack()

root.mainloop()


# import tkinter as tk
# from tkinter import scrolledtext
# import random
# import json
# import torch

# from model import NeuralNet
# from nltk_utils import bag_of_words, tokenize

# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# # Load intents and model
# with open('intents.json', 'r') as json_data:
#     intents = json.load(json_data)

# FILE = "data.pth"
# data = torch.load(FILE)

# input_size = data["input_size"]
# hidden_size = data["hidden_size"]
# output_size = data["output_size"]
# all_words = data['all_words']
# tags = data['tags']
# model_state = data["model_state"]

# model = NeuralNet(input_size, hidden_size, output_size).to(device)
# model.load_state_dict(model_state)
# model.eval()

# bot_name = "Lib-Bot"

# # Function to handle sending message and getting bot response
# def send():
#     msg = entry.get()
#     entry.delete(0, tk.END)
#     if msg.strip() != "":
#         chat.config(state=tk.NORMAL)
#         chat.insert(tk.END, f"You: {msg}\n")
#         chat.config(state=tk.DISABLED)

#         sentence = tokenize(msg)
#         X = bag_of_words(sentence, all_words)
#         X = X.reshape(1, X.shape[0])
#         X = torch.from_numpy(X).to(device)

#         output = model(X)
#         _, predicted = torch.max(output, dim=1)

#         tag = tags[predicted.item()]

#         probs = torch.softmax(output, dim=1)
#         prob = probs[0][predicted.item()]
#         if prob.item() > 0.75:
#             for intent in intents['intents']:
#                 if tag == intent["tag"]:
#                     response = random.choice(intent['responses'])
#                     chat.config(state=tk.NORMAL)
#                     chat.insert(tk.END, f"{bot_name}: {response}\n")
#                     chat.config(state=tk.DISABLED)
#                     break
#         else:
#             chat.config(state=tk.NORMAL)
#             chat.insert(tk.END, f"{bot_name}: I do not understand...\n")
#             chat.config(state=tk.DISABLED)

# # Set up GUI
# root = tk.Tk()
# root.title("ChatBot")

# root.configure(background="#51829B") 
# # Background color for chat history
# chat_color = "#9683EC"  # 

# bg_image = tk.PhotoImage(file="/Users/amitsarang/Desktop/my_chatenv/background_image.gif")
# bg_label = tk.Label(root, image=bg_image)
# bg_label.configure(background="#51829B")
# bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)


# # Entry for user input
# entry = tk.Entry(root, width=40)
# entry.grid(row=10, column=10, columnspan=2, padx=10, pady=(10, 5), sticky="ew")

# # Send button
# button = tk.Button(root, text="Send", command=send, background="#827717", activebackground="#3c9d9b")
# button.grid(row=10, column=5, columnspan=3, padx=6, pady=5, sticky="ew")

# # Frame for chat history and scroll bar
# frame = tk.Frame(root, bg=chat_color)
# frame.grid(row=9, column=10, columnspan=1, padx=10, pady=5, sticky="nsew")

# # Chat history
# chat = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=40, height=10, bg=chat_color, fg="white")
# chat.grid(row=6, column=5, sticky="nsew")

# # Scroll bar
# scroll = tk.Scrollbar(frame, command=chat.yview)
# scroll.grid(row=4, column=2, sticky="ns")
# chat.config(yscrollcommand=scroll.set)

# # Configure grid weights to make the chat history expand vertically
# root.grid_rowconfigure(2, weight=1)

# root.mainloop()


