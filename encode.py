import cv2
import numpy as np
import time
from PIL import Image
import pytesseract

cap = cv2.VideoCapture(0)
print("Opened Camera")

fps = 25.0
duration = 3
dimensions = (640,  480)

# folosirea codecului FFV1
# compresie fara pierderi
fourcc = cv2.VideoWriter_fourcc(*'FFV1')

out = cv2.VideoWriter('output.avi', fourcc, fps, dimensions)
if(cap.isOpened()):
    t = time.time()
    while( (time.time() - t) < duration ):
        ret, frame = cap.read()
        if not ret:
            break
        
        out.write(frame)

cap.release()
out.release()
print("Video Saved")

# precizarea path-ului catre executabil
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'

# extragerea textului din imagine
img = Image.open('resurse/image.png')
text = pytesseract.image_to_string(img)

# deschiderea fisierului text in modul de scriere/creare
with open('text_from_image.txt', 'w+') as file:
    # scrierea textului in fisier
    file.write(text)

print("Text Written")

# deschiderea fisierului text in modul de citire
with open('text_from_image.txt', 'r') as file:
    # citirea continutului
    text = file.read()

# impartirea textului in bucati de lungime egala
num_frames = 10 
text_pieces = [text[i:i + len(text) // num_frames] for i in range(0, len(text), len(text) // num_frames)]

def get_binary(message):
    if( type(message) == str ):
        binary_message = ( char.split('b')[1] for char in map(bin,bytearray(message,'utf8')) )
        binary_message_8b = []
        for binary_char in binary_message:
            to_fill = ''.join('0' for l in range(len(binary_char), 8))
            binary_message_8b.append((to_fill + binary_char))
        return ''.join(binary_message_8b)
    elif( type(message) == np.uint8 or type(message) == int  ):
        binary_message = bin(message).split('b')[1]
        to_fill = ''.join('0' for l in range(len(binary_message), 8))
        return to_fill + binary_message
    elif( type(message) == np.ndarray ):
        binary_message_8b = []
        for value in message:
            binary_message = bin(value).split('b')[1]
            to_fill = ''.join('0' for l in range(len(binary_message), 8))
            binary_message_8b.append(to_fill + binary_message)
        return ''.join(binary_message_8b)
    
def encode_message(image, message):
    end_of_message_string = '@#$%^&'

    message = message + end_of_message_string
    binary_message = get_binary(message)

    max_bytes_to_encode = ((image.shape[0] * image.shape[1] * 3 ) // 8 ) * 2
    if( max_bytes_to_encode > len(message) ):
        # index pentru pozitia curenta din reprezentarea binara a mesajului
        index = 1
        for row in image:
            for pixel in row:
                b = get_binary(pixel[0])
                g = get_binary(pixel[1])
                r = get_binary(pixel[2])
                
                if( index < len(binary_message) ): 
                    b_steg = binary_message[index-1] + binary_message[index]
                    pixel[0] = int(b[0:-2] + b_steg, 2)
                    index += 2
                else: 
                    return image
                if( index < len(binary_message) ): 
                    g_steg = binary_message[index-1] + binary_message[index]
                    pixel[1] = int(g[0:-2] + g_steg, 2)
                    index += 2
                else: 
                    return image
                if( index < len(binary_message) ): 
                    r_steg = binary_message[index-1] + binary_message[index]
                    pixel[2] = int(r[0:-2] + r_steg, 2)
                    index += 2
                else: 
                    return image
        return image
    else:
        print("Mesajul este prea mare pentru a fi ascuns in imagine!")

def hide_text(name, out_video): 
    frame_pieces = [4, 8, 9, 10, 14, 27, 33, 57, 64, 72]
    nr_frame = 0
    tp = 0

    cap = cv2.VideoCapture(name)

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    out = cv2.VideoWriter(out_video, cv2.VideoWriter_fourcc(*'FFV1'), fps, (frame_width, frame_height))
    
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        #cv2.imshow(name, frame)

        if tp < len(frame_pieces) and nr_frame == frame_pieces[tp]:
            frame = encode_message(frame, text_pieces[tp])
            tp = tp+1

        nr_frame = nr_frame+1

        out.write(frame)
        
        #k = cv2.waitKey(15)
        #if( k == ord('q') ):
        #    break
    
    cap.release()
    #cv2.destroyAllWindows()
    
hide_text('output.avi', 'output_text.avi')
print("Text Hidden")