
import xlrd

workbook = xlrd.open_workbook("96wells.xlsx", on_demand = True)
worksheet = workbook.sheet_by_name('Sheet1')
num_rows = worksheet.nrows - 1

well_id_to_cell = {}
col_and_row_to_cell = {}

curr_row = 0
while curr_row < num_rows:
    curr_row += 1
    col_and_row = worksheet.cell_value(curr_row,0)
    well_id = int(worksheet.cell_value(curr_row,1))
    col = int(worksheet.cell_value(curr_row,2))
    row = int(worksheet.cell_value(curr_row,3))
    #print col_and_row, well_id, row, col
    well_id_to_cell[well_id] = {
        "col_and_row":col_and_row, 
        "well_id":well_id, 
        "row":row, 
        "col":col
    }
    col_and_row_to_cell[col_and_row] = {
        "col_and_row":col_and_row, 
        "well_id":well_id, 
        "row":row, 
        "col":col
    }

print "FOO"

print well_id_to_cell

well_id_to_cell_map_96 = {
    1: {
        'col_and_row': u'A1',
        'row': 1,
        'col': 1,
        'well_id': 1,
        },
    2: {
        'col_and_row': u'A2',
        'row': 1,
        'col': 2,
        'well_id': 2,
        },
    3: {
        'col_and_row': u'A3',
        'row': 1,
        'col': 3,
        'well_id': 3,
        },
    4: {
        'col_and_row': u'A4',
        'row': 1,
        'col': 4,
        'well_id': 4,
        },
    5: {
        'col_and_row': u'A5',
        'row': 1,
        'col': 5,
        'well_id': 5,
        },
    6: {
        'col_and_row': u'A6',
        'row': 1,
        'col': 6,
        'well_id': 6,
        },
    7: {
        'col_and_row': u'A7',
        'row': 1,
        'col': 7,
        'well_id': 7,
        },
    8: {
        'col_and_row': u'A8',
        'row': 1,
        'col': 8,
        'well_id': 8,
        },
    9: {
        'col_and_row': u'A9',
        'row': 1,
        'col': 9,
        'well_id': 9,
        },
    10: {
        'col_and_row': u'A10',
        'row': 1,
        'col': 10,
        'well_id': 10,
        },
    11: {
        'col_and_row': u'A11',
        'row': 1,
        'col': 11,
        'well_id': 11,
        },
    12: {
        'col_and_row': u'A12',
        'row': 1,
        'col': 12,
        'well_id': 12,
        },
    13: {
        'col_and_row': u'B1',
        'row': 2,
        'col': 1,
        'well_id': 13,
        },
    14: {
        'col_and_row': u'B2',
        'row': 2,
        'col': 2,
        'well_id': 14,
        },
    15: {
        'col_and_row': u'B3',
        'row': 2,
        'col': 3,
        'well_id': 15,
        },
    16: {
        'col_and_row': u'B4',
        'row': 2,
        'col': 4,
        'well_id': 16,
        },
    17: {
        'col_and_row': u'B5',
        'row': 2,
        'col': 5,
        'well_id': 17,
        },
    18: {
        'col_and_row': u'B6',
        'row': 2,
        'col': 6,
        'well_id': 18,
        },
    19: {
        'col_and_row': u'B7',
        'row': 2,
        'col': 7,
        'well_id': 19,
        },
    20: {
        'col_and_row': u'B8',
        'row': 2,
        'col': 8,
        'well_id': 20,
        },
    21: {
        'col_and_row': u'B9',
        'row': 2,
        'col': 9,
        'well_id': 21,
        },
    22: {
        'col_and_row': u'B10',
        'row': 2,
        'col': 10,
        'well_id': 22,
        },
    23: {
        'col_and_row': u'B11',
        'row': 2,
        'col': 11,
        'well_id': 23,
        },
    24: {
        'col_and_row': u'B12',
        'row': 2,
        'col': 12,
        'well_id': 24,
        },
    25: {
        'col_and_row': u'C1',
        'row': 3,
        'col': 1,
        'well_id': 25,
        },
    26: {
        'col_and_row': u'C2',
        'row': 3,
        'col': 2,
        'well_id': 26,
        },
    27: {
        'col_and_row': u'C3',
        'row': 3,
        'col': 3,
        'well_id': 27,
        },
    28: {
        'col_and_row': u'C4',
        'row': 3,
        'col': 4,
        'well_id': 28,
        },
    29: {
        'col_and_row': u'C5',
        'row': 3,
        'col': 5,
        'well_id': 29,
        },
    30: {
        'col_and_row': u'C6',
        'row': 3,
        'col': 6,
        'well_id': 30,
        },
    31: {
        'col_and_row': u'C7',
        'row': 3,
        'col': 7,
        'well_id': 31,
        },
    32: {
        'col_and_row': u'C8',
        'row': 3,
        'col': 8,
        'well_id': 32,
        },
    33: {
        'col_and_row': u'C9',
        'row': 3,
        'col': 9,
        'well_id': 33,
        },
    34: {
        'col_and_row': u'C10',
        'row': 3,
        'col': 10,
        'well_id': 34,
        },
    35: {
        'col_and_row': u'C11',
        'row': 3,
        'col': 11,
        'well_id': 35,
        },
    36: {
        'col_and_row': u'C12',
        'row': 3,
        'col': 12,
        'well_id': 36,
        },
    37: {
        'col_and_row': u'D1',
        'row': 4,
        'col': 1,
        'well_id': 37,
        },
    38: {
        'col_and_row': u'D2',
        'row': 4,
        'col': 2,
        'well_id': 38,
        },
    39: {
        'col_and_row': u'D3',
        'row': 4,
        'col': 3,
        'well_id': 39,
        },
    40: {
        'col_and_row': u'D4',
        'row': 4,
        'col': 4,
        'well_id': 40,
        },
    41: {
        'col_and_row': u'D5',
        'row': 4,
        'col': 5,
        'well_id': 41,
        },
    42: {
        'col_and_row': u'D6',
        'row': 4,
        'col': 6,
        'well_id': 42,
        },
    43: {
        'col_and_row': u'D7',
        'row': 4,
        'col': 7,
        'well_id': 43,
        },
    44: {
        'col_and_row': u'D8',
        'row': 4,
        'col': 8,
        'well_id': 44,
        },
    45: {
        'col_and_row': u'D9',
        'row': 4,
        'col': 9,
        'well_id': 45,
        },
    46: {
        'col_and_row': u'D10',
        'row': 4,
        'col': 10,
        'well_id': 46,
        },
    47: {
        'col_and_row': u'D11',
        'row': 4,
        'col': 11,
        'well_id': 47,
        },
    48: {
        'col_and_row': u'D12',
        'row': 4,
        'col': 12,
        'well_id': 48,
        },
    49: {
        'col_and_row': u'E1',
        'row': 5,
        'col': 1,
        'well_id': 49,
        },
    50: {
        'col_and_row': u'E2',
        'row': 5,
        'col': 2,
        'well_id': 50,
        },
    51: {
        'col_and_row': u'E3',
        'row': 5,
        'col': 3,
        'well_id': 51,
        },
    52: {
        'col_and_row': u'E4',
        'row': 5,
        'col': 4,
        'well_id': 52,
        },
    53: {
        'col_and_row': u'E5',
        'row': 5,
        'col': 5,
        'well_id': 53,
        },
    54: {
        'col_and_row': u'E6',
        'row': 5,
        'col': 6,
        'well_id': 54,
        },
    55: {
        'col_and_row': u'E7',
        'row': 5,
        'col': 7,
        'well_id': 55,
        },
    56: {
        'col_and_row': u'E8',
        'row': 5,
        'col': 8,
        'well_id': 56,
        },
    57: {
        'col_and_row': u'E9',
        'row': 5,
        'col': 9,
        'well_id': 57,
        },
    58: {
        'col_and_row': u'E10',
        'row': 5,
        'col': 10,
        'well_id': 58,
        },
    59: {
        'col_and_row': u'E11',
        'row': 5,
        'col': 11,
        'well_id': 59,
        },
    60: {
        'col_and_row': u'E12',
        'row': 5,
        'col': 12,
        'well_id': 60,
        },
    61: {
        'col_and_row': u'F1',
        'row': 6,
        'col': 1,
        'well_id': 61,
        },
    62: {
        'col_and_row': u'F2',
        'row': 6,
        'col': 2,
        'well_id': 62,
        },
    63: {
        'col_and_row': u'F3',
        'row': 6,
        'col': 3,
        'well_id': 63,
        },
    64: {
        'col_and_row': u'F4',
        'row': 6,
        'col': 4,
        'well_id': 64,
        },
    65: {
        'col_and_row': u'F5',
        'row': 6,
        'col': 5,
        'well_id': 65,
        },
    66: {
        'col_and_row': u'F6',
        'row': 6,
        'col': 6,
        'well_id': 66,
        },
    67: {
        'col_and_row': u'F7',
        'row': 6,
        'col': 7,
        'well_id': 67,
        },
    68: {
        'col_and_row': u'F8',
        'row': 6,
        'col': 8,
        'well_id': 68,
        },
    69: {
        'col_and_row': u'F9',
        'row': 6,
        'col': 9,
        'well_id': 69,
        },
    70: {
        'col_and_row': u'F10',
        'row': 6,
        'col': 10,
        'well_id': 70,
        },
    71: {
        'col_and_row': u'F11',
        'row': 6,
        'col': 11,
        'well_id': 71,
        },
    72: {
        'col_and_row': u'F12',
        'row': 6,
        'col': 12,
        'well_id': 72,
        },
    73: {
        'col_and_row': u'G1',
        'row': 7,
        'col': 1,
        'well_id': 73,
        },
    74: {
        'col_and_row': u'G2',
        'row': 7,
        'col': 2,
        'well_id': 74,
        },
    75: {
        'col_and_row': u'G3',
        'row': 7,
        'col': 3,
        'well_id': 75,
        },
    76: {
        'col_and_row': u'G4',
        'row': 7,
        'col': 4,
        'well_id': 76,
        },
    77: {
        'col_and_row': u'G5',
        'row': 7,
        'col': 5,
        'well_id': 77,
        },
    78: {
        'col_and_row': u'G6',
        'row': 7,
        'col': 6,
        'well_id': 78,
        },
    79: {
        'col_and_row': u'G7',
        'row': 7,
        'col': 7,
        'well_id': 79,
        },
    80: {
        'col_and_row': u'G8',
        'row': 7,
        'col': 8,
        'well_id': 80,
        },
    81: {
        'col_and_row': u'G9',
        'row': 7,
        'col': 9,
        'well_id': 81,
        },
    82: {
        'col_and_row': u'G10',
        'row': 7,
        'col': 10,
        'well_id': 82,
        },
    83: {
        'col_and_row': u'G11',
        'row': 7,
        'col': 11,
        'well_id': 83,
        },
    84: {
        'col_and_row': u'G12',
        'row': 7,
        'col': 12,
        'well_id': 84,
        },
    85: {
        'col_and_row': u'H1',
        'row': 8,
        'col': 1,
        'well_id': 85,
        },
    86: {
        'col_and_row': u'H2',
        'row': 8,
        'col': 2,
        'well_id': 86,
        },
    87: {
        'col_and_row': u'H3',
        'row': 8,
        'col': 3,
        'well_id': 87,
        },
    88: {
        'col_and_row': u'H4',
        'row': 8,
        'col': 4,
        'well_id': 88,
        },
    89: {
        'col_and_row': u'H5',
        'row': 8,
        'col': 5,
        'well_id': 89,
        },
    90: {
        'col_and_row': u'H6',
        'row': 8,
        'col': 6,
        'well_id': 90,
        },
    91: {
        'col_and_row': u'H7',
        'row': 8,
        'col': 7,
        'well_id': 91,
        },
    92: {
        'col_and_row': u'H8',
        'row': 8,
        'col': 8,
        'well_id': 92,
        },
    93: {
        'col_and_row': u'H9',
        'row': 8,
        'col': 9,
        'well_id': 93,
        },
    94: {
        'col_and_row': u'H10',
        'row': 8,
        'col': 10,
        'well_id': 94,
        },
    95: {
        'col_and_row': u'H11',
        'row': 8,
        'col': 11,
        'well_id': 95,
        },
    96: {
        'col_and_row': u'H12',
        'row': 8,
        'col': 12,
        'well_id': 96,
        },
    }

            
