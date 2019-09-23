import datetime
import os
import re
import fnmatch
import json
import sys
import datetime
from datetime import date

customers = []
roomavailable = []
roomtaken = []
datastruct = {}

#Great method
def writeToJSONFile(path, fileName, data):
    filePathNameWExt = path + fileName 
    print(filePathNameWExt)
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp, indent=4)

def readFromJSONFile(path, fileName):
    with open(fileName, "r") as f:
        data = json.load(f)
        return data

def Signature():
  for file in os.listdir('.'):
      if fnmatch.fnmatch(file, "sign.json"):
          return file
  c = input("Enter this computers name\n")
  writeToJSONFile('./', "sign.json", c)
  sign = c
  Signature()

def AddSignature():
    data = readFromJSONFile("./", "sign.json");
    print(data)
    return data

sign = Signature() 
computername = AddSignature()



def LoadRooms():
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, "room.json"):
            print("Room JSON found. Reading...\n")
            #print(file)
            return file;


roomFile = LoadRooms()
with open(roomFile, 'r') as f:
        datastore = json.load(f)
        #print(datastore)
        for key, value in datastore.items():
            #print(key, value)
            if value == True:
                roomavailable.append(key)
            else:
                roomtaken.append(key)
        
data = str(datetime.datetime.now())
#SET 10 for daily reports, higher for more frequent. 7 is monthly reports.
#print(data[0:10])
matchagainst = computername +"_"+ data[0:7] + "_STATUS_.json"
matchagainst2 = computername +"_"+ data[0:7] + "_REGISTRY_.json"


def ReadStatusFile():
    #if first 8 signs match first 8 of filename. load that file, else make a file.

    for file in os.listdir('.'):
        if matchagainst in file:
           print("Daily registry log found. Reading " + file + "\n")
           return file

    print("No daily registry log found. Creating one")
    with open(matchagainst, "w") as r:
        return matchagainst

def ReadRegistryFile():
    #if first 8 signs match first 8 of filename. load that file, else make a file.

    for file in os.listdir('.'):
        if matchagainst2 in file:
           print("Daily status log found. Reading " + file + "\n")
           return file
        
    print("No daily status log found. Creating one")

    obj = {}
    writeToJSONFile("./", matchagainst2,obj)
    #with open(matchagainst2, "w") as r:
        
       # print("READREGISTRYFILE" + matchagainst2)
        
    return matchagainst2

currentFile = ReadStatusFile()
registryFile = ReadRegistryFile()
#print(currentFile)
#print(registryFile)

    
def GetRoomPrice(r, d):

    d = int(d)
    #dorm
    if r[0] == "K":
        return 120000 * d

    #beachdorm
    elif r[0] == "B":
        return 150000 * d
    
    #love shack
    elif r[0] == "S":
        return 80000 * d 
    
    #terrance
    elif r[0] == "N":
        return 90000 * d

    #balcony
    elif r[0] == "H":
        return 80000 * d

    #tent
    elif r[0] == "T":
        return round(160000 * d)
    
    #4 peron room
    elif float(r) > 200 or float(r) < 203:
        return round(500000 * d)

    #3 peron room
    elif float(r) > 202 or float(r) < 206:
        return round(350000 * d)
    
    else:
        return 0


def AddCustomer():  
    print("Looking for empty places...\n")
    if len(roomavailable) == 0:
        print("Sorry, no rooms are available")

    else:
        FindEmptyPlaces()
        #checkout date cant be before checkin date

        c = input("Enter name of the customer\n")
        p = input("Enter passport number of the customer\n")
        if len(p) < 8:
            print("Length of passport number too short")
            AddCustomer()

        if p in currentFile:
             print("Passport number " + p + "is already checked in")

        room = input("Enter room to checkin to\n")

        if room in roomavailable:
            print("Booking room " + room)
            with open(roomFile, 'r') as f:
                data = json.load(f)
                data[room] = False
                os.remove(roomFile)
                with open(roomFile, 'w') as f:
                        json.dump(data, f)  
        else:
            print("Room already taken")
            AddCustomer()

        roomavailable.remove(room)

        d = input("Enter duration of stay in nights, counting from today.")
       
        ordernum = readFromJSONFile("./", "ordernum.json")
        ordernum += 1

        if readFromJSONFile("./", registryFile) == {}:
            print("Creating empty datastruct...\n")
            datastruct = {}

        else:
            datastruct = readFromJSONFile("./", registryFile)
            print("Printing datastruct... \n")
            #print(datastruct)
            
        datastruct[ordernum] = {}
        datastruct[ordernum][room] = []

        a = int(d)
        timenow = datetime.datetime.now()
        checkout = datetime.datetime.now() + datetime.timedelta(days=a)

        start = str(timenow)
        check = str(checkout)
        #print(checkout)

        price = GetRoomPrice(room, d)
        
        datastruct[ordernum][room] = ({
            'name' : c,
            'passport' : p,
            'checkin' : start,
            'checkout' : check,
            'debt' : round(int(price)),
            'orders': [],
            'lastchanged' : start
            })
