"""
 - Function to estimate ability (estimate_theta())
    * Rash model using formula rom: Baker, F. B., & Kim, S.-H. (2017). The Basics of Item Response Theory Using R.
     Springer International Publishing. https://doi.org/10.1007/978-3-319-54205-8

"""

import random

def main():
# Item database and initial lists and variables

    item_db = read_item_db('rn_db.csv') # item databas (dictionnaire)
    global item_db_new

    s = 0                               # scored response
    r = []                            # list of scored responses
    r = [1,1,1,1]
    i = [item_db["coditem"][0]]         # code of item administered
    bs =[item_db["b"][0]]               # item difficulties
    bs = [2,2.5,3,3.1,item_db["b"][0]]
    
    sem_theta = .70
    max_items = 18
    resp = ""

# Instructions and first pass. Administer item RN01 as training
    print('Hello! I am RN_CAT a Computerized Adaptive Test of Numerical Reasoning!')
    print("I am a simple program created by padawan Ricardo who is learning the ways of the force with Python")
    print()
    name =  input("What is your name ? ")
    print("Hi " + name + ". Lets solve problems of numerical reasoning  ?")
    print()
    print("I will present number sequences and ask you to finish with the last numbers that logically follows the sequence")
    print("For instance: ")
    print()
    print(item_db["item"][0])
    print()
    resp = input("What is the two last numbers? (type one number, space and the next number): ")
    print()


# Fist pass
    s = score(resp, item_db["key"][0])
    r.append(s)

    if s == 1:
        print("Correct! Lets start the test")
    else:
        print("This sequence is aways increasing +3 so the correct answer is " + item_db["key"][0])
        print("Lets start the test")
        

# remove item 1 from the dictionnaire (these are removed in place)
    item_db['coditem'].remove(item_db['coditem'][0]),
    item_db['b'].remove(item_db['b'][0]),
    item_db['item'].remove( item_db['item'][0]),
    item_db['key'].remove(item_db['key'][0])
    
    item_db_new = [item for item in item_db_new if item.get('coditem') != item_db['coditem'][0]]

# calculate theta and next item from first pass
    theta = estimate_theta(r, bs, [-3])
    print('First probablity :',theta)
    next_i = next_item(theta[0], item_db)
    selected_items = select_items(item_db_new,theta[0])
    print('Selected questions are::',selected_items)

# Actual CAT (runs until sem is lower than sem_theta or when item reach max items
    while theta[1] >= sem_theta and len(r) <= max_items:
        
        
        selected_questionscode = [item['coditem'] for item in selected_items]
        selected_questions = [item['item'] for item in selected_items]
        selected_questionskey = [item['key'] for item in selected_items]
        selected_questionslevel = [item['b'] for item in selected_items]
        print()
        #print('Question Code is ::',next_i["coditem"])
        print('Question Code is ::',selected_questionscode)
        #resp = input(next_i["item"])
        resp = input(selected_questions)
        print()

        #s = score(resp, next_i["key"])
        s = score_new(resp, selected_questionskey)
        
        count_of_correct = s.count(1)
        total_answer = len(s)
        
        yn = input("Out of " +str(total_answer) +" answers " +str(count_of_correct) +" are Correct! Type 'y' for the next item or 'n' to quit ")

        # if s == 1:
        #     yn = input("Correct! Type 'y' for the next item or 'n' to quit ")
        # else:
        #     yn = input("Incorrect! The correct answer is " + next_i["key"] + " Type 'y' for the next item or 'n' to quit ")
        if yn == "n": break


        for n in range(0,len(s)):
            r.append(s[n])
            #bs.append(next_i["b"])
            bs.append(float(selected_questionslevel[n]))
            i.append(selected_questionscode[n])

        theta = estimate_theta(r, bs, theta)
        print('Theta iS::',theta)
        selected_items = select_items(item_db_new,theta[0])
        #next_i = next_item(theta[0], item_db)

    print()
    print("Congratulations! You finished the CAT RN test")
    print("You answered " + str(len(r)) + " items")
    print("You got " + str(sum(r)) + " correct")
    print("Your IRT theta scores was " + str(round(theta[0], 2)) + ", sem = " + str(round(theta[1], 2)))
    print("Your standardized score (M=100, DP=15 like in IQ tests) was " + str(round( ((theta[0] - 1.40)/1.50)*15) + 100  ))




def score(resp, key):

    resp = resp.split()
    key = key.split()

    if (resp[0] == key[0]) & (resp[1] == key[1]):
        s = 1
    else:
        s = 0
    return(s)

def score_new(resp, key):
    
    s = []

    resp = resp.split(',')
    #key = key.split(',')
    
    for index,item in enumerate(key):
        key_int = item.split()
        resp_int = resp[index].split()
        if (resp_int[0] == key_int[0]) & (resp_int[1] == key_int[1]):
            s.append(1)
        else:
            s.append(0)
        
    return(s)

