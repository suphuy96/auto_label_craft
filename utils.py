import  cv2
import numpy as np
import imutils
import math

def align_box(image, bboxes, skew_threshold=5, top_box=3):
    vertical_vector = [0, -1]
    top_box = np.argpartition([box[1][0]- box[0][0] for box in bboxes], -top_box)[-top_box:]
    avg_angle = 0
    for idx in top_box:
        skew_vector = bboxes[idx][0] - bboxes[idx][3]
        angle = np.math.atan2(np.linalg.det([vertical_vector,skew_vector]),np.dot(vertical_vector,skew_vector))
        avg_angle += math.degrees(angle)/3

    if abs(avg_angle) < skew_threshold:
        return image,0
    return imutils.rotate(image, avg_angle),1

def rotate_box(img, bboxes,degree,rotate_90, flip):

    h,w = img.shape[:2]
    if degree:
        new_bboxes = [[[h - i[1], i[0]] for i in bbox] for bbox in bboxes]
        new_img = cv2.rotate(img, degree)
        return new_img, np.array(new_bboxes)
    if rotate_90:
        new_bboxes = [[[h - i[1], i[0]] for i in bbox] for bbox in bboxes]
        new_img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        return new_img, np.array(new_bboxes)

    if flip:
        new_bboxes = [[[w-i[0], h-i[1]] for i in bbox] for bbox in bboxes]
        new_img = cv2.rotate(img, cv2.ROTATE_180)
        return new_img, np.array(new_bboxes)
    return img, bboxes
def get_idx(out,score,label):

    rs_idx = None
    m = max(score, key=lambda x: x[0])[0]
    for idx in range(len(out)):
        if  out[idx] == label and score[idx][0] >= m:
            rs_idx = idx
    return rs_idx
def four_point_transform(image, rect):
    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([[0, 0],[maxWidth - 1, 0],[maxWidth - 1, maxHeight - 1],[0, maxHeight - 1]], dtype = "float32")

    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped
