import sys
sys.path.append("../")
# Events
EVENTS = ['Chat', 'Call']

# Possible events distribution for each connection type
DIS_EVENT = {'Friend': [[0.9, 0.1], [0.1, 0.9], [0.5, 0.5]],  # [% Phone Call, % chat]
             'Family': [[0.8, 0.2], [1, 0]],  # [% Phone Call, % chat]
             'Other': [[0.9, 0.1]]}  # [% Phone Call, % chat]
# Weight to choose the distribution
WEIGHTS_TO_CHOOSE_DIS = {'Friend': [.1, .85, .05],
                         'Family': [.9, .1],
                         'Other': [1]}
NUM_OF_EVENTS = 10000


