import os
import subprocess
import re

from openai import OpenAI

def chat(code, d):
    messages = []

    head_prompt = "
