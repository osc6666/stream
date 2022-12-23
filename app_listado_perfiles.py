

import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit


st.set_page_config(page_title="Profiles Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache
def get_data_from_excel():    
    df = pd.read_excel(
        io="listado_perfiles.xlsx",
        engine="openpyxl",
        sheet_name="Partidas",
        skiprows=0,
        usecols="A:P",
        nrows=1360,
        )
    return df

df = get_data_from_excel()
print(df)
# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
assembly = st.sidebar.multiselect(
    "Select the Assembly name:",
    options=df["Assembly_name"].unique(),
    default=df["Assembly_name"].unique()
)

grade = st.sidebar.multiselect(
    "Select the Grade:",
    options=df["Grade"].unique(),
    default=df["Grade"].unique()
)

profile= st.sidebar.multiselect(
    "Select the Profile:",
    options=df["Profile"].unique(),
    default=df["Profile"].unique()
)

df_selection = df.query(
    "Assembly_name == @assembly & Grade== @grade & Profile == @profile"
)

# ---- MAINPAGE ----
st.title(":bar_chart: Weigths Dashboard")
st.markdown("##")

# TOP KPI's
total_weight = int(df_selection["Weight"].sum())
average_lenght = round(df_selection["Lenght"].mean(), 1)
star_rating = ":star:" * int(round(average_lenght/12000, 0))
average_weight = round(df_selection["Weight"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Weight:")
    st.subheader(f"Kg {total_weight:,}")
with middle_column:
    st.subheader("Average Lenght:")
    st.subheader(f"{average_lenght} {star_rating}")
with right_column:
    st.subheader("Average Weight:")
    st.subheader(f"Kg {average_weight}")

st.markdown("""---""")

# Lenght BY Profile [BAR CHART]
lenght_by_profile = (
    df_selection.groupby(by=["Profile"]).sum()[["Lenght"]].sort_values(by="Lenght")
)
fig_lenght_by_profile = px.bar(
    lenght_by_profile,
    x="Lenght",
    y=lenght_by_profile.index,
    orientation="h",
    title="<b>Lenght by profile</b>",
    color_discrete_sequence=["#0083B8"] * len(lenght_by_profile),
    template="plotly_white",
)
fig_lenght_by_profile.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# surface_by_unit_weight [BAR CHART]
surface_by_unit_weight = df_selection.groupby(by=["Kg_m"]).sum()[["Surface"]]
fig_surface_by_unit_weight = px.bar(
    surface_by_unit_weight,
    x=surface_by_unit_weight.index,
    y="Surface",
    title="<b>Surface by unit weight</b>",
    color_discrete_sequence=["#0083B8"] * len(surface_by_unit_weight),
    template="plotly_white",
)
fig_surface_by_unit_weight.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_surface_by_unit_weight, use_container_width=True)
right_column.plotly_chart(fig_lenght_by_profile, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
