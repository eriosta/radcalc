import streamlit as st

def calculate_iron(T_value, X):
    if T_value == '1.5 T':
        return 2.603E-2 * X - 0.16
    elif T_value == '2.89 T':
        return 1.400E-2 * X - 0.03
    elif T_value == '3.0 T':
        return 1.349E-2 * X - 0.03

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
        return sum([m*a for m,a in zip(m_values, a_values)]) / total_area

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


st.title('MR Elastography App')

st.sidebar.header('Navigation')
nav_selection = st.sidebar.radio('', ['Calculate FSM', 'Determine Steatosis Grade', 'Calculate LIC', 'Generate Report', 'References'])

# Calculate FSM
if nav_selection == 'Calculate FSM':
    st.header('Calculate FSM')
    col1, col2 = st.columns(2)  # Assuming you're using a version of Streamlit that supports st.columns. If not, use st.beta_columns.
    
    m_values = [col1.number_input(f'Enter ROI{i} LSM:', value=0.0) for i in range(1, 5)]
    a_values = [col2.number_input(f'Enter ROI{i} area:', value=0.0) for i in range(1, 5)]
    
    if st.button('Calculate FSM'):
        if all(a != 0 for a in a_values):
            fsm = calculate_fsm(m_values, a_values)  # Assuming you have the calculate_fsm function defined somewhere.
            
            st.session_state['fsm'] = fsm
            st.session_state['fsm_min'] = min(m_values)
            st.session_state['fsm_max'] = max(m_values)
            st.session_state['fsm_grade'] = fsm_grading(fsm)  # Saving the grade to the session state.

            st.write(f"FSM: {fsm} kPa")
            st.write(st.session_state['fsm_grade'])
        else:
            st.error("All ROI areas must be non-zero!")


# Determine Steatosis Grade
elif nav_selection == 'Determine Steatosis Grade':
    st.header('Determine Steatosis Grade')
    percentage = st.number_input('Enter PDFF (%):', min_value=0.0, max_value=100.0, value=0.0)
    if st.button('Calculate Steatosis Grade'):
        grade = fat_grading(percentage)
        st.session_state['steatosis_percentage'] = percentage
        st.session_state['steatosis_grade'] = grade
        st.write(grade)

# Calculate LIC
elif nav_selection == 'Calculate LIC':
    st.header('Calculate LIC')
    T_values = ['1.5 T', '2.89 T', '3.0 T']
    T_value = st.selectbox('Select MR:', T_values)
    X = st.number_input('Enter R2* Value:', value=0.0)
    if st.button('Calculate LIC'):
        Y = calculate_iron(T_value, X)
        st.session_state['MR_type'] = T_value
        st.session_state['R2_value'] = X
        st.session_state['LIC'] = Y
        st.session_state['iron_grade'] = iron_grading(Y)
        st.write(f"LIC: {Y} mg/g")
        st.write(iron_grading(Y))

# Generate Report
elif nav_selection == 'Generate Report':
    st.header('Generate Report')
    
    # Select Sequence and Tesla scanner
    sequence_options = ['GRE', 'SE EPI']
    selected_sequence = st.selectbox('Select Sequence:', sequence_options)
    
    scanner_options = ['1.5', '3.0', '2.89']
    selected_scanner = st.selectbox('Select Tesla scanner:', scanner_options)

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
    report = f"""
PROCEDURE: {selected_sequence} MR elastography and chemical shift-encoded GRE sequences were performed for liver fibrosis, fat, and iron quantification on a {selected_scanner} Tesla scanner.

MR Liver Elastography
Mean liver stiffness (weighted mean of [{fsm_min} - {fsm_max}] measurements): {fsm} kPa
Interpretation of MR elastography results: {fsm_grade}

MR Liver Fat Quantification
In representative areas of the liver, the mean proton density fat-fraction (PDFF) is {steatosis_percentage}%.
Histological grade: {steatosis_grade}

MR Liver Iron Quantification
In representative areas of the liver, the mean transverse relaxation rate R2* is {R2_value}/s at {MR_type}, corresponding to a liver iron concentration (LIC) of {LIC} mg Fe/g.
Iron overload severity grade: {iron_grade}
"""

    st.write(report)


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