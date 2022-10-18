#run just a basic calculation for the recommended weight
def RecommendWeight (horizontialMulti,verticalMulti,DistMulti, cM):
    #set the defult values since we dont add this to our equation and its mutiplying make it 1
    asymetricMulti = 1
    freq = 1
    #RWL = LC (51) x HM x VM x DM x AM x FM x CM
    recWeight = 51 * horizontialMulti * verticalMulti * DistMulti * cM * freq * asymetricMulti
    
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

#run the vertical distance to get the VM factor
def VMFactor(verticalDist):
    if(verticalDist <= 0 and verticalDist < (30 * 2.54 )):
        return 1.0
    elif (verticalDist <= 30 and verticalDist < (50 * 2.54 )):
        return 0.87
    elif (verticalDist <= 50 and verticalDist < (70 * 2.54 )):
        return 0.93
    elif (verticalDist <= 70 and verticalDist < (100 * 2.54 )):
        return 0.99
    elif (verticalDist <= 100 and verticalDist < (150 * 2.54 )):
        return 0.93
    elif (verticalDist <= 150 and verticalDist < (175 * 2.54 )):
        return 0.78
    elif (verticalDist == 175):
        return 0.70
    else:
        return 0

#run the distance the load travels to get the DM factor
def DMFactor(dist):
    if(dist <= 0 and dist >= (25 * 2.54 )):
        return 1.0
    elif (dist < 25 and dist >= (40 * 2.54 )):
        return 0.93
    elif (dist < 40 and dist >= (55 * 2.54 )):
        return 0.90
    elif (dist < 55 and dist >= (100 * 2.54 )):
        return 0.87
    elif (dist < 100 and dist >= (175 * 2.54 )):
        return 0.85
    elif (dist > 175):
        return 0
    
    

#run to equation to couplingMuti from user input into a number
def couplingMultiplier(CM):
    if CM == "Good":
        return 1
    elif CM == "Fair":
        return 2
    elif CM == "Poor":
        return 3

#run for the  lifting index 
def liftingIndex (horizontialMulti,verticalMulti,DistMulti, cM, weight):
    #define the couplingMultiplier
    couplingMulti = couplingMultiplier(cM)
    #define the recommended weight
    rWL = RecommendWeight (horizontialMulti,verticalMulti,DistMulti, couplingMulti)
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
index = liftingIndex(float(hm), float(vm), float(dm), cm, int(weightOfObj))

print(index)
warnings(index)