import os, sys

def stdout():
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
