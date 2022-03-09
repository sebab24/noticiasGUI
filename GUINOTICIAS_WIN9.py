#INSTALACION LIBRERIAS
'''#   sudo apt-get install python3-tk		 #para python3 
#   sudo apt-get install python-tk		  #para python2 
#   sudo apt install python-pip3
#   sudo pip3 install SpeechRecognition
#   sudo apt-get install python-pyaudio python3-pyaudio
#   sudo apt install sshpass
#   sudo pip3 install sox	 #reproduce sonidos
#	sudo apt install libsox-fmt-all   # para reproducir mp3 y *
#	pip install lxml	# modificador para scrapear webs
#	sudo apt-get install fonts-symbola	 #instalar font para evitar caida al pegar texto en marco
 
#from scrapeNOTICIAS import SCRAPENOTICIAS

#from scrapegetTEXTO import 	EXTRAETEXTO
'''


import requests
from bs4 import BeautifulSoup

from datetime import date
from datetime import datetime
import time
import webbrowser

today = date.today()


import sys

import os, subprocess

import gtts
from gtts import gTTS
#import speech_recognition as sr



import numpy as np
import threading



import pygame
from pygame import mixer


from pydub import AudioSegment
from audioplayer import AudioPlayer

import tkinter as Tkinter
from tkinter import ttk
from tkinter import *
from tkinter.filedialog import askopenfilename



pygame.init()




#__________________________


global carpeta
carpeta =  os.getcwd()
#print(f'la carpeta es {os.getcwd()}')

carpeta+='/'
#print(f'la carpeta actual es :  {carpeta}')

#carpetactual= os.system('pwd')
#carpeta = "/home/seba/Documents/SEBA/24/NOTICIAS/"  # notebook 4
# carpeta = "/home/seba/Documentos/NEWS/"	#notebook 6




#--------------GUI--------------



#VENTANA PRINCIPAL.
root = Tkinter.Tk()
root.title("LECTOR DE NOTICIAS V.9")
root.geometry("1000x650")
root.configure(bg="light blue", bd=5)
#root.configure(bg='light green', bd=5)

#nombre = StringVar()
#numero = IntVar()

#PANEL PESTANAS
nb = ttk.Notebook(root)
#nb.configure(bg="ligth blue", bd=5)
nb.pack(fill='both',expand='yes')


#PESTANAS
p1 = ttk.Frame(nb)
#p1.configure(bg="light blue", bd=5)
p2 = ttk.Frame(nb)
p3 = ttk.Frame(nb)
#p4 = ttk.Frame(nb)
p5 = ttk.Frame(nb)
p6 = ttk.Frame(nb)
p7 = ttk.Frame(nb)
p8 = ttk.Frame(nb)
#p9 = ttk.Frame(nb)


#TITULO A PESTANAS 
nb.add(p1,text='URLs p1')
nb.add(p2,text='TITULARES p2')
nb.add(p3,text='TEXTO A VOZ p3')
#nb.add(p4,text='VOZ A TEXTO p4')
nb.add(p5,text='PDF A VOZ p5')
nb.add(p6,text='BLACK-LIST p6')
nb.add(p7,text='TITULARES-BLACK p7')

nb.add(p8,text='WHITE-LIST p8')
#nb.add(p9,text='TITULARES-WHITE p9')


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
		return self.T.get("1.0", END)
		#return textito


	def borrar(self):
		self.T.delete('1.0', END)




#------------PESTANA 1 ------------CUADRO 1 ------------


p1MARCO=MARCO(p1)
p1MARCO.dibuja()


def NORM(palabra):
	palabra=palabra.strip().lower()
	palabra=palabra.strip('\n')

	palabra=palabra.replace('á','a')
	palabra=palabra.replace('é','e')
	palabra=palabra.replace('í','i')
	palabra=palabra.replace('ó','o')
	palabra=palabra.replace('ú','u')

	return palabra


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
			
