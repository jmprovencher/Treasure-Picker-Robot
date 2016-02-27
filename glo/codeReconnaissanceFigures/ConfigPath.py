# import the necessary packages
import os

class Config():

    @staticmethod
    def appendToProjectPath(url):
        return os.path.join(os.path.dirname(__file__), url)

