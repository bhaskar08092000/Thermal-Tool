import pandas as pd
import numpy as np
import pprint

def load_extended_plant_data(df):
    """Load and process extended power plant operational data"""
    # df['PARAMETERS'] = df['PARAMETERS'].str.strip().str.upper()
    # df = (file_path)
    # df = pd.read_excel(file_path, sheet_name="Boiler Inputs", skiprows=2, usecols=["PARAMETERS", "DESIGN", "OPERATING"])

    parameters =[
        'LOAD', 'AMBIENT PRESSURE', 'AMBIENT TEMPERATURE', 'RELATIVE HUMIDITY',
        'MOISTURE CONTENT IN COAL', 'ASH CONTENT IN COAL', 'FIXED CARBON IN COAL',
        'VOLATILE MATTER IN COAL', 'TOTAL CARBON IN COAL', 'HYDROGEN CONTENT IN COAL',
        'NITROGEN CONTENT IN COAL', 'SULPHER CONTENT IN COAL', 'OXYGEN CONTENT IN COAL',
        'GCV OF COAL', 'UNBURNT CARBON IN FLY ASH', 'UNBURNT CARBON IN BOTTOM ASH',
        '% of Flyash to Total Ash', '% of Bottom ash to Total Ash', 'MS PRESSURE AT BOILER O/L',
        'MS FLOW', 'TOTAL FEED WATER FLOW', 'RH LHS DESUP FLOW', 'RH RHS DESUP FLOW',
        '1ST STAGE SHS DESUP FLOW', '2ND STAGE SHS DESUP FLOW', 'SH SPRAY WATER PRESSURE',
        'SH SPRAY WATER TEMP', 'RH SPRAY WATER PRESSURE', 'RH SPRAY WATER TEMP',
        'MILL-A CURRENT', 'MILL-B CURRENT', 'MILL-C CURRENT', 'MILL-D CURRENT',
        'MILL-E CURRENT', 'MILL-F CURRENT', 'MILL- A COAL FLOW', 'MILL- B COAL FLOW',
        'MILL- C COAL FLOW', 'MILL- D COAL FLOW', 'MILL- E COAL FLOW', 'MILL- F COAL FLOW',
        'TOTAL COAL FLOW', 'MILL-A O/L TEMP', 'MILL-B O/L TEMP', 'MILL-C O/L TEMP',
        'MILL-D O/L TEMP', 'MILL-E O/L TEMP', 'MILL-F O/L TEMP', 'APH-A I/L FLUE GAS TEMP-1',
        'APH-A I/L FLUE GAS TEMP-2', 'APH-A O/L FLUE GAS TEMP-1', 'APH-A FLUE GAS O/L TEMP-2',
        'APH-B I/L FLUE GAS TEMP-1', 'APH-B I/L FLUE GAS TEMP-2', 'APH-B O/L FLUE GAS TEMP-1',
        'APH-B FLUE GAS O/L TEMP-2', 'APH-A PA I/L TEMP', 'APH-B PA I/L TEMP',
        'APH -A OUT PRI AIR TEMP', 'APH -B OUT PRI AIR TEMP', 'APH -A SEC. AIR IN TEMP',
        'APH -B SEC. AIR IN TEMP', 'APH -A SEC AIR OUTLET TEMP', 'APH -B SEC AIR OUTLET TEMP',
        'APH -A INLET P.A PRESSURE', 'APH -B INLET P.A PRESSURE',
        'PA HEADER PRESSURE APH-A O/L', 'PA HEADER PRESSURE APH-B O/L',
        'APH -A INLET S.A PRESSURE', 'APH -B INLET S.A PRESSURE',
        'APH -A OUTLET S.A PRESSURE', 'APH -B OUTLET S.A PRESSURE',
        'APH-A INLET FLUE GAS PRESSURE', 'APH-B INLET FLUE GAS PRESSURE',
        'APH-A OUTLET FLUE GAS PRESSURE', 'APH-B OUTLET FLUE GAS PRESSURE',
        'APH-A I/L FLUE GAS OXYGEN CONTENT', 'APH-A O/L FLUE GAS OXYGEN CONTENT',
        'APH-B I/L FLUE GAS OXYGEN CONTENT', 'APH-B O/L FLUE GAS OXYGEN CONTENT',
        'TOTAL SEC AIR FLOW', 'TOTAL PRIMARY AIR FLOW', 'BURNER TILT POSITION',
        'FURNACE DRAFT SET POINT', 'PA HEADER PRESSURE SET POINT',
        'FD FAN A CURRENT', 'FD FAN B CURRENT', 'FDF-A BLADE PITCH', 'FDF-B BLADE PITCH',
        'FDF-A I/L SA TEMP', 'FDF-B I/L SA TEMP', 'FDF-A DISCHARGE PRESS',
        'FDF-B DISCHARGE PRESS', 'ID Fan A Current', 'ID Fan B Current', 'IDF-A I/L PRESS',
        'IDF-B I/L PRESS', 'IDF-A I/L TEMP', 'IDF-B I/L TEMP', 'IDF-A SCOOP POSITION',
        'IDF-B SCOOP POSITION', 'IDF-A SPEED', 'IDF-B SPEED', 'IDF-A DISCHARGE PRESS',
        'IDF-B DISCHARGE PRESS', 'PAF-A CURRENT', 'PAF-B CURRENT', 'PAF-A SCOOP POSITION',
        'PAF-B SCOOP POSITION', 'PAF-A SPEED', 'PAF-B SPEED', 'PAF-A DISCHARGE PRESS',
        'PAF-B DISCHARGE PRESS', 'ID FAN-A VFD CURRENT', 'ID FAN-B VFD CURRENT',
        'FG TEMP AT CHIMNEY', 'CHIMNEY NOX', 'CHIMNEY SOX', 'CHIMNEY SPM',
        'Radiation & Unaccounted Loss',

        {'Dry bulb Temp': ['AMBIENT TEMPERATURE'],
        'RH': ['RELATIVE HUMIDITY'],
        'Atmospheric pressure': ['AMBIENT PRESSURE'],
        'Avg. Flue Gas O2 - APH In': [
            'APH-A I/L FLUE GAS OXYGEN CONTENT',
            'APH-B I/L FLUE GAS OXYGEN CONTENT'
        ],
        'Avg. Flue Gas O2 - APH Out': [
            'APH-A O/L FLUE GAS OXYGEN CONTENT',
            'APH-B O/L FLUE GAS OXYGEN CONTENT'
        ],
        'Avg. Flue Gas Temp - APH In': [
            'APH-B I/L FLUE GAS TEMP-1',
            'APH-B I/L FLUE GAS TEMP-2'
        ],
        'Avg. Flue Gas Temp - APH Out': [
            'APH-B O/L FLUE GAS TEMP-1',
            'APH-B FLUE GAS O/L TEMP-2'
        ],
        'Primary Air to APH Temp In': [
            'APH-A PA I/L TEMP',
            'APH-B PA I/L TEMP'
        ],
        'Secondary Air to APH Temp In': [
            'APH -A SEC. AIR IN TEMP',
            'APH -B SEC. AIR IN TEMP'
        ],
        'Primary Air to APH Temp out': [
            'APH -A OUT PRI AIR TEMP',
            'APH -B OUT PRI AIR TEMP'
        ],
        'Secondary Air to APH Temp out': [
            'APH -A SEC AIR OUTLET TEMP',
            'APH -B SEC AIR OUTLET TEMP'
        ],
        'Total Secondary Air Flow': ['TOTAL SEC AIR FLOW'],
        'Total Primary Air Flow': ['TOTAL PRIMARY AIR FLOW'],}
        
    ]
    

    results = {}
    for param in parameters:
        row = df[df['PARAMETERS'].str.contains(param, na=False, regex=False)]
        if not row.empty:
            results[param] = {
                'Design': row['DESIGN'].iloc[0],
                'Operating': row['OPERATING'].iloc[0]
            }
   
        
    
    return results
