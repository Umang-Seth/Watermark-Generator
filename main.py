import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select an Image",
        filetypes=[("PNG","*.png"),("JPG","*.jpg")]
    )
    print(f"Selected file: {file_path}")
    if file_path:
        try:
            img = cv2.imread(f'{file_path}', cv2.IMREAD_UNCHANGED)
        except FileNotFoundError:
            print("The file was not found. Please check the path and try again.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("No file selected.")
    return img

print("Select the Image on which you want to add Watermark. Supported File Formats .jpg,.png. Do you want to continue? [Y/n]")
proceed_1 = input().lower()
if proceed_1 == "y":
    img = select_file()
else:
    exit()

print("Select the logo which be Watermark. Supported File Formats .png. Do you want to continue? [Y/n]")
proceed_2 = input().lower()
if proceed_2 == "y":
    logo = select_file()
else:
    exit()


#ADD PROVISION TO CONVERT JPG LOGO TO PNG
img_h, img_w, _ = img.shape
logo_h, logo_w, a = logo.shape

if img_h < logo_h or img_w < logo_w:
    print("Logo is greater than image")
    img_h_w = img.shape[:2]
    lower = min(img_h_w)
    value = img.shape[img_h_w.index(lower)]/logo.shape[img_h_w.index(lower)]
    rounded_down = round(value - 0.05, 1)


if a != 4:
    print("The Selected Logo in not png format")
    exit()

print(f"Scale Down the Watermark Logo. 1 to 0 1 begin original size. Recommendated Value < {rounded_down}")
scale = float(input().lower())
logo = cv2.resize(logo, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)

logo_bgr = logo[:, :, 0:3]
logo_alpha = logo[:, :, 3]

logo_h, logo_w, a = logo.shape

"""
To Added Logo in Center of Image with 100% Transparency
"""
cx = int(img_w/2)
cy = int(img_h/2)

tlc_x = int(cx - logo_w/2)
tlc_y = int(cy - logo_h/2)

brc_x = int(cx + logo_w/2)
brc_y = int(cy + logo_h/2)

roi = img[tlc_y:brc_y, tlc_x:brc_x]

logo_mask = cv2.merge([logo_alpha, logo_alpha, logo_alpha])
logo_mask_inv = cv2.bitwise_not(logo_mask)
masked_roi = cv2.bitwise_and(roi, logo_mask_inv)
masked_logo = cv2.bitwise_and(logo_bgr, logo_mask)

roi_final = cv2.bitwise_or(masked_roi, masked_logo)

roi_1 = roi.copy()
img_1 = img.copy()

img_1[tlc_y:brc_y, tlc_x:brc_x] = roi_final

cv2.imwrite('Output.jpg', img_1)
"""
Viewer for Intermediate Code
"""
# cv2.imshow('Leaves', img)
# cv2.imshow('opencv_logo', logo)
# cv2.imshow('logo_bgr', logo_bgr)
# cv2.imshow('logo_alpha', logo_alpha)
# cv2.imshow('roi', roi)
# cv2.imshow('logo_mask_inv', logo_mask_inv)
# cv2.imshow('masked_roi', masked_roi)
# cv2.imshow('logo_bgr', logo_bgr)
# cv2.imshow('logo_mask', logo_mask)
# cv2.imshow('masked_logo', masked_logo)
# cv2.imshow('roi_final', roi_final)


# cv2.imshow('Final', img_1)
# cv2.waitKey(0)