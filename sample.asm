section .data
	a dd 5
	b dd 10
	c dd 10
	d dd 20
	msg db "hello",10,0

section .bss
	s1 resd 3
	s2 resb 1
	s3 resd 3
section .text
	global main
	extern printf
main:
	mov eax,a
	add ebx,b
	mov ecx,12
	mov eax,14
	mov edx,12
	mov eax,13
	mov eax,'a'
	mov al,'z'
	mov ebx,eax
	mov eax,dword[a]
	mov eax,dword[a+ebx]
	mov eax,dword[ebx+b]
	mov eax,dword[ebx+1]
	mov eax,dword[1+ebx]
	mov dword[a],eax
	mov dword[a+edx],eax
