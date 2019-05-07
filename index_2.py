from tkinter import *
from backup6_36ejecutable import *

window = Tk()

window.title("Sistema de Recomendación")
window.geometry('900x900')

lbl = Label(window, text="Sistema de Recomendación\n", fg="red", font=("Arial Bold", 20 ,"bold"))
lbl.grid(column=1, row=0)

img = PhotoImage(file="pelicula_pq.png")
lb_img = Label(window, image=img, relief=RAISED)
lb_img.grid(column=1, row=1)
#lb_img.pack()
lbl2 = Label(window, text="Cantidad de Data: \n", font=("Arial Bold", 12 ,"bold"))
lbl2.grid(column=0, row=2)

selected = IntVar()

rad1 = Radiobutton(window,text='10 Millones', value=1, variable=selected)

rad2 = Radiobutton(window,text='20 Millones', value=2, variable=selected)

rad3 = Radiobutton(window,text='27 Millones', value=3, variable=selected)

""" def clicked():

   print(selected.get())

btn = Button(window, text="Click Me", command=clicked) """

rad1.grid(column=0, row=3)

rad2.grid(column=1, row=3)

rad3.grid(column=2, row=3)

def clicked_cargar():
   i = selected.get()
   t = CargaData(i)

   if(i == 1):
      res = "Se cargo 10 millones "
   if(i == 2):
      res = "Se cargo 20 millones "
   if(i == 3):
      res = "Se cargo 27 millones "
   print(selected.get())

   
   lbl3.configure(text= res+" en "+str(t))



img_cargar = PhotoImage(file="upload_pq.png") 
btn = Button(window, text="Cargar Data", command=clicked_cargar, font=("Arial Bold", 12,"bold"), image=img_cargar, compound=LEFT)
 
btn.grid(column=4, row=3)

lbl3 = Label(window, fg="blue", font=("Arial Bold", 12))
lbl3.grid(column=1, row=4)


lbl4 = Label(window, text="Usuario:\n", font=("Arial Bold", 12,"bold"))
lbl4.grid(column=0, row=5)

txt = Entry(window,width=30)
txt.grid(column=1, row=5)

lblTipoDis = Label(window, text="Tipo de Distancia", font=("Arial Bold", 12,"bold"))
lblTipoDis.grid(column=0, row=6)

selTipoDis = IntVar()

radTipoDis1 = Radiobutton(window,text='Pearson', value=1, variable=selTipoDis)

radTipoDis2 = Radiobutton(window,text='Coseno', value=2, variable=selTipoDis)

radTipoDis3 = Radiobutton(window,text='Euclediana', value=3, variable=selTipoDis)

""" def clicked():

   print(selected.get())

btn = Button(window, text="Click Me", command=clicked) """

radTipoDis1.grid(column=0, row=7)

radTipoDis2.grid(column=1, row=7)

radTipoDis3.grid(column=2, row=7)

def clicked_recomendar():
   tipDis = selTipoDis.get()
   print("Tipo de Dis",tipDis)
   resultado_dic = ConsultaData(txt.get(), tipDis)
   
   print("resultaador",resultado_dic)
   var = 1
   for name in resultado_dic:
      string = name[0] + str(name[1])
      print(string)
      lisb.insert(var,string)
      var= var+1
   #res = suma(2,6)
 
    #res = "Welcome to " + txt.get()
 
   #lbl.configure(text= res)
   
img_find = PhotoImage(file="findPeq.png") 
btn = Button(window, text="Recomendar", command=clicked_recomendar, font=("Arial Bold", 12,"bold"), image=img_find, compound=LEFT)
 
btn.grid(column=4, row=8)




lbl5 = Label(window, text="Peliculas:\n", font=("Arial Bold", 12 ,"bold"))
lbl5.grid(column=0, row=8)

scrollbar = Scrollbar(window)
lisb = Listbox(window, width=50, bg="#000", fg="#fff", height=30,yscrollcommand=scrollbar.set) 
 
""" Lisb.insert(2, 'Java') 
Lisb.insert(3, 'C++') 
Lisb.insert(4, 'Any other') """
lisb.grid(column=1, row=9)


window.mainloop()

