import pandas as pd 
import numpy as np 
import plotly.express as px
import streamlit as st 
import altair as alt
import folium
from streamlit_folium import folium_static
from folium.features import GeoJsonPopup, GeoJsonTooltip
import requests
from streamlit_lottie import st_lottie
from PIL import Image

st.set_page_config(
    page_title = "Home Page",
    page_icon = "🏡"
)

# NOTE Allow pictures to be put into the document. 
def load_lottieurl(url):
    """If the lottie file does not display the image return nothing. This will prevent errors when trying to display the Lottie Files.
    Requires importing packages streamlit_lottie and requests"""
    r = requests.get(url)
    if r.status_code != 200:
        return None 
    return r.json()

def lottie_credit(credit):
    return st.markdown(f"<p style='text-align: center; color: gray;'>{credit}</p>", unsafe_allow_html=True)

#NOTE Introduction
st.title("Superstore Project :convenience_store: :moneybag: :credit_card:")
pic1, pic2 = st.columns(2)
with pic1:
    internet = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_sz668bkw.json")
    st_lottie(internet, height = 300, key = "internet_shopping")
    lottie_credit("Image was created by Hadii Hassan LottieFiles.")
with pic2:
    sale = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_vjrlq3tj.json")
    st_lottie(sale, height = 300, key = "sale_shop")
    lottie_credit("Image by: Ifran Munawar 3D on Lottie Files.")

st.write("This project explores a dataset of a superstore. The data has been published on Kaggle by user Vivek Chowdhuey. He credits the Tableau team for the dataset. The dataset has some of the same fields that would be of interest to a large retail corporation.")
st.write("Here is a breakdown of the variables found in this dataset provided by Chowdhuey:")

# expl_1, expl_2 = st.columns(2)


with st.expander("Click to see the explanation of the variables."):
    expl_1, expl_2, expl_3 = st.columns(3)
    with expl_1:
        st.markdown("""
        **Row ID** => Unique ID for each row. \n 
        **Order ID** => Unique Order ID for each Customer. \n 
        **Order Date** => Order Date of the product. \n 
        **Ship Date** => Shipping Date of the Product. \n 
        **Ship Mode** => Shipping Mode specified by the Customer. \n 
        **Customer ID** => Unique ID to identify each Customer. \n 
        **Discount** => Discount provided. \n 
        """)

    with expl_2:
        st.markdown("""
        **State** => State of residence of the Customer. \n 
        **Postal Code** => Postal Code of every Customer. \n 
        **Region** => Region where the Customer belong. \n 
        **Product ID** => Unique ID of the Product. \n 
        **Category** => Category of the product ordered. \n 
        **Sub-Category** => Sub-Category of the product ordered. \n 
        **Profit** => Profit/Loss incurred
        """)
    with expl_3:
        st.markdown("""
        **Customer Name** => Name of the Customer. \n 
        **Segment** => The segment where the Customer belongs. \n 
        **Country** => Country of residence of the Customer. \n 
        **City** => City of residence of of the Customer. \n 
        **Product Name** => Name of the Product \n 
        **Sales** => Sales of the Product. \n 
        **Quantity** => Quantity of the Product. \n 
    """)


# Clean Dataset import 
df = pd.read_csv("superstore_cleaned.csv", encoding = "latin1", parse_dates = ["Order Date", "Ship Date"])

#NOTE Filters 
# Sales 
# Ship Date 
# Discount 
# Days to Ship 
# Profit
# SAVE FOR FILTERS AND IS IN FOR SEPERATE PAGE 

# Make a list from dataset 
# Customer Name 
# City 
# State 
# Postal Code 
# Region
# Category
# Subcategory

class selector:
    def __init__(self, column_name):
        self.listing = df[column_name].unique().tolist()
        self.listing.sort()
        self.checkbox_all = st.checkbox("Select all.")

        if self.checkbox_all:
            self.select = st.multiselect(f"Select values from {column_name} that you wish to select.", self.listing, self.listing)
        else:
            self.select = st.multiselect(f"Select values from {column_name} that you wish to select.", self.listing)
        
        def filters(self):
            st.write("Filter.")
            return print("Hello.") 
            # df[column_name].isin(self.select)
        
    
#NOTE Selectors 


#NOTE GET RID OF THIS LINE OF CODE AFTER THE TEST



