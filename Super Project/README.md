# EID-Project-6 - MAGIC WAND
  
This project was completed under the course Embedded Interface Design at University of Colorado, Boulder under the guidance of Professor Bruce Montgomery in November - December 2019.
  
## Authors: Siddhant Jajoo, Satya Mehta, Vatsal Sheth  

## Installation Instructions 
 Run below commands to install all the libraries and dependencies to required for this project. 
    
***Python Installation***
- sudo apt-get update
- sudo apt-get upgrade
- sudo apt-get install python3-dev python3-pip
  
***MySQL Installation***
- pip install MySQL-python
- sudo apt-get install mysql-client
- sudo apt-get install mariadb-server
- sudo apt-get install mariadb-client

***PyQT Installation***
- sudo apt-get install qt5-default pyqt5-dev-pyqt5-dev-tools
- sudo apt-get install qttools-dev-tools

***Tornado Installation***
- sudo pip install tornado

***NodeJS Installation***
- curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash
- restart your terminal
- nvm -version should return 0.34.0
- nvm install node
- nvm install 10.16.3

***NodeJS Mysql Installation***
- npm install mysql
- npm install websocket (in the working directory)
- nm init -y (in the working directory)  

***AWS Python SDK Intsallation***
- sudo pip install AWSIoTPythonSDK


***AWS Account is required for this project and should have services like IoT Core, SQS, SNS enabled and authorized.***

## Instructions to Run
There is a run script provided in the current github repository in the Project6 folder. Just execute `./run.sh` to execute the nodejs and GUI programs on the server side.
In order to run client code , execute `python3 client.py`


## Project Work
The project consists of a microphone, a speaker, a camera and various amazon services such as Simple Queue Service (SQS), Simple Storage Service (S3) Bucket, LEX, AWS Poly and AWS Image Rekognition. The camera takes a picture on speaking a command such as identify and then sends the image to AWS which performs a couple of AWS services, recognizes the image and then sends the image and a label to the user and converts the label to speech and uses the speaker as well. The user needs to feedback if the image has been detected accurately or not by using the keywords such as right and wrong.
The feedback data is then sent to the client to keep statistics with the latest image taken in Mysql database.

Additional Feature: GUI LOGIN - The user can access the Statistics on the GUI only if he/she has a username and password or by using an RFID Tag. Thus, only authorized users are able to access the statistics on the GUI.


## Coding Languages used
- Nodejs
- Python

  
->Satya Mehta - Client Side of the Project
->Siddhant Jajoo - NodeJs Server Side, Mysql, SQS
->Vatsal Sheth - RFID and GUI in Python



## References
- https://github.com/adafruit/DHT-sensor-library - Adafruit library for DHT22 sensor.
- https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/ - Adafruit Sensor Installation
- https://www.w3schools.com/nodejs/nodejs_mysql.asp - Node.js talking to MySQL
- https://www.pubnub.com/blog/nodejs-websocket-programming-examples/ - Node.js WebServer example
- https://os.mbed.com/cookbook/Websockets-Server - Python-Tornado-HTML example
- http://www.tornadoweb.org/en/stable/
- https://wiki.python.org/moin/WebServers - Many other choices, many levels of complexity
- https://docs.aws.amazon.com/iot/latest/developerguide/iot-gs.html - AWS IoT Initialization.
- https://techblog.calvinboey.com/raspberrypi-aws-iot-python/ - Raspberry Pi AWS IoT SDK example
- https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-making-api-requests.html - SQS with HTTP Get, Set Request
- https://docs.aws.amazon.com/lambda/latest/dg/with-sns-example.html - Using Lambda with SNS
- https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/sqs-examples.html
