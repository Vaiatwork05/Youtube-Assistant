#!/usr/bin/env python3
"""
YouTube Assistant - Runner Quotidien
"""

import os
import sys
from datetime import datetime

def main():
    print("YouTube Assistant - Systeme pret!")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Debug: Affiche le repertoire courant
    print(f"Repertoire: {os.getcwd()}")
    
    # Verifier les inputs humains
    human_input_path = "human_input/daily_brief.txt"
    print(f"Recherche: {human_input_path}")
    
    if os.path.exists(human_input_path):
        with open(human_input_path, 'r') as f:
            brief = f.read().strip()
        print(f"Brief quotidien: {brief}")
        return True
    else:
        print("Fichier non trouve")
        # Lister le contenu de human_input pour debug
        if os.path.exists("human_input"):
            print(f"Contenu human_input: {os.listdir('human_input')}")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"ERREUR: {e}")
        sys.exit(1)
