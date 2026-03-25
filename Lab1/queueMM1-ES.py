#!/usr/bin/python3

import random
from queue import Queue, PriorityQueue

# ******************************************************************************
# Constants
# ******************************************************************************

SERVICE = 10.0 # SERVICE is the average service time; service rate = 1/SERVICE
ARRIVAL = 100.0 # ARRIVAL is the average inter-arrival time; arrival rate = 1/ARRIVAL
LOAD=SERVICE/ARRIVAL # This relationship holds for M/M/1

TYPE1 = 1 

SIM_TIME = 500000

arrivals=0
users=0
BusyServer=False # True: server is currently busy; False: server is currently idle

MM1=[]


# ******************************************************************************
# To take the measurements
# ******************************************************************************
class Measure:
    def __init__(self,Narr,Ndep,NAveraegUser,OldTimeEvent,AverageDelay):
        self.arr = Narr
        self.dep = Ndep
        self.ut = NAveraegUser
        self.oldT = OldTimeEvent
        self.delay = AverageDelay
        
# ******************************************************************************
# Client
# ******************************************************************************
class Client:
    def __init__(self,type,arrival_time):
        self.type = type
        self.arrival_time = arrival_time

# ******************************************************************************
# Server
# ******************************************************************************
class Server(object):

    # constructor
    def __init__(self):

        # whether the server is idle or not
        self.idle = True


# ******************************************************************************

# arrivals *********************************************************************
def arrival(time, FES, queue):
    global users
    
    #print("Arrival no. ",data.arr+1," at time ",time," with ",users," users" )
    
    # cumulate statistics
    data.arr += 1
    data.ut += users*(time-data.oldT)
    data.oldT = time

    # sample the time until the next event
    inter_arrival = random.expovariate(lambd=1.0/ARRIVAL)
    
    # schedule the next arrival
    FES.put((time + inter_arrival, "arrival"))

    users += 1
    
    # create a record for the client
    client = Client(TYPE1,time)

    # insert the record in the queue
    queue.append(client)

    # if the server is idle start the service
    if users==1:
        
        # sample the service time
        service_time = random.expovariate(1.0/SERVICE)
        #service_time = 1 + random.uniform(0, SEVICE_TIME)

        # schedule when the client will finish the server
        FES.put((time + service_time, "departure"))

# ******************************************************************************

# departures *******************************************************************
def departure(time, FES, queue):
    global users

    #print("Departure no. ",data.dep+1," at time ",time," with ",users," users" )
        
    # cumulate statistics
    data.dep += 1
    data.ut += users*(time-data.oldT)
    data.oldT = time
    
    # get the first element from the queue
    client = queue.pop(0)
    
    # do whatever we need to do when clients go away
    
    data.delay += (time-client.arrival_time)
    users -= 1
    
    # see whether there are more clients to in the line
    if users >0:
        # sample the service time
        service_time = random.expovariate(1.0/SERVICE)

        # schedule when the client will finish the server
        FES.put((time + service_time, "departure"))

        
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ******************************************************************************
# the "main" of the simulation
# ******************************************************************************

ARRIVAL_VALUES = [100, 50, 33.3, 25, 20, 16.7, 14.3, 12.5, 11.1, 10.5]
# rho =           0.1  0.2  0.3  0.4  0.5  0.6   0.7   0.8   0.9  0.95

rho_list = []
EN_list  = []
ET_list  = []
TP_list  = []

for ARRIVAL in ARRIVAL_VALUES:

    # reset variabili
    random.seed(42)
    users = 0
    MM1 = []
    data = Measure(0, 0, 0, 0, 0)
    time = 0
    FES = PriorityQueue()
    FES.put((0, "arrival"))

    # simulazione
    while time < SIM_TIME:
        (time, event_type) = FES.get()
        if event_type == "arrival":
            arrival(time, FES, MM1)
        elif event_type == "departure":
            departure(time, FES, MM1)

    # salva risultati
    rho = SERVICE / ARRIVAL
    rho_list.append(rho)
    EN_list.append(data.ut / time)
    ET_list.append(data.delay / data.dep)
    TP_list.append(data.dep / time)

    print(f"rho={rho:.2f} | E[N]={data.ut/time:.4f} | E[T]={data.delay/data.dep:.4f} | TP={data.dep/time:.4f}")

# ---- PLOT ----
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4))

ax1.plot(rho_list, EN_list, 'o-')
ax1.set_xlabel("ρ (load)")
ax1.set_ylabel("E[N] (avg users)")
ax1.set_title("Avg users in system")
ax1.grid(True)

ax2.plot(rho_list, ET_list, 'o-', color='orange')
ax2.set_xlabel("ρ (load)")
ax2.set_ylabel("E[T] (time units)")
ax2.set_title("Avg sojourn time")
ax2.grid(True)

ax3.plot(rho_list, TP_list, 'o-', color='green')
ax3.set_xlabel("ρ (load)")
ax3.set_ylabel("packets/time unit")
ax3.set_title("Throughput")
ax3.grid(True)

plt.tight_layout()
plt.savefig("task1a_plots.png")
print("Plot salvato: task1a_plots.png")