import pandas as pd
import numpy as np


def boiler_efficiency_calculation(df):
    """
    Performs the full boiler efficiency calculation using input from Excel file `file_path`.
    Returns a dictionary with all computed losses, efficiency, and iterative info.
    """
    # 1. DATA LOAD
    # df = pd.read_excel(file_path, sheet_name="Boiler Inputs", skiprows=2, usecols=["PARAMETERS", "DESIGN", "OPERATING"])
    results = {}
    for i, row in df.iterrows():
        param = str(row["PARAMETERS"]).strip()
        results[param] = {
            'Design': row.get("DESIGN", np.nan),
            'Operating': row.get("OPERATING", np.nan),
        }

    def get(k, mode): return float(results[k][mode])

    def calculate_mass_fraction_water_vapor(ambient_temp_c, relative_humidity, atmospheric_pressure_bar):
        temp_f = (ambient_temp_c * 9/5) + 32
        Pv_sat_psi = (
            0.019257 +
            0.001289016 * temp_f +
            0.0000121122 * temp_f**2 +
            0.0000004534007 * temp_f**3 +
            0.0000000000684188 * temp_f**4 +
            0.00000000002197092 * temp_f**5
        )
        P_psi = atmospheric_pressure_bar * 14.5038
        numerator = 0.622 * (0.01 * relative_humidity * Pv_sat_psi)
        denominator = P_psi - (0.01 * relative_humidity * Pv_sat_psi)
        return numerator / denominator if denominator != 0 else 0.0

    def calculate_unburnt_c_in_ash(results):
        flyash_percent_d = float(results['% of Flyash to Total Ash']['Design'])
        flyash_unburnt_c_d = float(results['UNBURNT CARBON IN FLY ASH']['Design'])
        bottomash_unburnt_c_d = float(results['UNBURNT CARBON IN BOTTOM ASH']['Design'])
        bottomash_percent_d = float(results['% of Bottom ash to Total Ash']['Design'])
        flyash_percent_o = float(results['% of Flyash to Total Ash']['Operating'])
        flyash_unburnt_c_o = float(results['UNBURNT CARBON IN FLY ASH']['Operating'])
        bottomash_unburnt_c_o = float(results['UNBURNT CARBON IN BOTTOM ASH']['Operating'])
        bottomash_percent_o = float(results['% of Bottom ash to Total Ash']['Operating'])
        unburnt_ash_design = (flyash_percent_d / 100) * flyash_unburnt_c_d + \
                             (bottomash_percent_d / 100) * bottomash_unburnt_c_d
        unburnt_ash_operating = (flyash_percent_o / 100) * flyash_unburnt_c_o + \
                                (bottomash_percent_o / 100) * bottomash_unburnt_c_o
        return unburnt_ash_design, unburnt_ash_operating

    def adjust_flue_gas_temperature(TFgLv, CpA, CpG, TAEn, TFgLvCr_initial_assumed=None, max_iter=2000, tolerance=0.01, step_size=1):
        if TFgLvCr_initial_assumed is None:
            TFgLvCr_assumed = TFgLv
        else:
            TFgLvCr_assumed = TFgLvCr_initial_assumed
        for iteration in range(max_iter):
            TFgLvCr = TFgLv + (CpA / CpG) * (TFgLvCr_assumed - TAEn)
            deviation = TFgLvCr - TFgLvCr_assumed
            if abs(deviation) < tolerance:
                return TFgLvCr, iteration + 1
            TFgLvCr_assumed += step_size * deviation
        return TFgLvCr, max_iter # type: ignore # fail-safe

    try:
        # FUEL & SYSTEM DATA
        C_d = get('TOTAL CARBON IN COAL', 'Design')
        C_o = get('TOTAL CARBON IN COAL', 'Operating')
        H_d = get('HYDROGEN CONTENT IN COAL', 'Design')
        H_o = get('HYDROGEN CONTENT IN COAL', 'Operating')
        S_d = get('SULPHER CONTENT IN COAL', 'Design')
        S_o = get('SULPHER CONTENT IN COAL', 'Operating')
        O_d = get('OXYGEN CONTENT IN COAL', 'Design')
        O_o = get('OXYGEN CONTENT IN COAL', 'Operating')
        N_d = get('NITROGEN CONTENT IN COAL', 'Design')
        N_o = get('NITROGEN CONTENT IN COAL', 'Operating')
        M_d = get('MOISTURE CONTENT IN COAL', 'Design')
        M_o = get('MOISTURE CONTENT IN COAL', 'Operating')
        A_d = get('ASH CONTENT IN COAL', 'Design')
        A_o = get('ASH CONTENT IN COAL', 'Operating')
        GCV_d = get('GCV OF COAL', 'Design')
        GCV_o = get('GCV OF COAL', 'Operating')
        rad_loss_d = float(results.get('Radiation & Unaccounted Loss', {}).get('Design', 2.0))
        rad_loss_o = float(results.get('Radiation & Unaccounted Loss', {}).get('Operating', 2.0))
        # T_fg_d = 132.8
        # T_fg_o = 143.0
        # T_fg_d = get('APH-A O/L FLUE GAS TEMP-1', 'Design')
        # T_fg_o = get('APH-A O/L FLUE GAS TEMP-1', 'Operating')
                # Average Design temperature
        T_fg_d_1 = get('APH-B O/L FLUE GAS TEMP-1', 'Design')
        T_fg_d_2 = get('APH-B FLUE GAS O/L TEMP-2', 'Design')
        T_fg_d = (T_fg_d_1 + T_fg_d_2) / 2
        
        # Average Operating temperature
        T_fg_o_1 = get('APH-B O/L FLUE GAS TEMP-1', 'Operating')
        T_fg_o_2 = get('APH-B FLUE GAS O/L TEMP-2', 'Operating')
        T_fg_o = (T_fg_o_1 + T_fg_o_2) / 2
        T_amb_d = get('AMBIENT TEMPERATURE', 'Design')
        T_amb_o = get('AMBIENT TEMPERATURE', 'Operating')
        relhum_d = get('RELATIVE HUMIDITY', 'Design')
        relhum_o = get('RELATIVE HUMIDITY', 'Operating')
        ambp_d = get('AMBIENT PRESSURE', 'Design')
        ambp_o = get('AMBIENT PRESSURE', 'Operating')

        mf_water_d = calculate_mass_fraction_water_vapor(T_amb_d, relhum_d, ambp_d)
        mf_water_o = calculate_mass_fraction_water_vapor(T_amb_o, relhum_o, ambp_o)

        unburnt_ash_d, unburnt_ash_o = calculate_unburnt_c_in_ash(results)
        c_in_ash_per_kg_d = (A_d / 100) * (unburnt_ash_d / (100 - unburnt_ash_d))
        c_in_ash_per_kg_o = (A_o / 100) * (unburnt_ash_o / (100 - unburnt_ash_o))

        O_derived_d = 100 - (C_d + S_d + H_d + M_d + N_d + A_d)
        O_derived_o = 100 - (C_o + S_o + H_o + M_o + N_o + A_o)

        stoich_air_d = 0.1151 * (C_d - c_in_ash_per_kg_d * 100) + 0.3429 * H_d + 0.0431 * S_d - 0.0432 * O_derived_d
        stoich_air_o = 0.1151 * (C_o - c_in_ash_per_kg_o * 100) + 0.3429 * H_o + 0.0431 * S_o - 0.0432 * O_derived_o

        CpA = 1.0052
        CpG = 1.1
        TAEn_d = T_amb_d
        TAEn_o = T_amb_o
        TFgLvCr_d, iter_d = adjust_flue_gas_temperature(TFgLv=T_fg_d, CpA=CpA, CpG=CpG, TAEn=TAEn_d, step_size=5, tolerance=0.001, TFgLvCr_initial_assumed=T_fg_d + 5)
        TFgLvCr_o, iter_o = adjust_flue_gas_temperature(TFgLv=T_fg_o, CpA=CpA, CpG=CpG, TAEn=TAEn_o, step_size=5, tolerance=0.001, TFgLvCr_initial_assumed=T_fg_o + 5)

        dry_flue_gas_loss_d = (CpG * (TFgLvCr_d - T_amb_d) * 100) / (GCV_d * 4.184)
        dry_flue_gas_loss_o = (CpG * (TFgLvCr_o - T_amb_o) * 100) / (GCV_o * 4.184)

        carbon_loss_d = (c_in_ash_per_kg_d * 8077.8 * 100) / GCV_d
        carbon_loss_o = (c_in_ash_per_kg_o * 8077.8 * 100) / GCV_o

        moisture_fuel_loss_d = M_d * (2771.44 - 104.67) / (4.184 * GCV_d)
        moisture_fuel_loss_o = M_o * (2771.44 - 104.67) / (4.184 * GCV_o)

        hydrogen_loss_d = 0.425 * (2771.41 - 104.67) / (6300 * 4.184) * 100
        hydrogen_loss_o = 0.425 * (2771.41 - 104.67) / (6300 * 4.184) * 100

        moisture_in_air_loss_d = (100 * mf_water_d * 11.52 * 224.21 / (GCV_d * 4.184))
        moisture_in_air_loss_o = (100 * mf_water_d * 11.52 * 224.21 / (GCV_d * 4.184))

        total_loss_d = dry_flue_gas_loss_d + carbon_loss_d + moisture_fuel_loss_d + hydrogen_loss_d + moisture_in_air_loss_d + rad_loss_d
        total_loss_o = dry_flue_gas_loss_o + carbon_loss_o + moisture_fuel_loss_o + hydrogen_loss_o + moisture_in_air_loss_o + rad_loss_o
        boiler_eff_d = 100 - total_loss_d
        boiler_eff_o = 100 - total_loss_o

        # return {
        #     'Efficiency': {'Design': boiler_eff_d, 'Operating': boiler_eff_o},
        #     'Losses': {
        #         'Dry Flue Gas': {'Design': dry_flue_gas_loss_d, 'Operating': dry_flue_gas_loss_o},
        #         'Carbon': {'Design': carbon_loss_d, 'Operating': carbon_loss_o},
        #         'Moisture in Fuel': {'Design': moisture_fuel_loss_d, 'Operating': moisture_fuel_loss_o},
        #         'Hydrogen': {'Design': hydrogen_loss_d, 'Operating': hydrogen_loss_o},
        #         'Moisture in Air': {'Design': moisture_in_air_loss_d, 'Operating': moisture_in_air_loss_o},
        #         'Radiation': {'Design': rad_loss_d, 'Operating': rad_loss_o},
        #     },
        #     'Iterations': {'Design': iter_d, 'Operating': iter_o},
        #     'Corrected_Flue_Gas_Temp': {'Design': TFgLvCr_d, 'Operating': TFgLvCr_o}
        # }
        return {
            "C_in_ash_per_kg": {"Design": c_in_ash_per_kg_d, "Operating": c_in_ash_per_kg_o},
            "Dry_flue_gas_loss": {"Design": dry_flue_gas_loss_d, "Operating": dry_flue_gas_loss_o},
            "Carbon_loss": {"Design": carbon_loss_d, "Operating": carbon_loss_o},
            "Moisture_fuel_loss": {"Design": moisture_fuel_loss_d, "Operating": moisture_fuel_loss_o},
            "Hydrogen_fuel_loss": {"Design": hydrogen_loss_d, "Operating": hydrogen_loss_o},
            "Moisture_air_loss": {"Design": moisture_in_air_loss_d, "Operating": moisture_in_air_loss_o},
            "Radiation_loss": {"Design": rad_loss_d, "Operating": rad_loss_o},
            "Total_loss": {"Design": total_loss_d, "Operating": total_loss_o},
            "Boiler_efficiency": {"Design": boiler_eff_d, "Operating": boiler_eff_o},
            
        }
    except Exception as e:
        print(f"Error in calculations: {e}")
        return None


