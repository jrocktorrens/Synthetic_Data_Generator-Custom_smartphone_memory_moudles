COLOR_MAPS = {'Family': 'cyan', 'Friend': 'red', 'Other': 'green'}
POSSIBLE_TYPES = ['Family', 'Friend', 'Other']
TYPE_DIRECT_CONNECTIONS = ['Family', 'Friend', 'Other', None]
PROB_DIRECT_CONNECTIONS = [0.25, 0.25, 0.25, 0.25]

# If a combination not in CONNECTIONS_ROOT_AND_EDGES_OF_OTHER_ROOT the prob is 0
# {Connection of the current root with the other root, Connection of the other root with the edge}
CONNECTIONS_ROOT_AND_EDGES_OF_OTHER_ROOT = [{'Family'},
                                            {'Family', 'Friend'},
                                            {'Family', 'Other'},
                                            {'Friend', 'Other'},
                                            {'Friend'}]
PROB_KIND_OF_CONNECTION = [[0.15, 0.1, 0.05, 0.7],  # { 'Family', 'Family'}
                           [0.05, 0.3, 0.05, 0.6],  # {'Family', 'Friend'}
                           [0.05, 0.05, 0.1, 0.8],  # {'Family', 'Other'}
                           [0.05, 0.05, 0.1, 0.8],  # {'Friend', 'Other'}
                           [0.05, 0.2, 0.1, 0.65]]  # {'Friend', 'Friend'}

# Weights

DIS_WEIGHTS = {'Family': [8, 2],
               'Friend': [12, 2],
               'Other': [5, 0.25]}



