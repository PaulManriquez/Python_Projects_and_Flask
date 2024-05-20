#Programmer: Paul Manriquez
#Date: May 2024

import time
import timeit


#Function to messure
def Function1():
    print("Starting function 1")
    time.sleep(3)               # We stop a little to be able to messure the execution, otherwise it would be very short time
    print("Ending function 1")

#Function:callable to messure any function
def MessureExecutionTime(Function:callable):
                                    #Function to execute/Number of execution times
    executionTime =timeit.timeit(stmt=Function,number=1)

    #=============== Calculate Time =================================================
    hours = int(executionTime / 3600)
    minutes = int((executionTime / 60) - hours * 60)
    seconds = int(executionTime - (hours * 3600) - (minutes * 60))
    # TotalSecondsLeft: get the current miliseconds in 0.~ format
    TotalSecondsLeft = (executionTime - ((hours * 3600) + (minutes * 60) + (seconds)))
    miliseconds = int(TotalSecondsLeft * 1000)
    #================================================================================

    print("\t Total execution time ")
    print(f"Hours:{hours}\nMinutes:{minutes}\nSeconds:{seconds}\nMiliseconds:{miliseconds}")

#=========================== Main =========================================================
def main():
    MessureExecutionTime(Function1)

if __name__ == "__main__":
    main()