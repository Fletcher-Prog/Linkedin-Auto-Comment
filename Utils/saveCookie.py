import Utils
import json


def saveCookies():

    with open( "cookies.json", "w" ) as file :
        coockies = Utils.bot.get_cookies()
        json.dump(coockies,file)

    print ( " cookie save " )
