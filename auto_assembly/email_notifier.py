#!/usr/bin/env python3
"""
Système de notification email pour validation de scripts
"""

import os
import json
import requests
from datetime import datetime

class EmailNotifier:
    def __init__(self):
        self.api_key = os.getenv('SENDGRID_API_KEY')
        self.from_email = "vaitea.atwork@gmail.com"  # Ton email vérifié
        self.template_id = "d-1feb56871d7a44cabfd0e1922935d996"  # ⚠️ REMPLACER APRÈS
        
    def send_script_approval_request(self, scripts, webhook_url):
        """Envoie un email avec les scripts à valider"""
        
        # Construction des données pour le template
        template_data = {
            "subject": f"🎬 VALIDATION REQUISE - Scripts YouTube du {datetime.now().strftime('%d/%m/%Y')}",
            "date": datetime.now().strftime('%d/%m/%Y'),
            "timestamp": datetime.now().strftime('%H:%M'),
            "scripts": scripts,
            "webhook_base": webhook_url
        }
        
        # Préparation données SendGrid
        data = {
            "personalizations": [{
                "to": [{"email": "vaiatwork05@gmail.com"}],  # Ton email
                "dynamic_template_data": template_data
            }],
            "from": {"email": self.from_email},
            "template_id": self.template_id
        }
        
        # Envoi via SendGrid
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                "https://api.sendgrid.com/v3/mail/send",
                headers=headers,
                data=json.dumps(data),
                timeout=10
            )
            
            if response.status_code == 202:
                print("✅ Email de validation envoyé !")
                return True
            else:
                print(f"❌ Erreur envoi email: {response.status_code}")
                print(f"📄 Détails: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Exception envoi email: {e}")
            return False

def test_email():
    """Teste l'envoi d'email"""
    notifier = EmailNotifier()
    
    # Scripts de test
    scripts_test = [
        {
            "title": "3 SECRETS HISTORIQUES CACHÉS",
            "content": "• Les pyramides construites par des ouvriers payés\n• Christophe Colomb pas le premier\n• Napoléon de taille moyenne"
        },
        {
            "title": "RÉVÉLATIONS SCIENTIFIQUES CHOQUANTES", 
            "content": "• La physique quantique remet tout en question\n• Découverte récente qui change tout\n• Ce que les labos cachent"
        }
    ]
    
    # Webhook de test (on le configurera après)
    webhook_test = "https://webhook.test.com"
    
    success = notifier.send_script_approval_request(scripts_test, webhook_test)
    
    if success:
        print("🎉 Test email réussi ! Vérifie ta boîte mail.")
    else:
        print("💥 Test email échoué.")
    
    return success

if __name__ == "__main__":
    test_email()
