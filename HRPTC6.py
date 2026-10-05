from collections import namedtuple
import pandas as pd
from iapws import IAPWS97
import numpy as np

# Helper functions

def mpato_bar(mp):
    return mp * 10  # 1 MPa = 10 bar

def tph_to_kgph(tph):
    return tph * 1000  # 1 TPH = 1000 kg/hr

def avg_temp(t1, t2):
    return (t1 + t2) / 2
def gauge_to_absolute_pressure(gauge_pressure_bar):
    return (1.013 * 100 + gauge_pressure_bar) / 100
def maptLP_bar(mp):
    return mp * 10 + 1.013



from iapws import IAPWS97

def get_enthalpy(pressure_bar_g, temperature_c):
    """
    Calculate steam enthalpy using IAPWS-97 from gauge pressure in bar and temperature in °C.
    Converts gauge pressure to absolute MPa.
    """
    pressure_mpa_abs = pressure_bar_g /10   # Convert bar(g) to MPa(abs)
    temp_k = temperature_c + 273.15

    steam = IAPWS97(P=pressure_mpa_abs, T=temp_k)
    return steam.h  # Enthalpy in kJ/kg
def get_saturation_temperature(pressure_bar):
    """
    Calculate saturation temperature (°C) of steam at a given pressure in bar.
    
    Parameters:
    pressure_bar (float): Steam pressure in bar
    
    Returns:
    float: Saturation temperature in °C
    """
    pressure_mpa = pressure_bar / 10  # Convert bar to MPa
    water = IAPWS97(P=pressure_mpa, x=0)  # x=0 means saturated liquid, x=1 would mean saturated vapor
    return water.T - 273.15  # Convert from Kelvin to °C
def hV_p(p_mpa):
    return IAPWS97(P=p_mpa, x=1).h

def get_enthalpy_saturated_vapor_temp(temp_c):
    """
    Returns enthalpy of saturated steam at given temperature (°C).
    """
    T = temp_c + 273.15
    steam = IAPWS97(T=T, x=1)  # x=1 means saturated vapor
    return steam.h


def get_enthalpy_saturated_liquid(pressure_bar):
    """
    Enthalpy of saturated liquid at given pressure
    """
    pressure_mpa = pressure_bar / 10
    steam = IAPWS97(P=pressure_mpa, x=0)  # x=0 means saturated liquid
    return steam.h
from iapws import IAPWS97

def get_enthalpy_saturated_liquid_temp(temp_c):
    """
    Returns enthalpy of saturated liquid water at given temperature (°C).
    """
    T = temp_c + 273.15
    water = IAPWS97(T=T, x=0)  # x=0 means saturated liquid
    return water.h
from iapws import IAPWS97
from scipy.optimize import root_scalar

def get_enthalpy_from_volume_pressure(V, p_mpa):
    """
    Returns enthalpy (kJ/kg) for given specific volume (m³/kg) and pressure (MPa).
    """
    f = lambda T: IAPWS97(P=p_mpa, T=T).v - V
    res = root_scalar(f, bracket=[274.15, 1073.15], method='brentq')
    return IAPWS97(P=p_mpa, T=res.root).h if res.converged else None


def hL_p(pressure_bar):
      # from Excel
    pressure_mpa = pressure_bar / 10 
    return IAPWS97(P=pressure_mpa, x=0).h


def hV_p(pressure_bar):
    pressure_mpa = pressure_bar / 10
    
    """Returns saturated vapor enthalpy at given pressure (MPa)."""
    return IAPWS97(P=pressure_mpa, x=1).h




# Load data from Excel or CSV file with a header skip since your file has metadata on top
def load_input_data(file_path):
    df = pd.read_excel(file_path, usecols=["S. No.","PARAMETERS","UoM","DESIGN","UoM","Values (D)","UoM", "OPERATING","UoM","VALUES (O)"])
    #print(df.head())
    #S. No.	PARAMETERS	UoM	DESIGN	UoM	Values (D)	UoM	OPERATING	UoM	VALUES (O)

    #= df.dropna(subset=["PARAMETERS"])  # drop empty rows
    df = df.set_index("PARAMETERS")
    return df
ThermalResults = namedtuple('ThermalResults', [
    'Load_MW', 'Hms', 'Hrh', 'Hcrh', 'Hrhspray', 'MFWii', 'MFWfi','MRHspray','HHPH8o','HHPH6i','MSHspray',
    'MHPH8EXT', 'MHPH7EXT', 'MHPH6EXT', 'MDAEXT', 'HDEAo','MSspray', 
    'Mw_o',  'Hms_o', 'Hrh_o', 'Hcrh_o', 'Hrhspray_o', 'MFWii_o', 'MFWfi_o', 'MRHspray_o',
    'HHPH8o_o', 'HHPH6i_o', 'MSHspray_o', 'MHPH8EXT_o', 'MHPH7EXT_o', 'MHPH6EXT_o', 'MDAEXT_o', 'HDEAo_o','MCDSTDi','MCDSTDi_o',
])
ThermalResults2 = namedtuple('ThermalResults2',['MFWii', 'MFWfi','max_iter','MRH','HR','Ms','Hms','MDAEXT','MHPH6EXT',])
ThermalResults3 = namedtuple('ThermalResults3',['MFWii_o','MFWfi_o','iteration',"MRH_o",'HR_o','Ms_o','Hms_o','MHPH6EXT_o','MDAEXT_o',])
ThermalresultsHeater = namedtuple('ThermalresultsHeaters', ["MHPH1EXT", "MHPH2EXT", "MHPH3EXT", "MHPH4EXT",'MHPH1EXT_o', "MHPH2EXT_o", "MHPH3EXT_o", "MHPH4EXT_o","Extraction_steam_flowGSC","Extraction_steam_flowGSC_o","GSCD","GSCD_o",
                                                            "LP1HDEAo","LP1HDEAo_o",'Saturation_Temp_of_extraction_steamHPH8',"Saturation_Temp_of_extraction_steamHPH8_o",
                                                            "Saturation_Temp_of_extraction_steamHPH7","Saturation_Temp_of_extraction_steamHPH7_o","Saturation_Temp_of_extraction_steamHPH6","Saturation_Temp_of_extraction_steamHPH6_o",
                                                            'Saturation_Temp_of_extraction_steamHPH5','Saturation_Temp_of_extraction_steamHPH5_o','Saturation_Temp_of_extraction_steamLPH4',"Saturation_Temp_of_extraction_steamLPH4_o",
                                                            'Saturation_Temp_of_extraction_steamLPH3','Saturation_Temp_of_extraction_steamLPH3_o','Saturation_Temp_of_extraction_steamLPH2','Saturation_Temp_of_extraction_steamLPH2_o',
                                                            'Saturation_Temp_of_extraction_steamLPH1','Saturation_Temp_of_extraction_steamLPH1_o','Saturation_Temp_of_extraction_steamGSC','Saturation_Temp_of_extraction_steamGSC_o',
                                                            'Feed_water_Temp_RiseHPH8','Feed_water_Temp_RiseHPH8_o','Feed_water_Temp_RiseHPH7','Feed_water_Temp_RiseHPH7_o','Feed_water_Temp_RiseHPH6','Feed_water_Temp_RiseHPH6_o',
                                                            'Feed_water_Temp_RiseHPH5','Feed_water_Temp_RiseHPH5_o','Feed_water_Temp_RiseLPH4','Feed_water_Temp_RiseLPH4_o','Feed_water_Temp_RiseLPH3','Feed_water_Temp_RiseLPH3_o',
                                                            'Feed_water_Temp_RiseLPH2','Feed_water_Temp_RiseLPH2_o','Feed_water_Temp_RiseLPH1','Feed_water_Temp_RiseLPH1_o','Feed_water_Temp_RiseGSC','Feed_water_Temp_RiseGSC_o',
                                                            'Terminal_Temp_DiffHPH8','Terminal_Temp_DiffHPH8_o','Terminal_Temp_DiffHPH7','Terminal_Temp_DiffHPH7_o','Terminal_Temp_DiffHPH6','Terminal_Temp_DiffHPH6_o',
                                                            'Terminal_Temp_DiffHPH5','Terminal_Temp_DiffHPH5_o','Terminal_Temp_DiffLPH4','Terminal_Temp_DiffLPH4_o','Terminal_Temp_DiffLPH3','Terminal_Temp_DiffLPH3_o',
                                                            'Terminal_Temp_DiffLPH2','Terminal_Temp_DiffLPH2_o','Terminal_Temp_DiffLPH1','Terminal_Temp_DiffLPH1_o','Terminal_Temp_DiffGSC','Terminal_Temp_DiffGSC_o',
                                                            'Drain_Cooler_Approach_TempHPH8','Drain_Cooler_Approach_TempHPH8_o','Drain_Cooler_Approach_TempHPH7','Drain_Cooler_Approach_TempHPH7_o',
                                                            'Drain_Cooler_Approach_TempHPH6','Drain_Cooler_Approach_TempHPH6_o','Drain_Cooler_Approach_TempLPH4','Drain_Cooler_Approach_TempLPH4_o',
                                                            'Drain_Cooler_Approach_TempLPH3','Drain_Cooler_Approach_TempLPH3_o','Drain_Cooler_Approach_TempLPH2','Drain_Cooler_Approach_TempLPH2_o',
                                                            'Drain_Cooler_Approach_TempLPH1','Drain_Cooler_Approach_TempLPH1_o','Drain_Cooler_Approach_TempGSC','Drain_Cooler_Approach_TempGSC_o',
                                                            'Extraction_steam_flowHPH8', 'Extraction_steam_flowHPH7', 'Extraction_steam_flowHPH6', 'Extraction_steam_flowHPH5',
                                                            'Extraction_steam_flowHPH8_o', 'Extraction_steam_flowHPH7_o', 'Extraction_steam_flowHPH6_o', 'Extraction_steam_flowHPH5_o','Drain_Cooler_Approach_TempHPH5','Drain_Cooler_Approach_TempHPH5_o'])
