import streamlit as st
from datetime import datetime

class GlenoidTrackAssessment:
    def __init__(self, D=0, d=0, HSI=0):
        self.D = D  # glenoid joint face diameter
        self.d = d  # maximum diametric width of glenoid rim defect
        self.HSI = HSI  # Humeral Side Injury

    def calculate_GTW(self):
        return (0.83 * self.D) - self.d

    def determine_tracking_status(self, GTW):
        if self.HSI > GTW:
            return "off track"
        else:
            return "on track"

    def produce_radiology_report(self, GTW):
        report = f"""Glenoid Diameter: {self.D}\n\nGlenoid Rim Defect: {self.d}\n\nGTW: {GTW}\n\nGTW Formula Used: GTW = (0.83 x D) - d\n\nHSI: {self.HSI}\n\nHSL Tracking Status: {self.determine_tracking_status(GTW)}
        """
        return report

def run():
    # Streamlit app
    st.title("Glenoid Track Assessment")

    # Add 'Home' to the navigation options
    nav_selection = st.sidebar.radio('Glenoid Track Assessment', ['Home', 'Step 1: Identify bipolar bone lesions', 'Step 2: Calculate GTW', 'Step 3: Measure HSI', 'Step 4: Determine tracking status of HSL', 'Step 5: Radiology Report'])
    if nav_selection == 'Home':
        st.write("### Objectives")
        st.write("""1. Guided Assessment of Anterior Shoulder Dislocation: The app provides a systematic and simplified step-by-step approach to identify bipolar bone lesions, calculate the Glenoid Track Width (GTW), and measure the Humeral Side Injury (HSI) as shown in Aydıngöz, et al. 2023. Radiographics.\n\n2. Determination and Reporting of HSL Tracking Status: Through user input and subsequent calculations, the app determines the tracking status of the Hill-Sachs lesion (HSL) as either "on track" or "off track," generating a brief radiology report that can be downloaded for documentation and sharing.""")
    elif nav_selection == 'Step 1: Identify bipolar bone lesions':
        st.write("### Step 1: Identify bipolar bone lesions at CT or ZTE MRI")
        st.write("""Sometimes only HSL is present without any discernible glenoid rim defect. If HSL is sufficiently medial, it can still be off track (engage an intact glenoid rim).""")
    elif nav_selection == 'Step 2: Calculate GTW':
        st.write("### Step 2: Calculate GTW")
        st.write("""Place the best-fit circle on the lower two-thirds of pear-shaped glenoid on the glenoid en face view at MPR CT or ZTE MRI.""")
        D = st.number_input("Enter glenoid joint face diameter (D):", value=0.0)
        st.session_state['D'] = D
        d = st.number_input("Enter maximum diametric width of glenoid rim defect (d):", value=0.0)
        st.session_state['d'] = d
        st.write("""Ascertain glenoid rim defect size by identifying the deepest extent of glenoid rim defect on imaginary concentric circles within the best-fit circle.""")
    elif nav_selection == 'Step 3: Measure HSI':
        st.write("### Step 3: Measure HSI using MPR tool and cross-referencing on multiple images")
        st.write("""Identify the medialmost extent of HSL with respect to the dome of the humeral head. HSI is the shortest distance from this point to the medial edge of the rotator cuff footprint.""")
        HSI = st.number_input("Enter Humeral Side Injury measurement (HSI):", value=0.0)
        st.session_state['HSI'] = HSI
    elif nav_selection == 'Step 4: Determine tracking status of HSL':
        st.write("### Step 4: Determine tracking status of HSL")
        assessment = GlenoidTrackAssessment(st.session_state['D'], st.session_state['d'], st.session_state['HSI'])
        GTW = assessment.calculate_GTW()
        st.session_state['GTW'] = GTW
        status = assessment.determine_tracking_status(GTW)
        st.session_state['status'] = status
        st.write(f"The HSL is {status}.")
        # Display the status inside a makeshift box using markdown
        st.markdown(f"""<div style="background-color: #f0f0f5; padding: 10px; border-radius: 5px; border: 1px solid gray;"><h4 style="color: black; text-align: center;">The HSL is <strong>{status}</strong>.</h4></div>""", unsafe_allow_html=True)
    elif nav_selection == 'Step 5: Radiology Report':
        st.write("### Step 5: Radiology Report")
        report = assessment.produce_radiology_report(st.session_state['GTW'])
        st.session_state['report'] = report
        st.text_area("Report", report, height=400)  # Display the report in a text area
        # Create the filename with current date and time
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Radiology_Report_{current_time}.txt"
        st.session_state['filename'] = filename
    else:
        st.write("Please select an option from the sidebar.")

# if __name__ == '__main__':
#     run()