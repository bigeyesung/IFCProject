import sqlite3
import re
def FetchDataLinks(filename):
    try:
        table = []
        conn = sqlite3.connect(filename)
        # self.__conn.row_factory = sqlite3.Row
        cursor = conn.cursor()    
        cursor.execute("SELECT IFC_PRODUCTS, NAME FROM IFC_PRODUCT_SELECTION")
        results =  cursor.fetchall()
        table.append(["TaskName", "GUID"])
        err_guid = []
        for IFC_PRODUCTS, NAME in results:
            # https://stackoverflow.com/questions/2525327/regex-for-a-za-z0-9-with-dashes-allowed-in-between-but-not-at-the-start-or-e
            ids = re.findall(r"\{([A-Za-z0-9-]+)\}", IFC_PRODUCTS)
            guids = []
            for id in ids:
                # https://stackoverflow.com/questions/3503879/assign-output-of-os-system-to-a-variable-and-prevent-it-from-being-displayed-on
                tmp = os.popen(Path.EXE_DIR.value + 'IfcGuidConverter.exe %s %s' % ("dot", id)).read()
                guid = tmp.split()[2]

                guids.append(guid)
            guids = ", ".join(guids)
            table.append([NAME,guids])
        print(err_guid)
        return table
    except sqlite3.Error as e:
        print("Database error: %s" % e)

    if conn:
        conn.close()