# Main calculation function
def calculate_thermal_performance(df):

    # Extract values from dataframe, handle missing gracefully
    Mw = float(df.loc["LOAD"]["Values (D)"])
    Mw_o = float(df.loc["LOAD"]["OPERATING"])
    # print(f"Load MW (Design): {load_mw_d}")
    # print(f"Load MW (Operating): {load_mw_0}")
    
    # Main steam
    ms_pressure_turbine_MPa = float(df.loc["MS PRESSURE AT TURBINE I/L"]["Values (D)"])
    ms_pressure_turbine_MPa_o = float(df.loc["MS PRESSURE AT TURBINE I/L"]["VALUES (O)"])
    
   
    ms_temp_tv1 = float(df.loc["MS TEMP AT TV1"]["Values (D)"])
    ms_temp_tv1_o = float(df.loc["MS TEMP AT TV1"]["VALUES (O)"])
    
    ms_temp_tv2 = float(df.loc["MS TEMP AT TV2"]["Values (D)"])
    ms_temp_tv2_o = float(df.loc["MS TEMP AT TV2"]["VALUES (O)"])
   
    ms_temp_avg = avg_temp(ms_temp_tv1, ms_temp_tv2)
    ms_temp_avg_o = avg_temp(ms_temp_tv1_o, ms_temp_tv2_o)
    print(f"Main Steam Average Temperature (C) (Operating): {ms_temp_avg_o}")
    print(f"Main Steam Average Temperature (C): {ms_temp_avg}")
    # ms_pressure_bar = mpato_bar(ms_pressure_turbine_MPa)
    # ms_pressure_bar_o = mpato_bar(ms_pressure_turbine_MPa_o)
    print(f"Main Steam Pressure (MPa): {ms_pressure_turbine_MPa_o}")
    print(f"Main Steam Pressure (bar): { ms_pressure_turbine_MPa}")
   
    Hms = get_enthalpy(ms_pressure_turbine_MPa, ms_temp_avg)
    Hms_o = get_enthalpy(ms_pressure_turbine_MPa_o, ms_temp_avg_o)
    print(f"Main Steam Enthalpy Hms_o (kJ/kg): {Hms_o}")
    print(f"Main Steam Enthalpy Hms (kJ/kg)Hmss: {Hms}")
    

    # HRH Enthalpy
    hrh_pressure_MPa = float(df.loc["HRH PRESSURE"]["Values (D)"])
    hrh_pressure_bar_o = float(df.loc["HRH PRESSURE"]["VALUES (O)"])
   
    hrh_temp1 = float(df.loc["IP I/L LH TEMP"]["Values (D)"])
    hrh_temp1_o = float(df.loc["IP I/L LH TEMP"]["VALUES (O)"])
    hrh_temp2 = float(df.loc["IP I/L RH TEMP"]["Values (D)"])
    hrh_temp2_o = float(df.loc["IP I/L RH TEMP"]["VALUES (O)"])
    hrh_temp_avg = avg_temp(hrh_temp1, hrh_temp2)
    hrh_temp_avg_o = avg_temp(hrh_temp1_o, hrh_temp2_o)
   
    # hrh_pressure_bar = mpato_bar(hrh_pressure_MPa)
    # hrh_pressure_bar_o = mpato_bar(hrh_pressure_bar_o)
   
    Hrh = round(get_enthalpy(hrh_pressure_MPa, hrh_temp_avg),2)
    Hrh_o = round(get_enthalpy(hrh_pressure_bar_o, hrh_temp_avg_o),2)
    print(f"Hot Reheat Enthalpy Hrh_o (kJ/kg): {Hrh_o}")
    print(f" Hot Reheat Enthalpy Hrh (kJ/kg): {Hrh}")
   

    # CRH Enthalpy
    crh_pressure_MPa = float(df.loc["CRH PRESSURE"]["Values (D)"])
    crh_pressure_MPa_o = float(df.loc["CRH PRESSURE"]["VALUES (O)"])
    crh_temp = float(df.loc["CRH TEMP"]["Values (D)"])
    crh_temp_o = float(df.loc["CRH TEMP"]["VALUES (O)"])
    crh_pressure_bar = (crh_pressure_MPa)
    crh_pressure_bar_o = (crh_pressure_MPa_o)
    Hcrh = round(get_enthalpy(crh_pressure_bar, crh_temp),2)
    Hcrh_o = round(get_enthalpy(crh_pressure_bar_o, crh_temp_o),2)
    print(f"Cold Reheat Enthalpy Hcrh_o (kJ/kg): {Hcrh_o}")
    print(f"Cold Reheat Enthalpy Hcrh (kJ/kg): {Hcrh}")
   
    # Reheater Spray Enthalpy
    rh_spray_pressure_MPa = float(df.loc["RH SPRAY WATER PRESSURE"]["Values (D)"])
    rh_spray_pressure_MPa_o = float(df.loc["RH SPRAY WATER PRESSURE"]["VALUES (O)"])
    rh_spray_temp = float(df.loc["RH SPRAY WATER TEMP"]["Values (D)"])
    rh_spray_temp_o = float(df.loc["RH SPRAY WATER TEMP"]["VALUES (O)"])
    # rh_spray_pressure_bar = mpato_bar(rh_spray_pressure_MPa)
    Hrhspray = round( get_enthalpy(rh_spray_pressure_MPa, rh_spray_temp),2)
    Hrhspray_o = round( get_enthalpy(rh_spray_pressure_MPa_o, rh_spray_temp_o),2)
    print(f"Reheater Spray Enthalpy Hrhspray_o (kJ/kg): {Hrhspray_o}")
    print(f"Reheater Spray Enthalpy Hrhspray (kJ/kg): {Hrhspray}")
   
    # Condensate flow at deaerator inlet
    condensate_flow_TPH = float(df.loc["CONDENSATE FLOW "]["Values (D)"])
    condensate_flow_TPH_o = float(df.loc["CONDENSATE FLOW "]["VALUES (O)"])
    print(f"Condensate Flow (TPH): {condensate_flow_TPH}")
    print(f"Condensate Flow (TPH) Operating: {condensate_flow_TPH_o}")

    # MCDSTDi = tph_to_kgph(condensate_flow_TPH)
    MCDSTDi = (condensate_flow_TPH)  # kg/hr
    MCDSTDi_o = condensate_flow_TPH_o
    print(f"Condensate Flow MCDSTDi (kg/hr): {MCDSTDi_o}")
    print   (f" MCDSTDi(kg/hr): {MCDSTDi}")

    # Feedwater flow initial iteration
    feedwater_flow_TPH = (float(df.loc["FEED WATER FLOW"]["Values (D)"]))* 1000  # Convert TPH to kg/hr
    feedwater_flow_TPH_o = tph_to_kgph( float(df.loc["FEED WATER FLOW"]["VALUES (O)"]))
    
    # MFWii = tph_to_kgph(feedwater_flow_TPH)
    MFWii = (feedwater_flow_TPH)
    MFWii_o = feedwater_flow_TPH_o
    #MFWii = 949192.93
    print(f"Feedwater Flow  MFWii (kg/hr): {MFWii}")
    print(f"Feedwater Flow  MFWii (kg/hr) Operating: {MFWii_o}")

    # HPH #8 Enthalpies
    # HPH8_EXT_pressure_bar = mpato_bar(float(df.loc["HPH-8 EXT PRESSURE"]["DESIGN"]))
    HPH8_EXT_pressure_bar = (float(df.loc["HPH-8 EXT PRESSURE"]["Values (D)"]))
    HPH8_EXT_pressure_bar_o = (float(df.loc["HPH-8 EXT PRESSURE"]["VALUES (O)"]))
   
    HPH8_EXT_temp = float(df.loc["HPH-8 EXT TEMP"]["Values (D)"])
    HPH8_EXT_temp_o = float(df.loc["HPH-8 EXT TEMP"]["VALUES (O)"])
    HHPH8EXT = round(get_enthalpy(HPH8_EXT_pressure_bar, HPH8_EXT_temp),2)
    HHPH8EXT_o = round(get_enthalpy(HPH8_EXT_pressure_bar_o, HPH8_EXT_temp_o),2)
    print(f"HPH8_EXT_pressure_bar : {HPH8_EXT_pressure_bar}, HPH8_EXT_temp :{HPH8_EXT_temp}")
    print(f"HPH-8 EXT Enthalpy HHPH8EXT (kJ/kg): {HHPH8EXT}")
    print(f"HPH8_EXT_pressure_bar_o : {HPH8_EXT_pressure_bar_o}, HPH8_EXT_temp_o :{HPH8_EXT_temp_o}")
    print(f"HPH-8 EXT Enthalpy HHPH8EXT_o (kJ/kg): {HHPH8EXT_o}")

    # HPH8_FW_out_pressure_bar = mpato_bar(float(df.loc["HPH-8 FW O/L PRESSURE"]["DESIGN"]))
    HPH8_FW_out_pressure_bar = (float(df.loc["HPH-8 FW O/L PRESSURE"]["Values (D)"]))
    HPH8_FW_out_pressure_bar_o = (float(df.loc["HPH-8 FW O/L PRESSURE"]["VALUES (O)"]))
    HPH8_FW_out_temp = float(df.loc["HPH-8 FW O/L TEMP"]["Values (D)"])
    HPH8_FW_out_temp_o = float(df.loc["HPH-8 FW O/L TEMP"]["VALUES (O)"])
    HHPH8o = round(get_enthalpy(HPH8_FW_out_pressure_bar, HPH8_FW_out_temp),2)
    HHPH8o_o = round(get_enthalpy(HPH8_FW_out_pressure_bar_o, HPH8_FW_out_temp_o),2)
    print(f"HPH-8 FW O/L Enthalpy HHPH8o (kJ/kg): {HHPH8o}")
    print(f"HPH-8 FW O/L Enthalpy HHPH8o_o (kJ/kg): {HHPH8o_o}")

    # HPH7_FW_out_pressure_bar = mpato_bar(float(df.loc["HPH-7 FW O/L PRESSURE"]["DESIGN"]))
    HPH7_FW_out_pressure_bar = (float(df.loc["HPH-7 FW O/L PRESSURE"]["Values (D)"]))
    HPH7_FW_out_pressure_bar_o = (float(df.loc["HPH-7 FW O/L PRESSURE"]["VALUES (O)"]))
    HPH7_FW_out_temp = float(df.loc["HPH-7 FW O/L TEMP"]["Values (D)"])
    HPH7_FW_out_temp_o = float(df.loc["HPH-7 FW O/L TEMP"]["VALUES (O)"])
   
    HHPH8i = round( get_enthalpy(HPH7_FW_out_pressure_bar, HPH7_FW_out_temp),2)  # feedwater inlet for HPH8
    HHPH8i_o = round( get_enthalpy(HPH7_FW_out_pressure_bar_o, HPH7_FW_out_temp_o),2)  # feedwater inlet for HPH8 operating
    print(f"HPH-8 FW I/L Enthalpy HHPH8i (kJ/kg):HHPH8i {HHPH8i}")
    print(f"HPH-8 FW I/L Enthalpy HHPH8i_o (kJ/kg): {HHPH8i_o}")
   
    # For HPH8 Drip temperature, assume enthalpy of saturated liquid at that temp
    HPH8_drip_temp = float(df.loc["HPH-8 DRIP TEMP"]["Values (D)"])
    HPH8_drip_temp_o = float(df.loc["HPH-8 DRIP TEMP"]["VALUES (O)"])
    HHPH8D = round(get_enthalpy_saturated_liquid_temp(HPH8_drip_temp),2)  
    HHPH8D_o = round(get_enthalpy_saturated_liquid_temp(HPH8_drip_temp_o),2) 
    print(f"HPH-8 Drip Enthalpy HHPH8D (kJ/kg)HHPH8D: {HHPH8D}")
    print(f"HPH-8 Drip Enthalpy HHPH8D_o (kJ/kg): {HHPH8D_o}")
   

    
    # numerator = (HHPH8o - HHPH8i)               # this should be around 177.34
    # denominator = (HHPH8EXT - HHPH8D)           # this should be around 2101.69
    # fraction = numerator / denominator           # about 0.08442
    # print(f"Numerator (kJ/kg): {numerator}")
    # print(f"Denominator (kJ/kg): {denominator}")
    # print(f"Fraction: {fraction}")
    # MHPH8EXT = MFWii * fraction
    MHPH8EXT = MFWii * (HHPH8o - HHPH8i) / (HHPH8EXT - HHPH8D)
    print(f" MHPH8EXT  (kJ/kg): {MHPH8EXT}")
    numerator_o = (HHPH8o_o - HHPH8i_o)  
    denominator_o = (HHPH8EXT_o - HHPH8D_o)
    fraction_o = numerator_o / denominator_o
    #MHPH8EXT_o = MFWii_o * fraction_o
    MHPH8EXT_o = MFWii_o * (HHPH8o_o - HHPH8i_o) / (HHPH8EXT_o - HHPH8D_o)
    print(f" MHPH8EXT_o  (kJ/kg): {MHPH8EXT_o}")           
    # Repeat similar for HPH7 and HPH6:
    # HPH7
    # HPH7_EXT_pressure_bar = mpato_bar(float(df.loc["HPH-7 EXT PRESSURE"]["DESIGN"]))
    HPH7_EXT_pressure_bar = (float(df.loc["HPH-7 EXT PRESSURE"]["Values (D)"]))
    HPH7_EXT_pressure_bar_o = (float(df.loc["HPH-7 EXT PRESSURE"]["VALUES (O)"]))
    HPH7_EXT_temp = float(df.loc["HPH-7 EXT TEMP"]["Values (D)"])
    HPH7_EXT_temp_o = float(df.loc["HPH-7 EXT TEMP"]["VALUES (O)"])
    HHPH7EXT = round(get_enthalpy(HPH7_EXT_pressure_bar, HPH7_EXT_temp),2)
    HHPH7EXT_o = round(get_enthalpy(HPH7_EXT_pressure_bar_o, HPH7_EXT_temp_o),2)
    print(f"HPH-7 EXT Enthalpy HHPH7EXT (kJ/kg): {HHPH7EXT}")
    print(f"HPH-7 EXT Enthalpy HHPH7EXT_o (kJ/kg): {HHPH7EXT_o}")

    # HPH7_FW_out_pressure_bar = mpato_bar(float(df.loc["HPH-7 FW O/L PRESSURE"]["DESIGN"]))
    HPH7_FW_out_pressure_bar = (float(df.loc["HPH-7 FW O/L PRESSURE"]["Values (D)"]))
    HPH7_FW_out_pressure_bar_o = (float(df.loc["HPH-7 FW O/L PRESSURE"]["VALUES (O)"]))
    HPH7_FW_out_temp = float(df.loc["HPH-7 FW O/L TEMP"]["Values (D)"])
    HPH7_FW_out_temp_o = float(df.loc["HPH-7 FW O/L TEMP"]["VALUES (O)"])
    
    HHPH7o = round(get_enthalpy(HPH7_FW_out_pressure_bar, HPH7_FW_out_temp),2)
    HHPH7o_o = round(get_enthalpy(HPH7_FW_out_pressure_bar_o, HPH7_FW_out_temp_o),2)
    print(f"HPH-7 FW O/L Enthalpy HHPH7o (kJ/kg): {HHPH7o}")
    print(f"HPH-7 FW O/L Enthalpy HHPH7o_o (kJ/kg): {HHPH7o_o}")
    

    # HPH6_FW_out_pressure_bar = mpato_bar(float(df.loc["HPH-6 FW O/L PRESSURE"]["DESIGN"]))
    HPH6_FW_out_pressure_bar = (float(df.loc["HPH-6 FW O/L PRESSURE"]["Values (D)"]))
    HPH6_FW_out_pressure_bar_o = (float(df.loc["HPH-6 FW O/L PRESSURE"]["VALUES (O)"]))
    HPH6_FW_out_temp = float(df.loc["HPH-6 FW O/L TEMP"]["Values (D)"])
    HPH6_FW_out_temp_o = float(df.loc["HPH-6 FW O/L TEMP"]["VALUES (O)"])
    HHPH7i = round(get_enthalpy(HPH6_FW_out_pressure_bar, HPH6_FW_out_temp),2)  # inlet for HPH7
    HHPH7i_o = round(get_enthalpy(HPH6_FW_out_pressure_bar_o, HPH6_FW_out_temp_o),2)  # inlet for HPH7 operating
    print(f"HPH-7 FW I/L Enthalpy HHPH7i (kJ/kg): {HHPH7i}")
    print(f"HPH-7 FW I/L Enthalpy HHPH7i_o (kJ/kg): {HHPH7i_o}")
   

    HPH7_drip_temp = float(df.loc["HPH-7 DRIP TEMP"]["Values (D)"])
    HPH7_drip_temp_o = float(df.loc["HPH-7 DRIP TEMP"]["VALUES (O)"])
    HHPH7D = round(get_enthalpy_saturated_liquid_temp(HPH7_drip_temp),2)  # approx
    HHPH7D_o = round(get_enthalpy_saturated_liquid_temp(HPH7_drip_temp_o),2)  # approx operating
    print(f"HPH-7 Drip Enthalpy HHPH7D (kJ/kg): {HHPH7D}")
    print(f"HPH-7 Drip Enthalpy HHPH7D_o (kJ/kg): {HHPH7D_o}")
    
   
    MHPH7EXT = (
    (MFWii * (HHPH7o - HHPH7i)) - 
    (MHPH8EXT * (HHPH8D - HHPH7D))
) / (HHPH7EXT - HHPH7D)

    print(f"HPH-7 MHPH7EXT (kJ/kg): {MHPH7EXT}")
    N = (MFWii_o * (HHPH7o_o - HHPH7i_o)) - (MHPH8EXT_o * (HHPH8D_o - HHPH7D_o))
    D = (HHPH7EXT_o - HHPH7D_o)
    MHPH7EXT_o = N / D
    
    # MHPH7EXT_o = (MFWii_o * (HHPH7o_o - HHPH7i_o)) - (MHPH8EXT_o * (HHPH8D_o - HHPH7D_o)) / (HHPH7EXT_o - HHPH7D_o)
    print(f"HPH-7 MHPH7EXT_o (kJ/kg): {MHPH7EXT_o}")

  
    HPH6_EXT_pressure_bar = (float(df.loc["HPH-6 EXT PRESSURE"]["Values (D)"]))
    HPH6_EXT_pressure_bar_o = (float(df.loc["HPH-6 EXT PRESSURE"]["VALUES (O)"]))
    HPH6_EXT_temp = float(df.loc["HPH-6 EXT TEMP"]["Values (D)"])
    HPH6_EXT_temp_o = float(df.loc["HPH-6 EXT TEMP"]["VALUES (O)"])
    HHPH6EXT = round(get_enthalpy(HPH6_EXT_pressure_bar, HPH6_EXT_temp),2)
    HHPH6EXT_o = round( get_enthalpy(HPH6_EXT_pressure_bar_o, HPH6_EXT_temp_o),2)
    print(f"HPH-6 EXT Enthalpy HHPH6EXT (kJ/kg): {HHPH6EXT}")
    print(f"HPH-6 EXT Enthalpy HHPH6EXT_o (kJ/kg): {HHPH6EXT_o}")
   

    # HPH6_FW_out_pressure_bar = mpato_bar(float(df.loc["HPH-6 FW O/L PRESSURE"]["DESIGN"]))
    HPH6_FW_out_pressure_bar = (float(df.loc["HPH-6 FW O/L PRESSURE"]["Values (D)"]))
    HPH6_FW_out_pressure_bar_o = (float(df.loc["HPH-6 FW O/L PRESSURE"]["VALUES (O)"]))
    HPH6_FW_out_temp = float(df.loc["HPH-6 FW O/L TEMP"]["Values (D)"])
    HPH6_FW_out_temp_o = float(df.loc["HPH-6 FW O/L TEMP"]["VALUES (O)"])
    HHPH6o = round(get_enthalpy(HPH6_FW_out_pressure_bar, HPH6_FW_out_temp),2)
    HHPH6o_o = round(get_enthalpy(HPH6_FW_out_pressure_bar_o, HPH6_FW_out_temp_o),2)
    print(f"HPH-6 FW O/L Enthalpy HHPH6o (kJ/kg): {HHPH6o}")
    print(f"HPH-6 FW O/L Enthalpy HHPH6o_o (kJ/kg): {HHPH6o_o}")
   

    # HPH6_FW_in_pressure_bar = mpato_bar(float(df.loc["HPH-6 FW I/L PRESSURE"]["DESIGN"]))
    HPH6_FW_in_pressure_bar = float(df.loc["HPH-6 FW I/L PRESSURE"]["Values (D)"])
    HPH6_FW_in_pressure_bar_o = float(df.loc["HPH-6 FW I/L PRESSURE"]["VALUES (O)"])
    HPH6_FW_in_temp = float(df.loc["HPH-6 FW I/L TEMP"]["Values (D)"])
    HPH6_FW_in_temp_o = float(df.loc["HPH-6 FW I/L TEMP"]["VALUES (O)"])
    HHPH6i = round(get_enthalpy(HPH6_FW_in_pressure_bar, HPH6_FW_in_temp),2)
    HHPH6i_o = round(get_enthalpy(HPH6_FW_in_pressure_bar_o, HPH6_FW_in_temp_o),2)
    print(f"HPH-6 FW I/L Enthalpy HHPH6i (kJ/kg): {HHPH6i}")
    print(f"HPH-6 FW I/L Enthalpy HHPH6i_o (kJ/kg): {HHPH6i_o}")
   

    HPH6_drip_temp = float(df.loc["HPH-6 DRIP TEMP"]["Values (D)"])
    HPH6_drip_temp_o = float(df.loc["HPH-6 DRIP TEMP"]["VALUES (O)"])
    HHPH6D = round(get_enthalpy_saturated_liquid_temp(HPH6_drip_temp),2)
    HHPH6D_o = round( get_enthalpy_saturated_liquid_temp(HPH6_drip_temp_o),2)
    print(f"HPH-6 Drip Enthalpy HHPH6D (kJ/kg): {HHPH6D}")
    print(f"HPH-6 Drip Enthalpy HHPH6D_o (kJ/kg): {HHPH6D_o}")
    
    

    # Calculate MHPH6EXT
    # MHPH6EXT = (MFWii * (HHPH6o - HHPH6i) - MHPH7EXT * (HHPH7D - HHPH7D) - MHPH8EXT * (HHPH8D - HHPH8D)) / (HHPH6EXT - HHPH6D)
    numerator = MFWii * (HHPH6o - HHPH6i) - (MHPH8EXT + MHPH7EXT) * (HHPH7D - HHPH6D)
    denominator = HHPH6EXT - HHPH6D
    MHPH6EXT = numerator / denominator
    print(f"HPH-6  MHPH6EXT (kJ/kg): {MHPH6EXT}")
    
    numerator_o = MFWii_o * (HHPH6o_o - HHPH6i_o) - (MHPH8EXT_o + MHPH7EXT_o) * (HHPH7D_o - HHPH6D_o)
    denominator_o = HHPH6EXT_o - HHPH6D_o
    MHPH6EXT_o = numerator_o / denominator_o
    print(f"HPH-6  MHPH6EXT_o (kJ/kg): {MHPH6EXT_o}")

    # Calculate Spray Water for Reheater (MSFLOW - FeedWaterFlow)
    ms_flow_tph = float(df.loc["MS FLOW"]["DESIGN"])
    ms_flow_kgph = tph_to_kgph(ms_flow_tph)
    
    MSspray = ms_flow_kgph - MFWii
   
        # Deaerator #5 Feedwater Inlet Enthalpy (HDEAi)
    # dea_i_pressure_bar = mpato_bar(float(df.loc["DEA I/L COND PRESSURE"]["DESIGN"]))
    dea_ext_pressure_bar = (float(df.loc["DEA EXT STEAM PRESSURE"]["Values (D)"]))
    dea_ext_pressure_bar_o = (float(df.loc["DEA EXT STEAM PRESSURE"]["VALUES (O)"]))
    dea_ext_temp = float(df.loc["DEA EXT STEAM TEMP"]["Values (D)"])
    dea_ext_temp_o = float(df.loc["DEA EXT STEAM TEMP"]["VALUES (O)"])
    HDEAEXT = round(get_enthalpy(dea_ext_pressure_bar, dea_ext_temp),2)
    HDEAEXT_o = round(get_enthalpy(dea_ext_pressure_bar_o, dea_ext_temp_o),2)
    print(f"Deaerator Extraction Steam Enthalpy HDEAEXT_o (kJ/kg): {HDEAEXT_o}")
    print(f"Deaerator Extraction Steam Enthalpy HDEAEXT (kJ/kg): {HDEAEXT}")
    print(f"dea_ext_pressure_bar {dea_ext_pressure_bar} dea_ext_temp {dea_ext_temp}")

    # Deaerator #5 Feedwater Outlet Enthalpy (HDEAo)
    dea_o_temp = float(df.loc["BFP I/L FW TEMP"]["Values (D)"])  # This is HDEAo temp
    dea_o_temp_o = float(df.loc["BFP I/L FW TEMP"]["VALUES (O)"])  # This is HDEAo temp operating
    #dea_o_pressure_bar = dea_i_pressure_bar  # assume same pressure
    HDEAo = round(get_enthalpy_saturated_liquid_temp( dea_o_temp),2)
    HDEAo_o = round( get_enthalpy_saturated_liquid_temp(dea_o_temp_o),2)
    print(f"Deaerator Outlet Enthalpy HDEAo_o (kJ/kg): {HDEAo_o}")
    print(f"Deaerator Outlet Enthalpy HDEAo (kJ/kg): {HDEAo}")
   

    # Deaerator #5 Extraction Steam Enthalpy (HDEAEXT)
    # dea_ext_pressure_bar = mpato_bar(float(df.loc["DEA EXT STEAM PRESSURE"]["DESIGN"]))
    

    dea_i_pressure_bar = (float(df.loc["DEA EXT STEAM PRESSURE"]["Values (D)"]))
    dea_i_pressure_bar_o = (float(df.loc["DEA EXT STEAM PRESSURE"]["VALUES (O)"]))
    dea_i_temp = float(df.loc["DEA I/L COND TEMP"]["Values (D)"])
    dea_i_temp_o = float(df.loc["DEA I/L COND TEMP"]["VALUES (O)"])
    HDEAi = round( get_enthalpy(dea_i_pressure_bar, dea_i_temp) ,2)
    HDEAi_o = round( get_enthalpy(dea_i_pressure_bar_o, dea_i_temp_o) ,2)
    print(f"Deaerator Inlet Enthalpy HDEAi_o (kJ/kg): {HDEAi_o}")
    print(f"Deaerator Inlet Enthalpy HDEAi (kJ/kg): {HDEAi}")
  
    # Step-by-step correct implementation
    Hdiff = HDEAo - HDEAi  # 752.1262583187043 - 587.624977462506
    print(f"Hdiff{Hdiff}")
    delta = HHPH6D - HDEAo  # 773.3580326890391 - 752.1262583187043
    print(f"delta : {delta}")
    denominator = HDEAEXT - HDEAo  # 3175.430537744348 - 752.1262583187043


    # Compute numerator
    term1 = MCDSTDi * Hdiff
    print(f"term1{term1}")
    term2 = (MHPH8EXT + MHPH7EXT + MHPH6EXT) * delta
    print(f"MHPH8EXT + MHPH7EXT + MHPH6EXT: {MHPH8EXT + MHPH7EXT + MHPH6EXT}")
    print(f"term2 {term2}")
    numerator1 = term1 - term2
    sum2 =  (MHPH8EXT + MHPH7EXT + MHPH6EXT) 
    print(f"sum2{sum2}")

    # Final MDEA_EXT
    MDEA_EXT = numerator1 / denominator
    print(f"denominator (kJ/kg): {denominator}")
    print(f"numerator (kJ/kg): {numerator1}")
    print(f"MDEA_EXT (kJ/kg): {MDEA_EXT}")

    Hdiff_o = HDEAo_o - HDEAi_o  # 752.1262583187043 - 587.624977462506
    delta_o = HHPH6D_o - HDEAo_o  # 773.3580326890391 - 752.1262583187043
    denominator_o = HDEAEXT_o - HDEAo_o  # 3175.430537744348 - 752.1262583187043
    term1_o = MCDSTDi_o * Hdiff_o
    term2_o = (MHPH8EXT_o + MHPH7EXT_o + MHPH6EXT_o) * delta_o
    numerator1_o = term1_o - term2_o
    MDEA_EXT_o = numerator1_o / denominator_o
    print(f"denominator_o (kJ/kg): {denominator_o}")
    print(f"numerator_o (kJ/kg): {numerator1_o}")
    print(f"MDEA_EXT_o (kJ/kg): {MDEA_EXT_o}")


    

    MS1= float(df.loc["1ST STAGE SHS DESUP FLOW"]["Values (D)"])
    MS1_o= float(df.loc["1ST STAGE SHS DESUP FLOW"]["VALUES (O)"])
    MS2= float(df.loc["2ND STAGE SHS DESUP FLOW"]["Values (D)"])
    MS2_o= float(df.loc["2ND STAGE SHS DESUP FLOW"]["VALUES (O)"])
    MSHspray = (MS1 + MS2)  # kg/hr
    MSHspray_o = (MS1_o + MS2_o)  # kg/hr operating
    print(f" (MSHspray)_o [kg/hr]: {MSHspray_o}")
    print(f" (MsHspray) [kg/hr]: {MSHspray}")

    R1= float(df.loc["RH LHS DESUP FLOW"]["Values (D)"])
    R1_o= float(df.loc["RH LHS DESUP FLOW"]["VALUES (O)"])
    R2= float(df.loc["RH RHS DESUP FLOW"]["Values (D)"])
    R2_o= float(df.loc["RH RHS DESUP FLOW"]["VALUES (O)"])
    MRHspray = (R1 + R2)  # kg/hr
    MRHspray_o = (R1_o + R2_o)  # kg/hr operating
    print(f" (MRHspray) [kg/hr] Operating: {MRHspray_o}")
    print(f" (MRHspray) [kg/hr]: {MRHspray}")
    MFWfi = MCDSTDi + MHPH8EXT + MHPH7EXT + MHPH6EXT + MDEA_EXT - (MSHspray + MRHspray)
    diff = MFWfi - MFWii
    # tolerance = 0.00000009
    # max_iter = 100
    # iteration = 0
    # step_size = 0.5

    # while iteration < max_iter:
    #     # Recalculate dependent variables that depend on MDEA_EXT
    #     # For example:
    #     MFWfi = MCDSTDi + MHPH8EXT + MHPH7EXT + MHPH6EXT + MDEA_EXT - (MSHspray + MRHspray)
    #     MFWfi_o = MCDSTDi_o + MHPH8EXT_o + MHPH7EXT_o + MHPH6EXT_o + MDEA_EXT_o - (MSHspray_o + MRHspray_o)
    #     diff = MFWfi - MFWii
    #     diff_o = MFWfi_o - MFWii_o
        
    #     print(f"Iter {iteration}: diff={diff:.8f}, MDEA_EXT={MDEA_EXT:.8f}")

    #     if abs(diff) < tolerance:
    #         print("Converged to zero difference.")
    #         break

    #     # Update MDEA_EXT
    #     #MDEA_EXT -= step_size * diff  # move opposite direction of diff
    #     MFWii += step_size * diff

    #     # Optionally reduce step_size if oscillation detected

    #     iteration += 1

    # if iteration == max_iter:
    #     print("Did not converge.")
    tolerance = 1e-4
    max_iter = 100
    iteration = 0
    step_size = 0.5
    MFWfi = MCDSTDi + MHPH8EXT + MHPH7EXT + MHPH6EXT + MDEA_EXT - (MSHspray + MRHspray)
    print(f"Initial MFWfi: {MFWfi:.8f}")
    diff = MFWfi - MFWii
    print(f"Initial diff: {diff:.8f}, MFWii={MFWii:.8f}")



    # while iteration < max_iter:
    #     diff = MFWfi - MFWii
    #     # print(f"Iter {iteration}: diff={diff:.8f}, MFWii={MFWii:.8f}")
    #     print(f"Iter {iteration}: MWFii={MFWii:.6f}, MFWfi={MFWfi:.6f}, diff={diff:.6f}")

    #     if abs(diff) < tolerance:
    #         print("✅ Converged: MFWii matches MFWfi within tolerance.")
    #         break

    #     # Adjust MFWii to approach MFWfi
    #     MFWii += step_size * diff
       

    #     iteration += 1
    #     df.loc["FEED WATER FLOW"] ["Values (D)"] = MFWii
       
    # print(f"Final MFWii: {MFWii:.8f}, MFWfi: {MFWfi:.8f}, after {iteration} iterations")
    # print(f"MDEA_EXT (kJ/kg)Updated: {MDEA_EXT}")
    

    # if iteration == max_iter:
    #     print("❌ Did not converge within max iterations.")


    
    # Calculated Feedwater flow (MFWfi)
    #MFWfi = (MCDSTDi + MHPH8EXT + MHPH7EXT + MHPH6EXT) - (MSHspray + MRHspray)  # Replace 0s with MSHspray, MRHspray if available
    #MFWfi = MCDSTDi + MHPH8EXT + MHPH7EXT + MHPH6EXT + MDEA_EXT - (MSHspray + MRHspray)
    MFWfi_o = MCDSTDi_o + MHPH8EXT_o + MHPH7EXT_o + MHPH6EXT_o + MDEA_EXT_o - (MSHspray_o + MRHspray_o)
    print(f" (MFWfi_o) [kg/hr] Operating: {MFWfi_o}")
    print(f" (MFWii_o) [kg/hr]: {MFWii_o}")
    print(f"MCDTSDi_o {MCDSTDi_o} MHPH8EXT_o {MHPH8EXT_o} MHPH7EXT_o {MHPH7EXT_o} MHPH6EXT_o {MHPH6EXT_o} MDEA_EXT_o {MDEA_EXT_o} MSHspray_o {MSHspray_o} MRHspray_o {MRHspray_o}")
#     print(f"Calculated Feedwater Flow (MFWfi) [kg/hr] Operating: {MFWfi_o}")
#     print(f"Calculated Feedwater Flow (MFWfi) [kg/hr]: {MFWfi}")
#     print(f"feedflow {MFWii} {MFWfi}")

#     Unaccounted_for_change_in_storage = float(df.loc["Hotwell storage change"]["Values (D)"])
#     Unaccounted_for_change_in_storage_o = float(df.loc["Hotwell storage change"]["VALUES (O)"])
#     MUA = tph_to_kgph(Unaccounted_for_change_in_storage)  # kg/hr
#     MUA_o = tph_to_kgph(Unaccounted_for_change_in_storage_o)  # kg/hr operating
#     print(f"Unaccounted for change in storage (MUA) [kg/hr] Operating: {MUA_o}")
#     print(f"Unaccounted for change in storage (MUA) [kg/hr]: {MUA}")

#     Ms = ( MFWfi + MSHspray + MUA )
#     Ms_o = ( MFWfi_o + MSHspray_o + MUA_o )
#     print(f"Total Mass Flow (Ms) [kg/hr] Operating: {Ms_o}")
    
#     print(f"Total Mass Flow (Ms) [kg/hr]: {Ms}")
#     #Auxiliary steam
#     Maux = 0
#     Maux_o = 0
#     #Cold reheat steam flow (Mcrh )
#     Mcrh = ( Ms - MHPH8EXT - MHPH7EXT - Maux)
#     Mcrh_o = ( Ms_o - MHPH8EXT_o - MHPH7EXT_o - Maux_o)
#     print(f"Cold Reheat Steam Flow (Mcrh) [kg/hr] Operating: {Mcrh_o}")
#     print(f"Cold Reheat Steam Flow (Mcrh) [kg/hr]: {Mcrh}")
#     #Hot reheat steam flow ( MRH) 
#     MRH = ( Mcrh + MRHspray)
#     MRH_o = ( Mcrh_o + MRHspray_o)
#     print(f"Hot Reheat Steam Flow (MRH) [kg/hr]: {MRH}")
#     #Heat Rate
#     # Mw =299.95
#     HR = (
#     (Ms * Hms)
#     + (Mcrh * (Hrh - Hcrh))
#     + (MRHspray * (Hrh - Hrhspray))
#     - (MFWfi * HHPH8o)
#     - (MSHspray *  HHPH6i)
# ) / (Mw * 1000)
#     HR_o = (
#     (Ms_o * Hms_o)
#     + (Mcrh_o * (Hrh_o - Hcrh_o))
#     + (MRHspray_o * (Hrh_o - Hrhspray_o))
#     - (MFWfi_o * HHPH8o_o)
#     - (MSHspray_o *  HHPH6i_o)  
# ) / (Mw * 1000)
#     print(f"Heat Rate (HR) [kJ/kg] Operating: {HR_o}")
    
