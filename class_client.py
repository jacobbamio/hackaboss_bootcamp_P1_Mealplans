import requests
import json
import pandas as pd
import numpy as np
from IPython.display import display
from creds import *

class client:

    def __init__(self,name,surname,kcal,menudays,diet, exclude, address, client_id):

        #Name es la variable que recogerá el nombre aleatorio de cada instancia de cliente

        self.name = name

        #Surname es la variable que recogerá el apellido aleatorio de cada instancia de cliente

        self.surname = surname

        #Kcal es la variable que recogerá las kcal aleatorias para crear el menú de cada instancia de cliente

        self.kcal = kcal

        #Menudays es la variable que recogerá para qué días aleatorios quiere recibir menú de cada instancia de cliente

        self.menudays = menudays

        #Diet es la variable que recogerá una dieta aleatoria de cada instancia de cliente

        self.diet = diet

        #Exclude es la variable que recogerá qué alimentos aleatorios se quieren excluir del menú de cada instancia de cliente

        self.exclude = exclude

        #Address es la variable que recogerá la dirección aleatoria de cada instancia de cliente

        self.address = address

        #client_id es la variable que recogerá el id del cliente para poder añadirlo a Airtable, y filtrar en base a él para extraer los datos

        self.client_id = client_id

##### Funciones para mostrar y editar la información inicial #########################################################################

    def display_info(self):

        print(f"Name: {self.name}")
        print(f"Surname: {self.surname}")
        print(f"Calories: {self.kcal}")
        print(f"Days of the menu: {self.menudays}")
        print(f"Kind of diet: {self.diet}")
        print(f"Excluded ingredients: {self.exclude}")
        print(f"Address: {self.address}")

        return [self.name, self.surname, self.kcal, self.menudays, self.diet, self.exclude, self.address, self.client_id]


    def edit_name(self, new_name):

        self.last_name = self.name
        self.name = new_name

        print(f"You changed from: {self.last_name} to {self.name}")

    def edit_surname(self, new_surname):

        self.last_surname = self.surname
        self.surname = new_surname

        print(f"You changed from: {self.last_surname} to {self.surname}")

    def edit_kcal(self, new_kcal):

        self.last_kcal = self.kcal
        self.kcal = new_kcal

        print(f"You changed from: {self.last_kcal} to {self.kcal}")

    def edit_menudays(self, new_menudays):

        self.last_menudays = self.menudays
        self.menudays = new_menudays

        print(f"You changed from: {self.last_menudays} to {self.menudays}")

    def edit_diet(self, new_diet):

        self.last_diet = self.diet
        self.diet = new_diet

        print(f"You changed from: {self.last_diet} to {self.diet}")

    def edit_exclude(self, new_exclude):

        self.last_exclude = self.exclude
        self.exclude = new_exclude

        print(f"You changed from: {self.last_exclude} to {self.exclude}")

    def edit_address(self, new_address):

        self.last_address = self.address
        self.address = new_address

        print(f"You changed from: {self.last_address} to {self.address}")

######################################################################################################################################


##### Funciones para crear menú individualizado #########################################################################

    def create_calendar_menu(self):

        url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/mealplans/generate"

        querystring = {"timeFrame":"week","targetCalories":self.kcal, "diet": self.diet,"exclude":self.exclude}

        headers = {
            "X-RapidAPI-Key": rapid_api_key,
            "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"}

        self.list_ids, self.list_menu_ids, self.list_recipes, self.list_daily_recipes = [],[],[],[]

        while len(self.list_ids) < (len(self.menudays)*3):

            response = requests.request("GET", url, headers=headers, params=querystring)

            if len(response.json()["items"]) == 0:

                self.list_ids = ["","","","","","","","","","","","","","","","","","","","","","",]
                return 0

            for enum, i in enumerate(response.json()["items"]):

                dict_recipe = json.loads(response.json()["items"][enum]["value"])

                self.list_ids.append(dict_recipe["id"])
                self.list_recipes.append(dict_recipe["title"])

        self.menu_calendar = pd.DataFrame()

        for i in range(len(self.menudays)):

            self.list_daily_recipes.append(self.list_recipes[i*3:(i*3)+3])

        for i in range((len(self.menudays)*3)):

            self.list_menu_ids.append(self.list_ids[i])

        for enum, day in enumerate(self.menudays):

            self.menu_calendar[day] = self.list_daily_recipes[enum]

        self.menu_calendar.index = ["Breakfast", "Lunch", "Dinner"]

        return "Calendar menu created!"

    def return_calendar_menu(self):

        return self.menu_calendar

    def display_calendar_menu(self):

        display(self.menu_calendar)

    def return_recipes_ids(self):

        return self.list_ids

