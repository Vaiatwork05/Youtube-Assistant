#!/usr/bin/env python3
"""
DEBUG DÉTAILLÉ - YouTube Assistant
"""

import os
import sys
import subprocess

print("=" * 50)
print("🔍 DEBUG DÉTAILLÉ - DÉMARRAGE")
print("=" * 50)

# 1. Info système
print("1. 🐍 INFO PYTHON:")
print(f"   Version: {sys.version}")
print(f"   Executable: {sys.executable}")
print(f"   Path: {sys.path}")

# 2. Répertoire courant
print("\n2. 📁 RÉPERTOIRE COURANT:")
current_dir = os.getcwd()
print(f"   Chemin: {current_dir}")

# 3. Liste tous les fichiers
print("\n3. 📋 LISTE FICHIERS COMPLÈTE:")
try:
    for root, dirs, files in os.walk('.'):
        level = root.replace('.', '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}📁 {os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f'{subindent}📄 {file}')
except Exception as e:
    print(f"   ❌ Erreur: {e}")

# 4. Test fichier spécifique
print("\n4. 🔍 TEST FICHIER daily_runner.py:")
runner_path = "auto_assembly/daily_runner.py"
if os.path.exists(runner_path):
    print(f"   ✅ Fichier trouvé: {runner_path}")
    print(f"   📏 Taille: {os.path.getsize(runner_path)} octets")
    
    # Affiche le contenu
    with open(runner_path, 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"   📝 Lignes: {len(content.splitlines())}")
        print(f"   🔤 Contenu (premières 3 lignes):")
        for i, line in enumerate(content.splitlines()[:3]):
            print(f"      {i+1}: {line}")
else:
    print(f"   ❌ Fichier NON trouvé: {runner_path}")

# 5. Test execution daily_runner
print("\n5. 🚀 TEST EXÉCUTION DIRECTE:")
try:
    result = subprocess.run([
        sys.executable, 
        "auto_assembly/daily_runner.py"
    ], capture_output=True, text=True, timeout=10)
    
    print(f"   Return code: {result.returncode}")
    print(f"   Stdout: {result.stdout}")
    print(f"   Stderr: {result.stderr}")
    
except Exception as e:
    print(f"   ❌ Erreur execution: {e}")

# 6. Test import
print("\n6. 📦 TEST IMPORTS:")
try:
    import moviepy
    print("   ✅ moviepy importé")
except ImportError as e:
    print(f"   ❌ moviepy: {e}")

try:
    import requests
    print("   ✅ requests importé")
except ImportError as e:
    print(f"   ❌ requests: {e}")

print("\n" + "=" * 50)
print("🔍 DEBUG TERMINÉ")
print("=" * 50)