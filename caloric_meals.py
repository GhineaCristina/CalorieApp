import sqlite3
import random


class Meals:
    database = "food.db"

    def __init__(self, kcal):
        self.kcal = kcal

    def select_food(self, condition, calorie_percentage):
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(f"""
                SELECT "food", "calories" FROM "food" WHERE "{condition}" = 1
                ORDER BY RANDOM() 
                LIMIT 1
            """)
            food, calories = cursor.fetchone()

            return food, calories * calorie_percentage / 100


    def select_foods(self, condition, calorie_percentage):
        foods = []
        total_calories = 0
        calorie_value = calorie_percentage * self.kcal / 100

        while total_calories < calorie_value:
            food, calories = self.select_food(condition, calorie_percentage)
            if food not in foods:
                foods.append(food)
                total_calories += calories

        return foods, total_calories


    def generate_menu(self):

        breakfast = self.select_foods("morning", 20)
        lunch = self.select_foods("lunch", 30)
        dinner = self.select_foods("dinner", 20)
        snack1 = self.select_foods("snack", 15)
        snack2 = self.select_foods("snack", 15)

        return breakfast, lunch, dinner, snack1, snack2


if __name__ == "__main__":
    meals = Meals(1400)
    menu = meals.generate_menu()

    print("Menu:", menu)

