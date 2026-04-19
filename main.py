import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
import sqlite3

#  Database Setup
conn = sqlite3.connect("websites.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS websites (
    url TEXT UNIQUE
)
""")
conn.commit()

# Global Variables
websites = []

# Functions
def tkadd():
    url = entry1.get()
    if url:
        if url not in websites:
            websites.append(url)
            messagebox.showinfo("Success", f"URL added: {url}")
        else:
            messagebox.showinfo("Info", "URL already in current list!")
        entry1.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please fill in the URL field!")

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

# Session (Current URLs) Functions 
def list_current():
    if websites:
        messagebox.showinfo("Current URLs", "\n".join(websites))
    else:
        messagebox.showinfo("Current URLs", "No URLs in the current session.")

def clear_current():
    global websites
    websites = []
    messagebox.showinfo("Current URLs", "All current URLs cleared!")

# SQLite Functions
def see_saved():
    cursor.execute("SELECT url FROM websites")
    rows = cursor.fetchall()
    if rows:
        messagebox.showinfo("Saved Websites", "\n".join([row[0] for row in rows]))
    else:
        messagebox.showinfo("Saved Websites", "No websites saved yet.")

def load_saved():
    cursor.execute("SELECT url FROM websites")
    rows = cursor.fetchall()
    count_added = 0
    for row in rows:
        if row[0] not in websites:
            websites.append(row[0])
            count_added += 1
    messagebox.showinfo("Load Saved", f"{count_added} URLs loaded into current session.")

def save_websites():
    if not websites:
        messagebox.showwarning("Save Error", "No URLs in current session to save!")
        return
    if messagebox.askyesno("Warning", "This will overwrite the saved websites. Continue?"):
        cursor.execute("DELETE FROM websites")
        for url in websites:
            cursor.execute("INSERT OR IGNORE INTO websites (url) VALUES (?)", (url,))
        conn.commit()
        messagebox.showinfo("Saved", f"{len(websites)} websites saved successfully!")

def clear_saved():
    if messagebox.askyesno("Confirm", "Are you sure you want to clear all saved websites?"):
        cursor.execute("DELETE FROM websites")
        conn.commit()
        messagebox.showinfo("Cleared", "All saved websites cleared!")

# GUI Setup
root = tk.Tk()
root.title("Search App with Persistent URLs")
root.geometry("450x500")
root.resizable(False, False)

title_label = tk.Label(root, text="Welcome to the Search App", font=("Arial", 14))
title_label.pack(pady=(10, 5))

help_label1 = tk.Label(root, text="Input Your URL Here", font=("Arial", 10))
help_label1.pack(pady=(5, 5))

frame1 = tk.Frame(root)
frame1.pack(pady=5, padx=10, fill="x")

entry1 = tk.Entry(frame1, width=30, font=("Arial", 12))
entry1.pack(side=tk.LEFT, expand=True, padx=(0, 10))

# Add URL button
add_btn = tk.Button(text="Add URL", font=("Arial", 12), command=tkadd)
add_btn.pack(pady=(5, 5))

# Current session buttons
list_current_btn = tk.Button(text="List Current URLs", font=("Arial", 12), command=list_current)
list_current_btn.pack(pady=(2, 2))

clear_current_btn = tk.Button(text="Clear Current URLs", font=("Arial", 12), command=clear_current)
clear_current_btn.pack(pady=(2, 10))

# SQLite buttons
see_btn = tk.Button(text="See Saved Websites", font=("Arial", 12), command=see_saved)
see_btn.pack(pady=(2, 2))

load_btn = tk.Button(text="Load Saved Websites", font=("Arial", 12), command=load_saved)
load_btn.pack(pady=(2, 2))

save_btn = tk.Button(text="Save Websites", font=("Arial", 12), command=save_websites)
save_btn.pack(pady=(2, 2))

clear_saved_btn = tk.Button(text="Clear Saved Websites", font=("Arial", 12), command=clear_saved)
clear_saved_btn.pack(pady=(2, 10))

help_label2 = tk.Label(root, text="Input Your Word Here", font=("Arial", 10))
help_label2.pack(pady=(5, 5))

frame2 = tk.Frame(root)
frame2.pack(pady=5, padx=10, fill="x")

entry2 = tk.Entry(frame2, width=30, font=("Arial", 12))
entry2.pack(side=tk.LEFT, expand=True, padx=(0, 10))

search_btn = tk.Button(text="Search", font=("Arial", 12), command=tksearch)
search_btn.pack(pady=(10, 10))

root.mainloop()
