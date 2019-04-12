import pickle
hashmap = {
           "83260060" : ["KHOSLA",0],
           "34082872" : ["CUMMINGS",0],
           "18656932" : ["SHELTON",0],
           "31383848" : ["STREHLOW",0],
           "33144341" : ["KATTEMALAVADI",0]
        }
pickle.dump(hashmap, open("hashdoc.pickle", "wb"))