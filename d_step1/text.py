import numpy as np
import cv2
from datetime import datetime

# Create a black image
img = np.zeros((512, 512, 3), np.uint8)

# Write some Text

font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10, 500)
fontScale = 1
fontColor = (255, 255, 255)
lineType = 2

cv2.putText(img, 'Hello World!',
            bottomLeftCornerOfText,
            font,
            fontScale,
            fontColor,
            lineType)

# Display the image
cv2.imshow("img", img)

# Save image
date = datetime.now().strftime("%Y%m%d-%H%M%S")
path = f"out-{date}.jpg"
cv2.imwrite(path, img)

cv2.waitKey(0)
