import random
import collections

CACHE = {}

def get_normalized_random_values(n):
    probabilities = [random.random() for _ in range(n)]
    s = sum(probabilities)
    normalized_probabilities = [p / s for p in probabilities]
    return normalized_probabilities


def _eta(symbolA, symbolB, symbol_string: [str]):

    if symbolA not in CACHE:
        CACHE[symbolA] = {}
    if symbolB not in CACHE[symbolA]:
        counter = 0
        for i in range(len(symbol_string) - 1):
            if symbol_string[i] == symbolA and symbol_string[i+1] == symbolB:
                counter += 1
            
        CACHE[symbolA][symbolB] = counter

    return CACHE[symbolA][symbolB]


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

    def init_m_plus(events: [str], symbol_string: str):
        m = TransitionMatrix()
        # Add all events to matrix - start and stop are already in
        for event in events:
            m.add_event(event)

        #symbols = ["START"] + list(symbol_string) + ["END"]
        symbols = list(symbol_string)

        for symbolA in events:
            for symbolB in events:
                if symbolA == symbolB:
                    continue
                nominator = _eta(symbolA, symbolB, symbols)
                denominator = 0
                for symbol_ in events:
                    denominator += _eta(symbolA, symbol_, symbols)
                value = nominator / denominator if denominator > 0 else 0
                m.set(symbolA, symbolB, value)

        return m

    def get_symbols(self):
        return list(self.matrix.keys())

    def get(self, eventA, eventB):
        return self.matrix[eventA][eventB]