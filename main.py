
from flask import Flask, render_template, Response, request
from camera import VideoCamera
import time
import threading
import os
import numpy as np
import cv2
import sys

pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.

# App Globals (do not edit)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') #you can customze index.html here

def buildGauss(frame,levels):
        pyramid = [frame]
        for level in range(levels):
            frame = cv2.pyrDown(frame)
            pyramid.append(frame)
        return pyramid

def gen(camera):
    
    realWidth = 320
    realHeight = 240
    videoWidth = 160
    videoHeight = 120
    videoChannels = 3
    videoFrameRate = 15
    
    # Color Magnification Parameters
    levels = 3
    alpha = 170
    minFrequency = 1.0
    maxFrequency = 2.0
    bufferSize = 150
    bufferIndex = 0

    # Output Display Parameters
    font = cv2.FONT_HERSHEY_SIMPLEX
    loadingTextLocation = (50, 50)
    bpmTextLocation = (50, 50)
    fontScale = 1
    fontColor = (255,255,255)
    lineType = 2
    boxColor = (0, 255, 0)
    boxWeight = 3

    # Initialize Gaussian Pyramid
    firstFrame = np.zeros((videoHeight, videoWidth, videoChannels))
    firstGauss = buildGauss(firstFrame, levels+1)[levels]
    videoGauss = np.zeros((bufferSize, firstGauss.shape[0], firstGauss.shape[1], videoChannels))
    fourierTransformAvg = np.zeros((bufferSize))

    # Bandpass Filter for Specified Frequencies
    frequencies = (1.0*videoFrameRate) * np.arange(bufferSize) / (1.0*bufferSize)
    mask = (frequencies >= minFrequency) & (frequencies <= maxFrequency)

    # Heart Rate Calculation Variables
    bpmCalculationFrequency = 15
    bpmBufferIndex = 0

    bpmBufferSize = 10
    bpmBuffer = np.zeros((bpmBufferSize))

    i = 0
    
    #get camera frame
    while True:
        try: 
            frame, image = camera.get_frame()
            #image1 = image.resize((realWidth,realHeight))
            detectionFrame = image[int(videoHeight/2):int(realHeight-videoHeight/2), int(videoWidth/2):int(realWidth-videoWidth/2), :]
    
            # Construct Gaussian Pyramid
            videoGauss[bufferIndex] = buildGauss(detectionFrame, levels+1)[levels]
            fourierTransform = np.fft.fft(videoGauss, axis=0)
    
            # Bandpass Filter
            fourierTransform[mask == False] = 0
    
            # Grab a Pulse
            if bufferIndex % bpmCalculationFrequency == 0:
                i = i + 1
                for buf in range(bufferSize):
                    fourierTransformAvg[buf] = np.real(fourierTransform[buf]).mean()
                hz = frequencies[np.argmax(fourierTransformAvg)]
                bpm = 60.0 * hz
                bpmBuffer[bpmBufferIndex] = bpm
                bpmBufferIndex = (bpmBufferIndex + 1) % bpmBufferSize
            bufferIndex = (bufferIndex + 1) % bufferSize
            
            if i > bpmBufferSize:
                print(bpmBuffer.mean())
                cv2.putText(frame, "BPM: %d" % bpmBuffer.mean(), bpmTextLocation, font, fontScale, fontColor, lineType)
            else:
               print( "Calculating BPM...")
               cv2.putText(frame, "Calculating BPM...",(0,100), font, 2, (255,255,255), 3)
            
            #cv2.putText(frame, "Calculating BPM...", loadingTextLocation, font, fontScale, fontColor, lineType)
            frame = frame.tobytes()
            yield (b'--frame\r\n' 
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        except:
            pass
        
        

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='192.168.56.1', debug=False)
    


