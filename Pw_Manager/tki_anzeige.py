
import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess


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


# Tk GUI
root = tk.Tk()
root.title("Deine Passwörter")

root.geometry("900x400")

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
