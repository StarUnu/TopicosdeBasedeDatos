from math import sqrt
import numpy as np
import operator

import pandas as pd
import csv
from  nodo import *
from backup6_36_recomendacion import *
import scipy.sparse as sparse
import datetime

#from mpi4py import MPI

import time


def hash(nombre,tam_hash):
	c=0
	suma=0
	while c<len(nombre)	:
		suma=suma+ord(nombre[c])
		c+=1
	#print("suma",suma)
	return suma%tam_hash

#comm = MPI.COMM_WORLD
#rank = comm.Get_rank()

def maximo(arreglo1,arreglo2):
	if len(arreglo1)<=len(arreglo2):
		return arreglo2
	return arreglo1



"""print("0:Cargar base de datos del libro")
print("1:Cargar base de datos movilans profesora 51 datos")
print("2:Cargar base de datos movilans tradicional 1 millon ")
print("3:Cargar base de datos movilans tradicional 20 millon")
print("4:Cargar base de datos movilans tradicional 27 millon")
"""
##a = int(input("Elija la opcion:"))


def CargaData(opcion):
	global movies_table, ratings, users, rating, movies
	global title_movies, indice_movies, user_item

	a = opcion
	tiempo_ini = time.time()

	if a==0:#esto es la base de datosdel libro
		dic_caracteristica={}
		usuarios=["Angelica","Bill","Chan","Den","Hailey","Jordyn","Sam","Veronica"]
		matriz_estatico=[]
		arreglo_Angelica=[3.5,2,-1,4.5,5,1.5,2.5,2]
		arreglo_Bill=    [2,3.5,4,-1,2,3.5,-1,3]
		arreglo_Chan=    [5,1,1,3,5,1,-1,-1]
		arreglo_Den=     [3,4,4.5,-1,3,4.5,4,2]
		arreglo_Hailey=  [-1,4,1,4,-1,-1,4,1]
		arreglo_Yordyn=  [-1,4.5,4,5,5,4.5,4,4]
		arreglo_Sam=     [5,2,-1,3,5,4,5,-1]
		arreglo_Veronica=[3,-1,-1,5,4,2.5,3,-1]
		matriz_estatico.append(arreglo_Angelica)
		matriz_estatico.append(arreglo_Bill)
		matriz_estatico.append(arreglo_Chan)
		matriz_estatico.append(arreglo_Den)
		matriz_estatico.append(arreglo_Hailey)
		matriz_estatico.append(arreglo_Yordyn)
		matriz_estatico.append(arreglo_Sam)
		matriz_estatico.append(arreglo_Veronica)

		caracteristica=['Blue Traveler','Broken Bells','Daedmons','Norehm Jones','Phonix','Sligtly','The Strones','Vampire']
	if a==1:
		ratings = pd.read_csv("Data/ml-10millones/ratings.dat",sep="::")
		movies_table = pd.read_csv("Data/ml-10millones/movies.dat",sep="::")
	if a==2:
		#user=int(input("Elija usuario:"))
		## solo cuando es data de 10 millones
		ratings = pd.read_csv("/home/erika/Documentos/TopicosBasedeDatos/presentacion1/programa/Data/ml-20millones/ratings.csv",sep=",")
		movies_table = pd.read_csv("/home/erika/Documentos/TopicosBasedeDatos/presentacion1/programa/Data/ml-20millones/movies.csv",sep=",")
	if a==3:
		ratings = pd.read_csv("/home/erika/Documentos/TopicosBasedeDatos/presentacion1/programa/Data/ml-27millones/ratings.csv",sep=",")
		movies_table = pd.read_csv("/home/erika/Documentos/TopicosBasedeDatos/presentacion1/programa/Data/ml-27millones/movies.csv",sep=",")

	
	#ratings = ratings[["userId", "movieId", "rating"]]
	users = list(np.sort(ratings.userId.unique())) # Get our unique customers
	rating = list(ratings.rating)
	movies = list(ratings.movieId.unique())

	#ratings.movieId.astype('category', categories = title_movies).cat.codes
	#esto lo ordena de tal manera por orden alfabetico y ponen a cada elementos un numero
	#si en  vez de numeros hay string se usaria esto
	#rows=ratings.userId.astype('category', categories = users).cat.codes
	#cols = ratings.movieId.astype('category', categories = movies).cat.codes
	#user_item.toarray()
	user_item = sparse.csr_matrix((rating, (ratings.userId,ratings.movieId)))
	
	###para sacar de una pelicula un indice se hace lo siguiente
	##tendria problemas si los id_movies se repitieran
	title_movies=list(movies_table.title)
	indice_movies=list(movies_table.movieId)

	tiempo_fin = time.time() # tiempo en segundo
	tiempo_total = (tiempo_fin-tiempo_ini)/1000
	print("Tiempo en minutos de Cargar la Data ==> "+str(tiempo_total))
	
	return tiempo_total

def ConsultaData(id_user, tip_dis):
	print(tip_dis)
	tiempo_ini = time.time()
	dic_caracteristica={}		

	
	'''a=user_item.indices
	
	temp_indice=a[30]
	while indice_movies[temp_indice]!=a[30]:	
		temp_indice=temp_indice-1
	print(title_movies[temp_indice])'''

	#####################
	dic_caracteristica={}
	tam_hash=12
	
	#sacando item iguales  con sus ratings	

	rec_principal=recomendacion(dic_caracteristica,tam_hash)
	userid_recomen = id_user
	k_vecino=2
	diccionario=0
	if(tip_dis==1):# Pearson
		diccionario=rec_principal.recomendacion_versionmillon(user_item,rating,movies_table,users,movies,indice_movies,title_movies,userid_recomen,k_vecino,rec_principal.pearson)
	if(tip_dis==2):#coseno
		diccionario=rec_principal.recomendacion_versionmillon(user_item,rating,movies_table,users,movies,indice_movies,title_movies,userid_recomen,k_vecino,rec_principal.coseno)
	if(tip_dis==3):#euclediana
		diccionario=rec_principal.recomendacion_versionmillon(user_item,rating,movies_table,users,movies,indice_movies,title_movies,userid_recomen,k_vecino,rec_principal.Euclidiana)
		

	tiempo_fin = time.time() # tiempo en segundos 
	print("Tiempo en milisegundos en cargar los datos "+str(tiempo_fin.second-tiempo_ini.second))

	return diccionario

CargaData(3)
#recomendacion=recomendacion(cos,)
#ConsultaData(16006,1)
userid_recomen=4598;
k_vecino=10;

dic_caracteristica={};
tam_hash=12;
	#sacando item iguales  con sus ratings	

rec_principal=recomendacion(dic_caracteristica,tam_hash)
rec_principal.k_vecinos_mascercanos(user_item,rating,movies_table,users,movies,indice_movies,title_movies,userid_recomen,k_vecino,rec_principal.pearson)

#rec_principal.k_vecinos_mascercanos(user_item,rating,movies_table,users,movies,indice_movies,title_movies,userid_recomen,k_vecino,rec_principal.pearson)
