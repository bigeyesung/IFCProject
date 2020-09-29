import base64
import uuid

class IfcConvert:
    def __init__(self):
        self.b64_charset = str.encode('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/')
        self.ifc_charset = str.encode('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_$')
    def generate(self):
        return self.encode_uuid_to_ifc_guid(uuid.uuid4().bytes)

    def encode_uuid_to_ifc_guid(self, uuid):
        table = bytes.maketrans(self.b64_charset, self.ifc_charset)
        return base64.b64encode(uuid)[0:22].translate(table)

    def decode_ifc_guid_to_uuid(self, guid):
        table = bytes.maketrans(self.ifc_charset, self.b64_charset)
        ori = base64.b64decode(guid.translate(table) + str.encode('=='))
        return uuid.UUID(bytes=ori)



if __name__ == "__main__":
    ifcconverter = IfcConvert()
    some_uuid = uuid.uuid4()
    some_ifc_guid = ifcconverter.encode_uuid_to_ifc_guid(some_uuid.bytes)
    some_uuid_again = ifcconverter.decode_ifc_guid_to_uuid(some_ifc_guid)
    print(some_uuid) 
    print(some_ifc_guid) 
    print(some_uuid_again) 