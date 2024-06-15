import json

def save_matrix(matrix):
    with open('matrix.json', 'w') as f:
        json.dump(matrix, f, indent=4)  # Use indent=4 for pretty-printing

def load_matrix():
    with open('matrix.json') as f:
        return json.load(f)
