#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the bicycle domain.  

'''
bicycle STATESPACE 
'''
#   You may add only standard python imports---i.e., ones that are automatically
#   available on CDF.
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

from search import *
from random import randint
from math import sqrt

class bicycle(StateSpace):
    def __init__(self, action, gval, curr_jobs, curr_location, curr_time, curr_money, unstarted_jobs, parent = None):
#IMPLEMENT
        '''Initialize a bicycle search state object.'''
        if action == 'START':   #NOTE action = 'START' is treated as starting the search space
            StateSpace.n = 0


        StateSpace.__init__(self, action, gval, parent)
        #implement the rest of this function.
        self.curr_jobs = curr_jobs
        self.curr_location = curr_location
        self.curr_time = curr_time
        self.curr_money = curr_money
        self.unstarted_jobs = unstarted_jobs

    def successors(self): 
#IMPLEMENT
        '''Return list of bicycle objects that are the successors of the current object'''

        States = list()
        travel_time = get_travel_time(self.curr_location, bicycle.map)
        end_time = 1140

        # Delivery
        if self.action != 'START':
            for i in range(len(self.curr_jobs)):
                each_job = self.curr_jobs[i]
                destination = each_job[3]
                travel_time_to_destination = travel_time[destination]
                new_time = self.curr_time + travel_time_to_destination
                new_current_jobs = self.curr_jobs[:i] + self.curr_jobs[i+1:]
                earning = self.get_earning(each_job, new_time)
                action_name = "deliver(" + str(each_job[0]) + ")"
                max_earning = each_job[5][0][1]
                gval_diff = max_earning - earning
                if new_time <= end_time:
                    States.append(bicycle(action_name, self.gval + gval_diff, new_current_jobs, destination, new_time, self.curr_money + earning, self.unstarted_jobs, self))

        # Pickups
        current_weight = self.get_load()
        tuple_curr_jobs = tuple(self.curr_jobs)
        current_delivery_locations = self.get_delivery_locations()

        for i in range(len(self.unstarted_jobs)):
            each_job = self.unstarted_jobs[i]
            pickup_location = each_job[1]

            if pickup_location in current_delivery_locations:
                continue

            pickup_time = each_job[2]
            new_unstarted_jobs = self.unstarted_jobs[:i] + self.unstarted_jobs[i+1:]

            if self.action == 'START':
                current_jobs = list()
                current_jobs.append(each_job)
                action_name = "first_pickup(" + str(each_job[0]) + ")"
                States.append(bicycle(action_name, self.gval, current_jobs, pickup_location, pickup_time, 0, new_unstarted_jobs, self))
            elif current_weight + each_job[4] <= 10000:
                current_jobs = list(tuple_curr_jobs)
                action_name = "pickup(" + str(each_job[0]) + ")"
                time = max(pickup_time, self.curr_time + travel_time[pickup_location])
                current_jobs.append(each_job)
                if time <= end_time:
                    States.append(bicycle(action_name, self.gval, current_jobs, pickup_location, time, self.curr_money, new_unstarted_jobs, self))
            else:
                continue

        return States

    def hashable_state(self):  # IMPLEMENT
        '''Return a data item that can be used as a dictionary key to UNIQUELY represent the state.'''

        carrying_tuple = tuple(self.get_carrying())
        unstarted_tuple = tuple(self.get_unstarted())
        hashable = (self.curr_time, self.curr_location, self.curr_money, carrying_tuple, unstarted_tuple)
        return hashable

    def print_state(self):
        #DO NOT CHANGE THIS FUNCTION---it will be used in auto marking
        #and in generating sample trace output. 
        #Note that if you implement the "get" routines below properly, 
        #This function should work irrespective of how you represent
        #your state. 

        if self.parent:
            print("Action= \"{}\", S{}, g-value = {}, (From S{})".format(self.action, self.index, self.gval, self.parent.index))
        else:
            print("Action= \"{}\", S{}, g-value = {}, (Initial State)".format(self.action, self.index, self.gval))
            
        print("    Carrying: {} (load {} grams)".format(
                      self.get_carrying(), self.get_load()))
        print("    State time = {} loc = {} earned so far = {}".format(
                      self.get_time(), self.get_loc(), self.get_earned()))
        print("    Unstarted Jobs.{}".format(self.get_unstarted()))

    def get_earning(self, job, time):
        ''' Calculate amount of money recieved from a particular delivery at a particular time'''

        payoffs = job[5]

        for payoff_pair in payoffs:
            if time <= payoff_pair[0]:
                return payoff_pair[1]
        return 0

    def get_delivery_locations(self):
        'returns the delivery locations of all packages that are currently being carried in a list'

        delivery_locations = list()
        for each_job in self.curr_jobs:
            delivery_locations.append(each_job[3])
        return delivery_locations

    def get_loc(self): #IMPLEMENT
        '''Return location of courier in this state'''

        return self.curr_location

    def get_carrying(self): #IMPLEMENT
        '''Return list of NAMES of jobs being carried in this state'''

        carrying = list()

        for each_job in self.curr_jobs:
            carrying.append(each_job[0])

        return carrying
    
    def get_load(self): #IMPLEMENT
        '''Return total weight being carried in this state'''
        # Calculate current weight in basket
        current_weight = 0
        for each_package in self.curr_jobs:
            current_weight += each_package[4]

        return current_weight

    def get_time(self): #IMPLEMENT
        '''Return current time in this state'''
        return self.curr_time

    def get_loc(self): #IMPLEMENT
        '''Return current location in this state'''
        return self.curr_location

    def get_earned(self): #IMPLEMENT
        '''Return amount earned so far in this state'''
        return self.curr_money

    def get_unstarted(self): #IMPLEMENT
        '''Return list of NAMES of jobs not yet stated in this state'''
        unstarted = list()

        for each_job in self.unstarted_jobs:
            unstarted.append(each_job[0])

        return unstarted