def next_item(theta, item_db):
    # Find index of item closest to theta
    # Pop this item from item_db
    # Returns a dictionnaire with the current item for administration

    i_nxt_itm = index_of_closest(item_db['b'], theta)

    next_item_db = {
        'coditem' : item_db['coditem'].pop(i_nxt_itm ),
        'b': item_db['b'].pop(i_nxt_itm ),
        'item' : item_db['item'].pop(i_nxt_itm ),
        'key' : item_db['key'].pop(i_nxt_itm )
    }

    return next_item_db


def select_items(item_db, probability_value):
    global item_db_new
    # Sort items based on Difficulty Index
    #sorted_items = sorted(items, key=lambda x: x['b'][0])
    sorted_items = item_db_new

    # Calculate the number of items to select for each category
    total_items = len(sorted_items)
    total_items = 6
    below_threshold = int(0.25 * total_items)
    above_threshold = int(0.25 * total_items)
    near_threshold = total_items - below_threshold - above_threshold

    # Determine the threshold levels
    threshold_below = probability_value - 1
    threshold_above = probability_value + 1
    
    random_sample_med = []
    random_sample_hard = []
    selected_items = []
    
    filtered_simplelevel = [item for item in sorted_items if float(item['b']) < threshold_below]
    selected_items.append(random.sample(filtered_simplelevel, below_threshold))
    
    filtered_medlevel = [item for item in sorted_items if float(item['b']) > threshold_above]
    if len(filtered_medlevel) > above_threshold:
        selected_items.append(random.sample(filtered_medlevel, above_threshold))
    else:
        selected_items.append(filtered_medlevel)
        
    filtered_hardlevel = [item for item in sorted_items if threshold_below < float(item['b']) < threshold_above]
    if len(filtered_hardlevel) > near_threshold:
        selected_items.append(random.sample(filtered_hardlevel, near_threshold))
    else:
        selected_items.append(filtered_hardlevel)
    
    #selected_items = (random_sample_simple,random_sample_med,random_sample_hard)
    
    selected_items = [item for sublist in selected_items for item in sublist]
    remaining_items = [item for item in item_db_new if item not in selected_items]
    item_db_new = remaining_items
    #filtered_difflevel = [value for index, value in enumerate(sorted_items['b']) if value < threshold_below]
    #selected_question_id = [sorted_items['coditem'][index] for index in filtered_difflevel]
    #selected_random_question_id = random.sample(selected_question_id,below_threshold)

    # Select items based on the specified distribution
    # selected_items = (
    #     random.sample([item for item in sorted_items if item['b'] < threshold_below], below_threshold) +
    #     random.sample([item for item in sorted_items if threshold_below <= item['b'] <= threshold_above], near_threshold) +
    #     random.sample([item for item in sorted_items if item['b'] > threshold_above], above_threshold)
    # )
    

    return selected_items


def index_of_closest(list, number):
    # Creates a list with bs (item difficulties) minus current theta.
    # The result item closest to zero is the item  with maximum information at current theta
    # Returns item index

    aux = []
    for valor in list:
        aux.append(abs(number-valor))
    return aux.index(min(aux))


import csv
def read_item_db(file):

    filename = open(file)

    file = csv.DictReader(filename)

    coditem = []
    b = []
    item = []
    key = []
   

    for col in file:
        coditem.append(col['coditem'])
        b.append(float(col['b']))
        item.append(col['item'])
        key.append(col['key'])
        

    item_db = {
        'coditem' : coditem,
        'b': b,
        'item' : item,
        'key' : key
     }
    return(item_db)

def read_item_db_new(file):
    

    filename = open(file)

    file = csv.DictReader(filename)

    coditem = []
    b = []
    item = []
    key = []
    item_db_new = []

    for col in file:
        item_db_new.append({
        'coditem' : col['coditem'],
        'b': col['b'],
        'item' : col['item'],
        'key' : col['key']
        }
        )
        
    return(item_db_new)



def estimate_theta(r, b, th):
    # r: response vector
    # b: item difficulty parameters

    import math
    conv = 0.001
    J = len(r)
    se = 10.0
    delta = conv + 1
    th = float(th[0])

    th_max = max(b) + .5
    th_min = min(b) - .5

    if sum(r) == J:
        th = th_max
    elif sum(r) == 0:
        th = th_min
    else:
        while abs(delta) > conv:
            sumnum = 0.0
            sumdem = 0.0
            for j in range(J):
                phat = 1 / (1.0 + math.exp(-1 * (th - b[j])))
                sumnum = sumnum + 1.0 * (r[j] - phat)
                sumdem = sumdem - 1.0 * phat * (1.0 - phat)
            delta = sumnum / sumdem
            th = th - delta
            se = 1 / math.sqrt(-sumdem)

    return [th, se]

 

item_db_new = read_item_db_new('rn_db.csv') # item databas (dictionnaire)
if __name__ == '__main__':
    main()