def eliminarepetidos2(lista):
	#listaset=set(lista)
	#lista=list(set(lista))
	return list(set(lista))

def SCRAPENOTICIAS(carpeta):

	#os.system('clear')   # comando en linux
	os.system('cls')	#comando en windows
	
	print (f'LA CARPETA ES {carpeta}')
	today = date.today()  #Fecha actual
	
	
	now = datetime.now()  #Fecha actual
	
	#now= now.strftime("%Y%m%d%H%M%S")
	
	#print(today)
	#print(now)
	
	
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
			
			#print (soup)
			
			titulares= soup.find_all('a')
			
			
			'''
			
			#titulares= soup.find_all(target="_self")
			#titulares= soup.find_all('span')#, attrs={'class':'tag'})
			#links=titulares.find_all('href')
			#titulares= soup.find_all('h1')
			#titulares= soup.find_all('a', 'href')#, attrs={'class':'contenedor-titulo'})
			#seguidores2= soup.find('meta', attrs={'property':'og:description'})
			#seguidores3= soup.find('meta', attrs={'name':'description'})
			
			
			#print (titulares)
			
			#titulo= soup.title.string
			#print (titulo)
			
								  		
			#print(soup.get_text())
			
			'''
			
			#eliminarepetidos(titulares)
			#eliminarepetidos2(titulares)
			titulares=list(set(titulares))
			
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
	
	
	
	# Formatea Titulares, elimina espacios en blanco o repeticiones.
	
	f  = open(carpeta+'TITULARES.txt','r')
	
	lineas= f.readlines()
	
	
	
	eliminarepetidos(lineas)
	#eliminarepetidos2(lineas)
	#lineas=list(set(lineas))
	
	f.close()
	#
	os.system('rm '+carpeta+'TITULARES.txt')  #comando en linux
	#os.system(f'del TITULARES.txt')	#comandon en windows
	
	
	
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
		URL= open(carpeta+'URLs.txt','r').read()
		print (f'LA CARPETA DE URL ES {carpeta}URLs.txt')
		
		
		#mensaje=""
	
		#for line in URL:
		#	mensaje+=line
			
		p1MARCO.borrar()
		#p1MARCO.textoOUT(mensaje)

		p1MARCO.textoOUT(URL)
		#T1.delete('1.0', END)
		#T1.insert(END, mensaje)
		print ('URL ACTUALIZADO')
	
	except:
		p1MARCO.borrar()
		p1MARCO.textoOUT('TEMA')


def ACTUALIZARTITULARES():
	
	today = date.today()
	
	try:
		TITULARESLISTADO=open(carpeta+'TITULARES-'+str(today)+'.txt','r').read()
		#TITULARESLISTADO=open('TITULARES-'+str(today)+'.txt','r')
		textotitulares=""
		
		p2MARCO.borrar()
		
	
		#titulares=""
		#for line in TITULARESLISTADO:
		#	titulares+=line
		#p2MARCO.textoOUT(titulares)
		p2MARCO.textoOUT(TITULARESLISTADO)

	except:
		p2MARCO.borrar()
		p2MARCO.textoOUT('No hay titulares disponibles de hoy, presiona NEWS')


def EXIT():
	#os.system('echo salida')
	#os.system('SYSTEMINFO')
	#os.system('taskkill /im cmd.exe') #para window
	#os.system('exit')  # para linux
	#quit()
	exit()
#botonSTOP= Button(root, text='STOP',bg='red',command=STOP).place(x=20,y=50)


def GUARDAR():
	links=p1MARCO.textoIN()
	#os.system('rm URLs.txt')
	URL  = open(carpeta+'URLs.txt','w')
	URL.write (links)
p1botonGUARDAR= Button(p1, text='GUARDAR',bg='yellow',command=GUARDAR).place(x=200,y=100)
p1labelINGRESAURL= Label(p1, text='INGRESA URLs PARA LEER').place(x=400, y=120)