def print_boiler_efficiency_results(output):
    if output is None:
        print("No output to display.")
        return

    print("\n" + "="*60)
    print("BOILER EFFICIENCY AND LOSS BREAKDOWN")
    print("="*60)

    efficiencies = output.get('Efficiency', {})
    losses = output.get('Losses', {})
    iterations = output.get('Iterations', {})
    corrected_temps = output.get('Corrected_Flue_Gas_Temp', {})

    print(f"{'Parameter':<30} {'Design':>15} {'Operating':>15}")
    print("-"*60)
    print(f"{'Corrected Flue Gas Temp (°C)':<30} "
          f"{corrected_temps.get('Design', float('nan')):15.3f} "
          f"{corrected_temps.get('Operating', float('nan')):15.3f}")
    print(f"{'Iterations':<30} "
          f"{iterations.get('Design', 0):15d} "
          f"{iterations.get('Operating', 0):15d}")
    print()

    loss_order = ['Dry Flue Gas', 'Carbon', 'Moisture in Fuel', 'Hydrogen', 'Moisture in Air', 'Radiation']
    print(f"{'Loss Type':<30} {'Design (%)':>15} {'Operating (%)':>15}")
    print("-"*60)

    for loss_name in loss_order:
        loss_data = losses.get(loss_name, {})
        design_val = loss_data.get('Design', float('nan'))
        oper_val = loss_data.get('Operating', float('nan'))
        print(f"{loss_name:<30} {design_val:15.3f} {oper_val:15.3f}")

    print("-"*60)
    print(f"{'Total Efficiency (%)':<30} "
          f"{efficiencies.get('Design', float('nan')):15.3f} "
          f"{efficiencies.get('Operating', float('nan')):15.3f}")
    print("="*60 + "\n")


