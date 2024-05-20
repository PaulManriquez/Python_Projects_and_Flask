from GuestM import Guest
class GuestManager:
    def __init__(self):
        self.TotalGuest=[]

    def AppendGuest(self,NewGuest:Guest):
        self.TotalGuest.append(NewGuest)

    def ShowGuests(self):
        if len(self.TotalGuest)!=0:
            i:int = 0
            # Print header
            print("{:<3} {:<15} {:<15} {:<5} {:<5}".format("ID", "First Name", "Last Name", "Rank", "Age"))
            print("-" * 45)

            # Print each guest's information
            for guest in self.TotalGuest:
                print("{:<3} {:<15} {:<15} {:<5} {:<5}".format(i,guest.GetF_Name(), guest.GetL_Name(), guest.GetRank(),guest.GetAge()))
                i+=1
        else:
            print("There are no guest")

    def ShowLoyaltyGuest(self):
        if len(self.TotalGuest)>1:
            print()
            print("Displaying loyal guests:")
            for x in self.TotalGuest:
                if x.GetRank()>=10:
                    print(f"Loyal Guest {x.GetL_Name()}")
        else:
            print("There are no guests")