def CARGARURL():
	ACTUALIZARURL()
	ACTUALIZARTITULARES()
	CARGARblacklist()
	TITULARESfiltrados()
	CARGARwhitelist()
	FILTRADOSWHITE()

p1botonCARGARURLS= Button(p1, text='CARGAR URLs-TITULARES',bg='light blue',command=CARGARURL).place(x=100,y=50)


def NEWS():
	
	#GUARDAR()
	
	p1labelBUSCANDOTITULARES= Label(p1, text='BUSCANDO TITULARES', bg = 'white').place(x=500, y=50)
	
	#ACTUALIZARURL()
	
	#LEER URL DESDE T1, Y OK(EXPORTAR RESULTADOS A ARCHIVO TITULARES, Y ACTUALIZAR CUADRO EN PESTANA 2). 
	
	#subprocess.Popen(['python3', 'scrapeNOTICIAS.py'])
	SCRAPENOTICIAS(carpeta)
	ACTUALIZARTITULARES()
	#os.system('python3 '+carpeta+'scrape-NOTICIAS.py')

	p1labelBUSCANDOACTUALIZADOS(p1, text='TITULARES ACTUALIZADOS', bg = 'white').place(x=500, y=50)
p1botonNEWS= Button(p1, text='NEWS',bg='light green',command=NEWS).place(x=300, y=50)


# --------------------PESTANA 2  -----TITULARES----------------

p2MARCO=MARCO(p2)
p2MARCO.dibuja()



#--------------------------PESTANA 3-----TEXTO A VOZ----------------


p3MARCO=MARCO(p3)
p3MARCO.dibuja()

'''
def PLAY(archivo):
	tempo=1.5
	pitch=400
	
	#reproduce=subprocess.Popen(['play -q',archivo,'tempo',tempo], shell=True)
	
	os.system(f'play -q {archivo} tempo {tempo}')

def PLAY2(archivo):
	player = AudioPlayer(archivo)
	player.play()
'''

def PLAY(archivo):
	
	AudioSegment.from_mp3(archivo).export('salida.ogg', format='ogg')

	LECTURA=pygame.mixer.Sound('salida.ogg')
	
	LECTURA.play()


def LEERVOZ():
	texto=p3MARCO.textoIN()
	tts = gTTS(texto, lang='es')
	tts.save('SALIDA.mp3')

	p3labelREPRODUCIENDO= Label(p3, text='REPRODUCIENDO		').place(x=300, y=100)
	PLAY('SALIDA.mp3')
p3botonLEERVOZ= Button(p3, text='TXT A VOZ',bg='yellow',command=LEERVOZ).place(x=500,y=50)


def BORRA3():
	#pass
	p3MARCO.borrar()
p3botonBORRA= Button(p3, text='BORRA',bg='light green',command=BORRA3).place(x=850, y=95)


def CONTINUA():
	pygame.mixer.unpause()
#p3botonCONTINUA= Button(p3, text='CONTINUA',bg='light green',command=CONTINUA).place(x=850, y=65)


global p
p=0
def PAUSA():
	global p
	p+=1
	if p%2==1:
		Label(p3, text='PAUSADO		').place(x=300, y=100)
		Label(p5, text='PAUSADO		').place(x=300, y=100)
		pygame.mixer.pause()
	else:
		Label(p3, text='REPRODUCIENDO		').place(x=300, y=100)
		Label(p5, text='REPRODUCIENDO		').place(x=300, y=100)
		pygame.mixer.unpause()
p3botonPAUSA= Button(p3, text='PAUSA',bg='light blue',command=PAUSA).place(x=500, y=95)

def STOP():
	pygame.mixer.stop()
	Label(p3, text='		').place(x=300, y=100)
	Label(p5, text='		').place(x=300, y=100)
p3botonSTOPAUDIO= Button(p3, text='STOP AUDIO',bg='RED',command=STOP).place(x=500, y=125)



'''
#--------------------------PESTANA 4-----VOZ A TEXTO--------------



MARCO4=MARCO(p4)
MARCO4.dibuja()
'''



