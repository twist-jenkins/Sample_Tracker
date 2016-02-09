def maps_json():
    return {
        "transfer_maps": {
            1: {  # keyed to transfer_template_id in the database
                "description": "Source and destination are SAME TYPE."
                ,"source": {
                    "plate_count": 1
                }
                ,"destination": {
                    "plate_count": 1
                }
            }
            ,2: {  # keyed to transfer_template_id in the database
                "description": "Source and destination are SAME PLATE"
                ,"source": {
                    "plate_count": 1
                }
                ,"destination": {
                    "plate_count": 0
                }
            }
            ,13: {  # keyed to transfer_template_id in the database
                "description": "384 to 4x96"
                ,"source": {
                    "plate_count": 1
                    ,"well_count": 384
                    ,"plate_type_id": "SPTT_0006"
                }
                ,"destination":{
                    "plate_count": 4
                    ,"well_count": 96
                    ,"plate_type_id": "SPTT_0005"
                }
                ,"plate_well_to_well_maps": [ # index in plate_well_to_well_map array = source_plate_index
                    {   #key= sopurce plate well id
                        1: {"destination_plate_number": 1, "destination_well_id": 1}
                        ,2: {"destination_plate_number": 2, "destination_well_id": 1}
                        ,3: {"destination_plate_number": 1, "destination_well_id": 2}
                        ,4: {"destination_plate_number": 2, "destination_well_id": 2}
                        ,5: {"destination_plate_number": 1, "destination_well_id": 3}
                        ,6: {"destination_plate_number": 2, "destination_well_id": 3}
                        ,7: {"destination_plate_number": 1, "destination_well_id": 4}
                        ,8: {"destination_plate_number": 2, "destination_well_id": 4}
                        ,9: {"destination_plate_number": 1, "destination_well_id": 5}
                        ,10: {"destination_plate_number": 2, "destination_well_id": 5}
                        ,11: {"destination_plate_number": 1, "destination_well_id": 6}
                        ,12: {"destination_plate_number": 2, "destination_well_id": 6}
                        ,13: {"destination_plate_number": 1, "destination_well_id": 7}
                        ,14: {"destination_plate_number": 2, "destination_well_id": 7}
                        ,15: {"destination_plate_number": 1, "destination_well_id": 8}
                        ,16: {"destination_plate_number": 2, "destination_well_id": 8}
                        ,17: {"destination_plate_number": 1, "destination_well_id": 9}
                        ,18: {"destination_plate_number": 2, "destination_well_id": 9}
                        ,19: {"destination_plate_number": 1, "destination_well_id": 10}
                        ,20: {"destination_plate_number": 2, "destination_well_id": 10}
                        ,21: {"destination_plate_number": 1, "destination_well_id": 11}
                        ,22: {"destination_plate_number": 2, "destination_well_id": 11}
                        ,23: {"destination_plate_number": 1, "destination_well_id": 12}
                        ,24: {"destination_plate_number": 2, "destination_well_id": 12}
                        ,25: {"destination_plate_number": 3, "destination_well_id": 1}
                        ,26: {"destination_plate_number": 4, "destination_well_id": 1}
                        ,27: {"destination_plate_number": 3, "destination_well_id": 2}
                        ,28: {"destination_plate_number": 4, "destination_well_id": 2}
                        ,29: {"destination_plate_number": 3, "destination_well_id": 3}
                        ,30: {"destination_plate_number": 4, "destination_well_id": 3}
                        ,31: {"destination_plate_number": 3, "destination_well_id": 4}
                        ,32: {"destination_plate_number": 4, "destination_well_id": 4}
                        ,33: {"destination_plate_number": 3, "destination_well_id": 5}
                        ,34: {"destination_plate_number": 4, "destination_well_id": 5}
                        ,35: {"destination_plate_number": 3, "destination_well_id": 6}
                        ,36: {"destination_plate_number": 4, "destination_well_id": 6}
                        ,37: {"destination_plate_number": 3, "destination_well_id": 7}
                        ,38: {"destination_plate_number": 4, "destination_well_id": 7}
                        ,39: {"destination_plate_number": 3, "destination_well_id": 8}
                        ,40: {"destination_plate_number": 4, "destination_well_id": 8}
                        ,41: {"destination_plate_number": 3, "destination_well_id": 9}
                        ,42: {"destination_plate_number": 4, "destination_well_id": 9}
                        ,43: {"destination_plate_number": 3, "destination_well_id": 10}
                        ,44: {"destination_plate_number": 4, "destination_well_id": 10}
                        ,45: {"destination_plate_number": 3, "destination_well_id": 11}
                        ,46: {"destination_plate_number": 4, "destination_well_id": 11}
                        ,47: {"destination_plate_number": 3, "destination_well_id": 12}
                        ,48: {"destination_plate_number": 4, "destination_well_id": 12}
                        ,49: {"destination_plate_number": 1, "destination_well_id": 13}
                        ,50: {"destination_plate_number": 2, "destination_well_id": 13}
                        ,51: {"destination_plate_number": 1, "destination_well_id": 14}
                        ,52: {"destination_plate_number": 2, "destination_well_id": 14}
                        ,53: {"destination_plate_number": 1, "destination_well_id": 15}
                        ,54: {"destination_plate_number": 2, "destination_well_id": 15}
                        ,55: {"destination_plate_number": 1, "destination_well_id": 16}
                        ,56: {"destination_plate_number": 2, "destination_well_id": 16}
                        ,57: {"destination_plate_number": 1, "destination_well_id": 17}
                        ,58: {"destination_plate_number": 2, "destination_well_id": 17}
                        ,59: {"destination_plate_number": 1, "destination_well_id": 18}
                        ,60: {"destination_plate_number": 2, "destination_well_id": 18}
                        ,61: {"destination_plate_number": 1, "destination_well_id": 19}
                        ,62: {"destination_plate_number": 2, "destination_well_id": 19}
                        ,63: {"destination_plate_number": 1, "destination_well_id": 20}
                        ,64: {"destination_plate_number": 2, "destination_well_id": 20}
                        ,65: {"destination_plate_number": 1, "destination_well_id": 21}
                        ,66: {"destination_plate_number": 2, "destination_well_id": 21}
                        ,67: {"destination_plate_number": 1, "destination_well_id": 22}
                        ,68: {"destination_plate_number": 2, "destination_well_id": 22}
                        ,69: {"destination_plate_number": 1, "destination_well_id": 23}
                        ,70: {"destination_plate_number": 2, "destination_well_id": 23}
                        ,71: {"destination_plate_number": 1, "destination_well_id": 24}
                        ,72: {"destination_plate_number": 2, "destination_well_id": 24}
                        ,73: {"destination_plate_number": 3, "destination_well_id": 13}
                        ,74: {"destination_plate_number": 4, "destination_well_id": 13}
                        ,75: {"destination_plate_number": 3, "destination_well_id": 14}
                        ,76: {"destination_plate_number": 4, "destination_well_id": 14}
                        ,77: {"destination_plate_number": 3, "destination_well_id": 15}
                        ,78: {"destination_plate_number": 4, "destination_well_id": 15}
                        ,79: {"destination_plate_number": 3, "destination_well_id": 16}
                        ,80: {"destination_plate_number": 4, "destination_well_id": 16}
                        ,81: {"destination_plate_number": 3, "destination_well_id": 17}
                        ,82: {"destination_plate_number": 4, "destination_well_id": 17}
                        ,83: {"destination_plate_number": 3, "destination_well_id": 18}
                        ,84: {"destination_plate_number": 4, "destination_well_id": 18}
                        ,85: {"destination_plate_number": 3, "destination_well_id": 19}
                        ,86: {"destination_plate_number": 4, "destination_well_id": 19}
                        ,87: {"destination_plate_number": 3, "destination_well_id": 20}
                        ,88: {"destination_plate_number": 4, "destination_well_id": 20}
                        ,89: {"destination_plate_number": 3, "destination_well_id": 21}
                        ,90: {"destination_plate_number": 4, "destination_well_id": 21}
                        ,91: {"destination_plate_number": 3, "destination_well_id": 22}
                        ,92: {"destination_plate_number": 4, "destination_well_id": 22}
                        ,93: {"destination_plate_number": 3, "destination_well_id": 23}
                        ,94: {"destination_plate_number": 4, "destination_well_id": 23}
                        ,95: {"destination_plate_number": 3, "destination_well_id": 24}
                        ,96: {"destination_plate_number": 4, "destination_well_id": 24}
                        ,97: {"destination_plate_number": 1, "destination_well_id": 25}
                        ,98: {"destination_plate_number": 2, "destination_well_id": 25}
                        ,99: {"destination_plate_number": 1, "destination_well_id": 26}
                        ,100: {"destination_plate_number": 2, "destination_well_id": 26}
                        ,101: {"destination_plate_number": 1, "destination_well_id": 27}
                        ,102: {"destination_plate_number": 2, "destination_well_id": 27}
                        ,103: {"destination_plate_number": 1, "destination_well_id": 28}
                        ,104: {"destination_plate_number": 2, "destination_well_id": 28}
                        ,105: {"destination_plate_number": 1, "destination_well_id": 29}
                        ,106: {"destination_plate_number": 2, "destination_well_id": 29}
                        ,107: {"destination_plate_number": 1, "destination_well_id": 30}
                        ,108: {"destination_plate_number": 2, "destination_well_id": 30}
                        ,109: {"destination_plate_number": 1, "destination_well_id": 31}
                        ,110: {"destination_plate_number": 2, "destination_well_id": 31}
                        ,111: {"destination_plate_number": 1, "destination_well_id": 32}
                        ,112: {"destination_plate_number": 2, "destination_well_id": 32}
                        ,113: {"destination_plate_number": 1, "destination_well_id": 33}
                        ,114: {"destination_plate_number": 2, "destination_well_id": 33}
                        ,115: {"destination_plate_number": 1, "destination_well_id": 34}
                        ,116: {"destination_plate_number": 2, "destination_well_id": 34}
                        ,117: {"destination_plate_number": 1, "destination_well_id": 35}
                        ,118: {"destination_plate_number": 2, "destination_well_id": 35}
                        ,119: {"destination_plate_number": 1, "destination_well_id": 36}
                        ,120: {"destination_plate_number": 2, "destination_well_id": 36}
                        ,121: {"destination_plate_number": 3, "destination_well_id": 25}
                        ,122: {"destination_plate_number": 4, "destination_well_id": 25}
                        ,123: {"destination_plate_number": 3, "destination_well_id": 26}
                        ,124: {"destination_plate_number": 4, "destination_well_id": 26}
                        ,125: {"destination_plate_number": 3, "destination_well_id": 27}
                        ,126: {"destination_plate_number": 4, "destination_well_id": 27}
                        ,127: {"destination_plate_number": 3, "destination_well_id": 28}
                        ,128: {"destination_plate_number": 4, "destination_well_id": 28}
                        ,129: {"destination_plate_number": 3, "destination_well_id": 29}
                        ,130: {"destination_plate_number": 4, "destination_well_id": 29}
                        ,131: {"destination_plate_number": 3, "destination_well_id": 30}
                        ,132: {"destination_plate_number": 4, "destination_well_id": 30}
                        ,133: {"destination_plate_number": 3, "destination_well_id": 31}
                        ,134: {"destination_plate_number": 4, "destination_well_id": 31}
                        ,135: {"destination_plate_number": 3, "destination_well_id": 32}
                        ,136: {"destination_plate_number": 4, "destination_well_id": 32}
                        ,137: {"destination_plate_number": 3, "destination_well_id": 33}
                        ,138: {"destination_plate_number": 4, "destination_well_id": 33}
                        ,139: {"destination_plate_number": 3, "destination_well_id": 34}
                        ,140: {"destination_plate_number": 4, "destination_well_id": 34}
                        ,141: {"destination_plate_number": 3, "destination_well_id": 35}
                        ,142: {"destination_plate_number": 4, "destination_well_id": 35}
                        ,143: {"destination_plate_number": 3, "destination_well_id": 36}
                        ,144: {"destination_plate_number": 4, "destination_well_id": 36}
                        ,145: {"destination_plate_number": 1, "destination_well_id": 37}
                        ,146: {"destination_plate_number": 2, "destination_well_id": 37}
                        ,147: {"destination_plate_number": 1, "destination_well_id": 38}
                        ,148: {"destination_plate_number": 2, "destination_well_id": 38}
                        ,149: {"destination_plate_number": 1, "destination_well_id": 39}
                        ,150: {"destination_plate_number": 2, "destination_well_id": 39}
                        ,151: {"destination_plate_number": 1, "destination_well_id": 40}
                        ,152: {"destination_plate_number": 2, "destination_well_id": 40}
                        ,153: {"destination_plate_number": 1, "destination_well_id": 41}
                        ,154: {"destination_plate_number": 2, "destination_well_id": 41}
                        ,155: {"destination_plate_number": 1, "destination_well_id": 42}
                        ,156: {"destination_plate_number": 2, "destination_well_id": 42}
                        ,157: {"destination_plate_number": 1, "destination_well_id": 43}
                        ,158: {"destination_plate_number": 2, "destination_well_id": 43}
                        ,159: {"destination_plate_number": 1, "destination_well_id": 44}
                        ,160: {"destination_plate_number": 2, "destination_well_id": 44}
                        ,161: {"destination_plate_number": 1, "destination_well_id": 45}
                        ,162: {"destination_plate_number": 2, "destination_well_id": 45}
                        ,163: {"destination_plate_number": 1, "destination_well_id": 46}
                        ,164: {"destination_plate_number": 2, "destination_well_id": 46}
                        ,165: {"destination_plate_number": 1, "destination_well_id": 47}
                        ,166: {"destination_plate_number": 2, "destination_well_id": 47}
                        ,167: {"destination_plate_number": 1, "destination_well_id": 48}
                        ,168: {"destination_plate_number": 2, "destination_well_id": 48}
                        ,169: {"destination_plate_number": 3, "destination_well_id": 37}
                        ,170: {"destination_plate_number": 4, "destination_well_id": 37}
                        ,171: {"destination_plate_number": 3, "destination_well_id": 38}
                        ,172: {"destination_plate_number": 4, "destination_well_id": 38}
                        ,173: {"destination_plate_number": 3, "destination_well_id": 39}
                        ,174: {"destination_plate_number": 4, "destination_well_id": 39}
                        ,175: {"destination_plate_number": 3, "destination_well_id": 40}
                        ,176: {"destination_plate_number": 4, "destination_well_id": 40}
                        ,177: {"destination_plate_number": 3, "destination_well_id": 41}
                        ,178: {"destination_plate_number": 4, "destination_well_id": 41}
                        ,179: {"destination_plate_number": 3, "destination_well_id": 42}
                        ,180: {"destination_plate_number": 4, "destination_well_id": 42}
                        ,181: {"destination_plate_number": 3, "destination_well_id": 43}
                        ,182: {"destination_plate_number": 4, "destination_well_id": 43}
                        ,183: {"destination_plate_number": 3, "destination_well_id": 44}
                        ,184: {"destination_plate_number": 4, "destination_well_id": 44}
                        ,185: {"destination_plate_number": 3, "destination_well_id": 45}
                        ,186: {"destination_plate_number": 4, "destination_well_id": 45}
                        ,187: {"destination_plate_number": 3, "destination_well_id": 46}
                        ,188: {"destination_plate_number": 4, "destination_well_id": 46}
                        ,189: {"destination_plate_number": 3, "destination_well_id": 47}
                        ,190: {"destination_plate_number": 4, "destination_well_id": 47}
                        ,191: {"destination_plate_number": 3, "destination_well_id": 48}
                        ,192: {"destination_plate_number": 4, "destination_well_id": 48}
                        ,193: {"destination_plate_number": 1, "destination_well_id": 49}
                        ,194: {"destination_plate_number": 2, "destination_well_id": 49}
                        ,195: {"destination_plate_number": 1, "destination_well_id": 50}
                        ,196: {"destination_plate_number": 2, "destination_well_id": 50}
                        ,197: {"destination_plate_number": 1, "destination_well_id": 51}
                        ,198: {"destination_plate_number": 2, "destination_well_id": 51}
                        ,199: {"destination_plate_number": 1, "destination_well_id": 52}
                        ,200: {"destination_plate_number": 2, "destination_well_id": 52}
                        ,201: {"destination_plate_number": 1, "destination_well_id": 53}
                        ,202: {"destination_plate_number": 2, "destination_well_id": 53}
                        ,203: {"destination_plate_number": 1, "destination_well_id": 54}
                        ,204: {"destination_plate_number": 2, "destination_well_id": 54}
                        ,205: {"destination_plate_number": 1, "destination_well_id": 55}
                        ,206: {"destination_plate_number": 2, "destination_well_id": 55}
                        ,207: {"destination_plate_number": 1, "destination_well_id": 56}
                        ,208: {"destination_plate_number": 2, "destination_well_id": 56}
                        ,209: {"destination_plate_number": 1, "destination_well_id": 57}
                        ,210: {"destination_plate_number": 2, "destination_well_id": 57}
                        ,211: {"destination_plate_number": 1, "destination_well_id": 58}
                        ,212: {"destination_plate_number": 2, "destination_well_id": 58}
                        ,213: {"destination_plate_number": 1, "destination_well_id": 59}
                        ,214: {"destination_plate_number": 2, "destination_well_id": 59}
                        ,215: {"destination_plate_number": 1, "destination_well_id": 60}
                        ,216: {"destination_plate_number": 2, "destination_well_id": 60}
                        ,217: {"destination_plate_number": 3, "destination_well_id": 49}
                        ,218: {"destination_plate_number": 4, "destination_well_id": 49}
                        ,219: {"destination_plate_number": 3, "destination_well_id": 50}
                        ,220: {"destination_plate_number": 4, "destination_well_id": 50}
                        ,221: {"destination_plate_number": 3, "destination_well_id": 51}
                        ,222: {"destination_plate_number": 4, "destination_well_id": 51}
                        ,223: {"destination_plate_number": 3, "destination_well_id": 52}
                        ,224: {"destination_plate_number": 4, "destination_well_id": 52}
                        ,225: {"destination_plate_number": 3, "destination_well_id": 53}
                        ,226: {"destination_plate_number": 4, "destination_well_id": 53}
                        ,227: {"destination_plate_number": 3, "destination_well_id": 54}
                        ,228: {"destination_plate_number": 4, "destination_well_id": 54}
                        ,229: {"destination_plate_number": 3, "destination_well_id": 55}
                        ,230: {"destination_plate_number": 4, "destination_well_id": 55}
                        ,231: {"destination_plate_number": 3, "destination_well_id": 56}
                        ,232: {"destination_plate_number": 4, "destination_well_id": 56}
                        ,233: {"destination_plate_number": 3, "destination_well_id": 57}
                        ,234: {"destination_plate_number": 4, "destination_well_id": 57}
                        ,235: {"destination_plate_number": 3, "destination_well_id": 58}
                        ,236: {"destination_plate_number": 4, "destination_well_id": 58}
                        ,237: {"destination_plate_number": 3, "destination_well_id": 59}
                        ,238: {"destination_plate_number": 4, "destination_well_id": 59}
                        ,239: {"destination_plate_number": 3, "destination_well_id": 60}
                        ,240: {"destination_plate_number": 4, "destination_well_id": 60}
                        ,241: {"destination_plate_number": 1, "destination_well_id": 61}
                        ,242: {"destination_plate_number": 2, "destination_well_id": 61}
                        ,243: {"destination_plate_number": 1, "destination_well_id": 62}
                        ,244: {"destination_plate_number": 2, "destination_well_id": 62}
                        ,245: {"destination_plate_number": 1, "destination_well_id": 63}
                        ,246: {"destination_plate_number": 2, "destination_well_id": 63}
                        ,247: {"destination_plate_number": 1, "destination_well_id": 64}
                        ,248: {"destination_plate_number": 2, "destination_well_id": 64}
                        ,249: {"destination_plate_number": 1, "destination_well_id": 65}
                        ,250: {"destination_plate_number": 2, "destination_well_id": 65}
                        ,251: {"destination_plate_number": 1, "destination_well_id": 66}
                        ,252: {"destination_plate_number": 2, "destination_well_id": 66}
                        ,253: {"destination_plate_number": 1, "destination_well_id": 67}
                        ,254: {"destination_plate_number": 2, "destination_well_id": 67}
                        ,255: {"destination_plate_number": 1, "destination_well_id": 68}
                        ,256: {"destination_plate_number": 2, "destination_well_id": 68}
                        ,257: {"destination_plate_number": 1, "destination_well_id": 69}
                        ,258: {"destination_plate_number": 2, "destination_well_id": 69}
                        ,259: {"destination_plate_number": 1, "destination_well_id": 70}
                        ,260: {"destination_plate_number": 2, "destination_well_id": 70}
                        ,261: {"destination_plate_number": 1, "destination_well_id": 71}
                        ,262: {"destination_plate_number": 2, "destination_well_id": 71}
                        ,263: {"destination_plate_number": 1, "destination_well_id": 72}
                        ,264: {"destination_plate_number": 2, "destination_well_id": 72}
                        ,265: {"destination_plate_number": 3, "destination_well_id": 61}
                        ,266: {"destination_plate_number": 4, "destination_well_id": 61}
                        ,267: {"destination_plate_number": 3, "destination_well_id": 62}
                        ,268: {"destination_plate_number": 4, "destination_well_id": 62}
                        ,269: {"destination_plate_number": 3, "destination_well_id": 63}
                        ,270: {"destination_plate_number": 4, "destination_well_id": 63}
                        ,271: {"destination_plate_number": 3, "destination_well_id": 64}
                        ,272: {"destination_plate_number": 4, "destination_well_id": 64}
                        ,273: {"destination_plate_number": 3, "destination_well_id": 65}
                        ,274: {"destination_plate_number": 4, "destination_well_id": 65}
                        ,275: {"destination_plate_number": 3, "destination_well_id": 66}
                        ,276: {"destination_plate_number": 4, "destination_well_id": 66}
                        ,277: {"destination_plate_number": 3, "destination_well_id": 67}
                        ,278: {"destination_plate_number": 4, "destination_well_id": 67}
                        ,279: {"destination_plate_number": 3, "destination_well_id": 68}
                        ,280: {"destination_plate_number": 4, "destination_well_id": 68}
                        ,281: {"destination_plate_number": 3, "destination_well_id": 69}
                        ,282: {"destination_plate_number": 4, "destination_well_id": 69}
                        ,283: {"destination_plate_number": 3, "destination_well_id": 70}
                        ,284: {"destination_plate_number": 4, "destination_well_id": 70}
                        ,285: {"destination_plate_number": 3, "destination_well_id": 71}
                        ,286: {"destination_plate_number": 4, "destination_well_id": 71}
                        ,287: {"destination_plate_number": 3, "destination_well_id": 72}
                        ,288: {"destination_plate_number": 4, "destination_well_id": 72}
                        ,289: {"destination_plate_number": 1, "destination_well_id": 73}
                        ,290: {"destination_plate_number": 2, "destination_well_id": 73}
                        ,291: {"destination_plate_number": 1, "destination_well_id": 74}
                        ,292: {"destination_plate_number": 2, "destination_well_id": 74}
                        ,293: {"destination_plate_number": 1, "destination_well_id": 75}
                        ,294: {"destination_plate_number": 2, "destination_well_id": 75}
                        ,295: {"destination_plate_number": 1, "destination_well_id": 76}
                        ,296: {"destination_plate_number": 2, "destination_well_id": 76}
                        ,297: {"destination_plate_number": 1, "destination_well_id": 77}
                        ,298: {"destination_plate_number": 2, "destination_well_id": 77}
                        ,299: {"destination_plate_number": 1, "destination_well_id": 78}
                        ,300: {"destination_plate_number": 2, "destination_well_id": 78}
                        ,301: {"destination_plate_number": 1, "destination_well_id": 79}
                        ,302: {"destination_plate_number": 2, "destination_well_id": 79}
                        ,303: {"destination_plate_number": 1, "destination_well_id": 80}
                        ,304: {"destination_plate_number": 2, "destination_well_id": 80}
                        ,305: {"destination_plate_number": 1, "destination_well_id": 81}
                        ,306: {"destination_plate_number": 2, "destination_well_id": 81}
                        ,307: {"destination_plate_number": 1, "destination_well_id": 82}
                        ,308: {"destination_plate_number": 2, "destination_well_id": 82}
                        ,309: {"destination_plate_number": 1, "destination_well_id": 83}
                        ,310: {"destination_plate_number": 2, "destination_well_id": 83}
                        ,311: {"destination_plate_number": 1, "destination_well_id": 84}
                        ,312: {"destination_plate_number": 2, "destination_well_id": 84}
                        ,313: {"destination_plate_number": 3, "destination_well_id": 73}
                        ,314: {"destination_plate_number": 4, "destination_well_id": 73}
                        ,315: {"destination_plate_number": 3, "destination_well_id": 74}
                        ,316: {"destination_plate_number": 4, "destination_well_id": 74}
                        ,317: {"destination_plate_number": 3, "destination_well_id": 75}
                        ,318: {"destination_plate_number": 4, "destination_well_id": 75}
                        ,319: {"destination_plate_number": 3, "destination_well_id": 76}
                        ,320: {"destination_plate_number": 4, "destination_well_id": 76}
                        ,321: {"destination_plate_number": 3, "destination_well_id": 77}
                        ,322: {"destination_plate_number": 4, "destination_well_id": 77}
                        ,323: {"destination_plate_number": 3, "destination_well_id": 78}
                        ,324: {"destination_plate_number": 4, "destination_well_id": 78}
                        ,325: {"destination_plate_number": 3, "destination_well_id": 79}
                        ,326: {"destination_plate_number": 4, "destination_well_id": 79}
                        ,327: {"destination_plate_number": 3, "destination_well_id": 80}
                        ,328: {"destination_plate_number": 4, "destination_well_id": 80}
                        ,329: {"destination_plate_number": 3, "destination_well_id": 81}
                        ,330: {"destination_plate_number": 4, "destination_well_id": 81}
                        ,331: {"destination_plate_number": 3, "destination_well_id": 82}
                        ,332: {"destination_plate_number": 4, "destination_well_id": 82}
                        ,333: {"destination_plate_number": 3, "destination_well_id": 83}
                        ,334: {"destination_plate_number": 4, "destination_well_id": 83}
                        ,335: {"destination_plate_number": 3, "destination_well_id": 84}
                        ,336: {"destination_plate_number": 4, "destination_well_id": 84}
                        ,337: {"destination_plate_number": 1, "destination_well_id": 85}
                        ,338: {"destination_plate_number": 2, "destination_well_id": 85}
                        ,339: {"destination_plate_number": 1, "destination_well_id": 86}
                        ,340: {"destination_plate_number": 2, "destination_well_id": 86}
                        ,341: {"destination_plate_number": 1, "destination_well_id": 87}
                        ,342: {"destination_plate_number": 2, "destination_well_id": 87}
                        ,343: {"destination_plate_number": 1, "destination_well_id": 88}
                        ,344: {"destination_plate_number": 2, "destination_well_id": 88}
                        ,345: {"destination_plate_number": 1, "destination_well_id": 89}
                        ,346: {"destination_plate_number": 2, "destination_well_id": 89}
                        ,347: {"destination_plate_number": 1, "destination_well_id": 90}
                        ,348: {"destination_plate_number": 2, "destination_well_id": 90}
                        ,349: {"destination_plate_number": 1, "destination_well_id": 91}
                        ,350: {"destination_plate_number": 2, "destination_well_id": 91}
                        ,351: {"destination_plate_number": 1, "destination_well_id": 92}
                        ,352: {"destination_plate_number": 2, "destination_well_id": 92}
                        ,353: {"destination_plate_number": 1, "destination_well_id": 93}
                        ,354: {"destination_plate_number": 2, "destination_well_id": 93}
                        ,355: {"destination_plate_number": 1, "destination_well_id": 94}
                        ,356: {"destination_plate_number": 2, "destination_well_id": 94}
                        ,357: {"destination_plate_number": 1, "destination_well_id": 95}
                        ,358: {"destination_plate_number": 2, "destination_well_id": 95}
                        ,359: {"destination_plate_number": 1, "destination_well_id": 96}
                        ,360: {"destination_plate_number": 2, "destination_well_id": 96}
                        ,361: {"destination_plate_number": 3, "destination_well_id": 85}
                        ,362: {"destination_plate_number": 4, "destination_well_id": 85}
                        ,363: {"destination_plate_number": 3, "destination_well_id": 86}
                        ,364: {"destination_plate_number": 4, "destination_well_id": 86}
                        ,365: {"destination_plate_number": 3, "destination_well_id": 87}
                        ,366: {"destination_plate_number": 4, "destination_well_id": 87}
                        ,367: {"destination_plate_number": 3, "destination_well_id": 88}
                        ,368: {"destination_plate_number": 4, "destination_well_id": 88}
                        ,369: {"destination_plate_number": 3, "destination_well_id": 89}
                        ,370: {"destination_plate_number": 4, "destination_well_id": 89}
                        ,371: {"destination_plate_number": 3, "destination_well_id": 90}
                        ,372: {"destination_plate_number": 4, "destination_well_id": 90}
                        ,373: {"destination_plate_number": 3, "destination_well_id": 91}
                        ,374: {"destination_plate_number": 4, "destination_well_id": 91}
                        ,375: {"destination_plate_number": 3, "destination_well_id": 92}
                        ,376: {"destination_plate_number": 4, "destination_well_id": 92}
                        ,377: {"destination_plate_number": 3, "destination_well_id": 93}
                        ,378: {"destination_plate_number": 4, "destination_well_id": 93}
                        ,379: {"destination_plate_number": 3, "destination_well_id": 94}
                        ,380: {"destination_plate_number": 4, "destination_well_id": 94}
                        ,381: {"destination_plate_number": 3, "destination_well_id": 95}
                        ,382: {"destination_plate_number": 4, "destination_well_id": 95}
                        ,383: {"destination_plate_number": 3, "destination_well_id": 96}
                        ,384: {"destination_plate_number": 4, "destination_well_id": 96}
                    }
                ]
            }
            ,14: {  # keyed to transfer_template_id in the database
                "description": "96 to 2x48"
                ,"source": {
                    "plate_count": 1
                    ,"well_count": 96
                    ,"plate_type_id": "SPTT_0005"
                }
                ,"destination":{
                    "plate_count": 2
                    ,"well_count": 48
                    ,"plate_type_id": "SPTT_0004"
                }
                ,"plate_well_to_well_maps": [ # array of source plates
                    {   # index in plate_well_to_well_map array = source_plate_index
                        1: {"destination_plate_number": 1 ,"destination_well_id": 1}
                        ,2: {"destination_plate_number": 1 ,"destination_well_id": 2}
                        ,3: {"destination_plate_number": 1 ,"destination_well_id": 3}
                        ,4: {"destination_plate_number": 1 ,"destination_well_id": 4}
                        ,5: {"destination_plate_number": 1 ,"destination_well_id": 5}
                        ,6: {"destination_plate_number": 1 ,"destination_well_id": 6}
                        ,7: {"destination_plate_number": 2 ,"destination_well_id": 1}
                        ,8: {"destination_plate_number": 2 ,"destination_well_id": 2}
                        ,9: {"destination_plate_number": 2 ,"destination_well_id": 3}
                        ,10: {"destination_plate_number": 2 ,"destination_well_id": 4}
                        ,11: {"destination_plate_number": 2 ,"destination_well_id": 5}
                        ,12: {"destination_plate_number": 2 ,"destination_well_id": 6}
                        ,13: {"destination_plate_number": 1 ,"destination_well_id": 7}
                        ,14: {"destination_plate_number": 1 ,"destination_well_id": 8}
                        ,15: {"destination_plate_number": 1 ,"destination_well_id": 9}
                        ,16: {"destination_plate_number": 1 ,"destination_well_id": 10}
                        ,17: {"destination_plate_number": 1 ,"destination_well_id": 11}
                        ,18: {"destination_plate_number": 1 ,"destination_well_id": 12}
                        ,19: {"destination_plate_number": 2 ,"destination_well_id": 7}
                        ,20: {"destination_plate_number": 2 ,"destination_well_id": 8}
                        ,21: {"destination_plate_number": 2 ,"destination_well_id": 9}
                        ,22: {"destination_plate_number": 2 ,"destination_well_id": 10}
                        ,23: {"destination_plate_number": 2 ,"destination_well_id": 11}
                        ,24: {"destination_plate_number": 2 ,"destination_well_id": 12}
                        ,25: {"destination_plate_number": 1 ,"destination_well_id": 13}
                        ,26: {"destination_plate_number": 1 ,"destination_well_id": 14}
                        ,27: {"destination_plate_number": 1 ,"destination_well_id": 15}
                        ,28: {"destination_plate_number": 1 ,"destination_well_id": 16}
                        ,29: {"destination_plate_number": 1 ,"destination_well_id": 17}
                        ,30: {"destination_plate_number": 1 ,"destination_well_id": 18}
                        ,31: {"destination_plate_number": 2 ,"destination_well_id": 13}
                        ,32: {"destination_plate_number": 2 ,"destination_well_id": 14}
                        ,33: {"destination_plate_number": 2 ,"destination_well_id": 15}
                        ,34: {"destination_plate_number": 2 ,"destination_well_id": 16}
                        ,35: {"destination_plate_number": 2 ,"destination_well_id": 17}
                        ,36: {"destination_plate_number": 2 ,"destination_well_id": 18}
                        ,37: {"destination_plate_number": 1 ,"destination_well_id": 19}
                        ,38: {"destination_plate_number": 1 ,"destination_well_id": 20}
                        ,39: {"destination_plate_number": 1 ,"destination_well_id": 21}
                        ,40: {"destination_plate_number": 1 ,"destination_well_id": 22}
                        ,41: {"destination_plate_number": 1 ,"destination_well_id": 23}
                        ,42: {"destination_plate_number": 1 ,"destination_well_id": 24}
                        ,43: {"destination_plate_number": 2 ,"destination_well_id": 19}
                        ,44: {"destination_plate_number": 2 ,"destination_well_id": 20}
                        ,45: {"destination_plate_number": 2 ,"destination_well_id": 21}
                        ,46: {"destination_plate_number": 2 ,"destination_well_id": 22}
                        ,47: {"destination_plate_number": 2 ,"destination_well_id": 23}
                        ,48: {"destination_plate_number": 2 ,"destination_well_id": 24}
                        ,49: {"destination_plate_number": 1 ,"destination_well_id": 25}
                        ,50: {"destination_plate_number": 1 ,"destination_well_id": 26}
                        ,51: {"destination_plate_number": 1 ,"destination_well_id": 27}
                        ,52: {"destination_plate_number": 1 ,"destination_well_id": 28}
                        ,53: {"destination_plate_number": 1 ,"destination_well_id": 29}
                        ,54: {"destination_plate_number": 1 ,"destination_well_id": 30}
                        ,55: {"destination_plate_number": 2 ,"destination_well_id": 25}
                        ,56: {"destination_plate_number": 2 ,"destination_well_id": 26}
                        ,57: {"destination_plate_number": 2 ,"destination_well_id": 27}
                        ,58: {"destination_plate_number": 2 ,"destination_well_id": 28}
                        ,59: {"destination_plate_number": 2 ,"destination_well_id": 29}
                        ,60: {"destination_plate_number": 2 ,"destination_well_id": 30}
                        ,61: {"destination_plate_number": 1 ,"destination_well_id": 31}
                        ,62: {"destination_plate_number": 1 ,"destination_well_id": 32}
                        ,63: {"destination_plate_number": 1 ,"destination_well_id": 33}
                        ,64: {"destination_plate_number": 1 ,"destination_well_id": 34}
                        ,65: {"destination_plate_number": 1 ,"destination_well_id": 35}
                        ,66: {"destination_plate_number": 1 ,"destination_well_id": 36}
                        ,67: {"destination_plate_number": 2 ,"destination_well_id": 31}
                        ,68: {"destination_plate_number": 2 ,"destination_well_id": 32}
                        ,69: {"destination_plate_number": 2 ,"destination_well_id": 33}
                        ,70: {"destination_plate_number": 2 ,"destination_well_id": 34}
                        ,71: {"destination_plate_number": 2 ,"destination_well_id": 35}
                        ,72: {"destination_plate_number": 2 ,"destination_well_id": 36}
                        ,73: {"destination_plate_number": 1 ,"destination_well_id": 37}
                        ,74: {"destination_plate_number": 1 ,"destination_well_id": 38}
                        ,75: {"destination_plate_number": 1 ,"destination_well_id": 39}
                        ,76: {"destination_plate_number": 1 ,"destination_well_id": 40}
                        ,77: {"destination_plate_number": 1 ,"destination_well_id": 41}
                        ,78: {"destination_plate_number": 1 ,"destination_well_id": 42}
                        ,79: {"destination_plate_number": 2 ,"destination_well_id": 37}
                        ,80: {"destination_plate_number": 2 ,"destination_well_id": 38}
                        ,81: {"destination_plate_number": 2 ,"destination_well_id": 39}
                        ,82: {"destination_plate_number": 2 ,"destination_well_id": 40}
                        ,83: {"destination_plate_number": 2 ,"destination_well_id": 41}
                        ,84: {"destination_plate_number": 2 ,"destination_well_id": 42}
                        ,85: {"destination_plate_number": 1 ,"destination_well_id": 43}
                        ,86: {"destination_plate_number": 1 ,"destination_well_id": 44}
                        ,87: {"destination_plate_number": 1 ,"destination_well_id": 45}
                        ,88: {"destination_plate_number": 1 ,"destination_well_id": 46}
                        ,89: {"destination_plate_number": 1 ,"destination_well_id": 47}
                        ,90: {"destination_plate_number": 1 ,"destination_well_id": 48}
                        ,91: {"destination_plate_number": 2 ,"destination_well_id": 43}
                        ,92: {"destination_plate_number": 2 ,"destination_well_id": 44}
                        ,93: {"destination_plate_number": 2 ,"destination_well_id": 45}
                        ,94: {"destination_plate_number": 2 ,"destination_well_id": 46}
                        ,95: {"destination_plate_number": 2 ,"destination_well_id": 47}
                        ,96: {"destination_plate_number": 2 ,"destination_well_id": 48}
                    }
                ]
            }
            ,18: {  # keyed to transfer_template_id in the database
                "description": "4x96 to 384"
                ,"source": {
                    "plate_count": 4
                    ,"well_count": 96
                    ,"plate_type_id": "SPTT_0005"
                }
                ,"destination":{
                    "plate_count": 1
                    ,"well_count": 384
                    ,"plate_type_id": "SPTT_0006"
                }
                ,"plate_well_to_well_maps": [
                    {
                        1:{"destination_plate_number":1,"destination_well_id":1}
                        ,2:{"destination_plate_number":1,"destination_well_id":3}
                        ,3:{"destination_plate_number":1,"destination_well_id":5}
                        ,4:{"destination_plate_number":1,"destination_well_id":7}
                        ,5:{"destination_plate_number":1,"destination_well_id":9}
                        ,6:{"destination_plate_number":1,"destination_well_id":11}
                        ,7:{"destination_plate_number":1,"destination_well_id":13}
                        ,8:{"destination_plate_number":1,"destination_well_id":15}
                        ,9:{"destination_plate_number":1,"destination_well_id":17}
                        ,10:{"destination_plate_number":1,"destination_well_id":19}
                        ,11:{"destination_plate_number":1,"destination_well_id":21}
                        ,12:{"destination_plate_number":1,"destination_well_id":23}
                        ,13:{"destination_plate_number":1,"destination_well_id":49}
                        ,14:{"destination_plate_number":1,"destination_well_id":51}
                        ,15:{"destination_plate_number":1,"destination_well_id":53}
                        ,16:{"destination_plate_number":1,"destination_well_id":55}
                        ,17:{"destination_plate_number":1,"destination_well_id":57}
                        ,18:{"destination_plate_number":1,"destination_well_id":59}
                        ,19:{"destination_plate_number":1,"destination_well_id":61}
                        ,20:{"destination_plate_number":1,"destination_well_id":63}
                        ,21:{"destination_plate_number":1,"destination_well_id":65}
                        ,22:{"destination_plate_number":1,"destination_well_id":67}
                        ,23:{"destination_plate_number":1,"destination_well_id":69}
                        ,24:{"destination_plate_number":1,"destination_well_id":71}
                        ,25:{"destination_plate_number":1,"destination_well_id":97}
                        ,26:{"destination_plate_number":1,"destination_well_id":99}
                        ,27:{"destination_plate_number":1,"destination_well_id":101}
                        ,28:{"destination_plate_number":1,"destination_well_id":103}
                        ,29:{"destination_plate_number":1,"destination_well_id":105}
                        ,30:{"destination_plate_number":1,"destination_well_id":107}
                        ,31:{"destination_plate_number":1,"destination_well_id":109}
                        ,32:{"destination_plate_number":1,"destination_well_id":111}
                        ,33:{"destination_plate_number":1,"destination_well_id":113}
                        ,34:{"destination_plate_number":1,"destination_well_id":115}
                        ,35:{"destination_plate_number":1,"destination_well_id":117}
                        ,36:{"destination_plate_number":1,"destination_well_id":119}
                        ,37:{"destination_plate_number":1,"destination_well_id":145}
                        ,38:{"destination_plate_number":1,"destination_well_id":147}
                        ,39:{"destination_plate_number":1,"destination_well_id":149}
                        ,40:{"destination_plate_number":1,"destination_well_id":151}
                        ,41:{"destination_plate_number":1,"destination_well_id":153}
                        ,42:{"destination_plate_number":1,"destination_well_id":155}
                        ,43:{"destination_plate_number":1,"destination_well_id":157}
                        ,44:{"destination_plate_number":1,"destination_well_id":159}
                        ,45:{"destination_plate_number":1,"destination_well_id":161}
                        ,46:{"destination_plate_number":1,"destination_well_id":163}
                        ,47:{"destination_plate_number":1,"destination_well_id":165}
                        ,48:{"destination_plate_number":1,"destination_well_id":167}
                        ,49:{"destination_plate_number":1,"destination_well_id":193}
                        ,50:{"destination_plate_number":1,"destination_well_id":195}
                        ,51:{"destination_plate_number":1,"destination_well_id":197}
                        ,52:{"destination_plate_number":1,"destination_well_id":199}
                        ,53:{"destination_plate_number":1,"destination_well_id":201}
                        ,54:{"destination_plate_number":1,"destination_well_id":203}
                        ,55:{"destination_plate_number":1,"destination_well_id":205}
                        ,56:{"destination_plate_number":1,"destination_well_id":207}
                        ,57:{"destination_plate_number":1,"destination_well_id":209}
                        ,58:{"destination_plate_number":1,"destination_well_id":211}
                        ,59:{"destination_plate_number":1,"destination_well_id":213}
                        ,60:{"destination_plate_number":1,"destination_well_id":215}
                        ,61:{"destination_plate_number":1,"destination_well_id":241}
                        ,62:{"destination_plate_number":1,"destination_well_id":243}
                        ,63:{"destination_plate_number":1,"destination_well_id":245}
                        ,64:{"destination_plate_number":1,"destination_well_id":247}
                        ,65:{"destination_plate_number":1,"destination_well_id":249}
                        ,66:{"destination_plate_number":1,"destination_well_id":251}
                        ,67:{"destination_plate_number":1,"destination_well_id":253}
                        ,68:{"destination_plate_number":1,"destination_well_id":255}
                        ,69:{"destination_plate_number":1,"destination_well_id":257}
                        ,70:{"destination_plate_number":1,"destination_well_id":259}
                        ,71:{"destination_plate_number":1,"destination_well_id":261}
                        ,72:{"destination_plate_number":1,"destination_well_id":263}
                        ,73:{"destination_plate_number":1,"destination_well_id":289}
                        ,74:{"destination_plate_number":1,"destination_well_id":291}
                        ,75:{"destination_plate_number":1,"destination_well_id":293}
                        ,76:{"destination_plate_number":1,"destination_well_id":295}
                        ,77:{"destination_plate_number":1,"destination_well_id":297}
                        ,78:{"destination_plate_number":1,"destination_well_id":299}
                        ,79:{"destination_plate_number":1,"destination_well_id":301}
                        ,80:{"destination_plate_number":1,"destination_well_id":303}
                        ,81:{"destination_plate_number":1,"destination_well_id":305}
                        ,82:{"destination_plate_number":1,"destination_well_id":307}
                        ,83:{"destination_plate_number":1,"destination_well_id":309}
                        ,84:{"destination_plate_number":1,"destination_well_id":311}
                        ,85:{"destination_plate_number":1,"destination_well_id":337}
                        ,86:{"destination_plate_number":1,"destination_well_id":339}
                        ,87:{"destination_plate_number":1,"destination_well_id":341}
                        ,88:{"destination_plate_number":1,"destination_well_id":343}
                        ,89:{"destination_plate_number":1,"destination_well_id":345}
                        ,90:{"destination_plate_number":1,"destination_well_id":347}
                        ,91:{"destination_plate_number":1,"destination_well_id":349}
                        ,92:{"destination_plate_number":1,"destination_well_id":351}
                        ,93:{"destination_plate_number":1,"destination_well_id":353}
                        ,94:{"destination_plate_number":1,"destination_well_id":355}
                        ,95:{"destination_plate_number":1,"destination_well_id":357}
                        ,96:{"destination_plate_number":1,"destination_well_id":359}
                    }
                    ,{
                        1:{"destination_plate_number":1,"destination_well_id":2}
                        ,2:{"destination_plate_number":1,"destination_well_id":4}
                        ,3:{"destination_plate_number":1,"destination_well_id":6}
                        ,4:{"destination_plate_number":1,"destination_well_id":8}
                        ,5:{"destination_plate_number":1,"destination_well_id":10}
                        ,6:{"destination_plate_number":1,"destination_well_id":12}
                        ,7:{"destination_plate_number":1,"destination_well_id":14}
                        ,8:{"destination_plate_number":1,"destination_well_id":16}
                        ,9:{"destination_plate_number":1,"destination_well_id":18}
                        ,10:{"destination_plate_number":1,"destination_well_id":20}
                        ,11:{"destination_plate_number":1,"destination_well_id":22}
                        ,12:{"destination_plate_number":1,"destination_well_id":24}
                        ,13:{"destination_plate_number":1,"destination_well_id":50}
                        ,14:{"destination_plate_number":1,"destination_well_id":52}
                        ,15:{"destination_plate_number":1,"destination_well_id":54}
                        ,16:{"destination_plate_number":1,"destination_well_id":56}
                        ,17:{"destination_plate_number":1,"destination_well_id":58}
                        ,18:{"destination_plate_number":1,"destination_well_id":60}
                        ,19:{"destination_plate_number":1,"destination_well_id":62}
                        ,20:{"destination_plate_number":1,"destination_well_id":64}
                        ,21:{"destination_plate_number":1,"destination_well_id":66}
                        ,22:{"destination_plate_number":1,"destination_well_id":68}
                        ,23:{"destination_plate_number":1,"destination_well_id":70}
                        ,24:{"destination_plate_number":1,"destination_well_id":72}
                        ,25:{"destination_plate_number":1,"destination_well_id":98}
                        ,26:{"destination_plate_number":1,"destination_well_id":100}
                        ,27:{"destination_plate_number":1,"destination_well_id":102}
                        ,28:{"destination_plate_number":1,"destination_well_id":104}
                        ,29:{"destination_plate_number":1,"destination_well_id":106}
                        ,30:{"destination_plate_number":1,"destination_well_id":108}
                        ,31:{"destination_plate_number":1,"destination_well_id":110}
                        ,32:{"destination_plate_number":1,"destination_well_id":112}
                        ,33:{"destination_plate_number":1,"destination_well_id":114}
                        ,34:{"destination_plate_number":1,"destination_well_id":116}
                        ,35:{"destination_plate_number":1,"destination_well_id":118}
                        ,36:{"destination_plate_number":1,"destination_well_id":120}
                        ,37:{"destination_plate_number":1,"destination_well_id":146}
                        ,38:{"destination_plate_number":1,"destination_well_id":148}
                        ,39:{"destination_plate_number":1,"destination_well_id":150}
                        ,40:{"destination_plate_number":1,"destination_well_id":152}
                        ,41:{"destination_plate_number":1,"destination_well_id":154}
                        ,42:{"destination_plate_number":1,"destination_well_id":156}
                        ,43:{"destination_plate_number":1,"destination_well_id":158}
                        ,44:{"destination_plate_number":1,"destination_well_id":160}
                        ,45:{"destination_plate_number":1,"destination_well_id":162}
                        ,46:{"destination_plate_number":1,"destination_well_id":164}
                        ,47:{"destination_plate_number":1,"destination_well_id":166}
                        ,48:{"destination_plate_number":1,"destination_well_id":168}
                        ,49:{"destination_plate_number":1,"destination_well_id":194}
                        ,50:{"destination_plate_number":1,"destination_well_id":196}
                        ,51:{"destination_plate_number":1,"destination_well_id":198}
                        ,52:{"destination_plate_number":1,"destination_well_id":200}
                        ,53:{"destination_plate_number":1,"destination_well_id":202}
                        ,54:{"destination_plate_number":1,"destination_well_id":204}
                        ,55:{"destination_plate_number":1,"destination_well_id":206}
                        ,56:{"destination_plate_number":1,"destination_well_id":208}
                        ,57:{"destination_plate_number":1,"destination_well_id":210}
                        ,58:{"destination_plate_number":1,"destination_well_id":212}
                        ,59:{"destination_plate_number":1,"destination_well_id":214}
                        ,60:{"destination_plate_number":1,"destination_well_id":216}
                        ,61:{"destination_plate_number":1,"destination_well_id":242}
                        ,62:{"destination_plate_number":1,"destination_well_id":244}
                        ,63:{"destination_plate_number":1,"destination_well_id":246}
                        ,64:{"destination_plate_number":1,"destination_well_id":248}
                        ,65:{"destination_plate_number":1,"destination_well_id":250}
                        ,66:{"destination_plate_number":1,"destination_well_id":252}
                        ,67:{"destination_plate_number":1,"destination_well_id":254}
                        ,68:{"destination_plate_number":1,"destination_well_id":256}
                        ,69:{"destination_plate_number":1,"destination_well_id":258}
                        ,70:{"destination_plate_number":1,"destination_well_id":260}
                        ,71:{"destination_plate_number":1,"destination_well_id":262}
                        ,72:{"destination_plate_number":1,"destination_well_id":264}
                        ,73:{"destination_plate_number":1,"destination_well_id":290}
                        ,74:{"destination_plate_number":1,"destination_well_id":292}
                        ,75:{"destination_plate_number":1,"destination_well_id":294}
                        ,76:{"destination_plate_number":1,"destination_well_id":296}
                        ,77:{"destination_plate_number":1,"destination_well_id":298}
                        ,78:{"destination_plate_number":1,"destination_well_id":300}
                        ,79:{"destination_plate_number":1,"destination_well_id":302}
                        ,80:{"destination_plate_number":1,"destination_well_id":304}
                        ,81:{"destination_plate_number":1,"destination_well_id":306}
                        ,82:{"destination_plate_number":1,"destination_well_id":308}
                        ,83:{"destination_plate_number":1,"destination_well_id":310}
                        ,84:{"destination_plate_number":1,"destination_well_id":312}
                        ,85:{"destination_plate_number":1,"destination_well_id":338}
                        ,86:{"destination_plate_number":1,"destination_well_id":340}
                        ,87:{"destination_plate_number":1,"destination_well_id":342}
                        ,88:{"destination_plate_number":1,"destination_well_id":344}
                        ,89:{"destination_plate_number":1,"destination_well_id":346}
                        ,90:{"destination_plate_number":1,"destination_well_id":348}
                        ,91:{"destination_plate_number":1,"destination_well_id":350}
                        ,92:{"destination_plate_number":1,"destination_well_id":352}
                        ,93:{"destination_plate_number":1,"destination_well_id":354}
                        ,94:{"destination_plate_number":1,"destination_well_id":356}
                        ,95:{"destination_plate_number":1,"destination_well_id":358}
                        ,96:{"destination_plate_number":1,"destination_well_id":360}
                    }
                    ,{
                        1:{"destination_plate_number":1,"destination_well_id":25}
                        ,2:{"destination_plate_number":1,"destination_well_id":27}
                        ,3:{"destination_plate_number":1,"destination_well_id":29}
                        ,4:{"destination_plate_number":1,"destination_well_id":31}
                        ,5:{"destination_plate_number":1,"destination_well_id":33}
                        ,6:{"destination_plate_number":1,"destination_well_id":35}
                        ,7:{"destination_plate_number":1,"destination_well_id":37}
                        ,8:{"destination_plate_number":1,"destination_well_id":39}
                        ,9:{"destination_plate_number":1,"destination_well_id":41}
                        ,10:{"destination_plate_number":1,"destination_well_id":43}
                        ,11:{"destination_plate_number":1,"destination_well_id":45}
                        ,12:{"destination_plate_number":1,"destination_well_id":47}
                        ,13:{"destination_plate_number":1,"destination_well_id":73}
                        ,14:{"destination_plate_number":1,"destination_well_id":75}
                        ,15:{"destination_plate_number":1,"destination_well_id":77}
                        ,16:{"destination_plate_number":1,"destination_well_id":79}
                        ,17:{"destination_plate_number":1,"destination_well_id":81}
                        ,18:{"destination_plate_number":1,"destination_well_id":83}
                        ,19:{"destination_plate_number":1,"destination_well_id":85}
                        ,20:{"destination_plate_number":1,"destination_well_id":87}
                        ,21:{"destination_plate_number":1,"destination_well_id":89}
                        ,22:{"destination_plate_number":1,"destination_well_id":91}
                        ,23:{"destination_plate_number":1,"destination_well_id":93}
                        ,24:{"destination_plate_number":1,"destination_well_id":95}
                        ,25:{"destination_plate_number":1,"destination_well_id":121}
                        ,26:{"destination_plate_number":1,"destination_well_id":123}
                        ,27:{"destination_plate_number":1,"destination_well_id":125}
                        ,28:{"destination_plate_number":1,"destination_well_id":127}
                        ,29:{"destination_plate_number":1,"destination_well_id":129}
                        ,30:{"destination_plate_number":1,"destination_well_id":131}
                        ,31:{"destination_plate_number":1,"destination_well_id":133}
                        ,32:{"destination_plate_number":1,"destination_well_id":135}
                        ,33:{"destination_plate_number":1,"destination_well_id":137}
                        ,34:{"destination_plate_number":1,"destination_well_id":139}
                        ,35:{"destination_plate_number":1,"destination_well_id":141}
                        ,36:{"destination_plate_number":1,"destination_well_id":143}
                        ,37:{"destination_plate_number":1,"destination_well_id":169}
                        ,38:{"destination_plate_number":1,"destination_well_id":171}
                        ,39:{"destination_plate_number":1,"destination_well_id":173}
                        ,40:{"destination_plate_number":1,"destination_well_id":175}
                        ,41:{"destination_plate_number":1,"destination_well_id":177}
                        ,42:{"destination_plate_number":1,"destination_well_id":179}
                        ,43:{"destination_plate_number":1,"destination_well_id":181}
                        ,44:{"destination_plate_number":1,"destination_well_id":183}
                        ,45:{"destination_plate_number":1,"destination_well_id":185}
                        ,46:{"destination_plate_number":1,"destination_well_id":187}
                        ,47:{"destination_plate_number":1,"destination_well_id":189}
                        ,48:{"destination_plate_number":1,"destination_well_id":191}
                        ,49:{"destination_plate_number":1,"destination_well_id":217}
                        ,50:{"destination_plate_number":1,"destination_well_id":219}
                        ,51:{"destination_plate_number":1,"destination_well_id":221}
                        ,52:{"destination_plate_number":1,"destination_well_id":223}
                        ,53:{"destination_plate_number":1,"destination_well_id":225}
                        ,54:{"destination_plate_number":1,"destination_well_id":227}
                        ,55:{"destination_plate_number":1,"destination_well_id":229}
                        ,56:{"destination_plate_number":1,"destination_well_id":231}
                        ,57:{"destination_plate_number":1,"destination_well_id":233}
                        ,58:{"destination_plate_number":1,"destination_well_id":235}
                        ,59:{"destination_plate_number":1,"destination_well_id":237}
                        ,60:{"destination_plate_number":1,"destination_well_id":239}
                        ,61:{"destination_plate_number":1,"destination_well_id":265}
                        ,62:{"destination_plate_number":1,"destination_well_id":267}
                        ,63:{"destination_plate_number":1,"destination_well_id":269}
                        ,64:{"destination_plate_number":1,"destination_well_id":271}
                        ,65:{"destination_plate_number":1,"destination_well_id":273}
                        ,66:{"destination_plate_number":1,"destination_well_id":275}
                        ,67:{"destination_plate_number":1,"destination_well_id":277}
                        ,68:{"destination_plate_number":1,"destination_well_id":279}
                        ,69:{"destination_plate_number":1,"destination_well_id":281}
                        ,70:{"destination_plate_number":1,"destination_well_id":283}
                        ,71:{"destination_plate_number":1,"destination_well_id":285}
                        ,72:{"destination_plate_number":1,"destination_well_id":287}
                        ,73:{"destination_plate_number":1,"destination_well_id":313}
                        ,74:{"destination_plate_number":1,"destination_well_id":315}
                        ,75:{"destination_plate_number":1,"destination_well_id":317}
                        ,76:{"destination_plate_number":1,"destination_well_id":319}
                        ,77:{"destination_plate_number":1,"destination_well_id":321}
                        ,78:{"destination_plate_number":1,"destination_well_id":323}
                        ,79:{"destination_plate_number":1,"destination_well_id":325}
                        ,80:{"destination_plate_number":1,"destination_well_id":327}
                        ,81:{"destination_plate_number":1,"destination_well_id":329}
                        ,82:{"destination_plate_number":1,"destination_well_id":331}
                        ,83:{"destination_plate_number":1,"destination_well_id":333}
                        ,84:{"destination_plate_number":1,"destination_well_id":335}
                        ,85:{"destination_plate_number":1,"destination_well_id":361}
                        ,86:{"destination_plate_number":1,"destination_well_id":363}
                        ,87:{"destination_plate_number":1,"destination_well_id":365}
                        ,88:{"destination_plate_number":1,"destination_well_id":367}
                        ,89:{"destination_plate_number":1,"destination_well_id":369}
                        ,90:{"destination_plate_number":1,"destination_well_id":371}
                        ,91:{"destination_plate_number":1,"destination_well_id":373}
                        ,92:{"destination_plate_number":1,"destination_well_id":375}
                        ,93:{"destination_plate_number":1,"destination_well_id":377}
                        ,94:{"destination_plate_number":1,"destination_well_id":379}
                        ,95:{"destination_plate_number":1,"destination_well_id":381}
                        ,96:{"destination_plate_number":1,"destination_well_id":383}
                    }
                    ,{
                        1:{"destination_plate_number":1,"destination_well_id":26}
                        ,2:{"destination_plate_number":1,"destination_well_id":28}
                        ,3:{"destination_plate_number":1,"destination_well_id":30}
                        ,4:{"destination_plate_number":1,"destination_well_id":32}
                        ,5:{"destination_plate_number":1,"destination_well_id":34}
                        ,6:{"destination_plate_number":1,"destination_well_id":36}
                        ,7:{"destination_plate_number":1,"destination_well_id":38}
                        ,8:{"destination_plate_number":1,"destination_well_id":40}
                        ,9:{"destination_plate_number":1,"destination_well_id":42}
                        ,10:{"destination_plate_number":1,"destination_well_id":44}
                        ,11:{"destination_plate_number":1,"destination_well_id":46}
                        ,12:{"destination_plate_number":1,"destination_well_id":48}
                        ,13:{"destination_plate_number":1,"destination_well_id":74}
                        ,14:{"destination_plate_number":1,"destination_well_id":76}
                        ,15:{"destination_plate_number":1,"destination_well_id":78}
                        ,16:{"destination_plate_number":1,"destination_well_id":80}
                        ,17:{"destination_plate_number":1,"destination_well_id":82}
                        ,18:{"destination_plate_number":1,"destination_well_id":84}
                        ,19:{"destination_plate_number":1,"destination_well_id":86}
                        ,20:{"destination_plate_number":1,"destination_well_id":88}
                        ,21:{"destination_plate_number":1,"destination_well_id":90}
                        ,22:{"destination_plate_number":1,"destination_well_id":92}
                        ,23:{"destination_plate_number":1,"destination_well_id":94}
                        ,24:{"destination_plate_number":1,"destination_well_id":96}
                        ,25:{"destination_plate_number":1,"destination_well_id":122}
                        ,26:{"destination_plate_number":1,"destination_well_id":124}
                        ,27:{"destination_plate_number":1,"destination_well_id":126}
                        ,28:{"destination_plate_number":1,"destination_well_id":128}
                        ,29:{"destination_plate_number":1,"destination_well_id":130}
                        ,30:{"destination_plate_number":1,"destination_well_id":132}
                        ,31:{"destination_plate_number":1,"destination_well_id":134}
                        ,32:{"destination_plate_number":1,"destination_well_id":136}
                        ,33:{"destination_plate_number":1,"destination_well_id":138}
                        ,34:{"destination_plate_number":1,"destination_well_id":140}
                        ,35:{"destination_plate_number":1,"destination_well_id":142}
                        ,36:{"destination_plate_number":1,"destination_well_id":144}
                        ,37:{"destination_plate_number":1,"destination_well_id":170}
                        ,38:{"destination_plate_number":1,"destination_well_id":172}
                        ,39:{"destination_plate_number":1,"destination_well_id":174}
                        ,40:{"destination_plate_number":1,"destination_well_id":176}
                        ,41:{"destination_plate_number":1,"destination_well_id":178}
                        ,42:{"destination_plate_number":1,"destination_well_id":180}
                        ,43:{"destination_plate_number":1,"destination_well_id":182}
                        ,44:{"destination_plate_number":1,"destination_well_id":184}
                        ,45:{"destination_plate_number":1,"destination_well_id":186}
                        ,46:{"destination_plate_number":1,"destination_well_id":188}
                        ,47:{"destination_plate_number":1,"destination_well_id":190}
                        ,48:{"destination_plate_number":1,"destination_well_id":192}
                        ,49:{"destination_plate_number":1,"destination_well_id":218}
                        ,50:{"destination_plate_number":1,"destination_well_id":220}
                        ,51:{"destination_plate_number":1,"destination_well_id":222}
                        ,52:{"destination_plate_number":1,"destination_well_id":224}
                        ,53:{"destination_plate_number":1,"destination_well_id":226}
                        ,54:{"destination_plate_number":1,"destination_well_id":228}
                        ,55:{"destination_plate_number":1,"destination_well_id":230}
                        ,56:{"destination_plate_number":1,"destination_well_id":232}
                        ,57:{"destination_plate_number":1,"destination_well_id":234}
                        ,58:{"destination_plate_number":1,"destination_well_id":236}
                        ,59:{"destination_plate_number":1,"destination_well_id":238}
                        ,60:{"destination_plate_number":1,"destination_well_id":240}
                        ,61:{"destination_plate_number":1,"destination_well_id":266}
                        ,62:{"destination_plate_number":1,"destination_well_id":268}
                        ,63:{"destination_plate_number":1,"destination_well_id":270}
                        ,64:{"destination_plate_number":1,"destination_well_id":272}
                        ,65:{"destination_plate_number":1,"destination_well_id":274}
                        ,66:{"destination_plate_number":1,"destination_well_id":276}
                        ,67:{"destination_plate_number":1,"destination_well_id":278}
                        ,68:{"destination_plate_number":1,"destination_well_id":280}
                        ,69:{"destination_plate_number":1,"destination_well_id":282}
                        ,70:{"destination_plate_number":1,"destination_well_id":284}
                        ,71:{"destination_plate_number":1,"destination_well_id":286}
                        ,72:{"destination_plate_number":1,"destination_well_id":288}
                        ,73:{"destination_plate_number":1,"destination_well_id":314}
                        ,74:{"destination_plate_number":1,"destination_well_id":316}
                        ,75:{"destination_plate_number":1,"destination_well_id":318}
                        ,76:{"destination_plate_number":1,"destination_well_id":320}
                        ,77:{"destination_plate_number":1,"destination_well_id":322}
                        ,78:{"destination_plate_number":1,"destination_well_id":324}
                        ,79:{"destination_plate_number":1,"destination_well_id":326}
                        ,80:{"destination_plate_number":1,"destination_well_id":328}
                        ,81:{"destination_plate_number":1,"destination_well_id":330}
                        ,82:{"destination_plate_number":1,"destination_well_id":332}
                        ,83:{"destination_plate_number":1,"destination_well_id":334}
                        ,84:{"destination_plate_number":1,"destination_well_id":336}
                        ,85:{"destination_plate_number":1,"destination_well_id":362}
                        ,86:{"destination_plate_number":1,"destination_well_id":364}
                        ,87:{"destination_plate_number":1,"destination_well_id":366}
                        ,88:{"destination_plate_number":1,"destination_well_id":368}
                        ,89:{"destination_plate_number":1,"destination_well_id":370}
                        ,90:{"destination_plate_number":1,"destination_well_id":372}
                        ,91:{"destination_plate_number":1,"destination_well_id":374}
                        ,92:{"destination_plate_number":1,"destination_well_id":376}
                        ,93:{"destination_plate_number":1,"destination_well_id":378}
                        ,94:{"destination_plate_number":1,"destination_well_id":380}
                        ,95:{"destination_plate_number":1,"destination_well_id":382}
                        ,96:{"destination_plate_number":1,"destination_well_id":384}
                    }
                ]
            }
        }
        ,"row_column_maps": {
            "SPTT_0006": {
                # 384 well plate
                 1: {"row":"A", "column": 1}
                ,2: {"row":"A", "column": 2}
                ,3: {"row":"A", "column": 3}
                ,4: {"row":"A", "column": 4}
                ,5: {"row":"A", "column": 5}
                ,6: {"row":"A", "column": 6}
                ,7: {"row":"A", "column": 7}
                ,8: {"row":"A", "column": 8}
                ,9: {"row":"A", "column": 9}
                ,10: {"row":"A", "column": 10}
                ,11: {"row":"A", "column": 11}
                ,12: {"row":"A", "column": 12}
                ,13: {"row":"A", "column": 13}
                ,14: {"row":"A", "column": 14}
                ,15: {"row":"A", "column": 15}
                ,16: {"row":"A", "column": 16}
                ,17: {"row":"A", "column": 17}
                ,18: {"row":"A", "column": 18}
                ,19: {"row":"A", "column": 19}
                ,20: {"row":"A", "column": 20}
                ,21: {"row":"A", "column": 21}
                ,22: {"row":"A", "column": 22}
                ,23: {"row":"A", "column": 23}
                ,24: {"row":"A", "column": 24}
                ,25: {"row":"B", "column": 1}
                ,26: {"row":"B", "column": 2}
                ,27: {"row":"B", "column": 3}
                ,28: {"row":"B", "column": 4}
                ,29: {"row":"B", "column": 5}
                ,30: {"row":"B", "column": 6}
                ,31: {"row":"B", "column": 7}
                ,32: {"row":"B", "column": 8}
                ,33: {"row":"B", "column": 9}
                ,34: {"row":"B", "column": 10}
                ,35: {"row":"B", "column": 11}
                ,36: {"row":"B", "column": 12}
                ,37: {"row":"B", "column": 13}
                ,38: {"row":"B", "column": 14}
                ,39: {"row":"B", "column": 15}
                ,40: {"row":"B", "column": 16}
                ,41: {"row":"B", "column": 17}
                ,42: {"row":"B", "column": 18}
                ,43: {"row":"B", "column": 19}
                ,44: {"row":"B", "column": 20}
                ,45: {"row":"B", "column": 21}
                ,46: {"row":"B", "column": 22}
                ,47: {"row":"B", "column": 23}
                ,48: {"row":"B", "column": 24}
                ,49: {"row":"C", "column": 1}
                ,50: {"row":"C", "column": 2}
                ,51: {"row":"C", "column": 3}
                ,52: {"row":"C", "column": 4}
                ,53: {"row":"C", "column": 5}
                ,54: {"row":"C", "column": 6}
                ,55: {"row":"C", "column": 7}
                ,56: {"row":"C", "column": 8}
                ,57: {"row":"C", "column": 9}
                ,58: {"row":"C", "column": 10}
                ,59: {"row":"C", "column": 11}
                ,60: {"row":"C", "column": 12}
                ,61: {"row":"C", "column": 13}
                ,62: {"row":"C", "column": 14}
                ,63: {"row":"C", "column": 15}
                ,64: {"row":"C", "column": 16}
                ,65: {"row":"C", "column": 17}
                ,66: {"row":"C", "column": 18}
                ,67: {"row":"C", "column": 19}
                ,68: {"row":"C", "column": 20}
                ,69: {"row":"C", "column": 21}
                ,70: {"row":"C", "column": 22}
                ,71: {"row":"C", "column": 23}
                ,72: {"row":"C", "column": 24}
                ,73: {"row":"D", "column": 1}
                ,74: {"row":"D", "column": 2}
                ,75: {"row":"D", "column": 3}
                ,76: {"row":"D", "column": 4}
                ,77: {"row":"D", "column": 5}
                ,78: {"row":"D", "column": 6}
                ,79: {"row":"D", "column": 7}
                ,80: {"row":"D", "column": 8}
                ,81: {"row":"D", "column": 9}
                ,82: {"row":"D", "column": 10}
                ,83: {"row":"D", "column": 11}
                ,84: {"row":"D", "column": 12}
                ,85: {"row":"D", "column": 13}
                ,86: {"row":"D", "column": 14}
                ,87: {"row":"D", "column": 15}
                ,88: {"row":"D", "column": 16}
                ,89: {"row":"D", "column": 17}
                ,90: {"row":"D", "column": 18}
                ,91: {"row":"D", "column": 19}
                ,92: {"row":"D", "column": 20}
                ,93: {"row":"D", "column": 21}
                ,94: {"row":"D", "column": 22}
                ,95: {"row":"D", "column": 23}
                ,96: {"row":"D", "column": 24}
                ,97: {"row":"E", "column": 1}
                ,98: {"row":"E", "column": 2}
                ,99: {"row":"E", "column": 3}
                ,100: {"row":"E", "column": 4}
                ,101: {"row":"E", "column": 5}
                ,102: {"row":"E", "column": 6}
                ,103: {"row":"E", "column": 7}
                ,104: {"row":"E", "column": 8}
                ,105: {"row":"E", "column": 9}
                ,106: {"row":"E", "column": 10}
                ,107: {"row":"E", "column": 11}
                ,108: {"row":"E", "column": 12}
                ,109: {"row":"E", "column": 13}
                ,110: {"row":"E", "column": 14}
                ,111: {"row":"E", "column": 15}
                ,112: {"row":"E", "column": 16}
                ,113: {"row":"E", "column": 17}
                ,114: {"row":"E", "column": 18}
                ,115: {"row":"E", "column": 19}
                ,116: {"row":"E", "column": 20}
                ,117: {"row":"E", "column": 21}
                ,118: {"row":"E", "column": 22}
                ,119: {"row":"E", "column": 23}
                ,120: {"row":"E", "column": 24}
                ,121: {"row":"F", "column": 1}
                ,122: {"row":"F", "column": 2}
                ,123: {"row":"F", "column": 3}
                ,124: {"row":"F", "column": 4}
                ,125: {"row":"F", "column": 5}
                ,126: {"row":"F", "column": 6}
                ,127: {"row":"F", "column": 7}
                ,128: {"row":"F", "column": 8}
                ,129: {"row":"F", "column": 9}
                ,130: {"row":"F", "column": 10}
                ,131: {"row":"F", "column": 11}
                ,132: {"row":"F", "column": 12}
                ,133: {"row":"F", "column": 13}
                ,134: {"row":"F", "column": 14}
                ,135: {"row":"F", "column": 15}
                ,136: {"row":"F", "column": 16}
                ,137: {"row":"F", "column": 17}
                ,138: {"row":"F", "column": 18}
                ,139: {"row":"F", "column": 19}
                ,140: {"row":"F", "column": 20}
                ,141: {"row":"F", "column": 21}
                ,142: {"row":"F", "column": 22}
                ,143: {"row":"F", "column": 23}
                ,144: {"row":"F", "column": 24}
                ,145: {"row":"G", "column": 1}
                ,146: {"row":"G", "column": 2}
                ,147: {"row":"G", "column": 3}
                ,148: {"row":"G", "column": 4}
                ,149: {"row":"G", "column": 5}
                ,150: {"row":"G", "column": 6}
                ,151: {"row":"G", "column": 7}
                ,152: {"row":"G", "column": 8}
                ,153: {"row":"G", "column": 9}
                ,154: {"row":"G", "column": 10}
                ,155: {"row":"G", "column": 11}
                ,156: {"row":"G", "column": 12}
                ,157: {"row":"G", "column": 13}
                ,158: {"row":"G", "column": 14}
                ,159: {"row":"G", "column": 15}
                ,160: {"row":"G", "column": 16}
                ,161: {"row":"G", "column": 17}
                ,162: {"row":"G", "column": 18}
                ,163: {"row":"G", "column": 19}
                ,164: {"row":"G", "column": 20}
                ,165: {"row":"G", "column": 21}
                ,166: {"row":"G", "column": 22}
                ,167: {"row":"G", "column": 23}
                ,168: {"row":"G", "column": 24}
                ,169: {"row":"H", "column": 1}
                ,170: {"row":"H", "column": 2}
                ,171: {"row":"H", "column": 3}
                ,172: {"row":"H", "column": 4}
                ,173: {"row":"H", "column": 5}
                ,174: {"row":"H", "column": 6}
                ,175: {"row":"H", "column": 7}
                ,176: {"row":"H", "column": 8}
                ,177: {"row":"H", "column": 9}
                ,178: {"row":"H", "column": 10}
                ,179: {"row":"H", "column": 11}
                ,180: {"row":"H", "column": 12}
                ,181: {"row":"H", "column": 13}
                ,182: {"row":"H", "column": 14}
                ,183: {"row":"H", "column": 15}
                ,184: {"row":"H", "column": 16}
                ,185: {"row":"H", "column": 17}
                ,186: {"row":"H", "column": 18}
                ,187: {"row":"H", "column": 19}
                ,188: {"row":"H", "column": 20}
                ,189: {"row":"H", "column": 21}
                ,190: {"row":"H", "column": 22}
                ,191: {"row":"H", "column": 23}
                ,192: {"row":"H", "column": 24}
                ,193: {"row":"I", "column": 1}
                ,194: {"row":"I", "column": 2}
                ,195: {"row":"I", "column": 3}
                ,196: {"row":"I", "column": 4}
                ,197: {"row":"I", "column": 5}
                ,198: {"row":"I", "column": 6}
                ,199: {"row":"I", "column": 7}
                ,200: {"row":"I", "column": 8}
                ,201: {"row":"I", "column": 9}
                ,202: {"row":"I", "column": 10}
                ,203: {"row":"I", "column": 11}
                ,204: {"row":"I", "column": 12}
                ,205: {"row":"I", "column": 13}
                ,206: {"row":"I", "column": 14}
                ,207: {"row":"I", "column": 15}
                ,208: {"row":"I", "column": 16}
                ,209: {"row":"I", "column": 17}
                ,210: {"row":"I", "column": 18}
                ,211: {"row":"I", "column": 19}
                ,212: {"row":"I", "column": 20}
                ,213: {"row":"I", "column": 21}
                ,214: {"row":"I", "column": 22}
                ,215: {"row":"I", "column": 23}
                ,216: {"row":"I", "column": 24}
                ,217: {"row":"J", "column": 1}
                ,218: {"row":"J", "column": 2}
                ,219: {"row":"J", "column": 3}
                ,220: {"row":"J", "column": 4}
                ,221: {"row":"J", "column": 5}
                ,222: {"row":"J", "column": 6}
                ,223: {"row":"J", "column": 7}
                ,224: {"row":"J", "column": 8}
                ,225: {"row":"J", "column": 9}
                ,226: {"row":"J", "column": 10}
                ,227: {"row":"J", "column": 11}
                ,228: {"row":"J", "column": 12}
                ,229: {"row":"J", "column": 13}
                ,230: {"row":"J", "column": 14}
                ,231: {"row":"J", "column": 15}
                ,232: {"row":"J", "column": 16}
                ,233: {"row":"J", "column": 17}
                ,234: {"row":"J", "column": 18}
                ,235: {"row":"J", "column": 19}
                ,236: {"row":"J", "column": 20}
                ,237: {"row":"J", "column": 21}
                ,238: {"row":"J", "column": 22}
                ,239: {"row":"J", "column": 23}
                ,240: {"row":"J", "column": 24}
                ,241: {"row":"K", "column": 1}
                ,242: {"row":"K", "column": 2}
                ,243: {"row":"K", "column": 3}
                ,244: {"row":"K", "column": 4}
                ,245: {"row":"K", "column": 5}
                ,246: {"row":"K", "column": 6}
                ,247: {"row":"K", "column": 7}
                ,248: {"row":"K", "column": 8}
                ,249: {"row":"K", "column": 9}
                ,250: {"row":"K", "column": 10}
                ,251: {"row":"K", "column": 11}
                ,252: {"row":"K", "column": 12}
                ,253: {"row":"K", "column": 13}
                ,254: {"row":"K", "column": 14}
                ,255: {"row":"K", "column": 15}
                ,256: {"row":"K", "column": 16}
                ,257: {"row":"K", "column": 17}
                ,258: {"row":"K", "column": 18}
                ,259: {"row":"K", "column": 19}
                ,260: {"row":"K", "column": 20}
                ,261: {"row":"K", "column": 21}
                ,262: {"row":"K", "column": 22}
                ,263: {"row":"K", "column": 23}
                ,264: {"row":"K", "column": 24}
                ,265: {"row":"L", "column": 1}
                ,266: {"row":"L", "column": 2}
                ,267: {"row":"L", "column": 3}
                ,268: {"row":"L", "column": 4}
                ,269: {"row":"L", "column": 5}
                ,270: {"row":"L", "column": 6}
                ,271: {"row":"L", "column": 7}
                ,272: {"row":"L", "column": 8}
                ,273: {"row":"L", "column": 9}
                ,274: {"row":"L", "column": 10}
                ,275: {"row":"L", "column": 11}
                ,276: {"row":"L", "column": 12}
                ,277: {"row":"L", "column": 13}
                ,278: {"row":"L", "column": 14}
                ,279: {"row":"L", "column": 15}
                ,280: {"row":"L", "column": 16}
                ,281: {"row":"L", "column": 17}
                ,282: {"row":"L", "column": 18}
                ,283: {"row":"L", "column": 19}
                ,284: {"row":"L", "column": 20}
                ,285: {"row":"L", "column": 21}
                ,286: {"row":"L", "column": 22}
                ,287: {"row":"L", "column": 23}
                ,288: {"row":"L", "column": 24}
                ,289: {"row":"M", "column": 1}
                ,290: {"row":"M", "column": 2}
                ,291: {"row":"M", "column": 3}
                ,292: {"row":"M", "column": 4}
                ,293: {"row":"M", "column": 5}
                ,294: {"row":"M", "column": 6}
                ,295: {"row":"M", "column": 7}
                ,296: {"row":"M", "column": 8}
                ,297: {"row":"M", "column": 9}
                ,298: {"row":"M", "column": 10}
                ,299: {"row":"M", "column": 11}
                ,300: {"row":"M", "column": 12}
                ,301: {"row":"M", "column": 13}
                ,302: {"row":"M", "column": 14}
                ,303: {"row":"M", "column": 15}
                ,304: {"row":"M", "column": 16}
                ,305: {"row":"M", "column": 17}
                ,306: {"row":"M", "column": 18}
                ,307: {"row":"M", "column": 19}
                ,308: {"row":"M", "column": 20}
                ,309: {"row":"M", "column": 21}
                ,310: {"row":"M", "column": 22}
                ,311: {"row":"M", "column": 23}
                ,312: {"row":"M", "column": 24}
                ,313: {"row":"N", "column": 1}
                ,314: {"row":"N", "column": 2}
                ,315: {"row":"N", "column": 3}
                ,316: {"row":"N", "column": 4}
                ,317: {"row":"N", "column": 5}
                ,318: {"row":"N", "column": 6}
                ,319: {"row":"N", "column": 7}
                ,320: {"row":"N", "column": 8}
                ,321: {"row":"N", "column": 9}
                ,322: {"row":"N", "column": 10}
                ,323: {"row":"N", "column": 11}
                ,324: {"row":"N", "column": 12}
                ,325: {"row":"N", "column": 13}
                ,326: {"row":"N", "column": 14}
                ,327: {"row":"N", "column": 15}
                ,328: {"row":"N", "column": 16}
                ,329: {"row":"N", "column": 17}
                ,330: {"row":"N", "column": 18}
                ,331: {"row":"N", "column": 19}
                ,332: {"row":"N", "column": 20}
                ,333: {"row":"N", "column": 21}
                ,334: {"row":"N", "column": 22}
                ,335: {"row":"N", "column": 23}
                ,336: {"row":"N", "column": 24}
                ,337: {"row":"O", "column": 1}
                ,338: {"row":"O", "column": 2}
                ,339: {"row":"O", "column": 3}
                ,340: {"row":"O", "column": 4}
                ,341: {"row":"O", "column": 5}
                ,342: {"row":"O", "column": 6}
                ,343: {"row":"O", "column": 7}
                ,344: {"row":"O", "column": 8}
                ,345: {"row":"O", "column": 9}
                ,346: {"row":"O", "column": 10}
                ,347: {"row":"O", "column": 11}
                ,348: {"row":"O", "column": 12}
                ,349: {"row":"O", "column": 13}
                ,350: {"row":"O", "column": 14}
                ,351: {"row":"O", "column": 15}
                ,352: {"row":"O", "column": 16}
                ,353: {"row":"O", "column": 17}
                ,354: {"row":"O", "column": 18}
                ,355: {"row":"O", "column": 19}
                ,356: {"row":"O", "column": 20}
                ,357: {"row":"O", "column": 21}
                ,358: {"row":"O", "column": 22}
                ,359: {"row":"O", "column": 23}
                ,360: {"row":"O", "column": 24}
                ,361: {"row":"P", "column": 1}
                ,362: {"row":"P", "column": 2}
                ,363: {"row":"P", "column": 3}
                ,364: {"row":"P", "column": 4}
                ,365: {"row":"P", "column": 5}
                ,366: {"row":"P", "column": 6}
                ,367: {"row":"P", "column": 7}
                ,368: {"row":"P", "column": 8}
                ,369: {"row":"P", "column": 9}
                ,370: {"row":"P", "column": 10}
                ,371: {"row":"P", "column": 11}
                ,372: {"row":"P", "column": 12}
                ,373: {"row":"P", "column": 13}
                ,374: {"row":"P", "column": 14}
                ,375: {"row":"P", "column": 15}
                ,376: {"row":"P", "column": 16}
                ,377: {"row":"P", "column": 17}
                ,378: {"row":"P", "column": 18}
                ,379: {"row":"P", "column": 19}
                ,380: {"row":"P", "column": 20}
                ,381: {"row":"P", "column": 21}
                ,382: {"row":"P", "column": 22}
                ,383: {"row":"P", "column": 23}
                ,384: {"row":"P", "column": 24}

            }
            ,"SPTT_0005": {
                # 96 well plate
                1:{ "row": "A", "column": 1}
                ,2:{ "row": "A", "column": 2}
                ,3:{ "row": "A", "column": 3}
                ,4:{ "row": "A", "column": 4}
                ,5:{ "row": "A", "column": 5}
                ,6:{ "row": "A", "column": 6}
                ,7:{ "row": "A", "column": 7}
                ,8:{ "row": "A", "column": 8}
                ,9:{ "row": "A", "column": 9}
                ,10: {"row": "A", "column": 10}
                ,11: {"row": "A", "column": 11}
                ,12: {"row": "A", "column": 12}
                ,13: {"row": "B", "column": 1}
                ,14: {"row": "B", "column": 2}
                ,15: {"row": "B", "column": 3}
                ,16: {"row": "B", "column": 4}
                ,17: {"row": "B", "column": 5}
                ,18: {"row": "B", "column": 6}
                ,19: {"row": "B", "column": 7}
                ,20: {"row": "B", "column": 8}
                ,21: {"row": "B", "column": 9}
                ,22: {"row": "B", "column": 10}
                ,23: {"row": "B", "column": 11}
                ,24: {"row": "B", "column": 12}
                ,25: {"row": "C", "column": 1}
                ,26: {"row": "C", "column": 2}
                ,27: {"row": "C", "column": 3}
                ,28: {"row": "C", "column": 4}
                ,29: {"row": "C", "column": 5}
                ,30: {"row": "C", "column": 6}
                ,31: {"row": "C", "column": 7}
                ,32: {"row": "C", "column": 8}
                ,33: {"row": "C", "column": 9}
                ,34: {"row": "C", "column": 10}
                ,35: {"row": "C", "column": 11}
                ,36: {"row": "C", "column": 12}
                ,37: {"row": "D", "column": 1}
                ,38: {"row": "D", "column": 2}
                ,39: {"row": "D", "column": 3}
                ,40: {"row": "D", "column": 4}
                ,41: {"row": "D", "column": 5}
                ,42: {"row": "D", "column": 6}
                ,43: {"row": "D", "column": 7}
                ,44: {"row": "D", "column": 8}
                ,45: {"row": "D", "column": 9}
                ,46: {"row": "D", "column": 10}
                ,47: {"row": "D", "column": 11}
                ,48: {"row": "D", "column": 12}
                ,49: {"row": "E", "column": 1}
                ,50: {"row": "E", "column": 2}
                ,51: {"row": "E", "column": 3}
                ,52: {"row": "E", "column": 4}
                ,53: {"row": "E", "column": 5}
                ,54: {"row": "E", "column": 6}
                ,55: {"row": "E", "column": 7}
                ,56: {"row": "E", "column": 8}
                ,57: {"row": "E", "column": 9}
                ,58: {"row": "E", "column": 10}
                ,59: {"row": "E", "column": 11}
                ,60: {"row": "E", "column": 12}
                ,61: {"row": "F", "column": 1}
                ,62: {"row": "F", "column": 2}
                ,63: {"row": "F", "column": 3}
                ,64: {"row": "F", "column": 4}
                ,65: {"row": "F", "column": 5}
                ,66: {"row": "F", "column": 6}
                ,67: {"row": "F", "column": 7}
                ,68: {"row": "F", "column": 8}
                ,69: {"row": "F", "column": 9}
                ,70: {"row": "F", "column": 10}
                ,71: {"row": "F", "column": 11}
                ,72: {"row": "F", "column": 12}
                ,73: {"row": "G", "column": 1}
                ,74: {"row": "G", "column": 2}
                ,75: {"row": "G", "column": 3}
                ,76: {"row": "G", "column": 4}
                ,77: {"row": "G", "column": 5}
                ,78: {"row": "G", "column": 6}
                ,79: {"row": "G", "column": 7}
                ,80: {"row": "G", "column": 8}
                ,81: {"row": "G", "column": 9}
                ,82: {"row": "G", "column": 10}
                ,83: {"row": "G", "column": 11}
                ,84: {"row": "G", "column": 12}
                ,85: {"row": "H", "column": 1}
                ,86: {"row": "H", "column": 2}
                ,87: {"row": "H", "column": 3}
                ,88: {"row": "H", "column": 4}
                ,89: {"row": "H", "column": 5}
                ,90: {"row": "H", "column": 6}
                ,91: {"row": "H", "column": 7}
                ,92: {"row": "H", "column": 8}
                ,93: {"row": "H", "column": 9}
                ,94: {"row": "H", "column": 10}
                ,95: {"row": "H", "column": 11}
                ,96: {"row": "H", "column": 12}
            }
            ,"SPTT_0004": {
                # 48 well plate
                 1: {"row": "A", "column": 1}
                ,2: {"row": "A", "column": 2}
                ,3: {"row": "A", "column": 3}
                ,4: {"row": "A", "column": 4}
                ,5: {"row": "A", "column": 5}
                ,6: {"row": "A", "column": 6}
                ,7: {"row": "B", "column": 1}
                ,8: {"row": "B", "column": 2}
                ,9: {"row": "B", "column": 3}
                ,10: {"row": "B", "column": 4}
                ,11: {"row": "B", "column": 5}
                ,12: {"row": "C", "column": 6}
                ,13: {"row": "C", "column": 1}
                ,14: {"row": "C", "column": 2}
                ,15: {"row": "C", "column": 3}
                ,16: {"row": "C", "column": 4}
                ,17: {"row": "C", "column": 5}
                ,18: {"row": "C", "column": 6}
                ,19: {"row": "D", "column": 1}
                ,20: {"row": "D", "column": 2}
                ,21: {"row": "D", "column": 3}
                ,22: {"row": "D", "column": 4}
                ,23: {"row": "D", "column": 5}
                ,24: {"row": "D", "column": 6}
                ,25: {"row": "E", "column": 1}
                ,26: {"row": "E", "column": 2}
                ,27: {"row": "E", "column": 3}
                ,28: {"row": "E", "column": 4}
                ,29: {"row": "E", "column": 5}
                ,30: {"row": "E", "column": 6}
                ,31: {"row": "F", "column": 1}
                ,32: {"row": "F", "column": 2}
                ,33: {"row": "F", "column": 3}
                ,34: {"row": "F", "column": 4}
                ,35: {"row": "F", "column": 5}
                ,36: {"row": "F", "column": 6}
                ,37: {"row": "G", "column": 1}
                ,38: {"row": "G", "column": 2}
                ,39: {"row": "G", "column": 3}
                ,40: {"row": "G", "column": 4}
                ,41: {"row": "G", "column": 5}
                ,42: {"row": "G", "column": 6}
                ,43: {"row": "H", "column": 1}
                ,44: {"row": "H", "column": 2}
                ,45: {"row": "H", "column": 3}
                ,46: {"row": "H", "column": 4}
                ,47: {"row": "H", "column": 5}
                ,48: {"row": "H", "column": 6}
            }

        }
    }