bicycle.map = False

def get_travel_time(location, map):
    ''' Calculate current distance to every other location. Returns a dictionary'''

    travel_time = {}

    if location == "home":
        for location in map[0]:
            travel_time[location] = 0
    else:
        distance_list = map[1]
        #print(map[1])

        for each_edge in distance_list:
            #print(each_edge)
            if each_edge[0] == location:
                location_a = travel_time.keys()
                if each_edge[1] in location_a:
                    continue
                else:
                    travel_time[each_edge[1]] = each_edge[2]
            elif each_edge[1] == location:
                location_b = travel_time.keys()
                if each_edge[0] in location_b:
                    continue
                else:
                    travel_time[each_edge[0]] = each_edge[2]
            else:
                continue
        # adding in our current location
        travel_time[location] = 0
        
    return travel_time

def heur_null(state):
    '''Null Heuristic use to make A* search perform uniform cost search'''
    return 0

def get_lost_revenue_carried(state):
    '''For every carried job, Lost revenue if we immediately travel to J's dropoff point and deliver J.
    Returns a list'''
    travel_times = get_travel_time(state.curr_location, bicycle.map)

    lost_revenue_carried = list()

    for each_job in state.curr_jobs:
        max_earning = each_job[5][0][1]
        #print(max_earning)
        time_reach_destination = travel_times[each_job[3]] + state.curr_time
        #print(time_reach_destination)
        actual_earning = state.get_earning(each_job, time_reach_destination)
        #print(actual_earning)
        diff_carried_jobs = max_earning - actual_earning

        lost_revenue_carried.append(diff_carried_jobs)

    return lost_revenue_carried

def get_lost_revenue_unstarted(state):
    '''For every unstarted job, Lost revenue if we immediately travel to J's pickup point then to J's dropoff poing and then deliver J.
    Returns a list'''

    # Sum over unstarted jobs
    travel_times = get_travel_time(state.curr_location, bicycle.map)
    #print(travel_times)
    lost_revenue_unstarted = list()

    for each_job in state.unstarted_jobs:
        #print(each_job)
        max_earning = each_job[5][0][1]
        time_to_pickup = travel_times[each_job[1]]
        #print(time_to_pickup)
        travel_times_delivery = get_travel_time(each_job[1], bicycle.map)
        time_to_destination = travel_times_delivery[each_job[3]]
        final_time = state.curr_time + time_to_pickup + time_to_destination
        actual_earning = state.get_earning(each_job, final_time)
        diff_unstarted_jobs = max_earning - actual_earning
        lost_revenue_unstarted.append(diff_unstarted_jobs)

    return lost_revenue_unstarted

def heur_sum_delivery_costs(state):  # IMPLEMENT
    '''Bicycle Heuristic sum of delivery costs.'''
    #Sum over every job J being carried: Lost revenue if we
    #immediately travel to J's dropoff point and deliver J.
    #Plus 
    #Sum over every unstarted job J: Lost revenue if we immediately travel to J's pickup 
    #point then to J's dropoff poing and then deliver J.

    # Sum over carried jobs

    carried = get_lost_revenue_carried(state)
    unstarted = get_lost_revenue_unstarted(state)

    return sum(carried) + sum(unstarted)

