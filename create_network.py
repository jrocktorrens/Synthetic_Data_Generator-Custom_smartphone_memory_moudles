import networkx as nx
import numpy as np
import configuration as conf
import itertools
from scipy.special import softmax


class Node:
    def __init__(self, id):
        self.connections = {}
        self.id = str(id)

    def add_connection(self, connected_to: str, type: str):
        try:
            assert type in conf.POSSIBLE_TYPES
        except AttributeError:
            raise AttributeError(f'Unidentified type was inserted: {type}')
        else:
            if connected_to not in self.connections.keys():
                self.connections[str(connected_to)] = {'Type': type}
            else:
                self.connections[str(connected_to)]['Type'] = type

    def add_weight(self, connected_to: str, weight: int):
        if connected_to not in self.connections.keys():
            self.connections[connected_to] = {'Weight': weight}
        else:
            self.connections[connected_to]['Weight'] = weight

    def __str__(self):
        return str(self.id)


class Root:
    def __init__(self, root_id: int, color: str, distribution_connections: dict):
        self.create_root(root_id)
        self.color = color
        self.how_many_each_type = {}
        self.distribution_connections = distribution_connections
        self.create_distribution_of_edge_types()

    def create_root(self, root_id):
        self.root = Node(root_id)

    def create_distribution_of_edge_types(self):
        for t, dis in self.distribution_connections.items():
            how_many = int(np.random.normal(dis[0], dis[1]))
            if how_many < 0:
                how_many = 0
            self.how_many_each_type[t] = how_many

    def __str__(self):
        return str(self.root)


class FullGraph:
    def __init__(self):
        self.current_id = 0
        self.full_graph = nx.Graph()
        self.color_map = []
        self.roots = []
        self.all_nodes = []
        self.all_weights = []

    def create_root(self, color='Blue', distribution_connections=None):
        if distribution_connections is None:
            distribution_connections = {'Family': [5, 2], 'Friend': [5, 2], 'Other': [5, 5]}
        current_root = Root(self.current_id, color, distribution_connections)
        self.add_root_to_graph(current_root)
        self.add_to_colormap(current_root.color)
        self.add_root_to_list(current_root)
        self.all_nodes.append(current_root.root)
        self.update_id()

    def add_root_to_graph(self, root):
        self.full_graph.add_node(root)

    def add_to_colormap(self, color):
        self.color_map.append(color)

    def add_root_to_list(self, root):
        self.roots.append(root)

    def add_edges_to_each_root(self):
        for r in self.roots:
            for t, how_many in r.how_many_each_type.items():
                for i in range(how_many):
                    current_node = Node(self.current_id)
                    current_node.add_connection(connected_to=str(r.root.id), type=t)
                    r.root.add_connection(connected_to=str(current_node.id), type=t)
                    weight = FullGraph.draw_weights(t)
                    current_node.add_weight(str(r.root.id), weight)
                    r.root.add_weight(str(current_node.id), weight)

                    self.full_graph.add_edge(r, current_node, weight=weight)
                    self.all_weights.append(weight)
                    self.update_id()
                    self.add_to_colormap(conf.COLOR_MAPS[t])
                    self.all_nodes.append(current_node)
                    self.connect_roots_and_edges_of_other_roots(r, current_node)

    def connect_roots(self):
        for pair in itertools.combinations(self.roots, 2):
            con = np.random.choice(conf.TYPE_DIRECT_CONNECTIONS, p=conf.PROB_DIRECT_CONNECTIONS)
            if con:
                weight = FullGraph.draw_weights(con)
                self.full_graph.add_edge(pair[0], pair[1], weight=weight)
                self.all_weights.append(weight)
                pair[0].root.add_connection(pair[1].root.id, con)
                pair[1].root.add_connection(pair[0].root.id, con)
                pair[0].root.add_weight(pair[1].root.id, weight)
                pair[1].root.add_weight(pair[0].root.id, weight)

    def connect_roots_and_edges_of_other_roots(self, root_connection_exist, node):
        for r in self.roots:
            if r.root.id != root_connection_exist.root.id:
                if root_connection_exist.root.id in r.root.connections.keys():
                    relation = {r.root.connections[root_connection_exist.root.id]['Type'],
                            node.connections[root_connection_exist.root.id]['Type']}
                    try:
                        index_prob_list = conf.CONNECTIONS_ROOT_AND_EDGES_OF_OTHER_ROOT.index(relation)
                    except ValueError:
                        pass
                    else:
                        type_con = np.random.choice(conf.TYPE_DIRECT_CONNECTIONS,
                                         p=conf.PROB_KIND_OF_CONNECTION[index_prob_list])
                        if type_con:
                            weight = FullGraph.draw_weights(type_con)
                            self.full_graph.add_edge(r, node, weight=weight)
                            self.all_weights.append(weight)
                            node.add_connection(str(r.root.id), type_con)
                            r.root.add_connection(str(node.id), type_con)
                            r.root.add_weight(str(node.id), weight)
                            node.add_weight(str(r.root.id), weight)

    def find_node(self, id):
        for n in self.all_nodes:
            if n.id == id:
                return n
        return None

    def normlize_weights(self):
        self.all_weights = softmax(self.all_weights)

    def update_id(self):
        self.current_id += 1

    def create_string_to_print(self):
        string_to_print = []
        for r in self.roots:
            string_to_print.append(f'*** Root ID: {r.root.id} ***')
            string_to_print.append(f'Connections:')
            string_to_print.append(str(r.root.connections))
            string_to_print.append(f'**************\n')
        return string_to_print

    def __str__(self):
        return '\n'.join(self.create_string_to_print())


    @staticmethod
    def draw_weights(relation):
        weight = np.random.normal(conf.DIS_WEIGHTS[relation][0],conf.DIS_WEIGHTS[relation][1])
        if weight < 0:
            weight = 0.01
        return weight


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    g = FullGraph()
    g.create_root('blue')
    g.create_root('blue')


    g.connect_roots()
    g.add_edges_to_each_root()
    g.normlize_weights()
    plt.figure(figsize=(20, 20))
    weights = np.array(g.all_weights)
    w = weights.copy()
    w[weights <= np.percentile(weights, 10)] = 0.2
    w[(weights > np.percentile(weights, 10)) & (w <= np.percentile(weights, 30))] = 1
    w[(weights > np.percentile(weights, 30)) & (w <= np.percentile(weights, 60))] = 1.5
    w[weights > np.percentile(weights, 60)] = 2
    nx.draw_networkx(g.full_graph, node_color=g.color_map, width=w)
    print(g)


    plt.show()
