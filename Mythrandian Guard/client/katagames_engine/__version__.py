VYEAR_2DIG = 22  # remember to use only 2 digits
VMONTH = 10
_idx = 1  # 1 =alpha, 2 =beta, 3 =release candidate, 0 =legit release
VRANK = 1

"""
We target this standard format:
- Alpha release     yy.MMaN
- Beta release      yy.MMbN
- Release candidate yy.MMrcN
- Final release     yy.MM

So, to respect the PEP440 do not change anything pass this line!
"""
VRTYPE = ['', 'a', 'b', 'rc'][_idx]  # do not change this line
_suffix = '' if '' == VRTYPE else VRTYPE + str(VRANK)
ENGI_VERSION = f"{VYEAR_2DIG}.{VMONTH}{_suffix}"
