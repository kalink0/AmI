'''
Created on Apr 21, 2013

@author: inkognito
'''

from ControlCenter import ControlCenter

if __name__ == '__main__':
    
    control = ControlCenter.ControlCenter()
    controlbyte = -1
    rfidnumber = 0
    print "Welcome to the Control Center for the Smart Senseo machine!"
    print "Enjoy your coffee responsible!"
    
    print "Current status: "
    currentstatus = control.getStatus()
    if (currentstatus & 0x01) == 0x00 :
        print "Machine is offline"  
    elif currentstatus == 1 :
        print "Machine is online, no water, no cup"
    elif currentstatus == 0x03 :
        print "Machine is online, let's start"
    elif currentstatus == 0x09 :
        print "Machine is online, no water" 
    elif currentstatus == 0x0B :
        print "Machine is online, let's start"
    else :
        print "Machine is online, someone is currently making a coffee!"   

    while controlbyte != 0 :
        print "What do you want to do?"
        print "1 = Switch on/off the machine"
        print "2 = Make a small cup of coffee"
        print "4 = Make a tall cup of coffee"
        print "0 = Exit application"
        
        controlbyte = input ("Your decision ?: ")
        currentstatus = control.getStatus()
        
        #Machine is offline, but user want to start a job
        if (currentstatus & 0x01) == 0 and (controlbyte & 0x0E) != 0 :
            print "Please switch on the Machine with 1"
            continue
        
        #Machine is offline and user wants to start it
        if (currentstatus & 0x01) == 0 and (controlbyte & 0x01) == 1 :
            print "Starting the machine"
            control.switchStatus()
            while (control.getStatus() & 0x01 != 1 ) :
                pass
            print "Machine is now online"
            continue
        
        #User wants to shutdown the machine, but there is an active job
        if (currentstatus & 0x04) == 1 and (controlbyte & 0x01) == 1 :
            print "Cannot shutdown the machine, a job is running"
            print " I will wait until the job is finished"
            while (control.getStatus() & 0x04) != 0 :
                pass
            print " Okay, I will shutdown the machine now for you"
            control.switchStatus()
            continue
 
        #User wants to start a job, but there is an active job
        if (currentstatus & 0x04) == 1 and (controlbyte & 0x06) != 0 :
            print "Cannot start a job, the machine is busy!"
            print " I will wait until the job is finished"
            while (control.getStatus() & 0x04) != 0 :
                pass
            print " Okay, now i will start with your coffee"
            #control.switchStatus()
            continue       
        #User wants to start a job, but there is no water in the machine
        if (currentstatus & 0x02) != 0x02 and (controlbyte & 0x06) != 0 :
            print "Sorry, I cannot start your job, there is no water in the machine"
            continue
        
        #User wants to start a job, but there is no cup recognized
        ''''if (currentstatus & 0x08) != 0x08 and (controlbyte & 0x06) != 0 :
            print "Sorry, I cannot start your job, there is no cup in the machine"
            continue
        else :
            rfidnumber = control.getRFIDNumberFromMachine()
            control.searchUsedRFID()
        '''
        #rfidnumber = control.getRFIDNumberFromMachine()
        #control.searchUsedRFID()
        if controlbyte == 0x01 :
            print "I shut down the machine"
            control.switchStatus();
            while (control.getStatus() & 0x01 != 0 ) :
                pass
            print "Machine is now offline"
            continue
        
        if controlbyte == 0x04 :
            print "I make a tall cup for you"
            control.fillCup(2)
            continue
        elif controlbyte == 0x02 :
            print "I make a small cup you"
            control.fillCup(1)
            continue
    
    del control