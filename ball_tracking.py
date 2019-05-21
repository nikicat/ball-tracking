import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
args = vars(ap.parse_args())

#greenLower = (29, 86, 6)
#greenUpper = (64, 255, 255)
greenLower = (0, 204, 82)
greenUpper = (14, 255, 255)
lower = [0, 231, 160]
upper = [14, 255, 255]

if not args.get("video", False):
    camera = cv2.VideoCapture(0)
else:
    camera = cv2.VideoCapture(args["video"])

# Create window
cv2.namedWindow('image')

def on_trackbar_change(position):
    pass

# Set mouse callback to capture HSV value on click
#cv2.setMouseCallback("image", on_mouse_click, hsv)
cv2.createTrackbar("Min H", "image", int(lower[0]), 255, on_trackbar_change)
cv2.createTrackbar("Min S", "image", int(lower[1]), 255, on_trackbar_change)
cv2.createTrackbar("Min V", "image", int(lower[2]), 255, on_trackbar_change)
cv2.createTrackbar("Max H", "image", int(upper[0]), 255, on_trackbar_change)
cv2.createTrackbar("Max S", "image", int(upper[1]), 255, on_trackbar_change)
cv2.createTrackbar("Max V", "image", int(upper[2]), 255, on_trackbar_change)

while True:
    (grabbed, frame) = camera.read()

    if args.get("video") and not grabbed:
        break

    frame = imutils.resize(frame, width=600)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get trackbar positions and set lower/upper bounds
    lower = tuple(cv2.getTrackbarPos(f"Min {axis}", "image") for axis in 'HSV')
    upper = tuple(cv2.getTrackbarPos(f"Max {axis}", "image") for axis in 'HSV')

    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)

        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)

    cv2.imshow("image", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
