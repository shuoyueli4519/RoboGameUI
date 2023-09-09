from PIL import Image
import cv2
import numpy as np
import PIL

def PictureCreate():
    # 加载图像
    image = cv2.imread('InitImage.png')

    width, height = image.shape[1], image.shape[0]

    # 绘制矩形
    cv2.rectangle(image, (0, int(0.2*height)), (int(width), int(0.6*height)), (255, 255, 255), -1)  # 在图像上绘制矩形，颜色为绿色，线宽为2

    # 保存图像
    cv2.imwrite('image_with_rectangle.jpg', image)

def PictureSolve():
    img1 = cv2.imread('./InitImage.png')
    img2 = cv2.imread('./image_with_rectangle.jpg')
    img3 = cv2.addWeighted(img1, 0.3, img2, 0.7, 1)
    cv2.imwrite('./BackGroundSolve.png', img3)

def PictureResult():
    image = cv2.imread('./BackGroundSolve.png')
    output = np.ones((image.shape[0], image.shape[1], 3), dtype="uint8") * 255
    alpha = 0.8
    cv2.addWeighted(image, alpha, output, 1 - alpha, 0, output)
    cv2.imwrite('Faded.png', output)

def ButtonResult():
    image = cv2.imread('./Source/Pic/RedButton.png')
    output = np.ones((image.shape[0], image.shape[1], 3), dtype="uint8") * 255
    alpha = 0.6
    cv2.addWeighted(image, alpha, output, 1 - alpha, 0, output)
    cv2.imwrite('RedButtonHover.png', output)

    output = np.ones((image.shape[0], image.shape[1], 3), dtype="uint8")
    alpha = 0.9
    cv2.addWeighted(image, alpha, output, 1 - alpha, 0, output)
    cv2.imwrite('RedButtonPress.png', output)

def TogglePicture():
    image = Image.open('./Source/Pic/TitleCut.png')
    image_rgb = image.convert("RGB")
    image_alpha = image.split()[3] if image.mode == "RGBA" else None

    # 反转颜色
    inverted_image_rgb = PIL.ImageOps.invert(image_rgb)

    # 合并颜色通道和透明度通道
    if image_alpha:
        inverted_image = Image.merge("RGBA", (*inverted_image_rgb.split(), image_alpha))
    else:
        inverted_image = inverted_image_rgb

    # 保存反转后的图像
    inverted_image.save("inverted_image.png")

