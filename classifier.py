import copy

def menuOptions():
    print("Tadas Rimkevicius's Naive Bayesian Classifier, 2023")
    model = []
    
    menuChoice = 4
    while(menuChoice != '4'):
        menuChoice = input("""
            Choose your desired option:
                1. Train
                2. Classify
                3. Test Accuracy
                4. Quit
                Enter your choice: """)
        if(menuChoice == '1'):
            model = train()
        if(menuChoice == '2'):
            classify(model)
        if(menuChoice == '3'):
            testAccuracy(model)
    print("\nTerminating...")

def train():
    #Open Meta and Training files
    metaFile = open(input("\nEnter Meta File Name: "))
    trainingFile = open(input("Enter Training File Name: "))

    #Split the metadata files
    temp = metaFile.read().split('\n')

    #meta holds the metadata, and will be split into the headings and values lists
    meta = []
    
    #Headings will hold the attribute names
    headings = []

    #Values will hold the possible attribute values
    values = []

    #Multiarray will have the format [attributeName,[possibleValues]]
    multiArray = []

    #TrainingArray will have all training data in the form of [[data1list],[data2list],[data3list]]
    trainingArray = []

    #ProbabilitiesArray will have the same format as multiArray, but will store the number of instances
    #of each attribute value rather than the possible values2
    #This will help greatly in calculating prior probabilities
    probabilitiesArray = []

    #PriorProbabilities will keep track of the number of instances of each classification in the training data
    priorProbabilities = []

    #CategoricalProbabilities will keep track of the likelyhood of each variable occuring given a classification
    categoricalProbabilities = []
    
    #Copy temp to meta
    for x in temp:
        meta.append(x)
        
    #Pop the newline character from the array
    meta.pop()

    #Split info into headings and values lists
    for x in meta:
        temp = x.split(':')
        headings.append(temp[0])
        values.append(temp[1])

    #Form the multiArray list
    i = 0
    for x in headings:
        nameArray = []
        nameArray.append(x)
        nameArray.append(values[i].split(','))
        multiArray.append(nameArray)
        i = i + 1

    #Since probabilitiesArray will have the same format as multiArray, we can do a deepcopy
    #using the built-in copy library
    probabilitiesArray = copy.deepcopy(multiArray)

    #trainingTemp temporarily stores all training data in the form [data1,data2,data3,...]
    trainingTemp = trainingFile.read().split('\n')
    trainingArray = []

    #split up trainingTemp from [data1,data2,data3,..] -> [[data1list],[data2list],[data3list],...]
    for x in trainingTemp:
        trainingArray.append(x.split(','))

    #Set all the 'attribute values' to 0 instead, such that probabilities1 has the form
    #[[attributeName1,[0,0,...]],[attributeName2,[0,0,...],...]
    i = 0
    for x in probabilitiesArray:
        while i < len(x[1]):
            x[1][i] = 0
            i = i + 1
        i = 0

    #Adjust the probabilities array with the number of instances of each attribute value
    i = 0
    for x in trainingArray:
        for y in x:
            if y != '':
                location = multiArray[i][1].index(y)
                probabilitiesArray[i][1][location] = probabilitiesArray[i][1][location] + 1
                i = i + 1
        i = 0
    trainingArray.pop()
    
    #Variable to track the total number of training points
    trainingPoints = sum(probabilitiesArray[len(probabilitiesArray)-1][1])
    

    #updating the priorProbabilities list
    i = 0
    for x in multiArray[len(multiArray)-1][1]:
        priorProbabilities.append(probabilitiesArray[len(probabilitiesArray)-1][1][i])
        i = i + 1

    #Format the categoricalProbabilities list
    i = 0
    j = 0
    for x in multiArray[len(multiArray)-1][1]:
        categoricalProbabilities.append(copy.deepcopy(multiArray))
        categoricalProbabilities[i].pop()
        for y in categoricalProbabilities[i]:
            while j < len(y[1]):
                y[1][j] = 0
                j = j + 1
            j = 0
        i = i + 1

    #Populate the categoricalProbabilities list
    j = 0
    for x in trainingArray:
        category = x[len(x)-1]
        location = multiArray[len(multiArray)-1][1].index(category)
        for y in x:
            if(j < len(multiArray)-1):
                attributeLocation = multiArray[j][1].index(y)
                categoricalProbabilities[location][j][1][attributeLocation] = categoricalProbabilities[location][j][1][attributeLocation] + 1
                j = j + 1
        j = 0

    print("\nSuccessfully trained model with ", len(trainingArray)," elements",sep='')
    return categoricalProbabilities,priorProbabilities,multiArray
    
