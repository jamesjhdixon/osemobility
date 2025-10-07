# Vehicle stock functions
# Objective: to calculate the number of required vehicles in year=y given demand for vehicles and scrap

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Temporarily store pkm_by_mode data here to be used
def return_input_data():
    pkm_by_mode = {2018: {'BUS': 8281.1479135,  # million km
                          'CAR': 3011.3265140000003,
                          'MOTO': 1505.6632570000002},
                   2019: {'BUS': 8605.207855741015,
                          'CAR': 3129.1664929967333,
                          'MOTO': 1564.5832464983666},
                   2020: {'BUS': 10027.353407440589,
                          'CAR': 3646.310329978396,
                          'MOTO': 1823.155164989198},
                   2021: {'BUS': 11678.98200465771,
                          'CAR': 4246.902547148258,
                          'MOTO': 2123.451273574129},
                   2022: {'BUS': 11491.999093342863,
                          'CAR': 4178.908761215587,
                          'MOTO': 2089.4543806077936},
                   2023: {'BUS': 12965.708721919502,
                          'CAR': 4714.803171607092,
                          'MOTO': 2357.401585803546},
                   2024: {'BUS': 14571.558975996335,
                          'CAR': 5298.748718544121,
                          'MOTO': 2649.3743592720607},
                   2025: {'BUS': 16397.286358817768,
                          'CAR': 5962.649585024643,
                          'MOTO': 2981.3247925123214},
                   2026: {'BUS': 18357.960614482894,
                          'CAR': 6675.622041630143,
                          'MOTO': 3337.8110208150715},
                   2027: {'BUS': 20533.130726597647,
                          'CAR': 7466.5929914900535,
                          'MOTO': 3733.2964957450267},
                   2028: {'BUS': 22984.38516000512,
                          'CAR': 8357.958240001863,
                          'MOTO': 4178.979120000931},
                   2029: {'BUS': 25706.56124730344,
                          'CAR': 9347.840453564888,
                          'MOTO': 4673.920226782444},
                   2030: {'BUS': 27706.56124730344,
                          'CAR': 12047.840453564888,
                          'MOTO': 6673.920226782444}}

    # Temporarily store avg. occupancy data here (average number of passengers per vehicle)
    # TODO: this will be user-editable and will go into an equivalent of the TEAM PARAMETERS_XX tables.
    occ_by_mode = {2018: {'BUS': 15,
                          'CAR': 2,
                          'MOTO': 1.5},
                   2019: {'BUS': 15,
                          'CAR': 2,
                          'MOTO': 1.5},
                   2020: {'BUS': 15,
                          'CAR': 2,
                          'MOTO': 1.5},
                   2021: {'BUS': 15,
                          'CAR': 2,
                          'MOTO': 1.5},
                   2022: {'BUS': 15,
                          'CAR': 2,
                          'MOTO': 1.5},
                   2023: {'BUS': 15,
                          'CAR': 2,
                          'MOTO': 1.5},
                   2024: {'BUS': 15,
                          'CAR': 2,
                          'MOTO': 1.5},
                   2025: {'BUS': 15,
                          'CAR': 2,
                          'MOTO': 1.5},
                   2026: {'BUS': 15,
                          'CAR': 2,
                          'MOTO': 1.5},
                   2027: {'BUS': 15,
                          'CAR': 2,
                          'MOTO': 1.5},
                   2028: {'BUS': 15,
                          'CAR': 2,
                          'MOTO': 1.5},
                   2029: {'BUS': 15,
                          'CAR': 2,
                          'MOTO': 1.5},
                   2030: {'BUS': 15,
                          'CAR': 2,
                          'MOTO': 1.5}}

    # Temporarily store kilometrage data here (avg. annual kilometrage by vehicle)
    # TODO: this will be user-editable and will go into an equivalent of the TEAM PARAMETERS_XX tables.
    kilometrage_by_mode = {2018: {'BUS': 31986,
                                  'CAR': 23023,
                                  'MOTO': 17807},
                           2019: {'BUS': 31986,
                                  'CAR': 23023,
                                  'MOTO': 17807},
                           2020: {'BUS': 31986,
                                  'CAR': 23023,
                                  'MOTO': 17807},
                           2021: {'BUS': 31986,
                                  'CAR': 23023,
                                  'MOTO': 17807},
                           2022: {'BUS': 31986,
                                  'CAR': 23023,
                                  'MOTO': 17807},
                           2023: {'BUS': 31986,
                                  'CAR': 23023,
                                  'MOTO': 17807},
                           2024: {'BUS': 31986,
                                  'CAR': 23023,
                                  'MOTO': 17807},
                           2025: {'BUS': 31986,
                                  'CAR': 23023,
                                  'MOTO': 17807},
                           2026: {'BUS': 31986,
                                  'CAR': 23023,
                                  'MOTO': 17807},
                           2027: {'BUS': 31986,
                                  'CAR': 23023,
                                  'MOTO': 17807},
                           2028: {'BUS': 31986,
                                  'CAR': 23023,
                                  'MOTO': 17807},
                           2029: {'BUS': 31986,
                                  'CAR': 23023,
                                  'MOTO': 17807},
                           2030: {'BUS': 31986,
                                  'CAR': 23023,
                                  'MOTO': 17807}}

    return pkm_by_mode, occ_by_mode, kilometrage_by_mode


