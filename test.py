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

# Streamlit app
st.title("Glenoid Track Assessment")

st.write("### Step 1: Identify bipolar bone lesions at CT or ZTE MRI")
st.write("""
Sometimes only HSL is present without any discernible glenoid rim defect.
If HSL is sufficiently medial, it can still be off track (engage an intact glenoid rim).
""")

st.write("### Step 2: Calculate GTW")
st.write("""
Place the best-fit circle on the lower two-thirds of pear-shaped glenoid on the glenoid
en face view at MPR CT or ZTE MRI.
""")
D = st.number_input("Enter glenoid joint face diameter (D):", value=0.0)
d = st.number_input("Enter maximum diametric width of glenoid rim defect (d):", value=0.0)

st.write("""
Ascertain glenoid rim defect size by identifying the deepest extent of glenoid
rim defect on imaginary concentric circles within the best-fit circle.
""")

st.write("### Step 3: Measure HSI using MPR tool and cross-referencing on multiple images")
st.write("""
Identify the medialmost extent of HSL with respect to the dome of the humeral head.
HSI is the shortest distance from this point to the medial edge of the rotator cuff footprint.
""")
HSI = st.number_input("Enter Humeral Side Injury measurement (HSI):", value=0.0)

assessment = GlenoidTrackAssessment(D, d, HSI)
GTW = assessment.calculate_GTW()

st.write("### Step 4: Determine tracking status of HSL")
status = assessment.determine_tracking_status(GTW)
st.write(f"The HSL is {status}.")

st.write("### Step 5: Radiology Report")
report = assessment.produce_radiology_report(GTW)
st.text_area("Report", report, height=400)  # Display the report in a text area

# Create the filename with current date and time
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"Radiology_Report_{current_time}.txt"

if st.download_button("Download Report", data=report, file_name=filename, mime="text/plain"):
    st.write("Report Downloaded Successfully!")

# Glossary Section
st.write("### Glossary")
glossary = """ABER = abduction and external rotation\n\nGTW = glenoid track width\n\nHSI = Hill-Sachs interval\n\nHSL = Hill-Sachs lesion\n\nMPR = multiplanar reformation\n\nZTE = zero echo time\n\n
"""
st.write(glossary)

# References
st.write("### References")
st.write("""Aydıngöz Ü, Yıldız AE, Huri G. Glenoid Track Assessment at Imaging in Anterior Shoulder Instability: Rationale and Step-by-Step Guide. Radiographics. 2023 Aug;43(8):e230030. doi: 10.1148/rg.230030. PMID: 37410625.""")