def classify(model):
    #Open file with unclassified data
    unclassifiedData = open(input("\nEnter Unclassified Data File Name: "))
    unclassifiedArray = []
    temp = unclassifiedData.read().split('\n')
    #Populate unclassifiedData with items from the temp array.
    for x in temp:
        unclassifiedArray.append(x.split(','))
        
    #Classification fucntion
    probability = 1
    probabilities = []
    classification = []
    i = 0
    j = 0

    temp = ['']    
    #For each item in the unclassified array
    for x in unclassifiedArray:
        if x != temp:
            #For each possible classification
            for y in model[2][len(model[2])-1][1]:
                for z in x:
                    #For each attribute within an entry
                    if(i < len(model[2])-1):
                        location = model[2][i][1].index(z)
                        probability = probability * ((model[0][j][i][1][location]+1)/(model[1][j]+len(model[2][i][1])))
                        i = i + 1
                #Making sure to multiply by the prior probability as well
                probabilities.append(probability*((model[1][j])/(sum(model[1]))))
                probability = 1
                i = 0
                j = j + 1
            j = 0
        #Append the most likely classification to the classifications array
        if(probabilities):
            classification.append(model[2][len(model[2])-1][1][probabilities.index(max(probabilities))])
            #Reset the probabilities array to be ready for a new entry
            probabilities = []

    i = 0
    #For each element in the classifications array add that element on the end of the corresponding unclassifiedArray element
    for x in classification:
        unclassifiedArray[i].pop()
        unclassifiedArray[i].append(x)
        i = i + 1

    #Ask user for output file
    classifiedFileName = input("\nEnter Output Data File Name: ")
    classifiedData = open(classifiedFileName,"w")

    #Write unclassifiedArray to the given file
    for x in unclassifiedArray:
        for y in x:
            classifiedData.write(y)
            if y not in model[2][len(model[2])-1][1] and y != '':
                classifiedData.write(",")
        if y != '':
            classifiedData.write("\n")
    classifiedData.close()

    print("\nSuccessfully classified ",len(unclassifiedArray)," elements and wrote the results to ",classifiedFileName,sep='')

def testAccuracy(model):
    #Open testing File and read it into testingArray
    testingFile = open(input("\nEnter Testing File Name: "))
    
    testingArray = []
    
    temp = testingFile.read().split('\n')
    
    for x in temp:
        testingArray.append(x.split(','))
    testingArray.pop()

    #Classification Function
    probability = 1
    probabilities = []
    classification = []
    i = 0
    j = 0

    print(model)
    #For each item in the unclassified array
    for x in testingArray:
        #For each possible classification
        for y in model[2][len(model[2])-1][1]:
            #For each attribute within an entry in the unclassified array
            for z in x:
                if(i < len(model[2])-1):
                    #Find the location of the selected value, and multiply the probability by that of the value
                    location = model[2][i][1].index(z)
                    probability = probability * ((model[0][j][i][1][location]+1)/(model[1][j]+len(model[2][i][1])))
                    i = i + 1
            probabilities.append(probability*((model[1][j])/(sum(model[1]))))
            probability = 1
            i = 0
            j = j + 1
        j = 0
        #Append the most likely classification to the classifications array
        classification.append(model[2][len(model[2])-1][1][probabilities.index(max(probabilities))])
        #Reset the probabilities array to be ready for a new entry
        probabilities = []

    #Calculate the accuracy of the model
    i = 0
    truePositives = 0
    total = 0
    
    #Calculate all truePositives
    for x in testingArray:
        if(x != ''):
            if x[len(x)-1] == classification[i]:
                truePositives = truePositives + 1
            i = i + 1
            total = total + 1
 
    print("\nTrue positives:",truePositives)
    print("Total elements tested:",total)
    print("Accuracy: ",100*truePositives/total,"%", sep='')
menuOptions()
