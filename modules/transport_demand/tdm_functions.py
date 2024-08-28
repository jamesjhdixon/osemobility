import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# %%
# import data - return TDSK
def return_tdsk(start_year=1990, end_year=2021):
    try:
        df = pd.read_excel("https://zenodo.org/records/10406893/files/TSDK_ALL.xlsx?download=1", sheet_name="Data")
        country_data = df[['Country name', 'Variable', 'Data code', 'Unit'] + [y for y in range(
            start_year, end_year)]]
        return country_data
    except Exception as e:
        return f"an error occurred (probably the source data at URL has changed): {e}"


# import data - return World Economic Outlook database (IMF)
def return_weo(start_year=1990, end_year=2030):
    try:
        df = pd.read_excel(f"./../data/WEOApr2024all.xlsx")
        country_data = df[['Country', 'WEO Subject Code', 'Subject Descriptor', 'Units'] + [y for y in range(
            start_year, end_year)]]
        return country_data
    except Exception as e:
        return f"an error occurred (probably the source data at URL has changed): {e}"


# %%
# Function to return forecast for data - IMF

def return_forecast(country, data, variables={'GDP': 'NGDPD', 'Population': 'LP'}, years=range(1990, 2030)):
    # Create the dictionary
    forecast_data = {}

    for variable in variables:

        forecast_data[variable] = {}

        # Return data for this country and this subject code
        country_data = data.loc[(data['Country'] == country) & (data['WEO Subject Code'] == variables[variable])]

        # Add GDP values to the dictionary
        if country_data.empty:
            print(f"Warning: No data found for {variable} in {country}")
            forecast_data[variable] = {}
        else:
            forecast_data[variable] = dict(zip(years, country_data[years].values[0]))

    return forecast_data


# %%
def get_base_pkm_per_mode(df, country, year):
    """
    Calculates base passenger-km by mode for a given country and year.

    Args:
        df: Pandas DataFrame containing transport data.
        country: Name of the country (string).
        year: Year for which base pkm is needed (int).

    Returns:
        base_pkm_per_mode: Dictionary containing base pkm for each mode (or None).
    """
    # Filter data for selected country and year
    df = df[df['Country name'] == country]

    #    print(df)

    # Check for mode split data availability
    mode_split_codes = ['ROAD_PA_MOV', 'ROAD_PA_MOTORC', 'ROAD_PA_CAR', 'ROAD_PA_BUS']
    if len([m for m in mode_split_codes if m in df['Data code'].tolist()]) == len(
            mode_split_codes):  # if mode split already in TSDK
        # Extract base pkm by mode from year data
        # base_pkm_per_mode = df[df['Data code'].isin(mode_split_codes)].iloc[0][year].to_dict()
        base_pkm_per_mode = {'BUS': df[df['Data code'] == 'ROAD_PA_BUS'].iloc[0][year],
                             'CAR': df[df['Data code'] == 'ROAD_PA_CAR'].iloc[0][year],
                             'MOTO': df[df['Data code'] == 'ROAD_PA_MOTORC'].iloc[0][year]}
    else:
        # Use total pkm and predefined mode shares if mode split data unavailable or NaN
        total_pkm = df[(df['Data code'] == 'ROAD_PA_MOV') & ~np.isnan(df[year])].iloc[0][year]

        # TODO: Add better data here!!
        mode_share_road_pkm = {'BUS': 0.55, 'CAR': 0.2, 'MOTO': 0.1}  # arbitrary(?) data
        base_pkm_per_mode = {mode: total_pkm * share for mode, share in mode_share_road_pkm.items()}

    return base_pkm_per_mode if base_pkm_per_mode else None


# %%
def calculate_travel_demand(df, country, base_year, projection_data, elasticity_function, end_year=2030):
    """
    Calculates passenger-km by mode for all years based on projections and elasticities.

    Args:
        df: Pandas DataFrame containing TDSK data.
        country: Name of the country (string).
        base_year: Base year for calculations (int).
        projection_data: Dictionary containing GDP and population projections.
        elasticity_function: Function that calculates dynamic elasticities (function).

    Returns:
        pkm_per_mode_per_year: Dictionary with pkm for each mode for all years.
    """
    # Get base pkm by mode for the base year
    base_pkm_per_mode = get_base_pkm_per_mode(df, country, base_year)

    # Check if base pkm data is available
    if not base_pkm_per_mode:
        return None

    # Initialize dictionary to store pkm by mode for all years
    pkm_per_mode_per_year = {year: {} for year in range(base_year, end_year)}

    # Iterate through years and calculate pkm for each mode
    for year in pkm_per_mode_per_year:
        # Get GDP and population for the current year from projections
        gdp_current = projection_data['GDP'][year]
        population_current = projection_data['Population'][year]

        # Calculate dynamic elasticities for the current year using the function
        gdp_elasticity, population_elasticity = elasticity_function(year)

        # Calculate pkm for each mode based on base pkm, GDP, population, and elasticities
        for mode, base_pkm in base_pkm_per_mode.items():
            pkm_per_mode_per_year[year][mode] = base_pkm * (
                    gdp_current / projection_data['GDP'][base_year]) ** gdp_elasticity * (
                                                        population_current / projection_data['Population'][
                                                    base_year]) ** population_elasticity

    return pkm_per_mode_per_year


# %%
# Example usage (replace with your actual elasticity function and projection data)
def example_elasticity_function(year):
    # Implement your logic to calculate dynamic elasticities based on year
    # This is a placeholder example, replace with your actual function
    return 1.2, 1.1  # Placeholder elasticity values


# %%
# Plot pkm_by_mode
def create_pkm_plot(base_year, end_year, pkm_by_mode, country, modes=None):

    if modes is None:
        modes = ['CAR', 'MOTO', 'BUS']

    years = []
    mode_values = {mode: [] for mode in modes}

    for year in range(base_year, end_year + 1):
        if year in pkm_by_mode:
            years.append(year)
            for mode in modes:
                mode_values[mode].append(pkm_by_mode[year].get(mode, 0))

    # Create figure and axes explicitly
    sns.set_style('whitegrid')
    fig, ax = plt.subplots(figsize=(10, 6))

    for mode, values in mode_values.items():
        ax.plot(years, values, marker='o', linestyle='-', label=mode)  # Plot on the axes object

    ax.set_xlabel('Year')
    ax.set_ylabel('Passenger-km')
    ax.set_title(f'{country}: Passenger-km by mode of transport ({base_year}-{end_year})')
    ax.legend()
    ax.grid(axis='y', linestyle='--')

    # Return the figure
    return fig
