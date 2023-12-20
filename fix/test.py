import os
import sys

import challs
import gptfix


if __name__ == '__main__':

    config = '../test/config.json'

    challenges = challs.load(config, "O0")
    failed_list = []
    for challenge in challenges:
        challenge.init_chall()

        starter_code = None
        with open(challenge.starter, 'r') as f:
            starter_code = f.read()

        fixed_code = gptfix.chat(starter_code, challenge.folder)

        if fixed_code == None:
            failed_list.append(challenge.name)
            continue

        if not os.path.exists(challenge.final):
            os.mkdir(challenge.final)

        with open(os.path.join(challenge.final, 'source.c'), 'w') as f:
            f.write(fixed_code)

        fixed_impl = challenge.impl(challenge.final)
        print(challenge.build(fixed_impl))
        print(challenge.test(fixed_impl))
