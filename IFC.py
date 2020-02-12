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

    def RemoveTypeElement(self):
        if not self.__init:
            return
        SaveGUID = []
        ifcFile = ifcopenshell.open(self.__ifcPath)
        for category in self.__categories:
            elements = ifcFile.by_type(category)
            for element in elements:
                if element.GlobalId in self.__removeList:
                    ifcFile.remove(element)
                    continue
                contain = element.ContainedInStructure
                if len(contain) == 0: continue
                item =  contain[0].RelatingStructure.Name

                ##for For Gravens_Hill_260719 second case
                # if self.__targetLevel == "00 Ground Floor" and item == "01 First Floor" and element.GlobalId == "3hR3mfu7LA8ed1jTcubv7L":
                #     SaveGUID.append(element.GlobalId)
                # elif self.__targetLevel == "01 First Floor" and item == "02 Roof Plan" and element.GlobalId == "0s8adBwwP3wO0g27aFJZfR":
                #     SaveGUID.append(element.GlobalId)
                # elif self.__targetLevel == "01 First Floor" and item == "02 Roof Plan" and element.GlobalId == "0s8adBwwP3wO0g27aFJZeb":
                #     SaveGUID.append(element.GlobalId)
                # else:
                #     if item != self.__targetLevel:
                #         ifcFile.remove(element)
                #     else:
                #         SaveGUID.append(element.GlobalId)

                if item != self.__targetLevel:
                    print(element.Name)
                    ifcFile.remove(element)
                else:
                    SaveGUID.append(element.GlobalId)


        ifcFile.write(self.__ifcPath)
        return SaveGUID

    def RemoveRedundantElement(self):
    if not self.__init:
        return

    # These types 
    ifcFile = ifcopenshell.open(self.__ifcPath)
    categories = ["IfcWindow", "IfcDoor", "IfcRailing", "IfcStair", 
                    "ifcRamp", "IfcBuildingElementProxy", 
                    "IfcAnnotation", "IfcCovering", "IfcSpace", "IfcFurnishingElement", 
                    "IfcFlowTerminal", "IfcFlowSegment", "IfcFlowFitting",
                    "IfcFlowController", "IfcElectricDistributionPoint"]
    for category in categories:
        elements = ifcFile.by_type(category)
        for element in elements:
            ifcFile.remove(element)
    ifcFile.write(self.__ifcPath)