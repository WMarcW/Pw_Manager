import os
import json
import tkinter as tk
from tkinter import ttk, messagebox

json_datei = "passwoerter.json"

if not os.path.exists(json_datei):
    messagebox.showerror("Fehler", "Die Datei wurde nicht gefunden")
    exit()

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

print(rows)

# Tk GUI
root = tk.Tk()
root.title("Deine Passwörter")

root.geometry("900x400")

tree = ttk.Treeview(root)
tree.pack(fill="both", expand=True)

tree["columns"] = ("Website", "Benutzername", "Hash", "Salt")
tree.column("#0", width=0, stretch=tk.NO)
tree.heading("#0", text="")

for col in tree["columns"]:
    tree.column(col, anchor=tk.W, width=200)
    tree.heading(col, text=col, anchor=tk.W)

for row in rows:
    tree.insert("", tk.END, values=(
        row["Website"], row["Benutzername"], row["Hash"], row["Salt"]
    ))

root.mainloop()
