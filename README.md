# Engineering Capstone Project - Vital Signs Detection Through a Camera

## About
Remote photoplethysmography (rPPG) performs contactless vital signs detection. This project focuses on heart rate. The solution proposed in this project is based on computer vision techniques that analyzes the  color signals from video. The web application detects heart rate in real-time through a video stream from a webcam and displays the BPM value and change in BPM value graphically. 

#### Credit
The video processing techniques used in this repo are from on the [script](https://github.com/giladoved/webcam-heart-rate-monitor) developed by Gilad Oved based the [paper](https://people.csail.mit.edu/mrub/evm/) by MIT Computer Science & Artificial Intelligence Lab. 


## How it Works
Our project uses classical image processing techniques in a 5 step pipeline, as commonly found in most pipelines for detecting heart rate contactlessly. To learn more about the pipeline and various techniques, you can read the paper *'Color Signal Processing Methods for Webcam-Based Heart Rate Evaluation'* by Mikhail Kopeliovich & Mikhail Petrushan.

#### 1 - Signal Color Extraction 
Viola-Jones Facial Detection  is used to identify the area with the most skin pixels. It finds faces by checking where the intensity of the pixels changes rapidly, indicating there might be an edge there.

#### 2 - Signal Amplification
By using image normalization to improve contrast, the consequences of poor lighting conditions can be mitigated. The signal is also spatially decomposed using a Gaussian pyramid. An image pyramid increases the amount of information in an image by storing it at different resolutions.

#### 3 - Signal Color Filtering
An Ideal Impulse Response (IIR) Bandpass filter is used to extract the band of frequencies that contains information related to the heart rate. This also performs denoising and makes the heart rate amplitudes clear.

#### 4 - Heart Rate Calculation
By converting the signal into the frequency domain using Fast Fourier Transform (FFT), the specific frequency component associated with the heart rate can be selected. This value is then converted to beats per minute.

#### 5 - Heart Rate Results Filtering
The final result is smoothed out by using an averaging window on a buffer on the heart rate results. This keeps the impact of outliers low.