# === MAIN SCRIPT USAGE ===
if __name__ == "__main__":
    file_path = r"D:\PROJECT - THERMAL 2025\BOILER EFFICIENCY CODE\Performance Monitoring Tool updated.xlsx"
    output = boiler_efficiency_calculation(file_path)
    print_boiler_efficiency_results(output)

# def print_parameters(results):
#     """Print the parameter values (Design and Operating)"""
#     print("\n====== Boiler Parameters (Design vs Operating) ======\n")
#     for param, values in results.items():
#         print(f"{param:<45} | Design: {values['Design']:>10} | Operating: {values['Operating']:>10}")

# def calculate_saturation_vapor_pressure(ambient_temp_c):
#     """Calculate saturation vapor pressure based on ambient temperature in Celsius"""
#     ambient_temp_f = (ambient_temp_c * 9/5) + 32  # Convert Celsius to Fahrenheit
#     saturation_vapor_pressure = (
#         (0.019257 +
#          0.001289016 * ambient_temp_f +
#          0.0000121122 * ambient_temp_f**2 +
#          0.0000004534007 * ambient_temp_f**3 +
#          0.0000000000684188 * ambient_temp_f**4 +
#          0.00000000002197092 * ambient_temp_f**5) * 6894.76  # Convert psi to Pa
#     ) / 10**5  # Convert Pa to bar
#     return saturation_vapor_pressure



# """ def calculate_mass_fraction_water_vapor(ambient_temp_c, relative_humidity, atmospheric_pressure):
#     Calculate mass fraction of water vapor in dry air
#     ambient_temp_f = (ambient_temp_c * 9/5) + 32  # Convert Celsius to Fahrenheit
#     saturation_vapor_pressure = (
#         (0.019257 +
#          0.001289016 * ambient_temp_f +
#          0.0000121122 * ambient_temp_f**2 +
#          0.0000004534007 * ambient_temp_f**3 +
#          0.0000000000684188 * ambient_temp_f**4 +
#          0.00000000002197092 * ambient_temp_f**5) * 6894.76  # Convert psi to Pa
#     ) / 10**5  # Convert Pa to bar
#     # Calculate mass fraction of water vapor in dry air
#     mass_fraction = (0.622 * (0.01 * relative_humidity * saturation_vapor_pressure)) / \
#                     ((atmospheric_pressure * 100000) - (0.01 * relative_humidity * saturation_vapor_pressure))
#     return mass_fraction
#       """


# def calculate_mass_fraction_water_vapor(ambient_temp_c, relative_humidity, atmospheric_pressure_bar):
#     """
#     Calculate mass fraction of water vapor in dry air using updated Excel-style formula
#     Inputs:
#         ambient_temp_c (float): Ambient temperature in °C
#         relative_humidity (float): Relative humidity in %
#         atmospheric_pressure_bar (float): Pressure in bar
#     Returns:
#         mass_fraction (float): Water vapor mass fraction in dry air
#     """
#     # Convert temperature to Fahrenheit
#     temp_f = (ambient_temp_c * 9/5) + 32

#     # Saturation vapor pressure in psi using polynomial fit (Excel style)
#     Pv_sat_psi = (
#         0.019257 +
#         0.001289016 * temp_f +
#         0.0000121122 * temp_f**2 +
#         0.0000004534007 * temp_f**3 +
#         0.0000000000684188 * temp_f**4 +
#         0.00000000002197092 * temp_f**5
#     )

#     # Convert pressure from bar to psi
#     P_psi = atmospheric_pressure_bar * 14.5038

#     # Calculate numerator and denominator
#     numerator = 0.622 * (0.01 * relative_humidity * Pv_sat_psi)
#     denominator = P_psi - (0.01 * relative_humidity * Pv_sat_psi)

#     # Avoid division by zero
#     if denominator == 0:
#         return 0.0

#     mass_fraction = numerator / denominator
#     return mass_fraction





# def calculate_mass_fraction_wet_air(mass_fraction_water_vapor):
#     """Calculate mass fraction of water vapor in wet air"""
#     return mass_fraction_water_vapor / (1 + mass_fraction_water_vapor)

# def calculate_unburnt_c_in_ash(results):
#     unburnt_ash_design = None
#     unburnt_ash_operating = None
#     """Calculate Unburnt Carbon in Ash for Design and Operating conditions"""
#     try:
#         flyash_percent_d = float(results['% of Flyash to Total Ash']['Design'])
#         flyash_unburnt_c_d = float(results['UNBURNT CARBON IN FLY ASH']['Design'])
#         bottomash_unburnt_c_d = float(results['UNBURNT CARBON IN BOTTOM ASH']['Design'])
#         bottomash_percent_d = float(results['% of Bottom ash to Total Ash']['Design'])

#         flyash_percent_o = float(results['% of Flyash to Total Ash']['Operating'])
#         flyash_unburnt_c_o = float(results['UNBURNT CARBON IN FLY ASH']['Operating'])
#         bottomash_unburnt_c_o = float(results['UNBURNT CARBON IN BOTTOM ASH']['Operating'])
#         bottomash_percent_o = float(results['% of Bottom ash to Total Ash']['Operating'])

#         # Apply formula for both design and operating
#         unburnt_ash_design = (flyash_percent_d / 100) * flyash_unburnt_c_d + \
#                              (bottomash_percent_d / 100) * bottomash_unburnt_c_d

#         unburnt_ash_operating = (flyash_percent_o / 100) * flyash_unburnt_c_o + \
#                                 (bottomash_percent_o / 100) * bottomash_unburnt_c_o

#         print(f"\n✅ Calculated Unburnt Carbon in Ash:")
#         print(f"  Design:    {unburnt_ash_design:.2f} %")
#         print(f"  Operating: {unburnt_ash_operating:.2f} %")

#     except KeyError as e:
#         print(f"❌ Missing parameter: {e}")
#     except Exception as e:
#         print(f"❌ Error during calculation: {str(e)}")
    
    
#     return unburnt_ash_design, unburnt_ash_operating








