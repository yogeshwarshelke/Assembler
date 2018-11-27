import sys,re
from opcode import *
from data import *
sy_names = []#TO store symbol names
sy_size = []#TO store symbol  types size
sy_totalsize = []#TO store symbol (require memory size in byte) 
sy_value = []#TO store symbol value
sy_lineno = []#TO store symbols line no
sy_address=[]#to store address of the symbol
temp2 = []
k = 1
sy_type= []#TO store symbol type
lit = []#to store literal value
lithex = []# to store values of hex of literal
reg=['eax','ebx','ecx','edx','esi','edi','esp','ebp','ax','bx','cx','dx','sp','bp','si','di','al','bl','cl','dl','ah','bh','ch','dh']
lenreg=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
ck=['1','2','3','4','5','6','7','8','9','0']
reglist=reglist_Data()#for register list to check type of register
op_data=opcode_Data()#for access opcode data to instruction
reglsth=reglsthh()#for to check code for reg
mod=modd()#for mod check
section=['section .data','section .bss','section .text']
fp=open("sample.asm","r")
fp1=open("LST.txt","w")
fp2=open("demo.txt","w")
def check(synames,sylist,l_no):
	if synames in sylist:
		print 'LINE ',l_no,":symbole redefin",'"',synames,'"'
		sys.exit()
	elif synames[0] in ck:
		print 'LINE ',l_no,":symbole name not correct",'"',synames,'"'
		sys.exit()
	else:
		return 1
def hexconvert(sum1):#TO calculate hexadecimal value
	k=hex(sum1)
	k=k[2::]
	k=k.upper()
	return k

def addforarray(sum1):
	k=hexconvert(sum1)
	str1='00000000'
	str1= '0' * (8-len(k))
	str1=str1+str(k)
	return str1
def hex_convert(sum1):#TO calculate address for instruction in hexadecimal
	str1='0E1B1000'
	k=hex(sum1)
	k=k[2::]
	k=k.upper()
	str1= '0' * (8-len(k))
	str1=str1+str(k)
	return str1

def get_int_line(z):#TO get lst of synbol in string
	str2=""	
	for i in range(len(z)):
		temp=hexconvert(z[i])
		if(len(temp)==1):
			str1= '0' * (7-len(temp))
			str2=str2+'0'+temp+str1
		else:	
			str1= '0' * (8-len(temp))
			str2=str2+temp+str1
	return str2
def get_db_line(z):#TO get lst of synbol in string
	str2=""	
	for i in range(len(z)):
		k=hex(ord(z[i]))
		k=k[2::]
		k=k.upper()
		str2=str2+k	
	return str2

def calsize(l_no,name,s_list,temp,type_size,sum1,line,stp):
	q=sum1	
	l =temp.count(',')						
	l = (l+1)*type_size
	sum1=sum1+l	
	t=hex_convert(sum1-l)
	sy_address.append(str(t))
	sy_lineno.append(str(l_no))				
	sy_names.append(name)				
	sy_size.append(str(type_size))
	sy_totalsize.append(str(l))
	sy_type.append(str(stp))
	z=map(int, re.findall(r'\d+', s_list[0]))
	sy_value.append(z)
	st=get_int_line(z)
	if(len(z)==2):
		fp1.write('\t'+t+' '+st+'\t'+line[0:(len(line)-1)]+"\n")
	elif(len(z)==1):
		fp1.write('\t'+t+' '+st+'\t\t'+line[0:(len(line)-1)]+"\n")
	else:
		j=18
		i=0
		q=9
		while(i<=len(st)):
			if(j<len(st)):
				t=addforarray(q-9)
				if(i==0):
					fp1.write('\t'+t+' '+st[i:j]+'-'+'\t'+line[0:(len(line)-1)]+"\n")
				else:
					fp1.write('\t'+t+' '+st[i:j]+'-'+"\n")
				q=q+9
			else:
				t=addforarray(q-9) 	
				fp1.write('\t'+t+' '+st[i:j]+"\n")
			i=j+1;
			j=i+18;		
	return sum1
