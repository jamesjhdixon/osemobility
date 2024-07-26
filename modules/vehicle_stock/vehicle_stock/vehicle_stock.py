"""
Vehicle stock code.
"""

# %%

from vehicle_stock_functions import (return_input_data, get_base_year_stock, calculate_vehicle_demand)

# %%

# TODO: replace this with an input/output from TDM
pkm_by_mode, occ_by_mode, kilometrage_by_mode = return_input_data()

# Return vehicle *demand* by mode for all years.
vehicle_demand = calculate_vehicle_demand(pkm_by_mode, occ_by_mode, kilometrage_by_mode)
print(vehicle_demand)
