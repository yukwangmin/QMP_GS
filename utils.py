import numpy as np

def relativeError(true: float, est: float):
    return (np.abs(true - est) / np.abs(true))


def extract(count, N, n):
    
    zeros = 0
    ones = 0
    
    for i in range(2**(N-1)):
        bin = f'{{0:0>{N-1}b}}'.format(i)
        bin0 = bin[:N-1-n] + '0' + bin[N-1-n:]
        bin1 = bin[:N-1-n] + '1' + bin[N-1-n:]
        
        #print(bin0)
        #print(bin1)
        
        zeros += count.get(bin0, 0)
        ones += count.get(bin1, 0)
    
    
    return zeros, ones




#
# count : return of result.get_counts()
# N     : The total number of bits of measurement
# least : The least bit of the extract
# n     : The number of bits of extract
#
def extractList(count, N, least, n):
    
    cnt = {}

    
    for i in range(2**n):
        key = f'{{0:0>{n}b}}'.format(i)
        cnt[key] = 0
    
    for j in range(2**n):
        key = f'{{0:0>{n}b}}'.format(j)
    
        for i in range(2**(N-n)):
            bin = f'{{0:0>{N-n}b}}'.format(i)
            nkey = bin[:N-n-least] + key + bin[N-n-least:]
            cnt[key] += count.get(nkey, 0)
            
    return cnt   
        