import cv2
import numpy as np

def detect_hand(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Blur the image
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)
    
    # Thresholding
    _, thresholded = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours
    contours, _ = cv2.findContours(thresholded.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Check if contours exist
    if len(contours) > 0:
        # Find the largest contour
        max_contour = max(contours, key=cv2.contourArea)
        
        # Approximate the contour to a polygon
        epsilon = 0.0005 * cv2.arcLength(max_contour, True)
        approx = cv2.approxPolyDP(max_contour, epsilon, True)
        
        # Convex hull
        hull = cv2.convexHull(max_contour)
        
        # Draw contours and hull on the frame
        cv2.drawContours(frame, [approx], 0, (0, 255, 0), 2)
        cv2.drawContours(frame, [hull], 0, (0, 0, 255), 3)
        
        # Find the center of the palm
        M = cv2.moments(max_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            center = (cx, cy)
            cv2.circle(frame, center, 7, (255, 255, 255), -1)
            
            # Determine direction of movement based on the change in center position
            if cx < 200:
                return "left"
            elif cx > 440:
                return "right"
            elif cy < 150:
                return "up"
            elif cy > 330:
                return "down"
    
    return None

# Main function
def main():
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Flip the frame horizontally for better user experience
        frame = cv2.flip(frame, 1)
        
        # Detect hand gesture
        direction = detect_hand(frame)
        if direction:
            print("Detected direction:", direction)
        
        # Display the frame
        cv2.imshow("Hand Gesture Recognition", frame)
        
        # Check for 'q' key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the capture and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