#--------------------------PESTANA 5-----PDF A VOZ--------------

p5MARCO=MARCO(p5)
p5MARCO.dibuja()


def FILE2TXT(nombre):
	
	if nombre[:-3]=='pdf':
		os.system(f'pdftotext -layout {nombre} SALIDAtxt.txt')
	elif nombre[:-3]=='doc':
		os.system(f'catdoc {nombre} > SALIDAtxt.txt')
	elif nombre[:-3]=='docx':
		os.system(f'docx2txt {nombre} SALIDAtxt.txt')
	
	
	texto= open('SALIDAtxt.txt','r')
	msjvacio=""
	for texto in texto:
		msjvacio+=texto
	msj=ELIMINAESPACIOS(msjvacio)
	return msj


def ELIMINAESPACIOS(msj):
	texto=msj.replace(' Pág ',' página ')
	#limpio=""
	limpiolista=texto.split()
	limpio=' '.join(limpiolista)
	#for limpiolista in limpiolista:
	#	limpio+=limpiolista+' '
	return limpio


def ELIGEFILE():
	filename = askopenfilename()
	msj=FILE2TXT(filename)
	
	limpio=ELIMINAESPACIOS(msj)
	
	p5MARCO.borrar()
	p5MARCO.textoOUT(limpio)
p5botonELIGEARCHIVO= Button(p5, text='EligeArchivo',bg='light blue',command=ELIGEFILE).place(x=100, y=125)



'''

def PLAY(archivo):
	tempo=1.5
	pitch=400
	
	try:
		#reproduce=subprocess.Popen(['play -q',archivo,'tempo',tempo], shell=True)
		os.popen(f'play -q {archivo} tempo {tempo}')
	except:
		print ('hubo error en reproducir')
		pass
	#os.system(f'play -q {archivo} tempo {tempo}')

'''



def PDFAVOZ():
	texto=p5MARCO.textoIN()
	tts = gTTS(texto, lang='es')
	tts.save('SALIDA.mp3')

	Label(p5, text='REPRODUCIENDO		').place(x=300, y=100)
	PLAY('SALIDA.mp3')
p5botonPDF2VOZ=Button(p5, text='PDF2VOZ',bg='yellow',command=PDFAVOZ).place(x=500,y=50)
p5botonPAUSA=Button(p5, text='PAUSA',bg='light blue',command=PAUSA).place(x=500, y=95)
p5botonSTOPAUDIO= Button(p5, text='STOP AUDIO',bg='RED',command=STOP).place(x=500, y=125)


def BORRA5():
	p5MARCO.borrar()
p5botonBORRAR= Button(p5, text='BORRAR',bg='light green',command=BORRA5).place(x=850, y=95)


def QUEPARTE():
	
	i = int(parte.get())
	cortado=msj[TAMANO*(i):TAMANO*(i+1)]

	var.set(f'PARTE {i} DE {PARTES+1} PARTES')
	#var.set('PARTE  PARTES')
	
	T1.delete('1.0', END)
	T1.insert(END, cortado)
	
	i=i+1
	parte.delete(0,END)
	parte.insert(0,i)


def LEERSGTEVOZ():
	QUEPARTE()
	texto = T1.get("1.0", END)
	try: 
		tts = gtts.gTTS(texto, lang='es-US')
		tts.save("SALIDA.mp3")
		PLAY('SALIDA.mp3')

	except:
		print('''
Espera un poco, estoy procesando... para detener presiona CONTROL+Z''')
		LEERVOZ()


#_------PESTANA 6    BLACK LIST

p6MARCO=MARCO(p6)
p6MARCO.dibuja()



def GUARDARblacklist():
	links=p6MARCO.textoIN()
	#os.system('rm URLs.txt')
	URL  = open(carpeta+'blacklist.txt','w')
	URL.write (links)
