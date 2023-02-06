import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import numpy as np
from pyairtable_funcs import *
from PIL import Image

##### Analyzed plots #############################################################################################################

def return_pie_diets(api_key,base_id,table_name):

    clients = extract_all_clients_from_airtable(api_key, base_id, table_name)

    list_diets=[]

    for diets in clients:

        list_diets.append(diets[4]) #Diets[4] contiene el tipo de dieta de este cliente

    df_diets=pd.DataFrame(list_diets)

    df_diets[0].replace(" ","No diet",inplace=True)

    df_diets = df_diets[0].value_counts()
    df_diets = df_diets.reset_index()
    df_diets.columns=["Diet","Quantity"]

    fig = plt.figure(figsize = (4, 4))
    fig.set_facecolor('#0E1117')

    plt.pie(x         = df_diets["Quantity"],
            explode   = (0.1, 0.1, 0.1, 0.1),
            labels    = df_diets["Diet"].values,
            shadow    = True,
            autopct   = "%1.1f%%",
            textprops = {'color':"w"},
            colors    = ["lightgreen", "cyan", "green","orange"])

    return fig

def return_wordcloud_graph(shopping_list):


    text=" ".join(shopping_list["Ingredient"])

    wordcloud_png = np.array(Image.open("corteLogo.png"))
    wordcloud_png.shape


    # Creamos de nuevo el objeto agregando la mascara
    fig = plt.figure(figsize=(5,5))
    fig.set_facecolor('#0E1117')

    wordcloud_obj = WordCloud(background_color = "#0E1117",
                              max_words        = 2000,
                              mask             = wordcloud_png,
                              contour_width    = 2,
                              contour_color    = "white").generate(text)

    plt.imshow(wordcloud_obj, interpolation = "bilinear")
    plt.axis("off")

    return fig

def return_sunburst_graph(nutrients_list):

    df_sunburst = nutrients_list

    df_sunburst = df_sunburst[df_sunburst['Amount']!=0]

    df_sunburst = df_sunburst.groupby(["Nutrient","Unit"]).agg({"Amount":"mean","Percentage of Daily Needs":"mean"})

    df_sunburst = df_sunburst.reset_index()

    fig = px.sunburst(data_frame             = df_sunburst,
                      values                 = "Percentage of Daily Needs",
                      hover_name             = "Amount",
                      color                  = "Percentage of Daily Needs",
                      path                   = ["Nutrient"],
                      color_continuous_scale = 'RdBu')

    return fig

def return_macronutrients_graph(nutrients_list):

    df_bar = nutrients_list

    df_bar = df_bar.groupby(["Nutrient","Unit"]).agg({"Amount":"mean","Percentage of Daily Needs":"mean"})

    df_bar = df_bar.reset_index()

    df_bar_macro = df_bar.loc[df_bar["Nutrient"].isin(("Fat","Carbohydrates","Net Carbohydrates","Sugar","Protein"))]

    df_bar_macro.columns = ["Nutrient","Nutrients","Amount","Percentage of Daily Needs"]

    df_bar_macro["Nutrients"] = ""


    fig = plt.figure(figsize = (10,10))

    sns.barplot(x = "Percentage of Daily Needs", y = "Nutrients", hue = "Nutrient", data = df_bar_macro, palette = "rainbow")

    return fig

def return_micronutrients_graph(nutrients_list):

    df_bar = nutrients_list

    df_bar = df_bar.groupby(["Nutrient","Unit"]).agg({"Amount":"mean","Percentage of Daily Needs":"mean"})

    df_bar = df_bar.reset_index()

    df_bar_micro = df_bar.loc[~df_bar["Nutrient"].isin(("Fat","Carbohydrates","Net Carbohydrates","Sugar","Protein"))]

    df_bar_micro.columns=["Nutrient","Nutrients","Amount","Percentage of Daily Needs"]

    df_bar_micro["Nutrients"]=""

    fig = plt.figure(figsize = (10,10))

    sns.barplot(x = "Percentage of Daily Needs", y = "Nutrients", hue = "Nutrient", data = df_bar_micro, palette = "rainbow")


    return fig