#TODO Bug causing replicas of checked out rooms to appear 3 times. check where room prints in AddCustomer and AddDays..
        datastruct[ordernum][room]["orders"].append({
                "name" : room,
                "cost" : GetRoomPrice(room, d),
                "time" : str(datetime.datetime.now())
                })
        
        #print(datastruct[ordernum][room])

        writeToJSONFile("./", "ordernum.json", ordernum)
        writeToJSONFile("./", currentFile, datastruct)
        writeToJSONFile("./", registryFile, datastruct)

        #TODO Delete other indexes from recipe or add to normal doc
        
    Intro()


def HasDebt(room):

    current = readFromJSONFile("./", currentFile)

    #FOR FETCHING VALUE
    #for id
    for key in current:
        #for room
        for key2 in current[key]:
            #print("key2")
            #print(key2)
            if key2 == room:
                localstruct = current[key][room]
                print(localstruct)
                if localstruct["debt"] != "":
                    print("Room " + room + " has debt of " + str(localstruct["debt"]))
                    return True
                        
    return False

def getDebt(roomnr):
    obj = readFromJSONFile("./", currentFile)
    total = 0
    for ordernum, value in obj.items():
        for room in value:
            if roomnr == room:
                total += obj[ordernum][room]["debt"]
                
    return total
    
def RemoveCustomer():
    
    i = input("Enter room number of the candidate to remove\n")

    d = getDebt(i)
    if d != 0:
        print(str("Customer has a debt of "+ str(d)))
        Intro()
    else:
        obj  = readFromJSONFile("./", registryFile)
        print(obj)

    for order,v in obj.items():
        for room in v:
            if room == i:
                obj[order][room] = {}
                with open(currentFile, 'r') as f:
                    data = json.load(f)
                    #Checked out
                    
                    data[order][room] = {}

                    roomavailable.append(i)
                    os.remove(currentFile)
                    with open(currentFile, 'w') as f:
                        json.dump(data, f, indent=4)
                        print("Checking out room " + i)    
                        
    #Assume room number
    with open("room.json", 'r') as f:
        data = json.load(f)
        #Checked out
        data[i] = True
        roomavailable.append(i)
        os.remove("room.json")
        with open("room.json", 'w') as f:
            json.dump(data, f, indent=4)
            print("Checking out room " + i)
    Intro()

#foreach 
            
def FindEmptyPlaces():
    print("Looking for empty places...\n")
    if len(roomavailable) == 0:
        print("Sorry, no rooms are available")
    else:
        for key in roomavailable:
            print("Room " + key + " is available \n")


def FindLatestOrder(room):
    current = readFromJSONFile("./", registryFile)
    latest = 1
    for order,v in current.items():
        #print(v)
        for r in v:
            if room == r:
                latest = order
                
    return latest
    