p6botonGUARDAR= Button(p6, text='GUARDAR',bg='yellow',command=GUARDARblacklist).place(x=200,y=100)
Label(p6, text='INGRESA black list').place(x=400, y=120)



def ACTUALIZARblacklist():
	
	try:
		URL= open(carpeta+'blacklist.txt','r').read()

		p6MARCO.borrar()
		p6MARCO.textoOUT(URL)
		print ('blacks ACTUALIZADO')

	except:
		p6MARCO.borrar()
		p6MARCO.textoOUT('TEMA')



def CARGARblacklist():
	ACTUALIZARblacklist()
	#ACTUALIZARTITULARES()
p6botonGARGARBLACKLIST=Button(p6, text='CARGAR Blacklist',bg='light blue',command=CARGARblacklist).place(x=100,y=50)




#_------PESTANA 7   TITULARES FILTRADOS BLACK

p7MARCO=MARCO(p7)
p7MARCO.dibuja()




def FILTRO(TITULARESLIST,BLACKFILE):


	lineas = TITULARESLIST.readlines()
	blacklist=BLACKFILE.readlines()

	listilla=[]
	for blacklist in blacklist:
		listilla.append(NORM(blacklist))

	blacklist= set(listilla)
	#blacklist= blacklist.discard('')

	#print (blacklist)

	i=0
	titulares=""
	titu = ""

	while i<len(lineas)-1:

		if lineas[i][:10]=='TEMA NUEVO':
			titulares += lineas[i]
			titulares += lineas[i+1]
			titulares += lineas[i+2]
			titulares += lineas[i+3]
			titulares += lineas[i+4]
			i+=3


		if lineas[i][:2]=='::':
			titulares += lineas[i]
			titulares += lineas[i+1]
			titulares+=lineas[i+2]
			titulares+=lineas[i+3]
			#titulares+='\n'
			i+=3


		if lineas[i][:6]=='TEMA =':
			titu=''
			titu+= lineas[i]
			titu+= lineas[i+1]
			titu+= lineas[i+2]
			titu+= "\n"


		if len(blacklist)>0:
			tituLOWER=titu.lower()

			m=0
			for blackw in blacklist:
				if blackw in tituLOWER and blackw!='':
					m+=1

			if m==0 and len(tituLOWER)>5:
				titulares += titu

			#x=set(NORM(titu).split())
			#inter = x.intersection(blacklist)
			#if inter == set():
			#	titulares+=titu

		else: 
			titulares+=titu
		
		
		titu=''

		i+=1


	return titulares


def TITULARESfiltrados():
	
	try:
	#TITULARESLISTADO=open(f'TITULARES-{today}.txt','r')
	#BLACKFILE=open(f'blacklist.txt','r')
		today = date.today()
		TITULARESLISTADO = open(carpeta+'TITULARES-'+str(today)+'.txt','r')
		BLACKFILE = open(carpeta+'blacklist.txt','r')

		titularesfiltrados = FILTRO(TITULARESLISTADO,BLACKFILE)

		p7MARCO.borrar()
		p7MARCO.textoOUT(titularesfiltrados)

	except:
		p7MARCO.borrar()
		p7MARCO.textoOUT('No hay titulares filtrados disponibles de hoy, presiona NEWS')
p7botonBLACKFILTRADOS= Button(p7, text='CARGAR Black-Filtrados',bg='light blue',command=TITULARESfiltrados).place(x=100,y=50)



def ABREWEB7():
	query=webver7.get()
	print (query)
	if query != None:
		webbrowser.open_new_tab(query)
p7botonABREWEB= Button(p7, text='ABRE WEB',bg='light green',command=ABREWEB7).place(x=800,y=95)


def LIMPIAWEB7():
	webver7.delete("0","end")
p7botonLIMPIAWEB= Button(p7, text='LIMPIA WEB',bg='light blue',command=LIMPIAWEB7).place(x=800,y=60)

Label(p7, text='INGRESA URL PARA ABRIR WEB').place(x=80, y=100)
webver7= Entry(p7, width=50)
webver7.place(x=300,y=100)

