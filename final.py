'''
Name: Kyle Gendreau
CS230: Section 02
Data: Cannabis Registry
URL: Link to your web application on Streamlit Cloud (if posted)

Description:
This program analyzes different parts of a Cannabis Registry file and presents different parts of the data in interactive
ways. One requirement was to create a map that shows all locations of registries in MA, which is shown and allows the user
to hover their cursor over the locations to get more information on them. There is also a dropdown in the sidebar that
lets the user choose a license category to see the total amount of them, as well as get a breakdown of it on the pie chart.
There are radio buttons as well to let users interact with one bar chart, and there is another bar chart to provide other
basic information.
'''

import streamlit as st
import pandas as pd
from PIL import Image
import pydeck as pdk
import matplotlib.pyplot as plt
import altair as alt

#Creating headers and adding an image
st.title("CS230 Final Project - Kyle Gendreau")
st.header("Massachusetts Cannabis Registries")
img = Image.open("projects/maweed.jpeg")
st.image(img, width=500)


#Find number of registries with each kind of license
def app_license_status():
    df = read_csv("Cannabis_Registry.csv")
    value_counts = df["app_license_status"].value_counts()  #Counting each kind of license status
    inactive_licenses_count = value_counts.get("Inactive")
    active_licenses_count = value_counts.get("Active")
    expired_licenses_count = value_counts.get("Expired")
    deleted_licenses_count = value_counts.get("Deleted")
    return inactive_licenses_count, active_licenses_count, expired_licenses_count, deleted_licenses_count


#Create a bar chart with number of registries and each kind of license status
def status_bar_chart(categories):
    licenses = ["Inactive", "Active", "Expired", "Deleted"]
    license = st.radio("Select a license status:", licenses)  #Have radio buttons for a better UI
    if license == "Inactive":
        st.write("There are " + str(categories[0]) + " cannabis registries in Boston that have inactive licenses.")
    elif license == "Active":
        st.write("There are " + str(categories[1]) + " cannabis registries in Boston that have active licenses.")
    elif license == "Expired":
        st.write("There are " + str(categories[2]) + " cannabis registries in Boston that have expired licenses.")
    elif license == "Deleted":
        st.write("There is " + str(categories[3]) + " cannabis registry in Boston that has a deleted license.")

    #A dictionary for license status (key) and counts (values)
    app_license_dictionary = {licenses[i]: categories[i] for i in range(len(licenses))}
    data = {"License Status": list(app_license_dictionary.keys()),
            "Amount of Licenses": list(app_license_dictionary.values())}
    df = pd.DataFrame(data)
    bar_chart = (alt.Chart(df, title="License Status and Amounts")
                 .mark_bar(color="darkgreen")  #Making bars on chart dark green
                 .encode(x="License Status", y="Amount of Licenses")  #Giving axis' names
                 .properties(width=600))  #Setting the right width
    st.altair_chart(bar_chart.configure_title(fontSize=20, anchor="middle")) #Set font size and position chart
    #https://altair-viz.github.io/user_guide/generated/toplevel/altair.Chart.html
    #https://docs.streamlit.io/library/api-reference/charts/st.altair_chart


#Creating a map of all registries in MA (watched Sandbox video on how to do this)
def generate_map():
    st.header("Cannabis Registries in Massachusetts")
    df = read_csv("Cannabis_Registry.csv")
    columns = ["app_business_name", "facility_address", "facility_zip_code", "latitude", "longitude"]
    dfLatlong = df.loc[:, columns] #Select every row from the column
    dfLatlong = dfLatlong.dropna(subset=columns)  #Remove null value columns
    view_Cannabis = pdk.ViewState(
        latitude=dfLatlong["latitude"].mean(),
        longitude=dfLatlong["longitude"].mean(),
        zoom=11,  #Zoom level of map
        pitch=0)  #Tilt of map view
    layer1 = pdk.Layer('ScatterplotLayer',
                       data=dfLatlong,
                       get_position='[longitude, latitude]',
                       get_radius=75,
                       get_color=[0, 153, 0],  #Have green circles where the dispensaries are, because, weed
                       pickable=True  #Putting cursor over the dot will provide some information
                       )
    #Information shown when cursor is over dot
    tool_tip = {"html": "<b>Registry Name:<br/> <b>{app_business_name}</b> <br/> "
                        "Registry Address: <br/> {facility_address},<br/>Zip Code: 0{facility_zip_code}",
                "style": {"backgroundColor": "forestgreen",
                          "color": "white"}
                }
    map = pdk.Deck(
        map_style='mapbox://styles/mapbox/outdoors-v11',  #Style of the map from mapbox
        initial_view_state=view_Cannabis,
        layers=layer1,
        tooltip=tool_tip
    )

    st.pydeck_chart(map)  #Display the map


