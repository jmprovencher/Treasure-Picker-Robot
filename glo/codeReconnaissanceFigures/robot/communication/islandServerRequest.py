import urllib2
import ssl

def islandServerRequest(ipAdress, manchesterCode):
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)  # Only for gangstars
    content = urllib2.urlopen("https://"+ipAdress+"/?code="+manchesterCode, context=gcontext).read()
    return content

