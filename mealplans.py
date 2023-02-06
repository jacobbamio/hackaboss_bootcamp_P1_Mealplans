import numpy as np
import pandas as pd
import streamlit as st
from analyzed_plots import *
from pyairtable_funcs import *
from class_client import *
from creds import *

st.set_page_config(page_title="Mealplan", page_icon="🥑", layout= "wide")

newclient_id = 0

sb_user_input_pressed = False

tab_user_input, tab_calendar_menu, tab_shopping_list, tab_meal_prep, tab_analysis = st.tabs(["Introduce your menu requisites!",
                                                                                             "My calendar menu",
                                                                                             "My shopping list",
                                                                                             "Steps to cook my meals",
                                                                                             "Graphs about your diet compared!"])
col_text_inputs, col_day_checks, col_diet_rad_buttons = tab_user_input.columns(3)
with tab_user_input:

    with col_text_inputs:

        ti_name                 = st.text_input("Name", "John")
        ti_surname              = st.text_input("Surname", "Davis")
        ti_kcal                 = st.text_input("Calories of your desired menu", "2000")
        ti_excluded_ingredients = st.text_input("Tell us what ingredients you hate!", "raisins, pumpkin")
        ti_address              = st.text_input("Your address (just for sending you the ingredients)", "C. de Campoamor, 13, 28004 Madrid, Spain")

    with col_day_checks:

        st.caption("Choose the days in which you want to receive this menu:")

        check_monday    = st.checkbox("Monday",help="Check this if you want to have menu on Monday")
        check_tuesday   = st.checkbox("Tuesday",help="Check this if you want to have menu on Tuesday")
        check_wednesday = st.checkbox("Wednesday",help="Check this if you want to have menu on Wednesday")
        check_thursday  = st.checkbox("Thursday",help="Check this if you want to have menu on Thursday")
        check_friday    = st.checkbox("Friday",help="Check this if you want to have menu on Friday")
        check_saturday  = st.checkbox("Saturday",help="Check this if you want to have menu on Saturday")
        check_sunday    = st.checkbox("Sunday",help="Check this if you want to have menu on Sunday")

    with col_diet_rad_buttons:

        rb_diet = st.radio("Input your dietary restrictions:",("Vegan","Vegetarian","Paleo","None, just surprise me!"))

    sb_user_input = st.button("I'm done! Create my menu!")

    if sb_user_input:

        sb_user_input_pressed = True

        list_menudays = []

        if check_monday:

            list_menudays.append("Monday")

        if check_tuesday:

            list_menudays.append("Tuesday")

        if check_wednesday:

            list_menudays.append("Wednesday")

        if check_thursday:

            list_menudays.append("Thursday")

        if check_friday:

            list_menudays.append("Friday")

        if check_saturday:

            list_menudays.append("Saturday")

        if check_sunday:

            list_menudays.append("Sunday")

        if rb_diet == "Vegan":

            client_diet = "vegan"

        elif rb_diet == "Vegetarian":

            client_diet = "vegetarian"

        elif rb_diet == "Paleo":

            client_diet = "paleo"

        elif rb_diet == "None, just surprise me!":

            client_diet = " "

        if ti_excluded_ingredients == "":

            ti_excluded_ingredients = " "

        #Obtenemos el id más alto que ya está en la tabla de Airtable, y le damos el siguiente al nuevo cliente

        newclient_id = str(return_max_id(api_key,base_id,table_name) + 1)

        #Creamos un nuevo cliente con toda la información introducida en los formularios
        newclient = [ti_name,ti_surname,ti_kcal,list_menudays,client_diet,ti_excluded_ingredients,ti_address,newclient_id]

        load_client_to_airtable(newclient,api_key,base_id,table_name)

with tab_calendar_menu:

    if sb_user_input_pressed == True:

        myclient_id = newclient_id

        extracted_client = extract_client_from_airtable(myclient_id,api_key,base_id,table_name)

        myclient = client(extracted_client[0],extracted_client[1],extracted_client[2],extracted_client[3],extracted_client[4],extracted_client[5],extracted_client[6],extracted_client[7])
        result_calendar_menu = myclient.create_calendar_menu()

        if result_calendar_menu == 0:

            st.write("Sorry, we can't create a calendar menu for your requisites. Try changing excluded ingredients.")

        else:

            st.header("This is the calendar menu we have created for you!")
            df_calendar = myclient.return_calendar_menu()
            st.dataframe(df_calendar)


with tab_shopping_list:

    if (sb_user_input_pressed == True) and (result_calendar_menu != 0):

        myclient.create_shopping_list()
        df_shopping_list = myclient.return_shopping_list()

        st.dataframe(df_shopping_list)

    elif (sb_user_input_pressed == True) and (result_calendar_menu == 0):

        st.write("Sorry, we can't create a calendar menu for your requisites. Try changing excluded ingredients.")

with tab_meal_prep:

    if (sb_user_input_pressed == True) and (result_calendar_menu != 0):

        myclient_recipes = myclient.return_recipes_instructions()

        expanders = {recipe : st.expander(recipe) for enum, recipe in enumerate(myclient_recipes.keys())}

        for expander, steps in zip(expanders.values(),myclient_recipes.values()):

            for step in steps:

                expander.write(step)

    elif (sb_user_input_pressed == True) and (result_calendar_menu == 0):

        st.write("Sorry, we can't create a calendar menu for your requisites. Try changing excluded ingredients.")


with tab_analysis:

    m1,m2,m3,m4 = tab_analysis.container(),tab_analysis.container(),tab_analysis.container(),tab_analysis.container()
    l1,r1 = m2.columns(2)
    l2,r2 = m4.columns(2)


    if (sb_user_input_pressed == True) and (result_calendar_menu != 0):

        myclient.create_nutrition_lists()

        with m1:

            st.header("These are all the nutrients in your diet!")

            st.subheader("In the following graphs you can see the average PDN of the ingredients in your diet")
            st.subheader("Global, sunburst style")
            st.plotly_chart(return_sunburst_graph(myclient.return_nutrients_list()), theme="streamlit", use_container_width=True)

        with l1:

            st.subheader("Micronutrients")
            st.pyplot(return_micronutrients_graph(myclient.return_nutrients_list()))

        with r1:

            st.subheader("Macronutrients")
            st.pyplot(return_macronutrients_graph(myclient.return_nutrients_list()))

        with m3:

            st.header("Some cool graphs now!")

        with l2:

            st.subheader("Main ingredients in your recipes!")
            st.pyplot(return_wordcloud_graph(myclient.return_shopping_list()))

        with r2:

            st.subheader("Our clients most popular diets!")
            st.pyplot(return_pie_diets(api_key,base_id,table_name))

    elif (sb_user_input_pressed == True) and (result_calendar_menu == 0):

        st.write("Sorry, we can't create a calendar menu for your requisites. Try changing excluded ingredients.")
