import socket
import sys
import os
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from threading import Thread
import threading
import time
# import tkSimpleDialog
ark_lst=['3']
grb_lst={}

class MyDialog(Frame):
	
	def __init__(self,ark_lst,grp_isim,superself):
		app=Tk()
		Frame.__init__(self,master=app)
		self.window=app
		self.grb_isim=grp_isim
		self.superself=superself
		width_of_screen=self.window.winfo_screenwidth()/2
		height_of_screen=self.window.winfo_screenheight()/2
		self.window.geometry("400x300+%d+%d"%( (width_of_screen-200),(height_of_screen-150)  ))
		self.window.resizable(width=False,height=False)
		self.grb_add={}
		counter=0
		for i in ark_lst:
			self.grb_add[i]=False
			self.name='var'+i
		
			self.name=Checkbutton(self.window,text=str(i),command=lambda a=str(i):self.deneme(a) )
			self.name.grid(row=counter,column=1)
			counter+=1
		Button(self.window,text='Ekle',command=self.ekle).grid(row=counter+1,column=1)


		self.window.mainloop()
	def deneme(self,a):
		# print(self.grb_add[a])
		if (self.grb_add[a])==False:
			self.grb_add[a]=True

		else:
			self.grb_add[a]=False
		# print(self.grb_add[a])

		
	def ekle(self):
		grb_lst[self.grb_isim]=''
		for key in self.grb_add.keys():
			if (self.grb_add[key])==True and (not grb_lst[self.grb_isim].__contains__(key)  ) :
				grb_lst[self.grb_isim]+=(key+',')
		# print(grb_lst)
		Chat_App.update_grb_listbox(self.superself,self.grb_isim)
		self.window.destroy()

class chat_screen(Frame):
	def __init__(self,superself,sendto):
		app=Tk()
		Frame.__init__(self,master=app)
		self.window=app
		self.client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sendmsg=sendto
		self.superself=superself
		width_of_screen=self.window.winfo_screenwidth()/2
		height_of_screen=self.window.winfo_screenheight()/2
		self.window.geometry("400x300+%d+%d"%( (width_of_screen-200),(height_of_screen-150)  ))
		self.window.resizable(width=False,height=False)
		self.label=Label(self.window,text=str(self.sendmsg))
		Button(self.window,text='Ekle',command=self.send).grid(row=0)
		self.label.grid(row=1)

		self.window.mainloop()
	
	def send(self):
		msg='tst'
		try:
			self.client.send(msg.encode('utf-8'))
			for i in range(0,10):
				data=self.client.recv(1024)
				if data:
					# print(data)
					break 
				time.sleep(1)
		except:
			self.send()
	# def __init___(self,window):
		
	# 	# Frame.__init__(self,master=window)
		
	# 	self.window=window
	# 	self.frametk=Frame(self.window,bg='green',width=500,height=500)
	# 	self.guit=Button(self.frametk,text='tst',command=self.send,bg='yellow')
	# 	self.quit.pack()
		# self.frametk.pack()
		
		# self.send()
		# self.window.mainloop()
	
		

