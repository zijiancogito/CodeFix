import os
import sys
from copy import deepcopy

from openai import OpenAI

import strategy_feasibility_analyzer
import code_optimizer
import gptfix

WT = 1  # while True
DW = 2  # Do-While
CP = 3  # condition repeat combine if
GT = 4  # goto
CE = 5  # condition exchange
IS = 6  # IF to SWITCH
IC = 7  # IF to Condition expression
WF = 8  # While to For, For to While
FC = 9  # For statement conplete
ND = 10 # nested deep

class CFGOptimizer:

    def __init__(self, chall) -> None:
        self.strategies = [1,2,3,4,5,6,7,8,9,10]
        self.chall = chall
        self.client = OpenAI(api_key='sk-fnW7WGNc6sfkWrf1SZLiPdLPclvm38X4JcT1M9m4OXmfOQ4f', 
                             base_url='https://api.openai-proxy.org/v1')
        
        self.code = None
        with open(chall.starter, 'r') as f:
            self.code = f.read()
            
        self.code = self.fix_compilation_errors()
        if self.code == None:
            raise NotImplementedError
         
        self.init_test_score = {}
        self.init_test()

        self.funcnames = []
        self.functions = {}
        self.init_functions()
        
        self.context = self.init_task()
        
    def init_test(self):
        if not os.path.exists(self.chall.final):
            os.mkdir(self.chall.final)
            
        with open(os.path.join(self.chall.final, 'source.c'), 'w') as f:
            f.write(self.code)
            
        fixed_impl = self.chall.impl(self.chall.final)
        self.chall.build(fixed_impl)
        self.init_test_score = self.chall.test(fixed_impl)
        
    def fix_compilation_errors(self):
        fixed_code = gptfix.chat(self.code, self.chall.folder)
        if fixed_code == None:
            return None
        return fixed_code
        
    def init_functions(self):
        # input:  self.code str
        # return: self.functions {func_name: func_body}, self.funcnames [] name list in order
        return {}
        
    def strategy_prompt(self, opt_type):
        if opt_type == WF:  # D1
            return "Please determine whether the loop structure in this code segment is more appropriately expressed using while, do-while, or for loops, and whether the code needs to be modified. Please answer with a clear yes or no."
        if opt_type == IS:
            return "Please determine whether the branch structure in this code segment is more appropriately expressed using if or switch statements, and whether the code needs to be modified. Please answer with a clear yes or no."
        if opt_type == IC:
            return "Does the if-else control structure in this code segment clearly lend itself to simplification into a conditional expression, making the code more concise and more in line with human programming habits? Please answer with a clear yes or no."
        if opt_type == GT:
            return "Does this code contain any goto statements, and is it necessary to eliminate goto for optimizing the control structure? Please answer with a clear yes or no."
        if opt_type == WT:
            return "Please check if there is any unreasonable While(1) type of control structure in this code. If so, please indicate which line of code has this issue, outputting it in the form of Line X."
        if opt_type == DW:
            return "Please consider the entire function to determine if the use of Do-While in this code segment is the optimal choice. Could the use of While instead make the code more concise and clear? Please answer with a clear yes or no."
        if opt_type == CP:
            return "Please analyze the entire function to determine if there are any redundant conditional statements. If so, can they be merged to make the code clearer and more concise? Please answer with a clear yes or no."
        if opt_type == CE:
            return "Please determine if there are basic blocks in this code segment that can be reordered to make the code more concise and the logic simpler and clearer. Please answer with a clear yes or no."
        if opt_type == FC:
            return "Please determine if the use of for loop statements in this code segment does not conform to programming conventions, exhibiting incomplete statements, and whether it can be optimized. Please answer with a clear yes or no."
        if opt_type == ND:
            return "Please determine if the loop nesting in this code segment is optimal, and whether there is room to simplify by adjusting the alignment of the control structures. Please answer with a clear yes or no."
        return ""

    def init_task(self):
        inst_prompt = "The following is decompiled code obtained from a binary using Hex-Rays decompiler. Please analyze the entire functionality of the binary."
        prompt = f"{inst_prompt}\n{self.code}"
        messages = []
        messages.append({"role":"user", "content":prompt})

        response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                stream=True,
                )
        
        full_response = ''
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
        messages.append({"role":"assistant", "content": full_response})
        
        return messages


    def strategy_feasibility_analysis(self, opt_type, function):
        strategy = self.strategy_prompt(opt_type)
        analyze_result = strategy_feasibility_analyzer.chat(strategy, function, self.context)
        
        prompt = "I asked a code analyzer about whether a piece of code is suitable for a specific optimization, and this is the response I received. Could you help me analyze whether the response means it is suitable or not? Please answer only with yes or no."
        
        prompt = f"{prompt}\n{analyze_result}"
        messages = []
        messages.append({"role":"user", "content":prompt})
        response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                stream=True,
                )
        
        full_response = ''
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
        
        isFeas = False
        if 'yes' in full_response or 'Yes' in full_response:
            return full_response
        return ""

    def code_optimization(self, function, optimization):
        optimized_code = code_optimizer.chat(optimization, function)
        return optimized_code

    def code_check(self, function, funcname):
        tmp_functions = deepcopy(self.functions)
        tmp_functions[funcname] = function

        with open(os.path.join(self.chall.final, 'source.c'), 'w') as f:
            for func in self.funcnames:
                f.write(tmp_functions[func])
                f.write('\n\n')
                
        fixed_impl = self.chall.impl(self.chall.final)
        self.chall.build(fixed_impl)
        check_res = self.chall.test(fixed_impl)

        for k in check_res:
            if check_res[k] != self.init_test_score[k]:
                return False
        return True
                
    def code_update(self, function, funcname):
        self.functions[funcname] = function
        self.code = ""

        for func in self.funcnames:
            self.code += self.functions[func]
            self.code += "\n\n"
         
    def workflow(self, funcname, opt_type):
        function = self.functions[funcname]
        
        opt_analyze = self.strategy_feasibility_analysis(opt_type, function)
        if len(opt_analyze) == 0:
            return 1
        opt_code = self.code_optimization(function, opt_analyze)
        check_res = self.code_check(self, opt_code, funcname)
        if check_res == False:
            return 2
        self.code_update(opt_code, funcname)
        return 0

    def optimize_all(self):
        for func in self.funcnames:
            for st in self.strategies:
                self.workflow(func, st)
     

