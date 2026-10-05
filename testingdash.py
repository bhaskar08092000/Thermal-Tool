import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
#report
from fpdf import FPDF
import matplotlib.pyplot as plt
from PIL import Image
import plotly.io as pio
import os

#normal
try:
    from streamlit_echarts import st_echarts as _st_echarts  # type: ignore
    st_echarts = _st_echarts
except ImportError:
    st.error("streamlit-echarts not installed. Run: pip install streamlit-echarts")
    def st_echarts(*args, **kwargs): st.warning("streamlit-echarts not available")
from HRPTC6 import condencer
from Boiler  import boiler_efficiency_calculation,load_extended_plant_data,calculate_aph_parameters

st.set_page_config(page_title="Thermal Power Dashboard", layout="wide")

# --- Initialize session states ---
if 'boiler_df' not in st.session_state:
    st.session_state['boiler_df'] = None
if 'turbine_df' not in st.session_state:
    st.session_state['turbine_df'] = None
if 'page' not in st.session_state:
    st.session_state['page'] = "Dashboard"

# --- Sidebar: Upload files ---
with st.sidebar:
    with st.expander("📂 Upload Input Files", expanded=True):
        boiler_file = st.file_uploader("Boiler", type=["xlsx", "csv"], label_visibility="collapsed")
        turbine_file = st.file_uploader("Turbine", type=["xlsx", "csv"], label_visibility="collapsed")

    # Optional: show filenames as confirmation
    if boiler_file is not None:
        st.caption(f"✔️ Boiler File: `{boiler_file.name}`")
        boiler_df = pd.read_excel(boiler_file) if boiler_file.name.endswith("xlsx") else pd.read_csv(boiler_file)
        st.session_state['boiler_df'] = boiler_df
        output = boiler_efficiency_calculation(boiler_df)
        Airpreheater = calculate_aph_parameters(boiler_df)
        st.session_state['Airpreheater'] = dict(Airpreheater) if Airpreheater else {}  # type: ignore

        
        st.session_state['boiler_output'] = output


    if turbine_file is not None and "condenser_result" not in st.session_state:
        st.caption(f"✔️ Turbine File: `{turbine_file.name}`")
        turbine_df = pd.read_excel(turbine_file) if turbine_file.name.endswith("xlsx") else pd.read_csv(turbine_file)  # type: ignore[assignment]

        if "PARAMETERS" in turbine_df.columns:
            turbine_df = turbine_df.set_index("PARAMETERS")

        st.session_state['turbine_df'] = turbine_df
       

        try:
            # ✅ Run condenser which includes all intermediate function results
            condenser_results = condencer(turbine_df)

            # Save full condenser result dictionary
            st.session_state["condenser_result"] = condenser_results

            # Extract namedtuples from condenser results
            resultW = condenser_results["resultW"]
            resultW_o = condenser_results["resultW_o"]

            # Safely store design and operating results using named attributes
            st.session_state["design_result"] = {
                "MFWii": resultW.MFWii,
                "MFWfi": resultW.MFWfi,
                "max_iter": resultW.max_iter,
                "HR": resultW.HR,
                "Ms": resultW.Ms,
                "Hms": resultW.Hms,
            }

            st.session_state["oper_result"] = {
                "MFWii": resultW_o.MFWii_o,
                "MFWfi": resultW_o.MFWfi_o,
                "max_iter": resultW_o.iteration,
                "HR": resultW_o.HR_o,
                "Ms": resultW_o.Ms_o,
                "Hms": resultW_o.Hms_o,
            }

            st.rerun()

        except Exception as e:
            st.error(f"Error in calculation: {e}")
    
