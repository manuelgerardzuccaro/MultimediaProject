import cv2

def calculate_psnr(original, restored):
    return cv2.PSNR(original, restored)

def save_image(image, path):
    cv2.imwrite(path, image)
