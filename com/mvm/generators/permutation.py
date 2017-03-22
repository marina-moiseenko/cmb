import logging
import inspect

class Permutation(object):

    __log = None
    
    errorsDict = {1000: 'Alphabet is not specified'}
    
    warningsDict = {}
    
    
    
    
    def __initLogger():
        
        if not Permutation.__log:
            Permutation.__log = logging.getLogger('x')
            Permutation.__log.setLevel(logging.DEBUG)
            handler = logging.StreamHandler()
            bf = logging.Formatter('{asctime} {name} {levelname:8s} '
                                    + ' {message}',style='{')
            handler.setFormatter(bf) 
            Permutation.__log.addHandler(handler)
            Permutation.__log.propagate = False
            Permutation.__log.debug("Logger set up")   
        
        
    def __new__(cls, alphabet): 
    
        
        Permutation.__initLogger() 
        obj = super(Permutation, cls).__new__(cls)   

        return obj
            
        

    __permutation_length = 0
        
    def __init__(self, alphabet):
        
        
        #l1 = permutation.__getLogger1()
        
        Permutation.__log.debug("__init__ invoked")
        
        

        if isinstance(alphabet, list):
            self.alphabet = alphabet[:]
            
        elif isinstance(alphabet, str):
            self.alphabet = []
            for c in alphabet:
                if self.alphabet.count(c) == 0:
                    self.alphabet.append(c)
                else:
                    Permutation.__log.warning(
                    'Char {} is duplicated in given alphabet \'{}\' '
                        .format(c, alphabet) 
                        + 'and will be ommited')
                        
        self.lastCall = list()
        
        self.lastCall.append(inspect.stack()[0][3])
        
                        

    def setPermutationLength(self, len):
    
        self.__permutation_length = len
        self.lastCall.append(inspect.stack()[0][3])                
                        
                        
    def getPermutationLength(self):
    
        if self.__permutation_length:
            return self.__permutation_length
        else:
            pass

                        
    def isFinal(self, permutation, startIndex=0):
    
        self.lastCall.append(inspect.stack()[0][3])
        
        usedElements = permutation[:startIndex]
        checkThis = permutation[startIndex:]
        alphabet = self.alphabet[:]
        for e in usedElements:
            if alphabet.count(e) > 0:
                alphabet.remove(e)
        return alphabet[:-len(checkThis)-1:-1] == checkThis 

    def getNextNonRepeatable(self, after=None, used=None):
        
        self.lastCall.append(inspect.stack()[0][3])
        
        alphabet = self.alphabet[:]
        
        if (after is None or alphabet.count(after) == 0): 
            x = -1
            if after is None:
                Permutation.__log.info("Available element will be searched from the begining of alphabet. Start point is not specified")
            else:
                Permutation.__log.warning("Given element {} is not included into alphabet {} and will not be taken into account"
                            .format(after, alphabet))

        else:
            x = alphabet.index(after) 
        
        if after == alphabet[:-2:-1][0]:
            Permutation.__log.warning("Given element is the last in array. None will be returned")
            return None 
        
        
        if (used is None) or (len(used) == 0):
            
            Permutation.__log.info("Used values are not set. Next element after {} of alphabet {} will be returned"
                            .format(after, alphabet))
            return alphabet[x+1]  
        
        for e in alphabet[x+1:]:
            if used.count(e) == 0:
                Permutation.__log.debug("Next element after {} of alphabet {}, excluding the following {}, is {}."
                            .format(after, alphabet, used, e))
                return e
        Permutation.__log.warning("Unexpected set of parameters for alphabet {}, start point {} and used elements {}"
                            .format(alphabet, after, used))
        return None
        
    
    def validate(self):
        
        self.lastCall.append(inspect.stack()[0][3])
        
        
        
    def isValidationPassed(self):
        
        if not self.__justValidated():
            self.validate()
        
        #todo check internal errorList
        
        return True

    def __getLastCallSafe(self):
        
        if self.lastCall:
            return self.lastCall[len(self.lastCall) - 1]
        
    def __justValidated(self):
        
        last = self.__getLastCallSafe()
        Permutation.__log.debug('last is {}'.format(last))
        return last == 'validate'

    
        
    def printCalls(self):
    #to delete
        Permutation.__log.debug(self.lastCall)
        
        
    
    def generatePermutation(self, previous=None):
        ''' Generates permutation which follows the given one  '''
        
        
        
        #if 
        
        self.lastCall.append(inspect.stack()[0][3])
        
        if previous is None:
            Permutation.__log.info("Previous permutation is not specified. None will be returned")
        
        permutation_length = len(previous) 
        previous = previous[:]
        permutation = []
        alphabet_to_use = self.alphabet[:]
        x = 0


        Permutation.__log.debug('Generating permutation for alphabet {}'
                            .format(self.alphabet))
        Permutation.__log.debug('Previous permutation is {}'.format(previous))
        
        if self.isFinal(previous) and permutation == []:
            Permutation.__log.info("Permutation {} is last in the row of alphabet {}"
                            .format(previous, self.alphabet))
            return None
        

        
        while len(permutation) <= permutation_length - 1:
            
               
            Permutation.__log.debug('x: {}'.format(x) + '_'*40)   
            Permutation.__log.debug('len(permutation): {}'.format(len(permutation)))   
               
            
            
            if permutation_length - len(permutation) == 1:
                #print('One last element of permutation is left ')
                permutation.append(self.getNextNonRepeatable(previous[x], permutation))
                alphabet_to_use.remove(permutation[x])
                 
                
            elif permutation_length - len(permutation) == 2: 
                Permutation.__log.debug('Two last elements of permutation are left {} and {}. Last alpha {}'.format(
                        previous[x], previous[x+1], self.alphabet[:-2:-1][0]))
                
                if self.isFinal(previous, x):
                    #print('Let\'s repeat them')
                
                    permutation.append(previous[x])
                    permutation.append(previous[x+1])
                    break
                    
                elif self.isFinal(previous, x+1):
                    
                    permutation.append(self.getNextNonRepeatable(previous[x], permutation)) 
                    #print("Increasing current... {}".format(permutation))
                    permutation.append(self.getNextNonRepeatable(used=permutation)) 
                    #print("Finding first not used... {}".format(permutation))
                    
                    break
                else:
                
                    permutation.append(previous[x]) 
                    Permutation.__log.debug("Repeating current... {}".format(permutation))
                    Permutation.__log.debug("Finding next for {} current... {}".format(previous[x+1], permutation))
                    permutation.append(self.getNextNonRepeatable(previous[x+1], permutation)) 
                    
                    break

            elif self.isFinal(previous,x+1): 
                
                #print('lefover is last in permutation, increase current sign')
                #print("position in current permutation = {}".format(x))

                permutation.append(self.getNextNonRepeatable( previous[x], permutation))
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

        Permutation.__log.debug("next permutation is {}".format(permutation))
        return permutation
