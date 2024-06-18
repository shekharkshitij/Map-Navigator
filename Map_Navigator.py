import tkinter as tk
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from tkinter import ttk
from tkinter import messagebox

# Define the capital cities of India
capital_cities = {
    1: "Redhills", 2: "Korukkupet", 3: "Perambur", 4: "Tondiarpet", 5: "Ennore",
    6: "Minjur", 7: "Madhavaram", 8: "Sowcarpet", 9: "Puzhal", 10: "Central Railway Station",
    11: "Surapet", 12: "Vallalar Nagar", 13: "Mannadi", 14: "Basin Bridge", 15: "Park Town",
    16: "Periyamet", 17: "Pattalam", 18: "Selavoyal", 19: "ICF Colony", 20: "TVK Nagar",
    21: "Sembiam", 22: "George Town", 23: "VIT Chennai", 24: "BroadWay", 25: "Royapuram",
    26: "Avadi", 27: "IIIT Kancheepuram", 28: "Anna Uni", 29: "IIT Madras"
}

# Define the connections where each city is connected to 3 other cities with distances and costs
city_connections = {
    1: [(2, 18, 20), (3, 11, 30), (4, 18, 40), (10, 18, 37)],
    2: [(1, 18, 20), (5, 12, 25), (6, 21, 35), (7, 10, 45), (10, 4, 47)],
    3: [(1, 11, 30), (8, 7, 22), (9, 7, 32), (10, 8, 42)],
    4: [(1, 18, 40), (11, 23, 21), (12, 23, 31), (13, 5, 41)],
    5: [(2, 12, 25), (14, 16, 28), (15, 19, 38), (16, 18, 48), (11, 21, 45)],
    6: [(2, 21, 35), (12, 25, 23), (7, 19, 33), (8, 23, 43)],
    7: [(2, 10, 45), (6, 19, 33), (21, 5, 36), (22, 10, 46)],
    8: [(3, 7, 22), (6, 23, 43), (23, 56, 23), (24, 1, 33), (25, 3, 43)],
    9: [(3, 7, 32), (13, 13, 21), (10, 12, 31), (26, 16, 29), (27, 46, 39), (28, 24, 49)],
    10: [(3, 8, 42), (29, 13, 27), (9, 12, 31), (1, 18, 37), (2, 4, 47)],
    11: [(4, 23, 21), (13, 16, 25), (5, 21, 45)],
    12: [(4, 23, 31), (6, 25, 23), (14, 16, 28), (13, 18, 38), (18, 13, 48)],
    13: [(4, 5, 41), (9, 13, 21), (12, 18, 38), (11, 16, 25), (16, 4, 45), (14, 3, 38), (18, 8, 48)],
    14: [(5, 16, 28), (12, 16, 28), (13, 3, 38)],
    15: [(5, 19, 38), (19, 9, 24), (16, 1, 34), (17, 3, 44)],
    16: [(5, 18, 48), (13, 4, 45), (15, 1, 34), (18, 8, 26), (19, 8, 36), (20, 7, 46)],
    17: [(15, 3, 44), (21, 4, 23), (22, 5, 33), (23, 55, 43)],
    18: [(13, 8, 48), (16, 8, 26), (26, 24, 49), (12, 13, 48)],
    19: [(15, 9, 24), (16, 8, 36), (26, 21, 49)],
    20: [(16, 7, 46), (21, 1, 45)],
    21: [(17, 4, 23), (20, 1, 45), (22, 7, 33), (7, 5, 36)],
    22: [(17, 5, 33), (21, 7, 33), (7, 10, 46)],
    23: [(17, 55, 43), (24, 40, 29), (25, 40, 39), (26, 39, 49), (8, 56, 23)],
    24: [(8, 1, 33), (23, 40, 29), (25, 2, 39), (26, 28, 49)],
    25: [(8, 3, 43), (23, 40, 39), (24, 2, 39), (26, 30, 36), (27, 51, 46)],
    26: [(25, 30, 36), (23, 39, 49), (24, 28, 49), (19, 21, 49), (18, 24, 49),(9,16,29)],
    27: [(9, 46, 39), (25, 51, 46), (28, 30, 23)],
    28: [(27, 30, 23), (29, 0.8, 33),(9,24,49)],
    29: [(10, 13, 27), (28, 0.8, 33)]
}