#Count values of each different license category
def app_license_category():
    df = read_csv("Cannabis_Registry.csv")
    column = "app_license_category"
    df = df.drop(98)  #Drop row with null values for cleaner data
    value_counts = df[column].value_counts()  #Counts of all unique values
    retail_licenses_count = value_counts.get("Retail")
    cultivate_licenses_count = value_counts.get("Cultivate")
    manufact_licenses_count = value_counts.get("Manufact")
    colocated_licenses_count = value_counts.get("Co-Located")
    courier_licenses_count = value_counts.get("Courier")
    operator_licenses_count = value_counts.get("Operator")
    testlab_licenses_count = value_counts.get("TestLab")
    transport_licenses_count = value_counts.get("Transport")
    medical_licenses_count = value_counts.get("Medical")

    return (retail_licenses_count, cultivate_licenses_count,  manufact_licenses_count, colocated_licenses_count,
            courier_licenses_count, operator_licenses_count, testlab_licenses_count, transport_licenses_count,
            medical_licenses_count) #Returns each of the different kinds of categories


#Create a pie chart based on user selection (dropdown)
def generate_pie_chart(categories):
    st.sidebar.title("Pie Chart Category Selection")
    columns = ["Retail", "Cultivate", "Manufact", "Co-Located", "Courier", "Operator", "Testlab", "Transport",
               "Medical"]
    df = pd.DataFrame({"License Category": columns, "Values": categories})
    app_license_category = st.sidebar.selectbox("Select a license category:", columns)
    if app_license_category == "Retail":
        st.sidebar.write("There are " + str(categories[0]) + " cannabis registries in Boston that have retail "
                                                             "licenses.")
    elif app_license_category == "Courier":
        st.sidebar.write("There are " + str(categories[1]) + " cannabis registries in Boston that have courier "
                                                             "licenses.")
    elif app_license_category == "Co-Located":
        st.sidebar.write("There are " + str(categories[2]) + " cannabis registries in Boston that have co-located "
                                                             "licenses.")
    elif app_license_category == "Operator":
        st.sidebar.write("There are " + str(categories[3]) + " cannabis registries in Boston that have operator "
                                                             "licenses.")
    elif app_license_category == "TestLab":
        st.sidebar.write("There is " + str(categories[4]) + " cannabis registry in Boston that has a testlab "
                                                            "license.")
    elif app_license_category == "Manufact":
        st.sidebar.write("There are " + str(categories[5]) + " cannabis registries in Boston that have manufact "
                                                             "licenses.")
    elif app_license_category == "Transport":
        st.sidebar.write("There is " + str(categories[6]) + " cannabis registry in Boston that has a transport "
                                                            "license.")
    elif app_license_category == "Cultivate":
        st.sidebar.write("There are " + str(categories[7]) + " cannabis registries in Boston that have cultivate "
                                                             "licenses.")
    elif app_license_category == "Medical":
        st.sidebar.write("There are " + str(categories[8]) + " cannabis registries in Boston that have medical "
                                                             "licenses.")
    st.header("License Category Pie Chart Breakdown")
    explode = [0] * len(df)
    for i in range(len(columns)):
        if app_license_category == columns[i]:
            explode[i] = 0.5
    plt.pie(df["Values"],  #Slice of pie will depend on the size of the value
            labels=df["License Category"],  #Each category has its own slice
            explode=explode)  #User selected option will explode on chart
    st.pyplot(plt)


#Reading the CSV file
def read_csv(data):
    df = pd.read_csv(data)
    return df


#Counting registries applying for Boston Equity Program (BEP)
def equity_program_designation():
    df = read_csv("Cannabis_Registry.csv")
    value_counts = df["equity_program_designation"].value_counts()
    no_count = value_counts.get("N")
    yes_count = value_counts.get("Y")
    null_count = len(df) - (no_count + yes_count)  #Not counting null values
    return yes_count, no_count, null_count


#Bar graph of registries that applied for the BEP
def bar_graph_bep(categories):
    designation = ["Yes", "No", "Not Applicable"]
    equity_program_dictionary = {designation[i]: categories[i] for i in range(len(designation))}
    data = {"Is Registry Applying for BEP?": list(equity_program_dictionary.keys()),
            "Number of Registries": list(equity_program_dictionary.values())}
    df = pd.DataFrame(data)
    st.header("The Boston Equity Program")
    bar_chart = (alt.Chart(df, title="Number of Registries Seeking Boston Equity Program")
                 .mark_bar(color="seagreen")  #Make bars green color
                 .encode(x="Is Registry Applying for BEP?", y="Number of Registries") #Naming axis'
                 .properties(width=600))  #Making width 600
    st.altair_chart(bar_chart.configure_title(fontSize=20, anchor="middle")) #Setting font size and adjusting position
    #https://altair-viz.github.io/user_guide/generated/toplevel/altair.Chart.html
    #https://docs.streamlit.io/library/api-reference/charts/st.altair_chart

def main():
    generate_pie_chart(app_license_category())
    status_bar_chart(app_license_status())
    bar_graph_bep(equity_program_designation())
    generate_map()


main()