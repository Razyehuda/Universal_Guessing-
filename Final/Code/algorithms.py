from utils import *
from tree import *
from compression import *
import random
from typing import Dict, List, Tuple




def decode_series_random(y):
    alpha_value = 2
    decoded = []
    previous_I = dict()
    phrase = ''
    past_phrases = dict()
    max_L = 1
    min_L = 1
    previous_L = dict()
    end = 0
    I_bits = ''

    while True:

        #generate random I series        
        if not I_bits:
            I_bits = generate_iid_sequence(len(y))

        #get current y phrase
        beg = end
        #generate random L
        L = random.randint(min_L, max_L)
        #find current y phrase with length of L
        end = beg + L
        #if we have reached to the end of y
        phrase = y[beg:end]

        #if we have reached the end of y, we break
        if end >= len(y):
            decoded.append(phrase)
            break

        #generate a new L if needed
        while L > 1 and\
            ((phrase[:-1] not in past_phrases) or\
            (phrase in past_phrases and len(past_phrases.get(phrase)) >= 2*len(past_phrases.get(phrase[:-1])))) or\
            phrase in past_phrases and len(past_phrases.get(phrase)) >= 2**L: 
            
            L = random.randint(min_L, max_L)
            end = beg + L
            phrase = y[beg:end]

        #find j for current phrase
        if phrase[:-1] in past_phrases:
            j = len(past_phrases.get(phrase[:-1])) + 1
            
        else:
            j = 1
        
        #find I, Ia and pi using random string I_bits and cut I_bits
        (I,I_bits) = find_current_I(j, I_bits, previous_I.get(phrase))

        while I is None or ((I == 1 or I == 0) and L > 1):
            #if func "find_current_I" returns I as None, it means I was in previous_I and we'll have to generate a new I
            # or I_bits was too short
            if I_bits is None:
                I_bits = generate_iid_sequence(len(y))
            (I,I_bits) = find_current_I(j, I_bits, previous_I.get(phrase)) 
            if not I_bits:  
                #if func "find_current_I" I_bits as None, it means it was too short and we need to generate more bits
                I_bits = generate_iid_sequence(len(y))
        Ia = I % alpha_value
        pi = int((I - Ia)/alpha_value)
        #find decoded x phrase


        if pi != 0:
            previous_phrases_y = past_phrases.get(phrase[:-1])
            decoded.append(str(previous_phrases_y[pi-1]) + str(Ia))
        else:
            decoded.append(str(Ia))

        #add decoded to past_phrases
        if phrase not in past_phrases:
            past_phrases[phrase] = []
        past_phrases[phrase].append(decoded[-1])

        #add I to past_I
        if phrase not in previous_I:
            previous_I[phrase] = []
        previous_I[phrase].append(I)
        
        if L in previous_L: # L = len(phrase)
            previous_L[L] += 1
        else:
            previous_L[L] = 1

        #update L range
        if previous_L.get(L) >= 4 ** L:
            min_L += 1

        if L == max_L:
            max_L = L + 1
    
    return list_to_str(decoded)

def guessing(ref_x,y):

    
    l = len(ref_x)   
    previous_I = dict()
    past_phrases = dict()
    previous_L = dict()
    decoded = []

    ref_I, ref_L, _ = encode_series(ref_x,y[0:l]) # DOTO: deal with case of last phrase too short
    parsed_y = parse_series_L(y[0:l],ref_L)
    parsed_ref_x = parse_series_L(ref_x,ref_L)
    #print('ref_I=', ref_I, ref_L,'parsed y = ', parsed_y)
    if len(list_to_str(parsed_y)) < l: #if last phrase too short to be parsed, add it to the random guessing
        l = len(list_to_str(parsed_y))

    for i in range(len(parsed_y)):
        I = ref_I[i]
        L = ref_L[i]
        y_phrase = parsed_y[i]
        x_phrase = parsed_ref_x[i]
        decoded.append(x_phrase)

        if y_phrase not in previous_I:
            previous_I[y_phrase] = []
        previous_I[y_phrase].append(I)

        if L not in previous_L:
            previous_L[L] = 0
        previous_L[L] += 1 

        if y_phrase not in past_phrases:
            past_phrases[y_phrase] = []
        past_phrases[y_phrase].append(x_phrase)


    alpha_value = 2
    max_L = max(ref_L)
    min_L = 1
    I_bits = ''
    end = l
    done = False

    for L in range(1,len(previous_L) + 1):
        if previous_L.get(L) >= 4 ** L:
            min_L += 1

    while True:

        #generate random I series        
        if not I_bits:
            I_bits = generate_iid_sequence(len(y))

        #get current y phrase
        beg = end
        #generate random L
        L = random.randint(min_L, max_L)
        #find current y phrase with length of L
        end = beg + L

        phrase = y[beg:end]

        #if we have reached the end of y, we break
        if end >= len(y):
            decoded.append(phrase)
            break

        #generate a new L if needed
        count = 0
        used_L = []
        while L > 1 and\
            ((phrase[:-1] not in past_phrases) or\
            (phrase in past_phrases and len(past_phrases.get(phrase)) >= 2*len(past_phrases.get(phrase[:-1])))) or\
            phrase in past_phrases and len(past_phrases.get(phrase)) >= 2**L: 
            
            used_L.append(L)
            aval_L = list(set(range(min_L,max_L + 1)) - set(used_L))

            #L = random.randint(min_L, max_L)
            L = random.choice(aval_L)
            end = beg + L
            phrase = y[beg:end]

            if end >= len(y):
                decoded.append(phrase)
                done = True
                break

            count +=1
            if count == 1000:
                print ("stuck")

        if done:
            break

        #find j for current phrase
        if phrase in past_phrases and False:
            index = random.randint(0, len(past_phrases[phrase])-1)
            decoded.append(str(past_phrases[phrase][index]))
            print(" ", len(str(past_phrases[phrase][index]))," ", str(past_phrases[phrase][index]))#

        else:
            if phrase[:-1] in past_phrases:
                j = len(past_phrases.get(phrase[:-1])) + 1
                (I,I_bits) = find_current_I2(j, I_bits, previous_I.get(phrase)) #change
            else:
                j = 1
            #find I, Ia and pi using random string I_bits and cut I_bits
            (I,I_bits) = find_current_I2(j, I_bits, previous_I.get(phrase)) #change

            while I is None or ((I == 1 or I == 0) and L > 1):
            #while I is None:
                #if func "find_current_I" returns I as None, it means I was in previous_I and we'll have to generate a new I
                # or I_bits was too short
                if I_bits is None:
                    I_bits = generate_iid_sequence(len(y))
                (I,I_bits) = find_current_I2(j, I_bits, previous_I.get(phrase)) #change
                if not I_bits:  
                    #if func "find_current_I" I_bits as None, it means it was too short and we need to generate more bits
                    I_bits = generate_iid_sequence(len(y))

            Ia = I % alpha_value
            pi = int((I - Ia)/alpha_value)
            #find decoded x phrase
            if pi != 0:
                previous_phrases_y = past_phrases.get(phrase[:-1])
                #print(str(previous_phrases_y[pi-1]) + str(Ia)) #
                decoded.append(str(previous_phrases_y[pi-1]) + str(Ia))
            else:
                decoded.append(str(Ia))

        #add decoded to past_phrases
        if phrase not in past_phrases:
            past_phrases[phrase] = []
        past_phrases[phrase].append(decoded[-1])

        #add I to past_I
        if phrase not in previous_I:
            previous_I[phrase] = []
        previous_I[phrase].append(I)
        
        if L not in previous_L: # L = len(phrase)
            previous_L[L] = 0
        else:
            previous_L[L] += 1

        #update L range
        if previous_L.get(L) >= 4 ** L:
            min_L += 1

        if L == max_L:
            max_L = L + 1
    
    return list_to_str(decoded)

