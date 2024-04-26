import re
from random import randrange

def CVTok(text):
    # Définition des expressions régulières pour les types de tokens
    cv_pattern = r'[^\W\d_]+'
    pn_pattern = r'[\.,;:!?]'
    es_pattern = r'\s+'

    # Fonction de normalisation
    def normalize(token):
        return token.lower()

    # Liste pour stocker les triplets
    tokens = []

    # Itération sur les tokens dans le texte
    for match in re.finditer(f'({cv_pattern})|({pn_pattern})|({es_pattern})', text):
        token = match.group()
        if match.group(1):  # CV
            token_type = 'CV'
            normalized_token = normalize(token)
            tokens.append((token, normalized_token, token_type))
        elif match.group(2):  # PN
            token_type = 'PN'
            normalized_token = normalize(token)
            tokens.append((token, normalized_token, token_type))
        elif match.group(3):  # ES
            # Ne rien faire pour les espaces (ignorer)
            continue

    return tokens

def printCVTok(filename, tokens):
    with open(filename, 'w', encoding='utf-8') as file:
        for token in tokens:
            file.write(str(token) + '\n')

if __name__ == "__main__":
    # Charger le texte à partir du fichier
    with open('corpus/notredame_vhugo.txt', 'r', encoding='utf-8') as file:
        text = file.read()

    # Choix d'un extrait de 4500 caractères au hasard
    deb = randrange(len(text) - 4500)
    excerpt = text[deb: deb + 4500]

    # Application de la fonction CVTok
    tokens = CVTok(excerpt)

    # Écriture des résultats dans un fichier
    printCVTok('tokens_output.txt', tokens)
