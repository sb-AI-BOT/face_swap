import cv2
import numpy as np
import dlib
import argparse
from utils import *
from google.colab.patches import cv2_imshow

parser = argparse.ArgumentParser(description='FaceSwap')
parser.add_argument('--src_img', required=True, help='Path for source image')
parser.add_argument('--dst_img', required=True, help='Path for target image')
args = parser.parse_args()


img1,img1_gray = input_image(args.src_img)
img2,img2_gray = input_image(args.dst_img)
img1_mask = np.zeros_like(img1_gray)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("./model/shape_predictor_81_face_landmarks.dat")
height, width, channels = img2.shape
img2_new_face = np.zeros((height, width, channels), np.uint8)



face1_det = detector(img1_gray)
face2_det = detector(img2_gray)



face2=landmarks(img2_gray,face2_det)
convexhull2,points2,landmarks_points2=face2

face1=landmarks(img1_gray,face1_det)
convexhull,points,landmarks_points=face1

face1_index=face(img1,img1_gray,face1_det,img1_mask)

lines_space_mask = np.zeros_like(img1_gray)
lines_space_new_face = np.zeros_like(img2)

processing_fw=processing_tri(face1_index,img1,convexhull2,points2,landmarks_points2,img2_new_face)


# Face swapped (putting 1st face into 2nd face)
img2_mask_1 = np.zeros_like(img2_gray)
img2_mask_2 = cv2.fillConvexPoly(img2_mask_1, convexhull2, 256)
img2_mask_3 = cv2.bitwise_not(img2_mask_2)


img2_mask_4 = cv2.bitwise_and(img2, img2, mask=img2_mask_3)
out = cv2.add(img2_mask_4, img2_new_face)

(x, y, w, h) = cv2.boundingRect(convexhull2)
center_f = (int((x + x + w) / 2), int((y + y + h) / 2))

seamlessclone = cv2.seamlessClone(out, img2, img2_mask_2, center_f, cv2.NORMAL_CLONE)
print(seamlessclone)
cv2.imwrite("/content/drive/MyDrive/face_swap/img/elon_iron.jpg",seamlessclone)
#cv2_imshow(seamlessclone)

