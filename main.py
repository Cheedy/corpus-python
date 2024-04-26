import re

def FiltrOnePOS(filename):
    # Dictionnaire pour stocker les entrées non ambigües
    entries_non_ambigues = {}

    # Expression régulière pour analyser chaque ligne du lexique
    regex_pattern = r'^(\S+)\s+([\w:.-]+)$'

    # Lecture du fichier lexique
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            match = re.match(regex_pattern, line)
            if match:
                mot = match.group(1)
                pos = match.group(2)

                if mot not in entries_non_ambigues:
                    entries_non_ambigues[mot] = pos
                else:
                    # Si le mot est déjà présent, vérifier s'il est ambigü
                    if entries_non_ambigues[mot] != pos:
                        # Le mot est ambigu, donc le retirer des entrées non ambigües
                        del entries_non_ambigues[mot]

    return entries_non_ambigues

def ecrireFichier(entries, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for mot, pos in entries.items():
            file.write(f"{mot}\t{pos}\n")

# Nom du fichier lexique à traiter
lexique_filename = 'lexique.txt'

# Appel de la fonction pour obtenir les entrées non ambigües
resultats_non_ambigues = FiltrOnePOS(lexique_filename)

# Nom du fichier de sortie pour les entrées non ambigües
output_filename = 'sous_lexique.txt'

# Écriture des entrées non ambigües dans le fichier de sortie
ecrireFichier(resultats_non_ambigues, output_filename)

print("Les entrées non ambigües ont été écrites dans le fichier sous_lexique.txt.")
