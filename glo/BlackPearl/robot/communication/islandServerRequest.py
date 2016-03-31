import urllib2
import ssl

def islandServerRequest(ipAdress, manchesterCode):
    reseau = '192.168.0.2'
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)  # Only for gangstars
    content = urllib2.urlopen("https://"+reseau+"/?code="+manchesterCode, context=gcontext).read()
    return content

