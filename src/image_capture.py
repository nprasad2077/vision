import cv2

def capture_image():
    # Init camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        raise IOError('Cannot open webcam')
    
    while True:
        ret, frame = cap.read()
        cv2.imshow('Capture Image', frame)
        
        # Save on 's' key
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite('/home/ravi/code/vision/data/images/captured_image.jpg', frame)
            break
        
    cap.release()
    cv2.destroyAllWindows()
    
    return '/home/ravi/code/vision/data/images/captured_image.jpg'
        
 
  