def dijkstra(WList, start_city, end_city):

    infinity = 1 + len(WList.keys()) * max([d for u in WList.keys() for (_, d, _) in WList[u]])
    visited, distance, path = {}, {}, {}

    for city in WList.keys():
        visited[city] = False
        distance[city] = infinity
        path[city] = []

    distance[start_city] = 0

    while True:
        min_dist = infinity
        next_city = None

        for city in WList.keys():
            if not visited[city] and distance[city] < min_dist:
                min_dist = distance[city]
                next_city = city

        if next_city is None:
            break

        visited[next_city] = True

        for (neighbor, dist, cost) in WList[next_city]:
            if not visited[neighbor]:
                if distance[next_city] + dist < distance[neighbor]:
                    distance[neighbor] = distance[next_city] + dist
                    path[neighbor] = path[next_city] + [next_city]

    shortest_path = path[end_city] + [end_city]
    return distance[end_city], shortest_path

def find_shortest_distance():

    start_city_name = start_city_var.get()
    end_city_name = end_city_var.get()

    # Use a dictionary to map city names to city numbers
    city_name_to_number = {v: k for k, v in capital_cities.items()}

    # Check if the selected city names exist in the dictionary
    if start_city_name in city_name_to_number and end_city_name in city_name_to_number:
        start_city = city_name_to_number[start_city_name]
        end_city = city_name_to_number[end_city_name]

        shortest_distance, path = dijkstra(city_connections, start_city, end_city)
        path_cities = [capital_cities[city] for city in path]
        
        # Calculate the total cost by summing up the costs along the path
        total_cost = sum([cost for city in path[:-1] for neighbor, _, cost in city_connections[city] if neighbor == path[path.index(city) + 1]])

        path_string = f"Path: {' -> '.join(path_cities)}"
        result_label.config(text=f"Shortest Distance from {start_city_name} to {end_city_name}: {shortest_distance} km")
        cost_label.config(text=f"Total Cost: {total_cost} units")
        path_label.config(text=path_string)

        # Visualize the graph with a larger size and clear layout
        G = nx.Graph()
        for city in city_connections.keys():
            for (neighbor, dist, cost) in city_connections[city]:
                G.add_edge(capital_cities[city], capital_cities[neighbor], weight=dist)

        fig, ax = plt.subplots(figsize=(12, 10))
        pos = nx.spring_layout(G, seed=42)

        node_colors = ['r' if city in path_cities else 'skyblue' for city in G.nodes()]

        nx.draw(G, pos, with_labels=True, node_size=300, node_color=node_colors, font_size=8)

        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)

        plt.title("City Graph", fontsize=16)
        plt.show()
    else:
        result_label.config(text="Invalid city names. Please select cities from the list.")

# ... (Rest of the code remains the same)

# Function to calculate the minimum distance to travel all of India
def calculate_minimum_distance_all():
    
    # Choose a random starting city
    start_city =14
    
    # Create a list to keep track of visited cities
    visited_cities = [start_city]
    total_distance = 0
    
    # Create a list to store the path
    path = [capital_cities[start_city]]
    
    while len(visited_cities) < len(capital_cities):
        min_distance = float('inf')
        next_city = None
        
        for city in city_connections:
            if city not in visited_cities and city_connections[city]:
                for neighbor, distance, _ in city_connections[city]:
                    if neighbor in visited_cities:
                        if distance < min_distance:
                            min_distance = distance
                            next_city = city
        
        if next_city is not None:
            visited_cities.append(next_city)
            total_distance += min_distance
            path.append(capital_cities[next_city])
        else:
            break

    # Add the last leg of the journey back to the starting city
    final_city = path[0]
    final_distance = 0
    for neighbor, distance, _ in city_connections[start_city]:
        if neighbor == visited_cities[-1]:
            final_distance = distance

    total_distance += final_distance
    print(path)

    result_label_all.config(text=f"Minimum Distance to Travel All of Chennai: {total_distance} km")
    path_string = f"Path: {' -> '.join(path)}"
    result_string = f"Minimum Distance to Travel All of Chennai: {total_distance} km\n{path_string}"
    tk.messagebox.showinfo("Travel All India Result", result_string)

