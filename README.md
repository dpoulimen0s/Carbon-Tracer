# Carbon-Tracer

## Carbon tracer is a web application which aims to make users conscious of their impact on the planet.
It consists of a home page with information about the application, a carbon emissions calculator where users can find out how they impact the planet, and a quiz where users can test their knowledge on contributing factors to carbon emissions. There is also a frame for users logging in and out, role-based access, and an extensive platform admins can use to change the questions for users, and send messages to users. Users are notified in an inbox when new questions are posted, and can edit their profile details.

## Run locally and access through a modern web browser of your choice- tested to run on chrome.
Feel free to use the project how you please- making an account will allow you access to the most features. Try the quiz and calculator out- we hope it helps you better understand your impact on our planet!

## Getting Started

This is a pretty straight forward process. All you have to do is to Fork the project to your space and clone the project
to your IDE.

### Prerequisites

* Python (3.10) or later.
* Pycharm IDEA (or your preferred IDE).


### Installing

First you will need python to be installed to your system. Secondly, you are going to
need an IDE (PycharmIDE) in order to run the program. However, you can run your program via command prompt if 
u are using Windows or terminal if u are on Unix system. Then you need to Fork the project to your personal space and
clone it to your IDE. After that you can install all the requirements you need in order to be able to run our Webapp.

Ensure you enter the following commands into the console so to load the database:
1. from models import init_db
2. init_db()


#
If you have a DataBase contact problem:
1. init project create db When the project migration database fails to be linked, you can run the Flask shell in the Dos terminal to link the database
1. flask shell
2. from app import app
3. from models import *
4. from app import db
5. db.create_all()


## Running the tests

We have created 5 users (admin included) where each user and not the admin has 2 c02 emission results to test the Web application.
These hardcoded sample data that we have provided are trying to test the classes, and the complexity of my methods.

## Built With

* Pycharm IDEA
* HTML/CSS
* Javascript
* jQuery
* Bootstrap
* Windows 10/11

## Authors

* **Dimitris Poulimenos** - {Initial Work} - [dpoulimenos](https://github.com/dpoulimen0s)
* **Jackson Thomas** - [jthomas](https://github.com/jacky-ct)
* **Will Newbould** - [wnewbould](https://github.com/WillNewbo12)
* **Will Adams** - [wadams](https://github.com/c0039921)
* **Zhuolin 'Winter' Yong** - [zyong](https://github.com/b9067280)

## License

This project is licensed under the MIT License.
