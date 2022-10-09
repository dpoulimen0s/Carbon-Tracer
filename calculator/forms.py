# Imports
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, FloatField
from wtforms.validators import input_required


# Author: Dimitrios Poulimenos
# Calculator Form
class CalculatorForm(FlaskForm):
    '''This function creates the form of the calculator page'''
    # Travel category
    bus = FloatField(validators=[input_required()])
    coach = FloatField(validators=[input_required()])
    natRail = FloatField(validators=[input_required()])
    taxiUber = FloatField(validators=[input_required()])

    # Car category
    car_mileage = FloatField(validators=[input_required()])
    car_type = SelectField('Car Type', choices=[('Car', 'Car '),
                                                ('Van', 'Van')], validators=[input_required()])
    fuel_type = SelectField('Fuel Type', choices=[('Gasoline', 'Gasoline'),
                                                  ('Diesel', 'Diesel'),
                                                  ('Petrol', 'Petrol'),
                                                  ('Hybrid', 'Hybrid'),
                                                  ('Electric', 'Electric'),
                                                  ], validators=[input_required()])

    # Energy category
    electricity = FloatField(validators=[input_required()])
    gas = FloatField(validators=[input_required()])
    propane = FloatField(validators=[input_required()])
    wood = FloatField(validators=[input_required()])

    # House category
    food = FloatField(validators=[input_required()])
    food_type = SelectField('Food Type', choices=[
        ('Vegan', 'Vegan'),
        ('Vegetarian', 'Vegetarian'),
        ('Pescaterian', 'Pescaterian'),
        ('Low', 'Low Meat Eater'),
        ('Medium', 'Medium Meat Eater'),
        ('High', 'High Meat Eater')], validators=[input_required()])
    clothes = FloatField(validators=[input_required()])
    telephone = FloatField(validators=[input_required()])
    hospitality = FloatField(validators=[input_required()])

    # Motorbike category
    motorbike_mileage = FloatField(validators=[input_required()])
    motorbike_type = SelectField('Motorbike Type', choices=[
        ('Low', 'Up to 125cc'),
        ('Medium', '125cc to 500cc'),
        ('Large', 'Over 500cc ')],
                                 validators=[input_required()])
    submit = SubmitField()
