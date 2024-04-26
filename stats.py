import os
import re
from statistics import mean, stdev

def load_lexique(path):
    lexique = {}
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            word, pos = line.strip().split('\t')
            lexique[word.lower()] = pos
    return lexique

def tokenize(text):
    return re.findall(r'\w+', text.lower())

def printStatPOS1(file_names, input_dir, output_dir, lexique_path):
    lexique = load_lexique(lexique_path)
    stats = {'pourcentAmbig': {}, 'POS1seqsz': {}}
    global_tokens = []
    
    for file_name in file_names:
        path = os.path.join(input_dir, file_name)
        with open(path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        tokens = tokenize(text)
        sequences = []
        current_sequence = []
        
        for token in tokens:
            if token in lexique:
                if current_sequence:  # if there is a sequence of ambig tokens, finalize it
                    sequences.append(current_sequence)
                    current_sequence = []
                sequences.append([token])  # start a new sequence with the non-ambig token
            else:
                current_sequence.append(token)
        
        # Final sequence might be ambiguous
        if current_sequence:
            sequences.append(current_sequence)

        # Calculate stats for this file
        non_ambig = sum(1 for token in tokens if token in lexique)
        total = len(tokens)
        stats['pourcentAmbig'][file_name] = (non_ambig / total) * 100 if total else 0
        sequence_lengths = [len(seq) for seq in sequences]
        stats['POS1seqsz'][file_name] = (mean(sequence_lengths), stdev(sequence_lengths) if len(sequence_lengths) > 1 else 0)
        global_tokens.extend(tokens)
        
        # Write output
        output_path = os.path.join(output_dir, file_name + '.POS1Chunk')
        with open(output_path, 'w', encoding='utf-8') as output_file:
            for seq in sequences:
                output_file.write(' '.join(seq) + '\n')

    # Global stats
    total_global = len(global_tokens)
    non_ambig_global = sum(1 for token in global_tokens if token in lexique)
    stats['pourcentAmbig']['CORPUS'] = (non_ambig_global / total_global) * 100 if total_global else 0
    global_lengths = [len(seq) for file_seqs in sequences for seq in file_seqs]
    stats['POS1seqsz']['CORPUS'] = (mean(global_lengths), stdev(global_lengths) if len(global_lengths) > 1 else 0)

    return stats

# Usage example
file_names = ['notredame_vhugo.txt', '93_vhugo.txt', 'education_sentim_flaubert.txt']
input_dir = 'corpus/'
output_dir = 'stats/'
lexique_path = 'sous_lexique.txt'
stats = printStatPOS1(file_names, input_dir, output_dir, lexique_path)
print(stats)
