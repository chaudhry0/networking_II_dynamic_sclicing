1) Use GUI also for topology creation:
```python
                switch_lst = []
                for i in range(swicth_numbers):
                    switch_lst.append("s"+str(i+1))
                first_switch1 = ttk.Combobox(screen1, textvariable=first_switch_value, width=7)
                second_switch1 = ttk.Combobox(screen1, textvariable=second_switch_value, width=7)
                bw1 = ttk.Combobox(screen1, textvariable=bw_value, width=7)


                for i in (n + 1 for n in range(host_numbers)):
                    h_list.append("h" + str(i))

                host_number1 = ttk.Combobox(links_host, textvariable=h_n_lists, width=7)
                label12=Label(links_host,text="list of hosts"+str(h_list),fg="red",bg="yellow")
                label12.pack()
                host_number1['values'] = h_list

```
3) Separete GUI from controller file.
4) Use dijkstra alghoritm to find best path using bandwidth graph (created in networkx). This graph should update each time a path is added or deleted.
* Here is a starting point (opensource dijkstra in python):

```python
# adjacency map [sw1][sw2]->port from sw1 to sw2
adjacency = defaultdict(lambda:defaultdict(lambda:None))

# getting the node with lowest distance in Q
def minimum_distance(distance, Q):
    min = float('Inf')
    node = 0
    for v in Q:
        if distance[v] < min:
            min = distance[v]
            node = v
    return node

 

def get_path (src, dst, first_port, final_port):
    # executing Dijkstra's algorithm
    print( "get_path function is called, src=", src," dst=", dst, " first_port=", first_port, " final_port=", final_port)
    
    # defining dictionaries for saving each node's distance and its previous node in the path from first node to that node
    distance = {}
    previous = {}

    # setting initial distance of every node to infinity
    for dpid in switches:
        distance[dpid] = float('Inf')
        previous[dpid] = None

    # setting distance of the source to 0
    distance[src] = 0

    # creating a set of all nodes
    Q = set(switches)

    # checking for all undiscovered nodes whether there is a path that goes through them to their adjacent nodes which will make its adjacent nodes closer to src
    while len(Q) > 0:
        # getting the closest node to src among undiscovered nodes
        u = minimum_distance(distance, Q)
        # removing the node from Q
        Q.remove(u)
        # calculate minimum distance for all adjacent nodes to u
        for p in switches:
            # if u and other switches are adjacent
            if adjacency[u][p] != None:
                # setting the weight to 1 so that we count the number of routers in the path
                w = 1
                # if the path via u to p has lower cost then make the cost equal to this new path's cost
                if distance[u] + w < distance[p]:
                    distance[p] = distance[u] + w
                    previous[p] = u

    # creating a list of switches between src and dst which are in the shortest path obtained by Dijkstra's algorithm reversely
    r = []
    p = dst
    r.append(p)
    # set q to the last node before dst 
    q = previous[p]
    while q is not None:
        if q == src:
            r.append(q)
            break
        p = q
        r.append(p)
        q = previous[p]

    # reversing r as it was from dst to src
    r.reverse()

    # setting path 
    if src == dst:
        path=[src]
    else:
        path=r

    # Now adding in_port and out_port to the path
    r = []
    in_port = first_port
    for s1, s2 in zip(path[:-1], path[1:]):
        out_port = adjacency[s1][s2]
        r.append((s1, in_port, out_port))
        in_port = adjacency[s2][s1]
    r.append((dst, in_port, final_port))
    return r
 ```