#     print(f"Heat Rate (HR) [kJ/kg]: {HR}")
#     print(f"Heat Rate (HR) [kJ/kWh]: {HR/4.184}")
#     print(f"Heat Rate (HR) [kcal/kg]: {HR_o/4.184}")
#     print(f"mfwii {MFWii} MFWfi {MFWfi}")
#     print(f"mfwii_o {MFWii_o} MFWfi_o {MFWfi_o}")
#     print(f"MDEA_EXT (kJ/kg): {MDEA_EXT}")



   

    return ThermalResults(
        Load_MW=Mw,
        Mw_o = Mw_o,
        Hms=Hms,
        Hms_o=Hms_o,
        Hrh=Hrh,
        Hrh_o=Hrh_o,
        Hcrh=Hcrh,
        Hcrh_o=Hcrh_o,
        Hrhspray=Hrhspray,
        Hrhspray_o=Hrhspray_o,
        MFWii=MFWii,
        MFWii_o=MFWii_o,
        MFWfi=MFWfi,
        MFWfi_o=MFWfi_o,
        MHPH8EXT = MHPH8EXT,
        MHPH8EXT_o = MHPH8EXT_o,
        MHPH7EXT=MHPH7EXT,
        MHPH7EXT_o=MHPH7EXT_o,
        MHPH6EXT=MHPH6EXT,
        MHPH6EXT_o=MHPH6EXT_o,
        MDAEXT=MDEA_EXT,
        MDAEXT_o=MDEA_EXT_o,
        MSspray=MSspray,
        HDEAo=HDEAo,
        HDEAo_o=HDEAo_o,
        HHPH8o = HHPH8o,
        HHPH8o_o = HHPH8o_o,
        HHPH6i=HHPH6i,
        HHPH6i_o=HHPH6i_o,
        MRHspray = MRHspray,
        MRHspray_o = MRHspray_o,
        MSHspray=MSHspray,
        MSHspray_o=MSHspray_o,
        MCDSTDi = MCDSTDi,
        MCDSTDi_o = MCDSTDi_o
        
    )

# def what_if_iteration(df, max_iter=15, tolerance=0.0005, step_size=1):
#     # Initial value in kg/hr
#     MFWii = float(df.loc["FEED WATER FLOW", "Values (D)"]) * 1000
#     print(f"Initial MFWii: {MFWii:.6f}")

#     for iteration in range(max_iter):
#         # Step 1: Update the DataFrame input
#         df.loc["FEED WATER FLOW", "Values (D)"] = MFWii / 1000
        
#         # Step 2: Run performance calculation
#         results = calculate_thermal_performance(df)
#         MFWfi = results.MFWfi
        

#         # Step 3: Check difference
#         diff = MFWfi - MFWii
#         print(f"Iter {iteration}: MFWii={MFWii:.6f}, MFWfi={MFWfi:.6f}, diff={diff:.6f}")
#         if abs(diff) < tolerance:
#             print(f"✅ Converged at iteration {iteration}")
#             Unaccounted_for_change_in_storage = float(df.loc["Hotwell storage change"]["Values (D)"])
           
#             MUA = (Unaccounted_for_change_in_storage)  # kg/hr
#              # kg/hr operating
           
#             print(f"Unaccounted for change in storage (MUA) [kg/hr]: {MUA}")
#             MSHspray=results.MSHspray
#             MHPH8EXT = results.MHPH8EXT
#             MHPH7EXT = results.MHPH7EXT
#             MHPH6EXT = results.MHPH6EXT
#             MRHspray = results.MRHspray
#             Hms = results.Hms
#             Hcrh = results.Hcrh
#             print(f"Hrch (kJ/kg): {results.Hcrh}")
#             Hrh = results.Hrh
#             print(f"Hcrh (kJ/kg): {Hrh}")
#             Hrhspray = results.Hrhspray
#             HHPH8o = results.HHPH8o
#             HHPH6i = results.HHPH6i
#             Mw = results.Load_MW

#             Ms = ( MFWfi + MSHspray + MUA )
#             print(f"Calculated Feedwater Flow (MFWfi) [kg/hr]: {MFWfi}")
#             print(f"MSHspray [kg/hr]: {MSHspray}")
#             #Ms_o = ( MFWfi_o + MSHspray_o + MUA_o )
#             # print(f"Total Mass Flow (Ms) [kg/hr] Operating: {Ms_o}")
            
#             print(f"Total Mass Flow (Ms) [kg/hr]: {Ms}")
#             #Auxiliary steam
#             Maux = 0
          
#             #Cold reheat steam flow (Mcrh )
#             Mcrh = ( Ms - MHPH8EXT - MHPH7EXT - Maux)
#             # Mcrh_o = ( Ms_o - MHPH8EXT_o - MHPH7EXT_o - Maux_o)
#             # print(f"Cold Reheat Steam Flow (Mcrh) [kg/hr] Operating: {Mcrh_o}")
#             print(f"Cold Reheat Steam Flow (Mcrh) [kg/hr]: {Mcrh}")
#             #Hot reheat steam flow ( MRH) 
#             MRH = ( Mcrh + MRHspray)
#             # MRH_o = ( Mcrh_o + MRHspray_o)
#             print(f"Hot Reheat Steam Flow (MRH) [kg/hr]: {MRH}")
#             #Heat Rate
#             # Mw =299.95
#             HR_1 = (
#             (Ms * Hms)
#             + (Mcrh * (Hrh - Hcrh))
#             + (MRHspray * (Hrh - Hrhspray))
#             - (MFWfi * HHPH8o)
#             - (MSHspray *  HHPH6i)
#         ) / (Mw * 1000)
#             HR = HR_1/ 4.184
#             print(f"Heat Rate (HR) [kJ/kg]: {HR}")
#             print(f"Heat Rate (HR) [kJ/kWh]: {HR/4.184}")

#             # return MFWii, MFWfi, iteration
#             return ThermalResults2 (MFWii=MFWii, MFWfi=MFWfi,max_iter= max_iter, MRH =  MRH,HR = HR , Ms = Ms ,Hms = Hms)

#         # Step 4: Update MFWii
#         MFWii += step_size * diff
        

#         # Step 5: Explicitly call thermal performance again immediately after update
#         df.loc["FEED WATER FLOW", "Values (D)"] = MFWii / 1000
#         calculate_thermal_performance(df)  # 👈 call immediately after update
   
#     print("❌ Did not converge")
#     print(f"Final MWFii: {MFWii:.6f}, MFWfi: {MFWfi:.6f}")
#     return MFWii ,MFWfi,max_iter,MRH
# def what_if_iteration(df, max_iter=15, tolerance=0.0005):
#     # Initial value in kg/hr
#     MFWii = float(df.loc["FEED WATER FLOW", "Values (D)"]) * 1000
#     print(f"Initial MFWii: {MFWii:.6f}")

#     for iteration in range(max_iter):
#         # Step 1: Update the DataFrame input (in t/hr)
#         df.loc["FEED WATER FLOW", "Values (D)"] = MFWii / 1000

#         # Step 2: Run performance calculation
#         results = calculate_thermal_performance(df)
#         MFWfi = results.MFWfi

#         # Step 3: Check deviation
#         diff = MFWfi - MFWii
#         print(f"Iter {iteration}: MFWii={MFWii:.6f}, MFWfi={MFWfi:.6f}, diff={diff:.6f}")

#         if abs(diff) < tolerance:
#             print(f"✅ Converged at iteration {iteration}")
#             Unaccounted_for_change_in_storage = float(df.loc["Hotwell storage change", "Values (D)"])
#             MUA = Unaccounted_for_change_in_storage

#             MSHspray = results.MSHspray
#             MHPH8EXT = results.MHPH8EXT
#             MHPH7EXT = results.MHPH7EXT
#             MHPH6EXT = results.MHPH6EXT
#             MRHspray = results.MRHspray
#             Hms = results.Hms
#             Hcrh = results.Hcrh
#             Hrh = results.Hrh
#             Hrhspray = results.Hrhspray
#             HHPH8o = results.HHPH8o
#             HHPH6i = results.HHPH6i
#             Mw = results.Load_MW

#             Ms = MFWfi + MSHspray + MUA
#             Maux = 0
#             Mcrh = Ms - MHPH8EXT - MHPH7EXT - Maux
#             MRH = Mcrh + MRHspray

#             HR1 = (
#                 (Ms * Hms)
#                 + (Mcrh * (Hrh - Hcrh))
#                 + (MRHspray * (Hrh - Hrhspray))
#                 - (MFWfi * HHPH8o)
#                 - (MSHspray * HHPH6i)
#             ) / (Mw * 1000)
#             HR = HR1 / 4.184  # Convert to kJ/kWh

#             print(f"Heat Rate (HR) [kJ/kg]: {HR}")
#             print(f"Heat Rate (HR) [kJ/kWh]: {HR1 / 4.184}")

#             # return ThermalResults2(MFWii=MFWii, MFWfi=MFWfi, max_iter=iteration+1, MRH=MRH)
#             return ThermalResults2 (MFWii=MFWii, MFWfi=MFWfi,max_iter= max_iter+1 , MRH =  MRH,HR = HR , Ms = Ms ,Hms = Hms)

#         # Step 4: Direct substitution for faster convergence
#         MFWii = MFWfi

#     print("❌ Did not converge")
#     print(f"Final MFWii: {MFWii:.6f}, MFWfi: {MFWfi:.6f}")
#     return MFWii, MFWfi, max_iter, MRH
def what_if_iteration(df, max_iter=15, tolerance=5e-4):
    MFWii = float(df.loc["FEED WATER FLOW", "Values (D)"]) * 1000  # Initial in kg/hr

    for _ in range(max_iter):
        df.loc["FEED WATER FLOW", "Values (D)"] = MFWii / 1000  # t/hr
        results = calculate_thermal_performance(df)
        MFWfi = results.MFWfi

        if abs(MFWfi - MFWii) < tolerance:
            MUA = float(df.loc["Hotwell storage change", "Values (D)"])
            Ms = MFWfi + results.MSHspray + MUA
            Mcrh = Ms - results.MHPH8EXT - results.MHPH7EXT
            MRH = Mcrh + results.MRHspray
            print(f"MRH: {MRH}")

            HR_kJ_kg = (
                (Ms * results.Hms)
                + (Mcrh * (results.Hrh - results.Hcrh))
                + (results.MRHspray * (results.Hrh - results.Hrhspray))
                - (MFWfi * results.HHPH8o)
                - (results.MSHspray * results.HHPH6i)
            ) / (results.Load_MW * 1000)

            HR = HR_kJ_kg / 4.184  # Convert to kJ/kWh
            print(f"Heat Rate (HR) [kJ/kg]: {HR}")

            return ThermalResults2(
                MFWii=MFWii,
                MFWfi=MFWfi,
                max_iter=_ + 1,
                MRH=MRH,
                HR=HR,
                Ms=Ms,
                Hms=results.Hms,
                MHPH6EXT = results.MHPH6EXT,
                MDAEXT = results.MDAEXT

            )

        MFWii = MFWfi  # Direct substitution for fast convergence
    print("❌ Did not converge")

    return MFWii, MFWfi, max_iter, results.MRHspray


    # return ThermalResults2 (MFWii=MFWii, MFWfi=MFWfi,max_iter= max_iter)
# def what_if_iteration_o(df, max_iter=25, tolerance=0.00000005, step_size=1):
#     # Initial value in kg/hr
   
#     MFWii_o = float(df.loc["FEED WATER FLOW", "Values (D)"]) * 1000
  
#     print(f"Initial MFWii_o: {MFWii_o:.6f}")

#     for iteration in range(max_iter):
#         # Step 1: Update the DataFrame input
       
#         df.loc["FEED WATER FLOW", "VALUES (O)"] = MFWii_o / 1000  # Assuming same value for operating condition

#         # Step 2: Run performance calculation
#         results = calculate_thermal_performance(df)
#         MFWfi_o = results.MFWfi_o  # Operating condition

#         # Step 3: Check difference
       
#         diff_o = MFWfi_o - MFWii_o
        
#         print(f"Iter {iteration}: MFWii_o={MFWii_o:.6f}, MFWfi_o={MFWfi_o:.6f}, diff_o={diff_o:.6f}")

#         if abs(diff_o) < tolerance:
#             print(f"✅ Converged at iteration {iteration}")
#         #     Unaccounted_for_change_in_storage = float(df.loc["Hotwell storage change"]["Values (D)"])
#             Unaccounted_for_change_in_storage_o = float(df.loc["Hotwell storage change"]["VALUES (O)"])
#         #     MUA = (Unaccounted_for_change_in_storage)  # kg/hr
#             MUA_o = (Unaccounted_for_change_in_storage_o)  # kg/hr operating
#             print(f"Unaccounted for change in storage (MUA) [kg/hr] Operating: {MUA_o}")
#         #     print(f"Unaccounted for change in storage (MUA) [kg/hr]: {MUA}")
#         #     MSHspray=results.MSHspray
#             MSHspray_o = results.MSHspray_o
#             MHPH8EXT_o = results.MHPH8EXT_o
#         #     MHPH8EXT = results.MHPH8EXT
#         #     MHPH7EXT = results.MHPH7EXT
#             MHPH7EXT_o = results.MHPH7EXT_o
#         #     MHPH6EXT = results.MHPH6EXT
#             MHPH6EXT_o = results.MHPH6EXT_o
#             MRHspray_o = results.MRHspray_o
#         #     MRHspray = results.MRHspray
#         #     Hms = results.Hms
#             Hms_o = results.Hms_o
#         #     Hcrh = results.Hcrh
#             Hcrh_o = results.Hcrh_o
#         #     print(f"Hrch (kJ/kg): {results.Hcrh}")
#         #     Hrh = results.Hrh
#             Hrh_o = results.Hrh_o
#         #     print(f"Hcrh (kJ/kg): {Hrh}")
#         #     Hrhspray = results.Hrhspray
#             Hrhspray_o = results.Hrhspray_o
#         #     HHPH8o = results.HHPH8o
#             HHPH8o_o = results.HHPH8o_o
#         #     HHPH6i = results.HHPH6i
#             HHPH6i_o = results.HHPH6i_o
#         #     Mw = results.Load_MW
#             Mw_o = results.Mw_o

#         #     Ms = ( MFWfi + MSHspray + MUA )
#         #     print(f"Calculated Feedwater Flow (MFWfi) [kg/hr]: {MFWfi}")
#         #     print(f"MSHspray [kg/hr]: {MSHspray}")
#             Ms_o = ( MFWfi_o + MSHspray_o + MUA_o )
#         #     # print(f"Total Mass Flow (Ms) [kg/hr] Operating: {Ms_o}")
            
#         #     print(f"Total Mass Flow (Ms) [kg/hr]: {Ms}")
#         #     #Auxiliary steam
#         #     Maux = 0
#             Maux_o = 0
#         #     #Cold reheat steam flow (Mcrh )
#         #     Mcrh = ( Ms - MHPH8EXT - MHPH7EXT - Maux)
#             Mcrh_o = ( Ms_o - MHPH8EXT_o - MHPH7EXT_o - Maux_o)
#         #     # print(f"Cold Reheat Steam Flow (Mcrh) [kg/hr] Operating: {Mcrh_o}")
#         #     print(f"Cold Reheat Steam Flow (Mcrh) [kg/hr]: {Mcrh}")
#         #     #Hot reheat steam flow ( MRH) 
#         #     MRH = ( Mcrh + MRHspray)
#             MRH_o = ( Mcrh_o + MRHspray_o)
#             print(f"Hot Reheat Steam Flow (MRH) [kg/hr]: {MRH_o}")
       
#             HR_o1 = (
#             (Ms_o * Hms_o)
#             + (Mcrh_o * (Hrh_o - Hcrh_o))
#             + (MRHspray_o * (Hrh_o - Hrhspray_o))
#             - (MFWfi_o * HHPH8o_o)
#             - (MSHspray_o *  HHPH6i_o)
#         ) / (Mw_o * 1000)
#             HR_o = HR_o1 / 4.184
#             print(f"Heat Rate (HR) [kJ/kg]: {HR_o}")
#             print(f"Heat Rate (HR) [kJ/kWh]: {HR_o/4.184}")

#             return ThermalResults3( MFWii_o = MFWii_o, MFWfi_o= MFWfi_o, iteration = iteration, MRH_o = MRH_o , HR_o = HR_o , Ms_o = Ms_o , Hms_o = Hms_o)
        

#         # Step 4: Update MFWii
        
#         MFWii_o += step_size * diff_o

#         # Step 5: Explicitly call thermal performance again immediately after update
        
#         df.loc["FEED WATER FLOW", "VALUES (O)"] = MFWii_o / 1000
#         calculate_thermal_performance(df)  # 👈 call immediately after update
   
#     print("❌ Did not converge")
#     print(f"Final MWFii: {MFWii_o:.6f}, MFWfi: {MFWfi_o:.6f}")
#     return MFWii_o, MFWfi_o, max_iter,MRH_o
# def what_if_iteration_o(df, max_iter=25, tolerance=0.00000005):
#     # Initial value in kg/hr
#     MFWii_o = float(df.loc["FEED WATER FLOW", "Values (D)"]) * 1000
#     print(f"Initial MFWii_o: {MFWii_o:.6f}")

#     for iteration in range(max_iter):
#         # Step 1: Update the DataFrame input (in t/hr)
#         df.loc["FEED WATER FLOW", "VALUES (O)"] = MFWii_o / 1000

#         # Step 2: Run performance calculation
#         results = calculate_thermal_performance(df)
#         MFWfi_o = results.MFWfi_o

#         # Step 3: Check difference
#         diff_o = MFWfi_o - MFWii_o
#         print(f"Iter {iteration}: MFWii_o={MFWii_o:.6f}, MFWfi_o={MFWfi_o:.6f}, diff_o={diff_o:.6f}")

#         if abs(diff_o) < tolerance:
#             print(f"✅ Converged at iteration {iteration}")
            
#             # Collect required parameters
#             MUA_o = float(df.loc["Hotwell storage change", "VALUES (O)"])
#             MSHspray_o = results.MSHspray_o
#             MHPH8EXT_o = results.MHPH8EXT_o
#             MHPH7EXT_o = results.MHPH7EXT_o
#             MHPH6EXT_o = results.MHPH6EXT_o
#             MRHspray_o = results.MRHspray_o
#             Hms_o = results.Hms_o
#             Hcrh_o = results.Hcrh_o
#             Hrh_o = results.Hrh_o
#             Hrhspray_o = results.Hrhspray_o
#             HHPH8o_o = results.HHPH8o_o
#             HHPH6i_o = results.HHPH6i_o
#             Mw_o = results.Mw_o

#             # Calculate flows and HR
#             Ms_o = MFWfi_o + MSHspray_o + MUA_o
#             Maux_o = 0
#             Mcrh_o = Ms_o - MHPH8EXT_o - MHPH7EXT_o - Maux_o
#             MRH_o = Mcrh_o + MRHspray_o

#             HR_o1 = (
#                 (Ms_o * Hms_o)
#                 + (Mcrh_o * (Hrh_o - Hcrh_o))
#                 + (MRHspray_o * (Hrh_o - Hrhspray_o))
#                 - (MFWfi_o * HHPH8o_o)
#                 - (MSHspray_o * HHPH6i_o)
#             ) / (Mw_o * 1000)
#             HR_o = HR_o1 / 4.184  # Convert to kJ/kWh


#             print(f"Heat Rate (HR) [kJ/kg]: {HR_o}")
#             print(f"Heat Rate (HR) [kJ/kWh]: {HR_o1 / 4.184}")

#             # return ThermalResults3(MFWii_o=MFWii_o, MFWfi_o=MFWfi_o, iteration=iteration + 1, MRH_o=MRH_o)
#             return ThermalResults3( MFWii_o = MFWii_o, MFWfi_o= MFWfi_o, iteration = iteration + 1, MRH_o = MRH_o , HR_o = HR_o , Ms_o = Ms_o , Hms_o = Hms_o)

#         # Step 4: Direct substitution for faster convergence
#         MFWii_o = MFWfi_o

#     print("❌ Did not converge")
#     print(f"Final MFWii_o: {MFWii_o:.6f}, MFWfi_o: {MFWfi_o:.6f}")
#     return MFWii_o, MFWfi_o, max_iter, results.MRHspray_o  # fallback in case MRH_o was never set
def what_if_iteration_o(df, max_iter=25, tolerance=5e-8):
    MFWii_o = float(df.loc["FEED WATER FLOW", "Values (D)"]) * 1000

    for _ in range(max_iter):
        df.loc["FEED WATER FLOW", "VALUES (O)"] = MFWii_o / 1000
        results = calculate_thermal_performance(df)
        MFWfi_o = results.MFWfi_o

        if abs(MFWfi_o - MFWii_o) < tolerance:
            MUA_o = float(df.loc["Hotwell storage change", "VALUES (O)"])
            Ms_o = MFWfi_o + results.MSHspray_o + MUA_o
            Mcrh_o = Ms_o - results.MHPH8EXT_o - results.MHPH7EXT_o
            MRH_o = Mcrh_o + results.MRHspray_o

            HR_kJ_kg = (
                (Ms_o * results.Hms_o)
                + (Mcrh_o * (results.Hrh_o - results.Hcrh_o))
                + (results.MRHspray_o * (results.Hrh_o - results.Hrhspray_o))
                - (MFWfi_o * results.HHPH8o_o)
                - (results.MSHspray_o * results.HHPH6i_o)
            ) / (results.Mw_o * 1000)

            HR_o = HR_kJ_kg / 4.184
            print(f"Heat Rate (HR) [kJ/kg]: {HR_o}")

            return ThermalResults3(
                MFWii_o=MFWii_o,
                MFWfi_o=MFWfi_o,
                iteration=_ + 1,
                MRH_o=MRH_o,
                HR_o=HR_o,
                Ms_o=Ms_o,
                Hms_o=results.Hms_o,
                MHPH6EXT_o = results.MHPH6EXT_o,
                MDAEXT_o = results.MDAEXT_o
            )

        MFWii_o = MFWfi_o  # Direct substitution for fastest convergence
    print("❌ Did not converge")

    return MFWii_o, MFWfi_o, max_iter, results.MRHspray_o








