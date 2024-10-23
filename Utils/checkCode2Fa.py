import Utils


import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException




def checkCode2Fa() -> None :
    
    bot = Utils.bot

    # texte pour savoir que je suis sur une page qui demande un cod 2FA
    # Enter the code we’ve sent to phone number ending 
    try :
        WebDriverWait( bot, 10 ).until( EC.presence_of_element_located( ( By.XPATH, "//*[contains(text(), 'Enter the code we’ve sent to phone number ending')]" ) ) )
    except TimeoutException :
        print( "texte non trouvais" )

    # input ou je doit saisir le code 
    # 

    try :
        chantDeSaisie = WebDriverWait(bot,10).until(EC.presence_of_element_located( ( By.XPATH, '//*[@aria-label="Please enter the code here"]' ) ) )
        chantDeSaisie.send_keys( input( "Quelle est le code de vérification ? :)  " ) )

    except TimeoutException :
        print( "input non trouvais" )

    # Button ou je doit appuiye une fois le code saisie
    # aria-label="Submit code"

    try :
        bouttonValidation = WebDriverWait(bot,10).until(EC.presence_of_element_located( ( By.XPATH, '//*[@aria-label="Submit code"]' ) ) )
        bouttonValidation.click()

    except TimeoutException :
        print( "boutton de validation non trouvais" )

    
    time.sleep(5)