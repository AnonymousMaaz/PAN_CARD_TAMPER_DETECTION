# Import the necessary packages
from skimage.metrics import structural_similarity
import imutils
import cv2
from PIL import Image
import requests
import numpy as np


# ================== Downloading the images ===============================
# requests.get(...) 
# → Sends an HTTP request to the given URL to download the image
# stream=True means:
# → Do not download the entire file at once
# → Download it as a stream (piece by piece) to save memory
# response.raw
# → Gives access to the raw binary content of the downloaded image
# → This behaves like a file object

# Image.open(...)
# → Opens the image using PIL
# → Converts raw binary data into an image object

original = Image.open(requests.get("https://www.thestatesman.com/wp-content/uploads/2019/07/pan-card.jpg", stream=True).raw)
tampered = Image.open(requests.get("https://assets1.cleartax-cdn.com/s/img/20170526124335/Pan4.png", stream=True).raw)

# =============== The File Format of the source File =============================
print("Original Image Format : ", original.format)
print("Tampered Image Format : ", tampered.format)

# ================ Image Size: in pixels. The size is given as a tuple (width, height) ==================
print("Original Image Size : ", original.size)
print("Tampered Image Size : ", tampered.size)

# ==================== Converting the format of the tampered image similar to original Image ==================
original = original.resize((250, 160))
print("Formatted Original Image Size: ", original.size)
original.save("pan_card_tampering/image/original.png")

tampered = tampered.resize((250, 160))
print("Formatted Tampered Image Size: ", tampered.size)
tampered.save("pan_card_tampering/image/tampered.png")

# ================= Display the Images ===========================
# original.show(title="Original Pan Card")
# tampered.show(title="Tampered Pan Card")
# original_cv = cv2.cvtColor(np.array(original), cv2.COLOR_RGB2BGR)
# tampered_cv = cv2.cvtColor(np.array(tampered), cv2.COLOR_RGB2BGR)


original = cv2.imread("pan_card_tampering/image/original.png")
tampered = cv2.imread("pan_card_tampering/image/tampered.png")

original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
tampered_gray = cv2.cvtColor(tampered, cv2.COLOR_BGR2GRAY)

# ============= Finding the Structural Similarity Index SSIM ==========================
(score, diff) = structural_similarity(original_gray, tampered_gray, full=True)
diff = (diff * 255).astype("uint8")

print("SSIM: {}".format(score))

thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours = imutils.grab_contours(contours)

for c in contours:
    (x, y, w, h) = cv2.boundingRect(c)
    cv2.rectangle(original, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.rectangle(tampered, (x, y), (x + w, y + h), (0, 0, 255), 2)

# cv2.imshow("Original Image", original)
# cv2.imshow("Tampered Image", tampered)
# comparison = cv2.hconcat([original_gray, tampered_gray])
# cv2.imshow("Original vs Tampered", comparison)
# cv2.imshow("DIFFERENCE IMAGE", diff)
# cv2.imshow("Threshold", thresh)
diff_bgr = cv2.cvtColor(diff, cv2.COLOR_GRAY2BGR)
thresh_bgr = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
tamp_og_concat = cv2.hconcat([original, tampered])
diff_thresh_concat = cv2.hconcat([diff_bgr, thresh_bgr])
comparison = cv2.vconcat([tamp_og_concat, diff_thresh_concat])
cv2.imshow("All Images Comparison", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()