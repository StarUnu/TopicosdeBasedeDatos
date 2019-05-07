import numpy as np
class nodo:
	def __init__(self,ini_array,name):
		self.array_hash=ini_array # es la lista con los puntajes
		self.nombre=name
		
		self.suma_ptj=np.sum(ini_array)

	def get_suma_ptj(self):
		return self.suma_ptj;

	def get_array_hash(self):
		return self.array_hash;
	
	def get_nombre(self):
		return self.nombre;