def calculated_Heater(df):
    """
    Calculate LPH based on the input dataframe.
    """
    # HPH #8 Enthalpies
    HPH8_EXT_pressure_bar = (float(df.loc["HPH-8 EXT PRESSURE"]["Values (D)"]))
    HPH8_EXT_pressure_bar_o = (float(df.loc["HPH-8 EXT PRESSURE"]["VALUES (O)"]))
   
    HPH8_EXT_temp = float(df.loc["HPH-8 EXT TEMP"]["Values (D)"])
    HPH8_EXT_temp_o = float(df.loc["HPH-8 EXT TEMP"]["VALUES (O)"])
    HHPH8EXT = get_enthalpy(HPH8_EXT_pressure_bar, HPH8_EXT_temp)
    HHPH8EXT_o = get_enthalpy(HPH8_EXT_pressure_bar_o, HPH8_EXT_temp_o)
    print(f"HPH-8 EXT Enthalpy HHPH8EXT (kJ/kg): {HHPH8EXT}")
    print(f"HPH-8 EXT Enthalpy HHPH8EXT_o (kJ/kg): {HHPH8EXT_o}")

    # HPH8_FW_out_pressure_bar = mpato_bar(float(df.loc["HPH-8 FW O/L PRESSURE"]["DESIGN"]))
    HPH8_FW_out_pressure_bar = (float(df.loc["HPH-8 FW O/L PRESSURE"]["Values (D)"]))
    HPH8_FW_out_pressure_bar_o = (float(df.loc["HPH-8 FW O/L PRESSURE"]["VALUES (O)"]))
    HPH8_FW_out_temp = float(df.loc["HPH-8 FW O/L TEMP"]["Values (D)"])
    HPH8_FW_out_temp_o = float(df.loc["HPH-8 FW O/L TEMP"]["VALUES (O)"])
    HHPH8o = get_enthalpy(HPH8_FW_out_pressure_bar, HPH8_FW_out_temp)
    HHPH8o_o = get_enthalpy(HPH8_FW_out_pressure_bar_o, HPH8_FW_out_temp_o)
    print(f"HPH-8 FW O/L Enthalpy HHPH8o (kJ/kg): {HHPH8o}")
    print(f"HPH-8 FW O/L Enthalpy HHPH8o_o (kJ/kg): {HHPH8o_o}")

    # HPH7_FW_out_pressure_bar = mpato_bar(float(df.loc["HPH-7 FW O/L PRESSURE"]["DESIGN"]))
    HPH7_FW_out_pressure_bar = (float(df.loc["HPH-7 FW O/L PRESSURE"]["Values (D)"]))
    HPH7_FW_out_pressure_bar_o = (float(df.loc["HPH-7 FW O/L PRESSURE"]["VALUES (O)"]))
    HPH7_FW_out_temp = float(df.loc["HPH-7 FW O/L TEMP"]["Values (D)"])
    HPH7_FW_out_temp_o = float(df.loc["HPH-7 FW O/L TEMP"]["VALUES (O)"])
   
    HHPH8i = get_enthalpy(HPH7_FW_out_pressure_bar, HPH7_FW_out_temp)  # feedwater inlet for HPH8
    HHPH8i_o = get_enthalpy(HPH7_FW_out_pressure_bar_o, HPH7_FW_out_temp_o)  # feedwater inlet for HPH8 operating
    print(f"HPH-8 FW I/L Enthalpy HHPH8i (kJ/kg):HHPH8i {HHPH8i}")
    print(f"HPH-8 FW I/L Enthalpy HHPH8i_o (kJ/kg): {HHPH8i_o}")
   
    # For HPH8 Drip temperature, assume enthalpy of saturated liquid at that temp
    HPH8_drip_temp = float(df.loc["HPH-8 DRIP TEMP"]["Values (D)"])
    HPH8_drip_temp_o = float(df.loc["HPH-8 DRIP TEMP"]["VALUES (O)"])
    HHPH8D = get_enthalpy_saturated_liquid_temp(HPH8_drip_temp)  
    HHPH8D_o = get_enthalpy_saturated_liquid_temp(HPH8_drip_temp_o) 
    print(f"HPH-8 Drip Enthalpy HHPH8D (kJ/kg)HHPH8D: {HHPH8D}")
    print(f"HPH-8 Drip Enthalpy HHPH8D_o (kJ/kg): {HHPH8D_o}")
    
    result2 = what_if_iteration(df)
    result = what_if_iteration_o(df)
    
    Water_flow_through_tubesHPH8 = result2.MFWfi/1000
    Water_flow_through_tubesHPH8_o = result.MFWfi_o/ 1000
    print(f"flowHPH8 {Water_flow_through_tubesHPH8}")
    print(f"flowHPH8_o {Water_flow_through_tubesHPH8_o}")


     # HPH7_EXT_pressure_bar = mpato_bar(float(df.loc["HPH-7 EXT PRESSURE"]["DESIGN"]))
    HPH7_EXT_pressure_bar = (float(df.loc["HPH-7 EXT PRESSURE"]["Values (D)"]))
    HPH7_EXT_pressure_bar_o = (float(df.loc["HPH-7 EXT PRESSURE"]["VALUES (O)"]))
    HPH7_EXT_temp = float(df.loc["HPH-7 EXT TEMP"]["Values (D)"])
    HPH7_EXT_temp_o = float(df.loc["HPH-7 EXT TEMP"]["VALUES (O)"])
    HHPH7EXT = get_enthalpy(HPH7_EXT_pressure_bar, HPH7_EXT_temp)
    HHPH7EXT_o = get_enthalpy(HPH7_EXT_pressure_bar_o, HPH7_EXT_temp_o)
    print(f"HPH-7 EXT Enthalpy HHPH7EXT (kJ/kg): {HHPH7EXT}")
    print(f"HPH-7 EXT Enthalpy HHPH7EXT_o (kJ/kg): {HHPH7EXT_o}")

    # HPH7_FW_out_pressure_bar = mpato_bar(float(df.loc["HPH-7 FW O/L PRESSURE"]["DESIGN"]))
    HPH7_FW_out_pressure_bar = (float(df.loc["HPH-7 FW O/L PRESSURE"]["Values (D)"]))
    HPH7_FW_out_pressure_bar_o = (float(df.loc["HPH-7 FW O/L PRESSURE"]["VALUES (O)"]))
    HPH7_FW_out_temp = float(df.loc["HPH-7 FW O/L TEMP"]["Values (D)"])
    HPH7_FW_out_temp_o = float(df.loc["HPH-7 FW O/L TEMP"]["VALUES (O)"])
    
    HHPH7o = get_enthalpy(HPH7_FW_out_pressure_bar, HPH7_FW_out_temp)
    HHPH7o_o = get_enthalpy(HPH7_FW_out_pressure_bar_o, HPH7_FW_out_temp_o)
    print(f"HPH-7 FW O/L Enthalpy HHPH7o (kJ/kg): {HHPH7o}")
    print(f"HPH-7 FW O/L Enthalpy HHPH7o_o (kJ/kg): {HHPH7o_o}")
    

    # HPH6_FW_out_pressure_bar = mpato_bar(float(df.loc["HPH-6 FW O/L PRESSURE"]["DESIGN"]))
    HPH6_FW_out_pressure_bar = (float(df.loc["HPH-6 FW O/L PRESSURE"]["Values (D)"]))
    HPH6_FW_out_pressure_bar_o = (float(df.loc["HPH-6 FW O/L PRESSURE"]["VALUES (O)"]))
    HPH6_FW_out_temp = float(df.loc["HPH-6 FW O/L TEMP"]["Values (D)"])
    HPH6_FW_out_temp_o = float(df.loc["HPH-6 FW O/L TEMP"]["VALUES (O)"])
    HHPH7i = get_enthalpy(HPH6_FW_out_pressure_bar, HPH6_FW_out_temp)  # inlet for HPH7
    HHPH7i_o = get_enthalpy(HPH6_FW_out_pressure_bar_o, HPH6_FW_out_temp_o)  # inlet for HPH7 operating
    print(f"HPH-7 FW I/L Enthalpy HHPH7i (kJ/kg): {HHPH7i}")
    print(f"HPH-7 FW I/L Enthalpy HHPH7i_o (kJ/kg): {HHPH7i_o}")
   

    HPH7_drip_temp = float(df.loc["HPH-7 DRIP TEMP"]["Values (D)"])
    HPH7_drip_temp_o = float(df.loc["HPH-7 DRIP TEMP"]["VALUES (O)"])
    HHPH7D = get_enthalpy_saturated_liquid_temp(HPH7_drip_temp)  # approx
    HHPH7D_o = get_enthalpy_saturated_liquid_temp(HPH7_drip_temp_o)  # approx operating
    print(f"HPH-7 Drip Enthalpy HHPH7D (kJ/kg): {HHPH7D}")
    print(f"HPH-7 Drip Enthalpy HHPH7D_o (kJ/kg): {HHPH7D_o}")

    Water_flow_through_tubesHPH7 = result2.MFWfi/1000
    Water_flow_through_tubesHPH7_o = result.MFWfi_o/ 1000
    print(f"flowHPH7 {Water_flow_through_tubesHPH7}")
    print(f"flowHPH7_o {Water_flow_through_tubesHPH7_o}")


    
    HPH6_EXT_pressure_bar = (float(df.loc["HPH-6 EXT PRESSURE"]["Values (D)"]))
    HPH6_EXT_pressure_bar_o = (float(df.loc["HPH-6 EXT PRESSURE"]["VALUES (O)"]))
    HPH6_EXT_temp = float(df.loc["HPH-6 EXT TEMP"]["Values (D)"])
    HPH6_EXT_temp_o = float(df.loc["HPH-6 EXT TEMP"]["VALUES (O)"])
    HHPH6EXT = get_enthalpy(HPH6_EXT_pressure_bar, HPH6_EXT_temp)
    HHPH6EXT_o = get_enthalpy(HPH6_EXT_pressure_bar_o, HPH6_EXT_temp_o)
    print(f"HPH-6 EXT Enthalpy HHPH6EXT (kJ/kg): {HHPH6EXT}")
    print(f"HPH-6 EXT Enthalpy HHPH6EXT_o (kJ/kg): {HHPH6EXT_o}")
   

    # HPH6_FW_out_pressure_bar = mpato_bar(float(df.loc["HPH-6 FW O/L PRESSURE"]["DESIGN"]))
    HPH6_FW_out_pressure_bar = (float(df.loc["HPH-6 FW O/L PRESSURE"]["Values (D)"]))
    HPH6_FW_out_pressure_bar_o = (float(df.loc["HPH-6 FW O/L PRESSURE"]["VALUES (O)"]))
    HPH6_FW_out_temp = float(df.loc["HPH-6 FW O/L TEMP"]["Values (D)"])
    HPH6_FW_out_temp_o = float(df.loc["HPH-6 FW O/L TEMP"]["VALUES (O)"])
    HHPH6o = get_enthalpy(HPH6_FW_out_pressure_bar, HPH6_FW_out_temp)
    HHPH6o_o = get_enthalpy(HPH6_FW_out_pressure_bar_o, HPH6_FW_out_temp_o)
    print(f"HPH-6 FW O/L Enthalpy HHPH6o (kJ/kg): {HHPH6o}")
    print(f"HPH-6 FW O/L Enthalpy HHPH6o_o (kJ/kg): {HHPH6o_o}")
   

    # HPH6_FW_in_pressure_bar = mpato_bar(float(df.loc["HPH-6 FW I/L PRESSURE"]["DESIGN"]))
    HPH6_FW_in_pressure_bar = float(df.loc["HPH-6 FW I/L PRESSURE"]["Values (D)"])
    HPH6_FW_in_pressure_bar_o = float(df.loc["HPH-6 FW I/L PRESSURE"]["VALUES (O)"])
    HPH6_FW_in_temp = float(df.loc["HPH-6 FW I/L TEMP"]["Values (D)"])
    HPH6_FW_in_temp_o = float(df.loc["HPH-6 FW I/L TEMP"]["VALUES (O)"])
    HHPH6i = get_enthalpy(HPH6_FW_in_pressure_bar, HPH6_FW_in_temp)
    HHPH6i_o = get_enthalpy(HPH6_FW_in_pressure_bar_o, HPH6_FW_in_temp_o)
    print(f"HPH-6 FW I/L Enthalpy HHPH6i (kJ/kg): {HHPH6i}")
    print(f"HPH-6 FW I/L Enthalpy HHPH6i_o (kJ/kg): {HHPH6i_o}")
   

    HPH6_drip_temp = float(df.loc["HPH-6 DRIP TEMP"]["Values (D)"])
    HPH6_drip_temp_o = float(df.loc["HPH-6 DRIP TEMP"]["VALUES (O)"])
    HHPH6D = get_enthalpy_saturated_liquid_temp(HPH6_drip_temp)
    HHPH6D_o = get_enthalpy_saturated_liquid_temp(HPH6_drip_temp_o)
    print(f"HPH-6 Drip Enthalpy HHPH6D (kJ/kg): {HHPH6D}")
    print(f"HPH-6 Drip Enthalpy HHPH6D_o (kJ/kg): {HHPH6D_o}")

    Water_flow_through_tubesHPH6 = result2.MFWfi/1000
    Water_flow_through_tubesHPH6_o = result.MFWfi_o/ 1000
    print(f"flowHPH7 {Water_flow_through_tubesHPH6}")
    print(f"flowHPH7_o {Water_flow_through_tubesHPH6_o}")




    dea_ext_pressure_bar = (float(df.loc["DEA EXT STEAM PRESSURE"]["Values (D)"]))
    dea_ext_pressure_bar_o = (float(df.loc["DEA EXT STEAM PRESSURE"]["VALUES (O)"]))
    dea_ext_temp = float(df.loc["DEA EXT STEAM TEMP"]["Values (D)"])
    dea_ext_temp_o = float(df.loc["DEA EXT STEAM TEMP"]["VALUES (O)"])
    HDEAEXT = get_enthalpy(dea_ext_pressure_bar, dea_ext_temp)
    HDEAEXT_o = get_enthalpy(dea_ext_pressure_bar_o, dea_ext_temp_o)
    print(f"Deaerator Extraction Steam Enthalpy HDEAEXT_o (kJ/kg): {HDEAEXT_o}")
    print(f"Deaerator Extraction Steam Enthalpy HDEAEXT (kJ/kg): {HDEAEXT}")
    print(f"dea_ext_pressure_bar {dea_ext_pressure_bar} dea_ext_temp {dea_ext_temp}")
    print(f"dea_ext_pressure_bar_o {dea_ext_pressure_bar_o} dea_ext_temp {dea_ext_temp_o}")

    # Deaerator #5 Feedwater Outlet Enthalpy (HDEAo)
    dea_o_temp = float(df.loc["BFP I/L FW TEMP"]["Values (D)"])  # This is HDEAo temp
    dea_o_temp_o = float(df.loc["BFP I/L FW TEMP"]["VALUES (O)"])  # This is HDEAo temp operating
    #dea_o_pressure_bar = dea_i_pressure_bar  # assume same pressure
    HDEAo = get_enthalpy_saturated_liquid_temp( dea_o_temp)
    HDEAo_o = get_enthalpy_saturated_liquid_temp(dea_o_temp_o)
    print(f"Deaerator Outlet Enthalpy HDEAo_o (kJ/kg): {HDEAo_o}")
    print(f"Deaerator Outlet Enthalpy HDEAo (kJ/kg): {HDEAo}")
   

    # Deaerator #5 Extraction Steam Enthalpy (HDEAEXT)
    # dea_ext_pressure_bar = mpato_bar(float(df.loc["DEA EXT STEAM PRESSURE"]["DESIGN"]))
    


    dea_i_pressure_bar = (float(df.loc["DEA EXT STEAM PRESSURE"]["Values (D)"]))
    dea_i_pressure_bar_o = (float(df.loc["DEA EXT STEAM PRESSURE"]["VALUES (O)"]))
    dea_i_temp = float(df.loc["DEA I/L COND TEMP"]["Values (D)"])
    dea_i_temp_o = float(df.loc["DEA I/L COND TEMP"]["VALUES (O)"])
    HDEAi = get_enthalpy(dea_i_pressure_bar, dea_i_temp)
    HDEAi_o = get_enthalpy(dea_i_pressure_bar_o, dea_i_temp_o)
    print(f"Deaerator Inlet Enthalpy HDEAi_o (kJ/kg): {HDEAi_o}")
    print(f"Deaerator Inlet Enthalpy HDEAi (kJ/kg): {HDEAi}")
    print(f"dea_i_temp_o:{dea_i_temp_o}")
    
    result3 = calculate_thermal_performance(df)
    Water_flow_through_tubesHPH5 = result3.MCDSTDi/1000
    Water_flow_through_tubesHPH5_o = result3.MCDSTDi_o/1000
    
    print(f"Water_flow_through_tubesHPH5:{Water_flow_through_tubesHPH5}")
    print(f"Water_flow_through_tubesHPH5_o:{Water_flow_through_tubesHPH5_o}")



    #LPH4
    LPH4_EXT_pressure_bar = (float(df.loc["EXT-4  STEAM PRESS."]["Values (D)"]))
    LPH4_EXT_pressure_bar_o = (float(df.loc["EXT-4  STEAM PRESS."]["VALUES (O)"]))
    #LPH4_EXT_pressure_bar = 3.768
    LPH4_EXT_temp = float(df.loc["EXT-4 STEAM TEMP"]["Values (D)"])
    LPH4_EXT_temp_o = float(df.loc["EXT-4 STEAM TEMP"]["VALUES (O)"])
    #LPH4_EXT_temp = 272.17
    # print(f"LPH-4 EXT Pressure (bar): {LPH4_EXT_pressure_bar}")
    # print(f"LPH-4 EXT Temperature (C): {LPH4_EXT_temp}")
    LHPH4EXT = get_enthalpy(LPH4_EXT_pressure_bar, LPH4_EXT_temp)
    LHPH4EXT_o = get_enthalpy(LPH4_EXT_pressure_bar_o, LPH4_EXT_temp_o)
    print(f"LPH-4 EXT Enthalpy LHPH4EXT_o (kJ/kg): {LHPH4EXT_o}")
    print(f"LPH-4 EXT Enthalpy LHPH4EXT (kJ/kg): {LHPH4EXT}")

    LPH4_FW_out_pressure_bar = (float(df.loc["CEP O/L PRESSURE"]["Values (D)"]))
    print(f"PH4_FW_out_pressure_bar: {LPH4_FW_out_pressure_bar}")
    LPH4_FW_out_pressure_bar_o = (float(df.loc["CEP O/L PRESSURE"]["VALUES (O)"]))
    LPH4_FW_out_temp = float(df.loc["LPH-4 O/L WATER TEMP"]["Values (D)"])
    print(f" LPH4_FW_out_temp:{LPH4_FW_out_temp}")
    LPH4_FW_out_temp_o = float(df.loc["LPH-4 O/L WATER TEMP"]["VALUES (O)"])
    # print(f"LPH-4 FW O/L Pressure (bar): {LPH4_FW_out_pressure_bar}")
    # print(f"LPH-4 FW O/L Temperature (C): {LPH4_FW_out_temp}")
    LHPH4o = get_enthalpy(LPH4_FW_out_pressure_bar, LPH4_FW_out_temp)
    LHPH4o_o = get_enthalpy(LPH4_FW_out_pressure_bar_o, LPH4_FW_out_temp_o)
    print(f"LPH-4 FW O/L Enthalpy LHPH4o (kJ/kg): {LHPH4o}")
    print(f"LPH-4 FW O/L Enthalpy HHPH4_o (kJ/kg): {LHPH4o_o}")

    LPH7_FW_out_pressure_bar = (float(df.loc["CEP O/L PRESSURE"]["Values (D)"]))
    LPH7_FW_out_pressure_bar_o = (float(df.loc["CEP O/L PRESSURE"]["VALUES (O)"]))
    print(f"LPH-7 FW O/L Pressure (bar): {LPH7_FW_out_pressure_bar}")
    LPH7_FW_out_temp = float(df.loc["LPH-3 O/L WATER TEMP"]["Values (D)"])
    LPH7_FW_out_temp_o = float(df.loc["LPH-3 O/L WATER TEMP"]["VALUES (O)"])
    print(f"LPH-7 FW O/L Temperature (C): {LPH7_FW_out_temp}")
   
    LHPH4i = get_enthalpy(LPH7_FW_out_pressure_bar, LPH7_FW_out_temp)  # feedwater inlet for HPH8
    LHPH4i_o = get_enthalpy(LPH7_FW_out_pressure_bar_o, LPH7_FW_out_temp_o)
    print(f"LPH-4 FW I/L Enthalpy LHPH4i (kJ/kg):HHPH8i {LHPH4i}")
    print(f"LPH-4 FW I/L Enthalpy LHPH4i_o (kJ/kg):HHPH8i_o {LHPH4i_o}")

     # For HPH8 Drip temperature, assume enthalpy of saturated liquid at that temp
    LPH4_drain_temp = float(df.loc["LPH-4 DRAIN TEMP"]["Values (D)"])
    LPH4_drain_temp_o = float(df.loc["LPH-4 DRAIN TEMP"]["VALUES (O)"])
    LHPH4D = get_enthalpy_saturated_liquid_temp(LPH4_drain_temp)  # approx
    LHPH4D_o = get_enthalpy_saturated_liquid_temp(LPH4_drain_temp_o)
    print(f"LPH-8 Drain Enthalpy LHPH4D (kJ/kg)HHPH8D: {LHPH4D}")
    print(f"LPH-8 Drain Enthalpy LHPH4D_o (kJ/kg)HHPH8D_o: {LHPH4D_o}")

    Water_flow_through_tubesLPH4 = float(df.loc["CONDENSATE FLOW "]["Values (D)"])/1000
    Water_flow_through_tubesLPH4_o = float(df.loc["CONDENSATE FLOW "]["VALUES (O)"])/1000
    print(f"Water_flow_through_tubesLPH4:{Water_flow_through_tubesLPH4}")
    print(f"Water_flow_through_tubesLPH4_o:{Water_flow_through_tubesLPH4_o}")

    #LPH3


    LPH3_EXT_pressure_bar = (float(df.loc["EXT-3 STEAM PRESS."]["Values (D)"]))
    LPH3_EXT_pressure_bar_o = (float(df.loc["EXT-3 STEAM PRESS."]["VALUES (O)"]))
    LPH3_EXT_temp = float(df.loc["EXT-3 STAEM TEMP"]["Values (D)"])
    LPH3_EXT_temp_o = float(df.loc["EXT-3 STAEM TEMP"]["VALUES (O)"])
    LHPH3EXT = get_enthalpy(LPH3_EXT_pressure_bar, LPH3_EXT_temp)
    LHPH3EXT_o = get_enthalpy(LPH3_EXT_pressure_bar_o, LPH3_EXT_temp_o)
    # print(f"LPH-3 EXT Pressure (bar): {LPH3_EXT_pressure_bar}")
    # print(f"LPH-3 EXT Temperature (C): {LPH3_EXT_temp}")
    print(f"LPH-3 EXT Enthalpy LHPH3EXT (kJ/kg): {LHPH3EXT}")
    print(f"LPH-3 EXT Enthalpy LHPH3EXT_o (kJ/kg): {LHPH3EXT_o}")

    LPH3_FW_out_pressure_bar = (float(df.loc["CEP O/L PRESSURE"]["Values (D)"]))
    LPH3_FW_out_pressure_bar_o = (float(df.loc["CEP O/L PRESSURE"]["VALUES (O)"]))
    LPH3_FW_out_temp = float(df.loc["LPH-3 O/L WATER TEMP"]["Values (D)"])
    LPH3_FW_out_temp_o = float(df.loc["LPH-3 O/L WATER TEMP"]["VALUES (O)"])
    
    LHPH3o = get_enthalpy(LPH3_FW_out_pressure_bar, LPH3_FW_out_temp)
    LHPH3o_o = get_enthalpy(LPH3_FW_out_pressure_bar_o, LPH3_FW_out_temp_o)
    # print(f"LPH-3 FW O/L Pressure (bar): {LPH3_FW_out_pressure_bar}")
    # print(f"LPH-3 FW O/L Temperature (C): {LPH3_FW_out_temp}")
    print(f"LPH-3 FW O/L Enthalpy LHPH3o (kJ/kg): {LHPH3o}")
    print(f"LPH-3 FW O/L Enthalpy LHPH3o_o (kJ/kg): {LHPH3o_o}")
    

    LPH6_FW_out_pressure_bar = (float(df.loc["CEP O/L PRESSURE"]["Values (D)"]))
    LPH6_FW_out_pressure_bar_o = (float(df.loc["CEP O/L PRESSURE"]["VALUES (O)"]))
    LPH6_FW_out_temp = float(df.loc["LPH-2 O/L WATER TEMP"]["Values (D)"])
    LPH6_FW_out_temp_o = float(df.loc["LPH-2 O/L WATER TEMP"]["VALUES (O)"])
    LHPH3i = get_enthalpy(LPH6_FW_out_pressure_bar, LPH6_FW_out_temp)
    LHPH3i_o = get_enthalpy(LPH6_FW_out_pressure_bar_o, LPH6_FW_out_temp_o)  # inlet for HPH7
    # print(f"LPH-3 FW I/L Pressure (bar): {LPH6_FW_out_pressure_bar}")
    # print(f"LPH-3 FW I/L Temperature (C): {LPH6_FW_out_temp}")
    print(f"LPH- FW I/L Enthalpy LHPH3i (kJ/kg): {LHPH3i}")
    print(f"LPH- FW I/L Enthalpy LHPH3i_o (kJ/kg): {LHPH3i_o}")
   

    LPH3_drain_temp = float(df.loc["LPH-3 DRAIN TEMP"]["Values (D)"])
    LPH3_drain_temp_o = float(df.loc["LPH-3 DRAIN TEMP"]["VALUES (O)"])
    LHPH3D = get_enthalpy_saturated_liquid_temp(LPH3_drain_temp)  # approx
    LHPH3D_o = get_enthalpy_saturated_liquid_temp(LPH3_drain_temp_o)
    print(f"HPH-7 Drip Enthalpy HHPH7D (kJ/kg): {LHPH3D}")
    print(f"HPH-7 Drip Enthalpy HHPH7D_o (kJ/kg): {LHPH3D_o}")


    Water_flow_through_tubesLPH3 = float(df.loc["CONDENSATE FLOW "]["Values (D)"])/1000
    Water_flow_through_tubesLPH3_o = float(df.loc["CONDENSATE FLOW "]["VALUES (O)"])/1000
    print(f"Water_flow_through_tubesLPH4:{Water_flow_through_tubesLPH3}")
    print(f"Water_flow_through_tubesLPH4_o:{Water_flow_through_tubesLPH3_o}")

    #LPH2
        
    LPH2_EXT_pressure_bar = (float(df.loc["LPH-2 I/L STEAM PRESS"]["Values (D)"]))
    LPH2_EXT_pressure_bar_o = (float(df.loc["LPH-2 I/L STEAM PRESS"]["VALUES (O)"]))
    LPH2_EXT_temp = float(df.loc["LPH-2 I/L STEAM TEMP"]["Values (D)"])
    LPH2_EXT_temp_o = float(df.loc["LPH-2 I/L STEAM TEMP"]["VALUES (O)"])
    # print(f"LPH-2 EXT Pressure (bar): {LPH2_EXT_pressure_bar}")
    # print(f"LPH-2 EXT Temperature (C): {LPH2_EXT_temp}")
    LHPH2EXT = get_enthalpy(LPH2_EXT_pressure_bar, LPH2_EXT_temp)
    LHPH2EXT_o = get_enthalpy(LPH2_EXT_pressure_bar_o, LPH2_EXT_temp_o)
    # print(f"HPH-6 EXT Enthalpy HHPH6EXT (kJ/kg): {LHPH2EXT}")
    print(f"HPH-6 EXT Enthalpy HHPH6EXT_o (kJ/kg): {LHPH2EXT_o}")
    print(f"HPH-6 EXT Enthalpy HHPH6EXT (kJ/kg): {LHPH2EXT}")
   

    LPH2_FW_out_pressure_bar = (float(df.loc["CEP O/L PRESSURE"]["Values (D)"]))
    LPH2_FW_out_pressure_bar_o = (float(df.loc["CEP O/L PRESSURE"]["VALUES (O)"]))
    LPH2_FW_out_temp = float(df.loc["LPH-2 O/L WATER TEMP"]["Values (D)"])
    LPH2_FW_out_temp_o = float(df.loc["LPH-2 O/L WATER TEMP"]["VALUES (O)"])
    LHPH2o = get_enthalpy(LPH2_FW_out_pressure_bar, LPH2_FW_out_temp)
    LHPH2o_o = get_enthalpy(LPH2_FW_out_pressure_bar_o, LPH2_FW_out_temp_o)
    # print(f"LPH-2 FW O/L Pressure (bar): {LPH2_FW_out_pressure_bar}")
    # print(f"LPH-2 FW O/L Temperature (C): {LPH2_FW_out_temp}")
    print(f"LP2HPH FW O/L Enthalpy HHPH6o (kJ/kg): {LHPH2o}")
    print(f"LP2HPH FW O/L Enthalpy HHPH6o_o (kJ/kg): {LHPH2o_o}")
   

    LPH2_FW_in_pressure_bar = (float(df.loc["CEP O/L PRESSURE"]["Values (D)"]))
    LPH2_FW_in_pressure_bar_o = (float(df.loc["CEP O/L PRESSURE"]["VALUES (O)"]))
    LPH2_FW_in_temp = float(df.loc["LPH-1 O/L WATER TEMP"]["Values (D)"])
    LPH2_FW_in_temp_o = float(df.loc["LPH-1 O/L WATER TEMP"]["VALUES (O)"])
    #LPH2_FW_in_temp =59.10
    LHPH2i = get_enthalpy(LPH2_FW_in_pressure_bar, LPH2_FW_in_temp)
    LHPH2i_o = get_enthalpy(LPH2_FW_in_pressure_bar_o, LPH2_FW_in_temp_o)
    # print(f"LPH-2 FW I/L Pressure (bar): {LPH2_FW_in_pressure_bar}")
    # print(f"LPH-2 FW I/L Temperature (C): {LPH2_FW_in_temp}")
    print(f"LP2HPH FW I/L Enthalpy HHPH6i (kJ/kg): {LHPH2i}")
    print(f"LPHPH FW I/L Enthalpy HHPH6i_o (kJ/kg): {LHPH2i_o}")
   

    LPH2_drain_temp = float(df.loc["LPH-2 DARIN TEMP"]["Values (D)"])
    LPH2_drain_temp_o = float(df.loc["LPH-2 DARIN TEMP"]["VALUES (O)"])
    LHPH2D = get_enthalpy_saturated_liquid_temp(LPH2_drain_temp)
    LHPH2D_o = get_enthalpy_saturated_liquid_temp(LPH2_drain_temp_o)
    print(f"HPH-6 Drip Enthalpy HHPH6D (kJ/kg): {LHPH2D}")
    print(f"HPH-6 Drip Enthalpy HHPH6D_o (kJ/kg): {LHPH2D_o}")

    Water_flow_through_tubesLPH2 = float(df.loc["CONDENSATE FLOW "]["Values (D)"])/1000
    Water_flow_through_tubesLPH2_o = float(df.loc["CONDENSATE FLOW "]["VALUES (O)"])/1000
    print(f"Water_flow_through_tubesLPH4:{Water_flow_through_tubesLPH2}")
    print(f"Water_flow_through_tubesLPH4_o:{Water_flow_through_tubesLPH2_o}")



     # dea_i_pressure_bar = mpato_bar(float(df.loc["DEA I/L COND PRESSURE"]["DESIGN"]))
    LP1dea_i_pressure_bar = (float(df.loc["LPH-1 I/L STEAM PRESS"]["Values (D)"]))
    LP1dea_i_pressure_bar_o = (float(df.loc["LPH-1 I/L STEAM PRESS"]["VALUES (O)"]))
    LP1dea_i_temp = float(df.loc["LPH-1 I/L STEAM TEMP"]["Values (D)"])
    LP1dea_i_temp_o = float(df.loc["LPH-1 I/L STEAM TEMP"]["VALUES (O)"])
    LP1HDEAi = get_enthalpy(LP1dea_i_pressure_bar, LP1dea_i_temp)
    LP1HDEAi_o = get_enthalpy(LP1dea_i_pressure_bar_o, LP1dea_i_temp_o)
    print(f"Deaerator Inlet Enthalpy LP1HDEAi_o (kJ/kg): {LP1HDEAi_o}")
    print(f"Deaerator Inlet Enthalpy LP1HDEAi (kJ/kg): {LP1HDEAi}")

    
   

    # Deaerator #5 Extraction Steam Enthalpy (HDEAEXT)
    # dea_ext_pressure_bar = mpato_bar(float(df.loc["DEA EXT STEAM PRESSURE"]["DESIGN"]))
    LP1dea_ext_pressure_bar = (float(df.loc["CEP O/L PRESSURE"]["Values (D)"]))
    LP1dea_ext_pressure_bar_o = (float(df.loc["CEP O/L PRESSURE"]["VALUES (O)"]))
    print(f"LP1dea_ext_pressure_bar:{LP1dea_ext_pressure_bar}")
    print(f"LP1dea_ext_pressure_bar:{LP1dea_ext_pressure_bar_o}")
    LP1dea_ext_temp = float(df.loc["LPH-1 O/L WATER TEMP"]["Values (D)"])
    LP1dea_ext_temp_o = float(df.loc["LPH-1 O/L WATER TEMP"]["VALUES (O)"])
    print(f"dea_ext_temp:{LP1dea_ext_temp}")
    print(f"dea_ext_temp_o:{LP1dea_ext_temp_o}")

    LPHDEAEXT = get_enthalpy(LP1dea_ext_pressure_bar, LP1dea_ext_temp)
    LPHDEAEXT_o = get_enthalpy(LP1dea_ext_pressure_bar_o, LP1dea_ext_temp_o)
    print(f"Deaerator Extraction Enthalpy LPHDEAEXT (kJ/kg): {LPHDEAEXT_o}")
    print(f"Deaerator Extraction Enthalpy LPHDEAEXT_o (kJ/kg): {LPHDEAEXT}")

    LPH1_FW_in_pressure_bar = (float(df.loc["CEP O/L PRESSURE"]["Values (D)"]))
    LPH1_FW_in_pressure_bar_o = (float(df.loc["CEP O/L PRESSURE"]["VALUES (O)"]))
    LPH1_FW_in_temp = float(df.loc["LPH-1 I/L WATER TEMP"]["Values (D)"])
    LPH1_FW_in_temp_o = float(df.loc["LPH-1 I/L WATER TEMP"]["VALUES (O)"])
    print(f" LPH1_FW_in_pressure_bar{ LPH1_FW_in_pressure_bar}")
    print(f" LPH1_FW_in_pressure_bar_o{ LPH1_FW_in_pressure_bar_o}")
    print(f" LPH1_FW_in_temp:{ LPH1_FW_in_temp}")
    print(f" LPH1_FW_in_temp_o:{ LPH1_FW_in_temp_o}")
    #LPH2_FW_in_temp =59.10
    LHPH1i = get_enthalpy(LPH1_FW_in_pressure_bar, LPH1_FW_in_temp)
    LHPH1i_o = get_enthalpy(LPH1_FW_in_pressure_bar_o, LPH1_FW_in_temp_o)
    print(f"LHPH1i (kJ/kg): {LHPH1i}")
    print(f"LHPH1i_o (kJ/kg): {LHPH1i_o}")

    # Deaerator #5 Feedwater Outlet Enthalpy (HDEAo)
    LP1dea_o_temp = float(df.loc["LPH-1 DRAIN TEMP"]["Values (D)"])  # This is HDEAo temp
    LP1dea_o_temp_o = float(df.loc["LPH-1 DRAIN TEMP"]["VALUES (O)"])  # This is HDEAo temp operating
    #dea_o_pressure_bar = dea_i_pressure_bar  # assume same pressure
    LP1HDEAo = get_enthalpy_saturated_liquid_temp( LP1dea_o_temp)
    LP1HDEAo_o = get_enthalpy_saturated_liquid_temp(LP1dea_o_temp_o)
    print(f"Deaerator Outlet Enthalpy HDEAo_o (kJ/kg): {LP1HDEAo_o}")
    print(f"Deaerator Outlet Enthalpy HDEAo (kJ/kg): {LP1HDEAo}")

    Water_flow_through_tubesLPH1 = float(df.loc["CONDENSATE FLOW "]["Values (D)"])/1000
    Water_flow_through_tubesLPH1_o = float(df.loc["CONDENSATE FLOW "]["VALUES (O)"])/1000
    print(f"Water_flow_through_tubesLPH4:{Water_flow_through_tubesLPH1}")
    print(f"Water_flow_through_tubesLPH4_o:{Water_flow_through_tubesLPH1_o}")

    #GSC

    GSC_EXT_pressure_bar = 1
    GSC_EXT_pressure_bar_o = 1
    # GSC_EXT_temp = float(df.loc["EXT-4 STEAM TEMP"]["Values (D)"])
    # GSC_EXT_temp_o = float(df.loc["EXT-4 STEAM TEMP"]["VALUES (O)"])
    #LPH4_EXT_temp = 272.17
    # print(f"LPH-4 EXT Pressure (bar): {LPH4_EXT_pressure_bar}")
    # print(f"LPH-4 EXT Temperature (C): {LPH4_EXT_temp}")
    # GSCEXT = get_enthalpy(GSC_EXT_pressure_bar, GSC_EXT_temp)
    # GSCEXT_o = get_enthalpy(GSC_EXT_pressure_bar_o, GSC_EXT_temp_o)
    GSCEXT =2985.311
    GSCEXT_o = 2985.311
    print(f"GSCEXT (kJ/kg): {GSCEXT}")
    print(f"GSCEXT_o (kJ/kg): {GSCEXT_o}")

    GSC_FW_out_pressure_bar = (float(df.loc["CEP O/L PRESSURE"]["Values (D)"]))
    print(f"PH4_FW_out_pressure_bar: {LPH4_FW_out_pressure_bar}")
    GSC_FW_out_pressure_bar_o = (float(df.loc["CEP O/L PRESSURE"]["VALUES (O)"]))
    GSC_FW_out_temp = float(df.loc["LPH-1 I/L WATER TEMP"]["Values (D)"])
    print(f" LPH4_FW_out_temp:{GSC_FW_out_temp}")
    GSC_FW_out_temp_o = float(df.loc["LPH-1 I/L WATER TEMP"]["VALUES (O)"])
    # print(f"LPH-4 FW O/L Pressure (bar): {LPH4_FW_out_pressure_bar}")
    # print(f"LPH-4 FW O/L Temperature (C): {LPH4_FW_out_temp}")
    GSCo = get_enthalpy(GSC_FW_out_pressure_bar, GSC_FW_out_temp)
    GSCo_o = get_enthalpy(GSC_FW_out_pressure_bar_o, GSC_FW_out_temp_o)
    print(f" GSCo : {GSCo}")
    print(f" GSCo_o {GSCo_o}")

    GSC2_FW_out_pressure_bar = (float(df.loc["CEP O/L PRESSURE"]["Values (D)"]))
    GSC2_FW_out_pressure_bar_o = (float(df.loc["CEP O/L PRESSURE"]["VALUES (O)"]))
    print(f"LPH-7 FW O/L Pressure (bar): {LPH7_FW_out_pressure_bar}")
    GSC2_FW_out_temp = float(df.loc["CEP O/L TEMP (GSC I/L)"]["Values (D)"])
    GSC2_FW_out_temp_o = float(df.loc["CEP O/L TEMP (GSC I/L)"]["VALUES (O)"])
    print(f"GSC2_FW_out_temp: {GSC2_FW_out_temp}")
   
    GSCi = get_enthalpy(GSC2_FW_out_pressure_bar, GSC2_FW_out_temp)  # feedwater inlet for HPH8
    GSCi_o = get_enthalpy(GSC2_FW_out_pressure_bar_o, GSC2_FW_out_temp_o)
    print(f"GSC FW I/L Enthalpy LHPH4i (kJ/kg):GSCi {GSCi}")
    print(f"GSC FW I/L Enthalpy LHPH4i_o (kJ/kg):GSCi_o {GSCi_o}")

     # For HPH8 Drip temperature, assume enthalpy of saturated liquid at that temp
    GSC_drain_temp = 99
    GSC_drain_temp_o = 99
    GSCD = get_enthalpy_saturated_liquid_temp(GSC_drain_temp)  # approx
    GSCD_o = get_enthalpy_saturated_liquid_temp(GSC_drain_temp_o)
    print(f"LPH-8 Drain Enthalpy LHPH4D (kJ/kg)HHPH8D: {GSCD}")
    print(f"LPH-8 Drain Enthalpy LHPH4D_o (kJ/kg)HHPH8D_o: {GSCD_o}")

    Water_flow_through_tubesGSC = float(df.loc["CONDENSATE FLOW "]["Values (D)"])/1000
    Water_flow_through_tubesGSC_o = float(df.loc["CONDENSATE FLOW "]["VALUES (O)"])/1000
    print(f"Water_flow_through_tubesGSC:{Water_flow_through_tubesGSC}")
    print(f"Water_flow_through_tubesGSC_o:{Water_flow_through_tubesGSC_o}")

    #Saturation Temp of extraction steam
    Saturation_Temp_of_extraction_steamHPH8 = get_saturation_temperature(HPH8_EXT_pressure_bar)
    print(f"Saturation_Temp_of_extraction_steamHPH8 : {Saturation_Temp_of_extraction_steamHPH8}")
    Saturation_Temp_of_extraction_steamHPH8_o = get_saturation_temperature(HPH8_EXT_pressure_bar_o)
    print(f"Saturation_Temp_of_extraction_steamHPH8 : {Saturation_Temp_of_extraction_steamHPH8_o}")
    
    Saturation_Temp_of_extraction_steamHPH7 = get_saturation_temperature(HPH7_EXT_pressure_bar)
    print(f"Saturation_Temp_of_extraction_steamHPH7 : {Saturation_Temp_of_extraction_steamHPH7}")
    Saturation_Temp_of_extraction_steamHPH7_o = get_saturation_temperature(HPH7_EXT_pressure_bar_o)
    print(f"Saturation_Temp_of_extraction_steamHPH7_o : {Saturation_Temp_of_extraction_steamHPH7_o}")

    Saturation_Temp_of_extraction_steamHPH6 = get_saturation_temperature(HPH6_EXT_pressure_bar)
    print(f"Saturation_Temp_of_extraction_steamHPH6 : {Saturation_Temp_of_extraction_steamHPH6}")
    Saturation_Temp_of_extraction_steamHPH6_o = get_saturation_temperature(HPH6_EXT_pressure_bar_o)
    print(f"Saturation_Temp_of_extraction_steamHPH6_o : {Saturation_Temp_of_extraction_steamHPH6_o}")

    Saturation_Temp_of_extraction_steamHPH5 = get_saturation_temperature(dea_i_pressure_bar)
    print(f"dea_i_pressure_ba:{dea_i_pressure_bar}")
    print(f"Saturation_Temp_of_extraction_steamHPH5 : {Saturation_Temp_of_extraction_steamHPH5}")
    Saturation_Temp_of_extraction_steamHPH5_o = get_saturation_temperature(dea_i_pressure_bar_o)
    print(f"Saturation_Temp_of_extraction_steamHPH5_o : {Saturation_Temp_of_extraction_steamHPH5_o}")

    #LPH
    #Saturation Temp of extraction steam
    Saturation_Temp_of_extraction_steamLPH4 = get_saturation_temperature(LPH4_EXT_pressure_bar)
    print(f"Saturation_Temp_of_extraction_steamLPH4 : {Saturation_Temp_of_extraction_steamLPH4}")
    Saturation_Temp_of_extraction_steamLPH4_o = get_saturation_temperature(LPH4_EXT_pressure_bar_o)
    print(f"Saturation_Temp_of_extraction_steamLPH4_O : {Saturation_Temp_of_extraction_steamLPH4_o}")
    
    Saturation_Temp_of_extraction_steamLPH3 = get_saturation_temperature(LPH3_EXT_pressure_bar)
    print(f"Saturation_Temp_of_extraction_steamLPH3 : {Saturation_Temp_of_extraction_steamLPH3}")
    Saturation_Temp_of_extraction_steamLPH3_o = get_saturation_temperature(LPH3_EXT_pressure_bar_o)
    print(f"Saturation_Temp_of_extraction_steamLPH3_O : {Saturation_Temp_of_extraction_steamLPH3_o}")

    Saturation_Temp_of_extraction_steamLPH2 = get_saturation_temperature(LPH2_EXT_pressure_bar)
    print(f"Saturation_Temp_of_extraction_steamLPH2 : {Saturation_Temp_of_extraction_steamLPH2}")
    Saturation_Temp_of_extraction_steamLPH2_o = get_saturation_temperature(LPH2_EXT_pressure_bar_o)
    print(f"Saturation_Temp_of_extraction_steamLPH2_o : {Saturation_Temp_of_extraction_steamLPH2_o}")

    Saturation_Temp_of_extraction_steamLPH1 = get_saturation_temperature(LP1dea_i_pressure_bar)
    print(f"Saturation_Temp_of_extraction_steamLPH1 : {Saturation_Temp_of_extraction_steamLPH1}")
    Saturation_Temp_of_extraction_steamLPH1_o = get_saturation_temperature(LP1dea_i_pressure_bar_o)
    print(f"P1dea_i_pressure_bar_o:{LP1dea_i_pressure_bar_o}")
    print(f"Saturation_Temp_of_extraction_steamLPH1_o : {Saturation_Temp_of_extraction_steamLPH1_o}")

       #Saturation Temp of extraction steam
    Saturation_Temp_of_extraction_steamGSC = get_saturation_temperature(GSC_EXT_pressure_bar)
    print(f"Saturation_Temp_of_extraction_steamGSC : {Saturation_Temp_of_extraction_steamGSC}")
    Saturation_Temp_of_extraction_steamGSC_o = get_saturation_temperature(GSC_EXT_pressure_bar_o)
    print(f"Saturation_Temp_of_extraction_steamGSC : {Saturation_Temp_of_extraction_steamGSC_o}")

    #Feed water Temp. Rise(TR)
    Feed_water_Temp_RiseHPH8 = (HPH8_FW_out_temp - HPH7_FW_out_temp)
    Feed_water_Temp_RiseHPH8_o = (HPH8_FW_out_temp_o - HPH7_FW_out_temp_o)
    print(f"Feed_water_Temp_RiseHPH8 : {Feed_water_Temp_RiseHPH8}")
    print(f"Feed_water_Temp_RiseHPH8 : {Feed_water_Temp_RiseHPH8_o}")
    
    Feed_water_Temp_RiseHPH7 = (HPH7_FW_out_temp - HPH6_FW_out_temp)
    Feed_water_Temp_RiseHPH7_o = (HPH7_FW_out_temp_o - HPH6_FW_out_temp_o)
    print(f"Feed_water_Temp_RiseHPH7 : {Feed_water_Temp_RiseHPH7}")
    print(f"Feed_water_Temp_RiseHPH7 : {Feed_water_Temp_RiseHPH7_o}")

    Feed_water_Temp_RiseHPH6 = ( HPH6_FW_out_temp -  HPH6_FW_in_temp)
    Feed_water_Temp_RiseHPH6_o = ( HPH6_FW_out_temp_o -  HPH6_FW_in_temp_o)
    print(f"Feed_water_Temp_RiseHPH6 : {Feed_water_Temp_RiseHPH6}")
    print(f"Feed_water_Temp_RiseHPH6 : {Feed_water_Temp_RiseHPH6_o}")

    Feed_water_Temp_RiseHPH5 = (dea_o_temp - dea_i_temp)
    print(f"dea_o_temp:{dea_o_temp} dea_ext_temp {dea_i_temp}")
    Feed_water_Temp_RiseHPH5_o = (dea_o_temp_o - dea_i_temp_o)
    print(f"dea_o_temp_o:{dea_o_temp_o} dea_ext_temp_o {dea_i_temp_o}")
    print(f"Feed_water_Temp_RiseHPH5 : {Feed_water_Temp_RiseHPH5}")
    print(f"Feed_water_Temp_RiseHPH5 : {Feed_water_Temp_RiseHPH5_o}")

    #LPH
    
    Feed_water_Temp_RiseLPH4 = (LPH4_FW_out_temp -  LPH7_FW_out_temp)
    Feed_water_Temp_RiseLPH4_o = (LPH4_FW_out_temp_o-  LPH7_FW_out_temp_o)
    print(f"Feed_water_Temp_RiseLPH4 : {Feed_water_Temp_RiseLPH4}")
    print(f"Feed_water_Temp_RiseLPH4 : {Feed_water_Temp_RiseLPH4_o}")

    Feed_water_Temp_RiseLPH3 = (LPH3_FW_out_temp - LPH6_FW_out_temp)
    Feed_water_Temp_RiseLPH3_o = (LPH3_FW_out_temp_o - LPH6_FW_out_temp_o)
    print(f"Feed_water_Temp_RiseLPH3 : {Feed_water_Temp_RiseLPH3}")
    print(f"Feed_water_Temp_RiseLPH3 : {Feed_water_Temp_RiseLPH3_o}")

    Feed_water_Temp_RiseLPH2 = (LPH2_FW_out_temp -  LPH2_FW_in_temp)
    Feed_water_Temp_RiseLPH2_o = (LPH2_FW_out_temp_o -  LPH2_FW_in_temp_o)
    print(f"Feed_water_Temp_RiseLPH2 : {Feed_water_Temp_RiseLPH2}")
    print(f"Feed_water_Temp_RiseLPH2 : {Feed_water_Temp_RiseLPH2_o}")

    Feed_water_Temp_RiseLPH1 = (LP1dea_ext_temp - LPH1_FW_in_temp)
    Feed_water_Temp_RiseLPH1_o = (LP1dea_ext_temp_o - LPH1_FW_in_temp_o)
    print(f"Feed_water_Temp_RiseHPH8 : {Feed_water_Temp_RiseLPH1}")
    print(f"Feed_water_Temp_RiseHPH8 : {Feed_water_Temp_RiseLPH1_o}")
    print(f"PH1_FW_in_temp_o{LPH1_FW_in_temp_o},LP1dea_ext_temp{LP1dea_ext_temp}")

    Feed_water_Temp_RiseGSC = (  GSC_FW_out_temp - GSC2_FW_out_temp )
    
    Feed_water_Temp_RiseGSC_o = (GSC_FW_out_temp_o - GSC2_FW_out_temp_o)
    print(f"Feed_water_Temp_RiseGSC : {Feed_water_Temp_RiseGSC}")
    print(f"Feed_water_Temp_RiseGSC_o : {Feed_water_Temp_RiseGSC_o}")

    #TTD (Terminal Temp. Diff.)
    Terminal_Temp_DiffHPH8 =(Saturation_Temp_of_extraction_steamHPH8 - HPH8_FW_out_temp )
    Terminal_Temp_DiffHPH8_o =(Saturation_Temp_of_extraction_steamHPH8_o -  HPH8_FW_out_temp_o)
    print(f"Terminal_Temp_DiffHPH8 : {Terminal_Temp_DiffHPH8} Terminal_Temp_DiffHPH8_o: {Terminal_Temp_DiffHPH8_o}")

    
    Terminal_Temp_DiffHPH7 =(Saturation_Temp_of_extraction_steamHPH7 - HPH7_FW_out_temp )
    Terminal_Temp_DiffHPH7_o =(Saturation_Temp_of_extraction_steamHPH7_o -  HPH7_FW_out_temp_o)
    print(f"Terminal_Temp_DiffHPH7 : {Terminal_Temp_DiffHPH7} Terminal_Temp_DiffHPH7_o: {Terminal_Temp_DiffHPH7_o}")

    
    Terminal_Temp_DiffHPH6 =(Saturation_Temp_of_extraction_steamHPH6 - HPH6_FW_out_temp )
    Terminal_Temp_DiffHPH6_o =(Saturation_Temp_of_extraction_steamHPH6_o -  HPH6_FW_out_temp_o)
    print(f"Terminal_Temp_DiffHPH6 : {Terminal_Temp_DiffHPH6} Terminal_Temp_DiffHPH6_o: {Terminal_Temp_DiffHPH6_o}")
    
    
    Terminal_Temp_DiffHPH5 =(Saturation_Temp_of_extraction_steamHPH5 - dea_o_temp )
    Terminal_Temp_DiffHPH5_o =(Saturation_Temp_of_extraction_steamHPH5_o - dea_o_temp_o)
    print(f"Terminal_Temp_DiffHPH5 : {Terminal_Temp_DiffHPH5} Terminal_Temp_DiffHPH5_o: {Terminal_Temp_DiffHPH5_o}")

    # #LPH
    Terminal_Temp_DiffLPH4 =(Saturation_Temp_of_extraction_steamLPH4 - LPH4_FW_out_temp )
    Terminal_Temp_DiffLPH4_o =(Saturation_Temp_of_extraction_steamLPH4_o -  LPH4_FW_out_temp_o)
    print(f"Terminal_Temp_DiffLPH4 : {Terminal_Temp_DiffLPH4} Terminal_Temp_DiffLPH4_o: {Terminal_Temp_DiffLPH4_o}")

    
    Terminal_Temp_DiffLPH3 =(Saturation_Temp_of_extraction_steamLPH3 - LPH3_FW_out_temp )
    Terminal_Temp_DiffLPH3_o =(Saturation_Temp_of_extraction_steamLPH3_o -  LPH3_FW_out_temp_o)
    print(f"Terminal_Temp_DiffLPH3 : {Terminal_Temp_DiffLPH3} Terminal_Temp_DiffLPH3_o: {Terminal_Temp_DiffLPH3_o}")

    
    Terminal_Temp_DiffLPH2 =(Saturation_Temp_of_extraction_steamLPH2 - LPH2_FW_out_temp )
    Terminal_Temp_DiffLPH2_o =(Saturation_Temp_of_extraction_steamLPH2_o -  LPH2_FW_out_temp_o)
    print(f"Terminal_Temp_DiffLPH2 : {Terminal_Temp_DiffLPH2} Terminal_Temp_DiffLPH2_o: {Terminal_Temp_DiffLPH2_o}")
    
    
    Terminal_Temp_DiffLPH1 =(Saturation_Temp_of_extraction_steamLPH1 - LP1dea_ext_temp )
    Terminal_Temp_DiffLPH1_o =(Saturation_Temp_of_extraction_steamLPH1_o -  LP1dea_ext_temp_o)
    print(f"Terminal_Temp_DiffLPH1 : {Terminal_Temp_DiffLPH1} Terminal_Temp_DiffLPH1_o: {Terminal_Temp_DiffLPH1_o}")
    print(f"LP1dea_ext_temp{LP1dea_ext_temp_o}")
    print(f"Saturation_Temp_of_extraction_steamLPH1_o :{Saturation_Temp_of_extraction_steamLPH1_o}")

    Terminal_Temp_DiffGSC =(Saturation_Temp_of_extraction_steamGSC - GSC_FW_out_temp )
    Terminal_Temp_DiffGSC_o =(Saturation_Temp_of_extraction_steamGSC_o -  GSC_FW_out_temp_o)
    print(f"Terminal_Temp_DiffGCS : {Terminal_Temp_DiffGSC} Terminal_Temp_DiffGSC_o: {Terminal_Temp_DiffGSC_o}")


    # Drain Cooler Approach Temp.(DCA)
    Drain_Cooler_Approach_TempHPH8 = (HPH8_drip_temp - HPH7_FW_out_temp)
    Drain_Cooler_Approach_TempHPH8_o = (HPH8_drip_temp_o - HPH7_FW_out_temp_o)
    print(f"Drain_Cooler_Approach_TempHPH8 {Drain_Cooler_Approach_TempHPH8} Drain_Cooler_Approach_TempHPH8_o:{Drain_Cooler_Approach_TempHPH8_o}")
    
   
    Drain_Cooler_Approach_TempHPH7 = (HPH7_drip_temp -  HPH6_FW_out_temp)
    Drain_Cooler_Approach_TempHPH7_o = (HPH7_drip_temp_o - HPH6_FW_out_temp_o)
    print(f"Drain_Cooler_Approach_TempHPH8 {Drain_Cooler_Approach_TempHPH7} Drain_Cooler_Approach_TempHPH8_o:{Drain_Cooler_Approach_TempHPH7_o}")

    Drain_Cooler_Approach_TempHPH6 = (HPH6_drip_temp -  HPH6_FW_in_temp)
    Drain_Cooler_Approach_TempHPH6_o = (HPH6_drip_temp_o - HPH6_FW_in_temp_o)
    print(f"Drain_Cooler_Approach_TempHPH8 {Drain_Cooler_Approach_TempHPH6} Drain_Cooler_Approach_TempHPH8_o:{Drain_Cooler_Approach_TempHPH6_o}")
    Drain_Cooler_Approach_TempHPH5 =0
    Drain_Cooler_Approach_TempHPH5_o =0
    #LPH
    Drain_Cooler_Approach_TempLPH4 = (LPH4_drain_temp -  LPH7_FW_out_temp)
    Drain_Cooler_Approach_TempLPH4_o = ( LPH4_drain_temp_o -LPH7_FW_out_temp_o)
    print(f"Drain_Cooler_Approach_TempLPH4 {Drain_Cooler_Approach_TempLPH4} Drain_Cooler_Approach_TempLPH4_o:{Drain_Cooler_Approach_TempLPH4_o}")

    Drain_Cooler_Approach_TempLPH3 = (LPH3_drain_temp -  LPH6_FW_out_temp)
    Drain_Cooler_Approach_TempLPH3_o = (LPH3_drain_temp_o - LPH6_FW_out_temp_o)
    print(f"Drain_Cooler_Approach_TempLPH3 {Drain_Cooler_Approach_TempLPH3} Drain_Cooler_Approach_TempLPH3_o:{Drain_Cooler_Approach_TempLPH3_o}")

    Drain_Cooler_Approach_TempLPH2 = (LPH2_drain_temp -  LPH2_FW_in_temp)
    Drain_Cooler_Approach_TempLPH2_o = (LPH2_drain_temp_o - LPH2_FW_in_temp_o)
    print(f"Drain_Cooler_Approach_TempLPH2 {Drain_Cooler_Approach_TempLPH2} Drain_Cooler_Approach_TempLPH2_o:{Drain_Cooler_Approach_TempLPH2_o}")

    Drain_Cooler_Approach_TempLPH1 = (LP1dea_o_temp -  LPH1_FW_in_temp)
    Drain_Cooler_Approach_TempLPH1_o = (LP1dea_o_temp_o - LPH1_FW_in_temp_o)
    print(f"Drain_Cooler_Approach_TempLPH1 {Drain_Cooler_Approach_TempLPH1} Drain_Cooler_Approach_TempLPH1_o:{Drain_Cooler_Approach_TempLPH1_o}")

    Drain_Cooler_Approach_TempGSC = (GSC_drain_temp - GSC2_FW_out_temp)
    Drain_Cooler_Approach_TempGSC_o = (GSC_drain_temp_o - GSC2_FW_out_temp_o)
    print(f"Drain_Cooler_Approach_TempHPH8 {Drain_Cooler_Approach_TempGSC} Drain_Cooler_Approach_TempHPH8_o:{Drain_Cooler_Approach_TempGSC_o}")

