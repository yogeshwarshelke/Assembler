import os
import sys
#l_no=0

#temp2 = []
k = 1
sym_type= []#TO store symbol type
fname=sys.argv[1]
fp=open(fname,"r")
fp3=open("symbol.txt","w+")

address=0
address1=0	
address2=0
count1=0 #total size of number present 
count2=0
count3=0	

def table(line,l_no,sum1,a):
	
	
	list1=line.split()
	global address
	global address1
	global address2
	global char
	
	count1=0 #total size of number present 
	count2=0
	count3=0
	
	#count total character or digits--------------------
	for i in range(len(list1)):
		if(list1[i]=='dd' or list1[i]=='dw' or list1[i]=='dq'):
			for j in range(0,len(list1)) :
				count1=list1[j].split(',')
				
			count1=len(count1)
			count1+1
		elif(list1[i]=='db'):
			for j in range(i+1,len(list1)): 
				count1=count1+len(list1[j])
				count2=list1[j].split('"')
				count3=list1[j].split(',')
				
			count2=len(count2)
			count3=len(count3)
			count1=count1-count2-count3-1
	#-------------------------------------------------
		
	for i in range(len(list1)):
		if (list1[i]== 'dd' and i>0):
				#print("%d\t%s\t%s\t%d\t%s\t%s\t%d\t%s\n"%(l_no,list1[i-1],list1[i],count1,'s','define',address,list1[i+1:]))
				fp3.write("%d\t%s\t%s\t%d\t%s\t%s\t%d\t%s\n"%(l_no,list1[i-1],list1[i],count1,'s','define',address,
				list1[i+1:]))
				address=address+4*count1
			
		if (list1[i]== 'dd' and i==0):
				#print("%d\t%s\t%s\t%d\t%s\t%s\t%d\t%s\n"%(l_no,'',list1[i],count1,'s','define',address,list1[i+1:]))
				fp3.write("%d\t%s\t%s\t%d\t%s\t%s\t%d\t%s\n"%(l_no,'',list1[i],count1,'s','define',address,list1[i+1:]))
				address=address+4*count1
											
		if (list1[i]== 'dq' and i>0):
				#print("%d\t%s\t%s\t%d\t%s\t%s\t%d\t%s\n"%(l_no,list1[i-1],list1[i],count1,'s','define',address,list1[i+1:]))
				fp3.write("%d\t%s\t%s\t%d\t%s\t%s\t%d\t%s\n"%(l_no,list1[i-1],list1[i],count1,'s','define',address,
				list1[i+1:]))
				address=address+8*count1
				
		if (list1[i]== 'dq' and i==0):
				#print("%d\t%s\t%s\t%d\t%s\t%s\t%d\t%s\n"%(l_no,'',list1[i],count1,'s','define',address,list1[i+1:]))
				fp3.write("%d\t%s\t%s\t%d\t%s\t%s\t%d\t%s\n"%(l_no,'',list1[i],count1,'s','define',address,list1[i+1:]))
				address=address+8*count1
		if (list1[i]== 'dw' and i>0):
				#print("%d\t%s\t%s\t%d\t%s\t%s\t%d\t%s\n"%(l_no,list1[i-1],list1[i],count1,'s','define',address,list1[i+1:]))
				fp3.write("%d\t%s\t%s\t%d\t%s\t%s\t%d\t%s\n"%(l_no,list1[i-1],list1[i],count1,'s','define',address,
				list1[i+1:]))
				address=address+2*count1
				
		if (list1[i]== 'dw' and i==0):		
				#print("%d\t%s\t%s\t%d\t%s\t%s\t%d\t%s\n"%(l_no,'',list1[i],count1,'s','define',address,list1[i+1:]))
				fp3.write("%d\t%s\t%s\t%d\t%s\t%s\t%d\t%s\n"%(l_no,'',list1[i],count1,'s','define',address,list1[i+1:]))
				address=address+2*count1
		
		if (list1[i]== 'db') and i>0:
			#if(check(list1[0],sym_names,l_no)):
				k=list1[i+1:]
				val=' '.join(k)
				#print("%d\t%s\t%s\t%d\t%s\t%s\t%d\t%s\n"%(l_no,list1[i-1],list1[i],count1,'s','define',address,val))
				fp3.write("%d\t%s\t%s\t%d\t%s\t%s\t%d\t%s\n"%(l_no,list1[i-1],list1[i],count1,'s','define',address,val))
				address=address+count1		
			#	z=calsize_db(l_no,list1[0],list1[i+1:],val,1,sum1,line,list1[i])
				#return z
		if (list1[i]== 'db') and i==0:	
				k=list1[i+1:]
				val=' '.join(k)	
				#print("%d\t%s\t%s\t%d\t%s\t%s\t%d\t%s\n"%(l_no,'',list1[i],count1,'s','define',address,val))
				fp3.write("%d\t%s\t%s\t%d\t%s\t%s\t%d\t%s\n"%(l_no,'',list1[i],count1,'s','define',address,val))
				address=address+count1
		
		if (list1[i]== 'jmp' or list1[i]== 'jnz' or list1[i]== 'loop' or list1[i]== 'je' or list1[i]== 'jz') and i==0:
				flag=0
				l_no1=0
				list2=[]
				list3=[]
				list4=[]
				list4=list1[i+1]
				list2=list1[i+1] + ':'
				
				
				if a==1:
					fp1=open(fname,"r")
					line1=fp1.readline() #open asm file line by line 
				else:
					fp1=open(fname1,"r")
					line1=fp1.readline() #open asm file line by line	
				
				while(line1!=""):
					l_no1 = l_no1 + 1  #line count 1...n
					list3=line1.split()
					for j in range(len(list3)):
						if(list2==list3[j]):
							flag=1
							break
							
						else:
							flag=0
					if(flag==1):
						break
				
					line1=fp1.readline()
					
				if(flag==1):
					#print("%d\t%s\t%s\t%d\t%s\t%s\tl[%d]\t%s\n"%(l_no,list4,list1[i],0,'l','define',l_no1,list1[i+1:]))
					fp3.write("%d\t%s\t%s\t%d\t%s\t%s\tl[%d]\t%s\n"%(l_no,list4,list1[i],0,'l','define',l_no1,list1[i+1:]))
					#address=address+1
					
				else:
					z=0
					#print("%d\t%s\t%s\t%d\t%s\t%s\tl[%d]\t%s\n"%(l_no,list4,list1[i],0,'l','und',z,list1[i+1:]))
					fp3.write("%d\t%s\t%s\t%d\t%s\t%s\tl[%d]\t%s\n"%(l_no,list4,list1[i],0,'l','und',z,list1[i+1:]))
					#address=address+1
		
		if(address2==0):			
			if (list1[i]== 'resd' or list1[i]== 'resw' or list1[i]== 'resq' or list1[i]== 'resd'):
				address1=0
				address2=1
		if (list1[i]== 'resb' and i==1):
			
			#print("%d\t%s\t%s\t%d\t%s\t%s\t%d\t%s\n"%(l_no,list1[i-1],list1[i],1,'s','define',address1,list1[i+1:]))
			fp3.write("%d\t%s\t%s\t%d\t%s\t%s\t%d\t%s\n"%(l_no,list1[i-1],list1[i],1,'s','define',address1,list1[i+1:]))
			address1=address1+(1*int(list1[i+1]))

		if (list1[i]== 'resd' and i==1):
			#print("%d\t%s\t%s\t%d\t%s\t%s\t%d\t%s\n"%(l_no,list1[i-1],list1[i],1,'s','define',address1,list1[i+1:]))
			fp3.write("%d\t%s\t%s\t%d\t%s\t%s\t%d\t%s\n"%(l_no,list1[i-1],list1[i],1,'s','define',address1,list1[i+1:]))
			address1=address1+(4*int(list1[i+1]))
			
		if(list1[i]== 'resq'):
			#print("%d\t%s\t%s\t%d\t%s\t%s\t%d\t%s\n"%(l_no,list1[i-1],list1[i],1,'s','define',address1,list1[i+1:]))
			fp3.write("%d\t%s\t%s\t%d\t%s\t%s\t%d\t%s\n"%(l_no,list1[i-1],list1[i],1,'s','define',address1,list1[i+1:]))
			address1=address1+(8*int(list1[i+1]))
		
		if (list1[i]== 'resw'):
			#print("%d\t%s\t%s\t%d\t%s\t%s\t%d\t%s\n"%(l_no,list1[i-1],list1[i],1,'s','define',address1,list1[i+1:]))
			fp3.write("%d\t%s\t%s\t%d\t%s\t%s\t%d\t%s\n"%(l_no,list1[i-1],list1[i],1,'s','define',address1,list1[i+1:]))
			address1=address1+(2*int(list1[i+1]))
		
	return sum1
def create_Symbol_Table():
	a=1							
	sum1 = 0					
	l_no = 1
	line=fp.readline()
	while(line!=""):
		sum1=table(line,l_no,sum1,a)
		#print(sum1)
		l_no = l_no + 1
		line=fp.readline()
	
	


	
create_Symbol_Table()#To create symbol table
fp.close()
fp3.close()
