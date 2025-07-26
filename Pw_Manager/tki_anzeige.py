
import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
from main import eintrag_speichern

json_datei = "passwoerter.json"


def lade_daten():
    if not os.path.exists(json_datei):
        messagebox.showerror("Fehler",
                             "Die Datei passwoerter.json existiert nicht.")
        return []

    with open(json_datei, "r") as f:
        daten = json.load(f)

    rows = []
    for website, eintraege in daten.items():
        if isinstance(eintraege, dict) and "username" in eintraege:
            eintraege = [eintraege]

        for eintrag in eintraege:
            rows.append({
                "Website": website,
                "Benutzername": eintrag.get("username", ""),
                "Hash": eintrag.get("hash", ""),
                "Salt": eintrag.get("salt", "")
            })

    return rows


def run_main():
    subprocess.run(["python", "main.py"])
    refresh_tree()


def refresh_tree():
    for item in tree.get_children():
        tree.delete(item)

    neue_zeilen = lade_daten()
    for row in neue_zeilen:
        tree.insert("", tk.END, values=(
            row["Website"], row["Benutzername"], row["Hash"], row["Salt"]
        ))


def speichern():
    website = entry_website.get()
    username = entry_username.get()

    if not website or not username:
        messagebox.showerror("Fehler",
                             "Bitte Website und Benutzername eingeben.")
        return

    eintrag_speichern(website, username)
    messagebox.showinfo("Erfolg", "Eintrag erfolgreich gespeichert.")

    entry_website.delete(0, tk.END)
    entry_username.delete(0, tk.END)


# Tk GUI
root = tk.Tk()
root.title("Deine Passwörter")

root.geometry("900x400")

eingabe_frame = tk.Frame(root)
eingabe_frame.pack(pady=10)


tk.Label(eingabe_frame, text="Website:").grid(row=0, column=0)
entry_website = tk.Entry(eingabe_frame)
entry_website.grid(row=0, column=1)

tk.Label(eingabe_frame, text="Benutzername:").grid(row=0, column=2)
entry_username = tk.Entry(eingabe_frame)
entry_username.grid(row=0, column=3)

btn_speichern = tk.Button(eingabe_frame, text="Speichern", command=speichern)
btn_speichern.grid(row=0, column=4, padx=5)

tree = ttk.Treeview(root)
tree.pack(fill="both", expand=True)

tree["columns"] = ("website", "Benutzername", "Hash", "Salt")
tree.column("#0", width=0, stretch=tk.NO)
tree.heading("#0", text="")

for col in tree["columns"]:
    tree.column(col, anchor=tk.W, width=200)
    tree.heading(col, text=col, anchor=tk.W)

refresh_tree()


tk.Button(root, text="Neues Passwort generieren",
          command=run_main).pack(pady=10)


root.mainloop()