def create_map(column_name, key_finish = "", map_tile_type  = "Stamen Terrain", color_fill = "PuRd"):
    m = folium.Map(location = [40, -95], zoom_start = 4, tiles = "Stamen Terrain")
    state_coord_key = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json"
    m = folium.Map(location = [40, -95], zoom_start = 4, tiles = map_tile_type)
    folium.Choropleth(
    geo_data = state_coord_key,
    name = "choropleth", 
    data = df.groupby("State", as_index= False).sum() ,
    columns = ["State", column_name],
    legend_name = f"{column_name} {key_finish}",
    key_on= "feature.properties.name", # Tells how to read the JSON file by using dots.
    highlight = True,
    fill_opacity = 0.7,
    line_opacity = 0.2,
    fill_color= color_fill).add_to(m)

    tabs1, tabs2 = st.tabs(["Map", f"State Table of Values for {column_name}"])
    with tabs1:
        st.header(f"{column_name} US Map")
        folium_static(m)
    
    with tabs2:
        summation = df.groupby("State", as_index= False).sum()
        summation.sort_values("State")
        st.write("Even floats are shown as integers")
        summation[column_name] = summation[column_name].astype(int).map('{:,d}'.format)
        st.write(summation[["State" ,column_name]])

df

map = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_svy4ivvy.json")
st_lottie(map, height = 300, key = "mapping")
lottie_credit("Image created by Anna Molchanova on Lottiefiles.")


with st.expander("Click to View the Map Section"):
    create_map("Sales", "in Dollars ($)",  map_tile_type= "OpenStreetMap")
    create_map("Profit", "in Dollars ($)",  map_tile_type= "OpenStreetMap")
    create_map("Quantity", "in Units Sold", map_tile_type= "OpenStreetMap",color_fill = "OrRd")
    create_map("Discount", "in Decimal Form (not percentage)", map_tile_type= "OpenStreetMap",color_fill = "OrRd")



def line_chart(metric, color = "red"):
    """Order date must be hard coded to have the chart present pro"""
    line = px.line(df.sort_values(by = "Order Date"), x = "Order Date", y = metric, markers = True, width = 1000, height = 500, color_discrete_sequence = [color],
    title = f"{metric} by Order Date")
    line.update_traces(marker=dict(size=2, line=dict(width=1, color= "rgba(248, 240, 187, 0.7)")) )
    st.plotly_chart(line)




def box_whisk(y, color = None , color_split = None, outliers = False):
    """Creates box and whiskers. Color splits seperates by distinct entities such as states. Color discrete is a general color."""
    y = y.title()
    boxw = px.box(df, y = y, title = f"{y} Box and Whiskers Chart", color_discrete_sequence = [color], color = color_split)
    boxw.update_traces(boxpoints = outliers)
    

    if outliers != False:
        boxw.update_layout(title = f"{y} Box and Whiskers Chart With OUTLIERS")



    description = df[f"{y}"].describe()

    #Have tabs nested in expanders. 

    tab1, tab2 = st.tabs(["Boxplot", f"{y} Summary Statistics/Description"])

    with tab1:
        st.plotly_chart(boxw)
    with tab2:
        st.write(description)
        st.warning("Shows the aggregate description even when several boxplots are shown.")
        st.write("Must filter the data precisely to get an accurate description.")
        



# NOTE Create pie charts.
def pie_chart(column_name):
    """Creates a pie chart and an accompanying table."""
    fig =  px.pie(df, values = df[f"{column_name}"].value_counts().values, names = df[f"{column_name}"].value_counts().index )
    

    table =  df[f"{column_name}"].value_counts()

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"Count Chart of {column_name}")
        st.write(table)
        
    with col2:
        st.write(f"Pie Chart of {column_name}")
        st.plotly_chart(fig)





bp_names = ["Boxplots", "Boxplots By Region", "Boxplots By State", "Boxplots By City"]
areas = ["Region", "City", "State"]
measures = ["Sales", "Profit", "Quantity", "Discount"]


# NOTE Box and Whiskers implementation Section 
tab_box1, tab_box2, tab_box3, tab_box4 = st.tabs(bp_names)


plot_box = Image.open("box-plot-chart.png")
st.image(plot_box, caption = "Image created by IconScout.", width = 200)

with tab_box1:
    with st.expander(f"Click to see the {bp_names[0]}"):
        box_whisk("Sales", "#DE7A7A") #Color: Granny Smith Apple changed to red 
        box_whisk("Sales", "#DE7A7A", outliers = "outliers")
        box_whisk("Profit", "#92C76E") #Color: Pistachio
        box_whisk("Profit", "#92C76E", outliers= "outliers")
        box_whisk("Quantity", "#DFAA7B")
        box_whisk("Quantity", "#DFAA7B", outliers= "outliers")
        box_whisk("Discount", "#EEE590")
        box_whisk("Discount", "#EEE590", outliers= "outliers")