def ImageShow():
    image = cv2.imread("./image.png")
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def ChangeColor():

    # 读取图像
    image = cv2.imread('./Source/Pic/BlueFrame.png')

    # 将图像转换为 HSV 颜色空间
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 定义白色的颜色范围
    lower_white = np.array([0, 0, 0])
    upper_white = np.array([0, 0, 2])

    # 根据白色的颜色范围创建掩膜
    mask = cv2.inRange(hsv_image, lower_white, upper_white)

    # 将不是白色的部分全部改为红色
    image[mask != 255] = [0, 0, 255]

    # 显示修改后的图像
    cv2.imshow('Modified Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def VeinPicture():
    yellow_color = (3, 118, 235)
    blue_color = (235, 120, 3)
    purple_color = (118, 2, 233)
    # list_first = [((6, 13), (23, 30)), ((6, 40), (23, 57)), ((6, 67), (23, 84)),
    #               ((6, 94), (23, 111)), ((6, 121), (23, 138))]
    image = cv2.imread('./Source/Pic/Store.png')
    # for i in range(0, 5):
    #     cv2.rectangle(image, list_first[i][0], list_first[i][1], purple_color, -1)
    cv2.imshow('image', image)
    key = cv2.waitKey(0)
    if key == ord('q'):
        cv2.destroyAllWindows()

def DrawPicture():
    first_vein_loaction = [((4, 16), (20, 32)), ((4, 43), (20, 59)), ((4, 70), (20, 86)), ((4, 97), (20, 113)), ((4, 124), (20, 140))]
    second_vein_location = [((264, 16), (280, 32)), ((264, 43), (280, 59)), ((264, 70), (280, 86)), ((264, 97), (280, 113)), ((264, 124), (280, 140))]
    third_vein_location = [((550, 16), (566, 32)), ((550, 43), (566, 59)), ((550, 70), (566, 86)), ((550, 97), (566, 113)), ((550, 124), (566, 140))]
    first_fuel_location = [((110, 207), (126, 223)), ((137, 207), (153, 223)), ((164, 207), (180, 223))]
    second_fuel_location = [((446, 207), (462, 223)), ((419, 207), (435, 223)), ((392, 207), (408, 223))]
    width = 572
    height = 228
    channels = 3
    yellow_color = (3, 118, 235)
    blue_color = (235, 120, 3)
    purple_color = (233, 2, 118)
    background_color_first = (236, 236, 236)
    background_color_first_area = (0, 228, 0, 286)
    background_color_second = (221, 192, 188)
    background_color_second_area = (0, 228, 286, 572)

    background_color_third = (145, 145, 145)
    background_color_third_area_first = (0, 202, 143, 147)
    background_color_third_area_second = (0, 202, 425, 429)
    background_color_third_area_third = (22, 26, 0, 572)
    background_color_third_area_fourth = (49, 53, 0, 572)
    background_color_third_area_fifth = (76, 80, 0, 572)
    background_color_third_area_sixth = (103, 107, 0, 572)
    background_color_third_area_seventh = (130, 134, 0, 572)
    background_color_third_area_eighth = (174, 178, 116, 174)
    background_color_third_area_ninth = (178, 202, 116, 120)
    background_color_third_area_tenth = (178, 202, 170, 174)
    background_color_third_area_eleventh = (178, 202, 398, 402)
    background_color_third_area_twelfth = (178, 202, 452, 456)
    background_color_third_area_thirteenth = (174, 178, 398, 456)

    background_color_fourth = (101, 167, 214)
    background_color_fourth_area_first = (202, 228, 105, 185)
    background_color_fourth_area_second = (202, 228, 387, 467)
    background_color_fourth_area_third = (10, 146, 0, 26)
    background_color_fourth_area_fourth = (10, 146, 260, 286)
    background_color_fourth_area_fifth = (10, 146, 546, 572)

    image = np.zeros((height, width, channels), dtype=np.uint8)
    image[background_color_first_area[0]:background_color_first_area[1], background_color_first_area[2]:background_color_first_area[3]] = background_color_first
    image[background_color_second_area[0]:background_color_second_area[1], background_color_second_area[2]:background_color_second_area[3]] = background_color_second

    image[background_color_third_area_first[0]:background_color_third_area_first[1], background_color_third_area_first[2]:background_color_third_area_first[3]] = background_color_third
    image[background_color_third_area_second[0]:background_color_third_area_second[1], background_color_third_area_second[2]:background_color_third_area_second[3]] = background_color_third
    image[background_color_third_area_third[0]:background_color_third_area_third[1], background_color_third_area_third[2]:background_color_third_area_third[3]] = background_color_third
    image[background_color_third_area_fourth[0]:background_color_third_area_fourth[1], background_color_third_area_fourth[2]:background_color_third_area_fourth[3]] = background_color_third
    image[background_color_third_area_fifth[0]:background_color_third_area_fifth[1], background_color_third_area_fifth[2]:background_color_third_area_fifth[3]] = background_color_third
    image[background_color_third_area_sixth[0]:background_color_third_area_sixth[1], background_color_third_area_sixth[2]:background_color_third_area_sixth[3]] = background_color_third
    image[background_color_third_area_seventh[0]:background_color_third_area_seventh[1], background_color_third_area_seventh[2]:background_color_third_area_seventh[3]] = background_color_third
    image[background_color_third_area_eighth[0]:background_color_third_area_eighth[1], background_color_third_area_eighth[2]:background_color_third_area_eighth[3]] = background_color_third
    image[background_color_third_area_ninth[0]:background_color_third_area_ninth[1], background_color_third_area_ninth[2]:background_color_third_area_ninth[3]] = background_color_third
    image[background_color_third_area_tenth[0]:background_color_third_area_tenth[1], background_color_third_area_tenth[2]:background_color_third_area_tenth[3]] = background_color_third
    image[background_color_third_area_eleventh[0]:background_color_third_area_eleventh[1], background_color_third_area_eleventh[2]:background_color_third_area_eleventh[3]] = background_color_third
    image[background_color_third_area_twelfth[0]:background_color_third_area_twelfth[1], background_color_third_area_twelfth[2]:background_color_third_area_twelfth[3]] = background_color_third
    image[background_color_third_area_thirteenth[0]:background_color_third_area_thirteenth[1], background_color_third_area_thirteenth[2]:background_color_third_area_thirteenth[3]] = background_color_third 

    image[background_color_fourth_area_first[0]:background_color_fourth_area_first[1], background_color_fourth_area_first[2]:background_color_fourth_area_first[3]] = background_color_fourth
    image[background_color_fourth_area_second[0]:background_color_fourth_area_second[1], background_color_fourth_area_second[2]:background_color_fourth_area_second[3]] = background_color_fourth
    image[background_color_fourth_area_third[0]:background_color_fourth_area_third[1], background_color_fourth_area_third[2]:background_color_fourth_area_third[3]] = background_color_fourth
    image[background_color_fourth_area_fourth[0]:background_color_fourth_area_fourth[1], background_color_fourth_area_fourth[2]:background_color_fourth_area_fourth[3]] = background_color_fourth
    image[background_color_fourth_area_fifth[0]:background_color_fourth_area_fifth[1], background_color_fourth_area_fifth[2]:background_color_fourth_area_fifth[3]] = background_color_fourth
    
    cv2.putText(image, 'A', (6, 166), cv2.FONT_HERSHEY_PLAIN, 1.7, (56, 56, 56), 2)
    cv2.putText(image, 'B', (266, 166), cv2.FONT_HERSHEY_PLAIN, 1.7, (56, 56, 56), 2)
    cv2.putText(image, 'C', (552, 166), cv2.FONT_HERSHEY_PLAIN, 1.7, (56, 56, 56), 2)
    cv2.putText(image, 'D', (187, 223), cv2.FONT_HERSHEY_PLAIN, 1.7, (56, 56, 56), 2)
    cv2.putText(image, 'E', (470, 223), cv2.FONT_HERSHEY_PLAIN, 1.7, (56, 56, 56), 2)
    # for i in range(0, 5):
    #     cv2.rectangle(image, first_vein_loaction[i][0], first_vein_loaction[i][1], purple_color, -1)
    #     cv2.rectangle(image, second_vein_location[i][0], second_vein_location[i][1], purple_color, -1)
    #     cv2.rectangle(image, third_vein_location[i][0], third_vein_location[i][1], purple_color, -1)
    # for i in range(0, 3):
    #     cv2.rectangle(image, first_fuel_location[i][0], first_fuel_location[i][1], purple_color, -1)
    #     cv2.rectangle(image, second_fuel_location[i][0], second_fuel_location[i][1], purple_color, -1)
    # cv2.imshow('image', image)
    # key = cv2.waitKey(0)
    # if key == ord('q'):
    #     cv2.destroyAllWindows()
    cv2.imwrite('VeinBackground.png', image)

def DrawStore():
    gray_color = (221, 192, 188)
    line_color = (160, 145, 141)
    store_color = (236, 236, 236)
    height = 277
    width = 232
    channels = 3

    first_store = [((24, 77), (54, 107)), ((64, 77), (94, 107)), ((138, 77), (168, 107)), ((178, 77), (208, 107))]
    second_store = [((24, 167), (54, 197)), ((64, 167), (94, 197)), ((138, 167), (168, 197)), ((178, 167), (208, 197))]
    image = np.zeros((height, width, channels), dtype=np.uint8)
    line_first_location = (90, 94, 0, 232)
    line_second_location = (180, 184, 0, 232)
    image[0:height, 0:width] = gray_color
    image[line_first_location[0]:line_first_location[1], line_first_location[2]:line_first_location[3]] = line_color
    image[line_second_location[0]:line_second_location[1], line_second_location[2]:line_second_location[3]] = line_color
    cv2.putText(image, 'B', (10, 267), cv2.FONT_HERSHEY_PLAIN, 1.7, (56, 56, 56), 2)
    cv2.putText(image, 'C', (205, 267), cv2.FONT_HERSHEY_PLAIN, 1.7, (56, 56, 56), 2)
    # for i in range(0, 4):
    #     cv2.rectangle(image, first_store[i][0], first_store[i][1], store_color, -1)
    #     cv2.rectangle(image, second_store[i][0], second_store[i][1], store_color, -1)
    # cv2.imshow('image', image)
    # key = cv2.waitKey(0)
    # if key == ord('q'):
    #     cv2.destroyAllWindows()
    cv2.imwrite('StoreBackground.png', image)


if __name__ == '__main__':
    # PictureCreate()
    # PictureSolve()  
    # PictureResult()
    # ButtonResult()
    # TogglePicture()
    # ImageShow()
    # ChangeColor()
    VeinPicture()
    # DrawPicture()
    DrawStore()