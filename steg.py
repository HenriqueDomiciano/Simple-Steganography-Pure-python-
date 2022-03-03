from PIL import Image
from tqdm import tqdm
from xor.Encript import cript

class Steganography:
    def __init__(self):
        pass
    def encode_str(self,img_path,string = " ",password = None):
        res = []
        if isinstance(password,str) and len(password)>0:
            string = cript(string,password)
        elif len(password)==0:
            raise ValueError('password needs to have at least one character')
        elif not(isinstance(password,None)):
                raise TypeError(f'password can only be str not {type(password)}')
        try:
            for i in string:
                s = bin(ord(i))[2:]
                if len(s)<24:
                    s = (24-len(s))*'0'+s
                for v in s:
                    res.append(v)
            img = Image.open(img_path)
            new_img = Image.new('RGB', (img.width, img.height))
            count = 0 
            if len(res)>img.width*img.height*3:
                print('Too much information cannot stegonograph')
                return None
            for x in tqdm(range(img.width)):
                for y in range(img.height):
                    actual = img.getpixel((x,y))
                    if count<len(res):
                        r_actual = int(str(bin(actual[0]))[:-1]+res[count],2)
                        g_actual = int(str(bin(actual[1]))[:-1]+res[count+1],2)
                        b_actual = int(str(bin(actual[2]))[:-1]+res[count+2],2)
                        count+=3
                        new_img.putpixel((x,y), (r_actual,g_actual,b_actual))
                    else:
                        r_actual = int(str(bin(actual[0]))[:-1]+'0',2)
                        g_actual = int(str(bin(actual[1]))[:-1]+'0',2)
                        b_actual = int(str(bin(actual[2]))[:-1]+'0',2)
                        new_img.putpixel((x,y), (r_actual,g_actual,b_actual))
            new_img.save(img_path.split('.')[0]+'steg.png')
            return True
        except:
            print("Only UTF-8 values are supported")
                
                
    
    def decode_str(self,img_path,password = None):
        res = []
        string_arr = []
        password_ex = False
        if isinstance(password,str) and len(password)>0:
            password_ex = True
        elif not(isinstance(password,None)):
                raise TypeError(f'password can only be str not {type(password)}')
        try:
            img = Image.open(img_path)
            
            for x in tqdm(range(img.width)):
                for y in range(img.height):
                    actual = img.getpixel((x,y))
                    for i in actual :
                        res.append(bin(i)[-1])
            
            for k in range(0,len(res),24):
                string_arr.append(chr(int(''.join(res[k:k+24]),2)))
                if string_arr[-1]=='\x00':
                    string_arr.pop(-1)
                    break

            arr = ''.join(string_arr)
            if password_ex:
                arr = cript(arr)
            return arr  
        except Exception as e:
            print(e)
            print('Something went wrong')
            raise e
    
    def get_text(self,text_path):
        with open(text_path,'r') as f :
            string_text = f.readlines()
        return ''.join(string_text)

    def encode_text(self,img_path,text_path):
        try:
            string = self.get_text(text_path)
            self.encode_str(img_path,string)
            return True
        except Exception as e:
            print(f'Something went wrong {e}')   
            return False         
    
    def encode_file(self,img_path,e_file):
        res = []
        try:
            print('pre-processing data')
            with open(e_file,'rb') as f:
                data = f.read()
                binary = [hex(b)[2:] for b in data] 
            for i in tqdm(binary):
                bi = bin(int(i,16))[2:]
                if len(bi)<8:
                    bi = (8-len(bi))*'0'+bi  
                for char in bi:
                    res.append(char)
            img = Image.open(img_path)
            new_img = Image.new('RGB', (img.width, img.height))
            count,second_count = 0,0
            ammount_of_bits = list(((39-len(bin(len(res))[2:]))*'0')+bin(len(res))[2:])
            is_big = False
            if len(res)>img.width*img.height*3-39 and len(res)<=img.width*img.height*3*2-39:
                print('using 2 bits for encoding')
                is_big = True
            elif len(res)<img.width*img.height*3 -39:
                is_big = False
            else:
                print(f'File is to big for 2 bit steg and will not suffer the process max:avaliable: {img.width*img.height*3*2} of {len(res)},{len(res)<=img.width*img.height*3*2}')
                return None
            if is_big:
                print(f'Size of avaliable bits {img.width*img.height*3*2},size of bits to write {len(res)}')
            else:
                print(f'Size of avaliable bits {img.width*img.height*3},size of bits to write {len(res)}')
                
            for x in tqdm(range(img.width)):
                for y in range(img.height):
                    actual = img.getpixel((x,y))
                    for i in range(len(actual)):
                        if is_big and count<len(res):
                            if i==0:
                                r_actual = int(str(bin(actual[i]))[:-2]+res[count]+res[count+1],2)
                                count+=2
                            elif i==1:
                                g_actual = int(str(bin(actual[i]))[:-2]+res[count]+res[count+1],2)
                                count+=2
                            else:
                                b_actual = int(str(bin(actual[i]))[:-2]+res[count]+res[count+1],2)
                                count+=2
                        if not(is_big) and count<len(res):
                            if i==0:
                                r_actual = int(str(bin(actual[i]))[:-1]+res[count],2)
                                count+=1
                            elif i==1:
                                g_actual = int(str(bin(actual[i]))[:-1]+res[count],2)
                                count+=1
                            else:
                                b_actual = int(str(bin(actual[i]))[:-1]+res[count],2)
                                count+=1
                        elif x==img.width-1 and y>=img.height-13:
                            if i == 0 :
                                r_actual = int(str(bin(actual[i]))[:-1]+ammount_of_bits[second_count],2)
                                second_count+=1
                            elif i==1:
                                g_actual = int(str(bin(actual[i]))[:-1]+ammount_of_bits[second_count],2)
                                second_count+=1
                            else:
                                b_actual = int(str(bin(actual[i]))[:-1]+ammount_of_bits[second_count],2)
                                second_count+=1
                        else:
                            if i == 0:
                                r_actual = actual[i]
                            elif i==1:
                                g_actual = actual[i]
                            else:
                                b_actual = actual[i] 
                    new_img.putpixel((x,y), (r_actual,g_actual,b_actual))
            #print(second_count)
            new_img.save(img_path.split('.')[0]+'steg.png')
            return True                 
        except Exception as e:
            print(f"Somethin went wrong {e}")
            raise e

    
    def decode_file(self,img_path,type_of_file,n_of_bits = 1):
        res = []
        string_arr = []
        n_of_the_message = []
        break_first = False
        try:
            img = Image.open(img_path)
            for y in range(img.height-39,img.height):
                info_pix = img.getpixel((img.width-1,y))
                for i in info_pix:
                    n_of_the_message.append(bin(i)[-1])
            n_of_the_message = int(''.join(n_of_the_message),2)
            for x in tqdm(range(img.width)):
                for y in range(img.height):
                    actual = img.getpixel((x,y))
                    for i in range(3):
                        if n_of_bits==1:
                            res.append(bin(actual[i])[-1])
                        elif n_of_bits==2:
                            if bin(actual[i])[-2]=='b':
                                res.append('0')
                            else:
                                res.append(bin(actual[i])[-2])
                            res.append(bin(actual[i])[-1])
                        else:
                            print('Not yet Supported')
                            return None
                    if len(res)>=n_of_the_message:
                        break_first = True
                        break
                if break_first:
                    break 
            #cleaning res
            print(len(res),n_of_the_message)
            res_cleaned = res.copy()
            for k in range(0,len(res_cleaned),8):
                string_arr.append(hex(int(''.join(res_cleaned[k:k+8]),2)))
            with open(img_path.split('.')[0]+'.'+type_of_file,'wb') as f:
                for b in string_arr:
                    b = b[2:]
                    if len(b)%2==1:
                        b='0'+b
                    f.write(bytes.fromhex(b))

        except Exception as e:
            print(f'Something went wrong {e}')
            raise e
