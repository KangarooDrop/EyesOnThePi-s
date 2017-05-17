#Importing necessary directories
from gpiozero import PWMOutputDevice, InputDevice, OutputDevice
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import thread
from time import sleep, time

#trig = input for ultrasonic distance sensors
trig = [OutputDevice(4), OutputDevice(27), OutputDevice(8)]
#echo = output to ultrasonic distance sensors
echo = [InputDevice(17), InputDevice(22),  InputDevice(7)]
#Vibration motor outputs
motor = [PWMOutputDevice(21), PWMOutputDevice(20), PWMOutputDevice(19), PWMOutputDevice(13)]

#Initialization of MCP3008 for IR distance sensor
CLK = 18
MISO = 23
MOSI = 24
CS = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

sleep(1)

#Turns on the ultrasonic distance sensors for 0.00001 seconds 
def send_pulse(index):
	trig[index].on()
	sleep(0.00001)
	trig[index].off()

#Calclates the difference in time between sensor activation for a maximum of
#   0.05 seconds (17.15m at 20*C)
def get_duration(index):
	send_pulse(index)
	start_time = -1
	act_start_time = -1
	while echo[index].is_active == False:
		start_time = time()
		if act_start_time == -1:
			act_start_time = time()
		elif time() - act_start_time > 0.05:
			break
	stop_time = -1
	while echo[index].is_active == True:
		stop_time = time()
		if act_start_time == -1:
			act_start_time = time()
		elif time() - act_start_time > 0.05:
			break
	if stop_time == -1:
		return start_time
	elif start_time == -1:
		return stop_time
	return (stop_time - start_time)


#Calculates the distance to an object based on the time duration at 20*C
def calc_dist(time_dur):
	air = 343
	distance = air * time_dur / 2
	return distance

#Sets the value between 0 and 1 and curves it based on the USDS distance
def calc_value(distance):
	max_dist = 4

	value = 1-(distance/max_dist)
	slope = 1.5
	if value > 0:
		value = pow(value, slope)
	if value >= 0.999:
		return 0.999
	elif value < 0:
		return 0
	return value

# Bounded value between 0 and 1 of the distance to an object in a straight
#   line to the IR senosor (getting the digital output of the ADC translated
#   from the IR sensor's analog output) 10 times and averaging them
def ir_val():
	num = 10
	max_val = 1023.0
	slope = 3.0/8
	a = []

	for i in range(num):
		adc_val =  mcp.read_adc(7)
		val = adc_val / max_val
		val = 0 if val<0 else 1 if val>1 else val
		val = pow(val, slope)
		a.append(val)
	return sum(a)/num

#Calculates the distance
def ir_dist():
	max_dist = 1.5
	return ir_val() * max_dist

# Tests the functionality of the ultrasonic by 
#   outputting to the vibration motors
def test_sensors ():
	for i in range(len(trig)):
		distance = calc_dist(get_duration(i))
		sleep(0.05)
		motor[i].value = calc_value (distance)

def set_usds(index):
	while True:
		distance = calc_dist(get_duration(index))
		sleep(0.05)
		motor[index].value = calc_value(distance)

def set_ir():
	while True:
		val = ir_val()
		print (val)
		motor[3].value = val
		sleep(0.005)
		
def run():
	print ("Starting The Oven")
	
	print ("Starting IR distance sensor")
	thread.start_new_thread(set_ir, ())
	print ("Starting Ultrasonic distance sensors")
	while True:
		test_sensors()
def test_motors ():
	for i in range(len(motor)):
		for j in range (100):
			motor[i].value = j/100.0
			sleep(0.01)
		motor[i].value = 0

run()

while True:
	test_motors()
