# Build a list of Bus, route and stop objects from JSON file downloaded from:
# http://golynx.doublemap.com/map/v2/buses
# http://golynx.doublemap.com/map/v2/routes
# http://golynx.doublemap.com/map/v2/stops

import json
from collections import namedtuple
import time

# Convert json dictionary into a a list of objects
# based on: https://pynative.com/python-convert-json-data-into-custom-python-object/
def custom_json_decoder( c_name, inDict ):
    createdClass = namedtuple( c_name, inDict.keys())(*inDict.values())
    return createdClass 

# Load and parse the JSON files
# create a list of objects from the specified JSON file
def load_lynx_json ( c_name, f_name):
    with open( f_name, 'r' ) as fp: 
        #Load the JSON 
        json_dict = json.load(fp)
        class_list = []
        for i in range( len( json_dict)) :
            tmp = custom_json_decoder( 'X', json_dict[i])
            class_list.append(tmp)
        return class_list
            
# Given a stop code, such as "1745", lookup the corresponding stop info
def search_stops_by_code ( target_code, stop_list ):
    for this_stop in range(len(stop_list)) :
        #print(str(stop_list[this_stop].id) + "," + stop_list[this_stop].name )
        if stop_list[this_stop].code == target_code :
            return stop_list[this_stop]

# Count the number of elements in JSON file (recursion)
          
def element_count(list, c=0):
    for item in range(len(list)):
      if isinstance(list[item], dict):
        c = element_count(list[item], c + 1)
      else:
        c += 1
    return c
  
# For any given bus, print the name of the route
def find_route_for_bus(route_list,bus_list, bus):
      for this_bus in range(len(bus_list)):
        if bus_list[this_bus].name == bus:
          for this_route in range(len(route_list)):
            if route_list[this_route].id == bus_list[this_bus].route:
              return route_list[this_route].name
            
          
          
        
# Given stop id (not a stop code), say 501932
# return a list of stops on that route
def search_routes_for_stop( stop_id, route_list ):
    for this_route in range(len(route_list)) :
        for this_stop in range( len(route_list[this_route].stops)):
            if route_list[this_route].stops[this_stop] == stop_id:
                return route_list[this_route]
    
# Loop through the list of target stops for the selected route 
# (the one containing our target stop).  Lookup each stop 
# in the  master stops list and print out the name, marking
# the target stop with a *
def print_stop_names( route_info, stops_list, target_stop_code ):
    for route_stop in route_info.stops:
        for i in range( len(stops_list)):
            if route_stop == stops_list[i].id:
                if stops_list[i].code == target_stop_code:
                    print( '*', end='')
                print( stops_list[i].code + " " + stops_list[i].name)
            
def main():

    target_stop = '3486'
    
    # Buses - not used in this example (future use)
    master_buses_list = load_lynx_json( 'Buses', "buses.json")

    # Stops
    master_stops_list = load_lynx_json( 'Stops', "stops.json")

    # Routes
    master_routes_list = load_lynx_json( 'Routes', "routes.json")

    elements = element_count(master_buses_list)
    print("Elements in bus file: " + str(elements))
    elements = element_count(master_stops_list)
    print("Elements in stops file: " + str(elements))
    elements = element_count(master_routes_list)
    print("Elements in route file: " + str(elements))

    
    bus = "174-415"
    route_info = find_route_for_bus(master_routes_list,master_buses_list, bus)
    print("Bus " + bus + " is on route " + str(route_info))

    
    

    # get time in nanoseconds -- maybe OS-specific?
    # See https://docs.python.org/3/library/time.html
    t0 = time.perf_counter_ns() 
    
    # find the stop info for this target stop
    target_stop_info = search_stops_by_code( target_stop, master_stops_list)
    # print( target_stop_info.id)
    # print(target_stop_info.code)

    route_info_for_stop = search_routes_for_stop( target_stop_info.id, master_routes_list)
    #print( route_info_for_stop )

    # print_stop_names( route_info_for_stop, master_stops_list, target_stop )
    t1 = time.perf_counter_ns() - t0
    # print( "elapsed " + str(t1))
    
if __name__ == "__main__":
    main( )