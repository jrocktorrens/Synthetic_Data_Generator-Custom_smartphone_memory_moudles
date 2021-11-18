import networkx as nx
import numpy as np
import configuration.network_configuration as conf
import configuration.events_configurations as event_conf
import itertools
from scipy.special import softmax
from faker import Faker
import math

class Node:
    def __init__(self, id):
        self.connections = {}
        faker = Faker().profile()
        self.id = str(id)
        self.name = faker['name']
        self.sex = faker['sex']
        self.birthdate = faker['birthdate']
        self.address = faker['address']
        self.mail = faker['mail']
        self.job = faker['job']

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


class Root(Node):
    def __init__(self, root_id: int, color: str, distribution_connections: dict):
        super().__init__(root_id)

        self.color = color
        self.how_many_each_type = {}
        self.distribution_connections = distribution_connections
        self.create_distribution_of_edge_types()



    def create_distribution_of_edge_types(self):
        for t, dis in self.distribution_connections.items():
            how_many = int(np.random.normal(dis[0], dis[1]))
            if how_many < 0:
                how_many = 0
            self.how_many_each_type[t] = how_many

    def __str__(self):
        return str(self.id)


class FullGraph:
    def __init__(self):
        self.current_id = 0
        self.full_graph = nx.Graph()
        self.color_map = []
        self.roots = []
        self.all_nodes = []
        self.all_weights = []
        self.relations = []


    def create_root(self, color='Blue', random=True, distribution_connections=None):
        if distribution_connections is None:
            distribution_connections = {'Family': [5, 2], 'Friend': [-3, 2], 'Other': [5, 5]}
        current_root = Root(self.current_id, color, distribution_connections)
        self.add_root_to_graph(current_root)
        self.add_to_colormap(current_root.color)
        self.add_root_to_list(current_root)
        self.all_nodes.append(current_root)
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
                    current_node.add_connection(connected_to=str(r.id), type=t)
                    r.add_connection(connected_to=str(current_node.id), type=t)
                    self.relations.append(t)
                    weight = FullGraph.draw_weights(t)
                    current_node.add_weight(str(r.id), weight)
                    r.add_weight(str(current_node.id), weight)
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
                self.relations.append(con)
                self.all_weights.append(weight)
                pair[0].add_connection(pair[1].id, con)
                pair[1].add_connection(pair[0].id, con)
                pair[0].add_weight(pair[1].id, weight)
                pair[1].add_weight(pair[0].id, weight)

    def connect_roots_and_edges_of_other_roots(self, root_connection_exist, node):
        for r in self.roots:
            if r.id != root_connection_exist.id:
                if root_connection_exist.id in r.connections.keys():
                    relation = {r.connections[root_connection_exist.id]['Type'],
                            node.connections[root_connection_exist.id]['Type']}
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
                            self.relations.append(type_con)
                            node.add_connection(str(r.id), type_con)
                            r.add_connection(str(node.id), type_con)
                            r.add_weight(str(node.id), weight)
                            node.add_weight(str(r.id), weight)

    def find_node(self, id):
        for n in self.all_nodes:
            if n.id == id:
                return n
        return None

    def get_events(self):
        if event_conf.NUM_OF_EVENTS < len(self.all_weights):
            raise ValueError('Num of events can not be less than num of edges,'
                             ' please check the configuration')
        all_dis_events = []
        num_created_events = 0
        num_of_event = event_conf.NUM_OF_EVENTS
        all_connections = list(self.full_graph.edges)
        all_normlize_weights = self.normlize_weights()
        assert len(all_connections) == len(all_normlize_weights)
        assert len(self.relations) == len(all_connections)
        for i in range(len(all_connections)):
            relation = self.relations[i]
            how_many_event_for_this_connection = all_normlize_weights[i] * num_of_event
            if how_many_event_for_this_connection < 1:
                how_many_event_for_this_connection = math.ceil(how_many_event_for_this_connection)
            else:
                how_many_event_for_this_connection = math.floor(how_many_event_for_this_connection)
            index_dis_event = np.random.choice(range(len(event_conf.DIS_EVENT[relation])),
                                             p=event_conf.WEIGHTS_TO_CHOOSE_DIS[relation])
            dis_event = event_conf.DIS_EVENT[relation][index_dis_event]
            all_dis_events.append(dis_event)
            for j in range(how_many_event_for_this_connection):
                event = np.random.choice(event_conf.EVENTS, p=dis_event)
                num_created_events += 1
                if 'Events' not in all_connections[i][0].connections[all_connections[i][1].id].keys():
                    all_connections[i][0].connections[all_connections[i][1].id]['Events'] = [event]
                    all_connections[i][1].connections[all_connections[i][0].id]['Events'] = [event]
                else:
                    all_connections[i][0].connections[all_connections[i][1].id]['Events'].append(event)
                    all_connections[i][1].connections[all_connections[i][0].id]['Events'].append(event)
        if num_created_events < num_of_event:
            index_to_add = np.argmax(all_normlize_weights)
            dis_event = all_dis_events[index_to_add]
            how_many_iter = event_conf.NUM_OF_EVENTS - num_created_events
            for j in range(how_many_iter):
                event = np.random.choice(event_conf.EVENTS, p=dis_event)
                all_connections[index_to_add][0].connections[all_connections[index_to_add][1].id]['Events'].append(event)
                all_connections[index_to_add][1].connections[all_connections[index_to_add][0].id]['Events'].append(event)
                num_created_events += 1
        elif num_created_events > num_of_event:
            indexes = np.argsort(all_normlize_weights)[-1::-1]
            index_in_indexes = 0
            while num_created_events > num_of_event:
                events_connection = all_connections[indexes[index_in_indexes]][0].connections[all_connections[indexes[index_in_indexes]][1].id]['Events']
                if len(events_connection) > 1:
                    index_event_to_delete = np.random.choice(range(len(events_connection)))
                    del all_connections[indexes[index_in_indexes]][0].connections[all_connections[indexes[index_in_indexes]][1].id]['Events'][index_event_to_delete]
                    del all_connections[indexes[index_in_indexes]][1].connections[all_connections[indexes[index_in_indexes]][0].id]['Events'][index_event_to_delete]
                    num_created_events -= 1
                index_in_indexes += 1
                if index_in_indexes > len(indexes) - 1:
                    index_in_indexes = 0
        assert num_of_event == num_created_events

    def update_id(self):
        self.current_id += 1

    def create_string_to_print(self):
        string_to_print = []
        for r in self.roots:
            string_to_print.append(f'*** Root ID: {r.id} ***')
            string_to_print.append(f'Connections:')
            string_to_print.append(str(r.connections))
            string_to_print.append(f'**************\n')
        return string_to_print

    def __str__(self):
        return '\n'.join(self.create_string_to_print())

    def normlize_weights(self):
        return softmax(self.all_weights)


    @staticmethod
    def draw_weights(relation):
        weight = np.random.normal(conf.DIS_WEIGHTS[relation][0], conf.DIS_WEIGHTS[relation][1])
        if weight < 0:
            weight = 0.01
        return weight


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    g = FullGraph()
    g.create_root('blue', distribution_connections={'Family': [5, 2], 'Friend': [3, 2], 'Other': [10, 5]})
    g.create_root('blue', distribution_connections={'Family': [10, 2], 'Friend': [10, 2], 'Other': [3, 5]})
    g.create_root('blue', distribution_connections={'Family': [10, 2], 'Friend': [10, 2], 'Other': [3, 5]})
    g.connect_roots()
    g.add_edges_to_each_root()
    g.normlize_weights()
    g.get_events()
    print(g)
    plt.figure(figsize=(20, 20))
    weights = np.array(g.all_weights)
    w = weights.copy()
    w[weights <= np.percentile(weights, 30)] = 0.2
    w[(weights > np.percentile(weights, 30)) & (w <= np.percentile(weights, 50))] = 1
    w[(weights > np.percentile(weights, 50)) & (w <= np.percentile(weights, 80))] = 2
    w[weights > np.percentile(weights, 60)] = 3
    nx.draw_networkx(g.full_graph, node_color=g.color_map, width=w)
    plt.show()


