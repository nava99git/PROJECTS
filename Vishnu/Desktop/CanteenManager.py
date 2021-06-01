from imutils.video import VideoStream
from pyzbar import pyzbar
import imutils
import cv2
import datetime
import time
import serial
import sqlite3
cart = []

ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)
ser.flush()
    
# loop over the frames from the video stream
while True:
    
    if ser.in_waiting > 0:
        RFIDTAG = ser.readline().decode('utf-8').rstrip()
        print(RFIDTAG)
        conn = sqlite3.connect('CanteenManagerDB.db')
        cur = conn.cursor()
        EID = 0
        name = ""
        try:
            cur.execute("SELECT ID, NAME FROM EmployeList WHERE RFID='"+RFIDTAG+"'")
            EID, name = cur.fetchone()
            print("EID: ", EID, "Name: ", name)
        except:
            print("INVALID RFID DETECTED")
        
        if name != "":
            # initialize the video stream and allow the camera sensor to warm up
            print("Starting video stream...")
            # vs = VideoStream(src=0).start()
            vs = VideoStream(usePiCamera=True).start()
            time.sleep(2.0)
            
            while ser.in_waiting == 0:
                # grab the frame from the threaded video stream and resize it to
                # have a maximum width of 400 pixels
                frame = vs.read()
                frame = imutils.resize(frame, width=400)
                ret, bw_im = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
                
                # find the barcodes in the frame and decode each of the barcodes
                barcodes = pyzbar.decode(bw_im)
                # loop over the detected barcodes
                for barcode in barcodes:
                    barcodeData = barcode.data.decode("utf-8")
                    barcodeType = barcode.type
                    
                    print("Barcode Data: ", barcodeData, " Barcode Type: ", barcodeType)
                    flag = 1
                    for i in range(len(cart)):
                        if cart[i]['Product'] == barcodeData:
                            cart[i]['Quantity'] += 1
                            cart[i]['Total'] = cart[i]['Price']*cart[i]['Quantity']
                            flag = 0
                            break;
                    if flag == 1:
                        cur.execute("SELECT Price from ProductList WHERE Product= '"+barcodeData+"'")
                        price = cur.fetchone()[0]
                        cart.append({'Product':barcodeData, 'Price': price, 'Quantity': 1, 'Total': price})
                        
                    time.sleep(1)
                # show the output frame
                cv2.imshow("QR Scanner", bw_im)
            
            print("Cart Confirmed")
            cv2.destroyAllWindows()
            
            RFIDTAG_cl = ser.readline().decode('utf-8').rstrip()
            print(RFIDTAG_cl)
            
            while RFIDTAG_cl != RFIDTAG:
                print("Use the same card you initiated the shopping")
                while ser.in_waiting == 0:
                    pass
                RFIDTAG_cl = ser.readline().decode('utf-8').rstrip()
            
            print("Employe ID: ", EID, " NAME : ", name, " RFID: ", RFIDTAG)
            print("Your Purchase: ")
            GrandTotal = 0
            for i in range(len(cart)):
                print(i+1, " ", cart[i]['Product'], " ",cart[i]['Price'], cart[i]['Quantity'], cart[i]['Total'])
                GrandTotal += cart[i]['Total']
            print("Grant Total: ", GrandTotal)
                
            
            cur.execute("INSERT INTO TransactionList VALUES (julianday('now'), %s, %f)" % (RFIDTAG, GrandTotal))
            conn.commit()
            conn.close()
            cart = []
            vs.stop()
        else:
            pass
