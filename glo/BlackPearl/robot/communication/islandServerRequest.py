import urllib2
import ssl
import time

def islandServerRequest(adresseIP, codeManchester):
    reseau = adresseIP
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    content = urllib2.urlopen("https://" + reseau + "/?code=" + codeManchester, context=gcontext).read()
    return content
