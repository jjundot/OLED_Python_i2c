#!/usr/bin/env python
# -*- coding: utf-8 -*-


import smbus
import time
from ascii_ls import *


OLED_ADDRESS = 0x3c
OLED_COMMAND = 0x00
OLED_DATA = 0x40

bus = smbus.SMBus(1)

#Rutina display

def init_oled():
    time.sleep(0.1)
    init_l1=[0xae,0x00,0x10,0x40,0x81,0xcf,0xa1,0xc8,0xa6,0xa0,0x3f,0xd3,\
             0x00,0xd5,0x80,0xd9,0xf1,0xda,0x12,0xdb,0x40,0x20,0x02,0x8d,\
             0x14,0xa4,0xa6,0xaf,0x00]
    init_l2=[0xAE,0x20,0x10,0xb0,0xc8,0x00,0x10,0x40,0x81,0xff,0xa1,0xa6,\
             0xa8,0x3F,0xa4,0xd3,0x00,0xd5,0xf0,0xd9,0x22,0xda,0x12,0xdb,\
             0x20,0x8d,0x14,0xaf]
    for i in init_l2:
        send_command(i)
        time.sleep(0.05)
    set_xy(0,0)

def clear_oled():
    time.sleep(0.1)
    for i in range(8):
        send_command(0xb0+i)
        send_command(0x01)
        send_command(0x10)
        for j in range(128):
            send_char(0x00)


def send_char(data):
    bus.write_byte_data(OLED_ADDRESS, OLED_DATA, data)

def send_command(command):
    bus.write_byte_data(OLED_ADDRESS, OLED_COMMAND, command)

def set_xy(x,y):
    send_command(0xb0+y)
    send_command(((x&0xf0)>>4)|0x10)
    send_command((x&0x0f)|0x01)

def send_string_8x16(x,y,string):
    time.sleep(0.1)
    for i in string:
        c=ord(i)-32
        if(x>120):
             x=0
             y+=2
        set_xy(x,y)
        for j in range(8):
            send_char(ASCII8X16[c*16+j])
        set_xy(x,y+1)
        for k in range(8):
             send_char(ASCII8X16[c*16+k+8])
        x+=8

def send_string_6x8(x,y,string):
    time.sleep(0.1)
    for i in string:
        c=ord(i)-32
        if(x>126):
            x=6
            y+=1
        set_xy(x,y)
        for j in range(6):
            send_char(ASCII6x8[c][j])
        x+=6
    return
def oled_on():
    send_command(0x8d) # set 
    send_command(0x14) # enable 
    send_command(0xaf) # 

def oled_off():
    send_command(0x8d)
    send_command(0x10)
    send_command(0xae)

def init_help(i):
    help=['display off','Set Memory Addressing Mode',\
          '00,Horizontal Addressing Mode;01,Vertical \
           Addressing Mode;10,Page Addressing Mode (R\
           ESET,);11,Invalid,Set Page Start Address f\
           or Page Addressing Mode,0-7','Set COM Outp\
           ut ScanDirection','set low column address'\
           ,'set high column address','set start line\
            address','set contrast control register',\
           'Brightness:0x00~0xff','set segment re-map\
           0 to 127','set normal display','set multip\
           lex ratio(1 to 64,)',' ','0xa4,Outputfoll\
           ows RAM content;0xa5,Output ignores RAM co\
           ntent','set display offset','not offset','\
           set display clock divide ratio/oscillator \
           frequency','set display clock divide ratio\
           /oscillator frequency','-c','set pre-charg\
           e period',' ','set com pins hardware confi\
           guration',' ','set vcomh','0x20,0.77xVcc',\
           'set DC-DC enable',' ','turn on oled panel']
    i-=1
    if i <=27 and i >=0:
        print help[i]

if __name__ == '__main__':

    init_oled()
    w = 0
    while True:
        clear_oled()
        print w
        send_string_8x16(0,w,'Hello, jjun!')
        w += 2
        if w > 6:
            w=0
        time.sleep(2)
    # init_oled()
    # bus.close()
    clear_oled()
    #send_string_8x16(0,2,'12345678901234567')
    send_string_6x8(0,0,'1234567890123456789012345')
    # oled_off()
    # time.sleep(8)
    # oled_on()
    bus.close()
