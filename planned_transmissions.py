import random

def generate_planned_transmission():
    # Number of nodes and time interval
    num_nodes = 22
    time_interval = 10  # 0 to 119 minutes

    # Initialize a contact plan as a list of tuples (node1, node2, start_time, end_time)
    contact_plan = []

    # Randomly generate contacts between nodes
    #for _ in range(3):  # Adjust the number of contacts as needed
    #    node1, node2 = random.sample(range(num_nodes), 2)
    #    start_time = random.randint(0, time_interval)
    #    contact_plan.append((node1, node2, start_time))

    contact_plan.append((0, 3, 0))
    contact_plan.append((0, 3, 1))
    contact_plan.append((0, 3, 2))

    # Sort the contact plan by start time
    contact_plan.sort(key=lambda x: x[2])

    return contact_plan


    