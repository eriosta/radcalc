import numpy as np

def calculate_FIB4(NAFLD_suspected, Age, AST, Platelets, ALT):
    if NAFLD_suspected == 'No':
        return "NAFLD not suspected. FIB4 not calculated."
    elif Age < 35 or Age > 65:
        return "Use with caution; FIB4 less reliable in these age groups"
    else:
        FIB4 = (Age * AST) / (Platelets * np.sqrt(ALT))
        if FIB4 >= 1.3:
            return "FIB4 score: " + str(FIB4) + ". 2023 AASLD Practice Guidance: FIB4 is greater than or equal to 1.3. Exclude advanced fibrosis with VCTE, MRE, or ELF."
        else:
            return "FIB4 score: " + str(FIB4)
