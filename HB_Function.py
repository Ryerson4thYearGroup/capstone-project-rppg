"""
Webcam Heart Rate Monitor
"""

import numpy as np
import cv2
import sys



class FBDunction(object):
    
    def __init__(self):
        global x
        videoGauss = np.zeros((bufferSize, firstGauss.shape[0], firstGauss.shape[1], videoChannels))
    
    # Helper Methods
    def buildGauss(self,frame,levels):
        pyramid = [frame]
        for level in range(levels):
            frame = cv2.pyrDown(frame)
            pyramid.append(frame)
        return pyramid
    

    def HB_caculation(self,frame, i,bpmBuffer,fourierTransformAvg,videoGauss):
        realWidth = 320
        realHeight = 240
        videoWidth = 160
        videoHeight = 120
        videoChannels = 3
        videoFrameRate = 15


        #Color Magnification Parameters
        levels = 3
        alpha = 170
        minFrequency = 1.0
        maxFrequency = 2.0
        bufferSize = 150
        bufferIndex = 0

        # Output Display Parameters
        font = cv2.FONT_HERSHEY_SIMPLEX
        loadingTextLocation = (20, 30)
        bpmTextLocation = (videoWidth//2 + 5, 30)
        fontScale = 1
        fontColor = (255,255,255)
        lineType = 2
        boxColor = (0, 255, 0)
        boxWeight = 3
        # Initialize Gaussian Pyramid

        # Bandpass Filter for Specified Frequencies
        frequencies = (1.0*videoFrameRate) * np.arange(bufferSize) / (1.0*bufferSize)
        #print (frequencies)
        mask = (frequencies >= minFrequency) & (frequencies <= maxFrequency)

        # Heart Rate Calculation Variables
        bpmCalculationFrequency = 15
        bpmBufferIndex = 0
        bpmBufferSize = 10
        #bpmBuffer = np.zeros((bpmBufferSize))

        originalFrame = frame.copy()

        detectionFrame = frame[int(videoHeight/2):int(realHeight-videoHeight/2), int(videoWidth/2):int(realWidth-videoWidth/2), :]
        
        firstFrame = np.zeros((videoHeight, videoWidth, videoChannels))
        #firstGauss = self.buildGauss(self,firstFrame, levels+1)[levels]
        
        #videoGauss = np.zeros((bufferSize, firstGauss.shape[0], firstGauss.shape[1], videoChannels))
        #fourierTransformAvg = np.zeros((bufferSize))
        
        # Construct Gaussian Pyramid
        videoGauss[bufferIndex] = self.buildGauss(self,detectionFrame, levels+1)[levels]
        fourierTransform = np.fft.fft(videoGauss, axis=0)
        #print (fourierTransform )

        # Bandpass Filter
        fourierTransform[mask == False] = 0
        print (fourierTransform )
        # Grab a Pulse
        if bufferIndex % bpmCalculationFrequency == 0:
            #i = i + 1
            #print (i)
            for buf in range(bufferSize):
                fourierTransformAvg[buf] = np.real(fourierTransform[buf]).mean()
            hz = frequencies[np.argmax(fourierTransformAvg)]
            bpm = 60.0 * hz
            print(bpm)
            bpmBuffer[bpmBufferIndex] = bpm
            bpmBufferIndex = (bpmBufferIndex + 1) % bpmBufferSize

        # Amplify
        filtered = np.real(np.fft.ifft(fourierTransform, axis=0))
        filtered = filtered * alpha

        # Reconstruct Resulting Frame
        bufferIndex = (bufferIndex + 1) % bufferSize
        #print (bpmBuffer.mean())
        
        if i > bpmBufferSize:
            print (bpmBuffer.mean())
            return  bpmBuffer.mean()
        else:
            #print ("Calculating BPM...")
            return "Calculating BPM..."
            

   