# --- Main Page Routing ---
if st.session_state['page'] == "Dashboard":
    st.title("🌡️ Thermal Power Dashboard")

    # # Summary cards
    col1, col2, col3 = st.columns(3)
  
    HR = round(float(st.session_state.get("design_result", {}).get("HR") or 0), 1)
    # HR = round(({"HR": __import__("random").uniform(2000, 3000)}).get("HR", 0), 1)
    


    # import streamlit as st, time, random; placeholder = st.empty(); [placeholder.metric("HR", f"{round(random.uniform(2000, 3000),1)} kJ/kWh") or time.sleep(3) for _ in iter(int, 1)]
    HR_o = round(float(st.session_state.get("oper_result", {}).get("HR") or 0), 1)

    def generate_echart_gauge(title, value, min_val, max_val, unit):
        return {
            "series": [
                {
                    "type": "gauge",
                    "startAngle": 225,
                    "endAngle": -45,
                    "min": min_val,
                    "max": max_val,
                    "splitNumber": 4,
                    "progress": {"show": True, "width": 18},
                    "axisLine": {"lineStyle": {"width": 18}},
                    "axisTick": {"show": False},
                    "splitLine": {
                        "length": 10,
                        "lineStyle": {"width": 2, "color": "#999"}
                    },
                    "axisLabel": {
                        "distance": 20,
                        "color": "#666",
                        "fontSize": 11,
                        # 👇 Use JS formatter as string
                        "formatter": "{value}"
                    },
                    "pointer": {"icon": "circle", "width": 6, "length": "70%"},
                    "detail": {
                        "valueAnimation": True,
                        "fontSize": 16,
                        "offsetCenter": [0, "80%"],
                        "formatter": f"{value} {unit}",  # value display inside dial
                        "color": "#222"
                    },
                    "data": [{"value": value, "name": title}]
                }
            ]
        }

 
    def generate_dual_gauge_o(value1, value2, min_val, max_val, unit, name1="DHR", name2="OHR"):
        return {
            "series": [
                {
                    "name": name1,
                    "type": "gauge",
                    "min": min_val,
                    "max": max_val,
                    "radius": "95%",
                    "center": ["50%", "45%"],
                    "axisLine": {
                        "lineStyle": {
                            "width": 15,
                            "color": [[1, "#e0e0e0ff"]]  # base gray ring
                        }
                    },
                    "progress": {
                        "show": True,
                        "width": 15,
                        "roundCap": True,
                        "itemStyle": {
                            "color": "#5470C6"  # Blue arc
                        }
                    },
                    "pointer": {
                        "width": 5,
                        "itemStyle": {
                            "color": "#5470C6"  # Blue needle
                        }
                    },
                    "detail": {"show": False},
                    "title": {"show": False},
                    "data": [{"value": value1}]
                },
                {
                    "name": name2,
                    "type": "gauge",
                    "min": min_val,
                    "max": max_val,
                    "radius": "95%",
                    "center": ["50%", "45%"],
                    "axisLine": {
                        "lineStyle": {
                            "width": 15,
                            "color": [[1, "transparent"]]  # transparent base
                        }
                    },
                    "progress": {
                        "show": True,
                        "width": 7,
                        "roundCap": True,
                        "itemStyle": {
                            "color": "#EE6666"  # Red arc
                        }
                    },
                    "pointer": {
                        "width": 3,
                        "itemStyle": {
                            "color": "#EE6666"  # Red needle
                        }
                    },
                    "detail": {"show": False},
                    "title": {"show": False},
                    "data": [{"value": value2}]
                }
            ],
            "graphic": [
                {
                    "type": "text",
                    "left": "center",
                    "top": "82%",
                    "style": {
                        "text": f"🔵 {name1}: {value1:.2f} {unit}",
                        "font": "bold 15px sans-serif",
                        "fill": "#5470C6"
                    }
                },
                {
                    "type": "text",
                    "left": "center",
                    "top": "90%",
                    "style": {
                        "text": f"🔴 {name2}: {value2:.2f} {unit}",
                        "font": "bold 15px sans-serif",
                        "fill": "#EE6666"
                    }
                }
            ]
        }



    col1, col2, col3,col4 = st.columns(4)
    
   
    output: dict = st.session_state.get("boiler_output") or {}
    boiler_eff_dict: dict = output.get("Boiler_efficiency") or {}

    
    boiler_eff_d = round(float(boiler_eff_dict.get("Design", 0)), 1)
    boiler_eff_o = round(float(boiler_eff_dict.get("Operating", 0)), 1)
    # boiler_eff_o = 95


    GHR_D =round( HR/ boiler_eff_d*100,2)
    GHR_o = round(HR_o / boiler_eff_o*100,2)
       
   


    # print(f"Boiler Efficiency Design: {boiler_eff_d}, Operating: {boiler_eff_o}")

    # with col1:
    #  st_echarts(options=generate_echart_gauge("DHR", HR, 0, 5000, "kcal/kWh"), height="250px")
    


    # with col2:
    #     st_echarts(options=generate_echart_gauge("OHR", HR_o, 0, 5000, "kcal/kWh"), height="250px")
    #     # st.plotly_chart(create_angular_gauge("TGCHR", HR_o, 2000, 15000, "kcal/kWh"), use_container_width=True)
    with col1:
    #     st_echarts(
    #     options=generate_dual_gauge_o("Heat Rate Comparison", HR, HR_o, 0, 5000, "kcal/kWh"),
    #     height="300px"
    # )  
      st_echarts(
        options=generate_dual_gauge_o(
            value1=GHR_o,
            value2=GHR_D,
            min_val=200,
            max_val=3000,
            unit="kcal/kWh",
            name1="O_GHR",
            name2="D_GHR"
        ),
        height="300px"
      )

       
    with col2:
    #     st_echarts(
    #     options=generate_dual_gauge_o("Gross Heat Rate Comparison", GHR_D, GHR_o, 0, 500, "kcal/kWh"),
    #     height="300px"
    # )
        st_echarts(
            options=generate_dual_gauge_o(
                value1=HR_o,
                value2=HR,
                min_val=1500,
                max_val=3000,
                unit="kcal/kWh",
                name1="O_TGHR",
                name2="D_TGHR"
            ),
            height="300px"
        )
         
        

    with col3:
        st_echarts(
            options=generate_dual_gauge_o(
                value1=boiler_eff_o,
                value2=boiler_eff_d,
                min_val=0,
                max_val=100,
                unit="%",
                name1="Boiler Eff O",
                name2="Boiler Eff D"
            ),
            height="300px"
        )

    # with col3:
    #     st_echarts(options=generate_echart_gauge("Boiler Efficiency D",boiler_eff_d,  0, 100, "%"), height="250px")
    # with col4:
    #     st_echarts(options=generate_echart_gauge("Boiler Efficiency O",boiler_eff_o,  0, 100, "%"), height="250px")
     

    st.divider()
    st.subheader("📊 Select Module")

    # First row of buttons
    col1, col2 = st.columns(2)
    if col1.button("🔥 Boiler Losses"):
        st.session_state['page'] = "Boiler Losses"
        st.rerun()

    if col2.button("⚙️ Turbine Pr. Survey"):
        st.session_state['page'] = "Turbine Pr. Survey"
        st.rerun()

    # Second row of buttons
    col3, col4 = st.columns(2)
    if col3.button("📈 Heat Rate Deviation"):
        st.session_state['page'] = "Heat Rate Deviation"
        st.rerun()

    if col4.button("STM Pressure Profile"):
        st.session_state['page'] = "STM Pressure Profile"
        st.rerun()

    # Third row of buttons
    col5, col6 = st.columns(2)
    if col5.button("📉 Turbine Efficiency"):
        st.session_state['page'] = "Turbine Efficiency"
        st.rerun()

    if col6.button("🌬️ APH Performance"):
        st.session_state['page'] = "APH Performance"
        st.rerun()

    # Fourth row (single button if needed)
    col7, col18 = st.columns(2)
    if col7.button("💧 Condenser"):
        st.session_state['page'] = "Condenser"
        st.rerun()
    if col18.button("🔥 Heaters"):
        st.session_state['page'] = "Heaters"
        st.rerun()



