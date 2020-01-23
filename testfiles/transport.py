from collections import deque

class Factory:
    def __init__(self, value, garage: list, available_points: list):
        self.containers_deque = deque(value)
        self.garage = garage
        self.available_points = available_points
        
    def loading_trucks(self):
        for truck in self.garage:
            if truck.at_start_point:
                if self.containers_deque:
                    truck.loaded = self.containers_deque.popleft()
                    if truck.loaded == 'A':
                        truck.go_to_dest_point(self.available_points[0])
                    if truck.loaded == 'B':
                        truck.go_to_dest_point(self.available_points[1])
            
        
class Port:
    def __init__(self, time, garage: list, available_points: list):
        self.time = time
        self.delivered_objects = 0
        self.garage = garage
        self.available_points = available_points
        
    def loading_boat(self):
        for boat in self.garage:
            if boat.at_start_point:
                if self.delivered_objects:
                    boat.loaded = 'A'
                    boat.go_to_dest_point(self.available_points[0])
        
        
class Transport:
    def __init__(self):
        self.at_start_point = True
        self.delivery_time = 0
        self.dest_point = None
        self.loaded = None

    def go_to_dest_point(self, dest_point):
        self.dest_point = dest_point
        self.delivery_time = 2 * dest_point.time
        self.at_start_point = False

    def timer(self):
        if not self.at_start_point:
            self.delivery_time -= 1
            if self.delivery_time == self.dest_point.time:
                self.dest_point.delivered_objects += 1
            if self.delivery_time == 0:
                self.at_start_point = True
        else:
            pass

        
class DestinationPoint:
    def __init__(self, time):
        self.time = time
        self.delivered_objects = 0


if __name__ == '__main__':
    time_factory_to_B = 5
    time_factory_to_port = 1
    time_port_to_A = 4
    value = input("Enter A or B destination point for each container: ")
    truck_1 = Transport()
    truck_2 = Transport()
    boat = Transport()
    dest_point_A = DestinationPoint(time_port_to_A)
    dest_point_B = DestinationPoint(time_factory_to_B)
    port = Port(time_factory_to_port, [boat], [dest_point_A])
    factory = Factory(value, [truck_1, truck_2], [port, dest_point_B])
    factory_contents = len(factory.containers_deque)
    result_time = 0
    while factory_contents != dest_point_A.delivered_objects + dest_point_B.delivered_objects:
        print("Start")
        factory.loading_trucks()
        print(f"Truck 1 is loaded with {truck_1.loaded}, Truck 2 is loaded with {truck_2.loaded}")
        port.loading_boat()
        print(f"Boat is loaded with {boat.loaded}")
        truck_1.timer()
        truck_2.timer()
        boat.timer()
        result_time += 1
        print(f"Containers delivered to A destination point: {dest_point_A.delivered_objects}")
        print(f"Containers delivered to B destination point: {dest_point_B.delivered_objects}")
        print("END")
    print(f"Containers delivered to A: {dest_point_A.delivered_objects}")
    print(f"Containers delivered to B: {dest_point_B.delivered_objects}")
    print(f"Delivery time: {result_time}")
    
    #Result for AABABBAB = 29
    #Result for ABBBABAAABBB = 39