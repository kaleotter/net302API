from json import JSONEncoder



class ResponseJsonFormatter:
    
    def create(self, status, errorMsg, data):
        
        return {"statusCode":status , "Message": errorMsg, "data":data}