#Extraction steam flow
    Extraction_steam_flowHPH8 = ((Water_flow_through_tubesHPH8 * (HHPH8o - HHPH8i))/(HHPH8EXT - HHPH8D ))
    print(f"Water_flow_through_tubesHPH8 :{Water_flow_through_tubesHPH8} ,HHPH8o : {HHPH8o}, HHPH8i{HHPH8i} ")
    print(f"HHPH8EXT : {HHPH8EXT},HHPH8D : {HHPH8D} ")
    print(f"Extraction_steam_flowHPH8: {Extraction_steam_flowHPH8}")

    Extraction_steam_flowHPH8_o = ((Water_flow_through_tubesHPH8_o * (HHPH8o_o - HHPH8i_o))/(HHPH8EXT_o - HHPH8D_o ))
    print(f"Water_flow_through_tubesHPH8_o :{Water_flow_through_tubesHPH8_o} ,HHPH8o : {HHPH8o_o}, HHPH8i{HHPH8i_o} ")
    print(f"HHPH8EXT_o : {HHPH8EXT},HHPH8D_o : {HHPH8D} ")
    print(f"Extraction_steam_flowHPH8: {Extraction_steam_flowHPH8_o}")

    Extraction_steam_flowHPH7 = ((Water_flow_through_tubesHPH7 * (HHPH7o - HHPH7i) - (Extraction_steam_flowHPH8*(HHPH8D - HHPH7D )) )/(HHPH7EXT - HHPH7D ))
    print(f"Extraction_steam_flowHPH7: {Extraction_steam_flowHPH7}")

    Extraction_steam_flowHPH7_o = ((Water_flow_through_tubesHPH7_o * (HHPH7o_o - HHPH7i_o) - (Extraction_steam_flowHPH8_o*(HHPH8D_o - HHPH7D_o )) )/(HHPH7EXT_o - HHPH7D_o ))
    print(f"Extraction_steam_flowHPH7_o : {Extraction_steam_flowHPH7_o}")

    Extraction_steam_flowHPH6 = ((Water_flow_through_tubesHPH6 * (HHPH6o - HHPH6i) - (Extraction_steam_flowHPH8 + Extraction_steam_flowHPH7)*(HHPH7D - HHPH6D )) /(HHPH6EXT - HHPH6D ))
    print(f"Extraction_steam_flowHPH6: {Extraction_steam_flowHPH6}")

    Extraction_steam_flowHPH6_o = ((Water_flow_through_tubesHPH6_o * (HHPH6o_o - HHPH6i_o) - (Extraction_steam_flowHPH8_o + Extraction_steam_flowHPH7_o)*(HHPH7D_o - HHPH6D_o )) /(HHPH6EXT_o - HHPH6D_o ))
    print(f"Extraction_steam_flowHPH6: {Extraction_steam_flowHPH6_o}")

    # Extraction_steam_flowHPH5 = ((Water_flow_through_tubesHPH5 * (HDEAo - HDEAi) - (Extraction_steam_flowHPH8 + Extraction_steam_flowHPH7+Extraction_steam_flowHPH6)*( HHPH6D - HDEAo )) /(HDEAEXT - HDEAo ))
    Extraction_steam_flowHPH5 = ((Water_flow_through_tubesHPH5 * (HDEAo - HDEAi) - (Extraction_steam_flowHPH8 + Extraction_steam_flowHPH7+Extraction_steam_flowHPH6)*( HHPH6D - HDEAo )) /(HDEAEXT - HDEAo ))
    print(f"Extraction_steam_flowHPH5: {Extraction_steam_flowHPH5}")
    print(f"water_flow_through_tubesHPH5 :{Water_flow_through_tubesHPH5} ,HDEAo : {HDEAo}, HDEAi{HDEAi} ")
    print(f"HDEAEXT : {HDEAEXT},HDEAo : {HDEAo} ")
    print(f"Extraction_steam_flowHPH8: {Extraction_steam_flowHPH8}")
    print(f"Extraction_steam_flowHPH7: {Extraction_steam_flowHPH7} Extraction_steam_flowHPH6: {Extraction_steam_flowHPH6}")
   
    print(f"HDEAo {HDEAo}")
    print(f"HDEAEXT : {HDEAEXT}")
    print(f"HHPH6D : {HHPH6D}")
    print(f"HDEAi :{HDEAi}")

    Extraction_steam_flowHPH5_o = ((Water_flow_through_tubesHPH5_o * (HDEAo_o - HDEAi_o) - (Extraction_steam_flowHPH8_o + Extraction_steam_flowHPH7_o + Extraction_steam_flowHPH6_o)*( HHPH6D_o - HDEAo_o )) /(HDEAEXT_o - HDEAo_o ))
    print(f"Extraction_steam_flowHPH5: {Extraction_steam_flowHPH5_o}")
    print(f"HDEAo {HDEAo_o}")
    print(f"HDEAEXT : {HDEAEXT_o}")
    print(f"HHPH6D : {HHPH6D_o}")
    print(f"HDEAi :{HDEAi_o}")


    #LPH
    Extraction_steam_flowLPH4 = ((Water_flow_through_tubesLPH4 * (LHPH4o - LHPH4i) ) /(LHPH4EXT - LHPH4D))
    print(f"Extraction_steam_flowLPH4: {Extraction_steam_flowLPH4}")
    Extraction_steam_flowLPH4_o = ((Water_flow_through_tubesLPH4_o * (LHPH4o_o - LHPH4i_o) ) /(LHPH4EXT_o - LHPH4D_o))
    print(f"Extraction_steam_flowLPH4_o: {Extraction_steam_flowLPH4_o}")

    Extraction_steam_flowLPH3 = ((Water_flow_through_tubesLPH3 * (LHPH3o - LHPH3i) - ( Extraction_steam_flowLPH4 *(LHPH4D-LHPH3D))) /(LHPH3EXT - LHPH3D))
    print(f"Extraction_steam_flowLPH3: {Extraction_steam_flowLPH3}")

    Extraction_steam_flowLPH3_o = ((Water_flow_through_tubesLPH3_o * (LHPH3o_o - LHPH3i_o) - ( Extraction_steam_flowLPH4_o *(LHPH4D_o-LHPH3D_o))) /(LHPH3EXT_o - LHPH3D_o))
    print(f"Extraction_steam_flowLPH3_O: {Extraction_steam_flowLPH3_o}")

    Extraction_steam_flowLPH2 = ((Water_flow_through_tubesLPH2 * (LHPH2o - LHPH2i) - ( (Extraction_steam_flowLPH4 +Extraction_steam_flowLPH3) *(LHPH3D-LHPH2D))) /(LHPH2EXT - LHPH2D))
    print(f"Extraction_steam_flowLPH2: {Extraction_steam_flowLPH2}")

    Extraction_steam_flowLPH2_o = ((Water_flow_through_tubesLPH2_o * (LHPH2o_o - LHPH2i_o) - ( (Extraction_steam_flowLPH4_o +Extraction_steam_flowLPH3_o) *(LHPH3D_o-LHPH2D_o))) /(LHPH2EXT_o - LHPH2D_o))
    print(f"Extraction_steam_flowLPH2_O: {Extraction_steam_flowLPH2_o}")

    Extraction_steam_flowLPH1 = ((Water_flow_through_tubesLPH1 * (LPHDEAEXT - LHPH1i) - ( (Extraction_steam_flowLPH4 +Extraction_steam_flowLPH3+Extraction_steam_flowLPH2) *(LHPH2D-LP1HDEAo))-5.775*(263.6-LP1HDEAo)) /(LP1HDEAi - LP1HDEAo))
    print(f"Extraction_steam_flowLPH1: {Extraction_steam_flowLPH1}")
    print(f"LPHDEAEXT {LPHDEAEXT} LHPH1i {LHPH1i}")

    Extraction_steam_flowLPH1_o = ((Water_flow_through_tubesLPH1_o * (LPHDEAEXT_o - LHPH1i_o) - ( (Extraction_steam_flowLPH4_o +Extraction_steam_flowLPH3_o+Extraction_steam_flowLPH2_o) *(LHPH2D_o-LP1HDEAo_o))-5.775*(263.6-LP1HDEAo_o)) /(LP1HDEAi_o - LP1HDEAo_o))
    print(f"Extraction_steam_flowLPH1: {Extraction_steam_flowLPH1_o}")
    print(f"LPHDEAEXT {LPHDEAEXT_o} LHPH1i {LHPH1i_o}")

    Extraction_steam_flowGSC = ((Water_flow_through_tubesGSC * (GSCo - GSCi) ) /(GSCEXT - GSCD))
    print(f"Extraction_steam_flowGSC: {Extraction_steam_flowGSC}")
    Extraction_steam_flowGSC_o = ((Water_flow_through_tubesGSC_o * (GSCo_o - GSCi_o) ) /(GSCEXT_o - GSCD_o))
    print(f"Extraction_steam_flowGSC: {Extraction_steam_flowGSC_o}")

    

    # return
    return ThermalresultsHeater(MHPH1EXT=Extraction_steam_flowLPH1,
                                MHPH2EXT=Extraction_steam_flowLPH2,
                                MHPH3EXT=Extraction_steam_flowLPH3,
                                MHPH4EXT=Extraction_steam_flowLPH4,
                                MHPH1EXT_o=Extraction_steam_flowLPH1_o,
                                MHPH2EXT_o=Extraction_steam_flowLPH2_o, 
                                MHPH3EXT_o=Extraction_steam_flowLPH3_o,
                                MHPH4EXT_o=Extraction_steam_flowLPH4_o,
                                Extraction_steam_flowGSC =Extraction_steam_flowGSC,
                                Extraction_steam_flowGSC_o =Extraction_steam_flowGSC_o,
                                GSCD=GSCD,
                                GSCD_o=GSCD_o,
                                LP1HDEAo= LP1HDEAo,
                                LP1HDEAo_o= LP1HDEAo_o,
                                Saturation_Temp_of_extraction_steamHPH8 = Saturation_Temp_of_extraction_steamHPH8,
                                Saturation_Temp_of_extraction_steamHPH8_o = Saturation_Temp_of_extraction_steamHPH8_o,
                                Saturation_Temp_of_extraction_steamHPH7 = Saturation_Temp_of_extraction_steamHPH7,
                                Saturation_Temp_of_extraction_steamHPH7_o = Saturation_Temp_of_extraction_steamHPH7_o,
                                Saturation_Temp_of_extraction_steamHPH6 = Saturation_Temp_of_extraction_steamHPH6,
                                Saturation_Temp_of_extraction_steamHPH6_o = Saturation_Temp_of_extraction_steamHPH6_o,
                                Saturation_Temp_of_extraction_steamHPH5 = Saturation_Temp_of_extraction_steamHPH5,
                                Saturation_Temp_of_extraction_steamHPH5_o = Saturation_Temp_of_extraction_steamHPH5_o,
                                Saturation_Temp_of_extraction_steamLPH4 = Saturation_Temp_of_extraction_steamLPH4,
                                Saturation_Temp_of_extraction_steamLPH4_o = Saturation_Temp_of_extraction_steamLPH4_o,
                                Saturation_Temp_of_extraction_steamLPH3 = Saturation_Temp_of_extraction_steamLPH3,
                                Saturation_Temp_of_extraction_steamLPH3_o = Saturation_Temp_of_extraction_steamLPH3_o,
                                Saturation_Temp_of_extraction_steamLPH2 = Saturation_Temp_of_extraction_steamLPH2,
                                Saturation_Temp_of_extraction_steamLPH2_o = Saturation_Temp_of_extraction_steamLPH2_o,
                                Saturation_Temp_of_extraction_steamLPH1 = Saturation_Temp_of_extraction_steamLPH1,
                                Saturation_Temp_of_extraction_steamLPH1_o = Saturation_Temp_of_extraction_steamLPH1_o,
                                Saturation_Temp_of_extraction_steamGSC = Saturation_Temp_of_extraction_steamGSC,
                                Saturation_Temp_of_extraction_steamGSC_o = Saturation_Temp_of_extraction_steamGSC_o,
                                Feed_water_Temp_RiseHPH8 = Feed_water_Temp_RiseHPH8,
                                Feed_water_Temp_RiseHPH8_o = Feed_water_Temp_RiseHPH8_o,
                                Feed_water_Temp_RiseHPH7 = Feed_water_Temp_RiseHPH7,
                                Feed_water_Temp_RiseHPH7_o = Feed_water_Temp_RiseHPH7_o,
                                Feed_water_Temp_RiseHPH6 = Feed_water_Temp_RiseHPH6,
                                Feed_water_Temp_RiseHPH6_o = Feed_water_Temp_RiseHPH6_o,
                                Feed_water_Temp_RiseHPH5 = Feed_water_Temp_RiseHPH5,
                                Feed_water_Temp_RiseHPH5_o = Feed_water_Temp_RiseHPH5_o,
                                Feed_water_Temp_RiseLPH4 = Feed_water_Temp_RiseLPH4,
                                Feed_water_Temp_RiseLPH4_o = Feed_water_Temp_RiseLPH4_o,
                                Feed_water_Temp_RiseLPH3 = Feed_water_Temp_RiseLPH3,
                                Feed_water_Temp_RiseLPH3_o = Feed_water_Temp_RiseLPH3_o,
                                Feed_water_Temp_RiseLPH2 = Feed_water_Temp_RiseLPH2,
                                Feed_water_Temp_RiseLPH2_o = Feed_water_Temp_RiseLPH2_o,
                                Feed_water_Temp_RiseLPH1 = Feed_water_Temp_RiseLPH1,
                                Feed_water_Temp_RiseLPH1_o = Feed_water_Temp_RiseLPH1_o,
                                Feed_water_Temp_RiseGSC = Feed_water_Temp_RiseGSC,
                                Feed_water_Temp_RiseGSC_o = Feed_water_Temp_RiseGSC_o,
                                Terminal_Temp_DiffHPH8 = Terminal_Temp_DiffHPH8,
                                Terminal_Temp_DiffHPH8_o = Terminal_Temp_DiffHPH8,
                                Terminal_Temp_DiffHPH7 = Terminal_Temp_DiffHPH7,
                                Terminal_Temp_DiffHPH7_o = Terminal_Temp_DiffHPH7_o,
                                Terminal_Temp_DiffHPH6 = Terminal_Temp_DiffHPH6,
                                Terminal_Temp_DiffHPH6_o = Terminal_Temp_DiffHPH6_o,
                                Terminal_Temp_DiffHPH5 = Terminal_Temp_DiffHPH5,
                                Terminal_Temp_DiffHPH5_o = Terminal_Temp_DiffHPH5_o,
                                Terminal_Temp_DiffLPH4 = Terminal_Temp_DiffLPH4,
                                Terminal_Temp_DiffLPH4_o = Terminal_Temp_DiffLPH4_o,
                                Terminal_Temp_DiffLPH3 = Terminal_Temp_DiffLPH3,
                                Terminal_Temp_DiffLPH3_o = Terminal_Temp_DiffLPH3_o,
                                Terminal_Temp_DiffLPH2 = Terminal_Temp_DiffLPH2,
                                Terminal_Temp_DiffLPH2_o = Terminal_Temp_DiffLPH2_o,
                                Terminal_Temp_DiffLPH1 = Terminal_Temp_DiffLPH1,
                                Terminal_Temp_DiffLPH1_o = Terminal_Temp_DiffLPH1_o,
                                Terminal_Temp_DiffGSC = Terminal_Temp_DiffGSC,
                                Terminal_Temp_DiffGSC_o = Terminal_Temp_DiffGSC_o,
                                Drain_Cooler_Approach_TempHPH8 = Drain_Cooler_Approach_TempHPH8,
                                Drain_Cooler_Approach_TempHPH8_o = Drain_Cooler_Approach_TempHPH8_o,
                                Drain_Cooler_Approach_TempHPH7 = Drain_Cooler_Approach_TempHPH7,
                                Drain_Cooler_Approach_TempHPH7_o = Drain_Cooler_Approach_TempHPH7_o,
                                Drain_Cooler_Approach_TempHPH6 = Drain_Cooler_Approach_TempHPH6,
                                Drain_Cooler_Approach_TempHPH6_o = Drain_Cooler_Approach_TempHPH6_o,
                                Drain_Cooler_Approach_TempLPH4 = Drain_Cooler_Approach_TempLPH4,
                                Drain_Cooler_Approach_TempLPH4_o = Drain_Cooler_Approach_TempLPH4_o,
                                Drain_Cooler_Approach_TempLPH3 = Drain_Cooler_Approach_TempLPH3,
                                Drain_Cooler_Approach_TempLPH3_o = Drain_Cooler_Approach_TempLPH3_o,
                                Drain_Cooler_Approach_TempLPH2 = Drain_Cooler_Approach_TempLPH2,
                                Drain_Cooler_Approach_TempLPH2_o = Drain_Cooler_Approach_TempLPH2_o,
                                Drain_Cooler_Approach_TempLPH1 = Drain_Cooler_Approach_TempLPH1,
                                Drain_Cooler_Approach_TempLPH1_o = Drain_Cooler_Approach_TempLPH1_o,
                                Drain_Cooler_Approach_TempGSC = Drain_Cooler_Approach_TempGSC,
                                Drain_Cooler_Approach_TempGSC_o = Drain_Cooler_Approach_TempGSC_o,
                                Extraction_steam_flowHPH8 =  Extraction_steam_flowHPH8,
                                 Extraction_steam_flowHPH7 = Extraction_steam_flowHPH7,
                                 Extraction_steam_flowHPH6 = Extraction_steam_flowHPH6,
                                 Extraction_steam_flowHPH5 = Extraction_steam_flowHPH5,
                                 Extraction_steam_flowHPH8_o =  Extraction_steam_flowHPH8_o,
                                 Extraction_steam_flowHPH7_o = Extraction_steam_flowHPH7_o,
                                 Extraction_steam_flowHPH6_o = Extraction_steam_flowHPH6_o,
                                 Extraction_steam_flowHPH5_o = Extraction_steam_flowHPH5_o,
                                 Drain_Cooler_Approach_TempHPH5 = Drain_Cooler_Approach_TempHPH5,
                                 Drain_Cooler_Approach_TempHPH5_o = Drain_Cooler_Approach_TempHPH5_o,)
