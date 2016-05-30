# Bluemix-IOT-Safehome
It is a complete workable safe home solution that keeps your home safe and looks after it while you are away. Your home informs you about any event that needs your attention as soon as the event happens (Gas leak, flooding, fire, increase in room temperature, intruder presence, opening of the front door, and many more such critical and no so critical cases). The application not only help your home communicate to you, it also allows you to communicate back to your home. For example if you want to trigger some alarm after verifying a photo (that gets sent to you automatically when the event happens), you can do that.

Find below the overall solution diagram.

![ScreenShot](/images/SafeHome-Overview.png)

#How to Build the Application

#Step 1

You need a list of elements to build this solution. Find below the Bill of Material for this project.

|Sl No    | Partn Name       |   Part Type   |Part Description                   |	URL                          | Quantity |
|:-------:|:----------------:|:-------------:|:---------------------------------:|:-----------------------------:|:--------:|
|1	|Raspberry Pi 2 Model B	|Raspberry Pi	|Raspberry Pi 2 Model B 1GB -The Complete Kit        | http://www.amazon.in/gp/product/B00T2U7R7I?psc=1&redirect=true&ref_=oh_aui_detailpage_o08_s00| 1   |
|2	|Micro SD Card 	|Memory	|Samsung Evo+ 32GB Class 10 micro SDHC Card Upto 80 Mbps speed (With adapter)|	http://www.amazon.in/Samsung-Class-micro-speed-adapter/dp/B00WR4IJBE/ref=sr_1_2?s=electronics&ie=UTF8&qid=1457519043&sr=1-2&keywords=micro+sd+memory+card |1   |
|3	|Camera	|Camera	|Raspberry Pi Camera Board | http://www.amazon.in/gp/product/B00L1FOIIS?psc=1&redirect=true&ref_=ox_sc_act_title_1&smid=A1NDZY44BCNIQJ | 1   |
|4	|IR Sensor	|Sensor	 |ELEMENTZ IR INFRARED PROXIMITY / OBSTACLE DETECTOR SENSOR MODULE   |	http://www.amazon.in/gp/product/B00MBXTA0A?psc=1&redirect=true&ref_=oh_aui_detailpage_o08_s00   |1   |
|5	|Rainwater Sensor	|Sensor	 |ARDUINO COMPATIBLE Rain Sensor Rainwater Module Rain Detection Module 3.3V-5V BY REES52   |	http://www.amazon.in/gp/product/B018GNR032?psc=1&redirect=true&ref_=od_aui_detailpages00   | 1   |
|6	|Gas Sensor	|Sensor   | VEEROBOT Smoke, Gas, LPG, Butane, Hydrogen, Gas Sensor Detector Module (MQ-2)   |	http://www.amazon.in/gp/product/B01307SNHG?psc=1&redirect=true&ref_=oh_aui_detailpage_o03_s00   | 1   |
|7	|Sound Sensor	|Sensor	|Sound Detection sensor Module / Intelligent Vehicle Microphone Arduino smart car |	http://www.amazon.in/gp/product/8385100644?psc=1&redirect=true&ref_=oh_aui_detailpage_o01_s00 | 1  |
|8	|Motion Sensor	| Sensor	| D Sun Hc-Sr501 Pyroelectric Infrared Pir Motion Sensor Detector Module|    http://www.amazon.in/gp/product/B007XQRKD4?psc=1&redirect=true&ref_=oh_aui_detailpage_o06_s00   | 1   |
|9	|Wireless Adapter	|Wireless Adapter(optional)	 | TP-Link TL-WN823N 300Mbps Mini Wireless N USB Adapter (Black) |	http://www.amazon.in/gp/product/B0088TKTY2?psc=1&redirect=true&ref_=oh_aui_detailpage_o00_s00   |1   |
|10	   |Wires	  |Connecting Wires	| Jumper Wire male to female(40 Pcs)   |	http://www.amazon.in/gp/product/B00SJHYN4K?psc=1&redirect=true&ref_=oh_aui_detailpage_o05_s00   |1 Bunch   |
|11	 | Wires	| Connecting Wires	 |Jumper Wire Female to Female (40 Pcs)   | http://www.amazon.in/Jumper-Wire-male-female-Pcs/dp/B00TZWORK8/ref=pd_sim_23_2?ie=UTF8&dpID=51RUa6UYg6L&dpSrc=sims&preST=_AC_UL160_SR160%2C160_&refRID=1N4NF5AAM0MZCAMAENH4   |1 Bunch   |
|12	  |Wires	 |Connecting Wires	 |Jumper Wire male to male(40 Pcs)   | 	http://www.amazon.in/Jumper-Wire-Female-40-Pcs/dp/B00SJI8SZ4/ref=pd_sim_23_3?ie=UTF8&dpID=51LKB7Wg%2BZL&dpSrc=sims&preST=_AC_UL160_SR160%2C160_&refRID=1N4NF5AAM0MZCAMAENH4   | 1 Bunch   |
|13	|LED	|LED	|Led 3Mm Three Color	|http://www.amazon.in/gp/product/B00WNYMLR6?psc=1&redirect=true&ref_=oh_aui_detailpage_o03_s00|1 Bunch    |
|14	| Buzzers  |Buzzers	  |Pizo Buzzer (5 Pcs)   |http://www.amazon.in/gp/product/B00W7ATBYC?psc=1&redirect=true&ref_=od_aui_detailpages00   |1 Bunch   |
|15	| Breadboard   |	Breadboard	   |830 Points Rectangular Adhesive Back Solderless Prototype Breadboard MB-102 |	http://www.amazon.in/gp/product/B00NSXA7YK?psc=1&redirect=true&ref_=oh_aui_detailpage_o02_s00 | 1   |


#Step 2

Connect all the sensors to your raspberry Pi. If you need help on how to connect sensors to the Raspberry Pi, visit the complete blog [here].

#Step 3

Copy the [SafeHome.py](RaspberryPi-Code/SafeHome.py) file to your Raspberry Pi. Create the following folder structures with read write permissions in your raspberry Pi.
#####/home/pi/SafeHome/Token/
#####/home/pi/SafeHome/Photos/



 






 
