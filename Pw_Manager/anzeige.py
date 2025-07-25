import os
import json
import pandas as pd
import webbrowser

# verknüpfung zur .json datei
json_datei = "passwoerter.json"

# prüfen ob datei exestiert

if not os.path.exists(json_datei):
    print("Die Datei passwoerter.json exestiert nicht")
    exit()

with open(json_datei, "r") as f:
    daten = json.load(f)

# json in DataFrame umwandeln
rows = []
for website, eintraege in daten.items():
    if isinstance(eintraege, dict):
        eintraege = [eintraege]
    for eintrag in eintraege:
        rows.append({
            "Website": website,
            "Username": eintrag["username"],
            "Hash": eintrag["hash"],
            "Salt": eintrag["salt"]
        })
df = pd.DataFrame(rows)

# Tabelle anzeigen
print(df)

df.to_html("passwoerter_ausgabe.html", index=False)

# HTML im Browser öffnen
webbrowser.open("passwoerter_ausgabe.html")