# # def calculate_c_in_ash_per_kg_coal(results, unburnt_ash_design, unburnt_ash_operating):
# #     """Calculate C in ash per kg of coal for Design and Operating"""
# #     try:
# #         ash_content_d = float(results['ASH CONTENT IN COAL']['Design'])
# #         ash_content_o = float(results['ASH CONTENT IN COAL']['Operating'])

# #         # Apply formula: (Ash/100) * (Unburnt / (100 - Unburnt))
# #         c_in_ash_per_kg_d = (ash_content_d / 100) * (unburnt_ash_design / (100 - unburnt_ash_design))
# #         c_in_ash_per_kg_o = (ash_content_o / 100) * (unburnt_ash_operating / (100 - unburnt_ash_operating))

# #         print(f"\n✅ Calculated C in Ash per kg of Coal:")
# #         print(f"  Design:    {c_in_ash_per_kg_d:.5f} kg/kg")
# #         print(f"  Operating: {c_in_ash_per_kg_o:.5f} kg/kg")

# #     except KeyError as e:
# #         print(f"❌ Missing parameter: {e}")
# #     except ZeroDivisionError:
# #         print("❌ Division by zero occurred in unburnt ash percentage.")
# #     except Exception as e:
# #         print(f"❌ Error during calculation: {str(e)}")

# #def calculate_c_in_ash_and_stoichiometric_air(results, unburnt_ash_design, unburnt_ash_operating):
#     """Calculate C in ash per kg of coal, Stoichiometric Air, and Moles of Air for Design and Operating"""
#     try:
#         # --- Extract values from input dict ---
#         carbon_d = float(results['TOTAL CARBON IN COAL']['Design'])
#         carbon_o = float(results['TOTAL CARBON IN COAL']['Operating'])

#         hydrogen_d = float(results['HYDROGEN CONTENT IN COAL']['Design'])
#         hydrogen_o = float(results['HYDROGEN CONTENT IN COAL']['Operating'])

#         sulfur_d = float(results['SULPHER CONTENT IN COAL']['Design'])
#         sulfur_o = float(results['SULPHER CONTENT IN COAL']['Operating'])

#         moisture_d = float(results['MOISTURE CONTENT IN COAL']['Design'])
#         moisture_o = float(results['MOISTURE CONTENT IN COAL']['Operating'])

#         nitrogen_d = float(results['NITROGEN CONTENT IN COAL']['Design'])
#         nitrogen_o = float(results['NITROGEN CONTENT IN COAL']['Operating'])

#         ash_d = float(results['ASH CONTENT IN COAL']['Design'])
#         ash_o = float(results['ASH CONTENT IN COAL']['Operating'])

#         # ---- Step 1: C in ash per kg of coal ----
#         c_in_ash_per_kg_d = (ash_d / 100) * (unburnt_ash_design / (100 - unburnt_ash_design))
#         c_in_ash_per_kg_o = (ash_o / 100) * (unburnt_ash_operating / (100 - unburnt_ash_operating))

#         # ---- Step 2: Oxygen Content ----
#         oxygen_d = 100 - carbon_d - hydrogen_d - sulfur_d - moisture_d - nitrogen_d - ash_d
#         oxygen_o = 100 - carbon_o - hydrogen_o - sulfur_o - moisture_o - nitrogen_o - ash_o

#         # ---- Step 3: Stoichiometric air (kg/kg fuel) ----
#         U_d = c_in_ash_per_kg_d * 100  # Unburnt C in %
#         U_o = c_in_ash_per_kg_o * 100

#         stoich_air_d = (0.1151 * (carbon_d - U_d)) + (0.3429 * hydrogen_d) + (0.0431 * sulfur_d) - (0.0432 * oxygen_d)
#         stoich_air_o = (0.1151 * (carbon_o - U_o)) + (0.3429 * hydrogen_o) + (0.0431 * sulfur_o) - (0.0432 * oxygen_o)

#         # ---- Step 4: Moles of air ----
#         MW_air = 28.9625  # kg/kmol
#         moles_air_d = stoich_air_d / MW_air
#         moles_air_o = stoich_air_o / MW_air

#         # ---- Output Results ----
#         print(f"\n✅ C in Ash per kg of Coal:")
#         print(f"  Design:    {c_in_ash_per_kg_d:.5f} kg/kg")
#         print(f"  Operating: {c_in_ash_per_kg_o:.5f} kg/kg")

#         print(f"\n✅ Stoichiometric Air Required:")
#         print(f"  Design:    {stoich_air_d:.4f} kg air/kg fuel")
#         print(f"  Operating: {stoich_air_o:.4f} kg air/kg fuel")

#         print(f"\n✅ Moles of Stoichiometric Air:")
#         print(f"  Design:    {moles_air_d:.4f} kmol/kg fuel")
#         print(f"  Operating: {moles_air_o:.4f} kmol/kg fuel")

#         return {
#             "C_in_ash_kg_coal": {
#                 "Design": c_in_ash_per_kg_d,
#                 "Operating": c_in_ash_per_kg_o
#             },
#             "Stoichiometric_air": {
#                 "Design": stoich_air_d,
#                 "Operating": stoich_air_o
#             },
#             "Moles_of_air": {
#                 "Design": moles_air_d,
#                 "Operating": moles_air_o
#             }
#         }

#     except KeyError as e:
#         print(f"❌ Missing parameter: {e}")
#     except ZeroDivisionError:
#         print("❌ Division by zero occurred due to unburnt ash percentage.")
#     except Exception as e:
#         print(f"❌ Error during calculation: {str(e)}")
# def calculate_combustion_metrics(results, unburnt_ash_design, unburnt_ash_operating):
#     """Calculate combustion metrics, all losses, and boiler efficiency."""

#     try:
#         def convert_c_to_f(temp_c):
#             return (temp_c * 9/5) + 32

#         # Extract required values
#         C_d = float(results['TOTAL CARBON IN COAL']['Design'])
#         C_o = float(results['TOTAL CARBON IN COAL']['Operating'])
#         H_d = float(results['HYDROGEN CONTENT IN COAL']['Design'])
#         H_o = float(results['HYDROGEN CONTENT IN COAL']['Operating'])
#         S_d = float(results['SULPHER CONTENT IN COAL']['Design'])
#         S_o = float(results['SULPHER CONTENT IN COAL']['Operating'])
#         O_d = float(results['OXYGEN CONTENT IN COAL']['Design'])
#         O_o = float(results['OXYGEN CONTENT IN COAL']['Operating'])
#         N_d = float(results['NITROGEN CONTENT IN COAL']['Design'])
#         N_o = float(results['NITROGEN CONTENT IN COAL']['Operating'])
#         M_d = float(results['MOISTURE CONTENT IN COAL']['Design'])
#         M_o = float(results['MOISTURE CONTENT IN COAL']['Operating'])
#         A_d = float(results['ASH CONTENT IN COAL']['Design'])
#         A_o = float(results['ASH CONTENT IN COAL']['Operating'])
#         mf_d = float(results.get('MASS FRACTION OF WATER VAPOR', {}).get('Design', 0))
#         mf_o = float(results.get('MASS FRACTION OF WATER VAPOR', {}).get('Operating', 0))
#         GCV_d = float(results['GCV OF COAL']['Design'])
#         GCV_o = float(results['GCV OF COAL']['Operating'])
#         radiation_loss_d = float(results.get('Radiation & Unaccounted Loss', {}).get('Design', 0))
#         radiation_loss_o = float(results.get('Radiation & Unaccounted Loss', {}).get('Operating', 0))