def AddDaysToCheckout(room, days):
    
    current = readFromJSONFile("./", currentFile)
    ordernum = readFromJSONFile("./", "ordernum.json")
    ordernum += 1
    d = int(days)

    latest = FindLatestOrder(room)

    if readFromJSONFile("./", currentFile) == {}:
        datastruct = {}

    else:
        datastruct = readFromJSONFile("./", currentFile)

        datastruct[ordernum] = {}
        datastruct[ordernum][room] = []

        a = int(d)
        timenow = datetime.datetime.now()
        checkout = datetime.datetime.now() + datetime.timedelta(days=a)

        start = str(timenow)
        check = str(checkout)
        
        price = GetRoomPrice(room, d)
        
        datastruct[ordernum][room] = ({
            'name' : room,
            'passport' : datastruct[latest][room]["passport"],
            'checkin' : start,
            'checkout' : check,
            'debt' : round(int(price)),
            'orders': [],
            'lastchanged' : start
            })

        datastruct[ordernum][room]["orders"].append({
                "name" : room + "_EXTENSION",
                "cost" : GetRoomPrice(room, d),
                "time" : str(datetime.datetime.now())
                })

        datum = current[latest][room]["checkout"];
        datum = datetime.datetime.strptime(datum, '%Y-%m-%d %H:%M:%S.%f')
        c = datum + datetime.timedelta(days=d)
        datastruct[ordernum][room]["checkout"] = str(c)                   
     
        writeToJSONFile("./", "ordernum.json", ordernum)
        writeToJSONFile("./", currentFile, datastruct)
        writeToJSONFile("./", registryFile, datastruct)

    Intro()

def CheckHasDebt(current, room):
    for key in current:
        #for room
        for key2 in current[key]:
            
            if key2 == room:
                beforestruct = current
                j = json.loads(json.dumps(beforestruct))

                if beforestruct[key][room]["debt"] != "0":
                    print("Room " + room + " has debt of " + str(beforestruct[key][room]["debt"]))
                    return True, key, room

    return False, key, room


def UpdatePayoff(current, key, room, payoff):

    
    obj = readFromJSONFile("./", currentFile)

    print("Payoff of " + payoff + " has been recieved")
    p = int(payoff)
    topoplist = []
    
    for ordernum, value in obj.items():
       # print(key)
       # print(value)
        for roomnr in value:
            if roomnr == room:
                
                if(int(obj[ordernum][room]["debt"]) <= p):
                    obj[ordernum][room]["debt"] = 0
                    p -= obj[ordernum][room]["debt"]
                    obj[ordernum][room]["lastchanged"] = str(datetime.datetime.now())

                    #receipt

                    #writeToJSONFile("./receipts/", "_RECEIPT_" + room +"_"+ str(date.today()) + ".json", obj)
                    topoplist.append(ordernum)
                    print("Order " + ordernum + " fully paid off")
                    
                else:
                    #receipt
                    
                    obj[ordernum][room]["debt"] -= p
                    #writeToJSONFile("./receipts/", "_RECEIPT_" + room +"_"+ str(date.today()) +".json", obj)
                    print("Order " + ordernum + " partially paid off for " + str(p) + "\n")
                    print(str(obj[ordernum][room]["debt"]) + " remains to pay")
                    p = 0
                    break;

    writeToJSONFile("./receipts/", "_RECEIPT_" + room +"_"+ str(date.today()) +".json", obj)

    #TODO Add remover for receipts
        
    return obj;

"""

def LoopPast():
    #today = todays date.
    #from 30 days ago.
    #look for filename, if no find, jump next.
    #if find, scan for passportnumber in order,room,passport
    #if find, scan debt > 0
    #remove debt"""
    
def RegisterPayoff():
    room = input("Input the room number and press enter\n")
    payoff = input("Enter amount paid off\n")
    
    obj = readFromJSONFile("./", registryFile)
    current = readFromJSONFile("./", currentFile)
    registry = readFromJSONFile("./", registryFile)

    data = CheckHasDebt(current, room)
    #print(data)
    
    if data[0] == True:
        #print("Debt to pay off")
        beforestruct = registry
        afterstruct = UpdatePayoff(current, data[1], data[2], payoff)

        j = json.loads(json.dumps(beforestruct))
        j2 = json.loads(json.dumps(afterstruct))

        writeToJSONFile("./", currentFile, j2)
        writeToJSONFile("./", registryFile, j2)
    else:
        print("Customer debt is 0")
                
    Intro()

def ExtendStay():
    room = input("Enter room number\n")
    days = input("Enter duration of stay in nights\n")

    AddDaysToCheckout(room, days)

