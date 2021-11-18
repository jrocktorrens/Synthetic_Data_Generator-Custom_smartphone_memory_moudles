# Events
EVENTS = ['Phone Call', 'Message']
# Possible events distribution for each connection type
DIS_EVENT = {'Friend': [[0.9, 0.1], [0.1, 0.9], [0.5, 0.5]],  # [% Phone Call, % Message]
             'Family': [[0.8, 0.2], [1, 0]],                  # [% Phone Call, % Message]
             'Other': [[0.9, 0.1]]}                           # [% Phone Call, % Message]
# Weight to choose the distribution
WEIGHTS_TO_CHOOSE_DIS = {'Friend': [.1, .85, .05],
                         'Family': [.9, .1],
                         'Other': [1]}
NUM_OF_EVENTS = 10000

# Call Duration by Relation
CALL_DURATION = {'Family': [5, 1], 'Friend': [10, 3], 'Other': [2, 0.5]}