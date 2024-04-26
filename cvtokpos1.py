import re

def load_sous_lexique(file_path):
    sous_lexique = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            token, morpho_tag = line.strip().split('\t')
            sous_lexique[token] = morpho_tag
    return sous_lexique

def process_tokens_with_morpho(text_file, lexicon_file, output_file):
    # Charger le sous-lexique
    sous_lexique = load_sous_lexique(lexicon_file)

    # Liste pour stocker les quadruplets
    quadruplets = []

    # Lecture des tokens du fichier text_file
    with open(text_file, 'r', encoding='utf-8') as file:
        for line in file:
            # Extraire le token et son type de token
            token_data = eval(line)  # Convertir la ligne en tuple Python
            token = token_data[0]
            token_type = token_data[2]

            # Normalisation du token
            normalized_token = token.lower()

            # Recherche de l'étiquette morphosyntaxique dans le sous-lexique
            morpho_tag = sous_lexique.get(normalized_token, None)

            # Création du quadruplet avec l'étiquette morphosyntaxique trouvée
            quadruplets.append((token, normalized_token, token_type, morpho_tag))

    # Écriture des résultats dans un fichier de sortie
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for quadruplet in quadruplets:
            outfile.write(str(quadruplet) + '\n')

if __name__ == "__main__":
    tokens_file = 'tokens_output.txt'
    lexicon_file = 'sous_lexique.txt'
    output_file = 'quadruplets_output.txt'

    process_tokens_with_morpho(tokens_file, lexicon_file, output_file)
