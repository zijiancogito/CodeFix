import collections
import json
import os
import re

import sandbox

disassembler = "/root/src/disassembler/disassembler.py"

class ChallengeImpl:
    def __init__(self, info, folder):
        self.info = info
        self.folder = folder
        self.source = os.path.join(folder, 'source' + info.extension)
        self.binary = os.path.join(folder, 'binary.out')
        self.disasm = os.path.join(folder, 'disasm.yml')


class ChallengeInfo:
    def __init__(self, name, root, data, level, defaults={}):
        self.name = name
        self.extension = '.c'
        self.level = level

        def replace(match):
            text = match.group()
            if text == '%n': return name
            if text == '%r': return root
            if text == '%f': return self.folder
            if text == '%l': return self.level
            if text == '%x': return self.extension
            raise Exception('Unknown escape: ' + text)

        def lookup(key):
            val = data.get(key)
            if val is not None:
                return val
            val = defaults[key]
            if isinstance(val, str):
                val = re.sub('%.', replace, val)
            return val

        self.include = os.path.join(root, lookup('include'))
        self.folder = os.path.join(root, lookup('folder'))
        self.container = lookup('container')
        self.functions = lookup('functions')
        self.options   = lookup('options')

        self.starter = os.path.join(root, lookup('starter'))  # Raw decompiled code
        self.source  = os.path.join(root, lookup('source'))   # Source code
        self.disasm  = os.path.join(root, lookup('disasm'))   # Raw disasm code
        self.binary  = os.path.join(root, lookup('binary'))   # Raw binary
        self.recomp  = os.path.join(root, lookup('recomp'))
        self.final   = os.path.join(root, lookup('final'))    # fixed source code
        
        self.tester  = os.path.join(root, lookup('tester'))   # 
        self.builder = os.path.join(root, lookup('builder'))

    def build(self, impl):
        return sandbox.build(self, impl)

    def impl(self, folder):
        return ChallengeImpl(self, folder)

    def test(self, impl, verbose=False):
        return sandbox.test(self, impl, verbose=verbose)

    def disassemble(self, impl, srcmap=True, warn=False):
        cmd = f"python3 {disassembler} -l c -s -y {impl.binary} {' '.join(impl.info.functions)} > {impl.disasm}"
        os.system(cmd)

    def init_chall(self):
        init_impl = self.impl(self.folder)
        self.disassemble(init_impl, True)


def load(path, level):
    root = os.path.abspath(os.path.dirname(path))
    with open(path) as file:
        config = json.load(file)

    challenges = []
    defaults   = config.get('defaults', {})
    for name, data in config['binaries'].items():
        challenges.append(ChallengeInfo(name, root, data, level, defaults))

    return challenges

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='path to config.json')
    args = parser.parse_args()

    challenges = load(args.config, 'O0')
    for challenge in challenges:
        print('Name:', challenge.name)
        print('  Container: ', challenge.container)
        print('  Functions: ', ' '.join(challenge.functions))
        print('  Builder:   ', challenge.builder)
        print('  Options:   ', ' '.join(challenge.options))
        print()
        print('  Include:   ', challenge.include)
        print('  Source:    ', challenge.source)
        print('  Binary:    ', challenge.binary)
        print('  Disasm:    ', challenge.disasm)
        print('  Starter:   ', challenge.starter)
        print('  Tester:    ', challenge.tester)
        print()

        init_impl = challenge.impl(challenge.folder)
        # challenge.build(init_impl)
        challenge.disassemble(init_impl, True)
        with open(challenge.disasm, 'r') as f:
            print(f.read())


    