# --- Boiler Losses ---
elif st.session_state['page'] == "Boiler Losses":
    st.header("🔥 Boiler Losses Analysis")
    if st.button("⬅️ Back to Dashboard"):
        st.session_state['page'] = "Dashboard"
        st.rerun()

    output: dict = st.session_state.get("boiler_output") or {}

    # 🧾 Prepare table rows
    boiler_loss_data = {
        "Loss Type": [
            "Dry Flue Gas Loss",
            "Carbon Loss",
            "Moisture Fuel",
            "Hydrogen Fuel",
            "Moisture Air",
            "Radiation Loss",
            "Total Loss",
            "Boiler Efficiency",
            "Unburnt C in Ash"
        ],
        "Design (%)":[
            round(output.get("Dry_flue_gas_loss", {}).get("Design", 0), 2),
            round(output.get("Carbon_loss", {}).get("Design", 0), 2),
            round(output.get("Moisture_fuel_loss", {}).get("Design", 0), 2),
            round(output.get("Hydrogen_fuel_loss", {}).get("Design", 0), 2),
            round(output.get("Moisture_air_loss", {}).get("Design", 0), 2),
            round(output.get("Radiation_loss", {}).get("Design", 0), 2),
            round(output.get("Total_loss", {}).get("Design", 0), 2),
            round(output.get("Boiler_efficiency", {}).get("Design", 0), 3),
            round(output.get("Unburnt_C_in_ash", {}).get("Design", 0), 2)
        ],
        "Operating (%)": [
            round(output.get("Dry_flue_gas_loss", {}).get("Operating", 0), 2),
            round(output.get("Carbon_loss", {}).get("Operating", 0), 2),
            round(output.get("Moisture_fuel_loss", {}).get("Operating", 0), 2),
            round(output.get("Hydrogen_fuel_loss", {}).get("Operating", 0), 2),
            round(output.get("Moisture_air_loss", {}).get("Operating", 0), 2),
            round(output.get("Radiation_loss", {}).get("Operating", 0), 2),
            round(output.get("Total_loss", {}).get("Operating", 0), 2),
            round(output.get("Boiler_efficiency", {}).get("Operating", 0), 3),
            round(output.get("Unburnt_C_in_ash", {}).get("Operating", 0), 2)
        ]
    }

    # 📊 Create DataFrame
    loss_df = pd.DataFrame(boiler_loss_data)
    #table report
    st.session_state["boiler_df"] = loss_df

    

    # 🖼️ Display nicely
    # st.markdown("### 🔥 Boiler Losses & Efficiency Table")
    # st.table(loss_df)
    st.dataframe(loss_df, use_container_width=True)

    #saving table as image
     # Save table to PNG
    # fig_table, ax = plt.subplots()
    # ax.axis('off')
    # table_img = ax.table(cellText=loss_df.values,
    #                      colLabels=loss_df.columns,
    #                      cellLoc='center',
    #                      loc='center')
    # table_path = os.path.join(report_dir, "boiler_losses_table.png")
    # fig_table.savefig(table_path, bbox_inches='tight')
    # plt.close(fig_table)

  

    # 🔍 List of loss keys (excluding efficiency)
    loss_keys = [
        "Dry_flue_gas_loss",
        "Carbon_loss",
        "Moisture_fuel_loss",
        "Hydrogen_fuel_loss",
        "Moisture_air_loss",
        "Radiation_loss","Unburnt_C_in_ash",
    ]
    # 📊 Prepare pie chart data for Design and Operating
    def get_pie_data(condition):
        labels = []
        values = []
        for key in loss_keys:
            value = output.get(key, {}).get(condition, 0)
            if value:
                labels.append(key)
                values.append(round(float(value), 2))
        return labels, values

    # 📊 Create pie charts
    col1, col2 = st.columns(2)

    with col1:
        labels_d, values_d = get_pie_data("Design")
        if labels_d:
            fig_d = px.pie(
                names=labels_d,
                values=values_d,
                title="Boiler Loss Breakdown (Design)",
                hole=0.3
            )
            fig_d.update_traces(textinfo="percent+label")
            st.plotly_chart(fig_d, use_container_width=True)
        else:
            st.warning("No loss data available for Design")

    with col2:
        labels_o, values_o = get_pie_data("Operating")
        if labels_o:
            fig_o = px.pie(
                names=labels_o,
                values=values_o,
                title="Boiler Loss Breakdown (Operating)",
                hole=0.3
            )
            fig_o.update_traces(textinfo="percent+label")
            st.plotly_chart(fig_o, use_container_width=True)
            
        else:
            st.warning("No loss data available for Operating")
    
# --- Turbine Pressure Survey ---
elif st.session_state['page'] == "Turbine Pr. Survey":
    st.header("⚙️ Turbine Pressure Survey")
    if st.button("⬅️ Back to Dashboard"):
        st.session_state['page'] = "Dashboard"
        st.rerun()

    df = st.session_state['turbine_df']
    if df is not None:
        st.dataframe(df)
        if "Turbine_Pressure" in df.columns:
            st.plotly_chart(px.line(df, x=df.columns[0], y="Turbine_Pressure", title="Turbine Pressure Over Time"))
    else:
        st.warning("Upload Turbine data file to see this section.")

