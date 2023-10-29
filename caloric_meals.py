import sqlite3
import random


class Meals:
    """
    This class is responsible for generating a menu based on the user's calorie requirements.
    It interacts with a SQLite database to select food items for breakfast, lunch, dinner, and snacks.
    The generated menu is returned as a list of food items with their associated calorie values.
    Attributes:
    - kcal (float): The user's daily calorie requirement.
    - database (str): The SQLite database file containing food data."""

    database = "food.db"

    def __init__(self, kcal):
        """
         Initialize a Meals object with the specified daily calorie requirement (kcal)."""
        self.kcal = kcal

    def select_food(self, condition, calorie_percentage):
        """
        Select a food item based on the given condition and calorie percentage.

        Args:
        - condition (str): The condition for selecting a food item (e.g., "morning" for breakfast).
        - calorie_percentage (int): The percentage of calories to consider for the food item.

        Returns:
        - food (str): The selected food item.
        - calories (float): The adjusted calorie value of the selected food item."""

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
        """
          Select multiple food items based on the given condition and calorie percentage.

        Args:
        - condition (str): The condition for selecting food items (e.g., "morning" for breakfast).
        - calorie_percentage (int): The percentage of calories to consider for the food items.

        Returns:
        - foods (list): A list of selected food items.
        - total_calories (float): The total adjusted calorie value of the selected food items."""

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
        """
        Generate a menu consisting of breakfast, lunch, dinner, and snacks."""

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

