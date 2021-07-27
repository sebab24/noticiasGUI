#INSTALACION LIBRERIAS
#   sudo apt-get install python3-tk         #para python3 
#   sudo apt-get install python-tk          #para python2 
#   sudo apt install python-pip3
#   sudo pip3 install SpeechRecognition
#   sudo apt-get install python-pyaudio python3-pyaudio
#   sudo apt install sshpass
#   sudo pip3 install sox     #reproduce sonidos
#	sudo apt install libsox-fmt-all   # para reproducir mp3 y *
#	pip install lxml    # modificador para scrapear webs
#	sudo apt-get install fonts-symbola     #instalar font para evitar caida al pegar texto en marco
 
#from scrapeNOTICIAS import SCRAPENOTICIAS

#from scrapegetTEXTO import 	EXTRAETEXTO

import requests
from bs4 import BeautifulSoup

from datetime import date
from datetime import datetime
import time
import webbrowser



#from TTS4 import leervoz

today = date.today()

import sys

import os, subprocess
#import speech_recognition as sr
import numpy as np
import threading


global carpeta
carpeta =  os.getcwd()
carpeta+='/'




#--------------GUI--------------

from tkinter import *
import tkinter as Tkinter
from tkinter import ttk




#VENTANA PRINCIPAL.
root = Tkinter.Tk()
root.title("LECTOR DE NOTICIAS V.2")
root.geometry("1000x650")
root.configure(bg="light blue", bd=5)
#root.configure(bg='light green', bd=5)


#PANEL PESTANAS
nb = ttk.Notebook(root)
#nb.configure(bg="ligth blue", bd=5)
nb.pack(fill='both',expand='yes')


#PESTANAS
p1 = ttk.Frame(nb)
#p1.configure(bg="light blue", bd=5)
p2 = ttk.Frame(nb)
#p3 = ttk.Frame(nb)
#p4 = ttk.Frame(nb)

#TITULO PESTANAS 
nb.add(p1,text='URLs')
nb.add(p2,text='TITULARES')
#nb.add(p3,text='TEXTO A VOZ')
#nb.add(p4,text='VOZ A TEXTO')






class MARCO:
	def __init__(self, pestana, posicion=[100,170], anchoalto=[80,18]): 
		self.x=posicion[0]
		self.y=posicion[1]
		self.ancho=anchoalto[0]
		self.alto=anchoalto[1]
		self.pestana=pestana

	def dibuja(self):
		frame = Frame(self.pestana, width=self.ancho, height=self.alto, bg="light blue", bd=5)
		frame.config(bd=10, relief="groove")
		frame.place(x=self.x, y=self.y)

		#CUADRO DE SCROLL URL 
		S = Tkinter.Scrollbar(frame)
		self.T = Tkinter.Text(frame, width=self.ancho, height=self.alto, font=("Helvetica", 14), fg="white", bg="black", insertbackground='white')
		S.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
		self.T.pack(side=Tkinter.LEFT, fill=Tkinter.Y)
		S.config(command=self.T.yview)
		self.T.config(yscrollcommand=S.set)
		
	def textoOUT(self, texto):
		self.T.insert(Tkinter.END, texto)


	def textoIN(self):
		textito=self.T.get("1.0", END)
		return textito


	def borrar(self):
		self.T.delete('1.0', END)
		




#P1 ------------CUADRO 1 ------------
MARCO1=MARCO(p1)
MARCO1.dibuja()



def eliminarepetidos(lista):
	i=0
			
	try:
		
		while i < len(lista):
			if lista[i]== lista[i+1]:
				del lista[i+1]
				i=-1
			i=i+1
			
			
	except:
		pass
			


