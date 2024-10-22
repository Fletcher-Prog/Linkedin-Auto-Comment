import re 
import Utils

import time
import openai 
import json
from random import randint
from datetime import datetime
from  Utils.Exception import *
import env


import pyperclip
from selenium import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, WebDriverException, StaleElementReferenceException, ElementNotInteractableException, ElementClickInterceptedException

class Poste(): 
    
    nbPosteCree            : int = 0
    nbPosteInFeed          : int = 0
    nbDejaCommenter        : int = 0
    countAddPostInPage     : int = 0
    tableauDeMotMotsExclus : str = ["recherche d'alternance","recherche de stage","Je suis actuellement à la recherche ","Je suis à la recherche "]
    nomCreateurAEsquiver   : str = ["nathalie scott","Linkedin"]

    # Définition et assignation d'un valeur au attribut d'instance
    def __init__( self, bot:WebDriver ) -> None:
        
        self.__idPoste   :str        = None
        self.__bio       :str        = None
        self.__texte     :str        = None
        self.estCommente :bool       = False
        self.estLiker    :bool       = False
        self.__divContentLePoste     = None
        self.auteur      :str        = None
        self.__numPoste  :int        = Poste.nbPosteInFeed
        self.__bot       :WebDriver  = bot
        self.actions                 = ActionChains(self.__bot)


        
        # Gestion en cas d'erreure que sa soit sur la divContentLePoste, l'idBlockInteration ou la récuperation de la bio échou 
        # cela veut dire que le poste n'est pas un poste valide
        # 
        while True :

            try:
                # Si 3 fois d'affiler le poste n'est pas trouvais je refrachit le page et je remet a 0 le compteur qui permet de chercher le poste
                if Poste.countAddPostInPage >= 3 :
                    Poste.nbPosteInFeed = 0
                    self.__bot.refresh()
                    Utils.logApp.info(" Page Refresh suite a de nombreux refus de poste " )

                    if randint( 0,2 ) == 1 :
                        tempAttente = randint(30,60)
                        Utils.logApp.info( "Attente de {temp} s commencer a {heure} ".format( heure=datetime.now().strftime("%H:%M:%S"), temp=tempAttente ) )
                        time.sleep(tempAttente)

                    if randint( 0,35 ) == 4:
                        tempAttente = randint(60,120)
                        Utils.logApp.info( "Attente de {temp} s commencer a {heure} ".format( heure=datetime.now().strftime("%H:%M:%S"), temp=tempAttente ) )
                        time.sleep(tempAttente)
                    
                    if randint( 0,115 ) == 14 :
                        tempAttente = randint(120,240)
                        Utils.logApp.info( "Attente de {temp} s commencer a {heure} ".format( heure=datetime.now().strftime("%H:%M:%S"), temp=tempAttente ) )
                        time.sleep(tempAttente)

                
                # Compteur auto incrementé qui permet d'aller chercher la div contenant un poste en fonction du numéro du compteur
                self.__divContentLePoste = WebDriverWait(self.__bot ,20).until(EC.presence_of_element_located((By.XPATH, '//*[@data-finite-scroll-hotkey-item="{number}"]'.format( number=self.__numPoste ))))        
                
                self.__bot .execute_script("arguments[0].scrollIntoView(true);", self.__divContentLePoste )
                
                # Verification que les interaction  (liker,reposter,send) son dispo si non on ne charge pas d'instance pour ce poste   
                self.__divContentLePoste.find_element( By.XPATH,".//*[ contains(@class, 'update-v2-social-activity')]" ).get_attribute('id')

                # Assignation de l'id du poste
                self._setIdPoste()
                
                # Récuperation de la bio du poste si possible 
                self.getBio()

                # l'intégrité du texte 
                self.getIntergraliteTextePoste() 

                # Récupére le nom de l'auteur 
                self.getNameAuteur()


                # Verif pour ne pas commenter certain poste qui contient des mots clé prés défini dans le tableau
                for element in Poste.tableauDeMotMotsExclus :
                    if element.lower() in self.__texte.lower()  :
                        Utils.logApp.info("\n Poste Skipé : contient des mot clé non autorisé \n " )
                        raise PosteNonValable()
                
                # Verif pour ne pas commenter certain auteur défini dans un tableau
                for element in Poste.nomCreateurAEsquiver :
                    if element.lower() in self.auteur.lower()  :
                        Utils.logApp.info("\n Poste Skipé : Auteur non autorisé \n " )
                        raise PosteNonValable()
                                        
                # Chiffre Auto incrementé pour avoir le nombre de poste crée
                Poste.nbPosteCree   += 1
                Poste.nbPosteInFeed += 1
                Poste.countAddPostInPage = 0
                
                break
            
            except ( PosteNonValable, WebDriverException, IdNonTrouvais, AuteurNeDoitPasEtreCommenter, AuteurNonTrouvais ) :
                
                # Utils.logApp.info("nb Poste crée : {tkt}".format( tkt=Poste.nbPosteCree ) )
                Poste.nbPosteCree   += 1
                Poste.nbPosteInFeed += 1
                Poste.countAddPostInPage += 1
                self.__numPoste = Poste.nbPosteInFeed
                self._addPosteInPage()

        
        # Commenter et liker poste
        if self.commenter() == "True" :
            self.liker()
            Utils.logApp.info( self.toString() )
        elif Poste.nbDejaCommenter >= 5 :
            self._addPosteInPage()
            Utils.logApp.info("\n Page Refresh suite a de nombreux poste deja commenter \n " )

        
        # Verification que les nombres de page et de 10 donc il faut en charger d'autre
        if Poste.nbPosteCree % 6 == 0:
            self._addPosteInPage()
    
    def toString( self ):
        
        Utils.logFonction.info ( " \n Id du poste : {idPoste} \n Auteur du poste {AuteurPoste} \n Bio du poste : {BioPoste} \n Le poster et liker ? {estLiker} \n Le poster et commenter ? {estCommenter} \n ".format(AuteurPoste=self.auteur,idPoste=self.__idPoste,BioPoste=self.__bio,estLiker=self.estLiker,estCommenter=self.estCommente ) )
        
        return " \n Id du poste : {idPoste} \n Auteur du poste : {AuteurPoste} \n Bio du poste : {BioPoste} \n Le poster et liker ? {estLiker} \n Le poster et commenter ? {estCommenter} \n Nombre de poste commenter et liker :  {nbPosteCommenter}".format(AuteurPoste=self.auteur,idPoste=self.__idPoste,BioPoste=self.__bio[0:18],estLiker=self.estLiker,estCommenter=self.estCommente, nbPosteCommenter=Poste.nbDejaCommenter )

    def _setIdPoste( self ) -> str:
        
        Utils.logFonction.info( "_setIdPoste :" )

        try :
            __idPoste = self.__divContentLePoste.find_elements(By.XPATH, "//div[contains(@class, 'feed-shared-update-v2') and contains(@class, 'feed-shared-update-v2--minimal-padding') and contains(@class, 'full-height') and contains(@class, 'relative') and contains(@class, 'feed-shared-update-v2--e2e') and contains(@class, 'artdeco-card')]")[self.__numPoste].get_attribute("id")
            self.__bot .execute_script("arguments[0].scrollIntoView(true);", self.__divContentLePoste.find_elements(By.XPATH, "//div[contains(@class, 'feed-shared-update-v2') and contains(@class, 'feed-shared-update-v2--minimal-padding') and contains(@class, 'full-height') and contains(@class, 'relative') and contains(@class, 'feed-shared-update-v2--e2e') and contains(@class, 'artdeco-card')]")[self.__numPoste] )

        except IndexError :
                
                try :

                    __idPoste = self.__divContentLePoste.find_elements(By.XPATH, "//div[contains(@class, 'feed-shared-update-v2') and contains(@class, 'feed-shared-update-v2--minimal-padding') and contains(@class, 'full-height') and contains(@class, 'relative') and contains(@class, 'artdeco-card')]")[self.__numPoste].get_attribute("id")
                    self.__bot .execute_script("arguments[0].scrollIntoView(true);", self.__divContentLePoste.find_elements(By.XPATH, "//div[contains(@class, 'feed-shared-update-v2') and contains(@class, 'feed-shared-update-v2--minimal-padding') and contains(@class, 'full-height') and contains(@class, 'relative') and contains(@class, 'artdeco-card')]")[self.__numPoste])
                
                except IndexError :

                    Utils.logFonction.info( "\t Sortie : id non trouvais " )

                    raise IdNonTrouvais()


                                
        # Verification que l'id du poste et sous la bonne forme
        # qu'il correspond a ember suivit de 1 a 6 chiffre
        if __idPoste != None :
            
            if re.match( r'ember\d{1,6}$' , __idPoste ):
                self.__idPoste = __idPoste
                Utils.logFonction.info( "\t Sortie : id trouvais " )
                return "True"
            
            else:
                __idPoste = None
                Utils.logFonction.info( "\t Sortie : id non valide " )
                return "L'id donne n'est pas bon"
        
        
    def getIdPoste( self ) -> str:
        if self.__idPoste != None:
            return self.__idPoste
        
        else:
            return "Aucun id na était définit pour se poste"
    

    
    def getBio( self ) -> str:

        Utils.logFonction.info( "getBio :" )

        try:

            if self.__bio == None and self.__idPoste != None :
                
                Utils.logFonction.info( "\t Etat : cas 1  " )
                
                self.__bio = WebDriverWait(self.__divContentLePoste,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#fie-impression-container > div.feed-shared-update-v2__description-wrapper.mr2"))).text
            
        
        except TimeoutException :

            try:

                if self.__bio == None and self.__idPoste != None :
                    Utils.logFonction.info( "\t Etat : cas 2  " )
                    self.__bio = WebDriverWait(self.__divContentLePoste,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#fie-impression-container > div:nth-child(1) > div:nth-child(3) > div:nth-child(2)"))).text
                    
            except TimeoutException :
                try:

                    if self.__bio == None and self.__idPoste != None :
                        
                        Utils.logFonction.info( "\t Etat : cas 3 " )
                        
                        self.__bio = WebDriverWait(self.__divContentLePoste,5).until(EC.presence_of_element_located((By.CLASS_NAME, "feed-shared-update-v2__description-wrapper"))).text                   
                
                except TimeoutException :
                    Utils.logFonction.info( "\t Sortie : Poste non valide" )
                    raise PosteNonValable()
                
        Utils.logFonction.info( "\t Sortie" )
        
        return self.__bio
    
    def getIntergraliteTextePoste( self ):

        Utils.logFonction.info( "Entre dans la fonction getIntergraliteTextePoste " )

        if self.__texte == None :

            try:
                Utils.logFonction.info( "\t Etat : cas 1 {idposte}".format(idposte=self.__idPoste)  )  
                self.__texte = WebDriverWait(self.__bot,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#{posteId} > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2)".format(posteId=self.__idPoste)))).text            
        
            except TimeoutException :
                    try:
                        Utils.logFonction.info( "\t Etat : cas 2 {idposte}".format(idposte=self.__idPoste)  ) 
                            
                        self.__texte = WebDriverWait(self.__bot,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#{posteId} > div > div > div.fie-impression-container > div.feed-shared-update-v2__description-wrapper > div.feed-shared-inline-show-more-text.feed-shared-update-v2__description.feed-shared-inline-show-more-text--minimal-padding.feed-shared-inline-show-more-text--3-lines > div > span > span".format(posteId=self.__idPoste)))).text            
                
                    except TimeoutException :
                        Utils.logFonction.info( "\t Sortie : Poste non valide" )
                        raise PosteNonValable()
        else:
            return self.__texte

        Utils.logFonction.info( "Sortie " )
    

    def liker( self ) -> bool :
        
        Utils.logFonction.info( "liker : " )
        
        cpt = 0
        
        while cpt < 10 :
            # Méthode par le XPATH
            try:
                # Récuperation de la div interaction de chaque poste en fonction de sa position dans la héarchie du fiche
                __divInteractionByXpath = WebDriverWait(self.__divContentLePoste ,6).until(EC.presence_of_element_located((By.XPATH,"//*[@id='{idPoste}']/div[{numDeDiv}]".format(idPoste=self.__idPoste,numDeDiv=cpt))))

                # Récupération de tout les buttons de la div interaction 
                __divInteractionByXpath = __divInteractionByXpath.find_elements(By.XPATH,".//button")
                # Si aucun boutton like trouvais alors modifier le chemein menant a la div interaction et re essayer
                # Les 2 boucle for permet juste de s'assure que tout les bouttons qui on le lable like son clicker

                nbButtonLike = 0
                for button in __divInteractionByXpath :
                    if button.text == "Like" or button.text == "J’aime":
                        nbButtonLike +=1
                

                nbButtonLikeClicker = 0
                for button in __divInteractionByXpath :
                    
                    Utils.logFonction.info ( button.text )
                    
                    if button.text == "Like" or button.text == "J’aime":
                        
                        # Déplacer le curseur de la souris sur l'élément
                        self.actions.move_to_element(button)

                        # Cliquer sur l'élément
                        self.actions.click()

                        # Exécuter les actions
                        self.actions.perform()

                        nbButtonLikeClicker +=1
                        
                        # si il ya 3 ou plus de poste alors j'en like 2 sinon j'en like 1
                        if nbButtonLike >= 3 and nbButtonLikeClicker == 2 or nbButtonLike < 3 and nbButtonLikeClicker == 1:
                            self.estLiker = True
                            Utils.logFonction.info( "\t Sortie : cas 1 valide" )
                            return True
                                    
            except (TimeoutException or StaleElementReferenceException):
                Utils.logFonction.info ( "1: Div Interaction non Trouvais fonction liker" )
                
                # Méthode par le CSS_Selector
                try:
                    # Récuperation de la div interaction de chaque poste en fonction de sa position dans la héarchie du fiche
                    __divInteraction = WebDriverWait(self.__divContentLePoste ,5).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#{idPoste} > div > div.update-v2-social-activity".format(idPoste=self.__idPoste))))
                
                    # Récupération de tout les buttons de la div interaction
                    __divInteraction = __divInteraction.find_elements(By.XPATH,".//button")
                    
                    # Si aucun boutton like trouvais alors modifier le chemein menant a la div interaction et re essayer
                    # Les 2 boucle for permet juste de s'assure que tout les bouttons qui on le lable like son clicker

                    nbButtonLike = 0
                    for button in __divInteraction :
                        if button.text == "Like" or button.text == "J’aime":
                            nbButtonLike +=1


                    nbButtonLikeClicker = 0
                    for button in __divInteraction :
                        
                        Utils.logFonction.info ( button.text )
                        
                        if button.text == "Like" or button.text == "J’aime":

                            # Déplacer le curseur de la souris sur l'élément
                            self.actions.move_to_element(button)

                            # Cliquer sur l'élément
                            self.actions.click()

                            # Exécuter les actions
                            self.actions.perform()

                            nbButtonLikeClicker +=1

                            # si il ya 3 ou plus de poste alors j'en like 2 sinon j'en like 1
                            if nbButtonLike >= 3 and nbButtonLikeClicker == 2 or nbButtonLike < 3 and nbButtonLikeClicker == 1:
                                self.estLiker = True
                                
                                Utils.logFonction.info( "\t Sortie : cas 2 valide" )

                                return True

                
                except TimeoutException:
                    Utils.logFonction.info ( "2: Div Interaction non Trouvais fonction liker" )
                    pass
                    
            cpt+=1

    
    def __genereCommentaire( self ) -> str :

        while True :

            Utils.logFonction.info( "__genereCommentaire" )

            Utils.logging.getLogger("openai").setLevel(Utils.logging.CRITICAL)

            # OPENAI
            OPENAI_API_KEY = env.OPENAI_API_KEY
            gptIdAssistant = env.gptIdAssistant

            client = openai.OpenAI(api_key=OPENAI_API_KEY)

            # Ciblage de l'assistant a utilise
            my_assistants = client.beta.assistants.retrieve(gptIdAssistant)
            #Utils.logApp.info(my_assistants)
            
            # Création du thread pour la conversation avec l'assistant
            thread = client.beta.threads.create()
            
            if self.__bio == None :
                bioPoste = self.getIntergraliteTextePoste()
            else:
                bioPoste = self.__bio
                bioPoste = re.sub(r'\s+',' ', bioPoste)

            # Création du message
            client.beta.threads.messages.create( thread.id,role="user", content=bioPoste )

            # Initialisation du thread de discution avec le bonne étudiant
            run = client.beta.threads.runs.create(
                thread.id,
                assistant_id= gptIdAssistant
            )

            # Envoi du message
            runStatus = client.beta.threads.runs.retrieve(thread_id=thread.id,run_id=run.id)
            
            nbRequette = 0

            # Attendre que l'ai réponde
            while runStatus.status != 'completed' :
                    
                    time.sleep(1)

                    runStatus = client.beta.threads.runs.retrieve(thread_id=thread.id,run_id=run.id)
                    
                    nbRequette += 1

                    if nbRequette == 5 :
                        break
            
            if runStatus.status == 'completed':
                messagesResponse = client.beta.threads.messages.list(thread.id)

                # "Convestion de la réponde en JSON
                messagesResponseJson = json.loads(messagesResponse.model_dump_json())
                
                commentaire = messagesResponseJson['data'][0]['content'][0]['text']['value']
                
                # Suppresion des guieummés
                sRet = ""
                for caractere in commentaire:
                    if not caractere == '"':
                        sRet += caractere
                
                Utils.logFonction.info( "\t Sortie : valide \n \t, commentaire : {tkt} ".format( tkt=sRet ) )

                return  sRet
            
    

    def estCommenter( self ) -> bool:

        Utils.logFonction.info( "estCommenter :" )

        if self.__bio == None :
            bioPoste = self.getBio().strip()
        else:
            bioPoste = self.__bio.strip()

        bioPoste = re.sub(r'\s+', ' ', bioPoste)
        
        bioPoste += '\n'

        with open("Saveposte/posteDejaCommenter.txt","r") as file:
        
            listeBioPoste = file.readlines()
        
        file.close()


        if bioPoste in listeBioPoste:
            
            Utils.logFonction.info( "\t Sortie : True" )

            return True
        
        Utils.logFonction.info( "\t Sortie : False " )
        return False


    def commenter( self ) -> str:
        
        Utils.logFonction.info( "commenter : " )
        
        if not self.estCommenter():
            
            # récupration et click sur le button commentaire qui permet d'activer le chant de saisie 
            buttonComment =  self.__divContentLePoste.find_element(By.CSS_SELECTOR, 'button.artdeco-button.comment-button')
            element = self.__bot.find_element(By.ID,"{idButton}".format(idButton=buttonComment.get_attribute("id")))
            self.__bot.execute_script("arguments[0].click();", element)

            # Saisie du commentaire
            try :
                
                inputComment = WebDriverWait( self.__divContentLePoste, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ql-editor' )))
                inputComment = inputComment.find_element(By.TAG_NAME,'p')
                inputComment.clear()
            
            except TimeoutException :
                Utils.logFonction.info("\t Sortie : Poste non commentable")
                return

            except ElementNotInteractableException :
                Utils.logFonction.info ( " \n error : Input commentaire non touvais " )
                WebDriverWait(self.__bot,5).until(EC.presence_of_element_located((By.CLASS_NAME, 'artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--2 artdeco-button--tertiary ember-view artdeco-modal__dismiss' ))).click()
                
            
            # géneration du commentaire
            commentaire = self.__genereCommentaire()

            while True:
                try :
                    pyperclip.copy( commentaire )

                    inputComment.send_keys(Keys.CONTROL + "v")
                    break

                except WebDriverException as e :
                    commentaire = self.__genereCommentaire()
                    print ( "Erreure copier coller " )

            # récupration et click sur le button poste ou publier qui permet selon langue de publie le commentaire
            
            try:
                Utils.logFonction.info( "\t Etat : cas 1 " )
                buttonComment = WebDriverWait( self.__divContentLePoste, 5).until(EC.presence_of_all_elements_located((By.XPATH, './/button[@class="m2 artdeco-button artdeco-button--1 artdeco-button--tertiary ember-view"]' )))
            except TimeoutException:
                try:
                    Utils.logFonction.info( "\t Etat : cas 2 " )
                    buttonComment = WebDriverWait( self.__divContentLePoste, 5).until(EC.presence_of_all_elements_located((By.XPATH, './/button[@class="comments-comment-box__submit-button mt3 artdeco-button artdeco-button--1 artdeco-button--primary ember-view"]' )))
                except TimeoutException:
                    Utils.logFonction.info( "\t Etat : cas 3 " )
                    buttonComment = WebDriverWait( self.__divContentLePoste, 5).until(EC.presence_of_all_elements_located((By.XPATH, './/button[@class="comments-comment-box__submit-button--cr artdeco-button artdeco-button--1 artdeco-button--primary ember-view"]' )))

            try :
                buttonComment[0].click()
                Poste.nbDejaCommenter +=1
                Utils.logFonction.info( "Sortie \n" )
                return
            except ElementClickInterceptedException :
                self.actions.move_to_element(buttonComment[0].find_element(By.XPATH, ".."))
                self.actions.click()
                self.actions.perform()
                Poste.nbDejaCommenter +=1
                Utils.logFonction.info( "Sortie 2 \n" )

                
            
            # Ajoute de la bio au fiche pour ne pas re commenter le poste
            # Traitement des espaces et autres caractére spéciaux est ajouts du délimitateur

            if self.__bio == None :
                bioPoste = self.getBio().strip()
            else:
                bioPoste = self.__bio.strip()

            bioPoste = re.sub(r'\s+', ' ', bioPoste)
            
            bioPoste += "\n"
                
            with open("Saveposte/posteDejaCommenter.txt",'a') as file :
                
                file.write(bioPoste)
                
                file.close()

            with open("Saveposte/posteEtComment.txt",'a') as file :

                bioPoste = "Bio poste : " + bioPoste + "Commentaire : " + commentaire + "\n\n\n\n\n\n"
                
                file.write(bioPoste)
                
                file.close()
            
            Utils.logFonction.info( "\t Sortie : poste commenter" )
            self.estCommente = True
            return "True"
        else:
            
            Utils.logFonction.info( "\t Sortie : étant déjà commenter" )
            Poste.nbDejaCommenter += 1
            self.estCommente = False
            
            
            
            return "Poste déjà commenter"


    def _addPosteInPage( self ):
        
        Utils.logFonction.info( "_addPosteInPage" )
    
        # Récupération est click sur le button qui permet d'ajouter des postes dans le feed
        bouttonAddPoste = []

        try :
            bouttonAddPoste = self.__bot.find_elements( By.XPATH,'//button[@class="artdeco-button artdeco-button--secondary mv5 t-14 t-black t-normal"][@type="button"]')
        
            if len( bouttonAddPoste ) > 0 :
                bouttonAddPoste[0].click()
                time.sleep(5)
                return "ok"
            
            bouttonAddPoste = self.__bot.find_elements( By.XPATH, '//button[@class="artdeco-button feed-new-update-pill__new-update-button Elevation-6dp justify-flex-start"][@type="button"]')

            #print ( bouttonAddPoste )

            if len( bouttonAddPoste ) > 0 :

                bouttonAddPoste[0].click()
                time.sleep(5)
                return "ok"

            bouttonAddPoste = self.__bot.find_elements( By.XPATH, '//button[@class="artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--full artdeco-button--secondary ember-view scaffold-finite-scroll__load-button"]')

            #print ( bouttonAddPoste )

            if len( bouttonAddPoste ) > 0 :

                bouttonAddPoste[0].click()
                time.sleep(5)
                return "ok"
        
        except ( StaleElementReferenceException, ElementNotInteractableException ):
            self.__bot.refresh()
            Poste.nbPosteInFeed = 0

            
                
        Utils.logFonction.info( "Sortie de la fonction _addPosteInPage" )



    
    def getNameAuteur( self ):

        Utils.logFonction.info( "getNameAuteur " )
        
        try :
        
            Utils.logFonction.info( "\t Etat : cas 1 {idposte}".format(idposte=self.__idPoste)  ) 
            self.auteur =  WebDriverWait( self.__divContentLePoste, 5 ).until( EC.presence_of_element_located( ( By.CSS_SELECTOR, '#{idPoste} > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1) > span:nth-child(1) > span:nth-child(1) > span:nth-child(1) > span:nth-child(1)'.format( idPoste=self.__idPoste ) ) ) ).text
        
        except TimeoutException :
                try :
                
                    Utils.logFonction.info( "\t Etat : cas 2 {idposte}".format(idposte=self.__idPoste)  ) 
                    self.auteur =  WebDriverWait(self.__divContentLePoste, 5).until( EC.presence_of_element_located( ( By.CSS_SELECTOR, "#{idPoste} > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1) > span:nth-child(1) > span:nth-child(1) > span:nth-child(1) > span:nth-child(1)".format(idPoste=self.__idPoste ) ) ) ).text

                except TimeoutException :
                    try :
                
                        Utils.logFonction.info( "\t Etat : cas 3 {idposte}".format(idposte=self.__idPoste)  ) 
                        self.auteur =  WebDriverWait(self.__divContentLePoste, 5).until( EC.presence_of_element_located( ( By.CSS_SELECTOR, "#{idPoste} > div > div > div.fie-impression-container > div.relative > div.update-components-actor.display-flex > div > div > a.app-aware-link.update-components-actor__meta-link > span.update-components-actor__title > span.update-components-actor__name.hoverable-link-text.t-14.t-bold.t-black > span > span:nth-child(1)".format(idPoste=self.__idPoste ) ) ) ).text

                    except TimeoutException : 
                        try : 
                
                            Utils.logFonction.info( "\t Etat : cas 4 {idposte}".format(idposte=self.__idPoste)  ) 
                            self.auteur =  WebDriverWait(self.__bot, 5).until( EC.presence_of_element_located( ( By.CSS_SELECTOR, "#{idPoste} > div > div > div.fie-impression-container > div.relative > div.update-components-actor.display-flex > div > div > a.app-aware-link.update-components-actor__meta-link > span.update-components-actor__title > span.update-components-actor__name.hoverable-link-text.t-14.t-bold.t-black > span > span:nth-child(1)".format(idPoste=self.__idPoste ) ) ) ).text

                        except TimeoutException : 
                            try :                 
                                Utils.logFonction.info( "\t Etat : cas 5 {idposte}".format(idposte=self.__idPoste)  ) 
                                self.auteur =  WebDriverWait(self.__divContentLePoste, 5).until( EC.presence_of_element_located( ( By.CSS_SELECTOR, "#{idPoste}  > div > div > div.fie-impression-container > div.relative > div.update-components-actor.display-flex.update-components-actor--with-control-menu > div > div > a > span.update-components-actor__title > span > span > span:nth-child(1) > span".format(idPoste=self.__idPoste ) ) ) ).text
                           
                            except TimeoutException : 
                                try :                 
                                    Utils.logFonction.info( "\t Etat : cas 6 {idposte}".format(idposte=self.__idPoste)  ) 
                                    self.auteur =  WebDriverWait(self.__divContentLePoste, 5).until( EC.presence_of_element_located( ( By.CSS_SELECTOR, "#{idPoste} > div > div > div.fie-impression-container > div.relative > div.update-components-actor.display-flex.update-components-actor--with-control-menu > div > div > a.app-aware-link.update-components-actor__meta-link > span.update-components-actor__title > span > span > span:nth-child(1) > span".format(idPoste=self.__idPoste ) ) ) ).text
                                except TimeoutException : 
                                        
                                    Utils.logFonction.info( "\t Sortie : auteur non trouvais {idposte}".format(idposte=self.__idPoste) )
                                    raise AuteurNonTrouvais()



        if self.auteur.lower() in Poste.nomCreateurAEsquiver:
            raise AuteurNeDoitPasEtreCommenter()