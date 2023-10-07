from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
from flask import Flask, render_template, request, session
from calorie import Calorie
from temperature import Temperature
from caloric_meals import Meals

app = Flask(__name__)

class HomePage(MethodView):

    def get(self):
        return render_template('index.html')


class CaloriesFormPage(MethodView):

    def get(self):
        calories_form =CaloriesForm()
        return render_template('calories_form_page.html', caloriesform=calories_form)

    def post(self):
        calories_form = CaloriesForm(request.form)

        temperature = Temperature(country=calories_form.country.data,
                                  city=calories_form.city.data).get()

        calorie = Calorie(weight=float(calories_form.weight.data),
                           height=float(calories_form.height.data),
                           age=float(calories_form.age.data),
                           temperature=temperature)
        global calories
        calories = calorie.calculate()


        return render_template('result.html',
                               caloriesform=calories_form,
                               calories=calories)

class CaloriesForm(Form):
    weight=StringField("Weight: ", default=70)
    height=StringField("Height: ", default=175)
    age=StringField("Age: ", default=32)
    country=StringField("Country: ", default="Romania")
    city=StringField("City: ", default="Bucharest")
    button=SubmitField("Calculate")


class Result(MethodView):
    def get(self):
        return render_template('result.html')



class MealsFormPage(MethodView):
    def get(self):
        meals_form = MealsForm()
        return render_template('meniu.html', mealsform=meals_form, calories=calories)

    def post(self):
        meals_form = MealsForm(request.form)

        meals = Meals(calories)
        menu = meals.generate_menu()
        breakfast = menu[0][0]
        breakfast_k = menu[0][1]
        lunch = menu[1][0]
        lunch_k = menu[1][1]
        dinner = menu[2][0]
        dinner_k = menu[2][1]
        snack1 = menu[3][0]
        snack1_k = menu[3][1]
        snack2 = menu[4][0]
        snack2_k = menu[4][1]
        return render_template('meniu.html', breakfast=breakfast, snack1=snack1, lunch=lunch, snack2=snack2, dinner=dinner,
                               breakfast_k=round(breakfast_k,2), lunch_k=round(lunch_k, 2), dinner_k=round(dinner_k,2),
                               snack1_k=round(snack1_k,2), snack2_k=round(snack2_k,2),
                               mealsform=meals_form, result=True)



class MealsForm(Form):
    button = SubmitField("Generate Menu")

app.add_url_rule('/',
                 view_func=HomePage.as_view('home_page'))
app.add_url_rule('/calories_form',
                 view_func=CaloriesFormPage.as_view('calories_form_page'))
app.add_url_rule('/result',
                 view_func=Result.as_view('result'))
app.add_url_rule('/meniu',
                  view_func=MealsFormPage.as_view('meniu'))

app.run(debug=True)