######################################################################################################################################

##### Funciones para lista de la compra individualizada ##############################################################################

    def create_shopping_list(self):

        self.list_recipe_info = []

        for id_ in self.list_menu_ids:

            url = f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{id_}/information"

            headers = {
                "X-RapidAPI-Key": rapid_api_key,
                "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
            }

            querystring = {"includeNutrition":"true"}

            response = requests.request("GET", url, headers=headers, params = querystring)
            self.list_recipe_info.append(response.json())
            #time.sleep(1)


        self.list_ingredient_names, self.list_ingredient_amounts, self.list_ingredient_units = [],[],[]
        self.list_nutrient_names, self.list_nutrient_amounts, self.list_nutrient_units, self.list_nutrient_pdn = [],[],[],[]
        self.list_properties_names, self.list_properties_amounts, self.list_properties_units = [],[],[]


        for recipe in self.list_recipe_info:

            for ingredients in recipe["extendedIngredients"]:

                self.list_ingredient_names.append(ingredients["name"])
                self.list_ingredient_amounts.append(ingredients["amount"])
                self.list_ingredient_units.append(ingredients["unit"])

        self.shopping_list = pd.DataFrame()

        self.shopping_list["Ingredient"] = self.list_ingredient_names
        self.shopping_list["Amount"] = self.list_ingredient_amounts
        self.shopping_list["Unit"] = self.list_ingredient_units

        return "Shopping list created!"


    def return_shopping_list(self):

        return self.shopping_list

    def display_shopping_list(self):

        display(self.shopping_list)

    def return_recipe_info(self):

        return self.list_recipe_info


######################################################################################################################################

##### Funciones para mostrar y retornar la preparación de las recetas del menú ##############################################################################

    def return_recipes_instructions(self):

        recipes = {}

        for recipe in self.list_recipe_info:

            recipe_steps = []

            for enum, steps in enumerate(recipe["analyzedInstructions"][0]["steps"]):

                step = steps["step"]

                recipe_steps.append(f"Step {enum+1}: {step}")

                recipes[recipe["title"]] = recipe_steps

        return recipes

    def display_recipes_instructions(self):

        for recipe in self.list_recipe_info:

            print(recipe["title"])
            print("-"*50)

            for enum, steps in enumerate(recipe["analyzedInstructions"][0]["steps"]):

                step = steps["step"]

                print(f"Step {enum+1}: {step}")
                print("-"*50)


######################################################################################################################################

##### Funciones de listas de nutrición individualizadas ##############################################################################

    def create_nutrition_lists(self):

        for recipe in self.list_recipe_info:

            for nutrients in recipe["nutrition"]["nutrients"]:

                self.list_nutrient_names.append(nutrients["name"])
                self.list_nutrient_amounts.append(nutrients["amount"])
                self.list_nutrient_units.append(nutrients["unit"])
                self.list_nutrient_pdn.append(nutrients["percentOfDailyNeeds"])

            for properties in recipe["nutrition"]["properties"]:
                self.list_properties_names.append(properties["name"])
                self.list_properties_amounts.append(properties["amount"])
                self.list_properties_units.append(properties["unit"])

        self.nutrients_list = pd.DataFrame()

        self.nutrients_list["Nutrient"] = self.list_nutrient_names
        self.nutrients_list["Amount"] = self.list_nutrient_amounts
        self.nutrients_list["Unit"] = self.list_nutrient_units
        self.nutrients_list["Percentage of Daily Needs"] = self.list_nutrient_pdn

        self.properties_list = pd.DataFrame()

        self.properties_list["Propertie"] = self.list_properties_names
        self.properties_list["Amount"] = self.list_properties_amounts
        self.properties_list["Unit"] = self.list_properties_units

        return "Nutrition lists created!"

    def return_nutrients_list(self):

        return self.nutrients_list

    def display_nutrients_list(self):

        display(self.nutrients_list)

    def return_properties_list(self):

        return self.properties_list

    def display_properties_list(self):

        display(self.properties_list)

######################################################################################################################################
