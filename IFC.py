import ifcopenshell
import os
from shutil import copyfile
class ParseIFC:
    def __init__(self, file):
        self.__levels = {}
        self.__removeList = []
        self.__dataProperties = {}
        self.__categories = ["IfcWall", "IfcSlab", "IfcRoof", "IfcColumn", "IfcBeam"]
        self.__categories_service = ["IFCFLOWSEGMENT", "IFCBUILDINGELEMENTPROXY", "IFCFLOWTERMINAL", "IFCFLOWCONTROLLER", "IFCFLOWFITTING"]
        self.__ifcPath = None
        self.__targetLevel = None
        self.__init = False
        self.__filename = None
        self.Init(file)
        
    def Init(self, file):
        if not os.path.isfile(file):
            print("read file error")
            return

        basename = os.path.basename(file)
        self.__filename, _ = os.path.splitext(basename)
        self.__ifcPath = ifcopenshell.open(file)
        storeys = self.__ifcPath.by_type("IFCBUILDINGSTOREY")
        for storey in storeys:
            self.__levels[storey.Name] =  storey.Name
        
        if len(self.__levels) > 0:
            self.__init = True
        else:
            print("read IFC level data error: ")

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

                #for For Gravens_Hill_260719 second case

                if item != self.__targetLevel:
                    print(element.Name)
                    ifcFile.remove(element)
                else:
                    SaveGUID.append(element.GlobalId)


        ifcFile.write(self.__ifcPath)
        return SaveGUID

    def LoadElementProperty(self, level, SaveGUID):
        if not self.__init:
            return
        ifcFile = ifcopenshell.open(self.__ifcPath)
        dataProperty = []
        dataProperty.append(["guid", "resource", "start", "groups", "ifcName", "name", "end", "dependency"])
        for guid in SaveGUID:
            element = ifcFile.by_guid(guid)
            ifc_name = element.Name.replace(":", "_")
            dataProperty.append([element.GlobalId, "default", "08/08/19 08:00:00", 
                                [level, 'concrete wall'], ifc_name, 
                                element.Name, "08/09/19 17:00:00", "default"]) 

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

    def SetRemoveList(self, li = []):
        if not self.__init:
            return
        self.__removeList = li

    def Del(self, src):
        types = ["IFCWALL", "IFCSLAB", "IFCCOLUMN"]
        for fielpath in src:
            ifcFile = ifcopenshell.open(fielpath)
            for eletype in types:
                elements = ifcFile.by_type(eletype)
                for element in elements:
                    if element.GlobalId == "1DIyRBByj18Ax$rOEtI14l":
                        continue
                    if element.GlobalId == "2sOXiqxR11FPF$18FGYBQO":
                        continue
                    ifcFile.remove(element)
            ifcFile.write(fielpath)

    def MergeIFC(self,src):
        if not self.__init:
            return
        ifcFile2 = ifcopenshell.open(src)
        # wall_ifc1 = ifcFile.by_guid("2sOXiqxR11FPF$18FGYBQO")
        project = ifcFile2.by_type("IFCPROJECT")
        site = ifcFile2.by_type("IFCSITE")       
        stories = ifcFile2.by_type("IFCBUILDINGSTOREY")
        openings = ifcFile2.by_type("IFCOPENINGELEMENT")
        cutopenings = ifcFile2.by_type("IFCRELVOIDSELEMENT")
        contains = ifcFile2.by_type("IFCRELCONTAINEDINSPATIALSTRUCTURE")
        aggres  = ifcFile2.by_type("IFCRELAGGREGATES")
        materials = ifcFile2.by_type("IFCRELASSOCIATESMATERIAL")
        pros = ifcFile2.by_type("IFCRELDEFINESBYPROPERTIES")

        wall2 = ifcFile2.by_type("IFCWALL")
        # self.__ifcPath.add(project)
        # self.__ifcPath.add(site)
        for storey in stories:
            self.__ifcPath.add(storey)
        for wall in wall2:
            self.__ifcPath.add(wall)
        for opening in openings:
            self.__ifcPath.add(opening)
        for cut in cutopenings:
            self.__ifcPath.add(cut)
        for contain in contains:
            self.__ifcPath.add(contain)
        for aggre in aggres:
            self.__ifcPath.add(aggre)
        for pro in pros:
            self.__ifcPath.add(pro)
        for mat in materials:
            self.__ifcPath.add(mat)
        self.__ifcPath.write("one_wall.ifc")

        print("ok")

    def SaveEachFloorIFC(self, src):
        if not self.__init:
            return
        if not os.path.isfile(src):
            return 
        # Copy ifc source to remove redundant elements
        cleanIFC = Path.IFC_DIR.value + self.__filename  + "_clean" + ".ifc"
        copyfile(src, cleanIFC)
        self.__ifcPath = cleanIFC
        # self.RemoveRedundantElement()
        for level in self.__levels:
            copyfile(cleanIFC, Path.IFC_DIR.value + self.__filename + "_" + level + ".ifc")
            self.__ifcPath = Path.IFC_DIR.value + self.__filename + "_" + level + ".ifc"
            self.__targetLevel = level
            SaveGUID = self.RemoveTypeElement()
            self.LoadElementProperty(level, SaveGUID)
    
    def SaveEachFloorCSV(self):
        if not self.__init:
            return

        for _level, _property in self.__dataProperties.items():
            WriteCSV( Path.DATA_DIR.value + self.__filename + "_" + _level + ".csv", _property)


    # def job(v, num): for _ in range(10): 
    #     import multiprocessing as mp
    #     import time
    #     time.sleep(0.1) v.value += num # 使用共享資料取值要用 value print(v.value) 
    #     def multicode(): v = mp.Value("i",0) # 宣告一個 process 之間共享的變數 p1 = mp.Process(target=job, args=(v,1)) # 把 v 傳值進去 
    #     p2 = mp.Process(target=job, args=(v,3)) p1.start() p2.start() p1.join() p2.join()

if __name__ == "__main__":
    # sample
    parser = ParseIFC("one_wall.ifc")
    if parser.GetInit():
        parser.MergeIFC("ST_onewall.ifc")
        # parser.SaveEachFloorIFC("file")
        # parser.SaveEachFloorCSV()