# --- Heat Rate Deviation ---
elif st.session_state['page'] == "Heat Rate Deviation":
    st.header("📈 Heat Rate Deviation")
    if st.button("⬅️ Back to Dashboard"):
        st.session_state['page'] = "Dashboard"
        st.rerun()
    turbine_df = st.session_state.get('turbine_df')
    if turbine_df is not None:
        try:
            design = st.session_state.get("design_result", {})
            oper = st.session_state.get("oper_result", {})

            comparison_data = {
                "Metric": ["Feedwater flow (for intial iteration) MFWii", "Calculated Feedwater flow (MFWfi)", "Max Iterations", "Heat Rate (HR)", "Main steam flow (Ms)", "Main steam(Hms)"],
                "Design Value": [design.get("MFWii"), design.get("MFWfi"), design.get("max_iter"), design.get("HR"), design.get("Ms"), design.get("Hms")],
                "Operational Value": [oper.get("MFWii"), oper.get("MFWfi"), oper.get("max_iter"), oper.get("HR"), oper.get("Ms"), oper.get("Hms")],
                "Unit": ["kg/hr", "kg/hr", "-", "kCal/kWh", "kg/hr", "kJ/kg"]
            }


            comparison_df = pd.DataFrame(comparison_data)
            comparison_df["Design Value"] = comparison_df["Design Value"].apply(lambda x: round(x, 2))
            comparison_df["Operational Value"] = comparison_df["Operational Value"].apply(lambda x: round(x, 2))

            st.subheader("📊 Design vs Operational Heat Rate Results")
            # st.table(comparison_df)
            st.dataframe(comparison_df, use_container_width=True)
            def get_hr_pie_data(values_dict):
                labels = []
                values = []
                for metric in comparison_df["Metric"]:
                    val = values_dict.get(metric)
                    if val:
                        labels.append(metric)
                        values.append(round(val, 2))
                return labels, values

            design_dict = dict(zip(comparison_df["Metric"], comparison_df["Design Value"]))
            oper_dict = dict(zip(comparison_df["Metric"], comparison_df["Operational Value"]))

            design_labels, design_values = get_hr_pie_data(design_dict)
            oper_labels, oper_values = get_hr_pie_data(oper_dict)

            # 📊 Show side-by-side pie charts using st.columns
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 🎯 Design Values")
                fig_design = go.Figure(data=[go.Pie(
                    labels=design_labels,
                    values=design_values,
                    hole=0.3,
                    textinfo='percent+label',
                    hovertemplate='%{label}: %{value}<extra></extra>',
                    marker=dict(colors=px.colors.qualitative.Set2)
                )])
                st.plotly_chart(fig_design, use_container_width=True)

            with col2:
                st.markdown("### ⚙️ Operational Values")
                fig_oper = go.Figure(data=[go.Pie(
                    labels=oper_labels,
                    values=oper_values,
                    hole=0.3,
                    textinfo='percent+label',
                    hovertemplate='%{label}: %{value}<extra></extra>',
                    marker=dict(colors=px.colors.qualitative.Set2)
                )])
                st.plotly_chart(fig_oper, use_container_width=True)



        except Exception as e:
            st.error(f"❌ Error in calculating heat rate: {e}")
    else:
        st.warning("⚠️ Please upload turbine input data from the sidebar.")



# --- STM Pressure Profile ---
elif st.session_state['page'] == "STM Pressure Profile":
    st.header("STM Pressure Profile")

    if st.button("⬅️ Back to Dashboard"):
        st.session_state['page'] = "Dashboard"
        st.rerun()

    # Check if condenser_result and resultsSTM are available
    if "condenser_result" in st.session_state:
        resultsh = st.session_state["condenser_result"].get("resultsSTM", None)

        if resultsh:
            # Merge pressure values into a single DataFrame
            df_pressure = pd.DataFrame({
                "Parameter": list(resultsh['pressure_design'].keys()),
                "Design Value": list(resultsh['pressure_design'].values()),
                "Operating Value": [resultsh['pressure_operating'].get(k, "") for k in resultsh['pressure_design'].keys()]
            })

            # Merge temperature values into a single DataFrame
            df_temperature = pd.DataFrame({
                "Parameter": list(resultsh['temperature_design'].keys()),
                "Design Value": list(resultsh['temperature_design'].values()),
                "Operating Value": [resultsh['temperature_operating'].get(k, "") for k in resultsh['temperature_design'].keys()]
            })

            # Show both tables
            st.subheader("Pressure Profile (Design vs Operating)")
            st.dataframe(df_pressure, use_container_width=True)

            st.subheader("Temperature Profile (Design vs Operating)")
            st.dataframe(df_temperature, use_container_width=True)

        else:
            st.warning("resultsSTM not found in condenser_result.")
        # Plot Pressure Graph
        st.subheader("Pressure Profile ")

        fig_pressure = go.Figure()

        fig_pressure.add_trace(go.Scatter(
            x=list(resultsh['pressure_design'].keys()),
            y=list(resultsh['pressure_design'].values()),
            mode='lines+markers',
            name='Design Pressure',
            line=dict(color='steelblue', width=2),
            marker=dict(symbol='circle')
        ))

        fig_pressure.add_trace(go.Scatter(
            x=list(resultsh['pressure_operating'].keys()),
            y=list(resultsh['pressure_operating'].values()),
            mode='lines+markers',
            name='Operating Pressure',
            line=dict(color='firebrick', width=2),
            marker=dict(symbol='diamond')
        ))

        fig_pressure.update_layout(
            xaxis_title='Pressure Parameters',
            yaxis_title='Pressure (kg/cm² or as applicable)',
            height=450,
            margin=dict(l=20, r=20, t=40, b=80),
            xaxis_tickangle=45,
            legend=dict(x=0, y=1.1, orientation="h")
        )

        st.plotly_chart(fig_pressure, use_container_width=True)
        # Line Graph for Temperature
        st.subheader("Temperature Profile ")

        fig_temp = go.Figure()

        fig_temp.add_trace(go.Scatter(
            x=list(resultsh['temperature_design'].keys()),
            y=list(resultsh['temperature_design'].values()),
            mode='lines+markers',
            name='Design Temperature',
            line=dict(color='royalblue', width=2),
            marker=dict(symbol='circle')
        ))

        fig_temp.add_trace(go.Scatter(
            x=list(resultsh['temperature_operating'].keys()),
            y=list(resultsh['temperature_operating'].values()),
            mode='lines+markers',
            name='Operating Temperature',
            line=dict(color='indianred', width=2),
            marker=dict(symbol='diamond')
        ))

        fig_temp.update_layout(
            xaxis_title='Temperature Parameters',
            yaxis_title='Temperature (°C)',
            height=450,
            margin=dict(l=20, r=20, t=40, b=80),
            xaxis_tickangle=45,
            legend=dict(x=0, y=1.1, orientation="h")
        )

        st.plotly_chart(fig_temp, use_container_width=True)
    else:
        st.warning("Condenser data not loaded yet.")


