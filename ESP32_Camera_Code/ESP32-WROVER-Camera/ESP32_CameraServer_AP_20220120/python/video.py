import numpy as np
import urllib.request
import cv2
import os
import socket
import time
url = 'http://192.168.4.1/capture'
script_dir = os.path.dirname(os.path.abspath(__file__))
#print(script_dir)
 
cap = cv2.VideoCapture(url)
whT=320
confThreshold = 0.5
nmsThreshold = 0.3
classesfile = os.path.join(script_dir, 'coco.names')
classNames=[]
with open(classesfile,'rt') as f:
    classNames=f.read().rstrip('\n').split('\n')
 
 
modelConfig = os.path.join(script_dir, 'yolov3.cfg')
modelWeights= os.path.join(script_dir, 'yolov3.weights')
net = cv2.dnn.readNetFromDarknet(modelConfig,modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
def findObject(outputs, im):
    hT, wT, cT = im.shape
    bbox = []
    classIds = []
    confs = []

    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                w, h = int(det[2]*wT), int(det[3]*hT)
                x, y = int((det[0]*wT)-w/2), int((det[1]*hT)-h/2)
                bbox.append([x, y, w, h])
                classIds.append(classId)
                confs.append(float(confidence))
    
    if len(classIds) > 0:
        indices = cv2.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold)
        if len(indices) > 0:
            for i in indices.flatten():
                box = bbox[i]
                x, y, w, h = box[0], box[1], box[2], box[3]
                cv2.rectangle(im, (x, y), (x+w, y+h), (255, 0, 255), 2)
                cv2.putText(im, f'{classNames[classIds[i]].upper()} {int(confs[i]*100)}%', 
                            (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
                print("Object detected:",classNames[classIds[i]])
                message = "{Object detected}"
                ESP32_IP = '192.168.4.1'  
                ESP32_PORT = 100  
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ESP32_IP, ESP32_PORT))
                print("Connected")
                s.sendall(message.encode())
                time.sleep(1)
                s.close()
                print("Disconnected")

while True:
    img_resp = urllib.request.urlopen(url)
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    image = cv2.imdecode(imgnp, -1)
    success, img = cap.read()
    blob = cv2.dnn.blobFromImage(image, 1/255, (whT, whT), [0, 0, 0], 1, crop=False)
    net.setInput(blob)
    outputLayerNames = net.getUnconnectedOutLayersNames()  
    outputs = net.forward(outputLayerNames)  

    findObject(outputs, image)

    cv2.imshow('Lab1 Object Detection', image)
    if cv2.waitKey(1) == 113:  # Press 'q' to exit
        break