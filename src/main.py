import logging
import datetime

log = logging.getLogger()
log.setLevel(logging.CRITICAL)
handler = logging.StreamHandler()
bf = logging.Formatter('{asctime} {levelname:8s} {message}', style='{')
handler.setFormatter(bf) 
log.addHandler(handler)
                           
    
if __name__ == "__main__":
    started_at = datetime.datetime.now()
    log.critical("Started at ..." + str(started_at))

    from com.mvm.generators.permutation import Permutation

    p1 = Permutation('123')
    # p1.start_after = '4231'
    p1.permutation_length = 2

    for e in p1.generate_permutations():
        print(e)

