import numpy as np
import math
from math import sqrt

import time

def hash(nombre,tam_hash):
	c=0
	suma=0
	while c<len(nombre)	:
		suma=suma+ord(nombre[c])
		c+=1
	#print("suma",suma)
	return suma%tam_hash


#solo por que las ids de las peliculas son ordenadas
##los arreglos_# son los id de las peliculas y los data_a# son las preferencias 
def iguales_indices(arreglo_1,arreglo_2,data_a1,data_a2):
	indice_a1=0
	indice_a2=0
	indice_r=0
	resultado=[]
	matriz_estatico=[]
	rating_a1=[]
	rating_a2=[]
	diferentes=[]#peliculas
	diferentes_prefe=[]
	i=0
	while indice_a1<len(arreglo_1) and indice_a2<len(arreglo_2):
		if arreglo_1[indice_a1]==arreglo_2[indice_a2]:
			resultado.append(arreglo_2[indice_a2])
			rating_a1.append(data_a1[indice_a1])
			rating_a2.append(data_a2[indice_a2])
			indice_r+=1
			indice_a2+=1
		else:
			if arreglo_1[indice_a1]<arreglo_2[indice_a2]:
				#diferentes.append(arreglo_1[indice_a1])
				indice_a1+=1
			else:
				diferentes_prefe.append(data_a2[indice_a2])
				diferentes.append(arreglo_2[indice_a2])
				indice_a2+=1
		i+=1
	rating_a1=np.array(rating_a1)
	rating_a2=np.array(rating_a2)
	return resultado,rating_a1,rating_a2,diferentes,diferentes_prefe