def SCRAPENOTICIAS(carpeta):

	#os.system('clear')   # comando en linux
	os.system('cls')	#comando en windows
	
	print (f'LA CARPETA ES {carpeta}')
	today = date.today()  #Fecha actual
	
	
	now = datetime.now()  #Fecha actual
	
	
	# Lee archivo URLs coloca cada linea a elementos de lista
	URL  = open(carpeta+'URLs.txt','r')
	URL= URL.readlines()
	
	
	
	for i in range(len(URL)):
		URL[i] = URL[i].replace('\n', '')
		#URL[i] = URL[i].replace('//w','w')
	
	f = open(carpeta+'TITULARES.txt','w')
	f.write('')
	f.close()
	
	f = open(carpeta+'TITULARES.txt','a')
	
	
	for i in range (len(URL)):
		try: 
			
			if str(URL[i][:4]) == "TEMA":
					temanuevo=URL[i]
					print ('\n' + 'TEMA NUEVO---> '+temanuevo)
					f.write ('\n' + 'TEMA NUEVO---> '+temanuevo)
					f.write ('\n')
				
				
			result = requests.get(URL[i])
			src = result.content
			#soup = BeautifulSoup(src, 'html.parser')
			soup = BeautifulSoup(src, 'lxml')
			
			
			print ("")
			print ("::::::::::::::"+str(temanuevo))
			print ("::::::::::::::BUSCANDO TITULARES DE |  "+soup.title.string)
			print ("::::::::::::::URL = " + URL[i])
			print ("")
			
			
			titulares= soup.find_all('a')
			
		
			eliminarepetidos(titulares)
				
			f.write('\n' )
			f.write('\n' + "::::::::::::::"+str(temanuevo))
			f.write('\n' + ":::::::::::FECHA = " + str(today))
			f.write('\n' + ":::::::::::TITULARES DE = |  "+soup.title.string)
			f.write('\n')
	
			try:
			
				for titulares in titulares:
	
					#f.write(f'{titulares} \n')
					
					if titulares.string != None:
						titulo=titulares.string.split()
						
						if len(titulo) > 3:
							
							titulofinal=" ".join(titulo)
							titulofinal=""
							for titulo in titulo:
								titulofinal	+= titulo + " "						
															
							f.write('\n' + str(temanuevo))
							f.write('\n' + "TITULO ---> "+ titulofinal)
							#f.write('\n' + URL[i]+titulares.get('href'))
							
							if (titulares.get('href')[:4] == 'http'):
								f.write('\n' + titulares.get('href'))
								
							elif (titulares.get('href')[:5] == '//www'):
								titulares2=titulares.get('href').replace('//www','http://www')
								f.write('\n' + titulares2)
								#f.write('\n' + titulares.get('href'))
							else: 
								f.write('\n' + URL[i]+titulares.get('href'))
								#f.write('\n' + titulares.get('href'))
				
					
					f.write('\n\n')
						
			except:
				pass
		except:
			pass
	
	
	f.write("::::::::::::::::::::FIN DE LOS TITULARES DE FECHA " + str(today)+ "::::::::::::::::::::::")
	f.close()
	
	
	# Formatea Titulares, elimina espacios en blanco ,repeticiones.
	
	f  = open(carpeta+'TITULARES.txt','r')
	
	lineas= f.readlines()

	eliminarepetidos(lineas)
		
	f.close()
	os.system('rm '+carpeta+'TITULARES.txt')  #comando en linux
	#os.system(f'del TITULARES.txt')    #comandon en windows
	
	
	#Exporta Titulares formateados y con fecha
	
	g = open(carpeta+'TITULARES-'+str(today)+'.txt','w')
	
	
	for lineas in lineas:
		g.write(lineas)
	
	g.close()
	
	
	
	print ("::::LISTO LOS TITULARES DE FECHA "+str(today)+" !!::::::::")
	print ("::::::")
	print ("::::")
	print ("::")
	print ("")
	print ("")


def ACTUALIZARURL():
	
	try:
		URL= open(carpeta+'URLs.txt','r')
		print (f'LA CARPETA DE URL ES {carpeta}URLs.txt')
				
		mensaje=""
	
		for line in URL:
			mensaje+=line
			
		MARCO1.borrar()
		MARCO1.textoOUT(mensaje)
	
		print ('URL ACTUALIZADO')
	
	except:
		MARCO1.borrar()
		MARCO1.textoOUT('TEMA')
	
	

def ACTUALIZARTITULARES():
	
	try:
		TITULARESLISTADO=open(carpeta+'TITULARES-'+str(today)+'.txt','r')
	
		textotitulares=""
		
		MARCO2.borrar()
		#T2.delete('1.0', END)
	
		cucu=""
		for line in TITULARESLISTADO:
			cucu+=line
		MARCO2.textoOUT(cucu)
	
	
	except:
		MARCO2.borrar()
		MARCO2.textoOUT('No hay titulares disponibles de hoy')
	




