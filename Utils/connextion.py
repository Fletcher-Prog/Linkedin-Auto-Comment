from selenium.webdriver.common.keys import Keys
import random
import json
import pickle
import time
import Utils
from os.path import exists
import json


def connextion(email,mdp,timeSleep=25):
    
    Utils.logging.info( "Connection en cours " )
    
    bot = Utils.bot

    # Aller à la page de connexion LinkedIn
    bot.get('https://www.linkedin.com/login')
    
    # Trouver et remplir le champ du nom d'utilisateur/email
    email_field = bot.find_element("id", "username")

    for lettreEmail in email :
        
        email_field.send_keys(lettreEmail)
        
        random.uniform(0.1,0.45)
            
            
        
    # Trouver et remplir le champ du mot de passe
    password_field = bot.find_element("id", "password")
    
    for lettrePassword in mdp :
                
        password_field.send_keys(lettrePassword)

        random.uniform(0.1,0.45)
        
    # Soumettre le formulaire
    password_field.send_keys(Keys.RETURN)
    
    time.sleep(timeSleep)