class Chat_App(Frame):
	def __init__(self,window):
		Frame.__init__(self,master=window)
		
		self.window=window
		self.client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		width_of_screen=self.window.winfo_screenwidth()/2
		height_of_screen=self.window.winfo_screenheight()/2
		self.window.geometry("800x600+%d+%d"%( (width_of_screen-400),(height_of_screen-350)  ))
		# self.window.resizable(width=False,height=False)
		self.client_flag=False
		self.Username=StringVar()
		self.Password=StringVar()
		self.password_again=StringVar()
		# Thread(self.guncelle).start()
		
		
		self.main_screen()
		

		# self.giris()
		# self.window.mainloop()
	def server_connect(self):
		try:
			self.client.connect(('127.0.0.1',45000))
			return 1
		except:
			return 0
	def server_rg(self,key):
		try:
			rc=''
			##to send for new self.client
			
			msg=key+'$'+self.Password.get()+'$'+self.Username.get()	
			self.client.send(msg.encode('utf-8'))
			for i in range(0,10):
				data=self.client.recv(1024)
				if data:
					# print(data.decode('utf-8'))
					
					break
				time.sleep(1)
			print(data.decode('utf-8'))
			return data.decode('utf-8')
			
		except:
			return 'servererror'
	def peer_info(self):
		try:
			# print(self.send_ark)
			# self.client.send(('peer'+'$'+self.send_ark).encode('utf-8'))

			while True:
				veri=self.client.recv(1024)
				if veri:
					# print(veri)
					return 1
					# data=data.decode('utf-8').split('ark')[1].split('$')
					# print(data)
					break
					# if self.send_ark==data[1]:
					# 	self.msj_lbl1.insert('end',self.send_ark+':'+item.split('$')[2]+'\n')
				
		except:
			print('server error')
	def mesaj_pano(self,ark):
		self.msj_lbl1.delete('1.0',END)
		self.send_ark=ark
		file=open('4dba.txt','r')
		msg=file.read()
		msg=msg.split(',')
		for item in msg:
			if item!='':
				info=item.split('$')
				# print(info)
				if len(info)==3 and (not info.__contains__('frd=')):
					if info[0]==self.Username.get() and info[1]==ark:
						self.msj_lbl1.insert('end','You:'+info[2]+'\n')
						self.msj_lbl1.yview_moveto(1)
					elif info[1]==self.Username.get() and info[0]==ark:
						self.msj_lbl1.insert('end',ark+':'+info[2]+'\n')
						self.msj_lbl1.yview_moveto(1)

			

	def lst1_clk(self,event=''):
		
		
		# self.peer_info()
		for item in self.mesaj_pane:
			state='state'
			item[state]='normal'

		 
		if len(self.list1.curselection())>0:
			selected=int(self.list1.curselection()[0])
			#print(self.list1.get(selected))
			ark=str(self.list1.get(selected))
		
			# 	print('try again')
			# self.msj_lbl1.delete('1.0',END)
			self.send_ark=ark
			# print(ark)
			self.client_flag=True
			Thread(target=self.mesaj_pano,args=(self.send_ark)).start()
			Thread(target=self.guncelle).start()
			# self.mesaj_pano(ark)

			# chat_screen(self,self.send_ark)
		# 		self.mesaj_pano(ark)
				

				# file=open('dba.txt','r')
				# msg=file.read()
				# msg=msg.split(',')
				# for item in msg:
				# 	source=item.split('$')[0]
				# 	destination=item.split('$')[1]
				# 	msg=item.split('$')[2]
				# 	if source==self.Username.get() and destination==ark:
				# 		self.msj_lbl1.insert('end','You:'+item.split('$')[2]+'\n')
				# 	elif destination==self.Username.get() and source==ark:
				# 		self.msj_lbl1.insert('end',ark+':'+item.split('$')[2]+'\n')
				# self.mesaj_pano(ark)
				
				# self.guncelle()
	
		
	def lst2_clk(self,event):
		for item in self.mesaj_pane:
			state='state'
			item[state]='disable'

		if len(self.list2.curselection())>0:
			selected2=int(self.list2.curselection()[0])
			grb=self.list2.get(selected2)
			grb+='_msg'
			with open ('4dba.txt','r') as file:
				for line in file:
					if str(line).startswith('##'+grb):
						msgs=line.split('[')
						msgs=msgs[1].split(']')
						msgs=msgs[0].split(',')
						# print(msgs)
  #  	def partial(self):
		# while True:
		# 	data=self.client.recv(1024)
		# 	if data:
		# 		partial.append(data.decode('utf-8'))
		# 		self.mesaj_pano(self.send_ark)
		# 		# self.window.after(5000,self.guncelle)
		# 	else:
		# 		self.client.send(('update').encode('utf-8'))
	def parca(self):
		time.sleep(1)
		# self.client.send(('parca').encode('utf-8'))
		try:
			while True:
				data=self.client.recv(1024)
				if data:
					msg=data.decode('utf-8').split('$')
					self.msj_lbl1.insert('end',msg[2]+'\n')
					open('dba.txt','a+').write(data.decode('utf-8'))
					# self.mesaj_pano(self.send_ark)
				# else:
				# 	self.client.send(('parca').encode('utf-8'))
				time.sleep(1)
		except:
			
			pass
	def guncelle(self):
		
		if self.client_flag:
			try:
				if listen:
					listen.stop()
			except:
				print('')

			self.client.send(('update$'+self.Username.get()).encode('utf-8'))
			
			while self.client_flag:
				print(self.client_flag)
				data=self.client.recv(4096)
				if data:
					open('4dba.txt','w').write(data.decode('utf-8'))
					newfile=data.decode('utf-8')
					
					# print(oldfile,newfile)
					
						# open('dba.txt','w').write(newfile)
					self.mesaj_pano(self.send_ark)
					self.window.after(1500,self.guncelle)

					break
					
		# listen=Thread(target=self.parca)
		# listen.start()

		
	def msg_gonder(self):
		self.client_flag=False
		# self.guncelle()
		# self.mesaj_pano(self.send_ark)
		
		self.mesaj='ark'+'$'+self.Username.get()+'$'+self.send_ark+'$'

		self.mesaj+=str(self.msj_box.get('1.0',END).replace('\n',''))
		# self.msj_lbl1.insert('end','You:'+self.mesaj.split('$')[3]+'\n')
		self.msj_box.delete('1.0',END)
		# self.msj_lbl1.insert('end','You:'+self.mesaj.split('$')[3]+'\n')

		try:
			self.client.send(str(self.mesaj).encode('utf-8'))
			self.mesaj_pano(self.send_ark)
		except socket.error as err:
			print(err)
		
		self.client_flag=True
			#open('dba.txt','a+').write(mesaj.replace('ark$','')+',')
			
	

	def ark_lst_guncelle(self):
		file=open(self.Username.get()+'dba.txt','r').readlines()
		for line in file:
			msgs=line.split(',')
			for msg in msgs:

				if msg.startswith('frd='):
					print(msg)
					frds=msg.split('frd=')[1].split('$')
					for frd in frds:
						ark_lst.append(frd)
					# print(ark_lst)
		for item in ark_lst:
			self.list1.insert(END,item)

	def control_ark_mail(self,mail):
		
		try:
			rc=''
			##to send for new self.client
			
			msg='mail$'+mail+'$'+self.Username.get()				
			self.client.send(msg.encode('utf-8'))
			for i in range(0,10):
				data=self.client.recv(1024)
				if data:
					# print(data.decode('utf-8'))
					
					break
				time.sleep(1)
			return data.decode('utf-8')
			
		except:
			return 'servererror'

	def ark_ekle_btn(self):
		self.client_flag=False
		try:
			
			self.mail=simpledialog.askstring('input string','please enter email adres',parent=self.window)
			exists=self.control_ark_mail(self.mail)
			self.list1.insert(END,self.mail)
			self.list1['state']='disable'
			
			try:
				if exists=='success':
					#msg=messagebox.askquestion(title='istek', message='istek gonder')
					ark_lst.append(self.mail)
					self.list1.selection_clear(0, END)
					self.list1['state']='normal'
					self.list1.insert(END,self.mail)
				
				elif exists=='Fail':

					 messagebox.showinfo("Hata","email was not found")
			except:
				self.control_ark_mail(self.mail)
		except:
			print('')
		self.client_flag=True
		
	def update_grb_listbox(self,grb_isim):
		self.list2.insert(0,grb_isim)
	def grb_ekle_btn(self):
		grb_isim=simpledialog.askstring('Grup Adi','')
		
		
		# print(grb_lst)
		MyDialog(ark_lst,grb_isim,self)
	def register_page(self):
		self.mp.destroy()
		self.rg=Frame(self.window,bg='green')
		self.rg_welcome=Label(self.rg,
			text='Welcome The Tenfinger App',fg='lime',bg='blue')
		
		#=======================================
		self.rg_Username=Label(self.rg,text="Email",width=12,anchor=W)
		self.rg_username=Entry(self.rg,textvariable=self.Username)
		self.rg_username.delete(0,'end')
		self.rg_username.insert(0,'4')

		self.rg_Password=Label(self.rg,text="Password",width=12,anchor=W)
		self.rg_password=Entry(self.rg,textvariable=self.Password,show='*')
		self.rg_Password_Again=Label(self.rg,text='Password again',width=12,anchor=W)
		self.rg_password_again=Entry(self.rg,textvariable=self.password_again,show='*')
		self.rg_password.delete(0,'end')
		self.rg_password.insert(0,'4')
		##self.mp_username.bind('<Control-w>',self.app_cikis)
		#self.mp_password.bind('<Return>',self.login_button)

		#========================================
		self.rg_loginbutton=Button(self.rg,text='Login',padx=50,command=self.login_button)
		self.rg_loginbutton.bind('<space>',lambda a:'break')
		self.rg_registerbutton=Button(self.rg,text='Register',padx=45,command=self.check_credentials)
		#========================================
		self.rg_welcome.grid(row=0,columnspan=2,padx=10,pady=10)
		self.rg_Username.grid(row=1,column=0,padx=5,pady=5)
		self.rg_username.grid(row=1,column=1,padx=5)
		self.rg_Password.grid(row=2,column=0,padx=5,pady=5)
		self.rg_Password_Again.grid(row=3,column=0)
		self.rg_password_again.grid(row=3,column=1)
		self.rg_password.grid(row=2,column=1,padx=5)
		# self.rg_loginbutton.grid(row=3,columnspan=2,padx=15,pady=5)
		self.rg_registerbutton.grid(row=4,columnspan=2,padx=15,pady=5)
		self.rg_username.focus()
		self.rg.pack(pady=100)
	def check_credentials(self):

		# print(self.Password.get(),self.password_again.get())
		if self.Password.get()!=self.password_again.get():
			messagebox.showinfo('Hata','parola eslesmiyor')
		else:
			try:
				reg=self.server_rg('register')
				# print(reg)
				if reg=='success':
					self.rg.destroy()
					self.main_screen()
				if reg=='Fail':
					messagebox.showinfo('Hata','Kayit tamamlanamadi')
			except :
				messagebox.showinfo('Hata','server error')
	def main_screen(self):
		try:
			if self.rg:
				self.rg.destroy()
		except :
			print('deneme')
		self.mp=Frame(self.window,bg='black')
		self.mp_welcome=Label(self.mp,
			text='Welcome The Tenfinger App',fg='lime',bg='blue')
		
		#=======================================
		self.mp_Username=Label(self.mp,text="Email")
		self.mp_username=Entry(self.mp,textvariable=self.Username)
		self.mp_username.delete(0,'end')
		self.mp_username.insert(0,'4')

		self.mp_Password=Label(self.mp,text="Password")
		self.mp_password=Entry(self.mp,textvariable=self.Password,show='*')
		self.mp_password.delete(0,'end')
		self.mp_password.insert(0,'4')
		##self.mp_username.bind('<Control-w>',self.app_cikis)
		#self.mp_password.bind('<Return>',self.login_button)

		#========================================
		self.mp_loginbutton=Button(self.mp,text='Login',padx=50,command=self.login_button)
		self.mp_loginbutton.bind('<space>',self.login_button)
		self.mp_registerbutton=Button(self.mp,text='Register',padx=45,command=self.register_page)
		#========================================
		self.mp_welcome.grid(row=0,columnspan=2,padx=10,pady=10)
		self.mp_Username.grid(row=1,column=0,padx=5,pady=5)
		self.mp_username.grid(row=1,column=1,padx=5)
		self.mp_Password.grid(row=2,column=0,padx=5,pady=5)
		self.mp_password.grid(row=2,column=1,padx=5)
		self.mp_loginbutton.grid(row=3,columnspan=2,padx=15,pady=5)
		self.mp_registerbutton.grid(row=4,columnspan=2,padx=15,pady=5)
		self.mp_username.focus()
		self.mp.pack(pady=100)

	def login_button(self):
		self.server_connect()
		self.client_flag=True
		Thread(target=self.guncelle).start()
		# peers=Thread(target=self.peer_info)
		# peers.daemon = True
		# peers.start()
		
		log=self.server_rg('login')
		if log=='success':
			self.mp.destroy()
			self.chat_screen()
		elif log=='Fail':
			messagebox.showinfo('hata','giris bilgileri yanlis')	
			
	
	def buton_cikis(self):
		sys.exit()
	def chat_screen(self):
		self.send_ark=''
		# self.menu_frame = Toplevel(self.window)
		# self.menu_frame.overrideredirect(True)
		# self.menu_frame.attributes('-topmost', True)
		self.menubar=Menu(self.window)
		# self.window.overrideredirect(1)
		name=Menu(self.menubar,tearoff=0)
		dropdownmen=Menu(self.menubar,tearoff=0)
		dropdownmen.add_command(label='Cikis',command=self.buton_cikis)

		dropdownmen1=Menu(self.menubar,tearoff=0)
		dropdownmen1.add_command(label='text insert')
		self.menubar.add_cascade(label=self.Username.get())
		self.menubar.add_cascade(label='cikis',menu=dropdownmen)
		# self.menubar.add_cascade(label='Edit',menu=dropdownmen1)
		
		# self.menu_frame.attributes('-topmost', False)
		self.window.config(menu=self.menubar)

		self.arkadaslar=Frame(self.window,bg='green',width=200,height=300)
		self.arkadas_label=Label(self.arkadaslar,fg='red',text='   Arkadaslar',anchor=W,justify='left',height=1,width=28)
		self.ark_ekle_btn=Button(self.arkadaslar,width=5,text='+',fg='green',bd=0,command=self.ark_ekle_btn)
		self.list1=Listbox(self.arkadaslar,height=17,width=40)
		self.list1.bind("<<ListboxSelect>>",self.lst1_clk)
		self.sbr1=Scrollbar(self.arkadaslar)
		self.sbr1.config(command=self.list1.yview)
		self.list1.config(yscrollcommand=self.sbr1.set)
		self.ark_lst_guncelle()

		
		self.ark_ekle_btn.grid(row=0,column=1)
		self.arkadas_label.grid(row=0,column=0)
		self.list1.grid(row=1,column=0,columnspan=2,sticky=W)
		self.sbr1.grid(row=1,column=1,sticky='nes',pady=2)

		
		self.grb=Frame(self.window,bg='green',width=200,height=300)
		self.grublar_label=Label(self.grb,fg='red',text='   Grublar',anchor=W,justify='left',height=1,width=28)
		self.grb_ekle_btn=Button(self.grb,text='+',width=5,bd=0,command=self.grb_ekle_btn)
		self.list2=Listbox(self.grb,height=17,width=40)
		self.list2.bind("<<ListboxSelect>>",self.lst2_clk)
		self.sbr2=Scrollbar(self.grb)
		self.sbr2.config(command=self.list2.yview)
		self.list2.config(yscrollcommand=self.sbr2.set)
		for i in grb_lst:
			self.list2.insert(END,'grub'+str(i))
		
		
		self.grb_ekle_btn.grid(row=0,column=1)
		self.grublar_label.grid(row=0,column=0)
		self.list2.grid(row=1,column=0,columnspan=2,sticky=W)
		self.sbr2.grid(row=1,column=1,sticky='nes',pady=2)



		self.mesaj_pane=[]
		self.msj=Frame(self.window,bg='green',width=600,height=600)
		self.msj_lbl1=Text(self.msj,width=66,height=33,bg='#eeffee',bd=0)
		self.mesaj_pane.append(self.msj_lbl1)
		self.msj_lbl_scl=Scrollbar(self.msj)
		self.msj_lbl_scl.config(command=self.msj_lbl1.yview)
		self.msj_lbl1.configure(yscrollcommand=self.msj_lbl_scl.set)

		self.msj_box=Text(self.msj,width=60,height=2)
		self.mesaj_pane.append(self.msj_box)
		self.mjs_btn=Button(self.msj,width=8,height=4,bd=0,text='send',command=self.msg_gonder)
		self.msj_box_scl=Scrollbar(self.msj,command=self.msj_box.yview,orient=VERTICAL)
		self.mesaj_pane.append(self.mjs_btn)
		self.msj_box.configure(yscrollcommand=self.msj_box_scl.set)
		# self.msj_box.bind('<Return>',self.msg_gonder)
		# self.send_btn=Button(self.msj,anchor='e',height=10,text='send',fg='yellow',bd=1,command=self.msg_gonder)
		for item in self.mesaj_pane:
			state='state'
			item[state]='disable'

		##textbox will be added
		# self.sbr3=Scrollbar(self.msj)
		# self.sbr3.config(command=self.msj.yview)
		# self.msj.config(yscrollcommand=self.sbr3.set)
		
		self.msj_lbl_scl.grid(row=0,column=1,sticky='nes')
		self.msj_lbl1.grid(row=0,column=0,columnspan=2,sticky='nws')
		# self.msj_lbl2.grid(row=0,column=1)
		# self.msj_lbl.pack(anchor='n')
		# self.send_btn.grid(row=1,column=0)
		self.mjs_btn.grid(row=1,column=1,sticky=E)
		self.msj_box_scl.grid(row=1,column=0,sticky="nes")
		self.msj_box.grid(row=1,column=0,sticky='nws')
		
		# self.msj_box.pack(anchor='s')
		
		
	
		self.arkadaslar.grid(row=0,column=0,sticky='n')				
		self.grb.grid(row=1,column=0)
		# self.msj.config(state=DISABLED)
		# print(help(self.msj.config))

		self.msj.grid(row=0,column=1,rowspan=2)

		


if __name__=='__main__':
	app=Tk()
	chat_app=Chat_App(app)
	app.mainloop()