#         # 1. C in ash per kg of coal
#         c_in_ash_per_kg_d = (A_d / 100) * (unburnt_ash_design / (100 - unburnt_ash_design))
#         c_in_ash_per_kg_o = (A_o / 100) * (unburnt_ash_operating / (100 - unburnt_ash_operating))

#         # --- Loss calculations ---
#         try:
#             T_fg_d = float(results['FG TEMP AT CHIMNEY']['Design'])
#             T_fg_o = float(results['FG TEMP AT CHIMNEY']['Operating'])
#         except Exception:
#             T_fg_d = 150
#             T_fg_o = 150
#         try:
#             T_ambient_d = float(results['AMBIENT TEMPERATURE']['Design'])
#             T_ambient_o = float(results['AMBIENT TEMPERATURE']['Operating'])
#         except Exception:
#             T_ambient_d = 25
#             T_ambient_o = 25
#         Cp_dry_flue_gas = 0.24  # kcal/kg.K
#         dry_flue_gas_loss_d = (Cp_dry_flue_gas * (T_fg_d - T_ambient_d) * 100) / GCV_d
#         dry_flue_gas_loss_o = (Cp_dry_flue_gas * (T_fg_o - T_ambient_o) * 100) / GCV_o

#         # 2. Carbon Loss (%)
#         carbon_loss_d = (c_in_ash_per_kg_d * 100) / GCV_d
#         carbon_loss_o = (c_in_ash_per_kg_o * 100) / GCV_o

#         # 3. Moisture in Fuel Loss (%)
#         moisture_fuel_d = (M_d * 586 * 100) / (100 * GCV_d)
#         moisture_fuel_o = (M_o * 586 * 100) / (100 * GCV_o)

#         # 4. Hydrogen Loss (%)
#         hydrogen_loss_d = (9 * H_d * 586 * 100) / (100 * GCV_d)
#         hydrogen_loss_o = (9 * H_o * 586 * 100) / (100 * GCV_o)

#         # 5. Moisture in Air Loss (%)
#         moisture_air_d = (mf_d * 586 * 100) / GCV_d
#         moisture_air_o = (mf_o * 586 * 100) / GCV_o

#         # 6. Radiation Loss (%)
#         radiation_loss = radiation_loss_d  # or use average if both are present

#         # 7. Total Loss (%)
#         total_loss_d = dry_flue_gas_loss_d + carbon_loss_d + moisture_fuel_d + hydrogen_loss_d + moisture_air_d + radiation_loss
#         total_loss_o = dry_flue_gas_loss_o + carbon_loss_o + moisture_fuel_o + hydrogen_loss_o + moisture_air_o + radiation_loss

#         # 8. Boiler Efficiency (%)
#         boiler_eff_d = 100 - total_loss_d
#         boiler_eff_o = 100 - total_loss_o

#         print("\n===== Boiler Losses and Efficiency =====")
#         print(f"Dry Flue Gas Loss: [Design]: {dry_flue_gas_loss_d:.2f}%, [Operating]: {dry_flue_gas_loss_o:.2f}%")
#         print(f"Carbon Loss:       [Design]: {carbon_loss_d:.2f}%, [Operating]: {carbon_loss_o:.2f}%")
#         print(f"Moisture Fuel:     [Design]: {moisture_fuel_d:.2f}%, [Operating]: {moisture_fuel_o:.2f}%")
#         print(f"Hydrogen Fuel:     [Design]: {hydrogen_loss_d:.2f}%, [Operating]: {hydrogen_loss_o:.2f}%")
#         print(f"Moisture Air:      [Design]: {moisture_air_d:.2f}%, [Operating]: {moisture_air_o:.2f}%")
#         print(f"Radiation Loss:    [Design]: {radiation_loss:.2f}%, [Operating]: {radiation_loss:.2f}%")
#         print(f"Total Loss:        [Design]: {total_loss_d:.2f}%, [Operating]: {total_loss_o:.2f}%")
#         print(f"Boiler Efficiency: [Design]: {boiler_eff_d:.3f}%, [Operating]: {boiler_eff_o:.3f}%")

#         return {
#             "C_in_ash_per_kg": {"Design": c_in_ash_per_kg_d, "Operating": c_in_ash_per_kg_o},
#             "Dry_flue_gas_loss": {"Design": dry_flue_gas_loss_d, "Operating": dry_flue_gas_loss_o},
#             "Carbon_loss": {"Design": carbon_loss_d, "Operating": carbon_loss_o},
#             "Moisture_fuel_loss": {"Design": moisture_fuel_d, "Operating": moisture_fuel_o},
#             "Hydrogen_fuel_loss": {"Design": hydrogen_loss_d, "Operating": hydrogen_loss_o},
#             "Moisture_air_loss": {"Design": moisture_air_d, "Operating": moisture_air_o},
#             "Radiation_loss": {"Design": radiation_loss, "Operating": radiation_loss},
#             "Total_loss": {"Design": total_loss_d, "Operating": total_loss_o},
#             "Boiler_efficiency": {"Design": boiler_eff_d, "Operating": boiler_eff_o},
#             "Unburnt_C_in_ash": {
#                 "Design": unburnt_ash_design, "Operating": unburnt_ash_operating },
            
#         }
#     except KeyError as e:
#         print(f"❌ Missing parameter: {e}")
#     except ZeroDivisionError:
#         print("❌ Division by zero occurred in unburnt ash percentage or excess air calculation.")
#     except Exception as e:
#         print(f"❌ Error during calculation: {str(e)}")
#     return None

# def adjust_flue_gas_temperature(df, max_iter=20, tolerance=0.1):
#     """
#     Adjust 'TFgLvCr (assumed)' in the DataFrame until deviation between
#     assumed and calculated flue gas exit temperature becomes zero.
#     Uses direct substitution (TFgLvCr_assumed = TFgLvCr) for fast convergence.
#     Prints all iteration outputs and returns the number of iterations and final deviation.
#     """
#     TFgLv = float(df.loc["Temp. of flue Gas at APH Exit (0C)", "Values (D)"])
#     CpA = float(df.loc["Cp air", "Values (D)"])
#     CpG = float(df.loc["Cp of Flue gas", "Values (D)"])
#     TAEn = float(df.loc["Weighted Temp Air In", "Values (D)"])
#     TFgLvCr_assumed = float(df.loc["Temp. of flue Gas at APH Exit Corrected (Assumed)", "Values (D)"])