def condencer(df):
    # resultsc = calculate_thermal_performance(df)
    resultW = what_if_iteration(df)
    resultW_o = what_if_iteration_o(df)
    resultsh = calculated_Heater(df)
    resultsSTM = extract_pressure_temp_values_from_df(df)
    resultsTE = calculate_turbine_efficiencies(df)
    print(f"resultsTE: {resultsTE}")
    # Total_Exaust_steam_flow_rate_from_LP_turbine = (resultW.MRH - resultsc.MHPH6EXT - resultsc. MDAEXT ) - (resultsh.MHPH1EXT * 1000+ resultsh.MHPH2EXT* 1000 + resultsh.MHPH3EXT* 1000 + resultsh.MHPH4EXT* 1000 ) 
    Total_Exaust_steam_flow_rate_from_LP_turbine = (resultW.MRH - resultW.MHPH6EXT - resultW. MDAEXT ) - (resultsh.MHPH1EXT * 1000+ resultsh.MHPH2EXT* 1000 + resultsh.MHPH3EXT* 1000 + resultsh.MHPH4EXT* 1000 ) 
    # print(f"resultW.MRH: {resultW.MRH}, resultsc.MHPH6EXT: {resultW.MHPH6EXT}, resultsc.MDAEXT: {resultW.MDAEXT}")
    # print(f"resultsh.MHPH1EXT: {resultsh.MHPH1EXT}, resultsh.MHPH2EXT: {resultsh.MHPH2EXT}, resultsh.MHPH3EXT: {resultsh.MHPH3EXT}, resultsh.MHPH4EXT: {resultsh.MHPH4EXT}")
    print(f"Total_Exaust_steam_flow_rate_from_LP_turbine: {Total_Exaust_steam_flow_rate_from_LP_turbine}")
    Total_Exaust_steam_flow_rate_from_LP_turbine_o = (resultW_o.MRH_o - resultW_o.MHPH6EXT_o - resultW_o. MDAEXT_o ) - (resultsh.MHPH1EXT * 1000+ resultsh.MHPH2EXT* 1000 + resultsh.MHPH3EXT* 1000 + resultsh.MHPH4EXT* 1000 ) 
    # print(f"resultW.MRH_o: {resultW_o.MRH_o}, resultsc.MHPH6EXT: {resultW_o.MHPH6EXT_o}, resultsc.MDAEXT: {resultW_o.MDAEXT_o}")
    print(f"resultsh.MHPH1EXT: {resultsh.MHPH1EXT_o}, resultsh.MHPH2EXT: {resultsh.MHPH2EXT_o}, resultsh.MHPH3EXT: {resultsh.MHPH3EXT_o}, resultsh.MHPH4EXT: {resultsh.MHPH4EXT_o}")
    print(f"Total_Exaust_steam_flow_rate_from_LP_turbine_o: {Total_Exaust_steam_flow_rate_from_LP_turbine_o}")
    # Total_Exaust_steam_flow_rate_from_LP_turbine = resultc.MHPH6EXT+resultc.MHPH7EXT+resultc.MHPH8EXT
    Steam_flow_rate_from_GSC = resultsh.Extraction_steam_flowGSC*1000
    print(f"Steam_flow_rate_from_GSC: {Steam_flow_rate_from_GSC}")
    Steam_flow_rate_from_GSC_o = resultsh.Extraction_steam_flowGSC_o*1000
    print(f"Steam_flow_rate_from_GSC: {Steam_flow_rate_from_GSC_o}")
    Condensate_Temperature = float(df.loc["CEP I/L TEMP"]["Values (D)"])
    Condensate_Temperature_o = float(df.loc["CEP I/L TEMP"]["VALUES (O)"])
    Condenser_outlet_enthalpy_h4 =  get_enthalpy_saturated_liquid_temp(Condensate_Temperature)
    print(f"Condenser_outlet_enthalpy_h4: {Condenser_outlet_enthalpy_h4}")
    Condenser_outlet_enthalpy_h4_o =  get_enthalpy_saturated_liquid_temp(Condensate_Temperature_o)
    print(f"Condenser_outlet_enthalpy_h4: {Condenser_outlet_enthalpy_h4_o}")
    Enthalpy_of_steam_from_GSC_to_main_condenser_h3 = resultsh.GSCD
    print(f"Enthalpy_of_steam_from_GSC_to_main_condenser_h3: {Enthalpy_of_steam_from_GSC_to_main_condenser_h3}")
    Enthalpy_of_steam_from_GSC_to_main_condenser_h3_o = resultsh.GSCD_o
    print(f"Enthalpy_of_steam_from_GSC_to_main_condenser_h3: {Enthalpy_of_steam_from_GSC_to_main_condenser_h3_o}")
    Drain_from_Last_LP_heaters_to_condenser_m5 = (resultsh.MHPH1EXT + resultsh.MHPH2EXT + resultsh.MHPH3EXT + resultsh.MHPH4EXT+ resultsh.Extraction_steam_flowGSC) * 1000
    print(f"Drain_from_Last_LP_heaters_to_condenser_m5: {Drain_from_Last_LP_heaters_to_condenser_m5}")
    Drain_from_Last_LP_heaters_to_condenser_m5_o = (resultsh.MHPH1EXT_o + resultsh.MHPH2EXT_o + resultsh.MHPH3EXT_o + resultsh.MHPH4EXT_o+ resultsh.Extraction_steam_flowGSC_o) * 1000
    print(f"Drain_from_Last_LP_heaters_to_condenser_m5_o: {Drain_from_Last_LP_heaters_to_condenser_m5_o}")
    Enthalpy_of_Last_LP_heaters_to_condenser_h5 = resultsh.LP1HDEAo
    print(f"Enthalpy_of_Last_LP_heaters_to_condenser_h5: {Enthalpy_of_Last_LP_heaters_to_condenser_h5}")
    Enthalpy_of_Last_LP_heaters_to_condenser_h5_o = resultsh.LP1HDEAo_o
    print(f"Enthalpy_of_Last_LP_heaters_to_condenser_h5_o: {Enthalpy_of_Last_LP_heaters_to_condenser_h5_o}")
    Condenser_Vaccum = float(df.loc["CONDENSOR VACUUM (DCS)"]["Values (D)"])*100
    print(f"Condenser_Vaccum: {Condenser_Vaccum}")
    Condenser_Vaccum_o = float(df.loc["CONDENSOR VACUUM (DCS)"]["VALUES (O)"])*100
    print(f"Condenser_Vaccum: {Condenser_Vaccum_o}")
    T_Sat_at_Condenser_Vaccum =( get_saturation_temperature(Condenser_Vaccum/100))
    print(f"T_Sat_at_Condenser_Vaccum: {T_Sat_at_Condenser_Vaccum}")
    T_Sat_at_Condenser_Vaccum_o = get_saturation_temperature(Condenser_Vaccum_o/100)
    print(f"T_Sat_at_Condenser_Vaccum_o: {T_Sat_at_Condenser_Vaccum_o}")
    LP_Exhaust_dryness_fraction = float(df.loc["LP EXHAUST DRYNESS FRACTION"]["Values (D)"])
    print(f"LP_Exhaust_dryness_fraction: {LP_Exhaust_dryness_fraction}")
    LP_Exhaust_dryness_fraction_o = float(df.loc["LP EXHAUST DRYNESS FRACTION"]["VALUES (O)"])
    print(f"LP_Exhaust_dryness_fraction_o: {LP_Exhaust_dryness_fraction_o}")
    Steam_from_LP_exhaust_Enthalpy_h1 = (hL_p(Condenser_Vaccum/100)*(100-LP_Exhaust_dryness_fraction)/100 + hV_p(Condenser_Vaccum/100)*(LP_Exhaust_dryness_fraction)/100)
    print(f"Steam_from_LP_exhaust_Enthalpy_h1: {Steam_from_LP_exhaust_Enthalpy_h1}")
    Steam_from_LP_exhaust_Enthalpy_h1_o = (hL_p(Condenser_Vaccum_o/100)*(100-LP_Exhaust_dryness_fraction_o)/100 + hV_p(Condenser_Vaccum_o/100)*(LP_Exhaust_dryness_fraction_o)/100)
    print(f"Steam_from_LP_exhaust_Enthalpy_h1: {Steam_from_LP_exhaust_Enthalpy_h1_o}")
   
    cop1 = float(df.loc["COND O/L WATER PRESSURE- PASS A"]["Values (D)"])
    cop2 = float(df.loc["COND O/L WATER PRESSURE- PASS B"]["Values (D)"])
    print(f"cop1: {cop1}, cop2: {cop2}")
    Condenser_Outlet_Pressure = (cop1 + cop2) / 2
    print(f"Condenser_Outlet_Pressure: {Condenser_Outlet_Pressure}")
    cop1_o = float(df.loc["COND O/L WATER PRESSURE- PASS A"]["VALUES (O)"])
    cop2_o = float(df.loc["COND O/L WATER PRESSURE- PASS B"]["VALUES (O)"])
    print(f"cop1: {cop1_o}, cop2: {cop2_o}")
    Condenser_Outlet_Pressure_o = (cop1_o + cop2_o) / 2

    print(f"Condenser_Outlet_Pressure: {Condenser_Outlet_Pressure_o}")

    cip1 = float(df.loc["COND I/L WATER PRESSURE- PASS A"]["Values (D)"])
    cip2 = float(df.loc["COND I/L WATER PRESSURE- PASS B"]["Values (D)"])

    Condenser_Inlet_Pressure = (cip1+cip2)/2
    print(f"Condenser_Inlet_Pressure: {Condenser_Inlet_Pressure}")

    cip1_o = float(df.loc["COND I/L WATER PRESSURE- PASS A"]["VALUES (O)"])
    cip2_o = float(df.loc["COND I/L WATER PRESSURE- PASS B"]["VALUES (O)"])

    Condenser_Inlet_Pressure_o = (cip1_o+cip2_o)/2
    print(f"Condenser_Inlet_Pressure: {Condenser_Inlet_Pressure_o}")

    Condenser_Inlet_Temperature = float(df.loc["COND I/L WATER TEMP- PASS A"]["Values (D)"])
    condenser_Inlet_Temperature_o = float(df.loc["COND I/L WATER TEMP- PASS A"]["VALUES (O)"])
    Condenser_Outlet_Temperature = float(df.loc["COND O/L WATER TEMP- PASS B"]["Values (D)"])
    condenser_Outlet_Temperature_o = float(df.loc["COND O/L WATER TEMP- PASS B"]["VALUES (O)"])


    Condenser_DT = Condenser_Outlet_Temperature - Condenser_Inlet_Temperature
    print(f"Condenser_DT: {Condenser_DT}")
    Condenser_DT_o = condenser_Outlet_Temperature_o - condenser_Inlet_Temperature_o
    print(f"Condenser_DT_o: {Condenser_DT_o}")

    Condenser_cooling_water_temperature_rise = Condenser_DT
    Condenser_cooling_water_temperature_rise_o = Condenser_DT_o

    Condenser_DP_of_tube_side = (Condenser_Inlet_Pressure - Condenser_Outlet_Pressure)*100
    print(f"Condenser_DP_of_tube_side: {Condenser_DP_of_tube_side}")
    Condenser_DP_of_tube_side_o = (Condenser_Inlet_Pressure_o - Condenser_Outlet_Pressure_o)*100
    print(f"Condenser_DP_of_tube_side: {Condenser_DP_of_tube_side_o}")

    Condenser_Effectiveness = Condenser_DT/((T_Sat_at_Condenser_Vaccum) - Condenser_Inlet_Temperature)*100
    print(f"Condenser_Effectiveness: {Condenser_Effectiveness}")

    Condenser_Effectiveness_o = Condenser_DT_o/(T_Sat_at_Condenser_Vaccum_o - condenser_Inlet_Temperature_o)*100
    print(f"Condenser_Effectiveness: {Condenser_Effectiveness_o}")

    Condenser_heat_load_steam_side = (((Steam_from_LP_exhaust_Enthalpy_h1 - Condenser_outlet_enthalpy_h4)*Total_Exaust_steam_flow_rate_from_LP_turbine) +((Enthalpy_of_steam_from_GSC_to_main_condenser_h3 - Condenser_outlet_enthalpy_h4)*Steam_flow_rate_from_GSC) + ((Enthalpy_of_Last_LP_heaters_to_condenser_h5 - Condenser_outlet_enthalpy_h4)*Drain_from_Last_LP_heaters_to_condenser_m5))/1000000
    print(f"Condenser_heat_load_steam_side: {Condenser_heat_load_steam_side}")
    # print(f"Steam_from_LP_exhaust_Enthalpy_h1: {Steam_from_LP_exhaust_Enthalpy_h1}, Condenser_outlet_enthalpy_h4: {Condenser_outlet_enthalpy_h4}, Total_Exaust_steam_flow_rate_from_LP_turbine: {Total_Exaust_steam_flow_rate_from_LP_turbine}, Steam_flow_rate_from_GSC: {Steam_flow_rate_from_GSC}, Enthalpy_of_Last_LP_heaters_to_condenser_h5: {Enthalpy_of_Last_LP_heaters_to_condenser_h5}, Drain_from_Last_LP_heaters_to_condenser_m5: {Drain_from_Last_LP_heaters_to_condenser_m5}")

    Condenser_heat_load_steam_side_o = (((Steam_from_LP_exhaust_Enthalpy_h1_o - Condenser_outlet_enthalpy_h4_o)*Total_Exaust_steam_flow_rate_from_LP_turbine_o) +((Enthalpy_of_steam_from_GSC_to_main_condenser_h3_o - Condenser_outlet_enthalpy_h4_o)*Steam_flow_rate_from_GSC_o) + ((Enthalpy_of_Last_LP_heaters_to_condenser_h5_o - Condenser_outlet_enthalpy_h4_o)*Drain_from_Last_LP_heaters_to_condenser_m5_o) )/ 1000000
    print(f"Condenser_heat_load_steam_side_o: {Condenser_heat_load_steam_side_o}")

    TTD = T_Sat_at_Condenser_Vaccum - Condenser_Outlet_Temperature
    print(f"TTD: {TTD}")
    TTD_o = T_Sat_at_Condenser_Vaccum_o - condenser_Outlet_Temperature_o
    print(f"TTD: {TTD_o}")
    Specific_heat_of_cooling_water = 4.186
    Specific_heat_of_cooling_water_o = 4.186

    Cooling_water_flow = Condenser_heat_load_steam_side / (Condenser_DT * Specific_heat_of_cooling_water )* 1000
    print(f"Cooling_water_flow: {Cooling_water_flow}")
    print(f"Condenser_heat_load_steam_side: {Condenser_heat_load_steam_side}, Condenser_DT: {Condenser_DT}, Specific_heat_of_cooling_water: {Specific_heat_of_cooling_water}")

    Cooling_water_flow_o = Condenser_heat_load_steam_side_o / Condenser_DT_o / Specific_heat_of_cooling_water_o * 1000
    print(f"Cooling_water_flow: {Cooling_water_flow_o}")

    Subcooling_temperature = abs(round(((T_Sat_at_Condenser_Vaccum - Condensate_Temperature)),1))
    print(f"T_Sat_at_Condenser_Vaccum: {T_Sat_at_Condenser_Vaccum}, Condensate_Temperature: {Condensate_Temperature}")
    print(f"Subcooling_temperature: {Subcooling_temperature}")

    Subcooling_temperature_o = T_Sat_at_Condenser_Vaccum_o - Condensate_Temperature_o
    print(f"Subcooling_temperature: {Subcooling_temperature_o}")
    T1 = T_Sat_at_Condenser_Vaccum - Condenser_Inlet_Temperature
    T2 = T_Sat_at_Condenser_Vaccum -  Condenser_Outlet_Temperature
    LMTD = (T1 - T2) / np.log(T1 / T2)

    # LMTD = abs((Condenser_Outlet_Temperature - Condenser_Inlet_Temperature) / np.log((Condenser_Outlet_Temperature - T_Sat_at_Condenser_Vaccum) / (Condenser_Inlet_Temperature - T_Sat_at_Condenser_Vaccum)))
    print(f"LMTD: {LMTD}")
    ΔT1 = T_Sat_at_Condenser_Vaccum_o - condenser_Inlet_Temperature_o
    ΔT2 = T_Sat_at_Condenser_Vaccum_o -  condenser_Outlet_Temperature_o
