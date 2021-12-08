import argparse
import create_network
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--how_many_device_owner', nargs=1, type=int, required=True)
    parser.add_argument('-c', '--connection_distribution', nargs=1, type=list, required=False)
    args = parser.parse_args()

    g = create_network.FullGraph()
    for i in range(args.how_many_device_owner[0]):
        g.create_root()
    g.connect_roots()
    g.add_edges_to_each_root()
    g.normlize_weights()
    g.get_events()
    plt.figure(figsize=(20, 20))
    weights = np.array(g.all_weights)
    w = weights.copy()
    w[weights <= np.percentile(weights, 10)] = 0.2
    w[(weights > np.percentile(weights, 10)) & (w <= np.percentile(weights, 20))] = 0.4
    w[(weights > np.percentile(weights, 20)) & (w <= np.percentile(weights, 50))] = 0.8
    w[(weights > np.percentile(weights, 50)) & (w <= np.percentile(weights, 80))] = 1
    w[weights > np.percentile(weights, 60)] = 3.5
    nx.draw_networkx(g.full_graph, node_color=g.color_map, width=w)
    plt.show()
if __name__ == "__main__":
    main()