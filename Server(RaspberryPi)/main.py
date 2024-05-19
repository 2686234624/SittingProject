import time
import Server
import Adafruit_PCA9685
 
def set_servo_angle(channel, angle):#输入角度转换成12^精度的数值
    date=int(4096*((angle*11)+500)/20000)#进行四舍五入运算 date=int(4096*((angle*11)+500)/(20000)+0.5)    
    pwm.set_pwm(channel, 0, date)

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

if __name__ == '__main__':
    print("等待连接")
    client,address = Server.mySocket.accept()
    print("新连接")
    print("IP is %s" % address[0])
    print("port is %d\n" % address[1])
    
    beangle = 100 #每个人的初始角度不同，建议先自己测试好角度
    beangle0 = 10

	#舵机插的通道口
    channel1 = 0 #上下
    channel2 = 1 #左右
	
	#变化幅度（这个越大，舵机动的幅度就越大）
    angleFreq = 1
	#超出屏幕范围（这个调大后，脸部离视频边界检测更灵敏）
    changeFreq = 25
 	
    #初始化角度
    set_servo_angle(channel1,beangle)
    set_servo_angle(channel2,beangle0)
    
    while True:
        msg = client.recv(1024)
        msg = msg.decode("utf-8")
        if msg != "":
            mess = msg.split(' ')
            
            x0 = int(mess[0])#左上角x
            y0 = int(mess[1])#左上角y
            x1 = int(mess[2])#右下角x
            y1 = int(mess[3])#右下角y

			#超出屏幕外
            if x0 < changeFreq:
                beangle += angleFreq
                if beangle >= 180:
                    beangle = 180
                set_servo_angle(channel1,beangle)
            
            if y0 < changeFreq:
                beangle0 += angleFreq
                if beangle0 >= 180:
                    beangle0 = 180
                set_servo_angle(channel2,beangle0)

            if x1 > 640 - changeFreq: #窗口宽为640
                beangle -= angleFreq
                if beangle <= 30:
                    beangle = 30
                set_servo_angle(channel1,beangle)
            
            if y1 > 480 - changeFreq: #窗口高为480
                beangle0 -= angleFreq
                if beangle0 <= 30:
                    beangle0 = 30
                set_servo_angle(channel2,beangle0)
