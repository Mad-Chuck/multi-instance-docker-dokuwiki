import fire

from cmd_animal.create import create
from cmd_animal.print import print
from cmd_animal.remove import remove
from cmd_animal.restart import restart
from cmd_animal.run import run
from cmd_animal.stop import stop
from cmd_animal.update import update

if __name__ == '__main__':
  fire.Fire()