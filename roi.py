from lxml import etree

class ParseRoi:
    def __init__(self,file):
        self.tree = etree.parse(file)
        self.root = self.tree.getroot()
        self.result = []

    def ParseData(self):
        for taskData in self.root.iter("roi"):
            id = taskData.find("id")
            # data: [id,pt1.x,pt1.y,pt2.x,pt2.y]
            data = []
            data.append(id.text)
            twoPoints = ["pt1","pt2"]
            for point in twoPoints:
                for subData in taskData.iter(point):
                    coordinates = ["pos_x", "pos_y"]
                    for coordinate in coordinates:
                        value = subData.find(coordinate)
                        data.append(value.text)
            self.result.append(data)

        return self.result


if __name__ == "__main__":
    table = {}
    # given index range, and give it table
    for id in range(195,220):
        fileName = "roi/DJI_0" + str(id) + ".xml"
        parser = ParseRoi(fileName)
        fileData = parser.ParseData()
        table[fileName] = fileData
