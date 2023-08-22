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
        return "Grade 0: Normal"
    elif 1.8 <= Y <= 3.2:
        return "Grade 1: Mild iron overload"
    elif 3.2 <= Y <= 7:
        return "Grade 2: Moderate Fe overload"
    elif 7 <= Y <= 15:
        return "Grade 3: Severe Fe overload"
    else:
        return "Grade 4: Extreme Fe overload"

def fat_grading(percentage):
    if percentage < 5:
        return "Grade 0: Normal"
    elif 5 <= percentage <= 17:
        return "Grade 1: Mild steatosis"
    elif 17 <= percentage <= 22:
        return "Grade 2: Moderate steatosis"
    else:
        return "Grade 3: Severe steatosis"

def calculate_fsm(m_values, a_values):
    return sum([m*a for m,a in zip(m_values, a_values)]) / sum(a_values)

def fsm_grading(fsm):
    if fsm < 2.5:
        return "Nl or chronic inflammation"
    elif 2.5 <= fsm <= 3.0:
        return "Stage 1-2"
    elif 3.0 <= fsm <= 3.5:
        return "Stage 2-3"
    elif 3.5 <= fsm <= 4.0:
        return "Stage 3-4"
    else:
        return "Stage 4-5"

st.title('Health Grading App')

# Calculate Iron
st.header('1) Calculate Iron')
T_values = ['1.5 T', '2.89 T', '3.0 T']
T_value = st.selectbox('Select T Value:', T_values)
X = st.number_input('Enter X Value:', value=0.0)
Y = calculate_iron(T_value, X)
st.write(f"Y value: {Y}")
st.write(iron_grading(Y))

# Determine Fat Grading
st.header('2) Determine Fat Grading')
percentage = st.slider('Enter Fat Percentage:', min_value=0.0, max_value=100.0, value=0.0)
st.write(fat_grading(percentage))

# Calculate the FSM
st.header('3) Calculate FSM')
m_values = [st.number_input(f'Enter roi{i}lsm Value:', value=0.0) for i in range(1, 5)]
a_values = [st.number_input(f'Enter roi{i}a Value:', value=0.0) for i in range(1, 5)]
fsm = calculate_fsm(m_values, a_values)
st.write(f"FSM Value: {fsm}")
st.write(fsm_grading(fsm))

# Clear results
st.header('4) Clear Results')
if st.button('Clear'):
    st.experimental_rerun()

if __name__ == "__main__":
    st.write('Welcome to the Health Grading App!')
