import urllib2
import ssl


def islandServerRequest(adresseIP, codeManchester):
    reseau = adresseIP
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    content = urllib2.urlopen("https://" + reseau + "/?code=" + codeManchester, context=gcontext).read()
    print("Envoie requete")
    while (content is None):
        content = urllib2.urlopen("https://" + reseau + "/?code=" + codeManchester, context=gcontext).read()
        print("GET request to server...")

    return content
