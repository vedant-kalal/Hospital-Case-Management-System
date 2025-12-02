import os

def print_tree(startpath):
    for root, dirs, files in os.walk(startpath):
        # Modify dirs in-place to skip unwanted directories
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.venv', 'venv', '.idea', '.vscode', 'node_modules']]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f'{subindent}{f}')

if __name__ == "__main__":
    print_tree('.')
