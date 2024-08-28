"""
Vehicle stock code.
"""

# %%

from vsm_functions import (return_input_data, return_age_data_cumulative_stock, return_age_data_new_stock,
                           return_scrappage_data, get_base_year_stock, get_base_year_new_stock, return_country_data,
                           calculate_desired_stock, calculate_vehicle_stocks, plot_stock_by_age, plot_cumulative_stock)

# %%

base_year = 2018
end_year = 2030

# TODO: Replace by input/output from TDM.
# get input data
pkm_by_mode, occ_by_mode, kilometrage_by_mode = return_input_data()

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
                                        scrappage_data)

# plot stock
plot_stock_by_age(annual_stock, year=int(input('Year?')))