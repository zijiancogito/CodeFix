import os
import sys

import challs
import gptfix

if __name__ == '__main__':

    config = '../test/config.json'

    challenges = challs.load(config)
    for challenge in challenges:
        challenge.init_chall()

        starter_code = None
        with open(challenge.starter, 'r') as f:
            starter_code = f.read()

        fixed_code = gptfix.chat(starter_code, challenge.folder)

        with open(challenge.final, 'w') as f:
            f.write(fixed_code)