def confirm_ride():
    response = tk.messagebox.askyesno("Confirmation", "Are you sure you want to confirm this ride?")
    if response:
        tk.messagebox.showinfo("Ride Confirmed", "Your ride has been confirmed!")

car_models = ["Sedan", "SUV", "Hatchback", "Luxury","Mahindra","Toyota","Skoda"]
# Create the main window
window = tk.Tk()
window.title("Shortest Path Calculator")

# Maximize the window
window.state('zoomed')
frame_width = 500
frame_height = 800

# Set the initial window size
window.geometry(f"{frame_width}x{frame_height}")

# Create a frame for the car selection
car_frame = tk.Frame(window)
car_frame.pack(padx=20, pady=20)

# Create a label for car selection
car_label = tk.Label(car_frame, text="Select a Car:", font=("Arial", 16))
car_label.grid(row=0, column=0)

# Create a variable to store the selected car model
car_var = tk.StringVar()

# Create a dropdown for selecting the car model
car_dropdown = ttk.Combobox(car_frame, textvariable=car_var, values=car_models, font=("Arial", 14))
car_dropdown.grid(row=0, column=1, padx=5)


# Create a frame for the shortest path calculator
shortest_path_frame = tk.Frame(window)
shortest_path_frame.pack(padx=20, pady=20)

# Create labels for start and end cities
start_city_label = tk.Label(shortest_path_frame, text="Start City:", font=("Arial", 16))
start_city_label.grid(row=0, column=0)

end_city_label = tk.Label(shortest_path_frame, text="End City:", font=("Arial", 16))
end_city_label.grid(row=1, column=0)

# Create variables to store the selected city names
start_city_var = tk.StringVar()
end_city_var = tk.StringVar()

# Create dropdowns for selecting start and end cities
start_city_dropdown = ttk.Combobox(shortest_path_frame, textvariable=start_city_var, values=list(capital_cities.values()), font=("Arial", 14))
start_city_dropdown.grid(row=0, column=1, padx=5)

end_city_dropdown = ttk.Combobox(shortest_path_frame, textvariable=end_city_var, values=list(capital_cities.values()), font=("Arial", 14))
end_city_dropdown.grid(row=1, column=1, padx=5)

# Create a button to find the shortest distance
find_shortest_distance_button = tk.Button(shortest_path_frame, text="Find Shortest Distance", command=find_shortest_distance, font=("Arial", 16))
find_shortest_distance_button.grid(row=2, column=0, columnspan=2, padx=5)

# Create a label to display the result
result_label = tk.Label(shortest_path_frame, text="", font=("Arial", 12))
result_label.grid(row=3, column=0, columnspan=2, pady=10)

# Create a label to display the total cost
cost_label = tk.Label(shortest_path_frame, text="", font=("Arial", 12))
cost_label.grid(row=4, column=0, columnspan=2, pady=10)

# Create a label to display the path
path_label = tk.Label(shortest_path_frame, text="", font=("Arial", 12))
path_label.grid(row=5, column=0, columnspan=2, pady=5)

# Create a button to calculate the minimum distance to travel all of India
calculate_all_button = tk.Button(shortest_path_frame, text="TRAVEL ALL CHENNAI", command=calculate_minimum_distance_all, font=("Arial", 16))
calculate_all_button.grid(row=6, column=0, columnspan=2, pady=10)

# Create a label to display the result for traveling all of India
result_label_all = tk.Label(shortest_path_frame, text="", font=("Arial", 12))
result_label_all.grid(row=7, column=0, columnspan=2, pady=10)

# Create a label to display the path for traveling all of India
path_label_all = tk.Label(shortest_path_frame, text="", font=("Arial", 6))
path_label_all.grid(row=8, column=0, columnspan=2, pady=5)

path_frame = tk.Frame(shortest_path_frame)
path_frame.grid(row=8, column=0, columnspan=2)

# Create a list of labels to display paths
path_labels = [tk.Label(path_frame, text="", font=("Arial", 4), wraplength=frame_width - 40) for _ in range(6)]
for i, label in enumerate(path_labels):
    label.grid(row=i, column=0, pady=5, sticky="w")

confirm_button = tk.Button(car_frame,text="Confirm Ride", command=confirm_ride, font=("Arial", 16))
confirm_button.grid(row=8, column=0, columnspan=2, pady=4)

# Start the GUI main loop
window.mainloop()
