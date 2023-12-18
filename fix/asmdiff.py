import os
import yaml

disassembler = '/root/src/disassembler/disassembler.py'
differ = '/root/src/disassembler/differ.py'

def build(code, d, candicate_id=0):
    c_file = f'{d}/{candicate_id}.c'
    with open(c_file, 'w') as f:
        f.write(code)

    o_file = f'{d}/{candicate_id}.o'
    cmd = f"bash ./build.sh {c_file} {o_file}"
    os.system(cmd)

def disasm(funcs, d, candicate_id=0):
    cmd = f"python3 {disassembler} -l c -s -y {d}/{o_file} {' '.join(funcs)} > {d}/{candicate_id}.yaml"
    os.system(cmd)

def differ(target, d, candicate_id):
    cmd = f"python3 {differ} {target} {candicate}.yaml > {d}/{candicate_id}-diff.yaml"
    os.system(cmd)

def parse_diff(d, candicate_id):
    diff_yaml = f"{d}/{candicate_id}-diff.yaml"
    diff_data = None
    with open(diff_yaml, 'r') as f:
        diff_data = yaml.safe_load(file)
    assert diff_data != None, "Failed to load diff yaml"

    candicate_only = {}
    target_only = {}
    shared = {}
    funcnames = diff_data["functions"].keys()
    for func in funcnames:
        candicate_only[func] = []
        target_only[func] = []
        shared[func] = []

        funcdiff = diff_data["functions"][func]

        co_count = funcdiff['delta'][0]  # number of lines appearing only in the candidate
        s_count = funcdiff['delta'][1]   # number of lines appearing in both disassemblies
        to_count = funcdiff['delta'][2]   # number of lines appearing only in the target

        for cid, hunk in enumerate(funcdiff['hunks']):
            hunk_tp = hunk[0]  # hunk type (-1 = candidate only; 0 = shared; 1 = target only)
            disasm_text = hunk[1]
            total = hunk[2]    # total number of lines in this hunk
            src_line = funcdiff['srcmap'][cid + 1]
            if hunk_tp == -1:
                candicate_only[func].append([disasm_text, total, src_line])
            elif hunk_tp == 0:
                shared[func].append([disasm_text, total, src_line])
            elif hunk_tp == 1:
                target_only[func].append([disasm_text, total, src_line])
            else:
                continue

        return candicate_only, target_only, shared
