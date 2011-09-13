#!/usr/bin/python

import math
import Image

c40="... 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
texte="... 0123456789abcdefghijklmnopqrstuvwxyz"
s01="".join([chr(i) for i in range(32)])
s02="".join([chr(i) for i in range(33,96)])
s03="".join([chr(i) for i in [96]+range(65,91)+range(123,128)])

def mul(self,a,b):
	global alog,log
	if a==0 or b==0: m=0
	else: m=alog[(log[a]+log[b])%255]
	return m

class DataMatrix:
	def __init__(self, data):
		self.txt=data
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
				self.poly[j]=self.poly[j-1]^mul(self.poly[j],self.alog[i])
			self.poly[0]=mul(self.poly[0],self.alog[i])

	def RS(self):
		wd=[0]*(nc+1)
		nd=len(data)
		# coeff poly
		c=PolyUnroot(PolyRS(nc))
		print("Polynome: ",c)
		for i in range(nd):
			k=wd[0]^data[i]
			for j in range(nc):
				wd[j]=wd[j+1]^mul(k,c[nc-j-1])
		return data+wd[:-1]

	def module(array,row,col,c,bit,nrow,ncol):
		if row<0:
			row+=nrow
			col+=4-((nrow+4)%8)
		if col<0:
			col+=ncol
			row+=4-((ncol+4)%8)
		array[row*ncol+col]=10*c+bit
		return array

	def utah(self, row, col, c):
		self.module(row-2,col-2,c,1)
		self.module(row-2,col-1,c,2)
		self.module(row-1,col-2,c,3)
		self.module(row-1,col-1,c,4)
		self.module(row-1,col,c,5)
		self.module(row,col-2,c,6)
		self.module(row,col-1,c,7)
		self.module(row,col,c,8)
	def corner1(c):
		self.module(self.nrow-1,0,c,1)
		self.module(self.nrow-1,1,c,2)
		self.module(self.nrow-1,2,c,3)
		self.module(0,self.ncol-2,c,4)
		self.module(0,self.ncol-1,c,5)
		self.module(1,self.ncol-1,c,6)
		self.module(2,self.ncol-1,c,7)
		self.module(3,self.ncol-1,c,8)
	def corner2(c):
		self.module(self.nrow-3,0,c,1)
		self.module(self.nrow-2,0,c,2)
		self.module(self.nrow-1,0,c,3)
		self.module(0,self.ncol-4,c,4)
		self.module(0,self.ncol-3,c,5)
		self.module(0,self.ncol-2,c,6)
		self.module(0,self.ncol-1,c,7)
		self.module(1,self.ncol-1,c,8)
	def corner3(c):
		self.module(self.nrow-3,0,c,1)
		self.module(self.nrow-2,0,c,2)
		self.module(self.nrow-1,0,c,3)
		self.module(0,self.ncol-2,c,4)
		self.module(0,self.ncol-1,c,5)
		self.module(1,self.ncol-1,c,6)
		self.module(2,self.ncol-1,c,7)
		self.module(3,self.ncol-1,c,8)
	def corner4(c):
		self.module(self.nrow-1,0,c,1)
		self.module(self.nrow-1,self.ncol-1,c,2)
		self.module(0,self.ncol-3,c,3)
		self.module(0,self.ncol-2,c,4)
		self.module(0,self.ncol-1,c,5)
		self.module(1,self.ncol-3,c,6)
		self.module(1,self.ncol-2,c,7)
		self.module(1,self.ncol-1,c,8)
	def mapDataMatrix(self):
		array=[0]*(self.nrow*self.ncol)
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

	def show(self):
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
		dm=[0]+[1,0]*(self.ncol/2)+[1]
		for y in range(self.nrow):
			dm+=[0]+[1-z for z in a[self.ncol*y:self.ncol*(y+1)]]+[1-(y%2)]
		dm+=[0]*(self.ncol+1)
		im=Image.new("1",(self.ncol+2,self.nrow+2))
		im.putdata(dm)
		im.save("dm.png","PNG")

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
		return d
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
		for i in range(0,len(v),3):
			k=1
			for j in range(3):
				k+=v[i+j]*40**(2-j)
			d+=[k/256,k%256]
		return d
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
		return d
	def getSize(self):
		s=[8,10,12,14,16,18,20,22,24]
		d=[3,5,8,12,18,22,30,36,44]
		rs=[5,7,10,12,14,18,20,24,28]
		for i in d:
			if i>=dataLEN:
				k=d.index(i)
				return [s[k],i,rs[k]]
		return 0
	def encode(self):
		self.data=[]
		mode="ASCII"
		last=0
		lt="none"
		for x in self.txt:
			if x in "0123456789":
				if lt=="num" and mode="ASCII":
					self.data
d=DataMatrix("Ceci est un test")
d.encode()
