import sys
import json
import math  # If you want to use math.inf for infinity
import netfuncs as nf

def get_ad(router):
    return router["ad"]

def to_visit(routers):
    list = []
    for router in routers:
        list.append(router)
    return list

def create_distance_dict(list):
    thisdict = {}
    for x in list:
        thisdict.update({f"{x}":10000000})
    #print(thisdict)
    return thisdict

def create_parent_dict(list):
    thisdict = {}
    for x in list:
        thisdict.update({f"{x}":None})
    #print(thisdict)
    return thisdict

def update_dict(thisdict, var):
    thisdict.update(var)
    #print(thisdict)

def min_ad(routers,router,to_visit):
    min = 1000000000
    save = None
    for connection in routers[f"{router}"]["connections"]:
        if connection in to_visit:
            ad = get_ad(routers[router]["connections"][connection])
            if min > ad:
                min = ad
                save = connection
    return save

def get_neighbors(routers,router):
    neighbors = []
    for connection in routers[f"{router}"]["connections"]:
        neighbors.append(connection)
    return neighbors

def get_path(src_ip, dest_ip, parent_dict, routers, dist_dict):

    src_ip = nf.find_router_for_ip(routers, src_ip)
    dest_ip = nf.find_router_for_ip(routers, dest_ip)

    current_node = dest_ip
    path = []
    path_ad = []

    if src_ip == dest_ip:
        return []

    while current_node != src_ip:
        path.append(parent_dict[current_node])
        path_ad.append(dist_dict[current_node])

        current_node = parent_dict[current_node]
    path.reverse()
    path.append(dest_ip)
    path_ad.reverse()
    return path, path_ad

def dijkstras_shortest_path(routers, src_ip, dest_ip):
    """
    This function takes a dictionary representing the network, a source
    IP, and a destination IP, and returns a list with all the routers
    along the shortest path.

    The source and destination IPs are **not** included in this path.

    Note that the source IP and destination IP will probably not be
    routers! They will be on the same subnet as the router. You'll have
    to search the routers to find the one on the same subnet as the
    source IP. Same for the destination IP. [Hint: make use of your
    find_router_for_ip() function from the last project!]

    The dictionary keys are router IPs, and the values are dictionaries
    with a bunch of information, including the routers that are directly
    connected to the key.

    This partial example shows that router `10.31.98.1` is connected to
    three other routers: `10.34.166.1`, `10.34.194.1`, and `10.34.46.1`:

    {
        "10.34.98.1": {
            "connections": {
                "10.34.166.1": {
                    "netmask": "/24",
                    "interface": "en0",
                    "ad": 70
                },
                "10.34.194.1": {
                    "netmask": "/24",
                    "interface": "en1",
                    "ad": 93
                },
                "10.34.46.1": {
                    "netmask": "/24",
                    "interface": "en2",
                    "ad": 64
                }
            },
            "netmask": "/24",
            "if_count": 3,
            "if_prefix": "en"
        },
        ...

    The "ad" (Administrative Distance) field is the edge weight for that
    connection.

    **Strong recommendation**: make functions to do subtasks within this
    function. Having it all built as a single wall of code is a recipe
    for madness.
    """

    to_visit_list = to_visit(routers)
    distance_dict = create_distance_dict(to_visit_list)
    parent_dict = create_parent_dict(to_visit_list)

    current_node = nf.find_router_for_ip(routers,src_ip)
    update_dict(distance_dict,{current_node: 0})
    
    while len(to_visit_list) != 0:
        #print(f"To visit: {to_visit_list}")
        #print(f"Current Node:{current_node}")
        neighbors = get_neighbors(routers,current_node)
        current_ad = distance_dict[current_node]
        for node in neighbors:
            neighbor_ad_total = get_ad(routers[current_node]["connections"][node]) + current_ad
            if distance_dict[node] > neighbor_ad_total:
                update_dict(distance_dict,{node: neighbor_ad_total})
                #print(f"{node} now connects to {current_node} with {neighbor_ad_total}")
                update_dict(parent_dict,{node: current_node})
        #print(neighbors)
        closet_node = min_ad(routers,current_node,to_visit_list)
        if closet_node != None:
            to_visit_list.remove(current_node)
            current_node = closet_node
        else:
            to_visit_list.remove(current_node)
            try:
                current_node = to_visit_list[0]
            except:
                break
   
     
    x,y = get_path(src_ip,dest_ip, parent_dict, routers,distance_dict)
    print(y)
    return x

#------------------------------
# DO NOT MODIFY BELOW THIS LINE
#------------------------------
def read_routers(file_name):
    with open(file_name) as fp:
        data = fp.read()

    return json.loads(data)

def find_routes(routers, src_dest_pairs):
    for src_ip, dest_ip in src_dest_pairs:
        path = dijkstras_shortest_path(routers, src_ip, dest_ip)
        print(f"{src_ip:>15s} -> {dest_ip:<15s}  {repr(path)}")
        

def usage():
    print("usage: dijkstra.py infile.json", file=sys.stderr)

def main(argv):
    try:
        router_file_name = argv[1]
    except:
        usage()
        return 1

    json_data = read_routers(router_file_name)

    routers = json_data["routers"]
    routes = json_data["src-dest"]

    find_routes(routers, routes)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
    
