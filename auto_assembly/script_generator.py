#!/usr/bin/env python3
"""
Générateur de scripts YouTube
"""

import json
import random
from datetime import datetime

def generate_scripts():
    """Génère 3 scripts YouTube"""
    
    themes = {
        "histoire": ["Pyramides", "Napoléon", "Rome Antique", "Moyen-Âge", "Révolution"],
        "science": ["Espace", "Quantique", "IA", "Climat", "Énergie"],
        "mystere": ["OVNIs", "Civilisations", "Trésors", "Conspiration", "Paranormal"]
    }
    
    scripts = []
    
    for i in range(3):
        categorie = random.choice(list(themes.keys()))
        sujet = random.choice(themes[categorie])
        
        titre = f"{random.randint(3,5)} SECRETS SUR {sujet.upper()}"
        contenu = "\n".join([
            f"• {random.choice(['Découverte récente', 'Révélation choquante', 'Preuve incontestable'])} sur {sujet}",
            f"• {random.choice(['Ce que les experts cachent', 'La vérité dérangeante', 'Les preuves ignorées'])}",
            f"• {random.choice(['Pourquoi on vous ment', 'La conclusion surprenante', 'Ce qui change tout'])}"
        ])
        
        scripts.append({
            "title": titre,
            "content": contenu
        })
    
    # Sauvegarde
    with open('scripts.json', 'w', encoding='utf-8') as f:
        json.dump(scripts, f, indent=2, ensure_ascii=False)
    
    print(f"✅ {len(scripts)} scripts générés et sauvegardés")
    return scripts

if __name__ == "__main__":
    generate_scripts()
