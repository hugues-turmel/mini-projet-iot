from time import sleep
from threading import Timer

def dowork():
  wlen = random.random()
  sleep(wlen) # Emulate doing some work
  print('work done in %0.2f seconds' % wlen)

def main():
  while 1:
    t = hread(target=dowork)
    time.sleep(4)