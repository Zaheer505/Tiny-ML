from tflite_runtime.interpreter import Interpreter
#import tensorflow as tf
import numpy as np
import time
import cv2
from PIL import Image

capture = cv2.VideoCapture('D:/dataset new/videos/4.mp4')


def main():

    j = 0
    labels = ["one","two","three","four","five","six","seven","eight","nine","addition","division","multiplication","subtraction"]
    model_path = r"C:\Users\Zaheer43\Downloads\tflite_model.tflite"
    interpreter = Interpreter(model_path)
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    interpreter.allocate_tensors()
    _, height, width, _ = interpreter.get_input_details()[0]['shape']

    while(1):
        ret, frame = capture.read() # frame is in numpy array
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if ret == False:
                 break
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);
        circles = cv2.HoughCircles(grayFrame, cv2.HOUGH_GRADIENT, 0.8, 10)
        if circles is not None:
                  circles = np.round(circles[0, :]).astype("int")
                  height = frame.shape[0]
                  width = frame.shape[1]
                  lemonROIs = []
                  for i in circles:
                           canvas = np.ones((height, width))
                           j+=1
                           color = (0, 0, 0)
                           thickness = -1
                           centerX = i[0]
                           centerY = i[1]
                           radius = i[2]
                           output = frame.copy()
                           output[canvas == 0] = (0, 0, 0)
                           x = centerX - radius
                           y = centerY - radius
                           h = 2 * radius
                           w = 2 * radius
                              
                           croppedImg = output[y+40:y-40 + h, x+40:x-40 + w]
                           image = cv2.cvtColor(croppedImg, cv2.COLOR_BGR2GRAY);
                           image = cv2.resize(image, (128, 128))
                          
                           image = np.expand_dims(image, axis = 2)
                           image = (np.expand_dims(image, axis = 0)).astype(np.float32)
                           interpreter.allocate_tensors()
                           interpreter.set_tensor(input_details[0]['index'], image)
                           interpreter.invoke()
                           tflite_model_predictions = interpreter.get_tensor(output_details[0]['index'])
                           prediction = labels[np.argmax(tflite_model_predictions)-1]
                           print ('TF Lite Prediction : ', prediction)

if __name__ == '__main__':
	main()
    