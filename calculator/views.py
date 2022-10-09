# Author: Dimitrios Poulimenos
# Imports
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from models import Energy, BusRail, Car, House, Motorbike, Emission
from app import db
from calculator.forms import CalculatorForm

# Config
calculator_blueprint = Blueprint('calculator', __name__, template_folder='templates')

# Author: Dimitrios Poulimenos
@calculator_blueprint.route('/calculator', methods=('GET', 'POST'))
def calculator():
    '''It takes the values from the user and calculating the emission of the user'''
    # Create Calculator form
    form = CalculatorForm()

    # If request method is POST or form is valid
    if form.validate_on_submit():
        if current_user.is_authenticated:
            # Create a new Emission for each category
            new_bus_rail = BusRail(username=current_user.username,
                                  bus=form.bus.data * 0.00016,
                                  coach=form.coach.data * 0.00004,
                                  natRail=form.natRail.data * 0.000057,
                                  taxiUber=form.taxiUber.data * 0.00024)

            new_car = Car(username=current_user.username,
                          car_mileage=form.car_mileage.data * 0.0003,
                          car_type=form.car_type.data,
                          fuel_type=form.fuel_type.data)

            new_energy = Energy(username=current_user.username,
                                electricity=form.electricity.data * 0.0002,
                                gas=form.gas.data * 0.0002,
                                propane=form.propane.data * 0.0016,
                                wood=form.wood.data * 0.0726)

            new_house = House(username=current_user.username,
                              food=form.food.data * 0.00077,
                              food_type=form.food_type.data,
                              clothes=form.clothes.data * 0.0209,
                              telephone=form.telephone.data * 0.0002,
                              hospitality=form.hospitality.data * 0.0004)

            new_motorbike = Motorbike(username=current_user.username,
                                      motorbike_mileage=form.motorbike_mileage.data * 0.0002,
                                      motorbike_type=form.motorbike_type.data)

            new_emission = Emission(username=current_user.username,
                                    result=new_motorbike.motorbike_mileage +
                                    new_house.food + new_house.clothes +
                                    new_house.hospitality + new_house.telephone +
                                    new_car.car_mileage + new_energy.wood +
                                    new_energy.gas + new_energy.propane +
                                    new_energy.electricity + new_bus_rail.bus +
                                    new_bus_rail.natRail + new_bus_rail.coach +
                                    new_bus_rail.taxiUber)

            # add the new question to the database
            db.session.add(new_bus_rail)
            db.session.add(new_car)
            db.session.add(new_energy)
            db.session.add(new_house)
            db.session.add(new_motorbike)
            db.session.add(new_emission)
            db.session.commit()

        # sends user to view questions page
        return redirect(url_for('users.panel'))
    # if request method is get or form not valid re-render create question page
    return render_template('calculator/calculator.html', form=form)
