import random

def generate_contact_plan():
    # Number of nodes and time interval
    num_nodes = 66
    time_interval = 10  # 0 to 119 minutes

    # Initialize a contact plan as a list of tuples (node1, node2, start_time, end_time)
    contact_plan = []

    # Randomly generate contacts between nodes
    for _ in range(3):  # Adjust the number of contacts as needed
        node1, node2 = random.sample(range(num_nodes), 2)
        start_time = random.randint(0, time_interval)
        end_time = start_time + random.randint(1, 3)
        contact_plan.append((node1, node2, start_time, end_time))

    # Sort the contact plan by start time
    contact_plan.sort(key=lambda x: x[2])

    return contact_plan

#contact_plan = generate_contact_plan()
# Print the contact plan
#for contact in contact_plan:
#    node1, node2, start_time, end_time = contact
#    print(f"Nodes {node1} and {node2} in contact from {start_time} to {end_time} minutes.")


    