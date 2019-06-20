import cv2
import numpy as np
import json
import time


class HandAnnotation(object):
    """docstring for HandAnnotation"""

    def __init__(self):
        self.index_Img_start = 0
        self.index_Img_end = 5
        self.currentImg = None
        self.finger_index = 0
        self.clickTimes = 0
        self.tempPointsCenter = [(0, 0)]
        self.tempPointsThumb = [(0, 0), (0, 0), (0, 0)]
        self.tempPointsIndex = [(0, 0), (0, 0), (0, 0), (0, 0)]
        self.tempPointsMiddle = [(0, 0), (0, 0), (0, 0), (0, 0)]
        self.tempPointsRing = [(0, 0), (0, 0), (0, 0), (0, 0)]
        self.tempPointsLittle = [(0, 0), (0, 0), (0, 0), (0, 0)]
        label_time = time.asctime(time.localtime(time.time()))
        self.wholeData = {"label time": label_time}

    def addKeyPoints(self, event, x, y, flags, _):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.clickTimes += 1
            print(self.clickTimes)
            # print(x, y)
            # print(self.FingerList[self.finger_index])

            # for hand center（red）
            if self.finger_index == 0:
                if self.clickTimes <= 1:
                    cv2.circle(self.currentImg, (x, y), 5, (0, 0, 255), -1)
                    self.tempPointsCenter[0] = (x, y)
            # for thumb （orange）
            elif self.finger_index == 1:
                if self.clickTimes <= 3:
                    cv2.circle(self.currentImg, (x, y), 5, (0, 165, 255), -1)
                    self.tempPointsThumb[self.clickTimes - 1] = (x, y)
            # for index （yellow）
            elif self.finger_index == 2:
                if self.clickTimes <= 4:
                    cv2.circle(self.currentImg, (x, y), 5, (0, 255, 255), -1)
                    self.tempPointsIndex[self.clickTimes - 1] = (x, y)
            # for middle（green）
            elif self.finger_index == 3:
                if self.clickTimes <= 4:
                    cv2.circle(self.currentImg, (x, y), 5, (0, 255, 0), -1)
                    self.tempPointsMiddle[self.clickTimes - 1] = (x, y)
            # for ring （blue）
            elif self.finger_index == 4:
                if self.clickTimes <= 4:
                    cv2.circle(self.currentImg, (x, y), 5, (255, 0, 0), -1)
                    self.tempPointsRing[self.clickTimes - 1] = (x, y)
            # for little（puple）
            elif self.finger_index == 5:
                if self.clickTimes <= 4:
                    cv2.circle(self.currentImg, (x, y), 5, (240, 32, 160), -1)
                    self.tempPointsLittle[self.clickTimes - 1] = (x, y)

    def saveKeyPoints(self, index_Img):

        # save the data in json
        KeyPointsData = {}
        KeyPointsData['HandCenter'] = self.tempPointsCenter
        Thumb = {}
        for i in range(3):
            Thumb[str(i)] = self.tempPointsThumb[i]

        IndexFinger = {}
        for i in range(4):
            IndexFinger[str(i)] = self.tempPointsIndex[i]

        MiddleFinger = {}
        for i in range(4):
            MiddleFinger[str(i)] = self.tempPointsMiddle[i]

        RingFinger = {}
        for i in range(4):
            RingFinger[str(i)] = self.tempPointsRing[i]

        LittleFinger = {}
        for i in range(4):
            LittleFinger[str(i)] = self.tempPointsLittle[i]

        KeyPointsData['thumb'] = Thumb
        KeyPointsData['indexFinger'] = IndexFinger
        KeyPointsData['middleFinger'] = MiddleFinger
        KeyPointsData['ringFinger'] = RingFinger
        KeyPointsData['littleFinger'] = LittleFinger

        self.wholeData['Image_' + str(index_Img)] = KeyPointsData

        with open("res/KeyPoints.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(self.wholeData, indent=2))

        print("saved successfully")

    def Annotation(self):
        print("now it is hand Center")
        index_Img = self.index_Img_start
        self.currentImg = cv2.imread("res/" + str(index_Img) + ".JPG")
        # when left click, add the point
        cv2.namedWindow("Hand Annotation Tool")
        cv2.setMouseCallback("Hand Annotation Tool", self.addKeyPoints)
        while(1):
            cv2.imshow("Hand Annotation Tool", self.currentImg)
            key = cv2.waitKey(66)
            # n for next image
            if key & 0xff == ord('n'):
                if index_Img == self.index_Img_end:
                    print("show all of the images")
                    break
                else:
                    index_Img += 1
                    self.finger_index = 0
                    self.clickTimes = 0
                    self.tempPointsCenter = [(0, 0)]
                    self.tempPointsThumb = [(0, 0), (0, 0), (0, 0)]
                    self.tempPointsOthers = [
                        (0, 0), (0, 0), (0, 0), (0, 0)]
                    self.currentImg = cv2.imread(
                        "res/" + str(index_Img) + ".JPG")
                    print("show next image:", index_Img)
                    print("now it is hand Center")

            # s for saving the points
            elif key & 0xff == ord('s'):
                self.saveKeyPoints(index_Img)

            # c for cleaning the points and datas
            elif key & 0xff == ord('c'):
                self.finger_index = 0
                self.clickTimes = 0
                self.tempPointsCenter = [(0, 0)]
                self.tempPointsThumb = [(0, 0), (0, 0), (0, 0)]
                self.tempPointsOthers = [(0, 0), (0, 0), (0, 0), (0, 0)]
                self.currentImg = cv2.imread("res/" + str(index_Img) + ".JPG")
                print("now it is hand Center")

            # space for changing the fingers
            elif key == 32:
                self.clickTimes = 0
                self.finger_index += 1
                if self.finger_index == 6:
                    self.finger_index = 0
                    print("now it is hand Center")
                else:
                    print("now it is finger:", self.finger_index)

            # esc for quit
            elif key == 27:
                break
        cv2.destroyAllWindows()

    def Display(self, labels):
        for i in range(self.index_Img_end - self.index_Img_start + 1):
            HandImg = cv2.imread("res/" + str(i) + ".JPG")
            # cv2.imshow("predict result", HandImg)
            wholeData = df['Image_' + str(i)]

            Center = tuple(wholeData['HandCenter'][0])
            cv2.circle(HandImg, Center, 5, (0, 0, 255), -1)
            thumbs = {}
            for i in range(3):
                thumbs[i] = tuple(wholeData['thumb'][str(i)])
                cv2.circle(HandImg, thumbs[i], 5, (0, 165, 255), -1)
            indexs = {}
            for i in range(4):
                indexs[i] = tuple(wholeData['indexFinger'][str(i)])
                cv2.circle(HandImg, indexs[i], 5, (0, 255, 255), -1)
            middles = {}
            for i in range(4):
                middles[i] = tuple(wholeData['middleFinger'][str(i)])
                cv2.circle(HandImg, middles[i], 5, (0, 255, 0), -1)
            rings = {}
            for i in range(4):
                rings[i] = tuple(wholeData['ringFinger'][str(i)])
                cv2.circle(HandImg, rings[i], 5, (255, 0, 0), -1)
            littles = {}
            for i in range(4):
                littles[i] = tuple(wholeData['littleFinger'][str(i)])
                cv2.circle(HandImg, littles[i], 5, (240, 32, 160), -1)

            cv2.line(HandImg, Center, thumbs[0], (0, 0, 255))
            cv2.line(HandImg, Center, indexs[0], (0, 0, 255))
            cv2.line(HandImg, Center, middles[0], (0, 0, 255))
            cv2.line(HandImg, Center, rings[0], (0, 0, 255))
            cv2.line(HandImg, Center, littles[0], (0, 0, 255))

            cv2.line(HandImg, thumbs[0], thumbs[1], (0, 165, 255))
            cv2.line(HandImg, thumbs[1], thumbs[2], (0, 165, 255))

            cv2.line(HandImg, indexs[0], indexs[1], (0, 255, 255))
            cv2.line(HandImg, indexs[1], indexs[2], (0, 255, 255))
            cv2.line(HandImg, indexs[2], indexs[3], (0, 255, 255))

            cv2.line(HandImg, middles[0], middles[1], (0, 255, 0))
            cv2.line(HandImg, middles[1], middles[2], (0, 255, 0))
            cv2.line(HandImg, middles[2], middles[3], (0, 255, 0))

            cv2.line(HandImg, rings[0], rings[1], (255, 0, 0))
            cv2.line(HandImg, rings[1], rings[2], (255, 0, 0))
            cv2.line(HandImg, rings[2], rings[3], (255, 0, 0))

            cv2.line(HandImg, littles[0], littles[1], (240, 32, 160))
            cv2.line(HandImg, littles[1], littles[2], (240, 32, 160))
            cv2.line(HandImg, littles[2], littles[3], (240, 32, 160))

            cv2.imshow("predict result", HandImg)
            cv2.waitKey(0)

            # cv2.circle(HandImg, (x, y), 5, (0, 0, 255), -1)


if __name__ == '__main__':
	# for label
    HandAnnotation().Annotation()
    # for showing the result
    # with open("res/KeyPoints.json") as f:
    #     df = json.load(f)
    # HandAnnotation().Display(df)
