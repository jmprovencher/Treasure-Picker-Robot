# import the necessary packages
import numpy as np
import cv2

from stationbase.interface.StationBase import StationBase
from stationbase.commande.RequeteJSON import RequeteJSON

stationBase = StationBase()
requete = RequeteJSON('avancer', 15)
