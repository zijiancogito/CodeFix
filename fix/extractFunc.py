import os

# compiler_generated_funcs = [
# 	'_init',
# 	'__cxa_finalize',
# 	'__stack_chk_fail',
# 	'__isoc99_scanf',
# 	'_start',
# 	'deregister_tm_clones',
# 	'register_tm_clones',
# 	'__do_global_dtors_aux',
# 	'_do_global_dtors_aux',
# 	'frame_dummy',
# 	'_fini',
# 	'__libc_start_main',
# 	'UnresolvableJumpTarget',
# 	'UnresolvableCallTarget',
# 	'__printf_chk',
# 	'__cxx_global_var_init-ir',
# 	'__cxx_global_var_init',
# 	'__cxa_atexit',
# 	'llvm.memset.p0i8.i64',
# 	'_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_',
# 	'(**init_proc())',
# 	'term_proc',
# 	'_libc_csu_init',
# 	'_libc_csu_fini',
# 	'_gmon_start__',
# 	'start',
# 	'sub_1020',
# ]

class ExtractFuncs(object):
	def __init__(self):
		pass

	def findFuncs(self, file):
		self.file = file
		self.funcs = []  # the number of rows of functions
		self.funcsname = []
		self._findCBs()
		funcs = self.funcs.copy()
		for func in funcs:
			sr = func[0]  # the number of row of {
			if self._preChar(sr) != ')':
				self.funcs.remove(func)
				continue
			lr, idx = self._findPare(sr)
			if lr != None:
				try:
					s = self.file[lr]
					s = s[:idx]
					s = s.split()
					func_name = s[-1]
					while func_name[0] == '*':
						func_name = func_name[1:]
				except:
					self.funcs.remove(func)
					continue

				# if func_name in compiler_generated_funcs:
				# 	self.funcs.remove(func)
				# 	continue

				self.funcsname.append(func_name)
				if len(s) == 1:
					lr -= 1
				'''
				for i in range(len(s)):
					c = s[i]
					if '(' in c:
						if (c.find('(') == 0 and i < 2) or (c.find('(') != 0 and i < 1):
							lr -= 1
						break
				'''
				if self.funcs.count(func):
					self.funcs[self.funcs.index(func)][0] = lr

	def getFuncs(self, file):
		self.findFuncs(file)
		funcs = []
		for funcrow in self.funcs:
			func = ""
			for i in self.file[funcrow[0]: funcrow[1] + 1]:
				func += i + '\n'
			funcs.append(func)

		return funcs, self.funcsname
	
	def _findCBs(self):  # CB: curly braces
		stack = []
		for i in range(len(self.file)):
			r = self.file[i]
			for s in r:
				if s == '{':
					stack.append(i)
				elif s == '}':
					if len(stack) > 1:
						stack.pop()
					elif len(stack) == 1:
						self.funcs.append([stack[0], i])
						stack.pop()
						break

	def _findPare(self, sr):
		stack = []
		for i in range(sr, -1, -1):
			r = self.file[i]
			if i == sr:
				range_begin = r.find('{')
			else:
				range_begin = len(r) - 1
			for j in range(range_begin, -1, -1):
				s = r[j]
				if s == ')':
					stack.append(i)
				elif s == '(':
					if len(stack) > 1:
						stack.pop()
					elif len(stack) == 1:
						return (i, j)
		return (None, None)

	def _preChar(self, row):
		r = self.file[row]
		idx = r.find('{')
		for i in range(idx - 1, -1, -1):
			if not r[i].isspace():
				return r[i]

		for i in range(row - 1, -1, -1):
			r = self.file[i]
			for j in range(len(r) - 1, -1, -1):
				if not r[j].isspace():
					return r[j]
		return None

	'''
	def _getFuncName(self):
		for func in self.funcs:
			for i in range(func[0], func[1]):
				r = self.file[i]
				if '(' in r:
					r = r.split('(')
					fn = r[0]
					fn = fn.split()
					self.funcsname.append(fn[-1])
					break
	'''