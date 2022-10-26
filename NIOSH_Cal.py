#create a class for the NIOSH equation
class Calc:
    def __init__(self, horizontalMulti, verticalMulti, DistMulti, cm, weight):
        self.horizontialMulti = HMFactor(horizontalMulti)
        self.verticalMulti = VMFactor(verticalMulti)
        self.DistMulti = DMFactor(DistMulti)
        self.cm = couplingMultiplier(cm)
        self.weight = weight

   #run just a basic calculation for the recommended weight
    def RecommendWeight (self):
        #set the defult values since we dont add this to our equation and its mutiplying make it 1
        asymetricMulti = 1.0
        freq = 1.0
        #RWL = LC (51) x HM x VM x DM x AM x FM x CM
        recWeight = 51.0 * self.horizontialMulti * self.verticalMulti * self.DistMulti * self.cm * freq * asymetricMulti
        
        return recWeight


    #run for the  lifting index 
    def liftingIndex (self):
        #index is Lifting weight index = weight / RWL
        if (self.RecommendWeight() > 0):
            index = float(self.weight) / self.RecommendWeight()
        else:
            return 1.1
        
        return index


#create a defintion for warns and colors/ work with GUI
    ''' A Lifting Index value of 1.0 or less indicates a nominal risk to healthy employees.
    A Lifting Index greater than 1.0 denotes that the task is high risk for some fraction of the population.'''
def warnings(index):
    if index > 1:
        print("it is not safe to lift")
    else:
        print("safe to lift")
    
#run the horizontal distance to get the HM factor
def HMFactor(horizontialDist):
    hD = float(horizontialDist)
    if(hD <= (25 * 2.54 )):
        return 1.0
    elif ( hD > (25 * 2.54 ) and hD <= (30 * 2.54 )):
        return 0.83
    elif (hD > (30 * 2.54 ) and hD <= (40 * 2.54 )):
        return 0.63
    elif(hD > (40 * 2.54 ) and hD <= (50 * 2.54 )):
        return 0.50
    elif(hD > (50 * 2.54 ) and hD <= (60 * 2.54 )):
        return 0.42
    else:
        return 0

#run the vertical distance to get the VM factor
def VMFactor(verticalDist):
    vD = float(verticalDist)
    if(vD >= 0 and vD < (30 * 2.54 )):
        return 1.0
    elif (vD >= (30* 2.54) and vD < (50 * 2.54 )):
        return 0.87
    elif (vD >= (50* 2.54) and vD < (70 * 2.54 )):
        return 0.93
    elif (vD >= (70* 2.54) and vD < (100 * 2.54 )):
        return 0.99
    elif (vD >= (100 * 2.54) and vD < (150 * 2.54 )):
        return 0.93
    elif (vD >= (150 * 2.54) and vD < (175 * 2.54 )):
        return 0.78
    elif (vD == (175* 2.54)):
        return 0.70
    else:
        return 0

#run the distance the load travels to get the DM factor
def DMFactor(distTravel):
    dT = float(distTravel)
    if(dT >= 0 and dT <= (25 * 2.54 )):
        return 1.0
    elif (dT > (25* 2.54) and dT <= (40 * 2.54 )):
        return 0.93
    elif (dT > (40* 2.54) and dT <= (55 * 2.54 )):
        return 0.90
    elif (dT > (55* 2.54) and dT <= (100 * 2.54 )):
        return 0.87
    elif (dT > (100* 2.54) and dT <= (175 * 2.54 )):
        return 0.85
    elif (dT > (175* 2.54)):
        return 0.0
    
    

#run to equation to couplingMuti from user input into a number
def couplingMultiplier(CM):
    if CM == "Good":
        return 1.0
    elif CM == "Fair":
        return 2.0
    elif CM == "Poor":
        return 3.0


def main():
    #test of the functions 
    hm = input("Please enter the Horizontal Multiplier: ")
    vm = input("Please enter the Vertical Multiplier: ")
    dm = input("Please enter the Distance Multiplier: ")
    cm = input("Please enter the coupling Multiplier: ")

    #take in the weight for the lifting index
    weightOfObj = input("Please enter the weight of the object: ")

    calc = Calc(hm,vm,dm,cm,weightOfObj)

    #index is Lifting weight index = weight / RWL
    index = calc.liftingIndex()

    print(index)
    warnings(index)