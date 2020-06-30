#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

class Ultrasonic(object):
    
    def __init__(self):
        self.dist=0.0
    
    # 距離を読む関数
    def getDistance(self):
        # 必要なライブラリのインポート・設定
        import RPi.GPIO as GPIO

        # 使用するピンの設定
        GPIO.setmode(GPIO.BCM)
        TRIG = 24 # GPIO02(Pin3)
        ECHO = 23 # GPIO03(Pin5)

        # ピンのモードをそれぞれ出力用と入力用に設定
        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)
        GPIO.output(TRIG, GPIO.LOW)

        # TRIG に短いパルスを送る
        GPIO.output(TRIG, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(TRIG, GPIO.LOW)

        # ECHO ピンがHIGHになるのを待つ
        signaloff = time.time()
        while GPIO.input(ECHO) == GPIO.LOW:
            signaloff = time.time()

        # ECHO ピンがLOWになるのを待つ
        signalon = signaloff
        while time.time() < signaloff + 0.1:
            if GPIO.input(ECHO) == GPIO.LOW:
                signalon = time.time()
                break

        # GPIO を初期化しておく
        GPIO.cleanup()

        # 時刻の差から、物体までの往復の時間を求め、距離を計算する
        timepassed = signalon - signaloff
        distance = timepassed * 17000

        # 500cm 以上の場合はノイズと判断する
        #if distance <= 500:
            #return distance
        self.dist=distance
        