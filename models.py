# Author: Dimitrios Poulimenos
# Imports
import base64
from datetime import datetime
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
from cryptography.fernet import Fernet
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from app import db

# Author: Dimitrios Poulimenos
# Encrypt Function
def encrypt(data, userkey):
    '''Takes userkey and encrypts the given data'''
    return Fernet(userkey).encrypt(bytes(data, 'utf-8'))

# Author: Dimitrios Poulimenos
# Decrypt Function
def decrypt(data, userkey):
    '''Takes userkey and decrypts the given encrypted data'''
    return Fernet(userkey).decrypt(data).decode("utf-8")

# Author: Dimitrios Poulimenos
# Users Class
class User(db.Model, UserMixin):
    '''It creates the entire database of our web application'''
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    update = db.Column(db.Boolean, nullable=False)

    # Crypto key for user's Emission.
    userkey = db.Column(db.BLOB)

    emissions = db.relationship('Emission')

    def __init__(self, username, firstname, lastname, email, password, role, update):
        '''Takes users given fields and creates an actual user'''
        self.username = username
        self.password = generate_password_hash(password)
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.role = role
        self.userkey = base64.urlsafe_b64encode(scrypt(password, str(get_random_bytes(32)), 32, N=2 ** 14, r=8, p=1))
        self.registered_on = datetime.now()
        self.update = update

    def update_user(self, role):
        self.role = role
        db.session.commit()

# Author: Dimitrios Poulimenos
# Emission Class
class Emission(db.Model):
    '''Takes data that has been stored into the database and creates the emission for the user'''
    __tablename__ = 'emissions'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, db.ForeignKey(User.username), nullable=True)
    result = db.Column(db.Float, nullable=False, default=False)
    created = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, result):
        self.username = username
        self.result = result
        self.created = datetime.now()

# Author: Dimitrios Poulimenos
# Travel Class
class BusRail(db.Model):
    '''Takes data from the calculator form and creates the emission for this specific category'''
    __tablename__ = 'busRail'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, db.ForeignKey(User.username), nullable=True)
    bus = db.Column(db.Float, nullable=False, default=False)
    coach = db.Column(db.Float, nullable=False, default=False)
    natRail = db.Column(db.Float, nullable=False, default=False)
    taxiUber = db.Column(db.Float, nullable=False, default=False)
    created = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, bus, coach, natRail, taxiUber):
        self.username = username
        self.bus = bus
        self.coach = coach
        self.natRail = natRail
        self.taxiUber = taxiUber
        self.created = datetime.now()

# Author: Dimitrios Poulimenos
# Car Class
class Car(db.Model):
    '''Takes data from the calculator form and creates the emission for this specific category'''
    __tablename__ = 'car'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, db.ForeignKey(User.username), nullable=True)
    car_mileage = db.Column(db.Float, nullable=False, default=False)
    car_type = db.Column(db.String, nullable=False, default=False)
    fuel_type = db.Column(db.String, nullable=False, default=False)
    created = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, car_mileage, car_type, fuel_type):
        self.username = username
        self.car_mileage = car_mileage
        self.car_type = car_type
        self.fuel_type = fuel_type
        self.created = datetime.now()

# Author: Dimitrios Poulimenos
# Energy Class
class Energy(db.Model):
    '''Takes data from the calculator form and creates the emission for this specific category'''
    __tablename__ = 'energy'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, db.ForeignKey(User.username), nullable=True)
    electricity = db.Column(db.Float, nullable=False, default=False)
    gas = db.Column(db.Float, nullable=False, default=False)
    propane = db.Column(db.Float, nullable=False, default=False)
    wood = db.Column(db.Float, nullable=False, default=False)
    created = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, electricity, gas, propane, wood):
        self.username = username
        self.electricity = electricity
        self.gas = gas
        self.propane = propane
        self.wood = wood
        self.created = datetime.now()

# Author: Dimitrios Poulimenos
# House Class
class House(db.Model):
    '''Takes data from the calculator form and creates the emission for this specific category'''
    __tablename__ = 'house'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, db.ForeignKey(User.username), nullable=True)
    food = db.Column(db.Float, nullable=False, default=False)
    food_type = db.Column(db.String, nullable=False, default=False)
    clothes = db.Column(db.Float, nullable=False, default=False)
    telephone = db.Column(db.Float, nullable=False, default=False)
    hospitality = db.Column(db.Float, nullable=False, default=False)
    created = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, food, food_type, clothes, telephone, hospitality):
        self.username = username
        self.food = food
        self.food_type = food_type
        self.clothes = clothes
        self.telephone = telephone
        self.hospitality = hospitality
        self.created = datetime.now()

