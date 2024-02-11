# Reads input data to generate baseline data (base year)
# v1 - set input data to TDSK

import pandas as pd

# return TSDK for specified country.
def return_country_data(country='Kenya', start_year=1990, end_year=2021):
    df = pd.read_excel("TSDK_ALL.xlsx", sheet_name="Data")
    country_data = df[df['Country name'] == country][['Country name', 'Data code', 'Unit'] + [y for y in range(
        start_year, end_year)]]
    return country_data

# return gdp per year (total) for country, for which data exists.
def return_gdp(df):
    gdp = pd.Series(df[df['Data code'] == 'GDP_TOT'].iloc[0])
    return gdp.dropna()

# return total population and share urb/rur
def return_pop(df):
    pop = df[df['Data code'].isin(['POP_TOT', 'POP_URB', 'POP_RUR'])]
    return pop.dropna()

# return pkm_road (total) for country, for which data exists. Amalgamate sources.
def return_pkm_road(df):
    pkm_road = (df[df['Data code'] == 'ROAD_PA_MOV'].set_index(['Country name', 'Data code']).stack().groupby
                (level=[1, 2]).first().unstack())
    return pkm_road

# return pkm_rail (total) for country, for which data exists. Amalgamate sources.
def return_pkm_rail(df):
    pkm_road = (df[df['Data code'] == 'ROAD_PA_MOV'].set_index(['Country name', 'Data code']).stack().groupby
                (level=[1, 2]).first().unstack())
    return pkm_road