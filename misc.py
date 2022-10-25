class Misc:
    def convertToLb(self, weight, unit):
        if (unit == "kg"):
            return weight * 2.20462262185
        return weight
    
    def convertToInch(self, len, unit):
        if (unit == "cm"):
            return len * 0.3937007874
        if (unit == "ft"):
            return len * 12
        if (unit == "m"):
            return self.convertToInch(len * 100.0, "cm")
        return len
    
    def cleanName(self, name):
        return ((name.strip()).replace(" ", "_")).lower()