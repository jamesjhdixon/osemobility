from tdm_functions import (return_tdsk, return_forecast, return_weo, get_base_pkm_per_mode, calculate_travel_demand,
                           example_elasticity_function)
import matplotlib.pyplot as plt

# %%
# Run through example -- retrieve base year data

# Return data
tdsk_data = return_tdsk()
imf_data = return_weo()

# Input country
country = input('Country?')

if country.lower() in [l.lower() for l in tdsk_data['Country name'].unique().tolist()]:

    years_with_data = []

    variables_of_interest = ['ROAD_PA_MOV']

    for year in range(min([t for t in tdsk_data.columns.tolist() if type(t) == int]),
                      max([t for t in tdsk_data.columns.tolist() if type(t) == int])):

        if not tdsk_data[(tdsk_data['Country name'] == country) & (tdsk_data['Data code'].isin(variables_of_interest))][
            year].isnull().all():
            years_with_data.append(year)

    base_year = int(input(f'Suggested base years for {country}: {years_with_data}. Base year?'))
    end_year = 2030

    forecast_data = return_forecast(country=country, data=imf_data)

    base_year_data = get_base_pkm_per_mode(df=tdsk_data, country=country, year=base_year)

    # Plot data from dictionaries

    # Prepare data for plotting
    years = []
    car_values = []
    moto_values = []
    bus_values = []

    data = calculate_travel_demand(df=tdsk_data, country=country, base_year=base_year, projection_data=forecast_data,
                                   elasticity_function=example_elasticity_function)

    for year in range(base_year, end_year):  # Iterate from 2015 to 2029
        if year in data:
            years.append(year)
            car_values.append(data[year]['CAR'])
            moto_values.append(data[year]['MOTO'])
            bus_values.append(data[year]['BUS'])

    # Create the plot
    plt.figure(figsize=(10, 6))  # Adjust figure size as needed
    plt.plot(years, car_values, marker='o', linestyle='-', label='CAR')
    plt.plot(years, moto_values, marker='o', linestyle='-', label='MOTO')
    plt.plot(years, bus_values, marker='o', linestyle='-', label='BUS')

    # Add labels and title
    plt.xlabel('Year')
    plt.ylabel('Passenger-km')
    plt.title(f'{country}: Passenger-km by mode of transport ({base_year}-{end_year})')
    plt.legend()

    # Show the plot
    plt.grid(axis='y', linestyle='--')  # Add a grid for better readability
    plt.show()

else:
    print(f'{country} not in data!')