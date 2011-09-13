#!/usr/bin/python

import math
import Image

c40="... 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
texte="... 0123456789abcdefghijklmnopqrstuvwxyz"
s01="".join([chr(i) for i in range(32)])
s02="".join([chr(i) for i in range(33,96)])
s03="".join([chr(i) for i in [96]+range(65,91)+range(123,128)])

class DataMatrix:
	def mul(self,a,b):
		if a==0 or b==0: m=0
		else: m=self.alog[(self.log[a]+self.log[b])%255]
		return m
	def __init__(self, txt):
		self.txt=txt
		self.data=[]
		self.mode="ASCII"
		self.alog={0:1}
		self.log={1:0}
		for i in range(1,256):
			a=2*self.alog[i-1]
			if a>=256: self.alog[i]=a^301
			else: self.alog[i]=a
			self.log[self.alog[i]]=i
		self.log[1]=0
		self.nrow=0
		self.ncol=0
		self.status=0
	def PolyRS(self,n):
		self.poly=[1]+[0]*n
		for i in range(1,n+1):
			self.poly[i]=self.poly[i-1]
			for j in range(i-1,0,-1):
				self.poly[j]=self.poly[j-1]^self.mul(self.poly[j],self.alog[i])
			self.poly[0]=self.mul(self.poly[0],self.alog[i])

	def RS(self,nc):
		wd=[0]*(nc+1)
		nd=len(self.data)
		n=self.getSize()
		# coeff poly
		self.PolyRS(nc)
		print("Polynome: ",self.poly)
		for i in range(nd):
			k=wd[0]^self.data[i]
			for j in range(nc):
				wd[j]=wd[j+1]^self.mul(k,self.poly[nc-j-1])
		self.data+=wd[:-1]

	def module(self,row,col,c,bit):
		if row<0:
			row+=self.nrow
			col+=4-((self.nrow+4)%8)
		if col<0:
			col+=self.ncol
			row+=4-((self.ncol+4)%8)
		self.array[row*self.ncol+col]=10*c+bit

	def utah(self, row, col, c):
		self.module(row-2,col-2,c,1)
		self.module(row-2,col-1,c,2)
		self.module(row-1,col-2,c,3)
		self.module(row-1,col-1,c,4)
		self.module(row-1,col,c,5)
		self.module(row,col-2,c,6)
		self.module(row,col-1,c,7)
		self.module(row,col,c,8)
	def corner1(self,c):
		self.module(self.nrow-1,0,c,1)
		self.module(self.nrow-1,1,c,2)
		self.module(self.nrow-1,2,c,3)
		self.module(0,self.ncol-2,c,4)
		self.module(0,self.ncol-1,c,5)
		self.module(1,self.ncol-1,c,6)
		self.module(2,self.ncol-1,c,7)
		self.module(3,self.ncol-1,c,8)
	def corner2(self,c):
		self.module(self.nrow-3,0,c,1)
		self.module(self.nrow-2,0,c,2)
		self.module(self.nrow-1,0,c,3)
		self.module(0,self.ncol-4,c,4)
		self.module(0,self.ncol-3,c,5)
		self.module(0,self.ncol-2,c,6)
		self.module(0,self.ncol-1,c,7)
		self.module(1,self.ncol-1,c,8)
	def corner3(self,c):
		self.module(self.nrow-3,0,c,1)
		self.module(self.nrow-2,0,c,2)
		self.module(self.nrow-1,0,c,3)
		self.module(0,self.ncol-2,c,4)
		self.module(0,self.ncol-1,c,5)
		self.module(1,self.ncol-1,c,6)
		self.module(2,self.ncol-1,c,7)
		self.module(3,self.ncol-1,c,8)
	def corner4(self,c):
		self.module(self.nrow-1,0,c,1)
		self.module(self.nrow-1,self.ncol-1,c,2)
		self.module(0,self.ncol-3,c,3)
		self.module(0,self.ncol-2,c,4)
		self.module(0,self.ncol-1,c,5)
		self.module(1,self.ncol-3,c,6)
		self.module(1,self.ncol-2,c,7)
		self.module(1,self.ncol-1,c,8)
	def mapDataMatrix(self):
		self.array=[0]*(self.nrow*self.ncol)
		c=1
		row=4
		col=0
		while True:
			if (row==self.nrow) and (col==0):
				self.corner1(c)
				c+=1
			if (row==self.nrow-2) and (col==0) and (self.ncol%4):
				self.corner2(c)
				c+=1
			if (row==self.nrow-2) and (col==0) and (self.ncol%8==4):
				self.corner3(c)
				c+=1
			if (row==self.nrow+4) and (col==2) and (not(self.ncol%8)):
				self.corner4(c)
				c+=1
			while True:
				if (row<self.nrow) and (col>=0) and (not(self.array[row*self.ncol+col])):
					self.utah(row,col,c)
					c+=1
				row -= 2
				col += 2
				if not ((row>=0) and (col<self.ncol)): break
			row += 1
			col += 3
			while True:
				if (row>=0) and (col<self.ncol) and (not(self.array[row*self.ncol+col])):
					self.utah(row,col,c)
					c+=1
				row += 2
				col -= 2
				if not ((row<self.nrow) and (col>=0)): break
			row += 3
			col += 1
			if not ((row <self.nrow) or (col < self.ncol)): break
		if not self.array[self.nrow*self.ncol-1]:
			self.array[self.nrow*self.ncol-1]=1 
			self.array[self.nrow*self.ncol-2]=1

	def fill(self):
		a=self.array[:]
		for d in enumerate(self.data):
			v=d[1]
			for i in range(7,-1,-1):
				kk=10*(d[0]+1)+8-i
				k=a.index(kk)
				if v>=2**i:
					v-=2**i
					a[k]=1
				else:
					a[k]=0
		self.matrix=a

	def encodeASCII(self,data):
		d=[]
		l=-1
		for i in range(len(data)):
			if (data[i] in "0123456789"):
				if l==-1:
					l=int(data[i])
				else:
					d.append(130+l*10+int(data[i]))
					l=-1
			else:
				if l==-1: d.append(ord(data[i])+1)
				else:
					d.append(48+l)
					d.append(ord(data[i])+1)
		if l>=0: d.append(49+l)
		self.data+=d
	def encodeTEXT(self,data):
		global texte,s01,s02
		s03="".join([chr(i) for i in [96]+range(65,91)+range(123,128)])
		v=[]
		for d in data:
			if d=='.': v+=[0,13]
			elif d in texte: v.append(texte.index(d))
			elif d in s01: v+=[0,s01.index(d)]
			elif d in s02: v+=[1,s02.index(d)]
			elif d in s03: v+=[2,s03.index(d)]
			else: print("Char %s not found. Droped"%(d))
		d=[]
		if len(v)%3!=0: v+=[0]*(3-len(v)%3)
		print ("TEXT-Data RAW (ie. 1 code per char)",v)
		for i in range(0,len(v),3):
			k=1
			for j in range(3):
				k+=v[i+j]*40**(2-j)
			d+=[k/256,k%256]
		self.data+=d
	def encodeC40(self,data):
		global c40,s01,d02
		s03="".join([chr(i) for i in range(96,128)])
		v=[]
		for d in data:
			if d=='.': v+=[0,13]
			elif d in c40: v.append(c40.index(d))
			elif d in s01: v+=[0,s01.index(d)]
			elif d in s02: v+=[1,s02.index(d)]
			elif d in s03: v+=[2,s03.index(d)]
			else: print("Char %s not found. Droped"%(d))
		d=[]
		if len(v)%3!=0: v+=[0]*(3-len(v)%3)
		for i in range(0,len(v),3):
			k=1
			for j in range(3):
				k+=v[i+j]*40**(2-j)
			d+=[k/256,k%256]
		self.data+=d
	def getSize(self):
		dataLEN=len(self.data)
		s={
			(8,8):(3,5,(1,1),1),
			(10,10):(5,7,(1,1),1),
			(12,12):(8,10,(1,1),1),
			(14,14):(12,12,(1,1),1),
			(16,16):(18,14,(1,1),1),
			(18,18):(22,18,(1,1),1),
			(20,20):(30,20,(1,1),1),
			(22,22):(36,24,(1,1),1),
			(24,24):(44,28,(1,1),1),
			(28,28):(62,36,(2,2),1),
			(32,32):(86,42,(2,2),1),
			(36,36):(114,48,(2,2),1),
			(40,40):(144,56,(2,2),1),
			(44,44):(174,68,(2,2),1)
			}
		md=-1
		ms=(44,44)
		for x in s:
			if s[x][0]>=dataLEN:
				if s[x][0]<md or md==-1:
					md=s[x][0]
					ms=x
		return [ms,s[ms]]
	def encode(self):
		# TODO
		pass
	def switchC40(self):
		if self.mode=="ASCII": self.data.append(230)
		elif self.mode=="C40": pass
		else: self.data+=[254,230]
		self.mode="C40"
	def switchASCII(self):
		if self.mode=="ASCII": pass
		else: self.data.append(254)
		self.mode="ASCII"
	def switchTEXT(self):
		if self.mode=="TEXT": pass
		elif self.mode=="ASCII": self.data.append(239)
		else: self.data+=[254,239]
		self.mode="TEXT"
	def showData(self):
		print(self.data)
	def calculateDM(self):
		self.display=[]
		es=[self.ncol/self.dataRegion[0],self.nrow/self.dataRegion[1]]
		for yy in range(self.dataRegion[0]):
			self.display+=[1]+[0,1]*(self.dataRegion[1]/2+self.ncol/2)+[0]
			for y in range(es[1]):
				for xx in range(self.dataRegion[1]):
					i=(yy*es[0]+y)*self.ncol+xx*es[1]
					self.display+=[1]+self.matrix[i:i+es[0]]+[y%2]
			self.display+=[1]*(self.ncol+2*self.dataRegion[1])
	def showDM(self):
		im=Image.new("1",(self.ncol+2*self.dataRegion[1],self.nrow+2*self.dataRegion[0]))
		im.putdata([1-z for z in self.display])
		# zoom
		z=8
		im=im.resize((z*(self.ncol+2*self.dataRegion[1]),z*(self.nrow+2*self.dataRegion[0])))
		im.show()
	def process(self):
		n=self.getSize()
		self.ncol=n[0][0]
		self.nrow=n[0][1]
		self.dataRegion=n[1][2]
		# Padd data
		if n[1][0]>len(self.data): self.data+=[254]
		self.data+=[129]*(n[1][0]-len(self.data))
		# Calculate Read-Solomon code
		self.RS(n[1][1])
		print("Data: ",self.data)
		# Calculate Matrix => self.array
		self.mapDataMatrix()
		self.fill()
		self.calculateDM()
		self.showDM()
	def optimizeSwitch(self, txt):
				# TODO
		pass
	def optimizeEncode(self, txt):
				# TODO: complete function
		dig="0123456789"
		i=0
		while i<len(txt):
			if self.mode=="ASCII":
				if i+1<len(txt):
					if (txt[i] in dig) and (txt[i+1] in dig):
												self.data+=[130+int(txt[i:i+2])]
												i+=2
				else: self.data+=ord(txt[i])+1
				
		
d=DataMatrix("")
d.switchTEXT()
d.encodeTEXT("bonjour!")
d.showData()
d.process()