# Author: Dimitrios Poulimenos
# Motorbike Class
class Motorbike(db.Model):
    '''Takes data from the calculator form and creates the emission for this specific category'''
    __tablename__ = 'motorbike'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, db.ForeignKey(User.username), nullable=True)
    motorbike_mileage = db.Column(db.Float, nullable=False, default=False)
    motorbike_type = db.Column(db.String, nullable=False, default=False)
    created = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, motorbike_mileage, motorbike_type):
        self.username = username
        self.motorbike_mileage = motorbike_mileage
        self.motorbike_type = motorbike_type
        self.created = datetime.now()


# Quiz Question
class Quiz(db.Model):
    '''Takes data from the quiz form and creates the questions'''
    __tablename__ = 'quiz'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, db.ForeignKey(User.username), nullable=True)
    question_number = db.Column(db.Integer, nullable=True, unique=True)
    question = db.Column(db.String(150), nullable=False, unique=True)
    option1 = db.Column(db.String(100), nullable=False)
    option2 = db.Column(db.String(100), nullable=False)
    option3 = db.Column(db.String(100), nullable=True)
    option4 = db.Column(db.String(100), nullable=True)
    answer = db.Column(db.String(100), nullable=False)
    created = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, question, option1, option2, option3, option4, answer, userkey):

        self.username = username
        self.created = datetime.now()
        self.question = encrypt(question, userkey)
        self.option1 = encrypt(option1, userkey)
        self.option2 = encrypt(option2, userkey)
        self.option3 = encrypt(option3, userkey)
        self.option4 = encrypt(option4, userkey)
        self.answer = encrypt(answer, userkey)

    def view_question(self, userkey):

        self.question = decrypt(self.question, userkey)
        self.option1 = decrypt(self.option1, userkey)
        self.option2 = decrypt(self.option2, userkey)
        self.option3 = decrypt(self.option3, userkey)
        self.option4 = decrypt(self.option4, userkey)
        self.answer = decrypt(self.answer, userkey)

    def update_question(self, question, option1, option2, option3, option4, answer, userkey):

        self.question = encrypt(question, userkey)
        self.option1 = encrypt(option1, userkey)
        self.option2 = encrypt(option2, userkey)
        self.option3 = encrypt(option3, userkey)
        self.option4 = encrypt(option4, userkey)
        self.answer = encrypt(answer, userkey)
        db.session.commit()


# Messages to inbox
class Message(db.Model):
    '''Takes data from the message form and creates the message to be sent'''
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String, db.ForeignKey(User.username), nullable=False)
    receiver = db.Column(db.String, db.ForeignKey(User.username), nullable=False)
    header = db.Column(db.Integer, nullable=False)
    body = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    read = db.Column(db.Boolean, nullable=False)

    def __init__(self, sender, receiver, header, body, read):
        '''Takes in a number n, returns the square of n'''
        self.sender = sender
        self.receiver = receiver
        self.header = header
        self.body = body
        self.date = datetime.now()
        self.read = read

