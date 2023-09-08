import streamlit as st
import io
import base64
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
import random
import altair as alt

# Define parameters for each MR type
params = {
    '1.5 T': {'intercept': -0.16, 'slope': 2.603e-2, 'r2': 0.88, 'conf_intercept': (-.64, 0.32), 'conf_slope': (2.468e-2, 2.738e-2)},
    '2.89 T': {'intercept': -0.03, 'slope': 1.400e-2, 'r2': 0.93, 'conf_intercept': (-.51, .45), 'conf_slope': (1.33e-2, 1.471e-2)},
    '3.0 T': {'intercept': -0.03, 'slope': 1.349e-2, 'r2': 0.87, 'conf_intercept': (-.51, .45), 'conf_slope': (1.282e-2, 1.417e-2)}
}

# Create a decorator to display a toast when a step is completed
# def step_completed(func):
#     def wrapper(*args, **kwargs):
#         result = func(*args, **kwargs)
#         messages = ['Completed!', 'Well done!', '10/10', "Let's go!", "Top 1 percentile!", "You inspire us!", "OK, go off!", "Superb!", "Nicely done!", "Show 'em how it's done!", "100%!"]
#         emojis = ['🎉', '👏', '💯', '🚀', '🔥', '🌟', '💪', '🎯', '🏆', '🥇']
#         st.toast(random.choice(messages), icon=random.choice(emojis))
#         return result
#     return wrapper

