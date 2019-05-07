def recomendacion_versionmillon(self,user_item,rating,movies_table,users,movies,indice_movies,title_movies,userid_recomen,k_vecino,funcion):
		indices1=user_item[userid_recomen].indices##poner el numero de usuario al que se le quiere aconsejar
		dist_menor=100000000000000000000
		conta=2
		dista_menores=[]
		diferentes_ini=movies
		matriz_diferentes=[]
		matriz_preferencia_nv=[]
		#aqui seria bueno paralelizar el procesamiento de la cantidad de usuar
		while conta<len(users):
			indices2=user_item[conta].indices

			#peliculas que son iguales y que tiene calificacion
			resultado,rating_a1,rating_a2,diferentes,diferentes_prefe=iguales_indices(indices1,indices2,user_item[1].data,user_item[conta].data)	

			distancia=funcion(rating_a1,rating_a2)
			if dist_menor>distancia:
				dist_menor=distancia
				dista_menores.append(conta)	#posicion de los usuarios menores
				matriz_diferentes.append(diferentes)
				matriz_preferencia_nv.append(diferentes_prefe)
			conta+=1


		## el  50% es encontrada
		conta=len(dista_menores)-1
		canti_k=len(dista_menores)-k_vecino
		promedio_ini=np.full(len(movies),0)
		print("peliculas recomendacion")
		diferentes_ini=[]
		#diferentes_ini=matriz_diferentes[dista_menores[conta]]
		#conta=conta-1

		#tan solo a dos usuarios
		anterior_pr=[]
		#los kvecinoss
		canti_k=2
		while conta>canti_k:
			if conta==len(dista_menores)-1:
				diferentes=matriz_diferentes[conta]
				print("primer paso",diferentes)
				anterior_pr=matriz_preferencia_nv[conta]
			else:
				#ids de las peliculas 
				temp_diferentes=set(diferentes) & set( matriz_diferentes[conta] )
				if len(temp_diferentes)==0:
					break;
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
				diferentes_ini=diferentes
			conta-=1

		#diferentes=list(diferentes)
		
		#promedio=[elemento for elemento in anterior_pr if elemento !=0]
		
		indices1=matriz_diferentes[len(dista_menores)-1]
		diccionario={}
		conta=0
		for elemento in indices1:
			temp_indice=elemento
			while indice_movies[temp_indice]!=elemento:	
				temp_indice=temp_indice-1
			diccionario[title_movies[temp_indice] ]=anterior_pr[conta]/canti_k
			conta+=1
			##respuesta imprimir en ventana
		diccionario=sorted(diccionario.items(), key=lambda k: k[1],reverse=True)
		for item in diccionario:
			print(item)
		print("termino por aca ",diccionario)
		return diccionario
