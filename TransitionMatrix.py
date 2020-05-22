import random
import collections

def get_normalized_random_values(n):
    probabilities = [random.random() for _ in range(n)]
    s = sum(probabilities)
    normalized_probabilities = [p / s for p in probabilities]
    return normalized_probabilities


class TransitionMatrix:
    def __init__(self):
        self.matrix = {}
        self.add_event("START")
        self.add_event("END")

    def add_event(self, event: str):
        if event not in self.matrix:
            new_entry = {event: 0}
            for other_event in self.matrix.keys():
                self.matrix[other_event][event] = 0
                new_entry[other_event] = 0
            self.matrix[event] = new_entry

    def set(self, eventA: str, eventB: str, value: float):
        assert eventA in self.matrix and eventB in self.matrix
        self.matrix[eventA][eventB] = value

    # The paper acutally describes a better initilization method - equation (3)
    # But this should work for now
    @staticmethod
    def init_randomized(events: [str]):
        m = TransitionMatrix()
        # Add all events to matrix - start and stop are already in
        for event in events:
            m.add_event(event)

        # add random value for event transitions
        start_probabilities = get_normalized_random_values(len(events))
        end_probabilities = get_normalized_random_values(len(events))
        for event in events:
            m.set("START", event, start_probabilities.pop())
            m.set(event, "END", end_probabilities.pop())
            probabilities = get_normalized_random_values(len(events)-1)
            for _event in events:
                if _event != event:
                    m.set(event, _event, probabilities.pop())
        
        return m

    def get_symbols(self):
        return list(self.matrix.keys())

    def get(self, eventA, eventB):
        return self.matrix[eventA][eventB]