def calsize_db(l_no,name,temp,val,type_size,sum1,line,stp):
	q=sum1	
	k=''.join(temp)
	c = 1
	if(k[c-1]=="'"):
		while(k[c]!="'"):
			c = c + 1
	if(k[c-1]=='"'):
		while(k[c]!='"'):
			c = c + 1
	sy_totalsize.append(str(c-1))
	sum1=sum1+(c-1)+2	
	t=hex_convert(sum1-(c-1)+2)
	sy_address.append(str(t))
	if('10,0' in val):
		sy_value.append(val[1:(len(val)-6)])
	elif(',10' in val):
		sy_value.append(val[1:(len(val)-4)])
	else:
		sy_value.append(val[1:(len(val)-1)])
	sy_lineno.append(str(l_no))				
	sy_names.append(name)	
	sy_size.append(str(type_size))
	sy_type.append(str(stp))
	if('10,0' in val):
		temp=get_db_line(val[1:(len(val)-6)])
		temp=temp+'0A00'	
	else:
		temp=get_db_line(val[1:(len(val)-6)])
	if(len(temp)<16):
		fp1.write('\t'+t+' '+temp+'\t\t'+line[0:(len(line)-1)]+"\n")
	else:
		j=18
		i=0
		q=q+9
		while(i<=len(temp)):
			if(j<len(temp)):
				t=hex_convert(q-9)
				if(i==0):
					fp1.write('\t'+t+' '+temp[i:j]+'-'+'\t'+line[0:(len(line)-1)]+"\n")
				else:
					fp1.write('\t'+t+' '+temp[i:j]+'-'+"\n")
				q=q+9  		
			else:
				t=hex_convert(q-9)
				fp1.write('\t'+t+' '+temp[i:j]+"\n")
			i=j;	
			j=i+18;		
	return sum1
def cal_other(l_no,name,type_size,val,sum1,line,stp):
	q=sum1
	k=type_size*int(val)
	sy_value.append(val)
	sy_lineno.append(str(l_no))				
	sy_names.append(name)	
	sy_size.append(str(type_size))
	sy_totalsize.append(str(k))
	sum1=sum1+k
	t=hex_convert(sum1-k)
	sy_address.append(str(t))
	sy_type.append(str(stp))
	fp1.write('\t'+t+' <res '+(hex_convert(k))+'>\t\t'+line[0:(len(line))-1]+'\n')
	return sum1

def table(line,l_no,sum1):
	for i in range(len(section)):
		if section[i] in line:
			fp1.write('\n0E1B100'+str(i)+' <'+section[i]+' >\n\n')
			return 0
	if('global' in line or 'extern' in line):
		fp1.write('\t\t\t\t'+line[0:(len(line))-1]+"\n")
	list1=line.split()
	for i in range(len(list1)):
		if (list1[i]== 'dd'):
			if(check(list1[0],sy_names,l_no)):
				s_list=list1[2].split()
				z=calsize(l_no,list1[0],s_list,list1[2],4,sum1,line,list1[i])
				return z				
		if (list1[i]== 'dq'):
			if(check(list1[0],sy_names,l_no)):
				s_list=list1[2].split()
				z=calsize(l_no,list1[0],s_list,list1[2],8,sum1,line,list1[i])
				return z
		if (list1[i]== 'dw'):
			if(check(list1[0],sy_names,l_no)):
				s_list=list1[2].split()
				z=calsize(l_no,list1[0],s_list,list1[2],2,sum1,line,list1[i])	
				return z
		if (list1[i]== 'db'):
			if(check(list1[0],sy_names,l_no)):
				k=list1[i+1:]
				val=' '.join(k)
				z=calsize_db(l_no,list1[0],list1[i+1:],val,1,sum1,line,list1[i])
				return z
		
		if (list1[i]== 'resd'):
			if(check(list1[0],sy_names,l_no)):
				z=cal_other(l_no,list1[0],4,list1[2],sum1,line,list1[i])
				return z
		if (list1[i]== 'resq'):
			if(check(list1[0],sy_names,l_no)):
				z=cal_other(l_no,list1[0],8,list1[2],sum1,line,list1[i])
				return z
		if (list1[i]== 'resw'):
			if(check(list1[0],sy_names,l_no)):
				z=cal_other(l_no,list1[0],2,list1[2],sum1,line,list1[i])
				return z
		if (list1[i]== 'resb'):
			if(check(list1[0],sy_names,l_no)):
				z=cal_other(l_no,list1[0],1,list1[2],sum1,line,list1[i])
				return z
	return sum1
def create_Symbol_Table():
									
	sum1 = 0					
	l_no = 1
	line=fp.readline()
	while(line!=""):
		sum1=table(line,l_no,sum1)
		
		l_no = l_no + 1
		line=fp.readline()

def display2():
	fp2.write('\n\n < symbol table > :\n\n')
	for i in range(len(sy_names)):
		fp2.write('\t'+sy_lineno[i]+'\t'+sy_address[i]+'\t'+sy_names[i]+'\t'+sy_size[i]+'\t'+sy_totalsize[i]+'\t'+sy_type[i]+'\t'+str(sy_value[i])+"\n")

def checkreg(opr):#To check register type
	for i in reglist:
		if opr in reglist[i]:
			return i
def checkmem(opr):#To check memory type
	i =0
	temp=0
	while(sy_names[i] != opr):
		i= i+1
	temp =int(sy_totalsize[i]) * 8
	if( temp > 0 and  temp <256):	
		return 8
	elif( temp > 256 and  temp <65536):
		return 16
	elif( temp > 65536 and  temp <4294967296):
		return 32

