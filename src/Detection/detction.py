import cv2
import imutils
import numpy as np

from .Analyze import analyze_number

def process_image(image_name):
    crop_dir = './src/images_crop/'
    imn = image_name.split('.')[0]
    crop_img_name = crop_dir + imn + '.png'
    try:
        img = cv2.imread('./src/images/' + image_name, cv2.IMREAD_COLOR)
        img = cv2.resize(img, (600, 400))

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 13, 15, 15)

        edged = cv2.Canny(gray, 30, 200)
        contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        screenCnt = None

        for c in contours:

            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)

            if len(approx) == 4:
                screenCnt = approx
                break

        if screenCnt is None:
            detected = 0
            print("No contour detected")
        else:
            detected = 1

        if detected == 1:
            cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)

        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1, )
        new_image = cv2.bitwise_and(img, img, mask=mask)

        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]
        img = cv2.resize(img, (500, 300))
        Cropped = cv2.resize(Cropped, (400, 200))
        cv2.imwrite(crop_img_name, Cropped)
        res = analyze_number(crop_img_name)
        print(res)
        return res
    except Exception as Ex:
        print(Ex)
        img = cv2.imread('./src/images/' + image_name, cv2.IMREAD_COLOR)
        img = cv2.resize(img, (600, 400))

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 13, 15, 15)
        print(crop_img_name)
        cv2.imwrite(crop_img_name, gray)
        res = analyze_number(crop_img_name)
        print(res)
        return res


def process_result(res):
    numbers = []
    word_before_numbers = []
    words_after_number = []
    numb_found = False
    for word in res:
        try:
            num = int(word)
            numbers.append(word)
            numb_found = True
        except:
            if (numb_found):
                words_after_number.append(word)
            else:
                word_before_numbers.append(word)
    final_number = ''.join(numbers)
    words_bef = ''.join(word_before_numbers)
    words_aft = ''.join(words_after_number)
    final = ''
    if not words_bef == '':
        final += words_bef + '-'
    if not final_number == '':
        final += final_number + '-'
    if not words_aft == '':
        final += words_aft
    return final

def main_detection(img):
    res = process_image(img)
    if res:
        number = process_result(res[0])
        print(number)
        return number
    else:
        message = "Img Not Exists"
        return message