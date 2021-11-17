import datetime
import random
import numpy as np
import configuration.events_configurations as conf


class ConnectionEvents:
    def __init__(self, relation, weight):



class Event:
    def __init__(self, min_timestamp: str, max_timestamp: str):
        try:
            self.time_stamp = Event.generate_timestamp(datetime.datetime.strptime(min_timestamp, "%d-%m-%Y %H:%M:%S"),
                                                       datetime.datetime.strptime(max_timestamp, "%d-%m-%Y %H:%M:%S"))
        except ValueError:
            raise ValueError("Please check timestamp format, should be: '%d-%m-%Y %H:%M:%S'")

    @staticmethod
    def generate_timestamp(min_timestamp, max_timestamp):
        dt = random.random() * (max_timestamp - min_timestamp) + min_timestamp
        return dt


class Call(Event):
    def __init__(self, relation: str, id_creator_call,  min_timestamp, max_timestamp):
        self.duration = Call.generate_duration(relation)
        self.id_creator_call = id_creator_call
        self.relation = relation
        super().__init__(min_timestamp, max_timestamp)

    def create_string_to_print(self):
        the_string = f'**** Call Event ***\nId creator: {self.id_creator_call}\n' \
                     f'Timestamp: {self.time_stamp}\n' \
                     f'Duration: {self.duration}'
        return the_string

    def __str__(self):
        return self.create_string_to_print()
    def generate_duration(relation: str):
        return round(max(np.random.normal(conf.CALL_DURATION[relation][0],
                                          conf.CALL_DURATION[relation][1]), 0.001),3)


if __name__ == "__main__":
    a = Call('Friend', "1", "23-01-2018 04:50:34", "23-01-2021 04:50:34")
    print(a)

