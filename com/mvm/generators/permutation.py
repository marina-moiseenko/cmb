import logging
import inspect


class Permutation(object):

    __log = None
    
    errorsDict = {1000: 'Alphabet is not specified'}
    
    warningsDict = {}

    @staticmethod
    def __init_logger():
        
        if not Permutation.__log:
            Permutation.__log = logging.getLogger('x')
            Permutation.__log.setLevel(logging.WARNING)
            handler = logging.StreamHandler()
            bf = logging.Formatter(
                '{asctime} {name} {levelname:8s} {message}', style='{')
            handler.setFormatter(bf) 
            Permutation.__log.addHandler(handler)
            Permutation.__log.propagate = False
            Permutation.__log.debug("Logger set up")   
        
    def __new__(cls, alphabet):

        Permutation.__init_logger()
        obj = super(Permutation, cls).__new__(cls)   

        return obj

    __permutation_length = 0
        
    def __init__(self, alphabet):

        # l1 = permutation.__getLogger1()
        
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
                        + 'and will be omitted')
                        
        self.lastCall = list()
        self.__start_after = list()
        self.lastCall.append(inspect.stack()[0][3])

    @property
    def permutation_length(self):
        return self.__permutation_length

    @permutation_length.setter
    def permutation_length(self, length):

        self.lastCall.append(inspect.stack()[0][3])
        self.__permutation_length = length

    @property
    def start_after(self):
        return self.__start_after

    @start_after.setter
    def start_after(self, start_after):

        self.lastCall.append(inspect.stack()[0][3])

        if not start_after:
            self.__start_after = None
        elif isinstance(start_after, list):
            self.__start_after = start_after
            self.__permutation_length = len(start_after)
        elif isinstance(start_after, str):
            self.__start_after = list()
            for c in start_after:
                self.__start_after.append(c)
            self.__permutation_length = len(start_after)

    def is_final(self, permutation, start_index=0):
    
        self.lastCall.append(inspect.stack()[0][3])
        
        used_elements = permutation[:start_index]
        check_this = permutation[start_index:]
        alphabet = self.alphabet[:]
        for e in used_elements:
            if alphabet.count(e) > 0:
                alphabet.remove(e)
        return alphabet[:-len(check_this)-1:-1] == check_this

    def get_next_non_repeatable(self, after=None, used=None):
        
        self.lastCall.append(inspect.stack()[0][3])
        
        alphabet = self.alphabet[:]
        
        if after is None or alphabet.count(after) == 0:
            x = -1
            if after is None:
                Permutation.__log.info(
                    "Available element will be searched from the beginning of alphabet. Start point is not specified")
            else:
                Permutation.__log.warning(
                    "Given element {} is not included into alphabet {} and will not be taken into account"
                    .format(after, alphabet))

        else:
            x = alphabet.index(after) 
        
        if after == alphabet[:-2:-1][0]:
            Permutation.__log.warning("Given element is the last in array. None will be returned")
            return None 

        if (used is None) or (len(used) == 0):
            
            Permutation.__log.info(
                "Used values are not set. Next element after {} of alphabet {} will be returned"
                .format(after, alphabet))
            return alphabet[x+1]  
        
        for e in alphabet[x+1:]:
            if used.count(e) == 0:
                Permutation.__log.debug(
                    "Next element after {} of alphabet {}, excluding the following {}, is {}."
                    .format(after, alphabet, used, e))
                return e
        Permutation.__log.warning(
            "Unexpected set of parameters for alphabet {}, start point {} and used elements {}"
            .format(alphabet, after, used))
        return None

    def validate(self):
        
        self.lastCall.append(inspect.stack()[0][3])

    def is_validation_passed(self):
        
        if not self.just_validated():
            self.validate()
        
        # to do check internal errorList
        
        return True

    def __get_last_call_safe(self):
        
        if self.lastCall:
            return self.lastCall[len(self.lastCall) - 1]
        
    def just_validated(self):
        
        last = self.__get_last_call_safe()
        Permutation.__log.debug('last is {}'.format(last))
        return last == 'validate'

    def generate_permutation(self):
        ''' Generates permutation which follows the given one ww 
        '''

        self.lastCall.append(inspect.stack()[0][3])

        previous = self.__start_after[:]

        if previous is None:
            Permutation.__log.info("Previous permutation is not specified. None will be returned")

        permutation = []
        alphabet_to_use = self.alphabet[:]
        x = 0

        Permutation.__log.debug(
            'Generating permutation for alphabet {}'.format(self.alphabet))
        Permutation.__log.debug('Previous permutation is {}'.format(previous))
        
        if self.is_final(previous) and permutation == []:
            Permutation.__log.info(
                "Permutation {} is last in the row of alphabet {}".format(previous, self.alphabet))
            return None

        while len(permutation) <= self.__permutation_length - 1:
            Permutation.__log.debug('x: {}'.format(x) + '_'*40)
            Permutation.__log.debug('len(permutation): {}'.format(len(permutation)))   
            if self.__permutation_length - len(permutation) == 1:
                # print('One last element of permutation is left ')
                permutation.append(self.get_next_non_repeatable(previous[x], permutation))
                alphabet_to_use.remove(permutation[x])

            elif self.__permutation_length - len(permutation) == 2:
                Permutation.__log.debug(
                    'Two last elements of permutation are left {} and {}. Last alpha {}'
                    .format(previous[x], previous[x+1], self.alphabet[:-2:-1][0]))
                
                if self.is_final(previous, x):
                    # print('Let\'s repeat them')
                
                    permutation.append(previous[x])
                    permutation.append(previous[x+1])
                    break
                    
                elif self.is_final(previous, x+1):
                    
                    permutation.append(self.get_next_non_repeatable(previous[x], permutation))
                    # print("Increasing current... {}".format(permutation))
                    permutation.append(self.get_next_non_repeatable(used=permutation))
                    # print("Finding first not used... {}".format(permutation))
                    
                    break
                else:
                
                    permutation.append(previous[x]) 
                    Permutation.__log.debug("Repeating current... {}".format(permutation))
                    Permutation.__log.debug("Finding next for {} current... {}".format(previous[x+1], permutation))
                    permutation.append(self.get_next_non_repeatable(previous[x + 1], permutation))
                    
                    break

            elif self.is_final(previous, x+1):
                
                # print('lefover is last in permutation, increase current sign')
                # print("position in current permutation = {}".format(x))

                permutation.append(self.get_next_non_repeatable(previous[x], permutation))
                alphabet_to_use.remove(permutation[x])
                
                # print("adding leftover {}".format(alphabet_to_use[:permutation_length - len(permutation)]))
                for e in alphabet_to_use[:self.__permutation_length - len(permutation)]:
                    permutation.append(e)
                    
                break    
            else:
                
                # print('Use the same element as in previous permutation')
                permutation.append(previous[x])
                alphabet_to_use.remove(permutation[x])
                
            x += 1
        self.__start_after = permutation
        Permutation.__log.info("next permutation is {}".format(permutation))
        return permutation

    def generate_permutations(self, count=0):

        x = 0

        res = []

        Permutation.__log.debug("Generate series of permutations issued")
        Permutation.__log.debug(
            "Alphabet: {}, required permutations: {}".format(self.alphabet, count))

        if not self.__start_after:
            next_p = self.alphabet
            res.append(self.alphabet)
        else:
            next_p = self.__start_after

        Permutation.__log.debug("start with {}".format(next_p))

        while (count == 0 or x < count) and next_p:
            next_p = self.generate_permutation()
            if next_p:
                res.append(next_p)
            x += 1

        return res

