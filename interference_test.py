

from gpiozero import InputDevice, OutputDevice, PWMOutputDevice
from time import sleep, time

trig = [OutputDevice(4), OutputDevice(4), OutputDevice(4), OutputDevice(4), OutputDevice(4)]
echo = [InputDevice(17), InputDevice(17), InputDevice(17), InputDevice(17), InputDevice(17)]
motor = [PWMOutputDevice(20), PWMOutputDevice(20), PWMOutputDevice(20), PWMOutputDevice(20)]
sleep (1)

def pulse(index):
	trig[index].on()
	sleep(0.00001)
	trig[index].off()

def calc_distance(duration):
	speed = 343
	return (speed * duration / 2)
	
def calc_vibration(distance):
	max_dist = 3
	min_dist = 0.01
	val = 1-((distance - min_dist) / (max_dist - min_dist)
	return val
	
def get_multi_pulse():
	start = [[-1 for x in range(len(trig))] for y in range(len(trig))]
	stop  = [[-1 for x in range(len(trig))] for y in range(len(trig))
	max_time = 0.05
	for i in range(len(trig)):
		pulse(i)
		r_start = time()
		while end == False:
			end = True
			for j in len(echo):
				if echo[j].is_active == False and start_time[i][j] = -1:
					r_start = time()
				if echo[j].is_active == False:
					start_time[i][j] = time()
				else:
					stop_time[i][j] = time()
				if stop_time[i][j] == -1 and echo[j].is_active == False and time() - r_start < max_time
					end = False
	for i in range(len(trig)):
		print (str(i) + ".   ", end='') 
		for j in range(len(echo)):
			print ("[" + str(calc_dist(stop_time[i][j] - start_time[i][j])) + "] ", end='')
		print()


def main ():
	sensor_num = 5

	dists = [[0 for x in range(sensor_num)] for y in range(sensor_num)]
	start_times = [[0 for x in range(sensor_num)] for y in range(sensor_num)]
	stop_times = [[0 for x in range(sensor_num)] for y in range(sensor_num)]
	calc = [[False for x in range(sensor_num)] for y in range(sensor_num)]
	recieved_pulse = [[True for x in range(sensor_num)]
	
	while True:
		for i in range(sensor_num):
			bool send_pulse = True
			for x in range(sensor_num):
				if (recieved_pulse[x] == False):
					send_pulse = False
			if send_pulse == False:
				for j in range(sensor_num):
					if calc[i][j] == True and echo[j].is_active == False:
						dists[i][j] = calc_distance(stop_time[i][j] - start_time[i][j])
						recieved_pulse[j] = True
					if echo[j].is_active == False:
						start_times[i][j] = time()
						calc[i][j] = False
					else:
						stop_time[i][j] = time()
						calc[i][j] = True
			else:
				trig[i].on()
				sleep(0.00001)
				trig[i].off()
				
while True:
	get_multi_pulse()