def Intro():
    print("What do you want to do?")
    print("1. Check in customer")
    print("2. Check out customer")
    print("3. Register purchases")
    print("4. Register pay offs")
    print("5. View customer")
    print("6. Extend checkout")
    
    c = input("Enter your action by number 1-6 followed by enter\n");

    if(int(c) < 1 or int(c) > 6):
        print("Please try again. We couldn't understand your action")
        Intro()

    elif(c == "1"):
        AddCustomer()

    elif(c == "2"):
        RemoveCustomer()

    elif(c == "3"):
        AddPurchase()

    elif(c == "4"):
        RegisterPayoff()

    elif(c == "5"):
        ViewCustomer()

    elif(c == "6"):
        ExtendStay()

def ViewCustomer():
    print("What do you want to do?")
    print("1. View all customers")
    print("2. View specific customer")
    c = input("Enter your action by number 1 or 2 followed by enter\n");  

    if(int(c) < 1 or int(c) > 2):
        print("Please try again. We couldn't understand your action")
        Intro()

    elif(c == "1"):
        ShowAllCustomers()

    elif(c == "2"):
        nr = input("Input the room number and press enter\n")
        ShowOneCustomer(nr)

def ShowAllCustomers():
    datastore = readFromJSONFile("./", currentFile)
    #print(datastore)
    for k,v in datastore.items():
        for k2, v2 in datastore[k].items():
            
            print("Room: " + str(k2) + "\n")
            print("Data: " + str(v2) + "\n")
        
    Intro()
      
def ShowOneCustomer(nr):
    datastore = readFromJSONFile("./", currentFile)
    for k,v in datastore.items():
        for k2, v2 in datastore[k].items():
            if k2 == nr:
                print("Room: " + str(k2) + "\n")
                print("Data: " + str(v2) + "\n")
                return;
    
    print("No customer is checking in there")

    Intro()

def AddPurchase():
    Buy()

def LoadAssets(kind):

    current = readFromJSONFile("./", currentFile)
    purchaseJSON = readFromJSONFile("./", "purchase.json")
    registry = readFromJSONFile("./", registryFile)

    #FOOD
    if kind == "Food":
        num = 1;
        #print(purchaseJSON)
        for food in purchaseJSON["Food"]:
            print(str(num) + ". " + food["name"] + "     " + str(food["price"]) + "\n")
            num +=1

        chosen = input("Type the number of the order you want to add\n")

        if int(chosen) > num:
            print("Invalid choice")
            LoadAssets(kind, purchaseJSON)

        amount = input("Type the amount of the order you want to add\n")

        b = purchaseJSON["Food"]
        count = 0
        for x in b:
            count +=1
            if int(chosen) == count:
                 return (x["price"] * int(amount),  datetime.datetime.now(), x["name"])

   #DRINK
    if kind == "Drink":
        num = 1;
        drink = "";
        for drink in purchaseJSON["Drink"]:
            print(str(num) + ". " + drink["name"] + "     " + str(drink["price"]) + "\n")
            num += 1

        chosen = input("Type the number of the order you want to add\n")

        if int(chosen) > num:
            print("Invalid choice")
            LoadAssets(kind, purchaseJSON)
            
        amount = input("Type the amount of the order you want to add\n")

        b = purchaseJSON["Drink"]
        count = 0
        for x in b:
            count+=1
            if int(chosen) == count:
                return (x["price"] * int(amount), datetime.datetime.now(), x["name"])

    #SNACK
    if kind == "Snack":
        num = 1;
        snack = "";
        for snack in purchaseJSON["Snack"]:
            print(str(num) + ". " + snack["name"] + "     " + str(snack["price"]) + "\n")
            num += 1

        chosen = input("Type the number of the order you want to add\n")

        if int(chosen) > num:
            print("Invalid choice")
            LoadAssets(kind, purchaseJSON)
            
        amount = input("Type the amount of the order you want to add\n")

        b = purchaseJSON["Snack"]
        count = 0
        for x in b:
            count+=1
            if int(chosen) == count:
                return (x["price"] * int(amount), datetime.datetime.now(), x["name"])


    #LAUNDRY           
    if kind == "Laundry":
        kilos = input("Enter kilos of laundry\n")
        pay = int(kilos) * purchaseJSON["Laundry"]["cost/kilo"]
        timeordered = datetime.datetime.now()

        return (pay, timeordered, "Laundry")

    if kind == "Other":
        print("Enter name of service or product\n")
        print("This function has yet to be added\n")
        #todo

    Intro()


