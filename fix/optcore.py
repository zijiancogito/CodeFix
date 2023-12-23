import os
import sys

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

def prompt_selector(opt_type):
    if opt_type == WT:
        return "Please check if there is any unreasonable While(1) type of control structure in this code. If so, please indicate which line of code has this issue, outputting it in the form of Line X."

