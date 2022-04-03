
import os
import cv2
import time
import numpy as np

import argparse
from utils import rotate_box, align_box, get_idx
from modules.text_detect.predict import test_net, net, refine_net, poly

import torch
def test(image):
    try:
        image = image
        image_copy = image.copy()
        bboxes, polys, score_text = test_net(net, image_copy, 0.7, 0.4, 0.4, True, poly, refine_net)
        if bboxes != []:
            bboxes_xxyy = []
            ratios = []
            for box in bboxes:
                x_min = min(box, key=lambda x: x[0])[0]
                x_max = max(box, key=lambda x: x[0])[0]
                y_min = min(box, key=lambda x: x[1])[1]
                y_max = max(box, key=lambda x: x[1])[1]
                if (x_max - x_min) > 20:
                    ratio = (y_max - y_min) / (x_max - x_min)
                    ratios.append(ratio)

            mean_ratio = np.mean(ratios)
            if mean_ratio >= 1:
                image, bboxes = rotate_box(image, bboxes, None, True, False)

            bboxes, polys, score_text = test_net(net, image, 0.7, 0.4, 0.4, True, poly, refine_net)

            image, check = align_box(image, bboxes, skew_threshold=0.9)

            if check:
                bboxes, polys, score_text = test_net(net, image, 0.7, 0.4, 0.4, True, poly, refine_net)
            h, w, c = image.shape

            for box in bboxes:
                x_min = max(int(min(box, key=lambda x: x[0])[0]), 1)
                x_max = min(int(max(box, key=lambda x: x[0])[0]), w - 1)
                y_min = max(int(min(box, key=lambda x: x[1])[1]), 3)
                y_max = min(int(max(box, key=lambda x: x[1])[1]), h - 2)
                bboxes_xxyy.append([x_min - 1, x_max, y_min - 1, y_max])


            width, height = image.shape[1],image.shape[0]
            box_list = []
            for box in bboxes_xxyy:
                x_min, x_max, y_min, y_max = box
                w = x_max - x_min
                h = y_max - y_min
                xcenter = x_min + (w) / 2
                ycenter = y_min + (h) / 2
                b= "0"+" " +str(xcenter / width) + ' ' + str(ycenter / height) + ' ' + str(w / width) + ' ' + str(h / height)
                # b = str(float(x_min / w))+" "+ str(float(x_max / w))+" "+ str(float(y_min / h))+" "+ str(float(y_max / h))

                box_list.append(b)
            return box_list

    except :
        print("c")

if __name__ == '__main__':
    start_time=time.time()
    device = torch.device('cpu')
    parser = argparse.ArgumentParser(description='AI')
    parser.add_argument('--folder_test', default=r'C:\Users\ADMIN\Desktop\auto_label_craft\pdf', type=str,
                        help='path to folder')
    args = parser.parse_args()
    path_des=r"C:\Users\ADMIN\Desktop\auto_label_craft\pdf"
    try:
        list_add = []
        for file_name in os.listdir(args.folder_test):
            image = cv2.imread(os.path.join(args.folder_test, file_name))
            print(file_name)
            texts = test(image)
            if texts:
                for text in texts:
                    with open(os.path.join(path_des, file_name.rstrip('.jpeg') + '.txt'), 'a') as ftxt:
                        # with open(os.path.join(path_des, filename.split('.')[0] + '.txt'), 'a') as ftxt:
                        ftxt.write(text)
                        ftxt.write('\n')
                        ftxt.close()
            else:
                continue
    except:
        print("error")