def checkopcode(string):#To check opcode of instruction
	for i in opcode_data:
		if string in opcode_data[i]:
			return i
def checkmod(str1):
	for i in mod:
		if str1 in mod[i]:
			return i
	
def memadd_rev(sum1):#TO calculate address for instruction in hexadecimal		
	str1='000000'	
	k=sum1[6:]
	return k+str1

def lit_hexconvert(a):#To calculate address of literal in hexadecimal for lst
	str2=""
	z=hexconvert(a)
	if(len(z)==1):
		str1= '0' * 6
		str2='0'+z+str1
		return str2
	else:
		str1='0' * (8-(len(z)))
		str2=z+str1
		return str2
def mod_calculator(op1,op2,tp):#to calculate mod 
	for i in reglsth:
		if op1 in reglsth[i]:
			str1=i
	for j in reglsth:
		if op2 in reglsth[j]:
			str2=j
	final=tp+str1+str2
	return (str(hex(int(final[0:4],2))))[2::].upper()+str(hex(int(final[4:8],2)))[2::].upper()
def sympos(sym):#to find position of symbol
	i=0
	while(sy_names[i] != sym):
		i = i+1
	return i
def mod_calculatorlit(op1,op2,tp):#mod calculator for literal
	for i in reglsth:
		if op1 in reglsth[i]:
			str1=i
	return str(int(final[0:4],2))+str(int(final[4:8],2))

def calline(f,s,lno,name,sum1,line,temp):#TO check instruction type ,address,lieral,memory_type,register_type
	k =0
	i =0
	z=0 
	if f in reg and s in sy_names:#first register second symbol		
		k=sympos(s)
		i=0
		while(reg[i]!=f):
			i=i+1
		if(temp==1):
			sum1=sum1+5
			t=hex_convert(sum1-5)
		else:
			sum1=sum1+6
			t=hex_convert(sum1-6)
		fp1.write(t)
		regtp=checkreg(f)
		mem=checkmem(s)
		string1=name+'_reg'+str(regtp)+'_imm'+str(mem)
		kk=checkopcode(string1)
		fp1.write(' '+str(kk)+'['+memadd_rev(sy_address[k])+']')
		'''fp1.write(' '+'reg'+str(lenreg[i]))
 		fp1.write(','+'sym#'+str(sy_lineno[k]))'''
		fp1.write('\t\t'+line)
		return sum1
	if f in reg and s in reg:#first register second register
		i =0
		while(reg[i]!=f):
			i=i+1
		k =0
		while(reg[k]!=s):
			k=k+1
		if(temp==1):
			sum1=sum1+2
			t=hex_convert(sum1-2)
		else:
			sum1=sum1+2
			t=hex_convert(sum1-2)
		fp1.write(t)
		regtp=checkreg(f)
		regtp2=checkreg(s)
		string1=name+'_reg'+str(regtp)+'_reg'+str(regtp2)
		z=checkopcode(string1)
		fp1.write(' '+str(z))
		'''fp1.write(' '+'reg'+str(lenreg[i]))
		fp1.write(','+'reg'+str(lenreg[k]))'''
		m=checkmod('rr')
		op=mod_calculator(s,f,str(m))
		fp1.write(op)			
		fp1.write('\t\t\t'+line)
		return sum1
	if f in reg and s not in sy_names:#first register second lit
		regtp=checkreg(f)
		while(reg[k]!=f):
			k=k+1
		if(temp==1) and regtp != 8:
			sum1=sum1+5
			t=hex_convert(sum1-5)
		elif (temp==0) and regtp != 8:
			sum1=sum1+3
			t=hex_convert(sum1-3)
		else:
			sum1=sum1+2
			t=hex_convert(sum1-2)	
		fp1.write(t)

		if('dword' in s and str(regtp) == '32'):
			string1=name+'_reg'+str(regtp)+'_mem32'
			z=checkopcode(string1)
			fp1.write(' '+str(z))
		else:
			string1=name+'_reg'+str(regtp)+'_imm8'
			z=checkopcode(string1)
			fp1.write(' '+str(z))	 
		if('dword' in s):
			i =0
			k =0
			if(s[6:len(s)-1] in sy_names):
				k=sympos(s[6])
				fp1.write('['+sy_address[k]+']')
				fp1.write('\t\t'+line)	
			else:
				t=s[6:len(s)-1].split('+')
				if (t[0] in sy_names and t[1] in reg) or (t[0] in reg and t[1] in sy_names):
					m=checkmod('rm16')
					if(t[0] in sy_names and t[1] in reg):					
						op=mod_calculator(f,t[1],str(m))
						fp1.write(op)
						fp1.write('['+memadd_rev(sy_address[sympos(t[0])])+']')
						fp1.write('\t\t'+line)
					else:
						op=mod_calculator(f,t[0],str(m))		
						fp1.write(op)
						fp1.write('['+memadd_rev(sy_address[sympos(t[1])])+']')
						fp1.write('\t\t'+line)
				elif(t[0] not in sy_names and t[1] in reg) or (t[0] in reg and t[1] not in  sy_names):
					m=checkmod('rm8')
					if(t[0] in reg and t[1] not in sy_names):
						op=mod_calculator(f,t[0],str(m))
						fp1.write(op)
						fp1.write(hex_convert(int (t[1]))[6::])
					else:
						op=mod_calculator(f,t[1],str(m))
						fp1.write(op)
						fp1.write(hex_convert(int (t[0]))[6::])
					fp1.write('\t\t\t'+line)	
		else:
			if(len(s)==3 and s[0]=="'"):
				if((ord(s[1])>=65 and ord(s[1])<=90) or (ord(s[1])>=97 and ord(s[1])<=122)):
					if(s[1] not in lit):
						lit.append(str(s[1]))
						lithex.append(hex(ord(s[1])))
						while(lit[i]!=str(s[1])):
							i=i+1
					if(regtp==32):
						z=lit_hexconvert(ord(s[1]))
						fp1.write(z)
						fp1.write('\t\t'+line)
					else:
						z=lit_hexconvert(ord(s[1]))
						fp1.write(z[::6])
						fp1.write('\t\t\t'+line)
			else:	
				if(int(s) not in lit):
					lit.append(int(s))
					lithex.append(hex(int(s)))
				while(lit[i]!=int(s)):
					i=i+1
				z=lit_hexconvert(int(s))
				fp1.write(z)
				fp1.write('\t\t'+line)
		return sum1
	if s in reg and f not in sy_names:#first dword,byte,word second register		
		c =0	
		sum1=sum1+6
		while(reg[c]!=s):
			c=c+1
		t=hex_convert(sum1-6)		
		fp1.write(t)
		regtp=checkreg(s)
		if('dword' in f):
			if('dword' in f and str(regtp) == '32'):
				regtp=checkreg(s)
				string1=name+'_mem32'+'_reg'+str(regtp)
				z=checkopcode(string1)
				fp1.write(' '+str(z))
				k =0
				if (f[6] in sy_names):
					k=sympos(f[6])
				fp1.write('['+sy_address[k]+']')
				fp1.write('\t\t'+line)
			#fp1.write(' '+'dword[sym#'+str(sy_lineno[k])+']')
			#fp1.write(','+'reg'+str(lenreg[c]))
		if('byte' in f):
			if('byte' in f and str(regtp) == '8'):
				regtp=checkreg(s)
				string1=name+'_mem8'+'_reg'+str(regtp)
				z=checkopcode(string1)
				fp1.write(' '+str(z))
			k =0
			if (f[5]+f[6] in sy_names):
				k=sympos(f[5]+f[6])

			fp1.write(' '+'byte[sym#'+str(sy_lineno[k])+']')
			fp1.write(','+'reg'+str(lenreg[c]))

		return sum1
def print_littable():#TO print literal table
	fp2.write('\n\n< literal table > :\n\n')
	for i in range(len(lit)):
		fp2.write('\t'+str(i))
		fp2.write('\t\t'+str(lit[i]))
		fp2.write('\t'+lithex[i])		
		fp2.write("\n")
def table2(line,lno,sum1):# TO make opcode table
	z=0
	if(len(line)!=1):
		if 'main' in line and 'global' not in line:
			fp1.write("\t\t\t\tmain:\n")
			return 0
		list1=line.split()
		for i in range(len(list1)):
			if (list1[i]== 'mov') or (list1[i]== 'add'):
				name=list1[i]
				k=list1[1].replace(',',' ')		
				k1=k.split()		
				if(list1[i]== 'mov'):
					z=calline(k1[0],k1[1],lno,name,sum1,line,1)
					return z
				else:
					z=calline(k1[0],k1[1],lno,name,sum1,line,0)
					return z
			else:
				return sum1
	return sum1
def create_LST():#To create lst
	lno =0	
	sum1 = 0
	fp=open("sample.asm","r")
	line=fp.readline()
	while(line!=""):
		lno = lno + 1	
		temp=table2(line,lno,sum1)
		sum1= temp
		line=fp.readline()
#print_littable()
def addd():
	fp1=open("LST.txt","r")
	l=fp1.readline()
	while(l!=""):
		fp2.write(l)
		l=fp1.readline()
	



def main():
	create_Symbol_Table()#To create symbol table
    	create_LST()#TO create lst part
	fp1.close()
	display2()
	print_littable()
	#addd()
if __name__ == "__main__":
    main()

