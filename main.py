# Halloballo
import secrets
import string
import random

pw_laenge = int(input("wählen sie die länge ihre passwords: \n"))


def generatePassword():
    # "zeichen" ist ein String
    zeichen = string.ascii_letters + string.digits + string.punctuation
    password = []
    password.append(secrets.choice(string.digits))
    password.append(secrets.choice(string.punctuation))
    for _ in range(pw_laenge - 2):
        password.append(secrets.choice(zeichen))

    random.shuffle(password)
    return ''.join(password)


print(generatePassword())
