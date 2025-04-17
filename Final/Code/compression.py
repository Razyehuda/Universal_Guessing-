
from collections import defaultdict
from tree import *
from utils import *

def parse_series(x, y):
    past = defaultdict(lambda: 0)
    i = 0
    l = 0
    parsed_phrases = []
    while i + l < len(x):
        phrase = x[i:i + l + 1], y[i:i + l + 1]
        if not past[phrase]:
            past[phrase] = True
            parsed_phrases.append(phrase)
            i += 1 + l
            l = 0
        else:
            if i + l >= len(x) - 1:
                break
            else:
                l += 1

    return parsed_phrases #possibly add weights to be able to give recuring patterns more weight

def encode_series(x, y):

    parsed_phrases = parse_series(x,y)
    pi_yx = dict()  # Updated to a nested defaultdict
    I_series,L_series = [], []

    for idx, (xi, yi) in enumerate(parsed_phrases):

        L = len(xi)

        if yi in pi_yx:
            pi_yx[yi] += [xi]
        else:
            pi_yx[yi] = [xi]

        if L > 1:
            pi = pi_yx[yi[:-1]].index(xi[:-1]) + 1
        else:
            pi = 0

        alpha = 2  
        Ia = int(xi[-1])  

        I = pi * alpha + Ia  # Use the index for the current (x, y) pair

        I_series.append(I)
        L_series.append(L)

    ClogC = sum([len(i)*(math.log2(len(i)) + 2) for i in pi_yx.values()])
    return I_series, L_series, ClogC

def parse_series_L(y,L_series):
    parsed_y = []
    end = 0
    for l in L_series:
        beg = end
        end = beg + l
        parsed_y.append(y[beg:end])

    return parsed_y

def decode_series(I_series,L_series,y):
    parsed_y = parse_series_L(y,L_series)
    alpha_value = 2
    decoded = []
    previous_I = []
    past_phrases = dict()
    i = -1
    for phrase in parsed_y:
        i += 1
        I = I_series[i]
        Ia = I % alpha_value
        pi = int((I - Ia)/alpha_value)   

        previous_I.append(I)
        if I == None:
            decoded.append(I_series)
            break

        if phrase not in past_phrases:
            past_phrases[phrase] = []
        if pi != 0:
            previous_phrases_y = past_phrases.get(phrase[:-1])
            decoded.append(str(previous_phrases_y[pi-1]) + str(Ia))
        else:
            decoded.append(str(Ia))

        past_phrases[phrase].append(decoded[-1])
    
    return list_to_str(decoded)
    


