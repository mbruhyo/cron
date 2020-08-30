import os

with open(f'{os.path.dirname(os.path.realpath(__file__))}/config.ini', 'r') as file:
    config = file.read().splitlines()

for _line in config:
    if not _line: continue
    line = _line.split('=')
    key = line[0].rstrip()
    val = line[1].lstrip()

# For future values
#if key == 'whatever':
	#whatever = val
#elif etc.
