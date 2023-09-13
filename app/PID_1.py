import signal
import time
#import logging, sys

class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self,signum, frame):
    self.kill_now = True

if __name__ == '__main__':
  #logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
  killer = GracefulKiller()
  while True:
    time.sleep(1)
    #logging.info("doing something in a loop ...")
    if killer.kill_now:
      break

  #logging.info("End of the program. I was killed gracefully :)")