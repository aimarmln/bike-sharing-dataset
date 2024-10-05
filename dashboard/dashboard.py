import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Definisikan function untuk membantu
def create_byseason_df(df: pd.DataFrame):
    byseason_df = df.groupby(by="season")["cnt"].sum().reset_index()
    return byseason_df

def create_byweather_df(df: pd.DataFrame):
    byweather_df = df.groupby(by="weathersit")["cnt"].sum().reset_index()
    return byweather_df

def create_bytimeofday_df(df: pd.DataFrame):
    time_order = ["Morning", "Afternoon", "Evening", "Night"]
    df["time_of_day"] = pd.Categorical(df["time_of_day"], categories=time_order, ordered=True)
    bytimeofday_df = df.groupby(by="time_of_day")["cnt"].sum().reset_index()
    return bytimeofday_df

def create_user_comparison_df(df: pd.DataFrame):
    total_casual = df["casual"].sum()
    total_registered = df["registered"].sum()

    comparison_df = pd.DataFrame({
    "Type": ["Casual", "Registered"],
    "Count": [total_casual, total_registered]
    })

    return comparison_df

# Mengambil semua data
hour_df = pd.read_csv("hour.csv")
day_df = pd.read_csv("day.csv")

# Buat semua data yang diperlukan menggunakan function di atas
byseason_df = create_byseason_df(day_df)
byweather_df = create_byweather_df(day_df)
bytimeofday_df = create_bytimeofday_df(hour_df)
user_comparison_df = create_user_comparison_df(day_df)

# Membuat komponen dashboard
st.title("Bike Sharing Dashboard")
st.metric(f"Total Sharing: ", value=byseason_df["cnt"].sum(), )

# Membuat beberapa tab untuk setiap analisis data
tab1, tab2, tab3 = st.tabs(["By Season & Weather", "By Time of Day", "User Comparison"])

with tab1:
    st.header("By Season and Weather")

    fig1, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        data=byseason_df,
        x="season",
        y="cnt"
    )
    plt.title("Number of Customer per Season", loc="center", fontsize=15)
    plt.ylabel(None)
    plt.xlabel(None)
    plt.tick_params(axis='x', labelsize=12)
    st.pyplot(fig1)

    fig2, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        data=byweather_df.sort_values(by="cnt", ascending=False),
        x="cnt",
        y="weathersit",
        palette=["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    )
    plt.title("Number of Customer per Weather", loc="center", fontsize=15)
    plt.ylabel(None)
    plt.xlabel(None)
    plt.tick_params(axis='x', labelsize=12)
    st.pyplot(fig2)

    with st.expander("See explanation"):
        st.write(
            """
            Fall is the season with the highest number of bike rentals, indicating that this period holds the most potential for increasing revenue. To capitalize on this, we should offer significant promotions during fall, encouraging more customers to rent bikes and thus boosting overall profits.
            """
        )

with tab2:
    st.header("By Time of Day")

    fig, ax = plt.subplots(figsize=(10, 5))
    plt.plot(bytimeofday_df["time_of_day"], bytimeofday_df["cnt"])
    st.pyplot(fig)

    with st.expander("See explanation"):
        st.write(
            """
            The data shows that morning and evening are the peak times for bike rentals, which can be attributed to the daily work commute—morning for going to work and evening for returning home. Understanding this pattern allows us to optimize our services and marketing strategies to cater to the commuting crowd, ensuring availability and potentially offering time-based promotions during these hours.
            """
        )

with tab3:
    st.header("User Comparison")

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        data=user_comparison_df,
        x="Type",
        y="Count"
    )
    plt.title("Non-Registered and Registered User Comparison", loc="center", fontsize=15)
    plt.ylabel(None)
    plt.xlabel(None)
    plt.tick_params(axis='x', labelsize=12)
    st.pyplot(fig)

    with st.expander("See explanation"):
        st.write(
            """
            Registered users account for a much higher number of rentals compared to casual users. To increase the number of registered users and thereby enhance customer retention, we should introduce targeted promotions. For example, as mentioned in the conclusion for question 1, offering exclusive fall deals that can only be accessed by registered members would incentivize casual users to sign up for membership. This strategy would help grow the user base and positively impact company revenue in the long term.
            """
        )


st.write("")
st.write("")
st.caption("aimarmln @dicoding")
