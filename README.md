# Getting Started

## Libraries used in mealplans.py

```python
import numpy as np
import pandas as pd
import streamlit as st
from analyzed_plots import *
from pyairtable_funcs import *
from class_client import *
from creds import *

```

## Libraries used in analyzed_plots.py
```python
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import numpy as np
from pyairtable_funcs import *
from PIL import Image
```
## Libraries used in pyairtable_funcs.py

```python
from pyairtable import Table
import ast
import numpy as np
```

## Libraries used in class_client.py

```python
import requests
import json
import pandas as pd
from IPython.display import display
from creds import *
```

## Project API-keys

The API-Keys used are private and belong to `Airtable` and `Spoonacular`. To use them, you will need to create a `creds.py` with the following code:

```python
api_key = #YOUR-API-KEY
base_id = #YOUR-BASE-ID
table_name = #YOUR-TABLE-NAME
rapid_api_key = #YOUR-RAPID-API-KEY
```

You can obtain [here](https://rapidapi.com/spoonacular/api/recipe-food-nutrition/) your `rapid_api_key`, and your `Airtable` needs are specified below, under the *Airtable functions* title.

# Main class: client

This is made to create instances of a client, with the attributes required to make for him:

- Calendar menu.
- Shopping list.
- Nutrition lists.

## __init__()

```python
def __init__(self,name,surname,kcal,menudays,diet, exclude, address, client_id):

```

- Name: *String* with the name of our client
- Surname: *String* with the surname of our client
- Kcal: *String* with the desired calories for each day of the menu
- Menudays: *List of strings* with the days that the client wants to receive menu
- Diet: *String* with the dietary restrictions of our client. In case it has none, the string should be “ “
- Exclude: *String* with the ingredients the client wants to exclude from the diet, separated with *commas.* As with diet, if none, enter a *space*.
- Address: *String* with the address of the client.
- Client_id: *String* with our client ID. *Optional*. This is used in case that we want to upload our client to Airtable. In that case, the ID should be obtained based on the current maximum ID in the clients database.

Example:

```python

myclient = client("Jacob","Bamio","2000",["Monday","Tuesday","Wednesday","Thursday","Friday"],"vegan","peanuts, raisins","Somewhere","159")

```

## display_info()

Prints our client info (without the ID), and returns a list with each attribute.

```python
myclient.display_info()

```

## edit_name()

Replaces the client name with the one provided, and prints the change you’ve made.

```python
myclient.edit_name("Jake")

```

## edit_surname()

Replaces the client surname with the one provided, and prints the change you’ve made.

```python
myclient.edit_surname("Bam")

```

## edit_menudays()

Replaces the client menu days of the week with the ones provided, and prints the change you’ve made.

```python
myclient.edit_menudays(["Friday","Saturday","Sunday"])

```

## edit_diet()

Replaces the client dietary restriction with the one provided, and prints the change you’ve made.

```python
myclient.edit_diet("vegetarian")

```

## edit_exclude()

Replaces the client excluded ingredients with the one-s provided, and prints the change you’ve made.

```python
myclient.edit_exclude("chicken, meat")

```

## edit_address()

Replaces the client address with the one provided, and prints the change you’ve made.

```python
myclient.edit_address("Somewhere 2")

```

## create_calendar_menu()

Makes a `request` to Spoonacular API and creates a `dataframe` with `[“Breakfast", "Lunch","Dinner”]` as index, and the `menudays` of this client as columns.

When it’s done, it prints `“Calendar menu created!”`.

```python
myclient.create_calendar_menu()

```

## return_calendar_menu()

Returns the `dataframe` created in `create_calendar_menu()`.

```python
myclient.return_calendar_menu()

```

## display_calendar_menu()

Displays the `dataframe` created in `create_calendar_menu()`.

```python
myclient.display_calendar_menu()

```

## return_recipes_ids()

Returns a `list of strings` with the `ids` of each recipe in the calendar menu.

```python
myclient.return_recipes_ids()

```

## create_shopping_list()

Makes a `request` to *Spoonacular API* and creates a `list` with the information of each recipe in the menu.

After, it loops over the `list` to create:

- *List* with the ingredient names of every recipe.
- *List* with the ingredient amounts of every recipe.
- *List* with the ingredient units of every recipe.

In the end, creates a `dataframe` with `lists` as columns, and prints `“Shopping list created!”`.

```python
myclient.create_shopping_list()

```
## return_shopping_list()

Returns the `dataframe` created in `create_shopping_list()`.

```python
myclient.return_shopping_list()

```

## display_shopping_list()

Displays the `dataframe` created in `create_shopping_list()`.

```python
myclient.display_shopping_list()

```

## return_recipe_info()

Returns the `list` with all the recipes info.

```python
myclient.return_recipe_info()

```

## return_recipes_instructions()

Returns a `dictionary` with recipes as `keys` and a `list of strings` with each step for the recipe.

```python
myclient.return_recipes_instructions()

```

## display_recipes_instructions()

Prints each step of every recipe in the created menu.

```python
myclient.display_recipes_instructions()

```

## create_nutrition_lists()

Creates the following *lists* and *dataframes*:

- *Lists*:
    - Nutrient names.
    - Nutrient amounts.
    - Nutrient units.
    - Nutrient PDN (Percentage of Daily Needs).
    - Properties names.
    - Properties amounts.
    - Properties units.
- *Dataframes*:
    - Nutrients.
    - Properties.

When it finishes, prints: `“Nutrition lists created!”`.

## return_nutrients_list()

Returns nutrients `dataframe` created in `create_nutrition_lists()`

```python
myclient.return_nutrients_list()

```

## display_nutrients_list()

Displays nutrients `dataframe` created in `create_nutrition_lists()`

```python
myclient.display_nutrients_list()

```

## return_properties_list()

Returns properties `dataframe` created in `create_nutrition_lists()`

```python
myclient.return_properties_list()

```

## display_properties_list()

Displays properties `dataframe` created in `create_nutrition_lists()`

```python
myclient.return_nutrients_list()

```

# Airtable functions

These are made to interact with the Airtable clients database, using [pyairtable](https://pyairtable.readthedocs.io/).

The structure of the database model for this app looks like this:

| Name | Surname | Calories | Days of the menu | Diet | Excluded ingredients | Address | ID |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|  STR  |  STR  |  STR  |  STR  |  STR  |  STR  |  STR  |  STR  |

## load_list_of_clients_to_airtable()

Loads a `list` of clients to Airtable

```python
clients = [

["Jake","Bam","2000",["Monday","Tuesday","Wednesday","Thursday","Friday"],"vegan","peanuts, raisins","Somewhere 1","159"],
["Jacob","Bamio","2500",["Monday","Tuesday","Wednesday","Thursday","Friday"]," ","raisins","Somewhere 2","160"]

]

load_list_of_clients_to_airtable(clients,api_key, base_id, table_name):

```

## load_client_to_airtable()

Loads one client to Airtable.

```python

myclient = ["Jacob","Bamio","2000",["Monday","Tuesday","Wednesday","Thursday","Friday"],"vegan","peanuts, raisins","Somewhere in Madrid","159"]

load_client_to_airtable(myclient,api_key, base_id, table_name)

```

## extract_all_clients_from_airtable()

Returns a `list` with all the clients in the Airtable database.

```python

airtable_clients = extract_all_clients_from_airtable(api_key, base_id, table_name)

```

## extract_client_from_airtable()

Returns the client from Airtable that matches the `client_id` passed to the function.

```python

myclient = extract_client_from_airtable("159",api_key, base_id, table_name)

```

## return_max_id()

Returns the higher ID in the entire Airtable database, in order to give the next to a new client.

```python

max_id = return_max_id(api_key, base_id, table_name)

```

## delete_all_records()

Deletes all the records in the Airtable database. Just used in case it’s needed for any test.

```python

delete_all_records(api_key, base_id, table_name)

```

# Analyzed plots functions

These are made show our client interesting data allocated in the app.

## return_pie_diets()

Returns a `figure` with a comparative between the dietary restrictions of our clients, made with `matplotlib`.

```python

fig = return_pie_diets(api_key,base_id,table_name)

```

## return_wordcloud_graph()

Returns a `figure` with a `wordcloud` that shows the main ingredients in our client menu. It requires a `shopping list` to extract the ingredients, that can be obtained with `return_shopping_list()`.

```python

fig = return_wordcloud_graph(myclient.return_shopping_list())

```

## return_sunburst_graph()

Returns a `figure` with a `sunburst` from `plotly` that shows the mean PDN of the nutrients in our client menu. It requires a `nutrients list` to extract the values, that can be obtained with `return_nutrients_list()`.

```python

fig = return_sunburst_graph(myclient.return_nutrients_list())

```

## return_macronutrients_graph()

Returns a `figure` with a `seaborn bar plot` that shows the mean PDN of the macronutrients in our client menu. It requires a `nutrients list` to extract the values, that can be obtained with `return_nutrients_list()`.

```python

fig = return_macronutrients_graph(myclient.return_nutrients_list())

```

## return_micronutrients_graph()

Returns a `figure` with a `seaborn bar plot` that shows the mean PDN of the micronutrients in our client menu. It requires a `nutrients list` to extract the values, that can be obtained with `return_nutrients_list()`.

```python

fig = return_micronutrients_graph(myclient.return_nutrients_list())

```