# return age data - EXISTING STOCK (based on GIZ INFRAS 2019 Kenya data)
def return_age_data_cumulative_stock():
    age_data = pd.read_csv('./../data/vehicle_stock/age_distribution.csv')
    return age_data


# return age data - NEW STOCK (based on Zambian vehicle registration data (Malindi))
def return_age_data_new_stock():
    new_age_data = pd.read_csv('./../data/vehicle_stock/age_distribution_new_vehicles.csv')
    return new_age_data


# return scrappage data
def return_scrappage_data():
    scrappage_data = pd.read_csv('./../data/vehicle_stock/scrappage_rates.csv')
    return scrappage_data


# Get base_year_stock
def get_base_year_stock(df, base_year, age_data=return_age_data_cumulative_stock(), vehicles=['BUS', 'CAR', 'MOTO']):#, 'MINIBUS', 'VAN', 'TRUCK']):
    """Retrieves vehicle stock by mode for the base year (input data).

    Args:
        df: Country data. Currently built on country-specific data.
        base_year: Integer. E.g. 2015.

    Returns:
        Dict with year as key and nested dict of mode:vehicles as value.
    """

    # Retrieve data from stock
    base_year_stock = {base_year: {vehicle: {} for vehicle in vehicles}}
    for vehicle in vehicles:
        for age in age_data.Age.dropna().unique().tolist():
            base_year_stock[base_year][vehicle][age] = np.round(df[df['Data code'] == f'ROAD_STOCK_CUM_{vehicle}']
                                                                [str(base_year)].item() * age_data[age_data['Age'] == age][[c for c in age_data.columns.tolist() if 'CAR' in c][0]].tolist()[0], 0) # TODO: this just takes the first matching age data. Improve with a better tech lookup.
    return base_year_stock


# get base_year_new_stock
def get_base_year_new_stock(df, base_year, age_data=return_age_data_new_stock(),
                            vehicles=['BUS', 'CAR', 'MOTO']):  # , 'MINIBUS', 'VAN', 'TRUCK']):
    """Retrieves new vehicle stock by mode for the base year (input data).

    Args:
        df: Country data. Currently built on country-specific data.
        base_year: Integer. E.g. 2015.

    Returns:
        Dict with year as key and nested dict of mode:vehicles as value.
    """

    # Retrieve data from stock
    base_year_new_stock = {base_year: {vehicle: {} for vehicle in vehicles}}
    for vehicle in vehicles:
        for age in age_data['age'].unique().tolist():
            base_year_new_stock[base_year][vehicle][age] = np.round(
                df[df['Data code'] == f'ROAD_STOCK_NEW_{vehicle}'][str(base_year)].item() * age_data[age_data['age'] == age][
                    f'{vehicle}_{base_year}'].item(), 0)

    return base_year_new_stock


# return country data
def return_country_data(country, start_year=1990, end_year=2022):
    try:
        df = pd.read_csv(f"./../data/country_data/{country}/{country}.csv")
        country_data = df[['Country name', 'Variable', 'Type', 'Sub-type', 'Fuel', 'Destination', 'Data code', 'Unit'] +
                          [str(y) for y in range(start_year, end_year)]]
        return country_data
    except Exception as e:
        return f"an error occurred: {e}"


# function to return desired vehicle fleet based on demand. Using basic formula vehicle_fleet = PKM / (occupancy * kilometrage)
def calculate_desired_stock(pkm_by_mode, occ_by_mode, kilometrage_by_mode):
    """Calculates the desired vehicle fleet for each mode based on PKM, occupancy, and annual kilometrage.

    Args:
        pkm_by_mode (dict): A dictionary containing PKM values for each mode and year.
        occ_by_mode (dict): A dictionary containing average occupancy values for each mode and year.
        kilometrage_by_mode (dict): A dictionary containing average annual kilometrage values for each mode and year.

    Returns:
        dict: A dictionary containing the desired vehicle fleet for each mode and year.
    """

    desired_stock = {}

    for year, pkm_data in pkm_by_mode.items():
        desired_stock[year] = {}
        for mode, pkm in pkm_data.items():
            occupancy = occ_by_mode[year][mode]
            kilometrage = kilometrage_by_mode[year][mode]
            desired_stock[year][mode] = 1e6 * pkm / (occupancy * kilometrage)  # pkm in million km

    return desired_stock


