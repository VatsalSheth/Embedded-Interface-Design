# Embedded Interface Design Project 1

by Vatsal Sheth and Ranger Beguelin

## Installation Instructions

To use this software numerous things need to be setup and installed on your Raspberry Pi 3. First and foremost Python (namely Python 3)
needs to be installed. Please ensure that Python 3.7.3 or later is installed on your Pi. As Python is often included with Raspbian, the
popular Linux distribution for Raspberry Pis, you may be able to skip this step. However, make sure the version of Python you have is sufficiently recent using the `python3 --version` command in the terminal.

Next, you will need the MySQL database software used by the team for this project. As declared on the class Slack channel on 9/16/19 MariaDB
is an acceptable drop in replacement for MySQL. As such, that is what the team used for this project. It is recommended that one follow
[this guide](https://pimylifeup.com/raspberry-pi-mysql/) for setting up MariaDB. When it comes to the last five steps for setting up a
user and database please follow the commands below instead:

* Log into MariaDB command line using `sudo mysql -u root -p` (We hope you remembered the root password made when MariaDB was installed!)
* Inside the MariaDB command line interface create the database the project will use (aptly named "project1") using this command: `CREATE DATABASE project1;`
* Still inside the MariaDB command line create the username and password the program will use with this command: `CREATE USER 'vatsal'@'localhost' IDENTIFIED BY '12345';`
* Grant the user you made in the previous step all the privileges it will need with this command: `GRANT ALL PRIVILEGES ON project1.* TO 'vatsal'@'localhost';`
* Flush the privileges table, allowing the changes made in the previous step to take effect, with this command: `FLUSH PRIVILEGES;`
* Exit the MariaDB command line using `CTRL + C`

Now that Python and MariaDB are installed we unfortunately still have a long way to go. Three of the necessary installs are quick and will be listed here. Please note that all of them assume the package handler "pip" has already been installed on your device:
* We need the MySQL driver "mysql connector"
  * Install mysql connector with this command: `sudo pip install mysql-connector`
* We need the Adafruit library for the temperature/humidity sensor we are using
  * Install the library with this command `sudo pip3 install Adafruit_DHT`
* We need the "multitimer" python module
  * Install the module with this command: `sudo pip install multitimer`

Last but not least we need the software that makes our graphical user interface (GUI) possible. This means we need QT, a software library, and we need PyQT, the bindings for QT on Linux when developing software in Python. Fortunately, the commands for installing these two items were provided in lecture and are as follows:

* `sudo apt-get install qt5-default pyqt5-dev  pyqt5-dev-tools`
* `sudo apt-get install qttools5-dev-tools`

And thats it! To the best of our knowledge these are the elements necessary to run our Project 1 code.


## Project Work

* Vatsal
  * GUI backend
  * Database code
  * Humidity/Temperature plots
  * "Project Additions" functionality
    * see below

* Ranger
  * GUI layout
  * Project README
  * Sensor circuit

## Project Additions

Going above and beyond for this project involved taking on the additional requirement of giving the user the ability to switch between degrees Fahrenheit and degrees Celsius. By selecting the corresponding radio button in the bottom right corner of the GUI window the user is free to select their desired units for the temperature readout(s).
