import time
import sys
import os
import pprint
import uuid
from uuid import getnode as get_mac
import subprocess
import base64
import json
import urllib3
from os.path import join, dirname
import picamera

#import pygame, sys
#import pygame.camera
#from pygame.locals import *
#pygame.init()
#pygame.camera.init()


import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
urllib3.disable_warnings()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) #Intruder Data PIN
GPIO.setup(12,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) #Door Open Data PIN
GPIO.setup(15,GPIO.IN,pull_up_down=GPIO.PUD_UP) #Smoke Digital Data PIN
GPIO.setup(22,GPIO.OUT,pull_up_down=GPIO.PUD_DOWN)# Alarm Data PIN
GPIO.setup(31,GPIO.OUT,pull_up_down=GPIO.PUD_DOWN) # RED LED PIN
GPIO.setup(33,GPIO.OUT,pull_up_down=GPIO.PUD_DOWN) # GREEN LED PIN
GPIO.setup(32,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # Noise Data PIN
GPIO.setup(35,GPIO.IN,pull_up_down=GPIO.PUD_UP) #Flooding Data PIN

GPIO.setup(38,GPIO.IN) #flooding Analog Data PIN
GPIO.setup(37,GPIO.IN) #Smoke Analog Data PIN



ls='OFF'


try:
    import ibmiotf.application
    import ibmiotf.device
except ImportError:
    # This part is only required to run the sample from within the samples
    # directory when the module itself is not installed.
    #
    # If you have the module installed, just use "import ibmiotf.application" & "import ibmiotf.device"
    import os
    import inspect
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../src")))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)
    import ibmiotf.application
    import ibmiotf.device

def generateToken():
	data=json.dumps({"auth": { "identity": {"methods": ["password"],"password": { "user": {"id": "edc0406595f44da3a4615f6ae996facf","password": "Vo!1h1uFh~xZxYNd"}}}}})
	http = urllib3.PoolManager()
	headers = urllib3.util.make_headers('Content-Type', 'application/json')
	res = http.request('POST','https://identity.open.softlayer.com/v3/auth/tokens',headers={'Content-Type': 'application/json'}, body=data)
#	print (res.getheader('X-Subject-Token'))
	token = res.getheader('X-Subject-Token')
	with open('/home/pi/SafeHome/Token/Token.txt', 'w') as token_data:
		token_data.write(token)
		token_data.close()
	print("New Token Generated")	
	return token
	

def formatURL(fileName):
	baseURL = 'https://dal.objectstorage.open.softlayer.com/v1'
	containerName = 'SafeHomePhoto'
	objectName = fileName
	projectId = 'a9d5aed2ad114ad59cbc862da2a4d066'
	finalURL = baseURL + '/'+'AUTH_'+projectId+'/'+containerName+'/'+objectName
	return finalURL
	
	
def uploadFile(filePath,fileName):
	tryAgain = False
	token=''
	try:
		with open('/home/pi/SafeHome/Token/Token.txt', 'r') as token_file:
			token=token_file.read()
			print("Token read from the file is: ", token)			
			token_file.close()
	except IOError:
		token = generateToken()
	with open(filePath, 'rb') as image_file:
		storageURL = formatURL(fileName)
		http = urllib3.PoolManager()
		res = http.request('PUT',storageURL,headers={'multipart-manifest':'put','X-Auth-Token':token}, body=image_file)		
		if res.status == 401:
			print("Could not upload photo. Token expired. Generating new token")
			token = generateToken()
			tryAgain=True
		else:
			print("2 - Photo uploaded at",storageURL)
		image_file.close()
	if tryAgain:	
		with open(filePath, 'rb') as image_file:	
			http = urllib3.PoolManager()
			res = http.request('PUT',storageURL,headers={'multipart-manifest':'put','X-Auth-Token':token}, body=image_file)
			print("1 - Photo uploaded at",storageURL)
			image_file.close()
	return storageURL
	
def takePhoto():
	#cam = pygame.camera.Camera("/dev/video0",(320,240))
	#cam.start()
	#setup window
	#windowSurfaceObj = pygame.display.set_mode((320,240),1,16)
	#pygame.display.set_caption('Camera')

	#take a picture
	#image = cam.get_image()
	#cam.stop()

	#display the picture
	#catSurfaceObj = image
	#windowSurfaceObj.blit(catSurfaceObj,(0,0))
	#pygame.display.update()

	#save picture
	#pygame.image.save(image,'picture.jpg')

	#print "Taking snapshot." 

	#print "Acquiring image file...." 
	import datetime 
	todays_date = datetime.datetime.today() 
	image_name = todays_date.strftime('%m-%d-%y-%H%M') 
	image_path = '/home/pi/SafeHome/Photos/' + image_name + '.jpg'

#	command = 'sudo fswebcam -r 320x240 -d /dev/video0 -q '+image_path
#	grab_cam = subprocess.Popen(command, shell=True) #replace as necessary
#	grab_cam.wait()
#	photoURL = uploadFile(image_path,image_name)
#	return photoURL

	with picamera.PiCamera() as camera:       
		camera.capture(image_path)
	photoURL = uploadFile(image_path,image_name)
	return photoURL

	
def sendPicture():
	print("Sending Picture")		
	
	
def myAppEventCallback(event):
	print("Received live data from %s (%s) sent at %s: hello=%s x=%s" % (event.deviceId, event.deviceType, event.timestamp.strftime("%H:%M:%S"), data['hello'], data['x']))

def myCommandCallback(cmd):
	stopAlarm=0
	print("Command received: %s" % cmd.data)
	if cmd.command == "status":
		print("Sending the status of the devices to Mobile")
		#intruder=GPIO.input(11)
		#doorOpen=GPIO.input(12)
		#noise=GPIO.input(32)
		#gasLeak=GPIO.input(22)
		#earthquake=GPIO.input(24)
		todays_date = datetime.datetime.today().strftime('%m-%d-%y-%H:%M')  
		data = { 'Gateway_Status': 'Active', 'date':todays_date}
		print("Gateway Status is active")
		deviceCli.publishEvent("status", "json", data)
		
			
	elif cmd.command == "photo":
		import datetime 
		print("Taking Photo")
		photoURL = takePhoto()
		with open('/home/pi/SafeHome/Token/Token.txt', 'r') as token_file:
			token=token_file.read();
		todays_date = datetime.datetime.today().strftime('%m-%d-%y-%H:%M')	
		data = { 'Sensor_Location': 'Living Room', 'Sensor_Type': 'Camera', 'Sensor_Id': 'DEV0', 'Sensor_State':'Active', 'Sensor_Event':'1', 'date':todays_date,'photo_url':photoURL,'token':token}
		deviceCli.publishEvent("status", "json", data)

	elif cmd.command == "startalarm":
		print("Starting Alarm")
		GPIO.output(22,1)
	
	elif cmd.command == "stopalarm":
		print("Stopping Alarm")
		GPIO.output(22,0)
	
		
#####################################
#FILL IN THESE DETAILS
#####################################     
organization = "ORG_NAME"
deviceType = "DEVICE_TYPE"
deviceId = "DEVICE_ID"
appId = str(uuid.uuid4())
authMethod = "token"
authToken = "AUTH_TOKEN"

# Initialize the device client.
try:
    deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
    deviceCli = ibmiotf.device.Client(deviceOptions)
except Exception as e:
	print(str(e))
	GPIO.output(31,1)
	GPIO.output(33,0)    
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
try:
	deviceCli.connect()
	GPIO.output(31,0)
	GPIO.output(33,1)
except ibmiotf.ConfigurationException as e:
	print(str(e))
	GPIO.output(31,1)
	GPIO.output(33,0)
	sys.exit()
except ibmiotf.UnsupportedAuthenticationMethod as e:
	print(str(e))
	GPIO.output(31,1)
	GPIO.output(33,0)
	sys.exit()
except ibmiotf.ConnectionException as e:
	print(str(e))
	GPIO.output(31,1)
	GPIO.output(33,0)
	sys.exit()

deviceCli.commandCallback = myCommandCallback

#x=0
intruder = 0
previousState = 0

while(1):
	
	previousState = intruder	
	intruder=GPIO.input(11)		
	if intruder == 1 and previousState == 0:		
		import datetime 
		todays_date = datetime.datetime.today().strftime('%m-%d-%y-%H:%M')		
		print("INTRUDER ALERT")
		photoURL = takePhoto()
		with open('/home/pi/SafeHome/Token/Token.txt', 'r') as token_file:
			token=token_file.read();
		data = { 'Sensor_Location': 'Bed Room', 'Sensor_Type': 'Intruder', 'Sensor_Id': '11', 'Sensor_State':'Active', 'Sensor_Event':'1', 'date':todays_date,'photo_url':photoURL,'token':token}
		deviceCli.publishEvent("status","json", data)
		

	doorOpen=GPIO.input(12)	
	if doorOpen == 1:	
		import datetime 
		todays_date = datetime.datetime.today().strftime('%m-%d-%y-%H:%M')  
		print("doorOpen ALERT")
		photoURL = takePhoto()
		with open('/home/pi/SafeHome/Token/Token.txt', 'r') as token_file:
			token=token_file.read();
		data = { 'Sensor_Location': 'Living Room', 'Sensor_Type': 'DoorOpen', 'Sensor_Id': '12', 'Sensor_State':'Active', 'Sensor_Event':'1', 'date':todays_date,'photo_url':photoURL,'token':token}
		deviceCli.publishEvent("status", "json", data)
		doorOpen=0
		time.sleep(3)	
		
	noise=GPIO.input(32)	
	if noise == 0:	
		import datetime 
		todays_date = datetime.datetime.today().strftime('%m-%d-%y-%H:%M')  
		data = { 'Sensor_Location': 'Living Room', 'Sensor_Type': 'Sound', 'Sensor_Id': '32', 'Sensor_State':'Active', 'Sensor_Event':'1', 'date':todays_date,'photo_url':' ','token':' '}
		print("SOUND ALERT")
		deviceCli.publishEvent("status", "json", data)
		noise=1
		time.sleep(3)
		

	smokeDigital=GPIO.input(15)	
	if smokeDigital == 1:	
		import datetime 
		todays_date = datetime.datetime.today().strftime('%m-%d-%y-%H:%M')  
		data = { 'Sensor_Location': 'Kitchen', 'Sensor_Type': 'Smoke', 'Sensor_Id': '15', 'Sensor_State':'Active', 'Sensor_Event':'1', 'date':todays_date,'photo_url':' ','token':' '}
		print("SMOKE ALERT")
		deviceCli.publishEvent("status", "json", data)
		smokeDigital=0
		time.sleep(3)
		
		
	floodDigital=GPIO.input(35)	
	if floodDigital ==0:	
		import datetime 
		todays_date = datetime.datetime.today().strftime('%m-%d-%y-%H:%M')  
		data = { 'Sensor_Location': 'Kitchen', 'Sensor_Type': 'Flood', 'Sensor_Id': '35', 'Sensor_State':'Active', 'Sensor_Event':'1', 'date':todays_date,'photo_url':' ','token':' '}
		print("FLOODING ALERT")
		deviceCli.publishEvent("status", "json", data)
		floodDigital=1
		time.sleep(3)
		
# Disconnect the device and application from the cloud
deviceCli.disconnect()
#appCli.disconnect()
