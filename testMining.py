import time
from pathlib import Path

SEED='251469421087879559362097720173178685771'
COMPLEXITY='5925843677574181546892424593879229674001377114484157008543128'

data_b = int(SEED).to_bytes(16, byteorder='big')
print(SEED)
data_b = bytearray(data_b)
print(data_b)

f = open("task.bin", "wb")
f.write(data_b)
f.close()

while True:
    solution = Path('solution.txt')
    if solution.is_file():
        break

    time.sleep(0.03)
