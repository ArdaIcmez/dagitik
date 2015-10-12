class Airline(object):
    
    def __init__(self,data):
        if(data):
            self.name = data[0]
            self.partners = []
            for i in data:
                self.partners.append(i)
            self.partners.remove(self.name)
            
    def getPartners(self):
        return self.partners
    
    def isPartner(self,name):
        return name in self.partners
    
    def getName(self):
        return self.name
    
    def toString(self):
        return self.name + ", partners: " + self.partners