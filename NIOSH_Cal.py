#run just a basic calculation for the recommended weight
def RecommendWeight (horizontialMulti,verticalMulti,DistMulti, cM):
    #set the defult values since we dont add this to our equation and its mutiplying make it 1
    asymetricMulti = 1.0
    freq = 1.0
    #RWL = LC (51) x HM x VM x DM x AM x FM x CM
    recWeight = 51.0 * horizontialMulti * verticalMulti * DistMulti * cM * freq * asymetricMulti
    
    return recWeight

#run the horizontal distance to get the HM factor
def HMFactor(horizontialDist):
    if(horizontialDist <= (25 * 2.54 )):
        return 1.0
    elif ( horizontialDist > (25 * 2.54 ) and horizontialDist <= (30 * 2.54 )):
        return 0.83
    elif (horizontialDist > (30 * 2.54 ) and horizontialDist <= (40 * 2.54 )):
        return 0.63
    elif(horizontialDist > (40 * 2.54 ) and horizontialDist <= (50 * 2.54 )):
        return 0.50
    elif(horizontialDist > (50 * 2.54 ) and horizontialDist <= (60 * 2.54 )):
        return 0.42
    else:
        return 0

#run the vertical distance to get the VM factor
def VMFactor(verticalDist):
    if(verticalDist >= 0 and verticalDist < (30 * 2.54 )):
        return 1.0
    elif (verticalDist >= 30 and verticalDist < (50 * 2.54 )):
        return 0.87
    elif (verticalDist >= 50 and verticalDist < (70 * 2.54 )):
        return 0.93
    elif (verticalDist >= 70 and verticalDist < (100 * 2.54 )):
        return 0.99
    elif (verticalDist >= 100 and verticalDist < (150 * 2.54 )):
        return 0.93
    elif (verticalDist >= 150 and verticalDist < (175 * 2.54 )):
        return 0.78
    elif (verticalDist == 175):
        return 0.70
    else:
        return 0

#run the distance the load travels to get the DM factor
def DMFactor(distTravel):
    if(distTravel >= 0 and distTravel <= (25 * 2.54 )):
        return 1.0
    elif (distTravel > 25 and distTravel <= (40 * 2.54 )):
        return 0.93
    elif (distTravel > 40 and distTravel <= (55 * 2.54 )):
        return 0.90
    elif (distTravel > 55 and distTravel <= (100 * 2.54 )):
        return 0.87
    elif (distTravel > 100 and distTravel <= (175 * 2.54 )):
        return 0.85
    elif (distTravel > 175):
        return 0.0
    
    

#run to equation to couplingMuti from user input into a number
def couplingMultiplier(CM):
    if CM == "Good":
        return 1.0
    elif CM == "Fair":
        return 2.0
    elif CM == "Poor":
        return 3.0

#run for the  lifting index 
def liftingIndex (horizontialMulti, verticalMulti, DistMulti, cM, weight):
    #define the couplingMultiplier
    couplingMulti = couplingMultiplier(cM)
    #print(couplingMulti)
    dm = DMFactor(DistMulti)
    hm = HMFactor(horizontialMulti)
    vm = VMFactor(verticalMulti)
    
    #define the recommended weight
    rWL = RecommendWeight (hm, vm, dm, float(couplingMulti))
    #index is Lifting weight index = weight / RWL
    index = weight / rWL
    
    return index


#create a defintion for warns and colors/ work with GUI
''' A Lifting Index value of 1.0 or less indicates a nominal risk to healthy employees.
 A Lifting Index greater than 1.0 denotes that the task is high risk for some fraction of the population.'''
def warnings(index):
    if index > 1:
        print("it is not safe to lift")
    else:
        print("safe to lift")



#test of the functions 
hm = input("Please enter the Horizontal Multiplier: ")
vm = input("Please enter the Vertical Multiplier: ")
dm = input("Please enter the Distance Multiplier: ")
cm = input("Please enter the coupling Multiplier: ")

#take in the weight for the lifting index
weightOfObj = input("Please enter the weight of the object: ")

#index is Lifting weight index = weight / RWL
index = liftingIndex(int(hm), int(vm), int(dm), cm, int(weightOfObj))

print(index)
warnings(index)