def MakeOrder(room, cost, timestamp, name):
    
    current = readFromJSONFile("./", currentFile)
    ordernum = readFromJSONFile("./", "ordernum.json")
    ordernum += 1
    latest = FindLatestOrder(room)

    if 1 == 2:
        print("No log found, customer not checked in")
    else:

        if readFromJSONFile("./", registryFile) == {}:
            datastruct = {}

        else:
            datastruct = readFromJSONFile("./", registryFile)

        datastruct[ordernum] = {}
        datastruct[ordernum][room] = []

        timenow = datetime.datetime.now()

        start = str(timenow)
        
        datastruct[ordernum][room] = ({
            'name' : datastruct[latest][room]["name"],
            'passport' : datastruct[latest][room]["passport"],
            'checkin' : datastruct[latest][room]["checkin"],
            'checkout' : datastruct[latest][room]["checkout"],
            'debt' : round(int(cost)),
            'orders': [],
            'lastchanged' : start
            })

        datastruct[ordernum][room]["orders"].append({
                "name" : name,
                "cost" : cost,
                "time" : str(datetime.datetime.now())
                })                  
     
        writeToJSONFile("./", "ordernum.json", ordernum)
        writeToJSONFile("./", currentFile, datastruct)
        writeToJSONFile("./", registryFile, datastruct)

    Intro()

def Buy():
    print("Purchase")
    room = input("Enter your room number\n")

    current = readFromJSONFile("./", currentFile)
             
    print("Choose category\n")
    print("1. Food\n")
    print("2. Drink\n")
    print("3. Snack\n")
    print("4. Laundry\n")
    print("5. Other\n")
    print("6. Exit\n")

    inp = input("Type the name or number of category, followed by enter\n")
    #inp = input("Type what they purchased by the code and press enter\n")
    print("type 'exit' followed by enter to leave/n")

    if inp == "1" or inp == "Food":
        a, b, name = LoadAssets("Food")
        MakeOrder(room, a, b, name)
    elif inp == "2" or inp == "Drink":
        a, b, name = LoadAssets("Drink")
        MakeOrder(room, a, b, name)
    elif inp == "3" or inp == "Snack":
        a, b, name = LoadAssets("Drink")
        MakeOrder(room, a, b, name)
    elif inp == "4" or inp == "Laundry":
        a, b, name = LoadAssets("Laundry")
        MakeOrder(room, a, b, name)
    elif inp == "5" or inp == "Other":
        a, b, name = LoadAssets("Other")
        MakeOrder(room, a, b, name)
    elif inp == "6" or inp == "Exit":
        Intro()
    else:
        print("Input unrecognized")
        Intro()
                    
    print("No customer signed in here")
    Intro()
     
Intro()

def mergeDict(dict1, dict2):
    merged_dict = {key: value for (key, value) in (dict1.items() + dict2.items())}
    json = json.dumps(merged_dict)
    return json

def UpdateCheckout(current, key, room, days):

    print("in update")
    #Read old file key
    top = int(current[key][room]["debt"])
    top -= int(payoff)
    print(top)
  

    #Add order number
    ordernum = readFromJSONFile("./", "ordernum.json")
    ordernum += 1
    
    writeToJSONFile("./", "ordernum.json", ordernum)

    current[ordernum] = {}
    current[ordernum][room] = []

    #addtodebt
    

    current[ordernum][room] = ({
        'name' : current[key][room]["name"],
        'passport' : current[key][room]["passport"],
        'checkin' : current[key][room]["checkin"],
        'checkout' : current[key][room]["checkout"],
        'debt' : str(top),
        'lastchanged' : str(datetime.datetime.now())
        })

    after = json.loads(json.dumps(current))

    print("Customer" + str(key) + " paid off " + payoff)

    return after
                
Intro()

#update price in editor for purchasable items
