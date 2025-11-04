#!/usr/bin/env python3
"""
YouTube Assistant - Runner Quotidien
"""

import os
import sys
from datetime import datetime

def main():
    print("🎬 YouTube Assistant - Système prêt!")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Debug: Affiche le répertoire courant
    print(f"📁 Répertoire: {os.getcwd()}")
    print(f"📁 Contenu: {os.listdir('.')}")
    
    # Vérifier les inputs humains
    human_input_path = "human_input/daily_brief.txt"
    print(f"🔍 Recherche: {human_input_path}")
    
    if os.path.exists(human_input_path):
        with open(human_input_path, 'r') as f:
            brief = f.read().strip()
        print(f"✅ Brief quotidien: {brief}")
    else:
        print("❌ Fichier non trouvé - Liste human_input:")
        if os.path.exists("human_input"):
            print(f"   Contenu: {os.listdir('human_input')}")
        else:
            print("   ❌ Dossier human_input n'existe pas")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"💥 ERREUR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)