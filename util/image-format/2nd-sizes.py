import os

import cv2

# imagefile = "0b39dab59.jpg"; bbox = [2, 2, 1031, 166]
# imagefile = "0d0a1d2fb.jpg"; bbox = [2, 97, 749, 240]
# imagefile = "0d605d56a.jpg"; bbox = [32,32,2372,288]
imagefile = "ba3154602.jpg";
bbox = [2, 64, 1036, 232]

# dirname = "../../data/train"
dirname = "../../tmp"


def get_cropped_img(image, bbox, is_mask=False):
    crop_margin = 0.1

    size_x = image.shape[1]
    size_y = image.shape[0]

    x0, y0, x1, y1 = bbox

    dx = x1 - x0
    dy = y1 - y0

    x0 -= dx * crop_margin
    x1 += dx * crop_margin + 1
    y0 -= dy * crop_margin
    y1 += dy * crop_margin + 1

    if x0 < 0:
        x0 = 0
    if x1 > size_x:
        x1 = size_x
    if y0 < 0:
        y0 = 0
    if y1 > size_y:
        y1 = size_y

    if is_mask:
        crop = image[int(y0):int(y1), int(x0):int(x1)]
    else:
        crop = image[int(y0):int(y1), int(x0):int(x1), :]

    return crop


image = cv2.imread(os.path.join(dirname, imagefile))
original = image = get_cropped_img(image, bbox, is_mask=False)

image = cv2.resize(original, (512, 256))
cv2.imwrite(os.path.join("../../tmp", "256x512-" + imagefile), image)

image = cv2.resize(original, (512, 512))
cv2.imwrite(os.path.join("../../tmp", "512x512-" + imagefile), image)