def STOP():
    os.system('echo salida')
    #os.system('SYSTEMINFO')
    os.system('taskkill /im cmd.exe')
    #os.system('exit')
    #quit()
#Button(root, text='STOP',bg='red',command=STOP).place(x=20,y=50)



def GUARDAR():
	
	#links=T1.get("1.0", END)
	links=MARCO1.textoIN()
	#os.system('rm URLs.txt')
	URL  = open(carpeta+'URLs.txt','w')
	URL.write (links)
Button(p1, text='GUARDAR',bg='yellow',command=GUARDAR).place(x=200,y=100)


Label(p1, text='INGRESA URLs PARA LEER').place(x=400, y=120)


def CARGARURL():
	ACTUALIZARURL()
	ACTUALIZARTITULARES()
Button(root, text='CARGAR URLs-TITULARES',bg='light blue',command=CARGARURL).place(x=100,y=50)








# --------------------PESTANA 2  -----TITULARES----------------



def NEWS():

	
	Label(p1, text='BUSCANDO TITULARES', bg = 'white').place(x=500, y=50)
	
	SCRAPENOTICIAS(carpeta)

	
	Label(p1, text='TITULARES ACTUALIZADOS', bg = 'white').place(x=500, y=50)
Button(root, text='NEWS',bg='light green',command=NEWS).place(x=300, y=50)


MARCO2=MARCO(p2)
MARCO2.dibuja()


def ABREWEB():
	query=webver.get()
	print (query)
	if query != None:
		webbrowser.open_new_tab(query)
Button(p2, text='ABRE WEB',bg='light blue',command=ABREWEB).place(x=800,y=95)


Label(p2, text='INGRESA URL PARA ABRIR WEB').place(x=80, y=100)
webver= Entry(p2, width=50)
webver.place(x=300,y=100)

query=webver.get()





#--------------------------PESTANA 3-----LEER----------------


'''
def LEERVOZ():
	textoleer=T3.get("1.0", END)
	print (textoleer)
	leervoz(textoleer)
	#subprocess.Popen(['python3', leervoz(textoleer)])
	#t1 = os.popen(leervoz(textoleer))
	#t1 = threading.Thread(target=leervoz(textoleer))
	#threads.append(t1)
	#t1.start()
Button(p3, text='LEERVOZ',bg='yellow',command=LEERVOZ).place(x=500,y=50)



def BORRA():
	pass
	T3.delete('1.0', END)
Button(p3, text='BORRA',bg='light green',command=BORRA).place(x=850, y=95)



"""
#TEXTOVOCES=open("textovoces.txt",'r')


#textoleer=""

#for line in TEXTOVOCES:
#	textoleer+=" "+line
"""

frame3 = Frame(p3, width=100, height=200)
frame3.config(bd=10, relief="groove")
 
#frame1.config(relief="sunken")
#frame1.config(cursor="pirate")
frame3.place(x=100, y=150)
#frame1.pack(side=BOTTOM)



#CUADRO DE SCROLL URL 


S3 = Tkinter.Scrollbar(frame3)
T3 = Tkinter.Text(frame3, height=20, width=100, font=("Helvetica", 14),  fg="white", bg="black", insertbackground='white')
#.place(x=50, y=20)
S3.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
T3.pack(side=Tkinter.LEFT, fill=Tkinter.Y)
S3.config(command=T3.yview)
T3.config(yscrollcommand=S3.set)



Label(p3, text='INGRESA URL PARA LEER').place(x=100, y=100)
webver3= Entry(p3, width=50)
webver3.place(x=300,y=100)

query3=webver3.get()



def TRAETEXTO():
	query3=webver3.get()
	print (query3)
	T3.delete('1.0', END)
	texto= EXTRAETEXTO(query3)
	texto2=texto.replace(".", ".\n\n")
	
	
	T3.insert(END, texto2)
	#if query3 != None:
	#	print (EXTRAETEXTO(query3))
		
		#webbrowser.open_new_tab(query3)
Button(p3, text='TRAE TEXT0',bg='light blue',command=TRAETEXTO).place(x=720,y=95)



'''


root.mainloop()


#-------------FIN PROGRAMA 










