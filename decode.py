import cv2
import numpy as np
import time
from PIL import Image
import pytesseract

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

def decode_message( image ):
    image_lsb_text = ''
    lsb_char_binary = ''
    end_of_message_string = '@#$%^&'

    for row in image:
        for pixel in row:
            b_steg = get_binary(pixel[0])
            g_steg = get_binary(pixel[1])
            r_steg = get_binary(pixel[2])
            
            if( len(lsb_char_binary) < 8 ): 
                lsb_char_binary += b_steg[-2]
                lsb_char_binary += b_steg[-1]
            else: 
                image_lsb_text += chr(int(lsb_char_binary, 2))
                lsb_char_binary = b_steg[-2]
                lsb_char_binary += b_steg[-1]

            if( len(lsb_char_binary) < 8 ): 
                lsb_char_binary += g_steg[-2]
                lsb_char_binary += g_steg[-1]
            else: 
                image_lsb_text += chr(int(lsb_char_binary, 2))
                lsb_char_binary = g_steg[-2]
                lsb_char_binary += g_steg[-1]

            if( len(lsb_char_binary) < 8 ): 
                lsb_char_binary += r_steg[-2]
                lsb_char_binary += r_steg[-1]
            else: 
                image_lsb_text += chr(int(lsb_char_binary, 2))
                lsb_char_binary = r_steg[-2]
                lsb_char_binary += r_steg[-1]
            
            if( (len(image_lsb_text) > 6) and ( image_lsb_text[-6:] == end_of_message_string )):
                return image_lsb_text[:-6]
    
    print('Nu a fost gasit separatorul de final!')
    return ''

def extract_text(name): 
    decoded_text = ''

    frame_pieces = [4, 8, 9, 10, 14, 27, 33, 57, 64, 72]
    nr_frame = 0
    tp = 0

    cap = cv2.VideoCapture(name)
    
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        #cv2.imshow(name, frame)

        if tp < len(frame_pieces) and nr_frame == frame_pieces[tp]:
            message_decoded = decode_message(frame)
            decoded_text = decoded_text + message_decoded 
            tp = tp+1

        nr_frame = nr_frame+1
        
        #k = cv2.waitKey(15)
        #if( k == ord('q') ):
        #    break
    
    cap.release()
    return decoded_text
    #cv2.destroyAllWindows()

decoded_text = extract_text('output_text.avi')

# afisarea mesajului decodat pe ecran

#print(decoded_text.encode('utf-8', 'ignore').decode('utf-8'))
for character in decoded_text:
    # datorita aparitiilor diacriticilor in text, la decodare,
    # am ales o afisare putin mai diferita
    # filtrarea caracterelor ASCII
    if ord(character) < 128:
        print(character, end='')

# memorarea mesajului decodat in fisier
#with open('text_from_video.txt', 'w', encoding='utf-8') as file:
#    file.write(decoded_text)