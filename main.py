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
    
 
def generatePermutation(alphabet, previous=None):
    ''' Generates permutation which follows the given one  '''

    
    if previous is None:
        log.info("Previous permutation is not specified. None will be returned")
    
    permutation_length = len(previous) 
    previous = previous[:]
    permutation = []
    alphabet_to_use = alphabet[:]
    x = 0


    log.debug('Generating permutation for alphabet {}'
                        .format(alphabet))
    log.debug('Previous permutation is {}'.format(previous))
    
    if isFinal(alphabet, previous) and permutation == []:
        log.info("Permutation {} is last in the row of alphabet {}"
                        .format(previous, alphabet))
        return None
    

    
    while len(permutation) <= permutation_length - 1:
        
           
        #print('x: {}'.format(x) + '_'*40)   
        #print('len(permutation): {}'.format(len(permutation)))   
           
        
        
        if permutation_length - len(permutation) == 1:
            #print('One last element of permutation is left')
            permutation.append(getNextNonRepeatable(alphabet, previous[x], permutation))
            alphabet_to_use.remove(permutation[x])
             
            
        elif permutation_length - len(permutation) == 2: 
            #print('Two last elements of permutation are left {} and {}. Last alpha {}'.format(
            #        previous[x], previous[x+1], alphabet[:-2:-1][0]))
            
            if isFinal(alphabet, previous, x):
                #print('Let\'s repeat them')
            
                permutation.append(previous[x])
                permutation.append(previous[x+1])
                break
                
            elif isFinal(alphabet, previous, x+1):
                
                permutation.append(getNextNonRepeatable(alphabet, previous[x], permutation)) 
                #print("Increasing current... {}".format(permutation))
                permutation.append(getNextNonRepeatable(alphabet, used=permutation)) 
                #print("Finding first not used... {}".format(permutation))
                
                break
            else:
            
                permutation.append(previous[x]) 
                #print("Repeating current... {}".format(permutation))
                permutation.append(getNextNonRepeatable(alphabet,previous[x+1],used=permutation)) 
                #print("Finding next for {} current... {}".format(previous[x+1], permutation))
                
                break

        elif isFinal(alphabet, previous,x+1): 
            
            #print('lefover is last in permutation, increase current sign')
            #print("position in current permutation = {}".format(x))

            permutation.append(getNextNonRepeatable(alphabet, previous[x], permutation))
            alphabet_to_use.remove(permutation[x])
            
            #print("adding leftover {}".format(alphabet_to_use[:permutation_length - len(permutation)]))
            for e in alphabet_to_use[:permutation_length - len(permutation)]:
                permutation.append(e)
                
            break    
        else:
            
            #print('Use the same element as in previous permutation')
            permutation.append(previous[x])
            alphabet_to_use.remove(permutation[x])
            
        x += 1
        #print('prev:     {}'.format(previous))
        #print('permutation: {}'.format(permutation))
        #print('x:        {}'.format(x))
        #print('abc left: {}'.format(alphabet_to_use))

    #print("permutation is {}".format(permutation))
    return permutation
    
    
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
    log.critical("Started at ..." + str(started_at))
    abc = [0,1,2,3,4,5,6,7,8]
    ##prev = [2,3, 1]
    ##prev = [2,3, 5]
    ##prev = [2,6] 
    ##prev = [6,5]
    prev = [1,2,3, 4]
    #prev = [1]
    #print(isFinal1([1,2,3], [2,3,1], 2))
    log.error("res \n{}".format(generatePermutations(abc)))
    #v = generateNextPermutations(prev, abc)
    #v = generateNextPermutation(prev, abc)
    #v = getNextNonRepeatable(abc, 5, [2,4])
    #print('abc is {}'.format(abc))
    #print('prev is {}'.format(prev))
    #print('v is {}'.format(v))
    
    log.critical("Ended for ..." + str(datetime.datetime.now() - started_at))
