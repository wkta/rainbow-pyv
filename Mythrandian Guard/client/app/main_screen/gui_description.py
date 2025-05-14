"""
constants that build the frame where Lackey icons can be
drag 'n dropped...

Structure:
  ............... [resources]...
  lackeys. ~ ~ -----------------
  |F|.|.|~ ~ ~  buildings.  ~ ~
  |.|.|.| ~ ~  ~ b0 ~ b1 ~ b2 ~
  |.|.|.| ~ ~ b3 ~ b4 ~ b5 ~ b6
  |.|.|.| ~ ~  ~ b7 ~ b8 ~ b9 ~
  |.|.|.| ~ ~ -----------------
  ....... ~ ~ m1 ~ m2 ~ m3 ~ m4
  ....(?).. ~ [ buttons GUI] ~~
"""

CENTERPOS_LACKEY_TITLE = (148, 90)  # where to position the title? centered

FIRST_LACKEY_POS = (25, 132)  # see the F letter in the structure in comm, topleft
LACKEY_X_OFFSET, LACKEY_Y_OFFSET = 90, 68
LACKEYS_PER_COL = 5

pos_buildings = [
    (494, 116),  # all elements given in the topleft style
    (494+1*106, 116),
    (494+2*106, 116),

    (441, 200),
    (441+1*106, 200),
    (441+2*106, 200),
    (441+3*106, 200),

    (494, 116+168),
    (494 + 1 * 106, 116+168),
    (494 + 2 * 106, 116+168),
]

pos_missions = [
    (365 + 0 * 190, 375),
    (365 + 1 * 190, 375),
    (365 + 2 * 190, 375),
]
