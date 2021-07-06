"""dijkstra.py: This module demonstrates an exemplative code of the dijkstra algorithm.
    Neither python dictionaries or sets are used in this module.
    Complexities mentioned in this file is of Worst Time unless otherwise specified."""

__author__ = "Shuta Gunraku"
__reference__ = """
                MinHeap class implementation for Dijkstra Algorithm
                title = MinHeap, MaxHeap classes
                author = Issac Turner
                publisher = stack overflow
                availability = https://stackoverflow.com/questions/2501457/what-do-i-use-for-a-max-heap-implementation-in-python
                """
import heapq

# MinHeap Class to be used as the data structure for Dijkstra algorithm.
class MinHeap(object):
    """
    push() and pop() both take O(log N) time complexity where N is the size of the Heap.
    """
    def __init__(self): self.heap = []
    def __getitem__(self, index): return self.heap[index]
    def __len__(self): return len(self.heap)
    def push(self, val, src): heapq.heappush(self.heap, [val, src])
    def pop(self): return heapq.heappop(self.heap)


class Vertex:
    def __init__(self, index):
        """
        :time complexity: O(1)
        :space complexity: O(1)
        """
        self.index = index
        self.edges = []
        self.distance = float("Inf")
        self.discovered = False
        self.visited = False
        self.previous = None

    def __str__(self):
        print_vertex = str(self.index)
        return print_vertex

    # The following 2 methods are to define the comparison of vertices, since in case the distances of 2 elements
    # in the heap are the same, the heap needs to compare the second elements which are vertices.
    def __lt__(self, other): return self.index < other.index
    def __le__(self, other): return self.index <= other.index

    def add_edges(self, u, v, w):
        new_edge = Edge(u, v, w)
        self.edges.append(new_edge)

    def add_to_queue(self): self.discovered = True
    def visit_node(self): self.visited = True


class Edge:
    def __init__(self, u, v, w):
        """
        :time complexity: O(1)
        :space complexity: O(1)
        """
        self.u = u
        self.v = v
        self.w = w


# DijkstraGraph Class based on an adjacency-list.
class DijkstraGraph:
    def __init__(self, v):
        """
        :time complexity: O(v) to add all the vertices.
        :space complexity: O(v) to store all the vertices.
        """
        self.vertices = [None] * v
        for i in range(v):
            self.vertices[i] = Vertex(i)

    def __str__(self):
        print_vertices = ""
        for vertex in self.vertices:
            print_vertices = print_vertices + "Vertex " + str(vertex) + "\n"
        return print_vertices

    def add_edges(self, u, v, w): self.vertices[u].add_edges(self.vertices[u], self.vertices[v], w)

    def dijkstra(self, src, dest):
        """
        Given 2 vertices, this method finds the shortest path.
        :param src: Source vertex from where the Dijkstra algorithm finds the shortest path.
        :param dest: Destination vertex to where the Dijkstra algorithm finds the shortest path.
        :return u: This algorithm returns the vertex representing the destination.
        :time complexity: Overall O(R log(N))
            where R is the total number of edges and N is the total number of vertices.
        :space complexity: Overall O(R)
            inputs take O(1) space respectively.
            discovered[] keeps track of all the paths thus it takes O(R).
        """
        src.distance = 0
        # discovered[] is a Heap
        discovered = MinHeap()
        discovered.push(src.distance, src)
        # This while loop takes O(V) time by itself.
        # since each iteration takes O(log V) + O(V log V),
        # overall complexity is O(V) * (O(log V) + O(V log V)) = O(V^2 * log V) <= O(E * log V)
        while len(discovered) > 0:
            # pop the smallest from the Heap
            # and visit u
            # pop() takes O(logV) time
            min_vertex = discovered.pop()
            u = min_vertex[1]
            u.visited = True  # the distance is finalised.
            # this code returns when the destination has been reached.
            if u == dest:
                return u
            # Perform edge relaxation on all adjacent vertices.

            # This for loop costs O(V log V) overall,
            # as this runs for all the vertices so it will cost O(V) time by itself.
            # each iteration costs O (log V) as of push(),
            # Thus overall O(V) * O(log V) = O(V log V)
            for edge in u.edges:
                v = edge.v
                if not v.discovered:
                    # v is discovered
                    v.discovered = True
                    v.distance = u.distance + edge.w
                    v.previous = u
                    discovered.push(v.distance, v)
                # In heap, but the distance isn't finalised.
                elif not v.visited:
                    if v.distance > u.distance + edge.w:
                        # update distance
                        v.distance = u.distance + edge.w
                        v.previous = u
                        # No need to remove the same v with larger distance previously pushed to the Heap,
                        # as the one with the shorter distance will always popped first.
                        discovered.push(v.distance, v)


