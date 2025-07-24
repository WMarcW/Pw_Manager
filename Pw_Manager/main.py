# Halloballo
import secrets
import string
import random
import os
import json
import hashlib


# generiere ein random passwort
def generatePassword():

    # "zeichen" ist ein String
    zeichen = string.ascii_letters + string.digits + string.punctuation
    unsicher_zeichen = ['"', "'", '\\']
    zeichen = ''.join(c for c in zeichen if c not in unsicher_zeichen)
    plain_pw = []
    plain_pw.append(secrets.choice(string.digits))
    plain_pw.append(secrets.choice(string.punctuation))
    for _ in range(16):
        plain_pw.append(secrets.choice(zeichen))

    random.shuffle(plain_pw)
    plain_pw = ''.join(plain_pw)
    print(plain_pw)
    return plain_pw


# hashe das random passwort

def hashen():
    rdm_passwort = generatePassword()
    salt = secrets.token_hex(16)
    rdm_passwort_bytes = (rdm_passwort + salt).encode()
    hash_object = hashlib.sha256(rdm_passwort_bytes)
    hash_hex = hash_object.hexdigest()

    return rdm_passwort, salt, hash_hex


def main():
    # .json datei erstellen
    if not os.path.exists("passwoerter.json"):
        with open("passwoerter.json", "w") as f:
            json.dump({}, f)

    # datei laden
    try:
        with open("passwoerter.json", "r") as f:
            daten = json.load(f)
    except json.decoder.JSONDecodeError:
        daten = {}

    # eingabe vom nutzer
    website = input("Website: ")
    username = input("Benutzername: ")
    plain_pw, salt, hash_value = hashen()

    # neuen eintrag hinzfg.
    if website not in daten:
        daten[website] = []

    daten[website].append({
        "username": username,
        "hash": hash_value,
        "salt": salt
    })
    # datei mit neuem inhalt überschreiben

    with open("passwoerter.json", "w") as f:
        json.dump(daten, f, indent=4)


if __name__ == "__main__":
    main()