#query=webver7.get()



#_------PESTANA 8   WHITELIST

p8MARCO_in=MARCO(p8, [100,150],[80,3])
p8MARCO_in.dibuja()


p8MARCO_out=MARCO(p8,[100,260],[80,15])
p8MARCO_out.dibuja()



def ACTUALIZARwhitelist():
	
	#try:
	URL= open(carpeta+'whitelist.txt','r').read()
	print (f'LA CARPETA DE URL ES {carpeta}whitelist.txt')
	
	
	#mensaje=""
	#for line in URL:
	#	mensaje+=line
		
	p8MARCO_in.borrar()
	p8MARCO_in.textoOUT(URL)

	print ('white list actualizada')
	
	#except:
		#p8MARCO_in.borrar()


def CARGARwhitelist():
	ACTUALIZARwhitelist()
	#ACTUALIZARTITULARES()
#p8botonCARGARWHITELIST= Button(p8, text='CARGAR whitelist',bg='light blue',command=CARGARwhitelist).place(x=100,y=50)


def FILTROwhite():#TITBLACK,WHITEFILE):
	lineas = open(carpeta + 'TITSblacks.txt', 'r').readlines()
	whitelist= open(carpeta + 'whitelist.txt', 'r').readlines()



	listilla=[]
	for whitelist in whitelist:
		listilla.append(NORM(whitelist))

	whitelist= set(listilla)
	whitelist.discard('')

	print (f'whitelist = {whitelist}')

	i=0
	titulares=""
	titu = ""
	#print (f'LENLINEAS {len(lineas)}')
	while i<len(lineas)-1:

		if lineas[i][:6]=='TEMA =':
			titu=''
			titu += lineas[i]
			titu += lineas[i+1]
			titu += lineas[i+2]
			titu += "\n"

		if len(whitelist)>0:
			tituLOWER = titu.lower()
			print (tituLOWER)

			m = 0
			for whitew in whitelist:
				if whitew in tituLOWER and whitew!='':
					m += 1
					print (f'SUME M {m}')
			print (f'M VALE {m}')
			if m > 0 and len(tituLOWER) > 5:
				titulares += titu


		else:
			titulares+=titu


		titu=""

		i+=1

	return titulares


def FILTRADOSWHITE():
	
	#try:
	tits=p7MARCO.textoIN()
		
	URL = open(carpeta+'TITSblacks.txt','w')
	URL.write(tits)
	

	TITULARESLISTADO = open(carpeta+'TITSblacks.txt','r')
	WHITEFILE = open(carpeta+'whitelist.txt','r')

	TITSwhite = FILTROwhite()#TITULARESLISTADO,WHITEFILE)

	p8MARCO_out.borrar()
	p8MARCO_out.textoOUT(f'WHITE ACTUALIZADOS {TITSwhite}')
	#except:
	#	p7MARCO.borrar()
	#	p7MARCO.textoOUT('No hay titulares filtrados disponibles de hoy, presiona NEWS')
#p9botonCARGARWHITEFILTRADOS= Button(p9, text='CARGAR white-Filtrados',bg='light blue',command=FILTRADOSWHITE).place(x=100,y=50)



def GUARDARwhitelist():
	links=p8MARCO_in.textoIN()
	#os.system('rm URLs.txt')
	URL  = open(carpeta+'whitelist.txt','w')
	URL.write (links)
	URL.close()
	
	FILTRADOSWHITE()
	
p8botonWHITES= Button(p8, text='WHITES',bg='yellow',command=GUARDARwhitelist).place(x=200,y=100)
Label(p8, text='INGRESA white list').place(x=400, y=120)



def ABREWEB9():
	query=webver9.get()
	print (query)
	if query != None:
		webbrowser.open_new_tab(query)
p8botonABREWEB= Button(p8, text='ABRE WEB',bg='light green',command=ABREWEB9).place(x=800,y=95)


