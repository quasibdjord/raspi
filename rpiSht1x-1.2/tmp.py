from sht1x.Sht1x import Sht1x as SHT1x
import RPi.GPIO as GPIO
#GPIO.setmode(GPIO.BOARD)
dataPin = 37
clkPin = 13
GPIO.setwarnings(False) 
#GPIO.setmode(GPIO.BOARD)
#SHT1x.GPIO.setmode(GPIO.BCM)
sht1x = SHT1x(dataPin, clkPin,SHT1x.GPIO_BOARD)

temperature = sht1x.read_temperature_C()
humidity = sht1x.read_humidity()
dewPoint = sht1x.calculate_dew_point(temperature, humidity)
#print temperature
print("Temperature: {} Humidity: {} Dew Point: {}".format(temperature, humidity, dewPoint))