#     for iteration in range(max_iter):
#         TFgLvCr = TFgLv + (CpA / CpG) * (TFgLvCr_assumed - TAEn)
#         deviation = TFgLvCr - TFgLvCr_assumed
#         print(f"Iter {iteration}: TFgLvCr={TFgLvCr:.3f}, Assumed={TFgLvCr_assumed:.3f}, Deviation={deviation:.5f}")
#         if abs(deviation) < tolerance:
#             print(f"✅ Converged at iteration {iteration}")
#             df.loc["Temp. of flue Gas at APH Exit Corrected(0C) (Formula as per PTC 4)", "Values (D)"] = TFgLvCr
#             df.loc["Deviation", "Values (D)"] = 0.0
#             return iteration + 1, TFgLvCr, 0.0  # Return number of iterations, final value, and deviation
#         TFgLvCr_assumed = TFgLvCr  # Direct substitution for fast convergence
#     print("❌ Did not converge within limit.")
#     df.loc["Deviation", "Values (D)"] = deviation
#     return max_iter, TFgLvCr, deviation


def calculate_aph_parameters(df):

    param_map = {
        'Dry bulb Temp': ['AMBIENT TEMPERATURE'],
        'RH': ['RELATIVE HUMIDITY'],
        'Atmospheric pressure': ['AMBIENT PRESSURE'],
        'Avg. Flue Gas O2 - APH In': [
            'APH-A I/L FLUE GAS OXYGEN CONTENT',
            'APH-B I/L FLUE GAS OXYGEN CONTENT'
        ],
        'Avg. Flue Gas O2 - APH Out': [
            'APH-A O/L FLUE GAS OXYGEN CONTENT',
            'APH-B O/L FLUE GAS OXYGEN CONTENT'
        ],
        'Avg. Flue Gas Temp - APH In': [
            'APH-B I/L FLUE GAS TEMP-1',
            'APH-B I/L FLUE GAS TEMP-2'
        ],
        'Avg. Flue Gas Temp - APH Out': [
            'APH-B O/L FLUE GAS TEMP-1',
            'APH-B FLUE GAS O/L TEMP-2'
        ],
        'Primary Air to APH Temp In': [
            'APH-A PA I/L TEMP',
            'APH-B PA I/L TEMP'
        ],
        'Secondary Air to APH Temp In': [
            'APH -A SEC. AIR IN TEMP',
            'APH -B SEC. AIR IN TEMP'
        ],
        'Primary Air to APH Temp out': [
            'APH -A OUT PRI AIR TEMP',
            'APH -B OUT PRI AIR TEMP'
        ],
        'Secondary Air to APH Temp out': [
            'APH -A SEC AIR OUTLET TEMP',
            'APH -B SEC AIR OUTLET TEMP'
        ],
        'Total Secondary Air Flow': ['TOTAL SEC AIR FLOW'],
        'Total Primary Air Flow': ['TOTAL PRIMARY AIR FLOW'],
    }

    results = {}
    for calc_param, sheet_params in param_map.items():
        vals_design = []
        vals_actual = []
        for sheet_param in sheet_params:
            row = df[df['PARAMETERS'].str.strip().str.upper() == sheet_param.strip().upper()]
            if not row.empty:
                vals_design.append(row['Values (D)'].iloc[0])
                vals_actual.append(row['VALUES (O)'].iloc[0])
        if vals_design and vals_actual:
            results[calc_param] = {
                'Design': sum(vals_design) / len(vals_design),
                'Actual': sum(vals_actual) / len(vals_actual)
            }
        else:
            results[calc_param] = {'Design': float('nan'), 'Actual': float('nan')}

    def calculate_aph_leakage(o2_out, o2_in):
        return ((o2_out - o2_in)/(21 - o2_out)) * 90

    # Air flow ratios
    total_air_design = results['Total Primary Air Flow']['Design'] + results['Total Secondary Air Flow']['Design']
    total_air_actual = results['Total Primary Air Flow']['Actual'] + results['Total Secondary Air Flow']['Actual']
    sec_air_ratio_design = results['Total Secondary Air Flow']['Design'] / total_air_design
    sec_air_ratio_actual = results['Total Secondary Air Flow']['Actual'] / total_air_actual
    pri_air_ratio_design = results['Total Primary Air Flow']['Design'] / total_air_design
    pri_air_ratio_actual = results['Total Primary Air Flow']['Actual'] / total_air_actual

    # APH Inlet/Outlet Temp averages
    aph_inlet_temp_design = (sec_air_ratio_design * results['Secondary Air to APH Temp In']['Design'] +
                             pri_air_ratio_design * results['Primary Air to APH Temp In']['Design']) / (sec_air_ratio_design + pri_air_ratio_design)
    aph_inlet_temp_actual = (sec_air_ratio_actual * results['Secondary Air to APH Temp In']['Actual'] +
                             pri_air_ratio_actual * results['Primary Air to APH Temp In']['Actual']) / (sec_air_ratio_actual + pri_air_ratio_actual)
    aph_outlet_temp_design = (sec_air_ratio_design * results['Secondary Air to APH Temp out']['Design'] +
                              pri_air_ratio_design * results['Primary Air to APH Temp out']['Design']) / (sec_air_ratio_design + pri_air_ratio_design)
    aph_outlet_temp_actual = (sec_air_ratio_actual * results['Secondary Air to APH Temp out']['Actual'] +
                              pri_air_ratio_actual * results['Primary Air to APH Temp out']['Actual']) / (sec_air_ratio_actual + pri_air_ratio_actual)

    # APH Leakage
    o2_in_design = results['Avg. Flue Gas O2 - APH In']['Design']
    o2_out_design = results['Avg. Flue Gas O2 - APH Out']['Design']
    o2_in_actual = results['Avg. Flue Gas O2 - APH In']['Actual']
    o2_out_actual = results['Avg. Flue Gas O2 - APH Out']['Actual']
    aph_leakage_design = calculate_aph_leakage(o2_out_design, o2_in_design)
    aph_leakage_actual = calculate_aph_leakage(o2_out_actual, o2_in_actual)

    def convert_c_to_f(celsius):
        return (celsius * 9/5) + 32

    def calculate_cp_air(temp_f):
        term1 = -0.000000000005 * (2 * temp_f - 77)**3
        term2 = 0.00000001 * (2 * temp_f - 77)**2
        term3 = 0.0000002 * (2 * temp_f - 77)
        term4 = 0.24
        return (term1 + term2 + term3 + term4) * 4.184

    temp1_f_design = convert_c_to_f(aph_inlet_temp_design)
    temp2_f_design = convert_c_to_f(results['Primary Air to APH Temp In']['Design'])
    cp_air_design = (calculate_cp_air(temp1_f_design) + calculate_cp_air(temp2_f_design)) / 2

    temp1_f_actual = convert_c_to_f(aph_inlet_temp_actual)
    temp2_f_actual = convert_c_to_f(results['Primary Air to APH Temp In']['Actual'])
    cp_air_actual = (calculate_cp_air(temp1_f_actual) + calculate_cp_air(temp2_f_actual)) / 2

    def calculate_cp_flue_gas(temp_c):
        temp_f = convert_c_to_f(temp_c)
        cp1 = (0.00002 * (2 * temp_f - 77) + 0.2343) * 4.184
        cp2 = (0.00002 * (2 * convert_c_to_f(temp_c + 5) - 77) + 0.2343) * 4.184
        return (cp1 + cp2) / 2

    cp_flue_gas_design = calculate_cp_flue_gas(results['Avg. Flue Gas Temp - APH Out']['Design'])
    cp_flue_gas_actual = calculate_cp_flue_gas(results['Avg. Flue Gas Temp - APH Out']['Actual'])

    # Corrected APH Exit Temperature
    flue_gas_exit_temp_design = (aph_leakage_design * cp_air_design * (results['Avg. Flue Gas Temp - APH Out']['Design'] - aph_inlet_temp_design) / (cp_flue_gas_design * 100)) + results['Avg. Flue Gas Temp - APH Out']['Design']
    flue_gas_exit_temp_actual = (aph_leakage_actual * cp_air_actual * (results['Avg. Flue Gas Temp - APH Out']['Actual'] - aph_inlet_temp_actual) / (cp_flue_gas_actual * 100)) + results['Avg. Flue Gas Temp - APH Out']['Actual']

    # Gas side efficiency
    gas_side_eff_design = ((results['Avg. Flue Gas Temp - APH In']['Design'] - flue_gas_exit_temp_design) * 100 /
                           (results['Avg. Flue Gas Temp - APH In']['Design'] - aph_inlet_temp_design))
    gas_side_eff_actual = ((results['Avg. Flue Gas Temp - APH In']['Actual'] - flue_gas_exit_temp_actual) * 100 /
                           (results['Avg. Flue Gas Temp - APH In']['Actual'] - aph_inlet_temp_actual))

    # X Ratio
    denom_design = aph_outlet_temp_design - aph_inlet_temp_design
    denom_actual = aph_outlet_temp_actual - aph_inlet_temp_actual
    x_ratio_design = (results['Avg. Flue Gas Temp - APH In']['Design'] - flue_gas_exit_temp_design) / denom_design if denom_design != 0 else float('nan')
    x_ratio_actual = (results['Avg. Flue Gas Temp - APH In']['Actual'] - flue_gas_exit_temp_actual) / denom_actual if denom_actual != 0 else float('nan')

    # Return only required parameters
    return {
        "Temp. of flue Gas at APH Exit (TFgLv)": {
            "Design": results['Avg. Flue Gas Temp - APH Out']['Design'],
            "Actual": results['Avg. Flue Gas Temp - APH Out']['Actual']
        },
        "Temp. of flue Gas at APH Exit Corrected (TFgLvCr)": {
            "Design": flue_gas_exit_temp_design,
            "Actual": flue_gas_exit_temp_actual
        },
        "APH Leakage (AL)": {
            "Design": aph_leakage_design,
            "Actual": aph_leakage_actual
        },
        "Gas side efficiency (ηg)": {
            "Design": gas_side_eff_design,
            "Actual": gas_side_eff_actual
        },
        "X-Ratio": {
            "Design": x_ratio_design,
            "Actual": x_ratio_actual
        }
    }