class  recomendacion():
	def __init__(self,caracteristica,tamano_array_ptj):
		print("tu puedes deberas")
		self.a_caracteristica=caracteristica
		self.tam_array_ptj=tamano_array_ptj

	def manhathan(self,array_hash,array_b):
		var=0
		sumaT=0
		while var<len(array_b):
			if array_b[var]!=-1 and array_hash[var]!=-1:
				sumaT=sumaT +abs(array_hash[var]-array_b[var])
			var+=1
		#print("resultado de manhathan",sumaT)
		return sumaT

	def Euclidiana(self,array_hash,array_b):
		var=0
		sumaT=0
		while var<len(array_b):
			if array_b[var]!=-1 and array_hash[var]!=-1:
				sumaT=sumaT +(array_hash[var]-array_b[var])**2
			var+=1
		sumaT=sumaT**(1.0/2)
		#print("resultado de Euclidiana",sumaT)
		return sumaT

	#esto es generealizado
	def Minkowaki(self,array_hash,array_b,tam_caracterisitica):
		var=0
		sumaT=0
		if tam_caracterisitica<=0:
			tam_caracterisitica=1


		while var<len(array_b):
			if array_b[var]!=-1 and array_hash[var]!=-1:
				sumaT=sumaT +(abs(array_hash[var]-array_b[var]))**tam_caracterisitica

			var+=1
		sumaT=sumaT**(1.0/tam_caracterisitica)
		#print("resultado con Minkowaki",sumaT)
		return sumaT

	def pearson(self,array_hash,array_op):
		
		'''x=[]
		y=[]
		var=0
		while var<len(array_op):
			if array_op[var]!=-1 and array_hash[var]!=-1:
				x.append(array_hash[var])
				y.append(array_op[var])
			#else:
			#	print("es un uno :",array_op[var] , array_hash[var])
			var+=1
		x=np.array(x)
		y=np.array(y)'''
		x=array_hash
		y=array_op

		n=len(x)	
		suma_x=np.sum(x)
		suma_y=np.sum(y)

		#print("multiplicar",np.sum(x*y))
		numerador= np.sum(x*y)-((suma_x*suma_y)/n)
		primer_raiz=sqrt(np.sum(x**2)-(suma_x**2/n))
		segunda_raiz=sqrt(np.sum(y**2)-(suma_y**2/n))
		denominador=primer_raiz*segunda_raiz
		#print("numerador",numerador)
		#print("primer_raiz",primer_raiz)
		#print("denominador",denominador)
		
		if numerador==0 or denominador==0:
			#print("esto es el tamano",len(array_hash) )	
			return self.Minkowaki(array_hash,array_op,len(array_hash)-1)
		r=numerador/denominador
		#print("r",r)
		
		#print("tu puedes erika",np.sum(array_op))
		#print("numerador",numerador)
		#print("denominador",denominador)
		#print("coeficiente de pearson",r)
		return abs(r);

	def coseno(self,array_hash,array_op):
		
		x=[]
		y=[]
		var=0
		while var<len(array_op):
			if array_op[var]==-1 :
				y.append(0)
			if array_hash[var]==-1:
				x.append(0)
			if array_op[var]!=-1 :
				y.append(array_op[var])
			if array_hash[var]!=-1:
				x.append(array_hash[var])
			var+=1
		x=np.array(x)
		y=np.array(y)
		n=len(x)+0.0	
		denominador=( sqrt(np.sum(x**2))*(sqrt(np.sum(y**2))) )
		if denominador<=0:
			self.Euclidiana(array_hash,array_op)
		cos=np.sum(x*y)/denominador
		#print("Distancia mediante coeficiente de coseno",cos)
		return cos;

	def k_vecinos_mascercanos(self,user_item,rating,movies_table,users,movies,indice_movies,title_movies,userid_recomen,k_vecino,funcion):
		tiempo_ini = time.time();
		userid_recomen=userid_recomen
		#userid_recomen=283228
		#k_vecino=8
		dic_caracteristica={}
		tam_hash=12

		#sacando item iguales  con sus ratings	

		#rec_principal=recomendacion(dic_caracteristica,tam_hash)
		if userid_recomen==len(users):
			userid_recomen=userid_recomen-1
		indices1=user_item[userid_recomen].indices##poner el numero de usuario al que se le quiere aconsejar
		dist_menor=100000000000000000000
		conta=2
		dista_menores=[]
		diferentes_ini=movies
		matriz_diferentes=[]
		matriz_preferencia_nv=[]
		#aqui seria bueno paralelizar el procesamiento de la cantidad de usuar
		dic_caracteristica={}
		tam_hash=12
		#recomendacion=recomendacion(dic_caracteristica,tam_hash)

		while conta<len(users):
			if conta!= userid_recomen:
				indices2=user_item[conta].indices
				#peliculas que son iguales y que tiene calificacion

				resultado,rating_a1,rating_a2,diferentes,diferentes_prefe=iguales_indices(indices1,indices2,user_item[userid_recomen].data,user_item[conta].data)	
				distancia=self.coseno(rating_a1,rating_a2)

				if dist_menor>=distancia and len(diferentes)>0:
					dist_menor=distancia
					dista_menores.append(conta)	#posicion de los usuarios menores
					matriz_diferentes.append(diferentes)
					matriz_preferencia_nv.append(diferentes_prefe)
			conta+=1
		if len(dista_menores)>k_vecino :
			print("usuarios más cercanos",dista_menores[len(dista_menores)-k_vecino:])
		print("distancia menores",dista_menores)
		tiempo_fin = time.time()
		diferencia_time=(tiempo_fin-tiempo_ini)/1000
		print("Tiempo en milisegundos procedimiento "+str(diferencia_time))
		return dista_menores

	def recomendacion_versionmillon(self,user_item,rating,movies_table,users,movies,indice_movies,title_movies,userid_recomen,k_vecino,funcion):
		userid_recomen=userid_recomen
		indices1=user_item[userid_recomen].indices##poner el numero de usuario al que se le quiere aconsejar

		dist_menor=100000000000000000000
		conta=2
		dista_menores=[]
		diferentes_ini=movies
		matriz_diferentes=[]
		matriz_preferencia_nv=[]
		#aqui seria bueno paralelizar el procesamiento de la cantidad de usuar
		dic_caracteristica={}
		tam_hash=12
		#recomendacion=recomendacion(dic_caracteristica,tam_hash)

		while conta<len(users):
			if conta!= userid_recomen:
				indices2=user_item[conta].indices
				#peliculas que son iguales y que tiene calificacion
				resultado,rating_a1,rating_a2,diferentes,diferentes_prefe=iguales_indices(indices1,indices2,user_item[1].data,user_item[conta].data)	

				distancia=funcion(rating_a1,rating_a2)

				if dist_menor>distancia and len(diferentes)>0:
					dist_menor=distancia
					dista_menores.append(conta)	#posicion de los usuarios menores
					matriz_diferentes.append(diferentes)
					matriz_preferencia_nv.append(diferentes_prefe)
			conta+=1


		## el  50% es encontrada
		conta=len(dista_menores)-1
		#canti_k=len(dista_menores)-k_vecino
		promedio_ini=np.full(len(movies),0)
		print("peliculas recomendacion")
		diferentes_ini=[]
		#diferentes_ini=matriz_diferentes[dista_menores[conta]]
		#conta=conta-1

		#tan solo a dos usuarios
		anterior_pr=[]
		#los kvecinoss
		#title_movies=matriz_diferentes[]
		#canti_k=2
		#while conta>canti_k:
		if conta==len(dista_menores)-1:
			diferentes=matriz_diferentes[conta]
			print("primer paso",diferentes)
			anterior_pr=matriz_preferencia_nv[conta]
		else:
			#ids de las peliculas 
			temp_diferentes=set(diferentes) & set( matriz_diferentes[conta] )
			#if len(temp_diferentes)==0:
			#	break;
			diferentes = temp_diferentes
			#print("diferentes",i)
			count_cmp=0
			count_md=0
			#promedio=np.full(len(diferentes),0)
			minimo=len(diferentes)
			diferentes=list(diferentes)
			while count_cmp<minimo and count_md<len(matriz_diferentes[conta]) :
				if matriz_diferentes[conta][count_md]==diferentes[count_cmp]:
					#promedio[count_cmp]=promedio[count_cmp]+matriz_preferencia_nv[conta][count_md]
					#promedio[count_cmp]=anterior_pr[count_cmp]+matriz_preferencia_nv[conta][count_md]
					anterior_pr[count_cmp]=anterior_pr[count_cmp]+matriz_preferencia_nv[conta][count_md]
					print("esto es el numero ",anterior_pr )
					count_cmp+=1
				count_md+=1
			#print(promedio)
			#break
		diferentes_ini=diferentes
		conta-=1

		#diferentes=list(diferentes)

		#promedio=[elemento for elemento in anterior_pr if elemento !=0]

		indices1=matriz_diferentes[len(dista_menores)-1:][0]
		canti_k=2
		diccionario={}
		conta=0
		for elemento in indices1:
			temp_indice=elemento
			while indice_movies[temp_indice]!=elemento:	
				temp_indice=temp_indice-1
			if temp_indice>=0:
				diccionario[title_movies[temp_indice] ]=anterior_pr[conta]/canti_k
			conta+=1
			##respuesta imprimir en ventana
		diccionario=sorted(diccionario.items(), key=lambda k: k[1],reverse=True)
		for item in diccionario:
			print(item)
		print("termino por aca ",diccionario)
		return diccionario	
	#distancia de dos personas
	def distancia(self,name1,name2,array_hash,tam_hash,funcion):
		#encontrar el primer name1
		print("Distancia hacia nombre = "+name1+" otro nombre2= "+name2)
		indicea=hash(name1,tam_hash);
		while array_hash[indicea].get_nombre()!=name1:
			indicea+=1;
			if indicea==tam_hash:
				indicea=0

		#encontrar el primer name2
		indiceb=hash(name2,tam_hash);
		while array_hash[indiceb].get_nombre()!= name2:
			indiceb+=1;
			if indiceb==tam_hash:
				indiceb=0

		#print("array",array_hash[indicea].get_array_hash())
		#print("array",array_hash[indiceb].get_array_hash())
		try:
			funcion(array_hash[indicea].get_array_hash(),array_hash[indiceb].get_array_hash())
		except Exception as e:	
			funcion(array_hash[indicea].get_array_hash(),array_hash[indiceb].get_array_hash(),2)
		

	

	#la musica es a donde quiere recomendar
	#devuelve los vecinos más cercanos hacia un array con su puntos  con la puntuacion a cada item 
	#y la catidad de similitud
	def vecinomascercano_k(self,indice_name,k,array_hash,tam_hash,musica):
		#encontrar el primer name1
		var=0
		#diccionario
		distancia_user={}
		##verificar si tiene ptj la musica
		indice_musica=self.a_caracteristica[musica]
		##aca comparon con tra todos
		sumatoria_distancia=0
		while var<tam_hash:
			if indice_name!=var:

				y=array_hash[indice_name].get_array_hash()
				x=array_hash[var].get_array_hash()
				distancia=self.pearson(y,x)
				sumatoria_distancia=sumatoria_distancia+distancia
				#print("sumatoriasdeberas",sumatoria_distancia)
				##verificar si tiene ptj la musica
				if  x[indice_musica]!=-1 :
					distancia_user[ array_hash[var].get_nombre() ]=[distancia,x[indice_musica],array_hash[var].get_array_hash()]

			var+=1

		#ordenacion mediante landas , con key=lambda k: k[1][0] esto quiere decir que 
		#de acuerdo a la distancia se va a ordenar , primero entra al segundo valor y desde de este al primero
		sumatoria_puntaje_v=0

		resultado = sorted(distancia_user.items(), key=lambda k: k[1][0],reverse=True)
		#print("RESULTADO",resultado)
		#print("que es esto ",distancia_user.items())		
		var=0
		distancia_minima=[]
		#print("esto es la sumatoria de las distancias",sumatoria_distancia)
		sumatoria=0.0
		for nombre in resultado:
			if var==k:
				break;
			sumatoria_puntaje_v=np.sum(nombre[1][2])/len(nombre[1][2])
			#print("promedio",sumatoria_puntaje_v)
			distancia_minima.append([nombre,nombre[1][0],nombre[1][1],sumatoria_puntaje_v ])
			sumatoria+=nombre[1][0]
			var+=1
		#print("deberia se ser ordenados",distancia_minima)
		#print("sumatoria",sumatoria)
		return sumatoria,distancia_minima


	def obtener_array(self,name,array_hash):
		tam_hash=len(array_hash)
		indicea=hash(name,tam_hash);
		while array_hash[indicea].get_nombre()!=name:
			indicea+=1;
			if indicea==tam_hash:
				indicea=0
		return indicea

	def influencia_amigos(self,name,k,array_hash,tam_hash,musica):
		indice_name=self.obtener_array(name,array_hash)
		print("esta es la influencia de amigos \n")

		sumatoria,dist_minima=self.vecinomascercano_k(indice_name,k,array_hash,tam_hash,musica)

		promedio_ptj_u=array_hash[indice_name].get_suma_ptj()/self.tam_array_ptj

		porcentaje_proyec=promedio_ptj_u
		#print("promedio",porcentaje_proyec)
		var=0
		while var <k:
			#print("esto es el nombre",dist_minima[var][0])
			dist_pearson=dist_minima[var][1]

			ptj_musica=dist_minima[var][2]
			promedio_ptj_v=dist_minima[var][3]
			#print("PORCENTAJE otro",dist_pearson/ptj_musica)
			grd_influ=dist_pearson/sumatoria #grado de influencia

			#print("grado de influencia",grd_influ)
			#print("grado de influencia",grd_influ*(100)*ptj_musica)
			porcentaje_proyec+=dist_pearson*(ptj_musica-promedio_ptj_v)
			#print("PORCENTAJE PROYECTO",porcentaje_proyec)
			var+=1
		porcentaje_proyec=porcentaje_proyec/sumatoria

		print("porcentaje proyectado para el item="+musica+",con  k="+str(k)+",salio="+str(porcentaje_proyec))


	def distancia_uno_todos(self,indice_name,array_hash,funcion,k):
		###ecncontrando name
		#indicea=hash(name,tam_hash);
		#while array_hash[indicea].get_nombre()!=name:
		#	indicea+=1;
		#	if indicea==tam_hash:
		#		indicea=0


		#distancia_minima=self.vecinomascercano_k_TaU(indice_name,k,array_hash,tam_hash,funcion)
		tam_hash=len(array_hash)
		var=0
		distancia_user={}
		while var<tam_hash:
			if indice_name!=var:
				y=array_hash[indice_name].get_array_hash()
				x=array_hash[var].get_array_hash()
				#print("x",x)	
				##verificar si tiene ptj la musica
				if  x[indice_name]!=-1 and y[indice_name]!=-1:
					distancia=math.fabs(self.pearson(y,x))
					distancia_user[ array_hash[var].get_nombre() ]=[distancia,x]
			var+=1
		#ordenacion mediante landas , con key=lambda k: k[1][0] esto quiere decir que 
		#de acuerdo a la distancia se va a ordenar , primero entra al segundo valor y desde de este al primero
		print("ESTO ES ",distancia_user)
		resultado = sorted(distancia_user.items(), key=lambda k: k[1][0],reverse=True)

		
		#print("DDDistancia",distancia_minima[var][0])
		var=0
		while var<k :
			print ("A {} = {}".format(resultado[var][0],resultado[var][1]) )
			var+=1

	#dista desde uno hacia todos los usuarios
	def vecinomascercano_k_TaU(self,indicea,k,array_hash,tam_hash,funcion):
		#encontrar el primer name
		var=0
		#diccionario
		distancia_user={}		
		while var<tam_hash:
			if indicea!=var:
				x=array_hash[var].get_array_hash()
				y=array_hash[indicea].get_array_hash()
				try:
					distancia=funcion(y,x)
				except Exception as e:
					distancia=funcion(y,x,2)

				distancia_user[ array_hash[var].get_nombre() ]=[distancia]
			var+=1
		#ordenacion mediante landas , con key=lambda k: k[1][0] esto quiere decir que 
		#de acuerdo a la distancia se va a ordenar , primero entra al segundo valor y desde de este al primero
		resultado = sorted(distancia_user.items(), key=lambda k: k[1][0],reverse=True)
		#print("que es esto ",distancia_user.items())		
		var=0
		distancia_minima=[] #al momentode meterlo en el diccionarios tambien lo pone
		for nombre in resultado:
			#print (distancia_minima)
			if var==k:
				break;
			distancia_minima.append([nombre[0],nombre[1][0]])
			var+=1
		#distancia_minima = sorted(distancia_minima.items(), key=lambda k: k[1][0],reverse=False)
		return distancia_minima

	##recomendar una pelicula a alguien
	def recomendar_a_alguien(self,name,k,array_hash,tam_hash,umbral):
		#encontrar el primer name1

		indicea=hash(name,tam_hash);
		while array_hash[indicea].get_nombre()!=name:
			indicea+=1;
			if indicea==tam_hash:
				indicea=0

		var=0
		#diccionario
		distancia_user={}
		while var<tam_hash:
			if indicea!=var:
				y=array_hash[indicea].get_array_hash()
				x=array_hash[var].get_array_hash()
				#print("x",x)	
				##verificar si tiene ptj la musica
				if  x[indice]!=-1 and y[indice]!=-1:
					distancia=math.fabs(recomendacion.pearson(y,x))
					distancia_user[ array_hash[var].get_nombre() ]=[distancia,x]
			var+=1
		#ordenacion mediante landas , con key=lambda k: k[1][0] esto quiere decir que 
		#de acuerdo a la distancia se va a ordenar , primero entra al segundo valor y desde de este al primero
		print("ESTO ES ",distancia_user)
		resultado = sorted(distancia_user.items(), key=lambda k: k[1][0],reverse=True)
		
		print("ESTO ES ",resultado)
		var=0
		distancia_minima=[]
		tamano_carac=len(self.a_caracteristica)

		suma_arreglos=np.full(tamano_carac,0) ;
		print("esto SUMA ARREGLOS",suma_arreglos)
		array_mayor_peli=[]
		sumatoria=0.0
		for nombre in resultado:
			if var==k:
				break;
			var2=0
			suma_num=0
			suma_arreglos=suma_arreglos+nombre[1][1]
			while var2<tamano_carac:
				if (nombre[1][1][var2]!=-1):
					suma_arreglos[var2]+= nombre[1][1][var2]
				var2+=1
			
			distancia_minima.append(nombre)
			sumatoria+=nombre[1][0]
			var+=1
		suma_arreglos=suma_arreglos/tamano_carac
		var3=-1
		indice_carac=0
		string_name=""
		max_num=-0.00000000000000000000000000000000001
		for name in self.a_caracteristica:
			if suma_arreglos[var3]>max_num:
				max_num=suma_arreglos[var3]
				indice_carac=var3
				string_name=name
			var3+=1

		return sumatoria,distancia_minima
