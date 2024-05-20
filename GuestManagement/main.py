import matplotlib.pyplot as ptl
import numpy as np
import mysql.connector
from ManagerM import GuestManager
from GuestM import Guest

#Get a connection and create a list of objects Guest to store it in an object ManagerM
def GetGuests():
    #==========================Retrieve the data from the database=================================
    cnn = mysql.connector.connect(host="localhost",user="root",passwd="password",database="guests")
    cur = cnn.cursor()
    cur.execute("SELECT * FROM myguests")
    Data = cur.fetchall()#Get a touple list
    #==============================================================================================
    GuestObjects = []
    for x in Data:
        MyGuest = Guest(x[1],x[2],x[3],x[4])#Generate a Guest object
        GuestObjects.append(MyGuest) #Save the object in the list

    return GuestObjects #Return the list of Guest objects created

#=========================================================================================

#=====================================MAIN================================================
def main():
#=======================Get the guest from the database===================================
    MyListOfGuest = GetGuests()
#============================Fill the MyManage============================================
    MyManage = GuestManager()
    for x in MyListOfGuest:
        MyManage.AppendGuest(x) #x = each Guest object to add to my principal class

    MyManage.ShowGuests()
    MyManage.ShowLoyaltyGuest()
#=========================================================================================

#========================Display the graphic of loyalGuests================================
    Names = []
    Rank = []
    for x in MyListOfGuest:
        Names.append(x.GetF_Name())
        Rank.append(x.GetRank())

    #Plot data
    x = np.array(Names)
    y = np.array(Rank)
    ptl.bar(x,y)
    ptl.show()

if __name__ == "__main__":
    main()










