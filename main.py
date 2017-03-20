import datetime




def isFinal(alphabet, permutation, startIndex=0):
    usedElements = permutation[:startIndex]
    checkThis = permutation[startIndex:]
    alphabet = alphabet[:]
    for e in usedElements:
        if alphabet.count(e) > 0:
            alphabet.remove(e)
    return alphabet[:-len(checkThis)-1:-1] == checkThis

    

def getNextNonRepeatable(alphabet, after=None, used=None):
    if alphabet is None:
        log.warning("Alphabet is not specified. None will be returned")
        return None 
    # or isn't list 
    
    if (after is None or alphabet.count(after) == 0): 
        x = -1
        if after is None:
            log.info("Available element will be searched from the begining of alphabet. Strat point is not specified"
                        .format(after, alphabet))
        else:
            log.warning("Given element {} is not included into alphabet {} and will not be taken into account"
                        .format(after, alphabet))

    else:
        x = alphabet.index(after) 
    
    if after == alphabet[:-2:-1][0]:
        log.warning("Given element is the last in array. None will be returned")
        return None 
    
    
    if (used is None) or (len(used) == 0):
        
        log.info("Used values are not set. Next element after {} of alphabet {} will be returned"
                        .format(after, alphabet))
        return alphabet[x+1]  
    
    for e in alphabet[x+1:]:
        if used.count(e) == 0:
            log.debug("Next element after {} of alphabet {}, excluding the following {}, is {}."
                        .format(after, alphabet, used, e))
            return e
    log.warning("Unexpected set of parameters for alphabet {}, start point {} and used elements {}"
                        .format(alphabet, after, used))
    return None
    
 
def generatePermutation(alphabet, previous):
    ''' Generates permutation which follows the given one  '''

    
    res_len = len(previous) 
    previous = previous[:]
    cur_perm = []
    cycle_abc = alphabet[:]
    x = 0


    log.debug('Generating permutation for alphabet {}'
                        .format(alphabet))
    log.debug('Previous permutation is {}'.format(previous))
    
    if isFinal(alphabet, previous) and cur_perm == []:
        log.info("Permutation {} is last in the row of alphabet {}"
                        .format(previous, alphabet))
        return None
    

    
    while len(cur_perm) <= res_len - 1:
        
           
        #print('x: {}'.format(x) + '_'*40)   
        #print('len(cur_perm): {}'.format(len(cur_perm)))   
           
        
        
        if res_len - len(cur_perm) == 1:
            #print('One last element of permutation is left')
            cur_perm.append(getNextNonRepeatable(alphabet, previous[x], cur_perm))
            cycle_abc.remove(cur_perm[x])
             
            
        elif res_len - len(cur_perm) == 2: 
            #print('Two last elements of permutation are left {} and {}. Last alpha {}'.format(
            #        previous[x], previous[x+1], alphabet[:-2:-1][0]))
            
            if isFinal(alphabet, previous, x):
                #print('Let\'s repeat them')
            
                cur_perm.append(previous[x])
                cur_perm.append(previous[x+1])
                break
                
            elif isFinal(alphabet, previous, x+1):
                
                cur_perm.append(getNextNonRepeatable(alphabet, previous[x], cur_perm)) 
                #print("Increasing current... {}".format(cur_perm))
                cur_perm.append(getNextNonRepeatable(alphabet, used=cur_perm)) 
                #print("Finding first not used... {}".format(cur_perm))
                
                break
            else:
            
                cur_perm.append(previous[x]) 
                #print("Repeating current... {}".format(cur_perm))
                cur_perm.append(getNextNonRepeatable(alphabet,previous[x+1],used=cur_perm)) 
                #print("Finding next for {} current... {}".format(previous[x+1], cur_perm))
                
                break

        elif isFinal(alphabet, previous,x+1): 
            
            #print('lefover is last in permutation, increase current sign')
            #print("position in current permutation = {}".format(x))

            cur_perm.append(getNextNonRepeatable(alphabet, previous[x], cur_perm))
            cycle_abc.remove(cur_perm[x])
            
            #print("adding leftover {}".format(cycle_abc[:res_len - len(cur_perm)]))
            for e in cycle_abc[:res_len - len(cur_perm)]:
                cur_perm.append(e)
                
            break    
        else:
            
            #print('Use the same element as in previous permutation')
            cur_perm.append(previous[x])
            cycle_abc.remove(cur_perm[x])
            
        x += 1
        #print('prev:     {}'.format(previous))
        #print('cur_perm: {}'.format(cur_perm))
        #print('x:        {}'.format(x))
        #print('abc left: {}'.format(cycle_abc))

    #print("cur_perm is {}".format(cur_perm))
    return cur_perm
    
    
def generatePermutations(alphabet, startWith=None, count=0):
    
    x = 0
    
    res = []
    
    if startWith is None:
        next = alphabet
        res.append(alphabet)
    else:
        next = startWith
        
    log.error("{}:  1".format(next))
            
    while (count == 0 or x < count) and not next is None:
        next = generatePermutation(alphabet, next)
        if not next is None:
            res.append(next)
            log.error("{}:  {}".format(next, x+2))
        x += 1
    return res
    
    
import logging    

log = logging.getLogger()
log.setLevel(logging.CRITICAL)
handler = logging.StreamHandler()
bf = logging.Formatter('{asctime} {levelname:8s} ' + 
                            ' {message}',style='{')
handler.setFormatter(bf) 
log.addHandler(handler)
                           
    
if __name__ == "__main__":
    started_at = datetime.datetime.now()
    log.critical("Started at ..." + str())
    abc = [0,1,2,3,4,5,6,7,8,9]
    ##prev = [2,3, 1]
    ##prev = [2,3, 5]
    ##prev = [2,6] 
    ##prev = [6,5]
    prev = [1,2,3, 4]
    #prev = [1]
    #print(isFinal1([1,2,3], [2,3,1], 2))
    log.critical("res \n{}".format(generatePermutations(abc)))
    #v = generateNextPermutations(prev, abc)
    #v = generateNextPermutation(prev, abc)
    #v = getNextNonRepeatable(abc, 5, [2,4])
    #print('abc is {}'.format(abc))
    #print('prev is {}'.format(prev))
    #print('v is {}'.format(v))
    
    log.critical("Ended for ..." + str(datetime.datetime.now() - started_at))

'''


12435

1?  -  len - 3

'''