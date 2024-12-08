import cv2

# Define the UDP stream URL
udp_stream_url = "udp://192.168.36.131:1234"  # Replace with your laptop's
# IP if
# needed

# Open the UDP stream
cap = cv2.VideoCapture(udp_stream_url)

if not cap.isOpened():
    print("Error: Unable to open UDP stream.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to receive frame.")
        break

    cv2.imshow("UDP Stream", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
