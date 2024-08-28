# Vehicle stock code
# Objective: to calculate the number of required vehicles in year=y given demand for vehicles and scrap

# SEE VSM-NOTEBOOK FOR DEVELOPMENT!

# %%
# Temporarily store pkm_by_mode data here to be used
def return_input_data():
    pkm_by_mode = {2018: {'BUS': 8281.1479135,
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
                          'MOTO': 4673.920226782444}}

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


# %%
# Return number of vehicles required for each mode based on demand
# General philosophy:
# 1. vkm = pkm/avg occupancy rate for each mode
# 2. required vehicle stock for year y = vkm/avg kilometrage for that vehicle

# define function to calculate 'demanded' vehicles per year, based on pkm, occupancy and kilometrage
def calculate_vehicle_demand(pkm_by_mode, occ_by_mode, kilometrage_by_mode):
    """Calculates desired number of vehicles by mode for each year.

    Args:
        pkm_by_mode: Dict with year as key and nested dict of mode:pkm as value.
        occ_by_mode: Dict with year as key and nested dict of mode:occupancy as value.
        kilometrage_by_mode: Dict with year as key and nested dict of mode:kilometrage as value.

    Returns:
        Dict with year as key and nested dict of mode:vehicles as value.
    """

    vehicle_demand = {}
    for year in pkm_by_mode:
        vehicle_demand[year] = {}
        for mode in pkm_by_mode[year]:
            # Ensure year and mode exist in all dictionaries, default to 0 if not
            pkm = pkm_by_mode.get(year, {}).get(mode, 0) * 1e6  # pkm is in million pkm
            occ = occ_by_mode.get(year, {}).get(mode, 0)
            km = kilometrage_by_mode.get(year, {}).get(mode, 0)

            # Avoid division by zero by setting demand to 0 if occupancy or kilometrage is 0
            demand = pkm / (occ * km) if occ != 0 and km != 0 else 0
            vehicle_demand[year][mode] = demand

    return vehicle_demand


