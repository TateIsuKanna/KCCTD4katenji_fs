import RPi.GPIO as GPIO
from tkinter import *
import datetime
import pygame.mixer
import time

stopwatch_signal_channel=37
sound_signal_channel=38

is_timer_enable=False#本当は使わずに済ませたい

pygame.mixer.init()
pygame.mixer.music.load("/home/pi/フラッシュザウルス.mp3")

def stopwatch_signal_callback(channel):
	if GPIO.input(channel):
		start_stopwatch()
	else:
		stop_stopwatch()

def start_stopwatch():
	global start_time
	start_time=datetime.datetime.now()
	global is_timer_enable
	is_timer_enable=True
	update_stopwatch_callback()

def stop_stopwatch():
	global is_timer_enable
	is_timer_enable=False

def update_stopwatch_callback():
	stopwatch_label_text.set(datetime.datetime.now()-start_time)
	if is_timer_enable:
		root.after(10,update_stopwatch_callback)

def sound_signal_callback(channel):
	pygame.mixer.music.play()
	time.sleep(30)
	pygame.mixer.music.stop()


root = Tk()
root.attributes("-fullscreen", True)
root.config(cursor="none")
stopwatch_label_text = StringVar()
stopwatch_label = Label(root,textvariable=stopwatch_label_text,font = ("",40))
stopwatch_label.pack(expand=1)

GPIO.setmode(GPIO.BOARD)
GPIO.setup([stopwatch_signal_channel,sound_signal_channel], GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(stopwatch_signal_channel, GPIO.BOTH, callback=stopwatch_signal_callback) 
GPIO.add_event_detect(sound_signal_channel, GPIO.RISING, callback=sound_signal_callback) 

root.mainloop()

GPIO.cleanup()