def new_guessing(ref_x,y):
    
    l = len(ref_x)   
    previous_I = dict()
    past_phrases = dict()
    previous_L = dict()
    decoded = []

    ref_I, ref_L, _ = encode_series(ref_x,y[0:l]) 
    parsed_y = parse_series_L(y[0:l],ref_L)
    parsed_ref_x = parse_series_L(ref_x,ref_L)

    if len(list_to_str(parsed_y)) < l: # if last phrase too short to be parsed, add it to the random guessing
        l = len(list_to_str(parsed_y))

    for i in range(len(parsed_y)):
        I = ref_I[i]
        L = ref_L[i]
        y_phrase = parsed_y[i]
        x_phrase = parsed_ref_x[i]
        decoded.append(x_phrase)

        if y_phrase not in previous_I:
            previous_I[y_phrase] = []
        previous_I[y_phrase].append(I)

        if L not in previous_L:
            previous_L[L] = 0
        previous_L[L] += 1 

        if y_phrase not in past_phrases:
            past_phrases[y_phrase] = []
        past_phrases[y_phrase].append(x_phrase)

    #print(decoded)
    alpha_value = 2
    max_L = max(ref_L)
    min_L = 1
    I_bits = ''
    end = l
    done = False
    count = 0
    j = 1
    for L in range(1,len(previous_L) + 1):
        if previous_L.get(L) >= 4 ** L:
            min_L += 1

    while True:



        beg = end

        L = max_L
        
        while True:
            #find current y phrase with length of L
            end = beg + L
            phrase = y[beg:end]
            #if we have reached the end of y, we break
            if end >= len(y):
                decoded.append(phrase)
                done = True
                break
            if phrase[:-1] in past_phrases or L == 1:
                break
            L -= 1

        if done:
            break
            
        #find j for current phrase
        if phrase[:-1] in past_phrases:
            j = len(past_phrases.get(phrase[:-1])) + 1
        else:
            j = 1
        #generate random I series        
        if not I_bits:
            I_bits = generate_iid_sequence(j)
        #find I, Ia and pi using random string I_bits and cut I_bits
        (I,I_bits) = find_current_I2(j, I_bits, previous_I.get(phrase))
        counter = 0
        
        while I is None or ((I == 1 or I == 0) and L > 1):
            #if func "find_current_I" returns I as None, it means I was in previous_I and we'll have to generate a new I
            # or I_bits was too short
            if I_bits is None:
                I_bits = generate_iid_sequence(j)
            (I,I_bits) = find_current_I2(j, I_bits, previous_I.get(phrase)) 
            if not I_bits:  
                #if func "find_current_I" I_bits as None, it means it was too short and we need to generate more bits
                I_bits = generate_iid_sequence(j)


            counter+=1
            if counter > 70000:
                raise BrokenPipeError
                #print("hi")
        Ia = I % alpha_value
        pi = int((I - Ia)/alpha_value)
        
        #find decoded x phrase
        if pi != 0:
            previous_phrases_y = past_phrases.get(phrase[:-1])
            decoded.append(str(previous_phrases_y[pi-1]) + str(Ia))
        else:
            decoded.append(str(Ia))

    return list_to_str(decoded)

