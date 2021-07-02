from os import read
import streamlit as st
import pandas as pd
import pickle
from jinja2 import Template

st.set_page_config(page_title="Value Calculator")

st.title("Value Calculator")

# remove the header and footer
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Reading Static Data
with open("assets/html/header.html", "r") as f:
    st.markdown(f.read(), unsafe_allow_html=True)


def load_data(filename):
    try:
        with open(f"{filename}.pkl", "rb") as f:
            data = pickle.load(f)
    except Exception as E:
        print(f"error on load : {E}")
        return
    return data


job_titles: dict = load_data("job_title")

job_selected = st.selectbox(
    "Position Held By Employee Doing Task?", list(job_titles.keys())
)

hourly_sal = format(
    (int(job_titles[job_selected].replace("£", "").replace(",", "")) / 52) / 37, ".2f"
)

st.text(f"Average Yearly Salary : {job_titles[job_selected]}")
st.text(f"Average Hourly Rate : £{hourly_sal}")

weekly_time_spent = st.number_input(
    "How many hours does this task take per week for all employees involved?",
    min_value=1,
    value=5,
)

# Saving calculations
savings = float(hourly_sal) * int(weekly_time_spent)
average_revenue_yearly = 118000
average_revenue_hourly = (average_revenue_yearly / 52) / 37

weekly_savings = format(float(hourly_sal) * int(weekly_time_spent), ".2f")
yearly_savings = format(float(hourly_sal) * int(weekly_time_spent) * 52, ".2f")


potential_revenue = format(average_revenue_hourly * weekly_time_spent * 52, ".2f")
total_year_savings = format(float(potential_revenue) + float(yearly_savings), ".2f")
# st.text(f"Total Potential Savings : £{total_year_savings}")
# pd.read_csv(
#     "https://www.ethnicity-facts-figures.service.gov.uk/work-pay-and-benefits/employment/employment-by-occupation/latest/downloads/employment-by-occupation.csv"
# )

# Savings text
with open("assets/html/savings.html", "r") as f:
    t = Template(f.read())
    variables = {
        "hours": int(weekly_time_spent) * 52,
        "yearly_saving": f"£{yearly_savings}",
        "revenue_potential": f"£{total_year_savings}",
    }
    st.markdown(
        t.render(variables), unsafe_allow_html=True,
    )

st.text(f"Yearly Hours Saved : {int(weekly_time_spent)*52}")
st.text(f"Weekly Cost of Task : £{weekly_savings}")
st.text(f"Yearly Cost of Task : £{yearly_savings}")
st.text(f"Potential Revenue: £{potential_revenue}")
st.text(f"Total Turnover (revenue + cost of task): £{total_year_savings}")

# Footer text
with open("assets/html/footer.html", "r") as f:

    st.markdown(
        f.read(), unsafe_allow_html=True,
    )