# Ensure both ΔT1 and ΔT2 are positive
    if ΔT1 <= 0 or ΔT2 <= 0:
        raise ValueError("Temperature difference must be positive")

    LMTD_o = (ΔT1 - ΔT2) / np.log(ΔT1 / ΔT2)
        # LMTD_o = (condenser_Outlet_Temperature_o - condenser_Inlet_Temperature_o) / np.log((condenser_Outlet_Temperature_o - T_Sat_at_Condenser_Vaccum_o) / (condenser_Inlet_Temperature_o - T_Sat_at_Condenser_Vaccum_o))
    print(f"LMTD_o: {LMTD_o}")
    print(f"check {resultW.MRH - resultW.MHPH6EXT - resultW. MDAEXT}")
    print(f"resultW.MRH :{resultW.MRH} ,{resultW.MHPH6EXT} ,{resultW.MDAEXT} ")
    print(f" check2 {(resultsh.MHPH1EXT * 1000+ resultsh.MHPH2EXT* 1000 + resultsh.MHPH3EXT* 1000 + resultsh.MHPH4EXT* 1000 )}")
    a = resultW.MRH - resultW.MHPH6EXT - resultW. MDAEXT
    b = resultsh.MHPH1EXT_o * 1000+ resultsh.MHPH2EXT_o* 1000 + resultsh.MHPH3EXT_o* 1000 + resultsh.MHPH4EXT_o* 1000 
    c = a-b
    print(f"check3 {c}")
    print(f"resultsh.MHPH1EXT_o{resultsh.MHPH1EXT_o} ,resultsh.MHPH2EXT_o{resultsh.MHPH2EXT_o} ,resultsh.MHPH3EXT_o{resultsh.MHPH3EXT_o} ,resultsh.MHPH4EXT_o{resultsh.MHPH4EXT_o} ")
    print(f"Total_Exaust_steam_flow_rate_from_LP_turbine;{Total_Exaust_steam_flow_rate_from_LP_turbine_o}")
    






    
    # return
    return {
        "Total_Exaust_steam_flow_rate_from_LP_turbine": Total_Exaust_steam_flow_rate_from_LP_turbine,
        "Total_Exaust_steam_flow_rate_from_LP_turbine_o": Total_Exaust_steam_flow_rate_from_LP_turbine_o,
        "Steam_flow_rate_from_GSC": Steam_flow_rate_from_GSC,
        "Steam_flow_rate_from_GSC_o": Steam_flow_rate_from_GSC_o,
        "Condenser_outlet_enthalpy_h4": Condenser_outlet_enthalpy_h4,
        "Condenser_outlet_enthalpy_h4_o": Condenser_outlet_enthalpy_h4_o,
        "Enthalpy_of_steam_from_GSC_to_main_condenser_h3": Enthalpy_of_steam_from_GSC_to_main_condenser_h3,
        "Enthalpy_of_steam_from_GSC_to_main_condenser_h3_o": Enthalpy_of_steam_from_GSC_to_main_condenser_h3_o,
        "Drain_from_Last_LP_heaters_to_condenser_m5": Drain_from_Last_LP_heaters_to_condenser_m5,
        "Drain_from_Last_LP_heaters_to_condenser_m5_o": Drain_from_Last_LP_heaters_to_condenser_m5_o,
        "Enthalpy_of_Last_LP_heaters_to_condenser_h5": Enthalpy_of_Last_LP_heaters_to_condenser_h5,
        "Enthalpy_of_Last_LP_heaters_to_condenser_h5_o": Enthalpy_of_Last_LP_heaters_to_condenser_h5_o,
        "Condenser_Vaccum": Condenser_Vaccum,
        "Condenser_Vaccum_o": Condenser_Vaccum_o,
        "T_Sat_at_Condenser_Vaccum": T_Sat_at_Condenser_Vaccum,
        "T_Sat_at_Condenser_Vaccum_o": T_Sat_at_Condenser_Vaccum_o,
        "LP_Exhaust_dryness_fraction": LP_Exhaust_dryness_fraction,
        "LP_Exhaust_dryness_fraction_o": LP_Exhaust_dryness_fraction_o,
        "Steam_from_LP_exhaust_Enthalpy_h1": Steam_from_LP_exhaust_Enthalpy_h1,
        "Steam_from_LP_exhaust_Enthalpy_h1_o": Steam_from_LP_exhaust_Enthalpy_h1_o,
        "Condenser_Outlet_Pressure": Condenser_Outlet_Pressure,
        "Condenser_Outlet_Pressure_o": Condenser_Outlet_Pressure_o,
        "Condenser_Inlet_Pressure": Condenser_Inlet_Pressure,
        "Condenser_Inlet_Pressure_o": Condenser_Inlet_Pressure_o,
        "Condenser_DT": Condenser_DT,
        "Condenser_DT_o": Condenser_DT_o,
        "Condenser_DP_of_tube_side": Condenser_DP_of_tube_side,
        "Condenser_DP_of_tube_side_o": Condenser_DP_of_tube_side_o,
        "Condenser_Effectiveness": Condenser_Effectiveness,
        "Condenser_Effectiveness_o": Condenser_Effectiveness_o,
        "Condenser_heat_load_steam_side": Condenser_heat_load_steam_side,
        "Condenser_heat_load_steam_side_o": Condenser_heat_load_steam_side_o,
        "TTD": TTD,
        "TTD_o": TTD_o,
        "Cooling_water_flow": Cooling_water_flow,
        "Cooling_water_flow_o": Cooling_water_flow_o,
        "Subcooling_temperature": Subcooling_temperature,
        "Subcooling_temperature_o": Subcooling_temperature_o,
        "LMTD": LMTD,
        "LMTD_o": LMTD_o,
        "resultsTE": resultsTE,
        
        # Optionally include input results as well
        # "resultsc": resultsc,
        "resultW": resultW,
        "resultW_o": resultW_o,
        "resultsh": resultsh,
        "resultsSTM":resultsSTM,
    }