# Author: Dimitrios Poulimenos
# Database Initialization
def init_db():
    '''Initialising the database'''
    db.drop_all()
    db.create_all()

    # Initialise users
    user0 = User(username='admin',
                 firstname='Thomas',
                 lastname='Anderson',
                 password='Admin1!',
                 email='admin@email.com',
                 role='admin',
                 update=True)

    user1 = User(username='jjones',
                 firstname='Joey',
                 lastname='Jones',
                 password='Jjo1!',
                 email='jjones@email.com',
                 role='user',
                 update=False)

    user2 = User(username='tshelton',
                 firstname='Troy',
                 lastname='Shelton',
                 password='tsh1!',
                 email='tshelton@email.com',
                 role='user',
                 update=True)

    user3 = User(username='cvictor',
                 firstname='Victor',
                 lastname='Clark',
                 password='Vcl1!',
                 email='johndoe@email.com',
                 role='user',
                 update=True)

    user4 = User(username='msebastian',
                 firstname='Sebastian',
                 lastname='Morgan',
                 password='Mse1!',
                 email='msebastian@email.com',
                 role='user',
                 update=True)



    # Author: Dimitrios Poulimenos
    # Initialise Energy results
    energy1 = Energy(username='jjones',
                     electricity=2000 * 0.0002,
                     gas=300 * 0.0002,
                     propane=500 * 0.0016,
                     wood=12 * 0.0726)

    energy2 = Energy(username='jjones',
                     electricity=1000 * 0.0002,
                     gas=200 * 0.0002,
                     propane=600 * 0.0016,
                     wood=2 * 0.0726)

    energy3 = Energy(username='tshelton',
                     electricity=5000 * 0.0002,
                     gas=900 * 0.0002,
                     propane=70 * 0.0016,
                     wood=1 * 0.0726)

    energy4 = Energy(username='tshelton',
                     electricity=3000 * 0.0002,
                     gas=1000 * 0.0002,
                     propane=468 * 0.0016,
                     wood=23 * 0.0726)

    energy5 = Energy(username='cvictor',
                     electricity=2000 * 0.0002,
                     gas=300 * 0.0002,
                     propane=500 * 0.0016,
                     wood=12 * 0.0726)

    energy6 = Energy(username='cvictor',
                     electricity=2000 * 0.0002,
                     gas=300 * 0.0002,
                     propane=500 * 0.0016,
                     wood=27 * 0.0726)

    energy7 = Energy(username='msebastian',
                     electricity=1234 * 0.0002,
                     gas=4564 * 0.0002,
                     propane=45 * 0.0016,
                     wood=0 * 0.0726)

    energy8 = Energy(username='msebastian',
                     electricity=6547 * 0.0002,
                     gas=8978 * 0.0002,
                     propane=987 * 0.0016,
                     wood=12 * 0.0726)

    # Author: Dimitrios Poulimenos
    # Initialise house results
    house1 = House(username='jjones',
                   food=1230 * 0.00077,
                   food_type='Vegan',
                   clothes=1987 * 0.0209,
                   telephone=1000 * 0.0002,
                   hospitality=2354 * 0.0004)

    house2 = House(username='jjones',
                   food=1500 * 0.00077,
                   food_type='Vegan',
                   clothes=654 * 0.0209,
                   telephone=3454 * 0.0002,
                   hospitality=2354 * 0.0004)

    house3 = House(username='tshelton',
                   food=6542 * 0.00077,
                   food_type='Vegetarian',
                   clothes=1234 * 0.0209,
                   telephone=3456 * 0.0002,
                   hospitality=1276 * 0.0004)

    house4 = House(username='tshelton',
                   food=123 * 0.00077,
                   food_type='Vegetarian',
                   clothes=654 * 0.0209,
                   telephone=900 * 0.0002,
                   hospitality=2354 * 0.0004)

    house5 = House(username='cvictor',
                   food=1210 * 0.00077,
                   food_type='Pescaterian',
                   clothes=654 * 0.0209,
                   telephone=1000 * 0.0002,
                   hospitality=2354 * 0.0004)

    house6 = House(username='cvictor',
                   food=1239 * 0.00077,
                   food_type='Pescaterian',
                   clothes=4567 * 0.0209,
                   telephone=456 * 0.0002,
                   hospitality=2354 * 0.0004)

    house7 = House(username='msebastian',
                   food=2000 * 0.00077,
                   food_type='Medium',
                   clothes=2000 * 0.0209,
                   telephone=1500 * 0.0002,
                   hospitality=2560 * 0.0004)

    house8 = House(username='msebastian',
                   food=2200 * 0.00077,
                   food_type='Medium',
                   clothes=2540 * 0.0209,
                   telephone=1233 * 0.0002,
                   hospitality=2700 * 0.0004)

    # Author: Dimitrios Poulimenos
    # Initialise BusRail results
    bus1 = BusRail(username='jjones',
                   bus=60 * 0.00016,
                   coach=658 * 0.00004,
                   natRail=132 * 0.000057,
                   taxiUber=45 * 0.00024)

    bus2 = BusRail(username='jjones',
                   bus=48 * 0.00016,
                   coach=123 * 0.00004,
                   natRail=454 * 0.000057,
                   taxiUber=98 * 0.00024)

    bus3 = BusRail(username='tshelton',
                   bus=45 * 0.00016,
                   coach=67 * 0.00004,
                   natRail=457 * 0.000057,
                   taxiUber=34 * 0.00024)

    bus4 = BusRail(username='tshelton',
                   bus=345 * 0.00016,
                   coach=35 * 0.00004,
                   natRail=76 * 0.000057,
                   taxiUber=45 * 0.00024)

    bus5 = BusRail(username='cvictor',
                   bus=12 * 0.00016,
                   coach=456 * 0.00004,
                   natRail=67 * 0.000057,
                   taxiUber=86 * 0.00024)

    bus6 = BusRail(username='cvictor',
                   bus=459 * 0.00016,
                   coach=546 * 0.00004,
                   natRail=78 * 0.000057,
                   taxiUber=89 * 0.00024)

    bus7 = BusRail(username='msebastian',
                   bus=56 * 0.00016,
                   coach=56 * 0.00004,
                   natRail=778 * 0.000057,
                   taxiUber=546 * 0.00024)

    bus8 = BusRail(username='msebastian',
                   bus=234 * 0.00016,
                   coach=643 * 0.00004,
                   natRail=346 * 0.000057,
                   taxiUber=477 * 0.00024)

    # Author: Dimitrios Poulimenos
    # Initialise Car results
    car1 = Car(username='jjones',
               car_mileage=55659 * 0.0003,
               car_type='Car',
               fuel_type='Diesel')

    car2 = Car(username='jjones',
               car_mileage=45987 * 0.0003,
               car_type='Car',
               fuel_type='Diesel')

    car3 = Car(username='tshelton',
               car_mileage=654654 * 0.0003,
               car_type='Car',
               fuel_type='Gasoline')

    car4 = Car(username='tshelton',
               car_mileage=987987 * 0.0003,
               car_type='Car',
               fuel_type='Gasoline')

    car5 = Car(username='cvictor',
               car_mileage=2132747 * 0.0003,
               car_type='Van',
               fuel_type='Gasoline')

    car6 = Car(username='cvictor',
               car_mileage=165768 * 0.0003,
               car_type='Van',
               fuel_type='Gasoline')

    car7 = Car(username='msebastian',
               car_mileage=998798 * 0.0003,
               car_type='Car',
               fuel_type='Petrol')

    car8 = Car(username='msebastian',
               car_mileage=16548 * 0.0003,
               car_type='Car',
               fuel_type='Petrol')

    # Author: Dimitrios Poulimenos
    # Initialise Motorbike results
    motorbike1 = Motorbike(username='jjones',
                           motorbike_mileage=1687 * 0.0002,
                           motorbike_type='Low')

    motorbike2 = Motorbike(username='jjones',
                           motorbike_mileage=1956 * 0.0002,
                           motorbike_type='Low')

    motorbike3 = Motorbike(username='tshelton',
                           motorbike_mileage=2654 * 0.0002,
                           motorbike_type='Medium')

    motorbike4 = Motorbike(username='tshelton',
                           motorbike_mileage=3500 * 0.0002,
                           motorbike_type='Medium')

    motorbike5 = Motorbike(username='cvictor',
                           motorbike_mileage=3600 * 0.0002,
                           motorbike_type='Large')

    motorbike6 = Motorbike(username='cvictor',
                           motorbike_mileage=4600 * 0.0002,
                           motorbike_type='Large')

    motorbike7 = Motorbike(username='msebastian',
                           motorbike_mileage=4556 * 0.0002,
                           motorbike_type='Medium')

    motorbike8 = Motorbike(username='msebastian',
                           motorbike_mileage=9897 * 0.0002,
                           motorbike_type='Medium')

    # Author: Dimitrios Poulimenos
    # Initialise Emission results
    emission1 = Emission(
        username='jjones',
        result=motorbike1.motorbike_mileage + house1.food + house1.clothes +
               house1.hospitality + house1.telephone + car1.car_mileage + energy1.wood
               + energy1.gas + energy1.propane + energy1.electricity + bus1.bus +
               bus1.natRail + bus1.coach + bus1.taxiUber
    )
    emission2 = Emission(
        username='jjones',
        result=motorbike2.motorbike_mileage + house2.food + house2.clothes +
               house2.hospitality + house2.telephone + car2.car_mileage + energy2.wood
               + energy2.gas + energy2.propane + energy2.electricity + bus2.bus +
               bus2.natRail + bus2.coach + bus2.taxiUber
    )
    emission3 = Emission(
        username='tshelton',
        result=motorbike3.motorbike_mileage + house3.food + house3.clothes +
               house3.hospitality + house3.telephone + car3.car_mileage + energy3.wood
               + energy3.gas + energy3.propane + energy3.electricity + bus3.bus +
               bus3.natRail + bus3.coach + bus3.taxiUber
    )
    emission4 = Emission(
        username='tshelton',
        result=motorbike4.motorbike_mileage + house4.food + house4.clothes +
               house4.hospitality + house4.telephone + car4.car_mileage + energy4.wood
               + energy4.gas + energy4.propane + energy4.electricity + bus4.bus +
               bus4.natRail + bus4.coach + bus4.taxiUber
    )
    emission5 = Emission(
        username='cvictor',
        result=motorbike5.motorbike_mileage + house5.food + house5.clothes +
               house5.hospitality + house5.telephone + car5.car_mileage + energy5.wood
               + energy5.gas + energy5.propane + energy5.electricity + bus5.bus +
               bus5.natRail + bus5.coach + bus5.taxiUber
    )
    emission6 = Emission(
        username='cvictor',
        result=motorbike6.motorbike_mileage + house6.food + house6.clothes +
               house6.hospitality + house6.telephone + car6.car_mileage + energy6.wood
               + energy6.gas + energy6.propane + energy6.electricity + bus6.bus +
               bus6.natRail + bus6.coach + bus6.taxiUber
    )
    emission7 = Emission(
        username='msebastian',
        result=motorbike7.motorbike_mileage + house7.food + house7.clothes +
               house7.hospitality + house7.telephone + car7.car_mileage + energy7.wood
               + energy7.gas + energy7.propane + energy7.electricity + bus7.bus +
               bus7.natRail + bus7.coach + bus7.taxiUber
    )
    emission8 = Emission(
        username='msebastian',
        result=motorbike8.motorbike_mileage + house8.food + house8.clothes +
               house8.hospitality + house8.telephone + car8.car_mileage + energy8.wood
               + energy8.gas + energy8.propane + energy8.electricity + bus8.bus +
               bus8.natRail + bus8.coach + bus8.taxiUber
    )

    # Author: Dimitrios Poulimenos
    # Initialise quiz questions
    quizq1 = Quiz(username="admin",
                  question="How many plastic bottles are purchased per year in the UK?",
                  option1="650 Million",
                  option2="1.4 Billion",
                  option3="4.2 Billion",
                  option4="7.7 Billion",
                  answer="7.7 Billion",
                  userkey=User.query.filter_by(username="admin").first.userkey)

    quizq2 = Quiz(username="admin",
                  question="Drying one load of laundry a week puts how many metric tons of CO2 into the atmosphere>",
                  option1="1",
                  option2="0.1",
                  option3="0.5",
                  option4="0.01",
                  answer="0.1",
                  userkey=User.query.filter_by(username="admin").first.userkey)

    quizq3 = Quiz(username="admin",
                  question="What sector contributes the largest amount of CO2 to the UK’s carbon footprint?",
                  option1="Agriculture",
                  option2="Transport",
                  option3="Energy",
                  option4="Residential",
                  answer="Transport",
                  userkey=User.query.filter_by(username="admin").first.userkey)

    # Author: Dimitrios Poulimenos
    # Add data to User database
    db.session.add(user0)
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)

    # Author: Dimitrios Poulimenos
    # Add data to Energy Database
    db.session.add(energy1)
    db.session.add(energy2)
    db.session.add(energy3)
    db.session.add(energy4)
    db.session.add(energy5)
    db.session.add(energy6)
    db.session.add(energy7)
    db.session.add(energy8)

    # Author: Dimitrios Poulimenos
    # Add data to House Database
    db.session.add(house1)
    db.session.add(house2)
    db.session.add(house3)
    db.session.add(house4)
    db.session.add(house5)
    db.session.add(house6)
    db.session.add(house7)
    db.session.add(house8)

    # Author: Dimitrios Poulimenos
    # Add data to Bus Database
    db.session.add(bus1)
    db.session.add(bus2)
    db.session.add(bus3)
    db.session.add(bus4)
    db.session.add(bus5)
    db.session.add(bus6)
    db.session.add(bus7)
    db.session.add(bus8)

    # Author: Dimitrios Poulimenos
    # Add data to Car Database
    db.session.add(car1)
    db.session.add(car2)
    db.session.add(car3)
    db.session.add(car4)
    db.session.add(car5)
    db.session.add(car6)
    db.session.add(car7)
    db.session.add(car8)

    # Author: Dimitrios Poulimenos
    # Add data to Motorbike Database
    db.session.add(motorbike1)
    db.session.add(motorbike2)
    db.session.add(motorbike3)
    db.session.add(motorbike4)
    db.session.add(motorbike5)
    db.session.add(motorbike6)
    db.session.add(motorbike7)
    db.session.add(motorbike8)

    # Author: Dimitrios Poulimenos
    # Add data to Emission database
    db.session.add(emission1)
    db.session.add(emission2)
    db.session.add(emission3)
    db.session.add(emission4)
    db.session.add(emission5)
    db.session.add(emission6)
    db.session.add(emission7)
    db.session.add(emission8)

    # Add data to question database
    db.session.add(quizq1)
    db.session.add(quizq2)
    db.session.add(quizq3)

    db.session.commit()
