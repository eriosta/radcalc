import streamlit as st

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
        report = f"""
        Glenoid Diameter: {self.D}
        Glenoid Rim Defect: {self.d}
        GTW: {GTW}
        GTW Formula Used: GTW = (0.83 x D) - d
        HSI: {self.HSI}
        HSL Tracking Status: {self.determine_tracking_status(GTW)}
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

st.write("### Step 5: Produce Radiology Report")
st.write(assessment.produce_radiology_report(GTW))

if st.button("Generate Report"):
    st.write("Report Generated Successfully!")