def extract_pressure_temp_values_from_df(df):
    # Strip column names and index
    df.columns = [col.strip() for col in df.columns]
    df.index = df.index.astype(str).str.strip()

    # Parameter lists
    pressure_parameters = [
        "MS PRESSURE AT TURBINE I/L", "HPH-8 EXT PRESSURE", "CRH PRESSURE", "HRH PRESSURE",
        "HPH-6 EXT PRESSURE", "DEA EXT STEAM PRESSURE", "EXT-4  STEAM PRESS.", "EXT-3 STEAM PRESS.",
        "LPH-2 I/L STEAM PRESS", "LPH-1 I/L STEAM PRESS", "CONDENSOR VACUUM (DCS)"
    ]

    temperature_parameters = [
        "MS TEMP AT TV1", "HPH-8 EXT TEMP", "CRH TEMP", "IP I/L LH TEMP", "HPH-6 EXT TEMP",
        "DEA EXT STEAM TEMP", "EXT-4 STEAM TEMP", "EXT-3 STAEM TEMP",
        "LPH-2 I/L STEAM TEMP", "LPH-1 I/L STEAM TEMP","CEP I/L TEMP",
    ]

    def fetch_parameters(param_list):
        design_vals = {}
        operating_vals = {}

        for param in param_list:
            param_key = param.strip()
            if param_key in df.index:
                design = df.at[param_key, 'Values (D)']
                operating = df.at[param_key, 'VALUES (O)']
                design_vals[param] = design
                operating_vals[param] = operating
                print(f"✅ Found '{param}': Design = {design}, Operating = {operating}")
            else:
                print(f"❌ Parameter '{param}' not found in the index.")

        return design_vals, operating_vals

    # Extract values
    pressure_design, pressure_oper = fetch_parameters(pressure_parameters)
    temp_design, temp_oper = fetch_parameters(temperature_parameters)

    return {
        "pressure_design": pressure_design,
        "pressure_operating": pressure_oper,
        "temperature_design": temp_design,
        "temperature_operating": temp_oper
    }

from iapws import IAPWS97

from iapws import IAPWS97
from pyXSteam.XSteam import XSteam
from iapws import IAPWS97
from pyXSteam.XSteam import XSteam

def calculate_turbine_efficiencies(df):
    df.columns = df.columns.str.strip()
    steam_table = XSteam(XSteam.UNIT_SYSTEM_MKS)

    def bar_to_mpa(bar_val): return round(bar_val / 10, 5) if bar_val is not None else None
    def kpa_to_mpa(kpa_val): return round(kpa_val / 1000, 5) if kpa_val is not None else None
    def compute_entropy(P_mpa, T_c): return round(IAPWS97(P=P_mpa, T=T_c + 273.15).s, 5) if P_mpa and T_c else None
    def compute_enthalpy(P_mpa, T_c): return round(IAPWS97(P=P_mpa, T=T_c + 273.15).h, 5) if P_mpa and T_c else None
    def compute_isentropic_enthalpy(P_mpa, s_in): return round(IAPWS97(P=P_mpa, s=s_in).h, 5) if P_mpa and s_in else None
    def hV_p(bar_p): return IAPWS97(P=bar_to_mpa(bar_p), x=1).h
    def hL_p(bar_p): return IAPWS97(P=bar_to_mpa(bar_p), x=0).h
    def calc_eff(h1, h2a, h2s): return round(((h1 - h2a) / (h1 - h2s))*100, 2) if None not in (h1, h2a, h2s) else None

    # Parameters needed for calculation
    param_list = [
        "MS PRESSURE AT TURBINE I/L", "MS TEMP AT TV1",
        "HRH PRESSURE", "HRH TEMP",
        "IP EXHAUST PRESSURE", "IP EXHAUST STEAM TEMP",
        "HP EXH PRESS", "CRH TEMP",
        "CONDENSOR VACUUM (DCS)", "LP TURBINE EXIT TEMP",
        "LP EXHAUST DRYNESS FRACTION"
    ]

    # Fetch design and operating values
    def fetch_parameters(param_list):
        design_vals, operating_vals = {}, {}
        for param in param_list:
            key = param.strip()
            if key in df.index:
                design_vals[param] = df.at[key, 'Values (D)']
                operating_vals[param] = df.at[key, 'VALUES (O)']
            else:
                design_vals[param] = None
                operating_vals[param] = None
        return design_vals, operating_vals

    design_vals, operating_vals = fetch_parameters(param_list)

    def compute_efficiency(vals):
        hp_p_mpa = bar_to_mpa(vals["MS PRESSURE AT TURBINE I/L"])
        hp_t_c = vals["MS TEMP AT TV1"]
        ip_p_mpa = bar_to_mpa(vals["HRH PRESSURE"])
        ip_t_c = vals["HRH TEMP"]
        lp_p_mpa = kpa_to_mpa(vals["IP EXHAUST PRESSURE"])
       
        lp_t_c = vals["IP EXHAUST STEAM TEMP"]
       
        hp_exit_p_mpa = bar_to_mpa(vals["HP EXH PRESS"])
        hp_exit_t_c = vals["CRH TEMP"]
        ip_exit_p_mpa = bar_to_mpa(vals["IP EXHAUST PRESSURE"] / 100) if vals["IP EXHAUST PRESSURE"] else None
        
        ip_exit_t_c = vals["IP EXHAUST STEAM TEMP"]
        lp_exit_p_mpa = (bar_to_mpa(vals["CONDENSOR VACUUM (DCS)"]))
        
        lp_exit_t_c = vals["LP TURBINE EXIT TEMP"]
       
        lp_x = vals["LP EXHAUST DRYNESS FRACTION"]

        # Entropies
        try:
            s_hp = steam_table.s_pt(vals["MS PRESSURE AT TURBINE I/L"], hp_t_c)
        except:
            s_hp = compute_entropy(hp_p_mpa, hp_t_c)

        s_ip = compute_entropy(ip_p_mpa, ip_t_c)
        s_lp = compute_entropy(lp_p_mpa, lp_t_c)

        # Enthalpies
        h1_hp = compute_enthalpy(hp_p_mpa, hp_t_c)
        h1_ip = compute_enthalpy(ip_p_mpa, ip_t_c)
        h1_lp = compute_enthalpy(lp_p_mpa, lp_t_c)

        h2a_hp = compute_enthalpy(hp_exit_p_mpa, hp_exit_t_c)
        h2a_ip = compute_enthalpy(ip_exit_p_mpa, ip_exit_t_c)
        h2a_lp = (
            hL_p(vals["CONDENSOR VACUUM (DCS)"]) * (100 - lp_x) / 100 +
            hV_p(vals["CONDENSOR VACUUM (DCS)"]) * lp_x / 100
        ) if lp_x is not None else None
        print(f"h2a_lp: {h2a_lp}")
        h2a_lp = round(h2a_lp, 0) 
        print(f"h2a_lp: {h2a_lp}")

        h2s_hp = compute_isentropic_enthalpy(hp_exit_p_mpa, s_hp)
        h2s_ip = compute_isentropic_enthalpy(ip_exit_p_mpa, s_ip)
        h2s_lp = compute_isentropic_enthalpy(lp_exit_p_mpa, s_lp)

        return {
            "HP_Turbine_Efficiency": calc_eff(h1_hp, h2a_hp, h2s_hp),
            "IP_Turbine_Efficiency": calc_eff(h1_ip, h2a_ip, h2s_ip),
            "LP_Turbine_Efficiency": calc_eff(h1_lp, h2a_lp, h2s_lp)
        }

    return {
        "Design": {
            "efficiencies": compute_efficiency(design_vals)
        },
        "Operating": {
            "efficiencies": compute_efficiency(operating_vals)
        }
    }

    # Calculate efficiencies
    # efficiencies = {
    #     # 'mode': mode,
    #     'HP': calc_eff(h1_hp, h2a_hp, h2s_hp),
    #     'IP': calc_eff(h1_ip, h2a_ip, h2s_ip),
    #     'LP': calc_eff(h1_lp, h2a_lp, h2s_lp),
    #     'enthalpies': {
    #         'inlet': {'HP': h1_hp, 'IP': h1_ip, 'LP': h1_lp},
    #         'exit_actual': {'HP': h2a_hp, 'IP': h2a_ip, 'LP': h2a_lp},
    #         'exit_isentropic': {'HP': h2s_hp, 'IP': h2s_ip, 'LP': h2s_lp}
    #     }
    # }
    
    # return efficiencies
# report_generator.py

# from fpdf import FPDF
# import pandas as pd
# from datetime import datetime
# from io import BytesIO
# import base64
# from PIL import Image
# import tempfile
# class ReportPDF(FPDF):
#     def header(self):
#         self.set_font("Arial", "B", 16)
#         self.set_text_color(0, 70, 140)  # Blue color
#         self.cell(0, 12, "Thermal Power Plant Report", ln=True, align="C")
#         self.ln(5)

#     def section_title(self, title):
#         self.set_font("Arial", "B", 12)
#         self.set_fill_color(240, 240, 240)
#         self.set_text_color(0, 0, 0)
#         self.cell(0, 10, title, ln=True, fill=True)
#         self.ln(2)

#     # def add_image(self, image_path):
#     #     if isinstance(image_path, str) and image_path.endswith(".html"):
#     #         print(f"Skipped HTML file: {image_path}")
#     #         return

#     #     try:
#     #         if isinstance(image_path, BytesIO):
#     #             img = Image.open(image_path)
#     #         else:
#     #             img = Image.open(image_path)

#     #         # Fill transparency
#     #         if img.mode in ('RGBA', 'LA'):
#     #             background = Image.new("RGB", img.size, (255, 255, 255))
#     #             background.paste(img, mask=img.split()[-1])
#     #             img = background
#     #         else:
#     #             img = img.convert("RGB")

#     #         # Save temp image
#     #         with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
#     #             img.save(tmp.name, format="JPEG")
#     #             self.image(tmp.name, w=180)
#     #             self.ln(10)  # 🔁 Add spacing below each image

#     #     except Exception as e:
#     #         print(f"Error adding image: {e}")
#     def add_image(self, image_path):
#         if isinstance(image_path, str) and image_path.endswith(".html"):
#             print(f"Skipped HTML file: {image_path}")
#             return

#         try:
#             if isinstance(image_path, BytesIO):
#                 img = Image.open(image_path)
#             else:
#                 img = Image.open(image_path)

#             # Fill transparency
#             if img.mode in ('RGBA', 'LA'):
#                 background = Image.new("RGB", img.size, (255, 255, 255))
#                 background.paste(img, mask=img.split()[-1])
#                 img = background
#             else:
#                 img = img.convert("RGB")

#             # Save temp image
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
#                 img.save(tmp.name, format="JPEG")

#                 # Check if space left, else add page
#                 if self.get_y() > self.h - 100:  # adjust threshold if needed
#                     self.add_page()

#                 self.image(tmp.name, w=180)
#                 self.ln(10)

#         except Exception as e:
#             print(f"Error adding image: {e}")






#     # def add_table(self, df):
#     #     self.set_font("Arial", size=9)
#     #     epw = self.w - 2 * self.l_margin  # Effective page width
#     #     col_widths = [epw / len(df.columns)] * len(df.columns)

#     #     # Header
#     #     self.set_fill_color(220, 230, 241)
#     #     self.set_text_color(0)
#     #     for i, col in enumerate(df.columns):
#     #         self.cell(col_widths[i], 8, str(col), border=1, fill=True, align='C')
#     #     self.ln()

#     #     # Rows
#     #     fill = False
#     #     for i in range(len(df)):
#     #         self.set_fill_color(245, 245, 245) if fill else self.set_fill_color(255, 255, 255)
#     #         for j, col in enumerate(df.columns):
#     #             text = str(df.iloc[i][col])
#     #             self.cell(col_widths[j], 8, text, border=1, fill=True, align="C")
#     #         self.ln()
#     #         fill = not fill
#     def add_table(self, df, title=None):
#         if title:
#             self.set_font("Arial", "B", 10)
#             self.cell(0, 10, title, ln=True)
#             self.set_font("Arial", size=9)

#         epw = self.w - 2 * self.l_margin
#         col_widths = [epw / len(df.columns)] * len(df.columns)

#         # Header
#         self.set_fill_color(220, 230, 241)
#         self.set_text_color(0)
#         for i, col in enumerate(df.columns):
#             self.cell(col_widths[i], 8, str(col), border=1, fill=True, align='C')
#         self.ln()

#         # Rows
#         fill = False
#         for i in range(len(df)):
#             if self.get_y() > self.h - 20:
#                 self.add_page()
#                 if title:
#                     self.set_font("Arial", "B", 10)
#                     self.cell(0, 10, title + " (contd.)", ln=True)
#                     self.set_font("Arial", size=9)
#                 # Re-draw header
#                 self.set_fill_color(220, 230, 241)
#                 for i, col in enumerate(df.columns):
#                     self.cell(col_widths[i], 8, str(col), border=1, fill=True, align='C')
#                 self.ln()

#             self.set_fill_color(245, 245, 245) if fill else self.set_fill_color(255, 255, 255)
#             for j, col in enumerate(df.columns):
#                 text = str(df.iloc[i][col])
#                 if len(text) > 20:
#                     text = text[:17] + "..."
#                 self.cell(col_widths[j], 8, text, border=1, fill=True, align="C")
#             self.ln()
#             fill = not fill



#     def add_summary(self, text):
#         self.set_text_color(80, 80, 80)
#         self.set_font("Arial", "I", 9)
#         self.multi_cell(0, 10, text)
#         self.ln(5)

# def generate_report(sections: list):
#     pdf = ReportPDF(orientation="L")
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()

#     for section in sections:
#         pdf.section_title(section.get("title", "Section"))
#         images = section.get("image", [])
#         if isinstance(images, list):
#             for img_path in images:
#                 pdf.add_image(img_path)
#         elif isinstance(images, str):  # fallback to single image
#             pdf.add_image(images)

#         if "summary" in section:
#             pdf.add_summary(section["summary"])
#         if "table" in section:
#             tables = section["table"]
#             if isinstance(tables, dict) and isinstance(tables.get("df"), pd.DataFrame):
#                 pdf.add_table(tables["df"], tables.get("title", "Table"))
#             elif isinstance(tables, list):
#                 for table in tables:
#                     if isinstance(table, dict) and isinstance(table.get("df"), pd.DataFrame):
#                         pdf.add_table(table["df"], table.get("title", "Table"))
#                         pdf.ln(5)


#         # if "table" in section and isinstance(section["table"], pd.DataFrame):
#         #     pdf.add_table(section["table"])

#     # Output as bytes
#     pdf_bytes = pdf.output(dest='S').encode('latin1') if isinstance(pdf.output(dest='S'), str) else pdf.output(dest='S')

#     buffer = BytesIO(pdf_bytes)
#     b64 = base64.b64encode(buffer.getvalue()).decode()
#     report_name = f"Thermal_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

#     # JavaScript trick to auto-reset Streamlit spinner state after download
#     href = f"""
#         <html>
#         <body>
#             <a href="data:application/pdf;base64,{b64}" download="{report_name}" 
#                onclick="setTimeout(() => window.parent.postMessage('streamlit:stopSpinner', '*'), 100);">
#                📥 <b>Download PDF Report</b>
#             </a>
#         </body>
#         </html>
#     """
#     return href
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import pandas as pd
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.units import inch
import tempfile
import base64


# def generate_report(sections, output_path="final_report.pdf"):
#     doc = SimpleDocTemplate(output_path, pagesize=A4,
#                             rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    
#     styles = getSampleStyleSheet()
#     story = []

#     # Title
#     title_style = styles['Heading1']
#     story.append(Paragraph("Thermal Power Plant Report", title_style))
#     story.append(Spacer(1, 12))

#     for section in sections:
#         # Section Title
#         section_title = section.get("title", "Section")
#         story.append(Paragraph(section_title, styles["Heading2"]))
#         story.append(Spacer(1, 6))

#         # Summary Text
#         if "summary" in section:
#             summary = section["summary"]
#             story.append(Paragraph(summary, styles["Normal"]))
#             story.append(Spacer(1, 10))

#         # Images
#         image_paths = section.get("image", [])
#         if isinstance(image_paths, str):
#             image_paths = [image_paths]

#         for img_path in image_paths:
#             if os.path.exists(img_path):
#                 im = Image(img_path)
#                 im._restrictSize(6 * inch, 4 * inch)
#                 story.append(im)
#                 story.append(Spacer(1, 10))

#         # Tables
#         if "table" in section:
#             table_data = section["table"]
#             if isinstance(table_data, dict):
#                 df = table_data.get("df")
#                 title = table_data.get("title", "")
#             else:
#                 df = table_data
#                 title = ""

#             if isinstance(df, pd.DataFrame):
#                 if title:
#                     story.append(Paragraph(title, styles["Heading3"]))
#                     story.append(Spacer(1, 4))

#                 data = [list(df.columns)] + df.values.tolist()
#                 table = Table(data, repeatRows=1)

#                 table_style = TableStyle([
#                     ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
#                     ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
#                     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#                     ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#                     ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
#                     ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
#                     ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
#                 ])
#                 table.setStyle(table_style)
#                 story.append(table)
#                 story.append(Spacer(1, 10))
       
        


#         story.append(PageBreak())

#     # Save PDF
#     doc.build(story)
#     return output_path
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A2
from reportlab.lib import colors
from reportlab.lib.units import inch
import os
import pandas as pd

def generate_report(sections, output_path="final_report.pdf"):
    doc = SimpleDocTemplate(output_path, pagesize=A2,
                            rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)

    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = styles['Heading1']
    story.append(Paragraph("Thermal Power Plant Report", title_style))
    story.append(Spacer(1, 12))

    for i, section in enumerate(sections):
        # Section Title
        section_title = section.get("title", "Section")
        story.append(Paragraph(section_title, styles["Heading2"]))
        story.append(Spacer(1, 6))

        # Summary Text
        summary = section.get("summary", "")
        if summary:
            story.append(Paragraph(summary, styles["Normal"]))
            story.append(Spacer(1, 10))

        # Images
        image_paths = section.get("image", [])
        if isinstance(image_paths, str):
            image_paths = [image_paths]

        for img_path in image_paths:
            if os.path.exists(img_path):
                try:
                    im = Image(img_path)
                    im._restrictSize(12 * inch, 8 * inch)
                    story.append(im)
                    story.append(Spacer(1, 10))
                except Exception as e:
                    print(f"⚠️ Failed to load image {img_path}: {e}")
            else:
                print(f"⚠️ Image not found: {img_path}")

        # Tables
        table_data = section.get("table")
        if table_data:
            # Support multiple tables
            if isinstance(table_data, list):
                tables = table_data
            else:
                tables = [table_data]

            for table_item in tables:
                df = None
                title = ""

                if isinstance(table_item, dict):
                    df = table_item.get("df")
                    title = table_item.get("title", "")
                elif isinstance(table_item, pd.DataFrame):
                    df = table_item

                if isinstance(df, pd.DataFrame):
                    if title:
                        story.append(Paragraph(title, styles["Heading3"]))
                        story.append(Spacer(1, 4))

                    data = [list(df.columns)] + df.values.tolist()
                    table = Table(data, repeatRows=1)

                    table_style = TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ])
                    table.setStyle(table_style)
                    story.append(table)
                    story.append(Spacer(1, 10))

        # Page break after section (but not after last one)
        if i < len(sections) - 1:
            story.append(PageBreak())

    # Save PDF
    doc.build(story)
    return output_path











if __name__ == "__main__":
    input_file = "enthalpyfile2.xlsx"  # Replace with your input file path
    df_input = load_input_data(input_file)
    # results = calculate_thermal_performance(df_input)
    # W = what_if_iteration_o(df_input)
    # H1 = calculated_Heater(df_input)
    # H2 = what_if_iteration(df_input)
    # conde = condencer(df_input)
    # MWFii_final, MFWfi_final, iters = what_if_iteration(df_input)
    #print(f"Final MWFii: {MWFii_final:.6f}, Final MFWfi: {MFWfi_final:.6f}, iterations: {iters}")
    # print("\n✅ Condenser Calculation Output:\n")
    # for key, value in conde.items():
    #     print(f"{key}: {value}")
    T = calculate_turbine_efficiencies(df_input)
    
    