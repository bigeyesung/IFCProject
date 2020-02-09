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
        
    def Init(self, file):
        if not os.path.isfile(file):
            #Logger().Initialise(LoggerType.CONSOLE.value, LoggerSeverity.ERROR.value)
            Logger().Error("read ifc error: " + file)
            return

        basename = os.path.basename(file)
        self.__filename, _ = os.path.splitext(basename)
        ifcFile = ifcopenshell.open(file)
        storeys = ifcFile.by_type("IFCBUILDINGSTOREY")
        for storey in storeys:
            self.__levels[storey.Name] =  storey.Name
        # categories = ["IfcWall", "IfcRoof"]
        # for category in categories:
        #     elements = ifcFile.by_type(category)
        #     for element in elements:
        #         contain = element.ContainedInStructure
        #         if len(contain) >0:
        #             if contain[0].RelatingStructure.Name is not None:
        #                 self.__levels[contain[0].RelatingStructure.Name] = contain[0].RelatingStructure.Name
        
        if len(self.__levels) > 0:
            self.__init = True
        else:
            #Logger().Initialise(LoggerType.CONSOLE.value, LoggerSeverity.ERROR.value)
            Logger().Error("read IFC level data error: " + self.__filename)

    def GetInit(self):
        return self.__init