def opt_delivery(n, roads, start, end, delivery):
    """
    This function determines whether it wil be cheaper to perform this delivery during the journey,
    or just go directly to the destination, to get the destination as cheaply as possible.
    To achieve that, this function will create a dijkstra_graph with vertices and edges,
    and call its dijkstra() method.
    :param n: The number of cities. The cities are numbered [0..n-1].
    :param roads: A list of tuples. Each tuple is of the form (u, v, w). Each tuple represents an road
        between cities u and v. w is the cost of traveling along that road, which is always non-negative.
        Roads can be traveled in either direction, and the cost is the same.
        There is at most 1 road between any pair of cities. roads will represent a simple, connected graph.
    :param start: An integer in the range [0..n-1]. It represents the start city.
    :param end: An integer in the range [0..n-1]. it represents the end city.
    :param delivery: A tuple containing 3 values.
        The first value is the city where we can pick up the item. (pickup city).
        The second value is the city where we can deliver the item. (delivery city).
        The third value is the amount of money we can make if we deliver the item from the pickup city
        to the delivery city.
    :return: This function returns a tuple containing 2 elements.
        The first element is the cost of travelling from the start city to the end city.
        This cost includes the profit we make from the delivery, if we choose the make the delivery. (possibly negative)
        The second element of the tuple is a list of integers. This list represents the cities we need to travel to
        in order to achieve the cheapest cost (in order). It should start with the start city,
        and end with the end city. Possibly need to visit a city twice.
    :time complexity: O(R log(N)) where R is the total number of roads and N is the total number of cities.
        1.Creating a graph with the size of vertices takes O(N).
        2.Adding edges(roads) to the graph takes 2*O(R) as it's an undirected graph.
        3.Running dijkstra() once takes O(R log(N)).
        4.Backtracking the path will take O(N) at maximum.
        As 1~4 will be running 4 times at maximum,
        thus its overall time complexity is 4 * (O(N) + 2*O(R) + O(R log(N)) + O(N)) == O(R log (N)).
    :space complexity: O()
        1.Creating a graph with the size of vertices takes O(N).
        2.Storing edges(roads) to the graph takes 2*O(R) as it's an undifrected graph.
        3.Running dijkstra() once takes O(R).
        4.Backtracking and storing the result takes O(N) at maximum.
        As 1~4 will be running 4 tiems at maximum,
        thus its overall time complexity is 4 * (O(N) 2*O(R) + O(R) + O(N)) == O(N) + O(R) < O(R log (N)).
    """
    # Step1: Find the shortest path without delivery
    # Create a graph
    dijkstra_graph = DijkstraGraph(n)
    # Add edges
    # Since this is an undirected graph, edges with both directions will be added.
    for road in roads:
        dijkstra_graph.add_edges(road[0], road[1], road[2])
        dijkstra_graph.add_edges(road[1], road[0], road[2])
    # Use Dijkstra algorithm to determine the shortest path without delivery
    res_without_delivery = dijkstra_graph.dijkstra(dijkstra_graph.vertices[start], dijkstra_graph.vertices[end])
    cost_without_delivery = res_without_delivery.distance
    res_order = []
    # Backtrack and get the order of travelling
    while res_without_delivery is not None and res_without_delivery != dijkstra_graph.vertices[start]:
        res_order.append(res_without_delivery.index)
        res_without_delivery = res_without_delivery.previous
    res_order.append(res_without_delivery.index)
    res_order = res_order[::-1]

    # Step2: Find the shortest path with delivery
    # by implementing Dijkstra algorithm 3 times;
    # 1st: from start to the start of the delivery,
    # 2nd: from the start of the delivery to the end of the delivery,
    # 3rd: from the end of the delivery to the end.
    # Those 3 combined will represent the shortest path with delivery.
    delivery_total_cost = 0
    # Create a graph for pre delivery
    dijkstra_graph_before = DijkstraGraph(n)
    # Add edges
    for road in roads:
        dijkstra_graph_before.add_edges(road[0], road[1], road[2])
        dijkstra_graph_before.add_edges(road[1], road[0], road[2])
    res_before_delivery = dijkstra_graph_before.dijkstra(dijkstra_graph_before.vertices[start], dijkstra_graph_before.vertices[delivery[0]])

    # Create a graph for delivery
    dijkstra_graph_during = DijkstraGraph(n)
    # Add edges
    for road in roads:
        dijkstra_graph_during.add_edges(road[0], road[1], road[2])
        dijkstra_graph_during.add_edges(road[1], road[0], road[2])
    res_during_delivery = dijkstra_graph_during.dijkstra(dijkstra_graph_during.vertices[delivery[0]], dijkstra_graph_during.vertices[delivery[1]])

    # Create a graph for post delivery
    dijkstra_graph_after = DijkstraGraph(n)
    # Add edges
    for road in roads:
        dijkstra_graph_after.add_edges(road[0], road[1], road[2])
        dijkstra_graph_after.add_edges(road[1], road[0], road[2])
    # Sum up the distances to get the total cost
    res_after_delivery = dijkstra_graph_after.dijkstra(dijkstra_graph_after.vertices[delivery[1]], dijkstra_graph_after.vertices[end])
    delivery_total_cost += res_before_delivery.distance
    delivery_total_cost += res_during_delivery.distance
    delivery_total_cost += res_after_delivery.distance
    cost_with_delivery = delivery_total_cost - delivery[2]

    # Backtrack and get the order of travelling if the cost is smaller with delivery
    if cost_with_delivery < cost_without_delivery:
        res_order = []
        cost = cost_with_delivery
        # Backtrack and get the order of travelling
        while res_after_delivery is not None and res_after_delivery != dijkstra_graph_after.vertices[delivery[1]]:
            res_order.append(res_after_delivery.index)
            res_after_delivery = res_after_delivery.previous
        while res_during_delivery is not None and res_during_delivery != dijkstra_graph_during.vertices[delivery[0]]:
            res_order.append(res_during_delivery.index)
            res_during_delivery = res_during_delivery.previous
        while res_before_delivery is not None and res_before_delivery != dijkstra_graph_before.vertices[start]:
            res_order.append(res_before_delivery.index)
            res_before_delivery = res_before_delivery.previous
        res_order.append(res_before_delivery.index)
        res_order = res_order[::-1]
    else:
        cost = cost_without_delivery
    return cost, res_order