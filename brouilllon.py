tableauDeMotMotsExclus       = ["recherche d'alternance","recherche de stage ",]
class PosteNonValable(Exception):
    pass

for element in tableauDeMotMotsExclus :
    print(element)
    if element.lower() in "🚨 Urgent : Recherche de Stage en Logistique / Supply Chain 🚨 Cher réseau, Actuellement étudiante en première année de Master Supply Chain Management à l'Université du Havre, je suis à la recherche d'un stage de 3 mois dans la région du Havre dans le domaine de la logistique, du transport ou de la supply chain. Disponible immédiatement, le stage doit commencer au plus tard le 3 juin 2024 afin de faire les 3 mois de stage, sans ce stage je ne pourrais malheureusement pas valider mon année académique. Si vous vous demandez pourquoi je me suis mise à faire ce post si tardivement c’est parce qu’initialement, j’avais trouvé une entreprise prête à m’accueillir pour mon stage. Malheureusement celle-ci a changé d’avis à la dernière minute, me faisant ainsi perdre près d’un mois. Un mois de recherche ou un mois ou j’aurais pu déjà être en entreprise… Depuis, j’ai contacté plusieurs entreprises, mais la majorité ont déjà leurs stagiaires ou ne peuvent pas accepter un stage de 3 mois, jugeant cette durée trop courte. C’est pourquoi je me tourne vers vous aujourd’hui et tente le tout pour tout, c’est mon dernier espoir. Motivée, curieuse et investie, je suis convaincue que cette expérience sera une opportunité précieuse pour développer mes compétences et contribuer activement à la performance de votre entreprise. Je vous mets à disposition ci-dessous mon CV et je compte sur vous pour vos nombreux partages. Résumé : 💡 Domaines ? logistique, transport, chaîne d’approvisionnement 📍 Où ? Le Havre 🗓 Quand ? 3 juin 2024 ⏳ Durée ? 3 mois ☎️ Contact : / 07 83 88 64 19 N'hésitez pas à me contacter en message privé, par mail ou par téléphone si vous avez des opportunités ou des recommandations. Je serais ravie d'en discuter. Et surtout, n'hésitez pas à partager ce post, cela me serait d'une grande aide. Merci pour votre aide et votre soutien ! …voir plus".lower()  :
        
        try:
            print ("True")
            raise PosteNonValable("PosteNonValable")
        except PosteNonValable :
            print ( "e" )