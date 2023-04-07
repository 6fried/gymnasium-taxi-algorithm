#!/usr/bin/env python

import gymnasium

env = gymnasium.make("Taxi-v3", render_mode="human")
observation, _ = env.reset()
rewards = 0

reward, terminated, truncated, info = 0, 0, 0, 0

# utilities
# utility class to represent a
# vector with two properties: x and y
class Vector:
    def __init__(self, x=-1, y=-1) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

# unnamed utility function
def f(state, ind):
    for i in range(ind):
        if ((state - i) % ind == 0):
            return i

# utility function to get destination, passenger
# and taxi location from observation or state
def get_params(obs):
    """
    Return the taxi, the passenger and the destination's coordinates in 
    the 2D frame of the environment. position (0, 0) is the top-left corner 
    according to pygame's representation
    
    Args:
        obs: an OservationTpe object that'll let us find the state

        state = ((taxi_row * 5 + taxi_col) * 5 + passenger_location) * 4 + destination

        where:
        
        taxi_row and taxi_col are in range(5) 
            taxi_row = taxi_y
            taxi_column = taxi_x

        passenger_location is 0:Passenger locations:
            0: Red
            1: Green
            2: Yellow
            3: Blue
            4: In taxi

        destination is:
            0: Red
            1: Green
            2: Yellow
            3: Blue
    """
    # basic state components

    dest = -1
    pass_loc = -1
    t = Vector()

    # advanced parameters
    # passenger and location coordinnates
    v_dest = Vector()
    v_pass = Vector()

    # get the state
    val_list = list(env.P[obs].values())
    state = val_list[4][0][1]

    # dest
    # (state - dest) is a multiple of 4
    dest = f(state, 4)

    # pass_loc
    state = (state - dest) / 4
    pass_loc = f(state, 5)

    # taxi_column / taxi_x
    state = (state - pass_loc) / 5
    t.x = f(state, 5)

    t.y = int((state - t.x) / 5)

    match pass_loc:
        case 0: # red
            v_pass.x, v_pass.y = 0, 0
        case 1: # green
            v_pass.x, v_pass.y = 4, 0
        case 2: # yellow
            v_pass.x, v_pass.y = 0, 4
        case 3: # blue
            v_pass.x, v_pass.y = 3, 4
        case 4: # in-car
            v_pass.x, v_pass.y = t.x, t.y
        case _:
            pass
    
    match dest:
        case 0: # red
            v_dest.x, v_dest.y = 0, 0
        case 1:  # green
            v_dest.x, v_dest.y = 4, 0
        case 2: # yellow
            v_dest.x, v_dest.y = 0, 4
        case 3: # blue
            v_dest.x, v_dest.y = 3, 4
        case _:
            pass

    # print(f"dest: {v_dest}, pass:{v_pass} taxi: {t}")
    return v_dest, v_pass, t

# utility function to give a value to destination, 
# passenger and value
def get_p():
    global destination, passenger, taxi
    destination, \
        passenger, \
        taxi = get_params(observation)

def make_action(action):
    global observation, terminated, truncated, info, rewards
    observation, reward, terminated, truncated, info = env.step(action)
    rewards += reward
    print(f"    Action: {get_action_name(action)}")
    print(f"    Reward: {reward}")
    print(f"    Score: {rewards}\n")
    env.render()

# utility function that gets an action name from the number
def get_action_name(action):
    match action:
        case 0:
            return "Move South (down)"
        case 1:
            return "Move North (up)"
        case 2:
            return "Move East (right)"
        case 3:
            return "Move West (left)"
        case 4:
            return "Pickup Passenger"
        case 5:
            return "Drop off Passenger"
        case _:
            return "Undefined Action"


destination, \
    passenger, \
    taxi = get_params(observation)

print("STEP1: Go to the passenger")
# go to y = 2
action = 0 if taxi.y < 2 else 1
while(taxi.y != 2):
    make_action(action)
    get_p()

# go to passenger column
action = 3 if passenger.x - taxi.x < 0 else 2
while(passenger.x - taxi.x != 0):
    make_action(action)
    get_p()


# go to passenger line
action = 1 if (passenger.y < taxi.x) else 0
while(passenger.y != taxi.y):
    make_action(action)
    get_p()


make_action(4)

print("\nSTEP2: Go to destination")
# go to y = 2
action = 0 if taxi.y < 2 else 1
while(taxi.y != 2):
    make_action(action)
    get_p()


# go to passenger column
action = 3 if destination.x - taxi.x < 0 else 2
while(destination.x - taxi.x != 0):
    make_action(action)
    get_p()


# go to destination line
action = 1 if destination.y - taxi.y < 0 else 0
while(destination.y - taxi.y != 0):
    make_action(action)
    get_p()


make_action(5)


if terminated or truncated:
    print("End")
    env.close()