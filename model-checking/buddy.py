import os
import http.client
import json
from ctypes import CDLL, c_double, c_int, c_char_p, byref

class BuDDy:

	# choose buddy.macos for macOS (arm64), buddy.linux for Linux (x64), buddy.windows for Windows (x64)
	def __init__(self, var_order: list, lib="buddy.macos"):
		self._bdd = CDLL(f"{os.path.split(__file__)[0]}/{lib}")

		self._bdd.bdd_satcountln.restype = c_double
		self._bdd.bdd_satcount.restype = c_double
		self._bdd.bdd_init(1<<27, 1<<22)
		self._bdd.bdd_setmaxincrease(1<<27)
		self._bdd.bdd_setcacheratio(64)
		self._bdd.bdd_setvarnum(c_int(len(var_order)))

		self.var_dict = dict(enumerate(var_order))
		self.name_dict = { x : k for k, x in self.var_dict.items() }
		self.var_bdds = { x : self.var2bdd(x) for x in self.name_dict.keys() }

	def __exit__(self):
		self._bdd.bdd_done()

	### basic methods
	@property
	# the terminal 0-node
	def false(self):
		return self._bdd.bdd_false()

	@property
	# the terminal 1-node
	def true(self):
		return self._bdd.bdd_true()

	# get the node that stands for the function x(0,1) for variable x
	def var2bdd(self, x):
		if x not in self.name_dict.keys():
			print(f"WARNING! {x} variable not found")
		return self._bdd.bdd_ithvar(self.name_dict[x])

	# get the node that stands for the function x(1,0) for variable x
	def nvar2bdd(self, x):
		if x not in self.name_dict.keys():
			print(f"WARNING! {x} variable not found")
		return self._bdd.bdd_nithvar(self.name_dict[x])

	# get the variable node u is labeled with
	def var(self, u):
		x = self._bdd.bdd_var(u)
		return self.var_dict[x]

	# get the level of node u
	def level(self, u):
		return self._bdd.bdd_var2level(self._bdd.bdd_var(u))


	# get the node to which the 0-branch from u points to
	def low(self, u):
		return self._bdd.bdd_low(u)

	# get the node to which the 1-branch from u points to
	def high(self, u):
		return self._bdd.bdd_high(u)

	# get the number of nodes of the sub-BDD in node u
	def nodecount(self, u):
		return self._bdd.bdd_nodecount(u)

	# get the number satisfying assignments in node u (integer variant)
	def satcount_int(self, u):
		scount = 0
		stack = [(u, 0)]
		vcount = len(self.var_dict)

		while stack:
			node, depth = stack.pop()
			if node == self.true:
				scount += 1 << (vcount - depth)
			elif node != self.false:
				stack.append((self.low(node),  depth +1))
				stack.append((self.high(node), depth +1))
		return scount

	# get the number satisfying assignments in node u (double variant)
	def satcount(self, u):
		return self._bdd.bdd_satcount(u)

	# get the logarithm of satisfying assignments in node u (for large model counts)
	def satcount_ln(self, u):
		return self._bdd.bdd_satcountln(u)

	def support(self, u):
		return self._bdd.bdd_support(u)
	
	### Operations
	def neg(self, u):
		return self._bdd.bdd_not(u)
		
	def apply_and(self, u, v):
		return self._bdd.bdd_and(u,v)
		
	def apply_or(self, u, v):
		return self._bdd.bdd_or(u,v)
	
	def apply_ite(self, u, v, w):
		return self._bdd.bdd_ite(u,v,w)

	def apply(self, op, u, v = None, w = None):
		if op in ('~', 'not', 'NOT', '!'):
			return self._bdd.bdd_not(u)
		elif op in ('or', 'OR', r'\/', '|', '||'):
			return self._bdd.bdd_or(u, v)
		elif op in ('and', 'AND', '/\\', '&', '&&'):
			return self._bdd.bdd_and(u, v)
		elif op in ('nand', 'NAND'):
			return self._bdd.bdd_not(self._bdd.bdd_and(u, v))
		elif op in ('xor', 'XOR', '^'):
			return self._bdd.bdd_xor(u, v)
		elif op in ('=>', '->', 'implies'):
			return self._bdd.bdd_imp(u, v)
		elif op in ('<=>', '<->', 'equiv'):
			return self._bdd.bdd_biimp(u, v)
		elif op in ('diff', '-'):
			return self._bdd.bdd_ite(u, self._bdd.bdd_not(u), self.false)
		elif op in ('ite', 'ITE'):
			return self.ite(u, v, w)
		else:
			raise Exception(f'unknown operator "{op}"')

	### reference counting and garbage collection
	def incref(self, u):
		return self._bdd.bdd_addref(u)

	def decref(self, u):
		return self._bdd.bdd_delref(u)

	def dump(self, u=None, filename="out.bdd"):
		tempf = filename+".tmp"
		if filename[-3:] == "dot":
			self._bdd.bdd_fnprintdot(c_char_p(filename.encode("UTF-8")), u)
		elif filename[-3:] == "pdf":
			self._bdd.bdd_fnprintdot(c_char_p(tempf.encode("UTF-8")), u)
			os.system(f"dot -Tpdf {tempf} > {filename}")
			os.remove(tempf)
		else:
			self._bdd.bdd_fnsave(c_char_p(filename.encode("UTF-8")), u)
			with open(filename+"v", "w") as f:
				for i in range(len(self.var_dict)):
					f.write(f"{self.var_dict[i]}\n")
				f.close()
	
	### input and output functionalities
	def visualize(
		self, 
		u=None, 
		vizname="viz", 
		# Note: no http://
		host="127.0.0.1:8080" #=localhost:8080 but is faster
	):
		tempf = vizname+".tmp"
		self._bdd.bdd_fnsave(c_char_p(tempf.encode("UTF-8")), u)
		with open(tempf, "r") as f:
			diagram = f.read().strip()
			vars = ""
			for i in range(len(self.var_dict)):
				vars += f"{self.var_dict[i]}\n"

			send_request(
				host, 
				"POST", 
				f'/api/buddy-diagram?name={vizname}&type=BDD',
				{
					"data": diagram,
					"vars": vars
				})
		os.remove(tempf)

	def remove_visualization(
		self,
		vizname,
		# Note: no http://
		host="127.0.0.1:8080" #=localhost:8080 but is faster
	): 
		send_request(
			host, 
			"DELETE", 
			f'/api/diagram?name={vizname}',
			{})

	def load(self, filename="in.bdd"):
		root = c_int()
		self._bdd.bdd_fnload(c_char_p(filename.encode("UTF-8")), byref(root))
		# TODO: also read variable names
		self.incref(root.value)
		return root.value

### helper functions
def send_request(host, kind, path, data):
	try:
		conn = http.client.HTTPConnection(host)
		body = json.dumps(data)
		conn.request(kind, path, body=body, headers={
			'Content-type': 'application/json'
		})
		conn.close()
	except Exception as e:
		print("Unable to perform request, is the visualization tool running?")
		raise e