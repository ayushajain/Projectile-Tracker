import cv2, numpy, math, csv, sys

cap = cv2.VideoCapture('videos/s9t3.mp4')

# video fps
FRAME_RATE = 30.0

# ball color threshold values
color_lower = (29, 86, 6)
color_upper = (64, 255, 255)

# position and time
path = []
ball_raw_x = 0
ball_raw_y = 0
time = 0

writer = csv.writer(open('output.csv', 'wb'))
writer.writerow(('Time', 'X', 'Y'))

# recording data
record = False

while True:
    ret, frame = cap.read()

    key = cv2.waitKey(1)

    if key == ord('q') or frame is None:
        break
    elif key == ord('s'):
        record = True
    elif key == ord('e'):
        record = False


    # resize frame and convert rgb to hsv colorscale
    frame = cv2.resize(frame, (0, 0), fx=float(0.5), fy=float(0.5))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # threshold color values to the ball's color
    mask = cv2.inRange(hsv, color_lower, color_upper)

    # erode noise picked up and dilate to compensate for ball's erosion
    mask = cv2.erode(mask, None, iterations=3)

    # find contours
    blobs = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(blobs[0]) == 1:
        ball = blobs[0][0]

        # calculate center of the ball and draw circle on original frame
        moments = cv2.moments(ball)
        ball_raw_x = int((moments["m10"] / moments["m00"]))
        ball_raw_y = int((moments["m01"] / moments["m00"]))

    # lapalacian filter for grid detection
    lap = cv2.Laplacian(gray, cv2.CV_16S, ksize=5, scale=1, delta=0)
    lap = cv2.convertScaleAbs(lap)
    t, lap = cv2.threshold(lap.copy(), 180, 255, cv2.THRESH_BINARY_INV)
    lap = cv2.erode(lap, None, iterations=1)
    lap = cv2.dilate(lap, None, iterations=2)
    square_blobs, _ = cv2.findContours(lap.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # find the grid square where i = 0 and j = 0
    bottom_left_square = None
    distance = 9999999
    for sqr in square_blobs:
        M = cv2.moments(sqr)
        cX = int((M["m10"] / M["m00"]) * 1)
        cY = int((M["m01"] / M["m00"]) * 1)
        dist = math.hypot(cX - 0, cY - 960)

        peri = cv2.arcLength(sqr, True)
        approx = cv2.approxPolyDP(sqr, 0.15 * peri, True)

        if len(approx) == 4 and cv2.contourArea(sqr) > 1500 and dist < distance:
            bottom_left_square = sqr
            distance = dist

    # calculate origin of grid
    rect = cv2.minAreaRect(bottom_left_square)
    origin_x = int(rect[0][0] - rect[1][0]/2)
    origin_y = int(rect[0][1] + rect[1][1]/2)
    ball_x = ball_raw_x - origin_x
    ball_y = origin_y - ball_raw_y
    path.append((ball_x, ball_y))

    pix_to_cm_ratio = 10.0/rect[1][0]

    # draw tracked objects and display ball position
    cv2.drawContours(frame, [bottom_left_square], -1, (0, 255, 0), 2)
    cv2.circle(frame, (origin_x, origin_y), 5, (0, 0, 255), -1)
    cv2.circle(frame, (ball_raw_x, ball_raw_y), 5, (0, 0, 255), -1)
    cv2.putText(frame, str(ball_x) + ", " + str(ball_y), (0, 30), cv2.FONT_HERSHEY_PLAIN, 2, 255)
    for pos in path:
        cv2.circle(frame, (pos[0] + origin_x, origin_y - pos[1]), 2, (0, 100, 255), -1)

    # write data to csv file
    if record:
        writer.writerow((time, ball_x * pix_to_cm_ratio, ball_y * pix_to_cm_ratio))

        # frame rate is 30 fps
        time += 1/FRAME_RATE

    cv2.imshow("MASK", mask)
    cv2.imshow("LAP", lap)
    cv2.imshow("FRAME", frame)