def get_col_and_row_for_well_id_96(well_id):
    cell = well_id_to_cell_map_96[well_id]
    return cell["col_and_row"]

#for key, value in stuff.items():
#    print "KEY: ", key, " col_and_row: ", value["col_and_row"]

#print col_and_row_to_cell

col_and_row_to_cell_map_96 = {
    u'G7': {
        'col_and_row': u'G7',
        'row': 7,
        'col': 7,
        'well_id': 79,
        },
    u'G6': {
        'col_and_row': u'G6',
        'row': 7,
        'col': 6,
        'well_id': 78,
        },
    u'G5': {
        'col_and_row': u'G5',
        'row': 7,
        'col': 5,
        'well_id': 77,
        },
    u'G4': {
        'col_and_row': u'G4',
        'row': 7,
        'col': 4,
        'well_id': 76,
        },
    u'G3': {
        'col_and_row': u'G3',
        'row': 7,
        'col': 3,
        'well_id': 75,
        },
    u'G2': {
        'col_and_row': u'G2',
        'row': 7,
        'col': 2,
        'well_id': 74,
        },
    u'G1': {
        'col_and_row': u'G1',
        'row': 7,
        'col': 1,
        'well_id': 73,
        },
    u'G9': {
        'col_and_row': u'G9',
        'row': 7,
        'col': 9,
        'well_id': 81,
        },
    u'G8': {
        'col_and_row': u'G8',
        'row': 7,
        'col': 8,
        'well_id': 80,
        },
    u'B4': {
        'col_and_row': u'B4',
        'row': 2,
        'col': 4,
        'well_id': 16,
        },
    u'B5': {
        'col_and_row': u'B5',
        'row': 2,
        'col': 5,
        'well_id': 17,
        },
    u'B6': {
        'col_and_row': u'B6',
        'row': 2,
        'col': 6,
        'well_id': 18,
        },
    u'B7': {
        'col_and_row': u'B7',
        'row': 2,
        'col': 7,
        'well_id': 19,
        },
    u'B1': {
        'col_and_row': u'B1',
        'row': 2,
        'col': 1,
        'well_id': 13,
        },
    u'B2': {
        'col_and_row': u'B2',
        'row': 2,
        'col': 2,
        'well_id': 14,
        },
    u'B3': {
        'col_and_row': u'B3',
        'row': 2,
        'col': 3,
        'well_id': 15,
        },
    u'B8': {
        'col_and_row': u'B8',
        'row': 2,
        'col': 8,
        'well_id': 20,
        },
    u'B9': {
        'col_and_row': u'B9',
        'row': 2,
        'col': 9,
        'well_id': 21,
        },
    u'E9': {
        'col_and_row': u'E9',
        'row': 5,
        'col': 9,
        'well_id': 57,
        },
    u'E8': {
        'col_and_row': u'E8',
        'row': 5,
        'col': 8,
        'well_id': 56,
        },
    u'E5': {
        'col_and_row': u'E5',
        'row': 5,
        'col': 5,
        'well_id': 53,
        },
    u'E4': {
        'col_and_row': u'E4',
        'row': 5,
        'col': 4,
        'well_id': 52,
        },
    u'E7': {
        'col_and_row': u'E7',
        'row': 5,
        'col': 7,
        'well_id': 55,
        },
    u'E6': {
        'col_and_row': u'E6',
        'row': 5,
        'col': 6,
        'well_id': 54,
        },
    u'E1': {
        'col_and_row': u'E1',
        'row': 5,
        'col': 1,
        'well_id': 49,
        },
    u'E3': {
        'col_and_row': u'E3',
        'row': 5,
        'col': 3,
        'well_id': 51,
        },
    u'E2': {
        'col_and_row': u'E2',
        'row': 5,
        'col': 2,
        'well_id': 50,
        },
    u'H10': {
        'col_and_row': u'H10',
        'row': 8,
        'col': 10,
        'well_id': 94,
        },
    u'H11': {
        'col_and_row': u'H11',
        'row': 8,
        'col': 11,
        'well_id': 95,
        },
    u'H12': {
        'col_and_row': u'H12',
        'row': 8,
        'col': 12,
        'well_id': 96,
        },
    u'F12': {
        'col_and_row': u'F12',
        'row': 6,
        'col': 12,
        'well_id': 72,
        },
    u'F10': {
        'col_and_row': u'F10',
        'row': 6,
        'col': 10,
        'well_id': 70,
        },
    u'F11': {
        'col_and_row': u'F11',
        'row': 6,
        'col': 11,
        'well_id': 71,
        },
    u'H8': {
        'col_and_row': u'H8',
        'row': 8,
        'col': 8,
        'well_id': 92,
        },
    u'H9': {
        'col_and_row': u'H9',
        'row': 8,
        'col': 9,
        'well_id': 93,
        },
    u'H2': {
        'col_and_row': u'H2',
        'row': 8,
        'col': 2,
        'well_id': 86,
        },
    u'H3': {
        'col_and_row': u'H3',
        'row': 8,
        'col': 3,
        'well_id': 87,
        },
    u'H1': {
        'col_and_row': u'H1',
        'row': 8,
        'col': 1,
        'well_id': 85,
        },
    u'H6': {
        'col_and_row': u'H6',
        'row': 8,
        'col': 6,
        'well_id': 90,
        },
    u'H7': {
        'col_and_row': u'H7',
        'row': 8,
        'col': 7,
        'well_id': 91,
        },
    u'H4': {
        'col_and_row': u'H4',
        'row': 8,
        'col': 4,
        'well_id': 88,
        },
    u'H5': {
        'col_and_row': u'H5',
        'row': 8,
        'col': 5,
        'well_id': 89,
        },
    u'D10': {
        'col_and_row': u'D10',
        'row': 4,
        'col': 10,
        'well_id': 46,
        },
    u'D11': {
        'col_and_row': u'D11',
        'row': 4,
        'col': 11,
        'well_id': 47,
        },
    u'D12': {
        'col_and_row': u'D12',
        'row': 4,
        'col': 12,
        'well_id': 48,
        },
    u'B12': {
        'col_and_row': u'B12',
        'row': 2,
        'col': 12,
        'well_id': 24,
        },
    u'B10': {
        'col_and_row': u'B10',
        'row': 2,
        'col': 10,
        'well_id': 22,
        },
    u'B11': {
        'col_and_row': u'B11',
        'row': 2,
        'col': 11,
        'well_id': 23,
        },
    u'C9': {
        'col_and_row': u'C9',
        'row': 3,
        'col': 9,
        'well_id': 33,
        },
    u'C8': {
        'col_and_row': u'C8',
        'row': 3,
        'col': 8,
        'well_id': 32,
        },
    u'C3': {
        'col_and_row': u'C3',
        'row': 3,
        'col': 3,
        'well_id': 27,
        },
    u'C2': {
        'col_and_row': u'C2',
        'row': 3,
        'col': 2,
        'well_id': 26,
        },
    u'C1': {
        'col_and_row': u'C1',
        'row': 3,
        'col': 1,
        'well_id': 25,
        },
    u'C7': {
        'col_and_row': u'C7',
        'row': 3,
        'col': 7,
        'well_id': 31,
        },
    u'C6': {
        'col_and_row': u'C6',
        'row': 3,
        'col': 6,
        'well_id': 30,
        },
    u'C5': {
        'col_and_row': u'C5',
        'row': 3,
        'col': 5,
        'well_id': 29,
        },
    u'C4': {
        'col_and_row': u'C4',
        'row': 3,
        'col': 4,
        'well_id': 28,
        },
    u'G12': {
        'col_and_row': u'G12',
        'row': 7,
        'col': 12,
        'well_id': 84,
        },
    u'G11': {
        'col_and_row': u'G11',
        'row': 7,
        'col': 11,
        'well_id': 83,
        },
    u'G10': {
        'col_and_row': u'G10',
        'row': 7,
        'col': 10,
        'well_id': 82,
        },
    u'F1': {
        'col_and_row': u'F1',
        'row': 6,
        'col': 1,
        'well_id': 61,
        },
    u'F2': {
        'col_and_row': u'F2',
        'row': 6,
        'col': 2,
        'well_id': 62,
        },
    u'F3': {
        'col_and_row': u'F3',
        'row': 6,
        'col': 3,
        'well_id': 63,
        },
    u'F4': {
        'col_and_row': u'F4',
        'row': 6,
        'col': 4,
        'well_id': 64,
        },
    u'F5': {
        'col_and_row': u'F5',
        'row': 6,
        'col': 5,
        'well_id': 65,
        },
    u'F6': {
        'col_and_row': u'F6',
        'row': 6,
        'col': 6,
        'well_id': 66,
        },
    u'F7': {
        'col_and_row': u'F7',
        'row': 6,
        'col': 7,
        'well_id': 67,
        },
    u'F8': {
        'col_and_row': u'F8',
        'row': 6,
        'col': 8,
        'well_id': 68,
        },
    u'F9': {
        'col_and_row': u'F9',
        'row': 6,
        'col': 9,
        'well_id': 69,
        },
    u'E11': {
        'col_and_row': u'E11',
        'row': 5,
        'col': 11,
        'well_id': 59,
        },
    u'E10': {
        'col_and_row': u'E10',
        'row': 5,
        'col': 10,
        'well_id': 58,
        },
    u'E12': {
        'col_and_row': u'E12',
        'row': 5,
        'col': 12,
        'well_id': 60,
        },
    u'C12': {
        'col_and_row': u'C12',
        'row': 3,
        'col': 12,
        'well_id': 36,
        },
    u'C11': {
        'col_and_row': u'C11',
        'row': 3,
        'col': 11,
        'well_id': 35,
        },
    u'C10': {
        'col_and_row': u'C10',
        'row': 3,
        'col': 10,
        'well_id': 34,
        },
    u'A11': {
        'col_and_row': u'A11',
        'row': 1,
        'col': 11,
        'well_id': 11,
        },
    u'A10': {
        'col_and_row': u'A10',
        'row': 1,
        'col': 10,
        'well_id': 10,
        },
    u'A12': {
        'col_and_row': u'A12',
        'row': 1,
        'col': 12,
        'well_id': 12,
        },
    u'A1': {
        'col_and_row': u'A1',
        'row': 1,
        'col': 1,
        'well_id': 1,
        },
    u'A3': {
        'col_and_row': u'A3',
        'row': 1,
        'col': 3,
        'well_id': 3,
        },
    u'A2': {
        'col_and_row': u'A2',
        'row': 1,
        'col': 2,
        'well_id': 2,
        },
    u'A5': {
        'col_and_row': u'A5',
        'row': 1,
        'col': 5,
        'well_id': 5,
        },
    u'A4': {
        'col_and_row': u'A4',
        'row': 1,
        'col': 4,
        'well_id': 4,
        },
    u'A7': {
        'col_and_row': u'A7',
        'row': 1,
        'col': 7,
        'well_id': 7,
        },
    u'A6': {
        'col_and_row': u'A6',
        'row': 1,
        'col': 6,
        'well_id': 6,
        },
    u'A9': {
        'col_and_row': u'A9',
        'row': 1,
        'col': 9,
        'well_id': 9,
        },
    u'A8': {
        'col_and_row': u'A8',
        'row': 1,
        'col': 8,
        'well_id': 8,
        },
    u'D8': {
        'col_and_row': u'D8',
        'row': 4,
        'col': 8,
        'well_id': 44,
        },
    u'D9': {
        'col_and_row': u'D9',
        'row': 4,
        'col': 9,
        'well_id': 45,
        },
    u'D6': {
        'col_and_row': u'D6',
        'row': 4,
        'col': 6,
        'well_id': 42,
        },
    u'D7': {
        'col_and_row': u'D7',
        'row': 4,
        'col': 7,
        'well_id': 43,
        },
    u'D4': {
        'col_and_row': u'D4',
        'row': 4,
        'col': 4,
        'well_id': 40,
        },
    u'D5': {
        'col_and_row': u'D5',
        'row': 4,
        'col': 5,
        'well_id': 41,
        },
    u'D2': {
        'col_and_row': u'D2',
        'row': 4,
        'col': 2,
        'well_id': 38,
        },
    u'D3': {
        'col_and_row': u'D3',
        'row': 4,
        'col': 3,
        'well_id': 39,
        },
    u'D1': {
        'col_and_row': u'D1',
        'row': 4,
        'col': 1,
        'well_id': 37,
        },
    }
def get_well_id_for_col_and_row(col_and_row):
    cell = col_and_row_to_cell_map[col_and_row]
    return cell["well_id"]


#for key, value in stuff.items():
#    print "KEY: ", key, " well_id: ", value["well_id"]

print "COL/ROW for well: ", get_col_and_row_for_well_id(2)

print "WELL ID for row/col: ", get_well_id_for_col_and_row("A2")




