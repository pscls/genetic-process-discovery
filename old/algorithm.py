from TransitionMatrix import TransitionMatrix
import pprint
import json

pp = pprint.PrettyPrinter(indent=4)


def _update_candidate_source(x, active_sources, y):
    l = []
    for k in range(len(y)):
        if x in y[k]:
            l.append(k)
    return [k for k in active_sources if k not in l]


def _should_source_be_activated(candidate_sources, M, x, epsilons):
    if len(candidate_sources) == 0:
        return True

    for k in candidate_sources:
        if M.get("START", x) <= M.get(epsilons[k], x):
            return False
    return True


def _should_source_be_deactivated(distinct_symbols, M, x):
    for b in distinct_symbols:
        if M.get(x, "END") <= M.get(x, b):
            return False
    return True


# m:TransitionMatrix    transition matrix
# x:[str]               symbol sequence
# http://web.ist.utl.pt/diogo.ferreira/papers/ferreira09discovering.pdf - Algorithm 1
def get_s_and_y(M: TransitionMatrix, X: [str]) -> [int]:
    # Initialize start values
    active_sources = []
    candidate_sources = []  # subset of active_sources
    K = 0   # total number of used sources
    distinct_symbols = set(X)
    y = {}
    epsilons = {}  # previous x for every k
    s = {}

    for n in range(len(X)):

        x = X[n]

        candidate_sources = _update_candidate_source(x, active_sources, y)
        if _should_source_be_activated(candidate_sources, M, x, epsilons):
            active_sources.append(K)  # activate source
            y[K] = ["START"]
            s[n] = K
            K += 1  # increment after the set operation to stay zero indexed
        else:
            argmax = candidate_sources[0]
            for k in candidate_sources:
                if M.get(epsilons[k], x) > M.get(epsilons[argmax], x):
                    argmax = k
            s[n] = argmax

        epsilons[s[n]] = x
        y[s[n]].append(x)
        if _should_source_be_deactivated(distinct_symbols, M, x):
            # deactivate source
            active_sources = [src for src in active_sources if src != s[n]]
            y[s[n]].append("END")

    # TODO: end all traces
    # in the end, all traces that are not ended yet have to be ended.
    for trace in y.values():
        if (trace[-1] != "END"):
            trace.append("END")

    # print(y.values())

    return s, y

# number of times that the transition from a to b occurs in sequence y^(k)


def _eta(symbolA, symbolB, y_k):
    counter = 0
    for i in range(len(y_k) - 1):
        if y_k[i] == symbolA and y_k[i+1] == symbolB:
            counter += 1
    return counter


def _update_position_in_m(M, s, y, symbolA, symbolB):
    numerator = 0
    for y_k in y.values():
        numerator += _eta(symbolA, symbolB, y_k)

    denominator = 0
    for y_k in y.values():
        for b_ in M.get_symbols():
            denominator += _eta(symbolA, b_, y_k)

    if denominator != 0:
        M.set(symbolA, symbolB, round(numerator / denominator, 4))
    return M


def update_m(M, s, y):
    symbols = M.get_symbols()
    for symbolA in symbols:
        for symbolB in symbols:
            if symbolA != symbolB and symbolA != "END" and symbolB != "START":
                if symbolA == "START" and symbolB == "END":
                    continue
                M = _update_position_in_m(M, s, y, symbolA, symbolB)

    return M


SymbolSequence = "ACDAEACCDDAEFFAFCCDFABAADACCCDDAFEDGABEGFCADEHBHACAGHACDEDECDAFAFAFCACDCDEAFCDFCGHDDFFACDAEACCDDAEFFAFCCDFABAADACCCDDAFEDGABEGFCADEHBHACAGHACDEDECDAFAFAFCACDCDEAFCDFCGHDDFFACDAEACCDDAEFFAFCCDFABAADACCCDDAFEDGABEGFCADEHBHACAGHACDEDECDAFAFAFCACDCDEAFCDFCGHDDFFACDAEACCDDAEFFAFCCDFABAADACCCDDAFEDGABEGFCADEHBHACAGHACDEDECDAFAFAFCACDCDEAFCDFCGHDDFFACDAEACCDDAEFFAFCCDFABAADACCCDDAFEDGABEGFCADEHBHACAGHACDEDECDAFAFAFCACDCDEAFCDFCGHDDFFACDAEACCDDAEFFAFCCDFABAADACCCDDAFEDGABEGFCADEHBHACAGHACDEDECDAFAFAFCACDCDEAFCDFCGHDDFFACDAEACCDDAEFFAFCCDFABAADACCCDDAFEDGABEGFCADEHBHACAGHACDEDECDAFAFAFCACDCDEAFCDFCGHDDFFACDAEACCDDAEFFAFCCDFABAADACCCDDAFEDGABEGFCADEHBHACAGHACDEDECDAFAFAFCACDCDEAFCDFCGHDDFFACDAEACCDDAEFFAFCCDFABAADACCCDDAFEDGABEGFCADEHBHACAGHACDEDECDAFAFAFCACDCDEAFCDFCGHDDFFACDAEACCDDAEFFAFCCDFABAADACCCDDAFEDGABEGFCADEHBHACAGHACDEDECDAFAFAFCACDCDEAFCDFCGHDDFFACDAEACCDDAEFFAFCCDFABAADACCCDDAFEDGABEGFCADEHBHACAGHACDEDECDAFAFAFCACDCDEAFCDFCGHDDFFACDAEACCDDAEFFAFCCDFABAADACCCDDAFEDGABEGFCADEHBHACAGHACDEDECDAFAFAFCACDCDEAFCDFCGHDDFFACDAEACCDDAEFFAFCCDFABAADACCCDDAFEDGABEGFCADEHBHACAGHACDEDECDAFAFAFCACDCDEAFCDFCGHDDFF"
print(len(SymbolSequence))
TM = TransitionMatrix.init_m_plus(
    ["A", "B", "C", "D", "E", "F", "G", "H"], SymbolSequence)
LAST_MATRIX = None

# for i in range(100):
#     s, y = get_s_and_y(TM, SymbolSequence)
#     update_m(TM, s, y)
#     if LAST_MATRIX == TM.matrix:
#         break
#     LAST_TM = json.loads(json.dumps(TM.matrix))

pp.pprint(TM.matrix)
