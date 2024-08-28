from modules.vehicle_stock.vehicle_stock.vsm_functions import (return_input_data, return_age_data_cumulative_stock, return_age_data_new_stock,
                           return_scrappage_data, get_base_year_stock, get_base_year_new_stock, return_country_data,
                           calculate_desired_stock, calculate_vehicle_stocks, plot_stock_by_age, plot_cumulative_stock)

from modules.transport_demand.tdm_functions import (return_tdsk, return_forecast, return_weo, get_base_pkm_per_mode, calculate_travel_demand,
                           example_elasticity_function, create_pkm_plot)

#%% TDM
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

#%% VSM

# TODO: base year alignment 1 off. testing to see if it works.
end_year -= 1

# TODO: using arbitary occupancy & kilometrage data. Change.
# get input data
pkm_by_mode_dummy, occ_by_mode, kilometrage_by_mode = return_input_data()

# get country data
df = return_country_data(country='zambia')

# get base year stock (cumulative)
base_year_stock = get_base_year_stock(df, base_year)

# get base year stock (new)
base_year_new_stock = get_base_year_new_stock(df, base_year)

# get scrappage data
scrappage_data = return_scrappage_data()

# get age profile data (new stock)
age_data_new_stock = return_age_data_new_stock()

# get age profile data (cumulative stock)
age_data = return_age_data_cumulative_stock()

# calculate desired stock
desired_stock = calculate_desired_stock(pkm_by_mode, occ_by_mode, kilometrage_by_mode)

# calculate annual stock
annual_stock = calculate_vehicle_stocks(desired_stock, base_year_stock, base_year_new_stock, age_data_new_stock,
                                        scrappage_data, base_year=base_year, end_year=end_year)

# plot stock
plot_stock_by_age(annual_stock, year=int(input('What year for the age distribution plot?')))