# calculate vehicle stock
def calculate_vehicle_stocks(desired_stock, base_year_stock, base_year_new_stock, age_data_new_stock, scrappage_data,
                             base_year=2018, end_year=2030, vehicles=['BUS', 'CAR', 'MOTO']):
    # vehicles=['BUS', 'CAR', 'MOTO']# , 'MINIBUS', 'VAN', 'TRUCK']
    scrappage_lookup = {'BUS': 'BUS', 'CAR': 'CAR', 'MOTO': 'MOTO', 'MINIBUS': 'LCV', 'VAN': 'LCV', 'TRUCK': 'HGV'}

    # instantiate dictionaries to track stock and scrap annually
    annual_stock = {base_year: base_year_stock[base_year]}  # (cumulative)
    annual_scrap = {year: {vehicle: {} for vehicle in vehicles} for year in
                    range(base_year, end_year + 1)}  # (scrap in that year)
    new_stock = {
        base_year: base_year_new_stock[base_year]}  # (new stock, can be second-hand: accounting for age profile

    # calculate the latest year available in the new stock age data
    latest_year = max([int(c.split('_')[-1]) for c in age_data_new_stock.columns.tolist() if '20' in c])

    for year in range(base_year + 1, end_year + 1):

        annual_stock[year] = {}
        annual_scrap[year] = {}
        new_stock[year] = {}

        for vehicle in vehicles:

            annual_stock[year][vehicle] = {}
            annual_scrap[year][vehicle] = {}
            new_stock[year][vehicle] = {}

            for age in range(len(annual_stock[year - 1][vehicle]) - 1):
                # calculate scrap in year y-1 based on the stock in y-1 and the scrappage probabilities (that are independent of time)
                annual_scrap[year - 1][vehicle][age] = annual_stock[year - 1][vehicle][age] * \
                                                       scrappage_data[scrappage_data['Age'] == age][
                                                           scrappage_lookup[vehicle]].item()

                # calculate stock in year y (before the addition of new vehicles) by subtracting scrap (y-1) from stock (y-1)
                annual_stock[year][vehicle][age] = annual_stock[year - 1][vehicle][age] - \
                                                   annual_scrap[year - 1][vehicle][
                                                       age]  # remove scrapped vehicles from the stock

            # calculate new stock required: new stock required = desired stock[y] - actual stock[y-1] + scrap[y-1]
            new_stock_required = desired_stock[year][vehicle] - sum(annual_stock[year - 1][vehicle].values()) + sum(
                annual_scrap[year - 1][vehicle].values())

            # if less than zero, return zero.
            if new_stock_required <= 0:
                new_stock_required = 0

            # calculate age distribution of additional stock
            for age in range(len(annual_stock[year - 1][vehicle]) - 1):

                if f'{vehicle}_{year}' in age_data_new_stock.columns:
                    new_stock[year][vehicle][age] = new_stock_required * \
                                                    age_data_new_stock[age_data_new_stock['age'] == age][
                                                        f'{vehicle}_{year}'].item()

                else:
                    new_stock[year][vehicle][age] = new_stock_required * \
                                                    age_data_new_stock[age_data_new_stock['age'] == age][
                                                        f'{vehicle}_{latest_year}'].item()

                annual_stock[year][vehicle][age] += new_stock[year][vehicle][age]

            # Age the fleet by shifting the age distribution down by one
            for age in range(len(annual_stock[year][vehicle]) - 1, 0, -1):
                annual_stock[year][vehicle][age] = annual_stock[year][vehicle][age - 1]

            annual_stock[year][vehicle][0] = 0

    print(f'Calculated annual vehicle stocks for set {vehicles} over years ({base_year, end_year})')

    return annual_stock


# plot stock data - bar chart/histogram by age and vehicle type
def plot_stock_by_age(stock_dict, year, vehicles=['BUS', 'CAR', 'MOTO']):  # , 'MINIBUS', 'VAN', 'TRUCK']):

    # bar width (plot)
    bar_width = 0.2

    sns.set_style('whitegrid')

    fig, ax = plt.subplots()

    for i, vehicle in enumerate(vehicles):
        data_for_vehicle = {year: stock_dict[year][vehicle]}
        ax.bar([x + (i * bar_width) for x in range(len(data_for_vehicle[year]))], data_for_vehicle[year].values(),
               width=bar_width, label=vehicle)

    # Plot settings
    ax.set_xlabel('Vehicle Age')
    ax.set_ylabel('Number of Vehicles')
    plt.title(f'Annual Stock by Vehicle Type and Age ({year})')
    plt.legend()

    # Show the plot
    plt.show()

    plt.savefig(f'stock_by_year_{year}.png')

    return plt.gcf()


# plot stock data - cumulative annual stock
def plot_cumulative_stock(stock_dict, years, vehicles=['BUS', 'CAR', 'MOTO']):  # , 'MINIBUS', 'VAN', 'TRUCK']):

    plot_dict = {}
    for vehicle in vehicles:
        plot_dict[vehicle] = {}
        for year in years:
            plot_dict[vehicle][year] = sum(stock_dict[year][vehicle].values())

    sns.set_style('whitegrid')

    fig, ax = plt.subplots()
    for vehicle in vehicles:
        ax.plot(years, plot_dict[vehicle].values(), label=vehicle)

    ax.set_ylabel('Stock')
    plt.legend()

    plt.show()
    plt.savefig('annual_stock.png')
    return plt.gcf()