def heur_max_delivery_costs(state):
#IMPLEMENT
    '''Bicycle Heuristic sum of delivery costs.'''
    #m1 = Max over every job J being carried: Lost revenue if we immediately travel to J's dropoff
    #point and deliver J.
    #m2 = Max over every unstarted job J: Lost revenue if we immediately travel to J's pickup 
    #point then to J's dropoff poing and then deliver J.
    #heur_max_delivery_costs(state) = max(m1, m2)

    carried = get_lost_revenue_carried(state)
    unstarted = get_lost_revenue_unstarted(state)

    if not carried:
        m1 = 0
    else:
        m1 = max(carried)

    if not unstarted:
        m2 = 0
    else:
        m2 = max(unstarted)

    return max(m1, m2)

def bicycle_goal_fn(state):
#IMPLEMENT
    '''Have we reached the goal (where all jobs have been delivered)?'''
    
    if state.unstarted_jobs or state.curr_jobs:
        return False
    return True

def make_start_state(map, job_list):
#IMPLEMENT
    '''Input a map list and a job_list. Return a bicycle StateSpace object
    with action "START", gval = 0, and initial location "home" that represents the 
    starting configuration for the scheduling problem specified'''

    bicycle.map = map
    current_jobs = list()
    unstarted_jobs = job_list

    return bicycle("START", 0, current_jobs, "home", 420, 0, unstarted_jobs, parent = None)

########################################################
#   Functions provided so that you can more easily     #
#   Test your implementation                           #
########################################################

def make_rand_map(nlocs):
    '''Generate a random collection of locations and distances 
    in input format'''
    lpairs = [(randint(0,50), randint(0,50)) for i in range(nlocs)]
    lpairs = list(set(lpairs))  #remove duplicates
    nlocs = len(lpairs)
    lnames = ["loc{}".format(i) for i in range(nlocs)]
    ldists = list()

    for i in range(nlocs):
        for j in range(i+1, nlocs):
            ldists.append([lnames[i], lnames[j],
                           int(round(euclideandist(lpairs[i], lpairs[j])))])
    return [lnames, ldists]

def dist(l1, l2, map):
    '''Return distance from l1 to l2 in map (as output by make_rand_map)'''
    ldist = map[1]
    if l1 == l2:
        return 0
    for [n1, n2, d] in ldist:
        if (n1 == l1 and n2 == l2) or (n1 == l2 and n2 == l1):
            return d
    return 0
    
def euclideandist(p1, p2):
    return sqrt((p1[0]-p2[0])*(p1[0]-p2[0]) + (p1[1]-p2[1])*(p1[1]-p2[1]))

def make_rand_jobs(map, njobs):
    '''input a map (as output by make_rand_map) object and output n jobs in input format'''
    jobs = list()
    for i in range(njobs):
        name = 'Job{}'.format(i)
        ploc = map[0][randint(0,len(map[0])-1)]
        ptime = randint(7*60, 16*60 + 30) #no pickups after 16:30
        dloci = randint(0, len(map[0])-1)
        if map[0][dloci] == ploc:
            dloci = (dloci + 1) % len(map[0])
        dloc = map[0][dloci]
        weight = randint(10, 5000)
        job = [name, ploc, ptime, dloc, weight]
        payoffs = list()
        amount = 50
        #earliest delivery time
        time = ptime + dist(ploc, dloc, map)
        for j in range(randint(1,5)): #max of 5 payoffs
            time = time + randint(5, 120) #max of 120mins between payoffs
            amount = amount - randint(5, 25)
            if amount <= 0 or time >= 19*60:
                break
            payoffs.append([time, amount])
        job.append(payoffs)
        jobs.append(job)
    return jobs

def test(nloc, njobs):
    map = make_rand_map(nloc)
    jobs = make_rand_jobs(map, njobs)
    print("Map = ", map)
    print("jobs = ", jobs)
    s0 = make_start_state(map, jobs)
    print("heur Sum = ", heur_sum_delivery_costs(s0))
    print("heur max = ", heur_max_delivery_costs(s0))
    se = SearchEngine('astar', 'full')
    #se.trace_on(2)
    final = se.search(s0, bicycle_goal_fn, heur_max_delivery_costs)