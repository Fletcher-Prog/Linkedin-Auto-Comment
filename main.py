import Utils
import time
from Poste import Poste 
from random import randint
from datetime import datetime
import env

lancer = True
nbPosteInteractionAujourdhui = 250


Utils.connextion(env.emailLinkedin,env.passwordLinkedin,15)

i = 0

while True :
    
    time.sleep(1/2)

    # Refresh du navigateure et remise a 0 des postes crée
    if datetime.now().strftime("%H:%M:%S") == "00:00:00":
        Poste.nbPosteCree     = 0
        Poste.nbPosteInFeed   = 0
        Poste.nbDejaCommenter = 0
        Poste.countAddPostInPage = 0
        i = 0
        Utils.bot.refresh()
        

    if datetime.now().strftime("%H:%M:%S") == "07:00:00" or lancer == True:
        
        lancer = False
        
        if lancer != True :
            nbPosteInteractionAujourdhui = randint(140,280)
        
        
        Utils.logging.info("Nombre de poste aujourd'hui : {tkt} ".format( tkt=nbPosteInteractionAujourdhui ) )

        while True :

            tkt = Poste(Utils.bot)

            print ( tkt.toString() )            
            
            if Poste.nbDejaCommenter >= nbPosteInteractionAujourdhui :
                boucleFini :bool = True
                break
            
            # Temps d'attente pour pas se   faire cramé
            tempAttente = 0

            # Verification que nous somme sur le bonne onglet
            for handle in Utils.bot.window_handles:
                if "Feed | LinkedIn" in Utils.bot.title :
                    break
                Utils.bot.switch_to.window(handle)


            
            tempAttente = randint(15,30)
            Utils.logging.info( "Attente de {temp} s commencer a {heure} ".format( heure=datetime.now().strftime("%H:%M:%S"), temp=tempAttente ) )
            time.sleep(tempAttente)

            if randint( 0,2 ) == 1 :
                tempAttente = randint(30,60)
                Utils.logging.info( "Attente de {temp} s commencer a {heure} ".format( heure=datetime.now().strftime("%H:%M:%S"), temp=tempAttente ) )
                time.sleep(tempAttente)

            if randint( 0,5 ) == 4:
                tempAttente = randint(60,120)
                Utils.logging.info( "Attente de {temp} s commencer a {heure} ".format( heure=datetime.now().strftime("%H:%M:%S"), temp=tempAttente ) )
                time.sleep(tempAttente)
            
            if randint( 0,15 ) == 14 :
                tempAttente = randint(120,240)
                Utils.logging.info( "Attente de {temp} s commencer a {heure} ".format( heure=datetime.now().strftime("%H:%M:%S"), temp=tempAttente ) )
                time.sleep(tempAttente)            
            
            i += 1  

        if boucleFini == True:
            boucleFini = False
            Utils.logging.info( "Le nombre de poste commenter et de {i} \t et le nombre de pose a faire aujourd'hui {i1} ".format( i=i, i1=nbPosteInteractionAujourdhui ) ) 



