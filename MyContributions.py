import streamlit as st
import openai

# OpenAI API key
openai.api_key='Your-API-Key-Here'

# Dictionary mapping cities to their OpenAI identifiers
city_mapping = {
    'Berkeley': 'city of berkeley',
    'Oakland': 'city of oakland',
    'San Leandro': 'city of san leandro',
    'Hayward': 'city of hayward',
    'Fremont': 'city of fremont',
    'Santa Clara': 'city of santa clara',
    'Milpitas': 'city of milpitas',
    'San Jose': 'city of san jose',
    'Sunnyvale': 'city of sunnyvale',
    'Palo Alto': 'city of palo alto',
    'San Mateo': 'city of san mateo',
    'Daly City': 'city of daly city',
    'Pacifica': 'city of pacifica'
}

# Function to get average monthly rent for a city from OpenAI
import re

def get_average_rent(city, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "Answer the prompt to your best abilities"},
            {"role": "user", "content": "What is the average monthly rent in " + city + "?"},
        ]
    )
    rent_response = response['choices'][0]['message']['content'].strip()
    rent = re.findall(r'\d+,\d+', rent_response)
    if rent:
        rent = float(rent[0].replace(',', ''))
    else:
        rent = None
    return rent

# Function to get average loan interest rate for a city from OpenAI
def get_average_interest_rate(city, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "Answer the prompt to your best abilities"},
            {"role": "user", "content": "What is the average loan interest rate in " + city + "?"},
        ]
    )
    rate_response = response['choices'][0]['message']['content'].strip()
    rate = re.findall(r'\d+.\d+', rate_response)
    if rate:
        rate = float(rate[0])
    else:
        rate = None
    return rate

st.title("BayBalance AI")

feature = st.selectbox("Select Feature", ["Affordability Calculator", "Mortgage Loan Calculator", "Expense Categorizer"])

if feature == "Affordability Calculator":
    st.title("Affordability Calculator")

    selected_city = st.selectbox("Select a city", list(city_mapping.keys()))
    average_rent = get_average_rent(city_mapping[selected_city])
    st.info(f"The average monthly rent in {selected_city} is {average_rent}")
    monthly_income = st.number_input("Enter your gross monthly income", value=0.0, step=100.0)
    transportation_cost = st.number_input("Enter transportation cost per month", value=0.0, step=10.0)
    food_cost = st.number_input("Enter food cost per month", value=0.0, step=10.0)
    entertainment_cost = st.number_input("Enter entertainment cost per month", value=0.0, step=10.0)
    activities_cost = st.number_input("Enter activities cost per month", value=0.0, step=10.0)
    savings_amount = st.number_input("Enter how much you want to save per month", value=0.0, step=10.0)
    investment_amount = st.number_input("Enter how much you want to invest per month", value=0.0, step=10.0)

    # Calculate total expenses
    total_expenses = transportation_cost + food_cost + entertainment_cost + activities_cost + savings_amount + investment_amount

    # Get average rent for the selected city
    average_rent = get_average_rent(city_mapping[selected_city])

    # Calculate affordability
    affordability = monthly_income - float(average_rent) - total_expenses

    # Display affordability result
    if affordability < 0:
        st.error("User cannot afford to live in selected area.")
        lower_rent_areas = [city for city, city_id in city_mapping.items() if city != selected_city and float(get_average_rent(city_id)) < float(average_rent)]
        if lower_rent_areas:
            st.warning(f"Consider living in these areas with lower average rents: {', '.join(lower_rent_areas)}")
        else:
            st.warning("User can't afford to live in any other areas in the Bay Area.")
    else:
        st.success("User can afford to live in selected area.")