elif st.session_state['page'] == "Turbine Efficiency":
    st.header("📉 Turbine Efficiency")
    if st.button("⬅️ Back to Dashboard"):
        st.session_state['page'] = "Dashboard"
        st.rerun()
    if "condenser_result" in st.session_state:
        results_te = st.session_state["condenser_result"].get("resultsTE", None)
        if results_te:
            # Extract only efficiencies
            design_eff = results_te["Design"]["efficiencies"]
            operating_eff = results_te["Operating"]["efficiencies"]

            # Format as DataFrame
            import pandas as pd
            eff_df = pd.DataFrame({
                "Design Efficiency": design_eff,
                "Operating Efficiency": operating_eff
            })

            # Show the table
            st.subheader("🧮 Turbine Efficiencies (Design vs Operating)")
            st.table(eff_df)

            # Convert efficiency keys into labels
            # Extract efficiency labels and values
            eff_labels = list(eff_df.index)
            design_values = eff_df["Design Efficiency"].tolist()
            oper_values = eff_df["Operating Efficiency"].tolist()

            # Create grouped bar chart
            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=eff_labels,
                y=design_values,
                name='Design',
                marker_color='steelblue',
                text=design_values,
                textposition='outside'
            ))

            fig.add_trace(go.Bar(
                x=eff_labels,
                y=oper_values,
                name='Operating',
                marker_color='red',
                text=oper_values,
                textposition='outside'
            ))

            fig.update_layout(
                title="Turbine Efficiencies: Design vs Operating",
                xaxis_title="Turbine Section",
                yaxis_title="Efficiency (%)",
                barmode='group',
                bargap=0.25,
                height=450,
                width=800,
                legend=dict(orientation="h", y=1.05, x=0.5, xanchor="center"),
                margin=dict(t=60, l=40, r=40, b=40)
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("⚠️ Turbine efficiency results not found.")
    else:
        st.warning("⚠️ No condenser result data available.")
elif st.session_state['page'] == "APH Performance":
    st.header("🌬️ Air Pre-heater Performance")
    if st.button("⬅️ Back to Dashboard"):
        st.session_state['page'] = "Dashboard"
        st.rerun()
    st.subheader("📊 APH Performance Parameters Table")
    aph_data = {
        "Parameter": [],
        "Design": [],
        "Actual": []
    }

    Airpreheater = st.session_state.get('Airpreheater', {})
    for param, values in Airpreheater.items():
        aph_data["Parameter"].append(param)
        aph_data["Design"].append(round(values.get("Design", 0), 2))
        aph_data["Actual"].append(round(values.get("Actual", 0), 2))

    aph_df = pd.DataFrame(aph_data)
    st.dataframe(aph_df, use_container_width=True)
    
    # Display APH analysis from boiler_df
      # 🎨 Use Qualitative Color Palette (distinct colors)
    color_palette = px.colors.qualitative.Plotly  # or 'Dark24', 'Set3', 'Pastel', etc.

    # 🔵 Pie Chart: Design
    col1, col2 = st.columns(2)

    with col1:
        # st.subheader("🎯 Design Pie Chart")
        fig_design = px.pie(
            aph_df,
            names="Parameter",
            values="Design",
            title="Design APH Parameters",
            color_discrete_sequence=color_palette
        )
        
        st.plotly_chart(fig_design, use_container_width=True)

    # 🔴 Pie Chart: Actual
    with col2:
        # st.subheader("✅ Actual Pie Chart")
        fig_actual = px.pie(
            aph_df,
            names="Parameter",
            values="Actual",
            title="Actual APH Parameters",
            color_discrete_sequence=color_palette
        )
        
        st.plotly_chart(fig_actual, use_container_width=True)




elif st.session_state['page'] == "Condenser":
    st.header("💧 Condenser Performance")

    if st.button("⬅️ Back to Dashboard"):
        st.session_state['page'] = "Dashboard"
        st.rerun()

    # Check if condenser results exist
    if "condenser_result" in st.session_state:
        data = st.session_state["condenser_result"]

        # Define data for the table
        condenser_metrics = [
            ("Condenser DP of tube side", "kPa(a)", round(data["Condenser_DP_of_tube_side"], 2), round(data["Condenser_DP_of_tube_side_o"], 2)),
            ("Condenser Effectiveness", "%", round(data["Condenser_Effectiveness"], 2), round(data["Condenser_Effectiveness_o"], 2)),
            ("TTD", "°C", round(data["TTD"], 2), round(data["TTD_o"], 2)),
            ("Condenser heat load steam side", "MJ/h", round(data["Condenser_heat_load_steam_side"], 2), round(data["Condenser_heat_load_steam_side_o"], 2)),
            ("Cooling water flow", "TPH", round(data["Cooling_water_flow"], 2), round(data["Cooling_water_flow_o"], 2)),
            ("LMTD", "°C", round(data["LMTD"], 2), round(data["LMTD_o"], 2)),
            ("Subcooling temperature", "°C", round(data["Subcooling_temperature"], 2), round(data["Subcooling_temperature_o"], 2)),
        ]

        # Create a dataframe for display
        import pandas as pd
        df_condenser = pd.DataFrame(condenser_metrics, columns=["Parameter", "Unit", "Design", "Operating"])

        st.subheader("📊 Condenser Parameters")
        # st.table(df_condenser)
        st.dataframe(df_condenser, use_container_width=True)

        # 🔁 Prepare dicts for Design and Operating values
        condenser_metrics_list = df_condenser["Parameter"].tolist()
        design_values_dict = dict(zip(df_condenser["Parameter"], df_condenser["Design"]))
        operating_values_dict = dict(zip(df_condenser["Parameter"], df_condenser["Operating"]))

        # 🧠 Extract labels and values for pie chart
        def get_condenser_pie_data(values_dict):
            labels = []
            values = []
            for param in condenser_metrics_list:
                val = values_dict.get(param)
                if val and val != 0:
                    labels.append(param)
                    values.append(round(val, 2))
            return labels, values

        design_labels, design_values = get_condenser_pie_data(design_values_dict)
        oper_labels, oper_values = get_condenser_pie_data(operating_values_dict)

        # 📊 Side-by-side pie charts
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🎯 Design Values")
            fig_design = go.Figure(data=[go.Pie(
                labels=design_labels,
                values=design_values,
                hole=0.3,
                textinfo='percent+label',
                hovertemplate='%{label}: %{value}<extra></extra>',
                marker=dict(colors=px.colors.qualitative.Set3)
            )])
            st.plotly_chart(fig_design, use_container_width=True)

        with col2:
            st.markdown("### ⚙️ Operating Values")
            fig_oper = go.Figure(data=[go.Pie(
                labels=oper_labels,
                values=oper_values,
                hole=0.3,
                textinfo='percent+label',
                hovertemplate='%{label}: %{value}<extra></extra>',
                marker=dict(colors=px.colors.qualitative.Set3)
            )])
            st.plotly_chart(fig_oper, use_container_width=True)

    # else:
    #     st.warning("Condenser results not available. Please upload a file from the dashboard.")
elif st.session_state['page'] == "Heaters":
    st.header("🔥 Heater Performance")
    if st.button("⬅️ Back to Dashboard"):
        st.session_state['page'] = "Dashboard"
        st.rerun()

    if "condenser_result" in st.session_state:
        resultsh = st.session_state["condenser_result"]["resultsh"]

        import pandas as pd

        def safe(val):  # To avoid NoneType in round()
            return round(val, 2) if val is not None else "-"

        # Table rows — each is a parameter with design/operating for each heater
        rows = [
            ["Saturation Temp of extraction steam", "°C",
            safe(resultsh.Saturation_Temp_of_extraction_steamHPH8), safe(resultsh.Saturation_Temp_of_extraction_steamHPH8_o),
            safe(resultsh.Saturation_Temp_of_extraction_steamHPH7), safe(resultsh.Saturation_Temp_of_extraction_steamHPH7_o),
            safe(resultsh.Saturation_Temp_of_extraction_steamHPH6), safe(resultsh.Saturation_Temp_of_extraction_steamHPH6_o),
            safe(resultsh.Saturation_Temp_of_extraction_steamHPH5), safe(resultsh.Saturation_Temp_of_extraction_steamHPH5_o),
            safe(resultsh.Saturation_Temp_of_extraction_steamLPH4), safe(resultsh.Saturation_Temp_of_extraction_steamLPH4_o),
            safe(resultsh.Saturation_Temp_of_extraction_steamLPH3), safe(resultsh.Saturation_Temp_of_extraction_steamLPH3_o),
            safe(resultsh.Saturation_Temp_of_extraction_steamLPH2), safe(resultsh.Saturation_Temp_of_extraction_steamLPH2_o),
            safe(resultsh.Saturation_Temp_of_extraction_steamLPH1), safe(resultsh.Saturation_Temp_of_extraction_steamLPH1_o),
            safe(resultsh.Saturation_Temp_of_extraction_steamGSC), safe(resultsh.Saturation_Temp_of_extraction_steamGSC_o)],
            
            ["Feed water Temp. Rise (TR)", "°C",
            safe(resultsh.Feed_water_Temp_RiseHPH8), safe(resultsh.Feed_water_Temp_RiseHPH8_o),
            safe(resultsh.Feed_water_Temp_RiseHPH7), safe(resultsh.Feed_water_Temp_RiseHPH7_o),
            safe(resultsh.Feed_water_Temp_RiseHPH6), safe(resultsh.Feed_water_Temp_RiseHPH6_o),
            safe(resultsh.Feed_water_Temp_RiseHPH5), safe(resultsh.Feed_water_Temp_RiseHPH5_o),
            safe(resultsh.Feed_water_Temp_RiseLPH4), safe(resultsh.Feed_water_Temp_RiseLPH4_o),
            safe(resultsh.Feed_water_Temp_RiseLPH3), safe(resultsh.Feed_water_Temp_RiseLPH3_o),
            safe(resultsh.Feed_water_Temp_RiseLPH2), safe(resultsh.Feed_water_Temp_RiseLPH2_o),
            safe(resultsh.Feed_water_Temp_RiseLPH1), safe(resultsh.Feed_water_Temp_RiseLPH1),
            safe(resultsh.Feed_water_Temp_RiseGSC), safe(resultsh.Feed_water_Temp_RiseGSC_o)],
            
            ["TTD (Terminal Temp Diff)", "°C",
            safe(resultsh.Terminal_Temp_DiffHPH8), safe(resultsh.Terminal_Temp_DiffHPH8_o),
            safe(resultsh.Terminal_Temp_DiffHPH7), safe(resultsh.Terminal_Temp_DiffHPH7_o),
            safe(resultsh.Terminal_Temp_DiffHPH6), safe(resultsh.Terminal_Temp_DiffHPH6_o),
            safe(resultsh.Terminal_Temp_DiffHPH5), safe(resultsh.Terminal_Temp_DiffHPH5_o),
            safe(resultsh.Terminal_Temp_DiffLPH4), safe(resultsh.Terminal_Temp_DiffLPH4_o),
            safe(resultsh.Terminal_Temp_DiffLPH3), safe(resultsh.Terminal_Temp_DiffLPH3_o),
            safe(resultsh.Terminal_Temp_DiffLPH2), safe(resultsh.Terminal_Temp_DiffLPH2_o),
            safe(resultsh.Terminal_Temp_DiffLPH1), safe(resultsh.Terminal_Temp_DiffLPH1_o),
            safe(resultsh.Terminal_Temp_DiffGSC), safe(resultsh.Terminal_Temp_DiffGSC_o)],
            
            ["Drain Cooler Approach (DCA)", "°C",
            safe(resultsh.Drain_Cooler_Approach_TempHPH8), safe(resultsh.Drain_Cooler_Approach_TempHPH8_o),
            safe(resultsh.Drain_Cooler_Approach_TempHPH7), safe(resultsh.Drain_Cooler_Approach_TempHPH7_o),
            safe(resultsh.Drain_Cooler_Approach_TempHPH6), safe(resultsh.Drain_Cooler_Approach_TempHPH6_o),
            # safe(DR_DCA = 0), safe(DR_DCA_o = 0),
            safe(resultsh.Drain_Cooler_Approach_TempLPH4), safe(resultsh.Drain_Cooler_Approach_TempLPH4_o),
            safe(resultsh.Drain_Cooler_Approach_TempLPH3), safe(resultsh.Drain_Cooler_Approach_TempLPH3_o),
            safe(resultsh.Drain_Cooler_Approach_TempLPH2), safe(resultsh.Drain_Cooler_Approach_TempLPH2),
            safe(resultsh.Drain_Cooler_Approach_TempLPH1), safe(resultsh.Drain_Cooler_Approach_TempLPH1),
            safe(resultsh.Drain_Cooler_Approach_TempGSC), safe(resultsh.Drain_Cooler_Approach_TempGSC_o)],
            
            ["Extraction Steam Flow", "TPH",
            safe(resultsh.Extraction_steam_flowHPH8), safe(resultsh.Extraction_steam_flowHPH8_o),
            safe(resultsh.Extraction_steam_flowHPH7), safe(resultsh.Extraction_steam_flowHPH7_o),
            safe(resultsh.Extraction_steam_flowHPH6), safe(resultsh.Extraction_steam_flowHPH6_o),
            safe(resultsh.Extraction_steam_flowHPH5), safe(resultsh.Extraction_steam_flowHPH5_o),
            safe(resultsh.MHPH4EXT), safe(resultsh.MHPH4EXT_o),
            safe(resultsh.MHPH3EXT), safe(resultsh.MHPH3EXT_o),
            safe(resultsh.MHPH2EXT), safe(resultsh.MHPH2EXT_o),
            safe(resultsh.MHPH1EXT), safe(resultsh.MHPH1EXT_o),
            safe(resultsh.Extraction_steam_flowGSC), safe(resultsh.Extraction_steam_flowGSC_o)],
        ]

        # Column headers
        columns = [
            "Description", "Unit",
            "HPH-8 D", "HPH-8 O",
            "HPH-7 D", "HPH-7 O",
            "HPH-6 D", "HPH-6 O",
            "Deaerator D", "Deaerator O",
            "LPH-4 D", "LPH-4 O",
            "LPH-3 D", "LPH-3 O",
            "LPH-2 D", "LPH-2 O",
            "LPH-1 D", "LPH-1 O",
            "GSC D", "GSC O",
        ]

        df_heaters = pd.DataFrame(rows, columns=columns)
        st.subheader("🌡️ Heater Performance Table")
        st.dataframe(df_heaters, use_container_width=True)


        # Heater names (used as x-axis categories)
        heaters = ["HPH-8", "HPH-7", "HPH-6", "Deaerator", "LPH-4", "LPH-3", "LPH-2", "LPH-1", "GSC"]

        # Utility function to extract values from your rows
        def get_row_data(label):
            for row in rows:
                if row[0] == label:
                    design = row[2::2]  # every second column starting from 2 (design values)
                    operating = row[3::2]  # every second column starting from 3 (operating values)
                    return design, operating
            return [], []

        def plot_param_vs_heaters(param_name, unit, chart_title):
            design, operating = get_row_data(param_name)

            fig = go.Figure()
            fig.add_trace(go.Bar(x=heaters, y=design, name="Design", marker_color="steelblue"))
            fig.add_trace(go.Bar(x=heaters, y=operating, name="Operating", marker_color="indianred"))

            fig.update_layout(
                title=chart_title,
                xaxis_title="Heaters",
                yaxis_title=f"{param_name} ({unit})",
                barmode="group",
                height=400,
                template="plotly_white",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)

        # 🔽 Plot each parameter
        plot_param_vs_heaters("Extraction Steam Flow", "TPH", "Extraction Steam Flow vs Heaters")
        plot_param_vs_heaters("Drain Cooler Approach (DCA)", "°C", "DCA vs Heaters")
        plot_param_vs_heaters("TTD (Terminal Temp Diff)", "°C", "TTD vs Heaters")
        plot_param_vs_heaters("Feed water Temp. Rise (TR)", "°C", "Feed Water Temp Rise vs Heaters")


    else:
        st.warning("Heater data not found. Please upload the turbine file first.")

# def meter_with_bottom_labels(title, value, color="#F4F00DFF", unit="%"):
#     option = {
#         "title": {
#             "text": title,
#             "left": "center",
#             "top": "5%",
#             "textStyle": {
#                 "fontSize": 22,
#                 "fontWeight": "bold"
#             }
#         },
#         "series": [
#             {
#                 "type": "gauge",
#                 "startAngle": 180,
#                 "endAngle": 0,
#                 "min": 0,
#                 "max": 100,
#                 "splitNumber": 5,
#                 "radius": "100%",
#                 "center": ["50%", "75%"],  # lower the gauge to show labels below
#                 "axisLine": {
#                     "lineStyle": {
#                         "width": 30,
#                         "color": [[1, "#eee"]]
#                     }
#                 },
#                 "progress": {
#                     "show": True,
#                     "width": 30,
#                     "roundCap": True,
#                     "itemStyle": {"color": color}
#                 },
#                 "pointer": {
#                     "show": True,
#                     "length": "65%",
#                     "width": 6,
#                     "itemStyle": {"color": "#000"}
#                 },
#                 "axisTick": {
#                     "show": True,
#                     "distance": 20,
#                     "length": 8,
#                     "lineStyle": {"color": "#999", "width": 1}
#                 },
#                 "splitLine": {
#                     "show": True,
#                     "distance": 25,
#                     "length": 15,
#                     "lineStyle": {"color": "#999", "width": 2}
#                 },
#                 "axisLabel": {
#                     "show": True,
#                     "distance": 30,  # ➡️ positive = below the arc
#                     "color": "#333",
#                     "fontSize": 12
#                 },
#                 "anchor": {
#                     "show": True,
#                     "showAbove": True,
#                     "size": 10,
#                     "itemStyle": {"color": "#000"}
#                 },
#                 "detail": {
#                     "formatter": f"{value}{unit}",
#                     "fontSize": 28,
#                     "fontWeight": "bold",
#                     "offsetCenter": [0, "-30%"]
#                 },
#                 "data": [{"value": value}]
#             }
#         ]
#     }
#     return option

# # Example usage
# st_echarts(
#     options=meter_with_bottom_labels("🔥 Boiler Efficiency", 88.5),
#     height="400px"
# )
import streamlit.components.v1 as components

# import streamlit.components.v1 as components

# def dual_gauge_card(title: str, design_value: float, operating_value: float, unit: str = "%", min_val: float = 0, max_val: float = 100):
#     html_code = f"""
#     <div style="border: 1px solid #ccc; border-radius: 12px; padding: 10px; background-color: #ffffff; width: 100%;">
#         <h4 style="text-align: center; margin-bottom: 10px; font-size: 18px; color: #222;">{title}</h4>
#         <div style="display: flex; justify-content: space-evenly;">
#             <div id="{title}_design" style="width: 48%; height: 260px;"></div>
#             <div id="{title}_operating" style="width: 48%; height: 260px;"></div>
#         </div>
#     </div>

#     <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
#     <script>
#         var baseOption = {{
#             type: 'gauge',
#             startAngle: 180,
#             endAngle: 0,
#             min: {min_val},
#             max: {max_val},
#             radius: '95%',
#             axisLine: {{
#                 lineStyle: {{
#                     width: 16,
#                     color: [
#                         [0.3, '#FF6E76'],
#                         [0.7, '#FDDD60'],
#                         [1, '#58D9F9']
#                     ]
#                 }}
#             }},
#             pointer: {{
#                 show: true,
#                 width: 4,
#                 length: '60%'
#             }},
#             progress: {{
#                 show: true,
#                 width: 16
#             }},
#             axisLabel: {{
#                 fontSize: 10,
#                 distance: -35
#             }},
#             title: {{
#                 fontSize: 13,
#                 offsetCenter: [0, '-30%']
#             }},
#             detail: {{
#                 fontSize: 16,
#                 offsetCenter: [0, '60%'],
#                 formatter: '{{{{value}}}}{unit}'
#             }},
#             data: [{{value: 0, name: ''}}]
#         }};

#         var chart1 = echarts.init(document.getElementById('{title}_design'));
#         var designOption = JSON.parse(JSON.stringify({{ series: [baseOption] }}));
#         designOption.series[0].data[0].value = {design_value};
#         designOption.series[0].data[0].name = "Design";
#         chart1.setOption(designOption);

#         var chart2 = echarts.init(document.getElementById('{title}_operating'));
#         var operatingOption = JSON.parse(JSON.stringify({{ series: [baseOption] }}));
#         operatingOption.series[0].data[0].value = {operating_value};
#         operatingOption.series[0].data[0].name = "Operating";
#         chart2.setOption(operatingOption);
#     </script>
#     """
#     components.html(html_code, height=290)

# col1, col2, col3 = st.columns(3)

# with col1:
#     dual_gauge_card("Boiler Efficiency", 89.5, 87.2, "%", min_val=80, max_val=100)

# with col2:
#     dual_gauge_card("Heat Rate", 2200, 2350, "kcal/kWh", min_val=2000, max_val=2600)

# with col3:
#     dual_gauge_card("Condenser Vacuum", 580, 595, "mmHg", min_val=550, max_val=650)
# import streamlit.components.v1 as components
# import streamlit.components.v1 as components

# def dual_gauge_card(title: str, design_value: float, operating_value: float, unit: str = "%", min_val: float = 0, max_val: float = 100):
#     html_code = f"""
#     <div style="border: 1px solid #ccc; border-radius: 12px; padding: 15px; background-color: #ffffff; width: 100%;">
#         <h4 style="text-align: center; margin-bottom: 10px; font-size: 18px; color: #333;">{title}</h4>
#         <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-top: 10px;">
#             <div id="{title}_design" style="width: 48%; height: 260px;"></div>
#             <div id="{title}_operating" style="width: 48%; height: 260px;"></div>
#         </div>
#     </div>

#     <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
#     <script>
#         function createGaugeConfig(value, name, color) {{
#             return {{
#                 type: 'gauge',
#                 startAngle: 180,
#                 endAngle: 0,
#                 min: {min_val},
#                 max: {max_val},
#                 radius: '90%',
#                 axisLine: {{
#                     lineStyle: {{
#                         width: 16,
#                         color: [[2, color]]
#                     }}
#                 }},
#                 pointer: {{
#                     show: true,
#                     width: 4,
#                     length: '55%'
#                 }},
#                 progress: {{
#                     show: true,
#                     width: 16,
#                     itemStyle: {{
#                         color: color
#                     }}
#                 }},
#                 axisLabel: {{
#                     fontSize: 10,
#                     distance: 15
#                 }},
#                 title: {{
#                     fontSize: 12,
#                     offsetCenter: [0, '-20%']
#                 }},
#                 detail: {{
#                     fontSize: 15,
#                     offsetCenter: [0, '30%'],
#                     formatter: '{{{{value}}}}{unit}'
#                 }},
#                 data: [{{value: value, name: name}}]
#             }};
#         }}

#         var chart1 = echarts.init(document.getElementById('{title}_design'));
#         chart1.setOption({{
#             series: [createGaugeConfig({design_value}, "Design", "#4A90E2")]
#         }});

#         var chart2 = echarts.init(document.getElementById('{title}_operating'));
#         chart2.setOption({{
#             series: [createGaugeConfig({operating_value}, "Operating", " #EE6666")]
#         }});
#     </script>
#     """
#     components.html(html_code, height=320)

# col1, col2 = st.columns(2)

# with col1:
#     dual_gauge_card("Boiler Efficiency", 89.5, 87.2, "%", 80, 100)

# with col2:
#     dual_gauge_card("Heat Rate", 2200, 2350, "kcal/kWh", 2000, 2600)

# col3, col4 = st.columns(2)

# with col3:
#     dual_gauge_card("APH Effectiveness", 88.0, 84.2, "%", 70, 100)

# with col4:
#     dual_gauge_card("Condenser Vacuum", 735, 710, "mmHg", 650, 760)




