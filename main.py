import string
import urllib.request
import json
import datetime
import time
from pathlib import Path


GIVERS = [
    'kf-kkdY_B7p-77TLn2hUhM6QidWrrsl8FYWCIvBMpZKprBtN', 
    'kf8SYc83pm5JkGt0p3TQRkuiM58O9Cr3waUtR9OoFq716lN-', 
    'kf-FV4QTxLl-7Ct3E6MqOtMt-RGXMxi27g4I645lw6MTWraV',
    'kf_NSzfDJI1A3rOM0GQm7xsoUXHTgmdhN5-OrGD8uwL2JMvQ', 
    'kf8gf1PQy4u2kURl-Gz4LbS29eaN4sVdrVQkPO-JL80VhOe6',
    'kf8kO6K6Qh6YM4ddjRYYlvVAK7IgyW8Zet-4ZvNrVsmQ4EOF', 
    'kf-P_TOdwcCh0AXHhBpICDMxStxHenWdLCDLNH5QcNpwMHJ8',
    'kf91o4NNTryJ-Cw3sDGt9OTiafmETdVFUMvylQdFPoOxIsLm', 
    'kf9iWhwk9GwAXjtwKG-vN7rmXT3hLIT23RBY6KhVaynRrIK7',
    'kf8JfFUEJhhpRW80_jqD7zzQteH6EBHOzxiOhygRhBdt4z2N', 
]

POOL_URL = 'https://pool.services.tonwhales.com/job'

def get_now()-> (str):
    return int(datetime.datetime.timestamp(datetime.datetime.utcnow()))

def get_job():
    job=json.loads(urllib.request.urlopen(POOL_URL, timeout = 5).read())
    print(job)
    expire=job["expire"]
    seed=job["seed"]
    wallet=job["wallet"]
    complexity=job["complexity"]
    prefix=job["prefix"]
    giver=job["giver"]
    return giver, seed, complexity, wallet

def createJob(seed):
    seed_dec=int(seed,16)
    data_b = seed_dec.to_bytes(16, byteorder='big')
    data_b = bytearray(data_b)

    f = open("task.bin", "wb")
    f.write(data_b)
    f.close()
    return

giver, seed, _,  _ = get_job()
createJob(seed)

while True:
    solution = Path("solution.txt")
    if solution.is_file():
        print('SUCCESS')
        exit()
    time.sleep(0.1)



### From  https://pool.services.tonwhales.com/job
'''
{'wallet': 'EQAAFhjXzKuQ5N0c96nsdZQWATcJm909LYSaCAvWFxVJP80D', 'seed': '1552e546aeb6a32773dae2c126989b04', 
'complexity': '0000000003ffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'prefix': 'a81a8a8de64ace4627d675b87cb3c1e0', 
'giver': 'Ef-kkdY_B7p-77TLn2hUhM6QidWrrsl8FYWCIvBMpZKprKDH', 'expire': 1643897846}
'''


## From giver
'''
result:  [ 282317623882463377444294663091804506354 3963001003893418939003277035325602897538378125021011482429544 100000000000 256 ]
'''
