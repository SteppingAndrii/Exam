import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox

websites = []

def tkadd():
    url = entry1.get()
    if url:
        websites.append(url)
        messagebox.showinfo("Success", f"URL added: {url}")
        entry1.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please fill in the URL field!")

def tkclear():
    global websites
    websites = []
    messagebox.showinfo("Success", "All URLs cleared!")

def tklist():
    if websites:
        messagebox.showinfo("Current URLs", "\n".join(websites))
    else:
        messagebox.showinfo("Current URLs", "No URLs added yet.")

def tksearch():
    word = entry2.get()
    if not word:
        messagebox.showwarning("Input Error", "Please fill in the word field!")
        return
    if not websites:
        messagebox.showwarning("Input Error", "No URLs added to search!")
        return

    results = []
    for url in websites:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text().lower()
            count = text.count(word.lower())
            results.append((url, count))
        except Exception as e:
            results.append((url, f"Error: {str(e)}"))

    results_sorted = sorted(results, key=lambda x: x[1] if isinstance(x[1], int) else -1, reverse=True)

    message = ""
    for url, count in results_sorted:
        message += f"{url}: {count}\n"

    messagebox.showinfo("Search Results", message)

root = tk.Tk()
root.title("Simple Search App")
root.geometry("400x350")
root.resizable(False, False)

title_label = tk.Label(root, text="Welcome to the Search App", font=("Arial", 14))
title_label.pack(pady=(10, 5))

help_label1 = tk.Label(root, text="Input Your URL Here", font=("Arial", 10))
help_label1.pack(pady=(5, 5))

frame1 = tk.Frame(root)
frame1.pack(pady=5, padx=10, fill="x")

entry1 = tk.Entry(frame1, width=30, font=("Arial", 12))
entry1.pack(side=tk.LEFT, expand=True, padx=(0, 10))

add_btn = tk.Button(text="Add URL", font=("Arial", 12), command=tkadd)
add_btn.pack(pady=(5, 5))

list_btn = tk.Button(text="List All URLs", font=("Arial", 12), command=tklist)
list_btn.pack(pady=(0, 5))

clear_btn = tk.Button(text="Clear All URLs", font=("Arial", 12), command=tkclear)
clear_btn.pack(pady=(0, 10))

help_label2 = tk.Label(root, text="Input Your Word Here", font=("Arial", 10))
help_label2.pack(pady=(5, 5))

frame2 = tk.Frame(root)
frame2.pack(pady=5, padx=10, fill="x")

entry2 = tk.Entry(frame2, width=30, font=("Arial", 12))
entry2.pack(side=tk.LEFT, expand=True, padx=(0, 10))

search_btn = tk.Button(text="Search", font=("Arial", 12), command=tksearch)
search_btn.pack(pady=(10, 10))

root.mainloop()
