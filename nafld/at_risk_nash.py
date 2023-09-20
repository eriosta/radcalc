import numpy as np

def calculate_FAST(LSM, CAP, AST):
    n = -1.65 + 1.07 * np.log(LSM) + 2.66 * 10**-8 * CAP**3 - 63.3 * AST**-1
    FAST = np.exp(n) / (1 + np.exp(n))
    if FAST >= 0.67:
        return "Specific for At-Risk NASH, FAST: " + str(FAST)
    elif FAST >= 0.35 and FAST < 0.67:
        return "Sensitive for At-Risk NASH, FAST: " + str(FAST)
    else:
        return "At-Risk NASH Unlikely, FAST: " + str(FAST)

def calculate_MAST(MRE, PDFF, AST):
    MAST = -12.17 + 7.07 * np.log(MRE) + 0.037 * PDFF - 3.55 * np.log(AST)
    if MAST >= 0.242:
        return "Specific for At-Risk NASH, MAST: " + str(MAST)
    elif MAST >= 0.165 and MAST < 0.242:
        return "Sensitive for At-Risk NASH, MAST: " + str(MAST)
    else:
        return "At-Risk NASH Unlikely, MAST: " + str(MAST)

def calculate_MEFIB(MRE, FIB4):
    if MRE >= 3.3 and FIB4 >= 1.6:
        return "At-Risk NASH"
    else:
        return "Not At-Risk NASH"




