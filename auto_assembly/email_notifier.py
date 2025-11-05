#!/usr/bin/env python3
"""
Email Notifier - Version avec déclenchement direct GitHub
"""

import os
import json
import requests
import urllib.parse
from datetime import datetime

class EmailNotifier:
    def __init__(self):
        self.api_key = os.getenv('SENDGRID_API_KEY')
        self.from_email = "vaitea.atwork@gmail.com"
        self.to_email = "vaitea.atwork@gmail.com"
        
    def send_script_approval(self, scripts):
        """Envoie l'email avec les scripts"""
        
        html_content = self._build_email_content(scripts)
        
        data = {
            "personalizations": [{
                "to": [{"email": self.to_email}],
                "subject": f"Scripts YouTube - {datetime.now().strftime('%d/%m/%Y')}"
            }],
            "from": {"email": self.from_email},
            "content": [{"type": "text/html", "value": html_content}]
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            "https://api.sendgrid.com/v3/mail/send",
            headers=headers,
            data=json.dumps(data)
        )
        
        success = response.status_code == 202
        if success:
            print("Email envoyé")
        else:
            print(f"Erreur email: {response.status_code} - {response.text}")
        
        return success
    
    def _build_email_content(self, scripts):
        """Construit le contenu HTML avec liens de déclenchement direct"""
        
        html = """
        <html>
        <body style="font-family: Arial; margin: 20px; background: #f5f5f5;">
            <div style="max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px;">
                <div style="background: #4CAF50; color: white; padding: 20px; border-radius: 5px; text-align: center;">
                    <h1>Scripts YouTube - Validation</h1>
                    <p>Date: """ + datetime.now().strftime('%d/%m/%Y') + """</p>
                </div>
        """
        
        for i, script in enumerate(scripts):
            # URL de déclenchement direct GitHub
            script_json = urllib.parse.quote(json.dumps(script))
            approve_url = f"https://github.com/Vaiatwork05/Youtube-Assistant/actions/workflows/video_production.yml?inputs=script_id={i}&script_data={script_json}"
            
            html += f"""
                <div style="border: 2px solid #4CAF50; padding: 15px; margin: 15px 0; border-radius: 10px;">
                    <h3>Option {i+1}: {script['title']}</h3>
                    <div style="color: #666; line-height: 1.5; margin: 10px 0; white-space: pre-line;">{script['content']}</div>
                    <a href="{approve_url}" 
                       style="display: block; padding: 12px; background: #4CAF50; color: white; text-align: center; 
                              text-decoration: none; border-radius: 5px; font-weight: bold;">
                        Produire cette vidéo
                    </a>
                </div>
            """
        
        html += """
            </div>
        </body>
        </html>
        """
        
        return html

def main():
    """Charge les scripts et envoie l'email"""
    try:
        with open('scripts.json', 'r', encoding='utf-8') as f:
            scripts = json.load(f)
        print("Scripts chargés depuis scripts.json")
    except FileNotFoundError:
        print("Fichier scripts.json non trouvé - utilisation de scripts de test")
        scripts = [
            {
                "title": "Script Test",
                "content": "Contenu de test pour validation"
            }
        ]
    
    notifier = EmailNotifier()
    success = notifier.send_script_approval(scripts)
    
    if not success:
        exit(1)

if __name__ == "__main__":
    main()