def step_completed(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        messages = ['Completed!']
        emojis = ['✅']
        st.toast(random.choice(messages), icon=random.choice(emojis))
        return result
    return wrapper

# Calculate LIC
def calculate_iron(T_value, R2_star):
    return round(params[T_value]['intercept'] + params[T_value]['slope'] * R2_star,1)

# Assuming params dictionary and other necessary variables are defined earlier in your script

import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# Assuming params dictionary and other necessary variables are defined earlier in your script

# Plot LIC with confidence intervals using Streamlit's built-in charts
def plot_LIC(T_value, R2_value, LIC):
    x = np.linspace(0, max(100, R2_value+10), 100)
    y = params[T_value]['intercept'] + params[T_value]['slope'] * x
    y_lower = params[T_value]['conf_intercept'][0] + params[T_value]['conf_slope'][0] * x
    y_upper = params[T_value]['conf_intercept'][1] + params[T_value]['conf_slope'][1] * x
    
    # Prepare data in a dataframe
    df = pd.DataFrame({
        'x': x,
        'y': y,
        'y_lower': y_lower,
        'y_upper': y_upper
    })

    # Create the Altair chart
    base = alt.Chart(df).encode(
        x=alt.X('x', title='R2* (/s)'),
        y=alt.Y('y', title='LIC (mg/g)')
    )

    line = base.mark_line(color='blue').encode(y='y')
    band = base.mark_area(opacity=0.1, color='blue').encode(y='y_lower', y2='y_upper')
    point = alt.Chart(pd.DataFrame({'x': [R2_value], 'y': [LIC]})).mark_circle(color='red', size=100).encode(x='x', y='y')

    # Combine the charts
    chart = (line + band + point).properties(
        width=600,
        height=400,
        title=f'LIC Visualization for {T_value}'
    ).interactive()

    # Display the chart in Streamlit
    st.altair_chart(chart)

    # Displaying the formula
    formula_text = f"LIC = {params[T_value]['intercept']:.2f} + {params[T_value]['slope']:.4f} * R2*"
    st.write(formula_text)


@step_completed
def iron_grading(Y):
    if Y < 1.8:
        return "Grade 0: Normal. No Fe overload."
    elif 1.8 <= Y <= 3.2:
        return "Grade 1: Mild Fe overload."
    elif 3.2 <= Y <= 7:
        return "Grade 2: Moderate Fe overload."
    elif 7 <= Y <= 15:
        return "Grade 3: Severe Fe overload."
    else:
        return "Grade 4: Extreme Fe overload."

@step_completed
def fat_grading(percentage):
    if percentage < 5:
        return "Grade 0: Normal. No steatosis."
    elif 5 <= percentage <= 17:
        return "Grade 1: Mild steatosis."
    elif 17 <= percentage <= 22:
        return "Grade 2: Moderate steatosis."
    else:
        return "Grade 3: Severe steatosis."

def calculate_fsm(m_values, a_values):
    total_area = sum(a_values)
    if total_area == 0:
        return 0  # or whatever default or error value you want to return
    else:
        result = sum([m*a for m,a in zip(m_values, a_values)]) / total_area
        return round(result, 1)

@step_completed
def fsm_grading(fsm_value):
    if fsm_value < 2.5:
        return "Normal"
    elif 2.5 <= fsm_value < 3.0:
        return "Normal or inflammation"
    elif 3.0 <= fsm_value < 3.5:
        return "Stage 1–2 fibrosis"
    elif 3.5 <= fsm_value < 4.0:
        return "Stage 2–3 fibrosis"
    elif 4.0 <= fsm_value < 5.0:
        return "Stage 3–4 fibrosis"
    else:
        return "Stage 4 fibrosis or cirrhosis"

# Function to create a download link for files
def download_link(object_to_download, download_filename, download_link_text):
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    # Encode to bytes and create a download link
    b64 = base64.b64encode(object_to_download.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

def run():
    st.title('MRE')

    # Add 'Home' to the navigation options
    nav_selection = st.sidebar.radio('MRE', ['Start Here', 'Step 1: Calculate LSM', 'Step 2: Determine Steatosis Grade', 'Step 3: Calculate LIC', 'Generate Report', 'References'])

    # Home Page
    if nav_selection == 'Start Here':
        st.header('MR Liver Elastography Calculator')
        st.write("""
        This calculator helps with:
        - Calculating Liver Stiffness Measure (LSM)
        - Determining Steatosis Grade
        - Calculating Liver Iron Content (LIC)
        - Generating structured reports
        - Referencing established standards

        Navigate using the sidebar and select the required function to begin.
        """)

    # Calculate FSM
    if nav_selection == 'Step 1: Calculate LSM':
        st.header('Calculate LSM')

        # Let the user choose the number of ROIs
        num_rois = st.selectbox('Select the number of ROIs:', [1, 2, 3, 4], index=3)  # Default is 4 ROIs

        col1, col2 = st.columns(2)  # Assuming you're using a version of Streamlit that supports st.columns. If not, use st.beta_columns.
               
        m_values = [col1.number_input(f'Enter ROI{i} LSM:', value=0.0) for i in range(1, num_rois + 1)]
        a_values = [col2.number_input(f'Enter ROI{i} area:', value=0.0) for i in range(1, num_rois + 1)]
        
        if st.button('Calculate LSM'):
            if all(a != 0 for a in a_values):
                fsm = calculate_fsm(m_values, a_values)  # Assuming you have the calculate_fsm function defined somewhere.
                
                st.session_state['fsm'] = fsm
                st.session_state['fsm_min'] = min(m_values)
                st.session_state['fsm_max'] = max(m_values)
                st.session_state['fsm_grade'] = fsm_grading(fsm)  # Saving the grade to the session state.

                fsm_display = f"LSM: {fsm} kPa"
                result_message = f"{fsm_display} corresponds to {st.session_state['fsm_grade']}"

                st.info(result_message)
            else:
                st.error("All ROI areas must be non-zero!")


    # Determine Steatosis Grade
    elif nav_selection == 'Step 2: Determine Steatosis Grade':
        st.header('Determine Steatosis Grade')
        percentage = st.number_input('Enter PDFF (%):', min_value=0.0, max_value=100.0, value=0.0)
        if st.button('Calculate Steatosis Grade'):
            grade = fat_grading(percentage)
            st.session_state['steatosis_percentage'] = percentage
            st.session_state['steatosis_grade'] = grade
            st.info(grade)

    # Calculate LIC
    elif nav_selection == 'Step 3: Calculate LIC':
        st.header('Calculate LIC')
        T_values = ['1.5 T', '2.89 T', '3.0 T']
        default_T_value = T_values.index('3.0 T')  # Index for '3.0 T'
        T_value = st.selectbox('Select MR:', T_values, index=default_T_value)
        X = st.number_input('Enter R2* Value:', value=0.0)
        if st.button('Calculate LIC'):
            Y = calculate_iron(T_value, X)
            st.session_state['MR_type'] = T_value
            st.session_state['R2_value'] = X
            st.session_state['LIC'] = Y
            st.session_state['iron_grade'] = iron_grading(Y)
            st.write(f"LIC: {Y:.2f} mg/g")
            st.info(iron_grading(Y))
            st.write(f"R^2 for {T_value}: {params[T_value]['r2']}")
            plot_LIC(T_value, X, Y)

    # Generate Report
    elif nav_selection == 'Generate Report':
        st.header('Generate Report')
        
        # Select Sequence and Tesla scanner
        sequence_options = ['GRE', 'SE EPI']
        default_sequence = sequence_options.index('SE EPI')  # Index for 'SE EPI'
        selected_sequence = st.selectbox('Select Sequence:', sequence_options, index=default_sequence)
        
        scanner_options = ['1.5', '3.0', '2.89']
        default_scanner = scanner_options.index('3.0')  # Index for '3.0'
        selected_scanner = st.selectbox('Select Tesla scanner:', scanner_options, index=default_scanner)

        # Retrieve FSM values and grading
        fsm = st.session_state.get('fsm', 'N/A')
        fsm_min = st.session_state.get('fsm_min', 'N/A')
        fsm_max = st.session_state.get('fsm_max', 'N/A')
        fsm_grade = st.session_state.get('fsm_grade', 'N/A')  # New: retrieve FSM grade from session state

        # Retrieve Steatosis values
        steatosis_percentage = st.session_state.get('steatosis_percentage', 'N/A')
        steatosis_grade = st.session_state.get('steatosis_grade', 'N/A')

        # Retrieve LIC values
        MR_type = st.session_state.get('MR_type', 'N/A')
        R2_value = st.session_state.get('R2_value', 'N/A')
        LIC = st.session_state.get('LIC', 'N/A')
        iron_grade = st.session_state.get('iron_grade', 'N/A')


        # Generate the report content
        st.header('Report:')
        report = f"""PROCEDURE: {selected_sequence} MR elastography and chemical shift-encoded GRE sequences were performed for liver fibrosis, fat, and iron quantification on a {selected_scanner} Tesla scanner.\n\nLIVER ELASTOGRAPHY: Mean liver stiffness (weighted mean of [{fsm_min} - {fsm_max}] measurements): {fsm} kPa. Interpretation of MR elastography results: {fsm_grade}.\n\nLIVER FAT FRACTION: In representative areas of the liver, the mean proton density fat-fraction (PDFF) is {steatosis_percentage}%. Histological grade: {steatosis_grade}.\n\nLIVER IRON CONTENT: In representative areas of the liver, the mean transverse relaxation rate R2* is {R2_value}/s at {MR_type}, corresponding to a liver iron concentration (LIC) of {LIC} mg Fe/g. Iron overload severity grade: {iron_grade}."""

        # Display the report in a text area
        st.text_area("Report Content:", value=report, height=400, max_chars=None)  # Adjust the height as required

        # Generate the current date and time and format it to a string
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f"MR_LIVER_ELASTOGRAPHY_{current_datetime}.txt"

        # Create a download link for the report
        download_link_text = "Download Report"
        st.markdown(download_link(report, filename, download_link_text), unsafe_allow_html=True)


    # References Section
    elif nav_selection == 'References':
        st.header("References")
        references = [
            "Guglielmo FF, Barr RG, Yokoo T, Ferraioli G, Lee JT, Dillman JR, Horowitz JM, Jhaveri KS, Miller FH, Modi RY, Mojtahed A, Ohliger MA, Pirasteh A, Reeder SB, Shanbhogue K, Silva AC, Smith EN, Surabhi VR, Taouli B, Welle CL, Yeh BM, Venkatesh SK. Liver Fibrosis, Fat, and Iron Evaluation with MRI and Fibrosis and Fat Evaluation with US: A Practical Guide for Radiologists. Radiographics. 2023 Jun;43(6):e220181. doi: 10.1148/rg.220181. PMID: 37227944.",
            "Hernando D, Zhao R, Yuan Q, Aliyari Ghasabeh M, Ruschke S, Miao X, Karampinos DC, Mao L, Harris DT, Mattison RJ, Jeng MR, Pedrosa I, Kamel IR, Vasanawala S, Yokoo T, Reeder SB. Multicenter Reproducibility of Liver Iron Quantification with 1.5-T and 3.0-T MRI. Radiology. 2023 Feb;306(2):e213256. doi: 10.1148/radiol.213256. Epub 2022 Oct 4. PMID: 36194113; PMCID: PMC9885339.",
            "Yokoo T, Serai SD, Pirasteh A, Bashir MR, Hamilton G, Hernando D, Hu HH, Hetterich H, Kühn JP, Kukuk GM, Loomba R, Middleton MS, Obuchowski NA, Song JS, Tang A, Wu X, Reeder SB, Sirlin CB; RSNA-QIBA PDFF Biomarker Committee. Linearity, Bias, and Precision of Hepatic Proton Density Fat Fraction Measurements by Using MR Imaging: A Meta-Analysis. Radiology. 2018 Feb;286(2):486-498. doi: 10.1148/radiol.2017170550. Epub 2017 Sep 11. PMID: 28892458; PMCID: PMC5813433."

        ]
        for ref in references:
            st.write("- " + ref)

# if __name__ == '__main__':
#     run()