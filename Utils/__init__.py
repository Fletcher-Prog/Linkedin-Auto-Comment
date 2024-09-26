from .connextion import *
from .Exception import *
from .saveCookie import *

import pyperclip


# Selenuim
# Configuration et lancement de WebDriver
from selenium_stealth import stealth
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options



# Systeme de logging
import logging
import os

# Créer un répertoire pour les logs s'il n'existe pas
log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_file = os.path.join(log_directory, 'app.log')

logging.basicConfig( filename="logs/log.txt", level=logging.INFO, format='%(asctime)s - %(message)s', datefmt="%d-%b-%y %H:%M:%S : " ) 




options = Options()
options.add_argument("--log-level=3")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
# disable the AutomationControlled feature of Blink rendering engine
options.add_argument('--disable-blink-features=AutomationControlled')
# disable pop-up blocking
options.add_argument('--disable-popup-blocking')
# start the browser window in maximized mode
options.add_argument('--start-maximized')
# disable extensions
options.add_argument('--disable-extensions')
# disable sandbox mode
options.add_argument('--no-sandbox')
# disable shared memory usage
options.add_argument('--disable-dev-shm-usage')

# Step 3: Rotate user agents 
user_agents = [
    # Add your list of user agents here
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
]

# select random user agent
user_agent = random.choice(user_agents)

# pass in selected user agent as an argument
options.add_argument(f'user-agent={user_agent}')

bot = webdriver.Chrome(service=Service( ChromeDriverManager().install() ), options=options)
bot.set_window_size( 800,800 )

# Step 4: Scrape using Stealth
#enable stealth mode
stealth(bot,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )


# Change the property value of the navigator for webdriver to undefined
bot.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")



# Verification que xsel fonctionne sur le poste
try:
    pyperclip.copy('Hello, world!')
    pyperclip.paste()
    logging.info( "xsel est bien installer" )

except pyperclip.PyperclipException :
    print ( "You need to install xsel use this command : sudo apt-get install xsel " )
    logging.info ( "You need to install xsel use this command : sudo apt-get install xsel " )
    raise SystemExit



