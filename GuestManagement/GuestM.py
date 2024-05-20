
class Guest:
    # Constructor
    def __init__(self,Fname:str,LName:str,rank:int,age:int):
        self.FName = Fname
        self.LName = LName
        self.Rank = rank
        self.Age  = age

    # Getters
    def GetF_Name(self):
        return self.FName
    def GetL_Name(self):
        return self.LName
    def GetRank(self):
        return self.Rank
    def GetAge(self):
        return self.Age

    #Methods
    def Information(self):
        return f"My name is {self.FName} {self.LName} and i have a rank of:{self.Rank} and My Age is:{self.Age}"
