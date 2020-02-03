import ifcopenshell
import os
from shutil import copyfile
from utils.utils import WriteCSV
from utils.enums import Path
from logger import Logger
class ParseIFC:
    def __init__(self, file):
        self.__levels = {}
        self.__removeList = []
        self.__dataProperties = {}
        self.__categories = ["IfcWall", "IfcSlab", "IfcRoof", "IfcColumn", "IfcBeam"]
        self.__ifcPath = None
        self.__targetLevel = None
        self.__init = False
        self.__filename = None
        self.Init(file)
        

