import sys
import os 
import hashlib

class Encript:
    def __init__(self,file_path,key1):
        self.file_path = file_path
        self.key1 = key1
        has = False

        with open(file_path,"r") as f:
            texto=f.read(-1)
        if os.path.exists(f'{file_path}SHA256.txt'):
            with open(f'{file_path}SHA256.txt',encoding='utf-8')as fl:
                hasa =fl.read(-1)  
        else:
            has = hashlib.sha256(texto.encode('utf-8')).hexdigest()
            with open(f'{file_path}SHA256.txt','w') as fili:
                fili.write(has)


        text = cript(texto,key1)
        if has :
            os.remove(file_path)
            with open(file_path,"w") as fi:
                fi.write(text)
            print('Mensagem criptografada')
        else:
            if hasa == hashlib.sha256(text.encode('utf-8')).hexdigest():
                with open(file_path,"w") as fi:
                    fi.write(text)
                os.remove(f'{file_path}SHA256.txt')
                print('Mensagem descriptada')
            else:
                print('Senha errada')
    def cript(self,string,key):
        out=''
        for r in range(len(string)):
            out+=chr(ord(string[r])^ord(key[r%len(key)]))
        return out