def LIMPIAWEB9():
	webver9.delete("0","end")
p8botonLIMPIAWEB= Button(p8, text='LIMPIA WEB',bg='light blue',command=LIMPIAWEB9).place(x=800,y=60)



Label(p8, text='INGRESA URL PARA ABRIR WEB').place(x=80, y=60)
webver9= Entry(p8, width=50)
webver9.place(x=300,y=60)

query=webver9.get()



CARGARURL()

root.mainloop()


#_--------------------------FIN PROGRAMA


# BASURAS ------


class NADAS:
	
	def NADA():

		etiqueta1=Label(cuadro, text='CUANTOS CARACTERES POR PARTE? (default =3000')
		etiqueta1.pack() #.place(x=50, y=50)

		E1 = Entry(cuadro, bd =5, bg='light blue')
		E1.pack()
		#E1.place(x=50,y=80)

		TAMANO=3000



		botonstop= Button(cuadro, text='STOP',bg='red',command=STOP)
		botonstop.pack(side = RIGHT) #.place(x=800,y=30)


		 
		carpeta =  os.getcwd()+'/'

		nombrePDF = askopenfilename(initialdir = carpeta,title = "Selecciona archivo PDF para leer en voz",filetypes = (("pdf files","*.pdf"),("all files","*.*")))

		etiqueta2=Label(cuadro, text=f'ARCHIVO A LEER = {nombrePDF}')
		etiqueta2.pack()

		#.place(x=50, y=120)


		msj=file2txt(nombrePDF)

		LARGO = len(msj)
		PARTES= int(LARGO/TAMANO)

		etiqueta3=Label(cuadro, text='INGRESA n° PARTE', bg='yellow')
		etiqueta3.pack() #.place(x=240, y=200)
		parte = Entry(cuadro, bd =5, bg='yellow')
		parte.insert(0,0)
		parte.pack()
		#place(x=400,y=200)


		var=StringVar()


		#var= f'PARTE {str(i)} DE {PARTES+1} PARTES', bg='light green'


		etiquetavariable=Label(cuadro, textvariable=var,bg='light green').pack() #place(x=50, y=275)


		cuadro2= Frame(cuadro,  width=700,  height=350, bg='white')
		cuadro2.config(relief="groove", bd=5)
		cuadro2.pack()





		T1.insert(Tkinter.END, '...ingresa texto aqui para leer en voz...')


	def NADA2():		

		boton1=Button(cuadro, text='TRAER TEXTO',bg='light blue',command=QUEPARTE)
		boton1.pack(side=LEFT) #lace(x=600,y=150)

		boton3=Button(cuadro, text='LEER',bg='light blue',command=LEERVOZ)
		boton3.pack(side =LEFT) #lace(x=600,y=250)

		boton2=Button(cuadro, text='LEER SIGUIENTE',bg='light blue',command=LEERSGTEVOZ)
		boton2.pack(side=LEFT) #lace(x=600,y=200)


	def NADA3():



		Label(p5, bg="light blue", text="COMANDOS VOZ:   \n PRENDE/APAGA   (LUZ 1;  LED 2;  ZUMBIDO)  \n  ABRE/CIERRA   (VLC;  FLORENCE) \n TERMINAR \n APAGAR COMPUTADOR", relief=RIDGE).place(x=200, y=20)


		Label(p5, text="Dijiste = ").place(x=100, y=180)





		  
		np.savetxt(carpeta+'valores.py', valores, fmt='%1.1f  ')

		def BRILLO1mas():
		  if valores[2,0]<5 :
			  valores[2,0]=valores[2,0]+0.1
		  os.system('xrandr --output VGA-1 --brightness '+str(valores[2,0]))
		  Label(p2, text=round(valores[2,0],2)).place(x=380, y=posicion1BRILLO)
		  np.savetxt(carpeta+'valores.py', valores, fmt='%1.1f  ')

		def BRILLO1menos():
		  if valores[2,0]>0.2 :
			  valores[2,0]=valores[2,0]-0.1
		  os.system('xrandr --output VGA-1 --brightness '+str(valores[2,0]))
		  Label(p2, text=round(valores[2,0],2)).place(x=380, y=posicion1BRILLO)
		  np.savetxt(carpeta+'valores.py', valores, fmt='%1.1f  ')


		def GAMMA1mas():
		  if valores[2,1]<5 :
			  valores[2,1]=valores[2,1]+0.1

		  b=str(valores[2,1])
		  os.system('xrandr --output VGA-1 --gamma '+b+':'+b+':'+b)
		  Label(p2, text=round(valores[2,1],2)).place(x=380, y=posicion1GAMMA)
		  np.savetxt(carpeta+'valores.py', valores, fmt='%1.1f  ')



		  Label(p2, text=round(valores[2,1],2)).place(x=380, y=posicion1GAMMA)
		  np.savetxt(carpeta+'valores.py', valores, fmt='%1.1f  ')


		def BRILLO2mas():
		  if valores[3,0]<5 :
			  valores[3,0]=valores[3,0]+0.1
		  os.system('xrandr --output eDP-1 --brightness '+str(valores[3,0]))
		  Label(p2, text=round(valores[3,0],2)).place(x=380, y=posicion2BRILLO)
		  np.savetxt(carpeta+'valores.py', valores, fmt='%1.1f  ')



		def BRILLO2menos():
		  if valores[3,0]>0.2 :
			  valores[3,0]=valores[3,0]-0.1
		  os.system('xrandr --output eDP-1 --brightness '+str(valores[3,0]))
		  Label(p2, text=round(valores[3,0],2)).place(x=380, y=posicion2BRILLO)
		  np.savetxt(carpeta+'valores.py', valores, fmt='%1.1f  ')

		def GAMMA2mas():
		  if valores[3,1]<5 :
			  valores[3,1]=valores[3,1]+0.1
		  b=str(valores[3,1])
		  os.system('xrandr --output eDP-1 --gamma '+b+':'+b+':'+b)
		  Label(p2, text=round(valores[3,1],2)).place(x=380, y=posicion2GAMMA)
		  np.savetxt(carpeta+'valores.py', valores, fmt='%1.1f  ')



		def GAMMA2menos():
		  if valores[3,1]>0.2 :
			  valores[3,1]=valores[3,1]-0.1
		  b=str(valores[3,1])
		  os.system('xrandr --output eDP-1 --gamma '+b+':'+b+':'+b)
		  Label(p2, text=round(valores[3,1],2)).place(x=380, y=posicion2GAMMA)
		  np.savetxt(carpeta+'valores.py', valores, fmt='%1.1f  ')


	def NADA4():

		# IMAGENES 
		#ampolletaON = PhotoImage(file = r"ampolletaON.png")
		#ampON = ampolletaON.subsample(2, 2)
		#ampolletaOFF = PhotoImage(file = r"ampolletaOFF.png")
		#ampOFF = ampolletaOFF.subsample(2, 2)


		#camaON = PhotoImage(file = r"camaON.png")
		#camON = camaON.subsample(8, 8)
		#camaOFF = PhotoImage(file = r"camaOFF.png")
		#camOFF = camaOFF.subsample(8, 8)




		#CARPETA LOCAL

		#carpeta="/home/seba/Documents/SEBA/24/CONTROLPIEZA/" #Notebook 8
		#carpeta="/home/sebab/Documents/SEBAB-mint/24/PYTHON/PIEZA/" # Notebook 3

		carpeta="/home/seba/Descargas/" #Notebook 6

		#CONEXION A RASPBERRY
		RPI1= 'sshpass -p "a" ssh pi@192.168.43.72'  #RPI3 EN AGUA
		#RPI1= 'sshpass -p "a" ssh pi@192.168.1.51'  #RPI3 EN AGUA?


		#INICIO MEMORIA ESTADOS

		valores= np.loadtxt(carpeta+'valores.py')





