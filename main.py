#!/usr/bin/env python3

## ITGOLD.IO 2022

import sys
from urllib import request
import json
import datetime
import time
import os
from pathlib import Path
import hashlib


## Need to init wallet in https://t.me/WhalesPoolBot
MINER_ADDR='EQCtj6TVhsruuFZX5j9xNMD8SnpEYegHjPfwxitl2IIPoKTB'

SOLUTION_FILENAME="solution.txt"
TASK_FILENAME="task.bin"

POOL_JOB_URL = 'https://rustcupgametest.itgold.io/jobs-distibutor/get'
POOL_RESULT_URL='https://pool.services.tonwhales.com/submit'

def printError(detail):
    print("Error:",detail)

def printSuccess(detail):
    print("Success:", detail)

def printWarning(detail):
    print("Warning:", detail)

def printInfo(detail):
    print("Info:", detail)


def get_now()-> (int):
    return int(datetime.datetime.timestamp(datetime.datetime.utcnow()))

def get_job():
    job=json.loads(request.urlopen(POOL_JOB_URL, timeout = 5).read())
    #printInfo(job)
    expire=job["expire"]
    seed=job["seed"]
    wallet=job["wallet"]
    complexity=job["complexity"]
    prefix=job["prefix"]  #don't use
    giver=job["giver"]
    return giver, seed, complexity, wallet, expire

def createJob(seed):
    seed_dec=int(seed,16)
    data_b = seed_dec.to_bytes(16, byteorder='big')
    data_b = bytearray(data_b)

    f = open(TASK_FILENAME, "wb")
    f.write(data_b)
    f.close()
    return

def sendJobResult(giver, result):
    data_set={"giver":giver, "miner_addr": MINER_ADDR, "inputs": [result]}
    jsondata = json.dumps(data_set)
    jsondatabytes=jsondata.encode('utf-8')

    req = request.Request(POOL_RESULT_URL)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    req.add_header('Content-Length', len(jsondatabytes))

    response = request.urlopen(req, jsondatabytes)

    #printSuccess("Sended: " +jsondata + " Responce: " + response.read().decode('utf-8'))

    ## {"ok":true,"rejected_seed":0,"rejected_invalid":1,"rejected_expire":0}
    result=json.loads(response.read().decode('utf-8'))
    result_rejected_seed=result["rejected_seed"]
    result_rejected_invalid=result["rejected_invalid"]
    result_rejected_expire=result["rejected_expire"]

    success = not bool(result_rejected_seed) and not bool(result_rejected_invalid) and not bool(result_rejected_expire)

    return success

def parse_solution(complexity):
    solution = Path(SOLUTION_FILENAME)
    if solution.is_file():
        with open(SOLUTION_FILENAME) as file:
            lines = file.readlines()
            os.remove(SOLUTION_FILENAME)

        
        ## нужно отправлять 123 байта от которых считается хеш в hex
        result = lines[0].replace('\n', '').replace(' ', '')
        result = result[:123*2]

        success=False

        if (int(complexity,16) > int(hashlib.sha256(bytes.fromhex(result)).hexdigest(), 16)):
            success=True

        return success, result
    #printError('Not found ' + SOLUTION_FILENAME)
    return False,''

if (len(sys.argv) > 1):
    TASK_FILENAME=sys.argv[1]+TASK_FILENAME
    SOLUTION_FILENAME=sys.argv[1]+SOLUTION_FILENAME


# удаляем старое решение.
solution = Path(SOLUTION_FILENAME)
if solution.is_file():
    os.remove(SOLUTION_FILENAME)

while True:
    giver, seed, complexity,  _, expire = get_job()
    createJob(seed)
    createJobTime=get_now()

    while True:
        solution = Path(SOLUTION_FILENAME)
        if solution.is_file():
            success, result=parse_solution(complexity)
            if (success):
                shares_accepted=sendJobResult(giver,result)
                diff=get_now()-createJobTime
                if (shares_accepted):
                    printInfo('SUCCESS:' + str(diff))
                else:
                    printInfo('REJECTED:' + str(diff))
                break
            #printWarning('Wrong result '+ result)

        time.sleep(0.03)
        
        if (int(expire) < get_now()):
            #printWarning('Job timeout')
            break
