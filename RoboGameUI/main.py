import sys
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow,QApplication,QGraphicsView,QGraphicsPixmapItem,QGraphicsScene,QLabel
from PIL import Image, ImageDraw, ImageEnhance
from PyQt5.QtWidgets import QGraphicsOpacityEffect, QPushButton, QCheckBox

import numpy as np
import cv2
import random
import time

class MainCode(QMainWindow):
	screen_width = 0
	screen_height = 0

	red_score_number = 0
	red_score_extra_number = 0
	red_fuel_number = 0
	red_bonanza_number = 0
	red_leanore_number = 0

	blue_score_number = 0
	blue_score_extra_number = 0
	blue_fuel_number = 0
	blue_bonanza_number = 0
	blue_leanore_number = 0

	one_min_heart_clock_number = 0
	five_min_heart_clock_number = 0
	red_flag = 0
	blue_flag = 0

	first_vein_loaction = [((4, 16), (20, 32)), ((4, 43), (20, 59)), ((4, 70), (20, 86)), ((4, 97), (20, 113)), ((4, 124), (20, 140))]
	second_vein_location = [((264, 16), (280, 32)), ((264, 43), (280, 59)), ((264, 70), (280, 86)), ((264, 97), (280, 113)), ((264, 124), (280, 140))]
	third_vein_location = [((550, 16), (566, 32)), ((550, 43), (566, 59)), ((550, 70), (566, 86)), ((550, 97), (566, 113)), ((550, 124), (566, 140))]
	first_fuel_location = [((110, 207), (126, 223)), ((137, 207), (153, 223)), ((164, 207), (180, 223))]
	second_fuel_location = [((446, 207), (462, 223)), ((419, 207), (435, 223)), ((392, 207), (408, 223))]
	
	first_store_location = [((24, 77), (54, 107)), ((64, 77), (94, 107)), ((138, 77), (168, 107)), ((178, 77), (208, 107))]
	second_store_location = [((24, 167), (54, 197)), ((64, 167), (94, 197)), ((138, 167), (168, 197)), ((178, 167), (208, 197))]
	
	yellow_color = (3, 118, 235)
	blue_color = (235, 120, 3)
	purple_color = (233, 2, 118)
	store_color = (236, 236, 236)

	def NegativeToZero(self, num):
		if num >= 0:
			return num
		else:
			return 0
		
	def MinuteNegativeToSixty(self, num):
		if num % 60 == 0:
			return(num // 60 - 1)
		else:
			return(num // 60)

	def SecondNegativeToSixty(self, num):
		if num % 60 == 0:
			return 0
		else:
			return(60 - num % 60)

	def __init__(self):
		super(MainCode, self).__init__()
		QMainWindow.__init__(self)
		self.UI_init()

	#获取屏幕尺寸
	def getScreenSize(self):
		screen = QtWidgets.QDesktopWidget().screenGeometry()
		screen_width, screen_height = screen.width(), screen.height()
		return screen_width, screen_height
	
	#设置窗口尺寸
	def setScreenSize(self):
		# self.screen_width = 1920
		# self.screen_height = 1080
		self.resize(self.screen_width, self.screen_height)
		
	
	#初始化UI
	def UI_init(self):
		self.screen_width, self.screen_height = self.getScreenSize()
		self.setScreenSize()
		self.setWindowTitle("2023Robogame UI")

		#设置背景
		label_background = QLabel(self)
		pixmap_background = QPixmap("./Source/Pic/Faded.png")
		label_background.setPixmap(pixmap_background)
		label_background.setGeometry(0, 0, self.screen_width, self.screen_height)
		label_background.setScaledContents(True)

		#设置标题
		label_title = QLabel(self)
		pixmap_title = QPixmap("./Source/Pic/TitleInverted.png")
		label_title.setPixmap(pixmap_title)
		label_title.setGeometry(int(0.15*self.screen_width), int(0.075*self.screen_height), 
			  int(0.63*self.screen_width), int(0.1*self.screen_height))
		label_title.setScaledContents(True)

		#设置标题旁LOGO
		label_logo = QLabel(self)
		pixmap_logo = QPixmap("./Source/Pic/Robogame LOGO.png")
		label_logo.setPixmap(pixmap_logo)
		label_logo.setGeometry(int(0.78*self.screen_width), int(0.075*self.screen_height), 
			 int(0.07*self.screen_width), int(0.12*self.screen_height))
		label_logo.setScaledContents(True)

		#设置QTimer
		self.one_min_heart_clock = QTimer(self)
		self.one_min_heart_clock.timeout.connect(self.OneMinUpdateTime)

		self.five_min_heart_clock = QTimer(self)
		self.five_min_heart_clock.timeout.connect(self.FiveMinUpdateTime)

		#设置按键
		red_style_sheet = "QPushButton{border-image: url(./Source/Pic/RedButton.png);font-size:"+str(int(0.009*self.screen_width))+"px;font-weight:900;color:rgb(255,255,255);font-family:Microsoft YaHei}" \
				+ "QPushButton:hover{border-image: url(./Source/Pic/RedButtonHover.png);font-size:"+str(int(0.009*self.screen_width))+"px;font-weight:900;color:rgb(255,255,255);font-family:Microsoft YaHei}" \
				+ "QPushButton:pressed{border-image: url(./Source/Pic/RedButtonPress.png);font-size:"+str(int(0.009*self.screen_width))+"px;font-weight:900;color:rgb(255,255,255);font-family:Microsoft YaHei}"

		blue_style_sheet = "QPushButton{border-image: url(./Source/Pic/BlueButton.png);font-size:"+str(int(0.009*self.screen_width))+"px;font-weight:900;color:rgb(255,255,255);font-family:Microsoft YaHei}" \
				+ "QPushButton:hover{border-image: url(./Source/Pic/BlueButtonHover.png);font-size:"+str(int(0.009*self.screen_width))+"px;font-weight:900;color:rgb(255,255,255);font-family:Microsoft YaHei}" \
				+ "QPushButton:pressed{border-image: url(./Source/Pic/BlueButtonPress.png);font-size:"+str(int(0.009*self.screen_width))+"px;font-weight:900;color:rgb(255,255,255);font-family:Microsoft YaHei}"
		
		yellow_style_sheet = "QPushButton{border-image: url(./Source/Pic/YellowButton.png);font-size:"+str(int(0.009*self.screen_width))+"px;font-weight:900;color:rgb(255,255,255);font-family:Microsoft YaHei}" \
				+ "QPushButton:hover{border-image: url(./Source/Pic/YellowButtonHover.png);font-size:"+str(int(0.009*self.screen_width))+"px;font-weight:900;color:rgb(255,255,255);font-family:Microsoft YaHei}" \
				+ "QPushButton:pressed{border-image: url(./Source/Pic/YellowButtonPress.png);font-size:"+str(int(0.009*self.screen_width))+"px;font-weight:900;color:rgb(255,255,255);font-family:Microsoft YaHei}"

		button_red_stop = QPushButton(self)
		button_red_stop.setText("红队停止计时")
		button_red_stop.setGeometry(int(0.38*self.screen_width), int(0.33*self.screen_height),
			    int(0.06*self.screen_width), int(0.05*self.screen_height))
		button_red_stop.setStyleSheet(red_style_sheet)
		button_red_stop.clicked.connect(self.RedStop)

		button_start = QPushButton(self)
		button_start.setText("开始计时")
		button_start.setGeometry(int(0.47*self.screen_width), int(0.33*self.screen_height),
			    int(0.06*self.screen_width), int(0.05*self.screen_height))
		button_start.setStyleSheet(yellow_style_sheet)
		button_start.clicked.connect(self.FiveMinStart)
		
		button_blue_stop = QPushButton(self)
		button_blue_stop.setText("蓝队停止计时")
		button_blue_stop.setGeometry(int(0.56*self.screen_width), int(0.33*self.screen_height),
			    int(0.06*self.screen_width), int(0.05*self.screen_height))
		button_blue_stop.setStyleSheet(blue_style_sheet)
		button_blue_stop.clicked.connect(self.BlueStop)

		button_location_create = QPushButton(self)
		button_location_create.setText("生成矿脉位置")
		button_location_create.setGeometry(int(0.38*self.screen_width), int(0.4*self.screen_height),
				int(0.06*self.screen_width), int(0.05*self.screen_height))
		button_location_create.setStyleSheet(yellow_style_sheet)
		button_location_create.clicked.connect(self.SetVeinAndStore)
		
		button_reset = QPushButton(self)
		button_reset.setText("复位")
		button_reset.setGeometry(int(0.47*self.screen_width), int(0.4*self.screen_height),
				int(0.06*self.screen_width), int(0.05*self.screen_height))
		button_reset.setStyleSheet(yellow_style_sheet)
		button_reset.clicked.connect(self.Reset)
		
		self.one_min_count = QPushButton(self)
		self.one_min_count.setText("1分钟倒计时")
		self.one_min_count.setGeometry(int(0.56*self.screen_width), int(0.4*self.screen_height),
				int(0.06*self.screen_width), int(0.05*self.screen_height))
		self.one_min_count.setStyleSheet(yellow_style_sheet)
		self.one_min_count.clicked.connect(self.OneMinStart)

		#设置队伍状态
		self.red_state = QLabel(self)
		self.red_state.setText("红队准备中...")
		self.red_state.setGeometry(int(0.22*self.screen_width), int(0.488*self.screen_height),
				int(0.089*self.screen_width), int(0.034*self.screen_height))
		self.red_state.setStyleSheet("QLabel{background-color:rgb(175, 0, 0); font-weight:bold; font-family:Microsoft YaHei; color:white; border: 1px solid white; border-radius: 10px; padding:2px 4px}")
		self.red_state.setAlignment(Qt.AlignCenter)

		self.blue_state = QLabel(self)
		self.blue_state.setText("蓝队准备中...")
		self.blue_state.setGeometry(int(0.691*self.screen_width), int(0.488*self.screen_height),
				int(0.089*self.screen_width), int(0.034*self.screen_height))
		self.blue_state.setStyleSheet("QLabel{background-color:rgb(0, 119, 235); font-weight:bold; font-family:Microsoft YaHei; color:white; border: 1px solid white; border-radius: 10px; padding:2px 4px}")
		self.blue_state.setAlignment(Qt.AlignCenter)

		#设置积分器
		self.red_score = QLabel(self)
		self.red_score.setText("0")
		self.red_score.setGeometry(int(0.22*self.screen_width), int(0.348*self.screen_height),
				int(0.089*self.screen_width), int(0.14*self.screen_height))
		self.red_score.setStyleSheet("QLabel{background-color:rgb(175, 0, 0); font-size:"+str(int(0.065*self.screen_width))+"px; font-weight:bold; font-family:Microsoft YaHei; color:white; border: 1px solid white; border-radius: 10px; padding:2px 4px}")
		self.red_score.setAlignment(Qt.AlignCenter)

		self.blue_score = QLabel(self)
		self.blue_score.setText("0")
		self.blue_score.setGeometry(int(0.691*self.screen_width), int(0.348*self.screen_height),
				int(0.089*self.screen_width), int(0.14*self.screen_height))
		self.blue_score.setStyleSheet("QLabel{background-color:rgb(0, 119, 235); font-size:"+str(int(0.065*self.screen_width))+"px; font-weight:bold; font-family:Microsoft YaHei; color:white; border: 1px solid white; border-radius: 10px; padding:2px 4px}")
		self.blue_score.setAlignment(Qt.AlignCenter)

		#设置富矿计数器及其加减按钮
		self.red_bonanza_count = QLabel(self)
		self.red_bonanza_count.setText("0")
		self.red_bonanza_count.setGeometry(int(0.22*self.screen_width), int(0.276*self.screen_height),
				int(0.029*self.screen_width), int(0.048*self.screen_height))
		self.red_bonanza_count.setStyleSheet("QLabel{background-color:rgb(255, 136, 0); font-size:"+str(int(0.038*self.screen_height))+"px; font-weight:bold; font-family:Microsoft YaHei; color:white; border: 1px solid white; border-radius: 10px; padding:2px 4px}")
		self.red_bonanza_count.setAlignment(Qt.AlignCenter)

		red_bonanza_count_crease = QPushButton(self)
		red_bonanza_count_crease.setText("+")
		red_bonanza_count_crease.setGeometry(int(0.22*self.screen_width), int(0.251*self.screen_height),
				int(0.029*self.screen_width), int(0.024*self.screen_height))
		red_bonanza_count_crease.setStyleSheet(red_style_sheet)
		red_bonanza_count_crease.clicked.connect(self.RedBonanzaButtonCrease)

		red_bonanza_count_decrease = QPushButton(self)
		red_bonanza_count_decrease.setText("-")
		red_bonanza_count_decrease.setGeometry(int(0.22*self.screen_width), int(0.324*self.screen_height),
				int(0.029*self.screen_width), int(0.024*self.screen_height))
		red_bonanza_count_decrease.setStyleSheet(red_style_sheet)
		red_bonanza_count_decrease.clicked.connect(self.RedBonanzaButtonDecrease)

		self.blue_bonanza_count = QLabel(self)
		self.blue_bonanza_count.setText("0")
		self.blue_bonanza_count.setGeometry(int(0.691*self.screen_width), int(0.276*self.screen_height),
				int(0.029*self.screen_width), int(0.048*self.screen_height))
		self.blue_bonanza_count.setStyleSheet("QLabel{background-color:rgb(255, 136, 0); font-size:"+str(int(0.038*self.screen_height))+"px; font-weight:bold; font-family:Microsoft YaHei; color:white; border: 1px solid white; border-radius: 10px; padding:2px 4px}")
		self.blue_bonanza_count.setAlignment(Qt.AlignCenter)

		blue_bonanza_count_crease = QPushButton(self)
		blue_bonanza_count_crease.setText("+")
		blue_bonanza_count_crease.setGeometry(int(0.691*self.screen_width), int(0.251*self.screen_height),
				int(0.029*self.screen_width), int(0.024*self.screen_height))
		blue_bonanza_count_crease.setStyleSheet(blue_style_sheet)
		blue_bonanza_count_crease.clicked.connect(self.BlueBonanzaButtonCrease)

		blue_bonanza_count_decrease = QPushButton(self)
		blue_bonanza_count_decrease.setText("-")
		blue_bonanza_count_decrease.setGeometry(int(0.691*self.screen_width), int(0.324*self.screen_height),
				int(0.029*self.screen_width), int(0.024*self.screen_height))
		blue_bonanza_count_decrease.setStyleSheet(blue_style_sheet)
		blue_bonanza_count_decrease.clicked.connect(self.BlueBonanzaButtonDecrease)

		#设置贫矿计数器及其加减按钮
		self.red_leanore_count = QLabel(self)
		self.red_leanore_count.setText("0")
		self.red_leanore_count.setGeometry(int(0.250*self.screen_width), int(0.276*self.screen_height),
				int(0.029*self.screen_width), int(0.048*self.screen_height))
		self.red_leanore_count.setStyleSheet("QLabel{background-color:rgb(0, 85, 255); font-size:"+str(int(0.038*self.screen_height))+"px; font-weight:bold; font-family:Microsoft YaHei; color:white; border: 1px solid white; border-radius: 10px; padding:2px 4px}")
		self.red_leanore_count.setAlignment(Qt.AlignCenter)

		red_leanore_count_crease = QPushButton(self)
		red_leanore_count_crease.setText("+")
		red_leanore_count_crease.setGeometry(int(0.250*self.screen_width), int(0.251*self.screen_height),
				int(0.029*self.screen_width), int(0.024*self.screen_height))
		red_leanore_count_crease.setStyleSheet(red_style_sheet)
		red_leanore_count_crease.clicked.connect(self.RedLeanoreButtonCrease)

		red_fuel_count_decrease = QPushButton(self)
		red_fuel_count_decrease.setText("-")
		red_fuel_count_decrease.setGeometry(int(0.250*self.screen_width), int(0.324*self.screen_height),
				int(0.029*self.screen_width), int(0.024*self.screen_height))
		red_fuel_count_decrease.setStyleSheet(red_style_sheet)
		red_fuel_count_decrease.clicked.connect(self.RedLeanoreButtonDecrease)

		self.blue_leanore_count = QLabel(self)
		self.blue_leanore_count.setText("0")
		self.blue_leanore_count.setGeometry(int(0.721*self.screen_width), int(0.276*self.screen_height),
				int(0.029*self.screen_width), int(0.048*self.screen_height))
		self.blue_leanore_count.setStyleSheet("QLabel{background-color:rgb(0, 85, 255); font-size:"+str(int(0.038*self.screen_height))+"px; font-weight:bold; font-family:Microsoft YaHei; color:white; border: 1px solid white; border-radius: 10px; padding:2px 4px}")
		self.blue_leanore_count.setAlignment(Qt.AlignCenter)

		blue_leanore_count_crease = QPushButton(self)
		blue_leanore_count_crease.setText("+")
		blue_leanore_count_crease.setGeometry(int(0.721*self.screen_width), int(0.251*self.screen_height),
				int(0.029*self.screen_width), int(0.024*self.screen_height))
		blue_leanore_count_crease.setStyleSheet(blue_style_sheet)
		blue_leanore_count_crease.clicked.connect(self.BlueLeanoreButtonCrease)

		blue_leanore_count_decrease = QPushButton(self)
		blue_leanore_count_decrease.setText("-")
		blue_leanore_count_decrease.setGeometry(int(0.721*self.screen_width), int(0.324*self.screen_height),
				int(0.029*self.screen_width), int(0.024*self.screen_height))
		blue_leanore_count_decrease.setStyleSheet(blue_style_sheet)
		blue_leanore_count_decrease.clicked.connect(self.BlueLeanoreButtonDecrease)

		#设置燃料计数器
		self.red_fuel_count = QLabel(self)
		self.red_fuel_count.setText("0")
		self.red_fuel_count.setGeometry(int(0.280*self.screen_width), int(0.276*self.screen_height),
				int(0.029*self.screen_width), int(0.048*self.screen_height))
		self.red_fuel_count.setStyleSheet("QLabel{background-color:rgb(187, 0, 255); font-size:"+str(int(0.038*self.screen_height))+"px; font-weight:bold; font-family:Microsoft YaHei; color:white; border: 1px solid white; border-radius: 10px; padding:2px 4px}")
		self.red_fuel_count.setAlignment(Qt.AlignCenter)

		red_fuel_count_crease = QPushButton(self)
		red_fuel_count_crease.setText("+")
		red_fuel_count_crease.setGeometry(int(0.280*self.screen_width), int(0.251*self.screen_height),
				int(0.029*self.screen_width), int(0.024*self.screen_height))
		red_fuel_count_crease.setStyleSheet(red_style_sheet)
		red_fuel_count_crease.clicked.connect(self.RedFuelButtonCrease)

		red_fuel_count_decrease = QPushButton(self)
		red_fuel_count_decrease.setText("-")
		red_fuel_count_decrease.setGeometry(int(0.280*self.screen_width), int(0.324*self.screen_height),
				int(0.029*self.screen_width), int(0.024*self.screen_height))
		red_fuel_count_decrease.setStyleSheet(red_style_sheet)
		red_fuel_count_decrease.clicked.connect(self.RedFuelButtonDecrease)

		self.blue_fuel_count = QLabel(self)
		self.blue_fuel_count.setText("0")
		self.blue_fuel_count.setGeometry(int(0.751*self.screen_width), int(0.276*self.screen_height),
				int(0.029*self.screen_width), int(0.048*self.screen_height))
		self.blue_fuel_count.setStyleSheet("QLabel{background-color:rgb(187, 0, 255); font-size:"+str(int(0.038*self.screen_height))+"px; font-weight:bold; font-family:Microsoft YaHei; color:white; border: 1px solid white; border-radius: 10px; padding:2px 4px}")
		self.blue_fuel_count.setAlignment(Qt.AlignCenter)

		blue_fuel_count_crease = QPushButton(self)
		blue_fuel_count_crease.setText("+")
		blue_fuel_count_crease.setGeometry(int(0.751*self.screen_width), int(0.251*self.screen_height),
				int(0.029*self.screen_width), int(0.024*self.screen_height))
		blue_fuel_count_crease.setStyleSheet(blue_style_sheet)
		blue_fuel_count_crease.clicked.connect(self.BlueFuelButtonCrease)

		blue_fuel_count_decrease = QPushButton(self)
		blue_fuel_count_decrease.setText("-")
		blue_fuel_count_decrease.setGeometry(int(0.751*self.screen_width), int(0.324*self.screen_height),
				int(0.029*self.screen_width), int(0.024*self.screen_height))
		blue_fuel_count_decrease.setStyleSheet(blue_style_sheet)
		blue_fuel_count_decrease.clicked.connect(self.BlueFuelButtonDecrease)

		#设置富矿QLabel
		red_bonanza_sign = QLabel(self)
		red_bonanza_sign.setText("富矿数")
		red_bonanza_sign.setGeometry(int(0.22*self.screen_width), int(0.225*self.screen_height),
				int(0.029*self.screen_width), int(0.024*self.screen_height))
		red_bonanza_sign.setStyleSheet("QLabel{background-color:rgb(175, 0, 0); font-size:"+str(int(0.012*self.screen_height))+"px; font-family:Microsoft YaHei; color:white;}")
		red_bonanza_sign.setAlignment(Qt.AlignCenter)

		blue_bonanza_sign = QLabel(self)
		blue_bonanza_sign.setText("富矿数")
		blue_bonanza_sign.setGeometry(int(0.691*self.screen_width), int(0.225*self.screen_height),
				int(0.029*self.screen_width), int(0.024*self.screen_height))
		blue_bonanza_sign.setStyleSheet("QLabel{background-color:rgb(0, 119, 235); font-size:"+str(int(0.012*self.screen_height))+"px; font-family:Microsoft YaHei; color:white;}")
		blue_bonanza_sign.setAlignment(Qt.AlignCenter)

		#设置贫矿QLabel
		red_leanore_sign = QLabel(self)
		red_leanore_sign.setText("贫矿数")
		red_leanore_sign.setGeometry(int(0.250*self.screen_width), int(0.225*self.screen_height),
				int(0.029*self.screen_width), int(0.024*self.screen_height))
		red_leanore_sign.setStyleSheet("QLabel{background-color:rgb(175, 0, 0); font-size:"+str(int(0.012*self.screen_height))+"px; font-family:Microsoft YaHei; color:white;}")
		red_leanore_sign.setAlignment(Qt.AlignCenter)

		blue_leanore_sign = QLabel(self)
		blue_leanore_sign.setText("贫矿数")
		blue_leanore_sign.setGeometry(int(0.721*self.screen_width), int(0.225*self.screen_height),
				int(0.029*self.screen_width), int(0.0254*self.screen_height))
		blue_leanore_sign.setStyleSheet("QLabel{background-color:rgb(0, 119, 235); font-size:"+str(int(0.012*self.screen_height))+"px; font-family:Microsoft YaHei; color:white;}")
		blue_leanore_sign.setAlignment(Qt.AlignCenter)

		#设置燃料QLabel
		red_fuel_sign = QLabel(self)
		red_fuel_sign.setText("燃料数")
		red_fuel_sign.setGeometry(int(0.280*self.screen_width), int(0.225*self.screen_height),
				int(0.029*self.screen_width), int(0.024*self.screen_height))
		red_fuel_sign.setStyleSheet("QLabel{background-color:rgb(175, 0, 0); font-size:"+str(int(0.012*self.screen_height))+"px; font-family:Microsoft YaHei; color:white;}")
		red_fuel_sign.setAlignment(Qt.AlignCenter)

		blue_fuel_sign = QLabel(self)
		blue_fuel_sign.setText("燃料数")
		blue_fuel_sign.setGeometry(int(0.751*self.screen_width), int(0.225*self.screen_height),
				int(0.029*self.screen_width), int(0.024*self.screen_height))
		blue_fuel_sign.setStyleSheet("QLabel{background-color:rgb(0, 119, 235); font-size:"+str(int(0.012*self.screen_height))+"px; font-family:Microsoft YaHei; color:white;}")
		blue_fuel_sign.setAlignment(Qt.AlignCenter)

		#设置计时器
		self.red_time_count = QLabel(self)
		self.red_time_count.setText("05:00")
		self.red_time_count.setGeometry(int(0.31*self.screen_width), int(0.23*self.screen_height),
				int(0.15*self.screen_width), int(0.07*self.screen_height))
		self.red_time_count.setStyleSheet("QLabel{font-size:"+str(int(0.05*self.screen_height))+"px; font-weight:bold; font-family:Microsoft YaHei; color:red;}")
		self.red_time_count.setAlignment(Qt.AlignCenter)

		self.blue_time_count = QLabel(self)
		self.blue_time_count.setText("05:00")
		self.blue_time_count.setGeometry(int(0.54*self.screen_width), int(0.23*self.screen_height),
				int(0.15*self.screen_width), int(0.07*self.screen_height))
		self.blue_time_count.setStyleSheet("QLabel{font-size:"+str(int(0.05*self.screen_height))+"px; font-weight:bold; font-family:Microsoft YaHei; color:rgb(0, 119, 235);}")
		self.blue_time_count.setAlignment(Qt.AlignCenter)

		self.one_minute_count = QLabel(self)
		self.one_minute_count.setText("01:00")
		self.one_minute_count.setGeometry(int(0.425*self.screen_width), int(0.23*self.screen_height),
				int(0.15*self.screen_width), int(0.07*self.screen_height))
		self.one_minute_count.setStyleSheet("QLabel{font-size:"+str(int(0.05*self.screen_height))+"px; font-weight:bold; font-family:Microsoft YaHei; color:rgb(239, 118, 0);}")
		self.one_minute_count.setAlignment(Qt.AlignCenter)

		#设置矿脉生成图
		self.vein_generation_label = QLabel(self)
		self.vein_generation_label.setGeometry(int(0.28*self.screen_width), int(0.60*self.screen_height),
				int(0.36*self.screen_width), int(0.28*self.screen_height))
		pixmap_vein = QPixmap("./Source/Pic/VeinBackground.png")
		self.vein_generation_label.setPixmap(pixmap_vein)
		self.vein_generation_label.setScaledContents(True)

		self.store_generation_label = QLabel(self)
		self.store_generation_label.setGeometry(int(0.64*self.screen_width), int(0.55*self.screen_height),
				int(0.13*self.screen_width), int(0.21*self.screen_height))
		pixmap_store = QPixmap("./Source/Pic/StoreBackground.png")
		self.store_generation_label.setPixmap(pixmap_store)
		self.store_generation_label.setScaledContents(True)

		#矿脉字体图
		vein_font = QLabel(self)
		vein_font.setGeometry(int(0.35*self.screen_width), int(0.52*self.screen_height),
				int(0.22*self.screen_width), int(0.08*self.screen_height))
		vein_pixmap = QPixmap('./Source/Pic/VeinTips.png')
		vein_font.setPixmap(vein_pixmap)
		vein_font.setScaledContents(True)

		#设置基础加分项复选框
		red_basescore_qlabel = QLabel(self)
		red_basescore_qlabel.setText("红队基础加分项:")
		red_basescore_qlabel.setGeometry(int(0.1*self.screen_width), int(0.28*self.screen_height),
				int(0.15*self.screen_width), int(0.03*self.screen_height))
		red_basescore_qlabel.setStyleSheet("QLabel{font-size:"+str(int(0.018*self.screen_height))+"px; font-weight:bold; font-family:Microsoft YaHei; color:black;}")
		red_basescore_qlabel.setAlignment(Qt.AlignLeft)

		red_basescore_background = QLabel(self)
		red_basescore_pixmap = QPixmap("./Source/Pic/Frame.png")
		red_basescore_background.setPixmap(red_basescore_pixmap)
		red_basescore_background.setGeometry(int(0.08*self.screen_width), int(0.185*self.screen_height),
				int(0.13*self.screen_width), int(0.29*self.screen_height))
		red_basescore_background.setScaledContents(True)

		self.red_basescore_checkbox_first = QCheckBox("成功到达采矿区", self)
		self.red_basescore_checkbox_first.setGeometry(int(0.1*self.screen_width), int(0.31*self.screen_height),
				int(0.15*self.screen_width), int(0.03*self.screen_height))
		self.red_basescore_checkbox_first.setStyleSheet("QCheckBox{font-size:"+str(int(0.018*self.screen_height))+"px; font-weight:bold; font-family:Microsoft YaHei; color:black;}")
		self.red_basescore_checkbox_first.stateChanged.connect(self.RedCheckboxFirst)
		
		self.red_basescore_checkbox_second = QCheckBox("成功抓取燃料矿", self)
		self.red_basescore_checkbox_second.setGeometry(int(0.1*self.screen_width), int(0.34*self.screen_height),
				int(0.15*self.screen_width), int(0.03*self.screen_height))
		self.red_basescore_checkbox_second.setStyleSheet("QCheckBox{font-size:"+str(int(0.018*self.screen_height))+"px; font-weight:bold; font-family:Microsoft YaHei; color:black;}")
		self.red_basescore_checkbox_second.stateChanged.connect(self.RedCheckboxSecond)

		self.red_basescore_checkbox_third = QCheckBox("成功抓取晶体矿", self)
		self.red_basescore_checkbox_third.setGeometry(int(0.1*self.screen_width), int(0.37*self.screen_height),
				int(0.15*self.screen_width), int(0.03*self.screen_height))
		self.red_basescore_checkbox_third.setStyleSheet("QCheckBox{font-size:"+str(int(0.018*self.screen_height))+"px; font-weight:bold; font-family:Microsoft YaHei; color:black;}")
		self.red_basescore_checkbox_third.stateChanged.connect(self.RedCheckboxThird)

		blue_basescore_qlabel = QLabel(self)
		blue_basescore_qlabel.setText("蓝队基础加分项:")
		blue_basescore_qlabel.setGeometry(int(0.81*self.screen_width), int(0.28*self.screen_height),
				int(0.15*self.screen_width), int(0.03*self.screen_height))
		blue_basescore_qlabel.setStyleSheet("QLabel{font-size:"+str(int(0.018*self.screen_height))+"px; font-weight:bold; font-family:Microsoft YaHei; color:black;}")
		blue_basescore_qlabel.setAlignment(Qt.AlignLeft)

		blue_basescore_frame = QLabel(self)
		blue_basescore_pixmap = QPixmap("./Source/Pic/Frame.png")
		blue_basescore_frame.setPixmap(blue_basescore_pixmap)
		blue_basescore_frame.setGeometry(int(0.79*self.screen_width), int(0.185*self.screen_height),
				int(0.13*self.screen_width), int(0.29*self.screen_height))
		blue_basescore_frame.setScaledContents(True)

		self.blue_basescore_checkbox_first = QCheckBox("成功到达采矿区", self)
		self.blue_basescore_checkbox_first.setGeometry(int(0.81*self.screen_width), int(0.31*self.screen_height),
				int(0.15*self.screen_width), int(0.03*self.screen_height))
		self.blue_basescore_checkbox_first.setStyleSheet("QCheckBox{font-size:"+str(int(0.018*self.screen_height))+"px; font-weight:bold; font-family:Microsoft YaHei; color:black;}")
		self.blue_basescore_checkbox_first.stateChanged.connect(self.BlueCheckboxFirst)

		self.blue_basescore_checkbox_second = QCheckBox("成功抓取燃料矿", self)
		self.blue_basescore_checkbox_second.setGeometry(int(0.81*self.screen_width), int(0.34*self.screen_height),
				int(0.15*self.screen_width), int(0.03*self.screen_height))
		self.blue_basescore_checkbox_second.setStyleSheet("QCheckBox{font-size:"+str(int(0.018*self.screen_height))+"px; font-weight:bold; font-family:Microsoft YaHei; color:black;}")
		self.blue_basescore_checkbox_second.stateChanged.connect(self.BlueCheckboxSecond)

		self.blue_basescore_checkbox_third = QCheckBox("成功抓取晶体矿", self)
		self.blue_basescore_checkbox_third.setGeometry(int(0.81*self.screen_width), int(0.37*self.screen_height),
				int(0.15*self.screen_width), int(0.03*self.screen_height))
		self.blue_basescore_checkbox_third.setStyleSheet("QCheckBox{font-size:"+str(int(0.018*self.screen_height))+"px; font-weight:bold; font-family:Microsoft YaHei; color:black;}")
		self.blue_basescore_checkbox_third.stateChanged.connect(self.BlueCheckboxThird)

	#设置计时器函数
	def OneMinUpdateTime(self):
		self.one_min_heart_clock_number += 1
		if self.one_min_heart_clock_number <= 60:
			self.one_minute_count.setText("00:%02d" % (60 - self.one_min_heart_clock_number))
		else:
			self.one_minute_count.setText("00:00")
			self.one_min_heart_clock.stop()

	def FiveMinUpdateTime(self):
		self.five_min_heart_clock_number += 1
		if self.five_min_heart_clock_number <= 300:
			if self.red_flag == 0:
				self.red_time_count.setText("%02d:%02d" % (4 - self.MinuteNegativeToSixty(self.five_min_heart_clock_number), self.SecondNegativeToSixty(self.five_min_heart_clock_number)))
				self.red_state.setText("红队比赛中...")
			if self.blue_flag == 0:
				self.blue_time_count.setText("%02d:%02d" % (4 - self.MinuteNegativeToSixty(self.five_min_heart_clock_number), self.SecondNegativeToSixty(self.five_min_heart_clock_number)))
				self.blue_state.setText("蓝队比赛中...")
		else:
			self.red_time_count.setText("00:00")
			self.blue_time_count.setText("00:00")
			self.five_min_heart_clock.stop()

	def OneMinStart(self):
		self.one_min_heart_clock.start(1000)

	def FiveMinStart(self):
		self.five_min_heart_clock.start(1000)

	def RedStop(self):
		self.red_time_count.setText("%02d:%02d" % (4 - self.MinuteNegativeToSixty(self.five_min_heart_clock_number), self.SecondNegativeToSixty(self.five_min_heart_clock_number)))
		self.red_flag = 1
		self.red_state.setText("红队用时%02d分%02d秒" % (self.five_min_heart_clock_number // 60, self.five_min_heart_clock_number % 60))

	def BlueStop(self):
		self.blue_time_count.setText("%02d:%02d" % (4 - self.MinuteNegativeToSixty(self.five_min_heart_clock_number), self.SecondNegativeToSixty(self.five_min_heart_clock_number)))
		self.blue_flag = 1
		self.blue_state.setText("蓝队用时%02d分%02d秒" % (self.five_min_heart_clock_number // 60, self.five_min_heart_clock_number % 60))
	
	#设置复位函数
	def Reset(self):
		self.one_min_heart_clock.stop()
		self.one_min_heart_clock_number = 0
		self.one_minute_count.setText("01:00")

		self.five_min_heart_clock.stop()
		self.five_min_heart_clock_number = 0
		self.red_time_count.setText("05:00")
		self.blue_time_count.setText("05:00")

		self.red_flag = 0
		self.blue_flag = 0

		self.red_state.setText("红队准备中...")
		self.blue_state.setText("蓝队准备中...")

		self.vein_generation_label.setPixmap(QPixmap("./Source/Pic/VeinBackground.png"))
		self.store_generation_label.setPixmap(QPixmap("./Source/Pic/StoreBackground.png"))

	#设置贫矿、富矿和燃料矿的响应函数
	def RedScoreCount(self):
		temp_fuel_number = self.red_fuel_number
		if temp_fuel_number >= 2:
			temp_fuel_number = 2
		if temp_fuel_number * 2 <= self.red_bonanza_number:
			self.red_score_number = temp_fuel_number * 2 * 3
		else:
			if temp_fuel_number * 2 - self.red_bonanza_number - self.red_leanore_number <= 0:
				self.red_score_number = self.red_bonanza_number * 3 + (temp_fuel_number * 2 - self.red_bonanza_number)
			else:
				self.red_score_number = self.red_bonanza_number * 3 + self.red_leanore_number
		self.red_score.setText(str(self.red_score_number + self.red_score_extra_number))

	def RedBonanzaButtonCrease(self):
		if self.red_bonanza_number < 6:
			self.red_bonanza_number += 1
		self.red_bonanza_count.setText(str(self.red_bonanza_number))
		self.RedScoreCount()

	def RedBonanzaButtonDecrease(self):
		if self.red_bonanza_number > 0:
			self.red_bonanza_number -= 1
		self.red_bonanza_count.setText(str(self.red_bonanza_number))
		self.RedScoreCount()

	def RedLeanoreButtonCrease(self):
		if self.red_leanore_number < 9:
			self.red_leanore_number += 1
		self.red_leanore_count.setText(str(self.red_leanore_number))
		self.RedScoreCount()

	def RedLeanoreButtonDecrease(self):
		if self.red_leanore_number > 0:
			self.red_leanore_number -= 1
		self.red_leanore_count.setText(str(self.red_leanore_number))
		self.RedScoreCount()

	def RedFuelButtonCrease(self):
		if self.red_fuel_number < 4:
			self.red_fuel_number += 1
		self.red_fuel_count.setText(str(self.red_fuel_number))
		self.RedScoreCount()

	def RedFuelButtonDecrease(self):
		if self.red_fuel_number > 0:
			self.red_fuel_number -= 1
		self.red_fuel_count.setText(str(self.red_fuel_number))
		self.RedScoreCount()

	def BlueScoreCount(self):
		temp_fuel_number = self.blue_fuel_number
		if temp_fuel_number >= 2:
			temp_fuel_number = 2
		if temp_fuel_number * 2 <= self.blue_bonanza_number:
			self.blue_score_number = temp_fuel_number * 2 * 3
		else:
			if temp_fuel_number * 2 - self.blue_bonanza_number - self.blue_leanore_number <= 0:
				self.blue_score_number = self.blue_bonanza_number * 3 + (temp_fuel_number * 2 - self.blue_bonanza_number)
			else:
				self.blue_score_number = self.blue_bonanza_number * 3 + self.blue_leanore_number
		self.blue_score.setText(str(self.blue_score_number + self.blue_score_extra_number))

	def BlueBonanzaButtonCrease(self):
		if self.blue_bonanza_number < 6:
			self.blue_bonanza_number += 1
		self.blue_bonanza_count.setText(str(self.blue_bonanza_number))
		self.BlueScoreCount()
	
	def BlueBonanzaButtonDecrease(self):
		if self.blue_bonanza_number > 0:
			self.blue_bonanza_number -= 1
		self.blue_bonanza_count.setText(str(self.blue_bonanza_number))
		self.BlueScoreCount()

	def BlueLeanoreButtonCrease(self):
		if self.blue_leanore_number < 9:
			self.blue_leanore_number += 1
		self.blue_leanore_count.setText(str(self.blue_leanore_number))
		self.BlueScoreCount()
	
	def BlueLeanoreButtonDecrease(self):
		if self.blue_leanore_number > 0:
			self.blue_leanore_number -= 1
		self.blue_leanore_count.setText(str(self.blue_leanore_number))
		self.BlueScoreCount()

	def BlueFuelButtonCrease(self):
		if self.blue_fuel_number < 4:
			self.blue_fuel_number += 1
		self.blue_fuel_count.setText(str(self.blue_fuel_number))
		self.BlueScoreCount()

	def BlueFuelButtonDecrease(self):
		if self.blue_fuel_number > 0:
			self.blue_fuel_number -= 1
		self.blue_fuel_count.setText(str(self.blue_fuel_number))
		self.BlueScoreCount()

	#复选框响应函数
	def RedCheckboxFirst(self, state):
		if state == 2:
			self.red_score_extra_number += 1
			self.red_score.setText(str(self.red_score_number + self.red_score_extra_number))
		else:
			self.red_score_extra_number -= 1
			self.red_score.setText(str(self.red_score_number + self.red_score_extra_number))

	def RedCheckboxSecond(self, state):
		if state == 2:
			self.red_score_extra_number += 1
			self.red_score.setText(str(self.red_score_number + self.red_score_extra_number))
		else:
			self.red_score_extra_number -= 1
			self.red_score.setText(str(self.red_score_number + self.red_score_extra_number))

	def RedCheckboxThird(self, state):
		if state == 2:
			self.red_score_extra_number += 1
			self.red_score.setText(str(self.red_score_number + self.red_score_extra_number))
		else:
			self.red_score_extra_number -= 1
			self.red_score.setText(str(self.red_score_number + self.red_score_extra_number))

	def BlueCheckboxFirst(self, state):
		if state == 2:
			self.blue_score_extra_number += 1
			self.blue_score.setText(str(self.blue_score_number + self.blue_score_extra_number))
		else:
			self.blue_score_extra_number -= 1
			self.blue_score.setText(str(self.blue_score_number + self.blue_score_extra_number))

	def BlueCheckboxSecond(self, state):
		if state == 2:
			self.blue_score_extra_number += 1
			self.blue_score.setText(str(self.blue_score_number + self.blue_score_extra_number))
		else:
			self.blue_score_extra_number -= 1
			self.blue_score.setText(str(self.blue_score_number + self.blue_score_extra_number))

	def BlueCheckboxThird(self, state):
		if state == 2:
			self.blue_score_extra_number += 1
			self.blue_score.setText(str(self.blue_score_number + self.blue_score_extra_number))
		else:
			self.blue_score_extra_number -= 1
			self.blue_score.setText(str(self.blue_score_number + self.blue_score_extra_number))

	#矿脉随机生成函数
	def VeinGeneration(self):
		vein_generation = cv2.imread('./Source/Pic/VeinBackground.png')
		vein_list_first, vein_list_second, vein_list_third, fuel_list_first, fuel_list_second = self.RandomVein()
		for i in range(0, 5):
			if vein_list_first[i] == 1:
				cv2.rectangle(vein_generation, self.first_vein_loaction[i][0], self.first_vein_loaction[i][1], self.yellow_color, -1)
			else:
				cv2.rectangle(vein_generation, self.first_vein_loaction[i][0], self.first_vein_loaction[i][1], self.blue_color, -1)

			if vein_list_second[i] == 1:
				cv2.rectangle(vein_generation, self.second_vein_location[i][0], self.second_vein_location[i][1], self.yellow_color, -1)
			else:
				cv2.rectangle(vein_generation, self.second_vein_location[i][0], self.second_vein_location[i][1], self.blue_color, -1)

			if vein_list_third[i] == 1:
				cv2.rectangle(vein_generation, self.third_vein_location[i][0], self.third_vein_location[i][1], self.yellow_color, -1)
			else:
				cv2.rectangle(vein_generation, self.third_vein_location[i][0], self.third_vein_location[i][1], self.blue_color, -1)

		for i in range(0, 3):
			if fuel_list_first[i] == 1:
				cv2.rectangle(vein_generation, self.first_fuel_location[i][0], self.first_fuel_location[i][1], self.purple_color, -1)
			if fuel_list_second[i] == 1:
				cv2.rectangle(vein_generation, self.second_fuel_location[i][0], self.second_fuel_location[i][1], self.purple_color, -1)

		vein_generation = cv2.cvtColor(vein_generation, cv2.COLOR_BGR2RGB)
		height, width, channel = vein_generation.shape
		q_image = QImage(vein_generation[:], width, height, width*3, QImage.Format_RGB888)
		self.vein_generation_label.setPixmap(QPixmap(q_image))

	def RandomVein(self):
		vein_list_first = [0] * 5
		vein_list_second = [0] * 5
		vein_list_third = [0] * 5
		fuel_list_first = [0] * 3
		fuel_list_second = [0] * 3

		first, second = random.sample(range(0, 5), 2)
		vein_list_first[first] = 1
		vein_list_first[second] = 1
		
		first, second = random.sample(range(0, 5), 2)
		vein_list_second[first] = 1
		vein_list_second[second] = 1

		first, second = random.sample(range(0, 5), 2)
		vein_list_third[first] = 1
		vein_list_third[second] = 1

		first, second = random.sample(range(0, 3), 2)
		fuel_list_first[first] = 1
		fuel_list_first[second] = 1

		first, second = random.sample(range(0, 3), 2)
		fuel_list_second[first] = 1
		fuel_list_second[second] = 1
		return vein_list_first, vein_list_second, vein_list_third, fuel_list_first, fuel_list_second

	def StoreGeneration(self):
		store_generation = cv2.imread('./Source/Pic/StoreBackground.png')
		store_list_first, store_list_second = self.RandomStore()
		for i in range(0, 4):
			if store_list_first[i] == 1:
				cv2.rectangle(store_generation, self.first_store_location[i][0], self.first_store_location[i][1], self.store_color, -1)
			if store_list_second[i] == 1:
				cv2.rectangle(store_generation, self.second_store_location[i][0], self.second_store_location[i][1], self.store_color, -1)
		store_generation = cv2.cvtColor(store_generation, cv2.COLOR_BGR2RGB)
		height, width, channel = store_generation.shape
		q_image = QImage(store_generation[:], width, height, width*3, QImage.Format_RGB888)
		self.store_generation_label.setPixmap(QPixmap(q_image))
		
	def RandomStore(self):
		store_first = [0] * 4
		store_second = [0] * 4
		first = random.sample(range(0, 2), 1)
		second = random.sample(range(0, 2), 1)
		store_first[first[0] * 2] = 1
		store_first[first[0] * 2 + 1] = 1
		store_second[second[0] * 2] = 1
		store_second[second[0] * 2 + 1] = 1
		return store_first, store_second
	
	def SetVeinAndStore(self):
		self.VeinGeneration()
		self.StoreGeneration()
	
if __name__=='__main__':
	random.seed(int(time.time()))
	app=QApplication(sys.argv)
	hmi_ws=MainCode()
	hmi_ws.show()
	sys.exit(app.exec_())