# # Example usage
# if __name__ == "__main__":
#     file_path = r"C:\Users\118391\Downloads\Performance Monitoring Tool updated 1.xlsx"

#     results = load_extended_plant_data(file_path)
   
#     # print_parameters(results)

#     # # Calculate saturation vapor pressure using the design value of ambient temperature
#     # ambient_temp_design = results['AMBIENT TEMPERATURE']['Design']
#     # saturation_vapor_pressure = calculate_saturation_vapor_pressure(float(ambient_temp_design))
    
#     # print(f"\nSaturation Vapor Pressure of Moisture at Design Ambient Temperature ({ambient_temp_design} °C): {saturation_vapor_pressure:.4f} bar")

    
#     # # From your earlier code
#     # # # Calculate mass fraction of water vapor using the design values and operating
#     # ambient_temp_design = float(results['AMBIENT TEMPERATURE']['Design'])
#     # relative_humidity_design = float(results['RELATIVE HUMIDITY']['Design'])
#     # atmospheric_pressure_design = float(results['AMBIENT PRESSURE']['Design'])

#     # ambient_temp_operating = float(results['AMBIENT TEMPERATURE']['Operating'])
#     # relative_humidity_operating = float(results['RELATIVE HUMIDITY']['Operating'])
#     # atmospheric_pressure_operating = float(results['AMBIENT PRESSURE']['Operating'])

#     # mf_water_dry_design = calculate_mass_fraction_water_vapor(
#     #     ambient_temp_design,
#     #     relative_humidity_design,
#     #     atmospheric_pressure_design
#     # )

#     # mf_water_dry_operating = calculate_mass_fraction_water_vapor(
#     #     ambient_temp_operating,
#     #     relative_humidity_operating,
#     #     atmospheric_pressure_operating
#     # )

#     # print(f"\nMass Fraction of Water Vapor (Design):    {mf_water_dry_design:.6f}")
#     # print(f"Mass Fraction of Water Vapor (Operating): {mf_water_dry_operating:.6f}")
 


#     calculate_unburnt_c_in_ash(results)

#     unburnt_c_d, unburnt_c_o = calculate_unburnt_c_in_ash(results)

#     output = calculate_combustion_metrics(results, unburnt_c_d, unburnt_c_o)

#     # if output is not None:  //working
#     #     moles_design = output["Moles_of_air"]["Design"]
#     #     print(f"Moles of Stoichiometric Air (Design): {moles_design}")
#     #     moles_operating = output["Moles_of_air"]["Operating"]
#     #     print(f"Moles of Stoichiometric Air (Operating): {moles_operating}")

#     # else:
#     #     print("⚠️ Calculation failed. Check input data or missing keys.")

#     # Example DataFrame for dry flue gas calculation (replace with actual values as needed)
#     # data = {
#     #     "Values (D)": {
#     #         "Temp. of flue Gas at APH Exit (0C)": 143.85,
#     #         "Cp air": 0.24,
#     #         "Cp of Flue gas": 0.25,
#     #         "Weighted Temp Air In": 40.0,
#     #         "Temp. of flue Gas at APH Exit Corrected (Assumed)": 140.0
#     #     }
#     # }
#     # df = pd.DataFrame(data)

#     # # Run the what-if iteration for dry flue gas
#     # print("\n--- What-if Iteration for Dry Flue Gas ---")
#     # num_iterations, final_TFgLvCr, final_deviation = adjust_flue_gas_temperature(df)
#     # print(f"\nNumber of iterations for deviation 0: {num_iterations}")
#     # print(f"Final Corrected Flue Gas Temperature: {final_TFgLvCr:.3f} °C")
#     # print(f"Final Deviation: {final_deviation:.5f}")