with tab_box2:
    with st.expander(f"Click to see the {bp_names[1]}"):
        for i in measures:
            box_whisk(i, color_split= "Region")
            box_whisk(i, color_split= "Region", outliers = "outliers")
            

with tab_box3:
    with st.expander(f"Click to see the {bp_names[2]}"):
        for i in measures:
            box_whisk(i, color_split = "State")
            box_whisk(i, color_split = "State", outliers = "outliers")
            
            

with tab_box4:
    with st.expander(f"Click to see the {bp_names[3]}"):
        for i in measures:
            box_whisk(i, color_split= "City")
            box_whisk(i, color_split= "City", outliers = "outliers")

with st.expander("Click Here to See Time Series of Metrics"):
    st.info("Each translucent yellow dot represents an instance a measure was recorded.")
    line_chart("Sales", "pink")  
    line_chart("Profit", "#ABDA95")
    line_chart("Quantity", "#AFD2E9")
    line_chart("Discount", "#553555")



# NOTE Pie Charts Being Graphed. Showing the chart in collaspeable format.  
with st.expander("Click to see the Pie Charts."):
    pie_chart("Region")
    pie_chart("Category")
    pie_chart("Sub-Category")
    pie_chart("Segment")
    pie_chart("Ship Mode")
    pie_chart("Country")
    pie_chart("State")
    pie_chart("City")
    pie_chart("Product Name")



#NOTE New and Improved 
def bar_chart(x, y):
    """Group by the the X value and computes the sum by it by the aggregate. 
    Reset the index. Then sort it by the index."""
    df_fixed = df.groupby(f"{x}").agg("sum").reset_index().sort_values( f"{y}",ascending= False)
    fig = px.bar(df_fixed, x = x , y = y, color = x, width = 1000, height  = 500,  text_auto = True, title = f"{y} by {x} Bar Charts")
    yaxis = {f"{y}" : "total descending" }
    st.plotly_chart(fig)

# NOTE Metrics By State
with st.expander("Click to see Bar Charts of Metrics By State"):
    bar_chart("State", "Sales")
    bar_chart("State", "Quantity")
    bar_chart("State", "Discount")
    bar_chart("State", "Profit")

# NOTE Metrics By City 
with st.expander("Click to see metrics by city."):
    bar_chart("City", "Sales")
    bar_chart("City", "Quantity")
    bar_chart("City", "Discount")
    bar_chart("City", "Profit")

def orders(order_column):
    """Creates a bar chart that tracks the orders throughout the week. Made for the order day and ship day columns only."""
    order =px.bar(df[f"{order_column}"].value_counts(), y = order_column ,color = order_column, title = f"{order_column} Bar Chart",
    category_orders = {"index" : ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]}, 
    labels = {order_column :"Count of Orders","index" : "Day of Week"}, color_continuous_scale= px.colors.sequential.Darkmint)
    return st.plotly_chart(order)

def histo(column, color = "blue"):
    hist = px.histogram(df, x = column , text_auto =  True, color_discrete_sequence = [color], title = f"{column} Histogram")
    st.plotly_chart(hist)

def histo_bins(column, color = "blue", numbins = 50, xbins = False, width = 1000):
    """Can define the number of bins directly or by using the size."""
    hist = px.histogram(df, x = column , text_auto =  True, color_discrete_sequence = [color], nbins = numbins, title = f"{column} Histogram")

    if xbins != False:
        hist.update_traces(xbins_size= xbins)

    st.plotly_chart(hist)


# NOTE Histogram for Order Turnaround and Sundry Shipping Information


with st.expander("Click to See Order and Shipping Visuals"):
    histo("Days to Ship", "#FFBFB8")
    st.markdown("<p style='text-align: center; color: gray;'>Note that 0  days to ship means that is was shipped on the same day.</p>", unsafe_allow_html=True)

    orders("Order Day of Week")
    orders("Ship Day of Week")


# NOTE Various Histograms Section 

with st.expander("Click here to see histograms."):
    histo_bins("Sales", "#e9edc9" ,xbins = 250)
    st.markdown("<p style='text-align: center; color: gray;'>Note that all of the sales are positive values. The smallest sale was about $0.44 cents.</p>", unsafe_allow_html=True)
    histo_bins("Profit", "#588157" ,xbins = 250)
    histo("Quantity", "#ffc300")
    histo("Discount", "#ffddd2")
# order_day =px.bar(df["Order Day of Week"].value_counts(), y = "Order Day of Week" ,color = "Order Day of Week", category_orders = {"index" : ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]})
# st.plotly_chart(order_day)


shopper = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_txqfn27k.json")
st_lottie(shopper, height = 400, key = "shopper")
lottie_credit("Created by Aexr Infotech, lottie files.")


