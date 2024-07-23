from tdm_functions import (return_tdsk, return_forecast, return_weo, get_base_pkm_per_mode, calculate_travel_demand,
                           example_elasticity_function, create_pkm_plot)

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

    # produce pkm_by_mode (output data vector)
    pkm_by_mode = calculate_travel_demand(df=tdsk_data, country=country, base_year=base_year, projection_data=forecast_data,
                                   elasticity_function=example_elasticity_function)

    # plot the data
    fig = create_pkm_plot(base_year, end_year, pkm_by_mode, country)
    fig.show()

else:
    print(f'{country} not in data!')