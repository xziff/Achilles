import pickle

with open('ss.pickle', 'rb') as f:
    data = pickle.load(f)

    for i in range(len(data)):
        with open(str(i)+'.txt', 'w') as ff:
            for line in data[i]:
                ff.write(str(line) + '\n')
    
    data = pickle.load(f)
    with open('t.txt', 'w') as ff:
        for line in data:
            ff.write(str(line) + '\n')