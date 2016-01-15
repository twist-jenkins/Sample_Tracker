app = angular.module('twist.app')

.factory('Maps', ['Constants', 
    function (Constants) {
        return {
            transferTemplates: {
                1: {  // keyed to sample_transfer_template_id in the database
                    description: 'Source and destination have SAME LAYOUT'
                    ,type: 'same-same'
                    ,source: {
                        plateCount: 1
                        ,variablePlateCount: false
                    }
                    ,destination: {
                        plateCount: 1
                        ,variablePlateCount: false
                    }
                }
                ,2: {  // keyed to sample_transfer_template_id in the database
                    description: 'Source and destination plate are SAME PLATE'
                    ,type: 'same-same'
                    ,source: {
                        plateCount: 1
                        ,variablePlateCount: false
                    }
                    ,destination: {
                        plateCount: 0
                        ,variablePlateCount: false
                    }
                }
                ,13: {  // keyed to sample_transfer_template_id in the database
                    description: '384 to 4x96'
                    ,type: 'standard_template'
                    ,source: {
                        plateCount: 1
                        ,wellCount: 384
                        ,plateTypeId: 'SPTT_0006'
                        ,variablePlateCount: false
                    }
                    ,destination:{
                        plateCount: 4
                        ,wellCount: 96
                        ,plateTypeId: 'SPTT_0005'
                        ,variablePlateCount: false
                        ,plateTitles: ['Quadrant&nbsp;1:&nbsp;','Quadrant&nbsp;2:&nbsp;','Quadrant&nbsp;3:&nbsp;','Quadrant&nbsp;4:&nbsp;']
                    }
                    ,plateWellToWellMaps: [ // index in plate_well_to_well_map array = source_plate_index
                        {   // key= sopurce plate well id
                            1: {destination_plate_number: 1, destination_well_id: 1}
                            ,2: {destination_plate_number: 2, destination_well_id: 1}
                            ,3: {destination_plate_number: 1, destination_well_id: 2}
                            ,4: {destination_plate_number: 2, destination_well_id: 2}
                            ,5: {destination_plate_number: 1, destination_well_id: 3}
                            ,6: {destination_plate_number: 2, destination_well_id: 3}
                            ,7: {destination_plate_number: 1, destination_well_id: 4}
                            ,8: {destination_plate_number: 2, destination_well_id: 4}
                            ,9: {destination_plate_number: 1, destination_well_id: 5}
                            ,10: {destination_plate_number: 2, destination_well_id: 5}
                            ,11: {destination_plate_number: 1, destination_well_id: 6}
                            ,12: {destination_plate_number: 2, destination_well_id: 6}
                            ,13: {destination_plate_number: 1, destination_well_id: 7}
                            ,14: {destination_plate_number: 2, destination_well_id: 7}
                            ,15: {destination_plate_number: 1, destination_well_id: 8}
                            ,16: {destination_plate_number: 2, destination_well_id: 8}
                            ,17: {destination_plate_number: 1, destination_well_id: 9}
                            ,18: {destination_plate_number: 2, destination_well_id: 9}
                            ,19: {destination_plate_number: 1, destination_well_id: 10}
                            ,20: {destination_plate_number: 2, destination_well_id: 10}
                            ,21: {destination_plate_number: 1, destination_well_id: 11}
                            ,22: {destination_plate_number: 2, destination_well_id: 11}
                            ,23: {destination_plate_number: 1, destination_well_id: 12}
                            ,24: {destination_plate_number: 2, destination_well_id: 12}
                            ,25: {destination_plate_number: 3, destination_well_id: 1}
                            ,26: {destination_plate_number: 4, destination_well_id: 1}
                            ,27: {destination_plate_number: 3, destination_well_id: 2}
                            ,28: {destination_plate_number: 4, destination_well_id: 2}
                            ,29: {destination_plate_number: 3, destination_well_id: 3}
                            ,30: {destination_plate_number: 4, destination_well_id: 3}
                            ,31: {destination_plate_number: 3, destination_well_id: 4}
                            ,32: {destination_plate_number: 4, destination_well_id: 4}
                            ,33: {destination_plate_number: 3, destination_well_id: 5}
                            ,34: {destination_plate_number: 4, destination_well_id: 5}
                            ,35: {destination_plate_number: 3, destination_well_id: 6}
                            ,36: {destination_plate_number: 4, destination_well_id: 6}
                            ,37: {destination_plate_number: 3, destination_well_id: 7}
                            ,38: {destination_plate_number: 4, destination_well_id: 7}
                            ,39: {destination_plate_number: 3, destination_well_id: 8}
                            ,40: {destination_plate_number: 4, destination_well_id: 8}
                            ,41: {destination_plate_number: 3, destination_well_id: 9}
                            ,42: {destination_plate_number: 4, destination_well_id: 9}
                            ,43: {destination_plate_number: 3, destination_well_id: 10}
                            ,44: {destination_plate_number: 4, destination_well_id: 10}
                            ,45: {destination_plate_number: 3, destination_well_id: 11}
                            ,46: {destination_plate_number: 4, destination_well_id: 11}
                            ,47: {destination_plate_number: 3, destination_well_id: 12}
                            ,48: {destination_plate_number: 4, destination_well_id: 12}
                            ,49: {destination_plate_number: 1, destination_well_id: 13}
                            ,50: {destination_plate_number: 2, destination_well_id: 13}
                            ,51: {destination_plate_number: 1, destination_well_id: 14}
                            ,52: {destination_plate_number: 2, destination_well_id: 14}
                            ,53: {destination_plate_number: 1, destination_well_id: 15}
                            ,54: {destination_plate_number: 2, destination_well_id: 15}
                            ,55: {destination_plate_number: 1, destination_well_id: 16}
                            ,56: {destination_plate_number: 2, destination_well_id: 16}
                            ,57: {destination_plate_number: 1, destination_well_id: 17}
                            ,58: {destination_plate_number: 2, destination_well_id: 17}
                            ,59: {destination_plate_number: 1, destination_well_id: 18}
                            ,60: {destination_plate_number: 2, destination_well_id: 18}
                            ,61: {destination_plate_number: 1, destination_well_id: 19}
                            ,62: {destination_plate_number: 2, destination_well_id: 19}
                            ,63: {destination_plate_number: 1, destination_well_id: 20}
                            ,64: {destination_plate_number: 2, destination_well_id: 20}
                            ,65: {destination_plate_number: 1, destination_well_id: 21}
                            ,66: {destination_plate_number: 2, destination_well_id: 21}
                            ,67: {destination_plate_number: 1, destination_well_id: 22}
                            ,68: {destination_plate_number: 2, destination_well_id: 22}
                            ,69: {destination_plate_number: 1, destination_well_id: 23}
                            ,70: {destination_plate_number: 2, destination_well_id: 23}
                            ,71: {destination_plate_number: 1, destination_well_id: 24}
                            ,72: {destination_plate_number: 2, destination_well_id: 24}
                            ,73: {destination_plate_number: 3, destination_well_id: 13}
                            ,74: {destination_plate_number: 4, destination_well_id: 13}
                            ,75: {destination_plate_number: 3, destination_well_id: 14}
                            ,76: {destination_plate_number: 4, destination_well_id: 14}
                            ,77: {destination_plate_number: 3, destination_well_id: 15}
                            ,78: {destination_plate_number: 4, destination_well_id: 15}
                            ,79: {destination_plate_number: 3, destination_well_id: 16}
                            ,80: {destination_plate_number: 4, destination_well_id: 16}
                            ,81: {destination_plate_number: 3, destination_well_id: 17}
                            ,82: {destination_plate_number: 4, destination_well_id: 17}
                            ,83: {destination_plate_number: 3, destination_well_id: 18}
                            ,84: {destination_plate_number: 4, destination_well_id: 18}
                            ,85: {destination_plate_number: 3, destination_well_id: 19}
                            ,86: {destination_plate_number: 4, destination_well_id: 19}
                            ,87: {destination_plate_number: 3, destination_well_id: 20}
                            ,88: {destination_plate_number: 4, destination_well_id: 20}
                            ,89: {destination_plate_number: 3, destination_well_id: 21}
                            ,90: {destination_plate_number: 4, destination_well_id: 21}
                            ,91: {destination_plate_number: 3, destination_well_id: 22}
                            ,92: {destination_plate_number: 4, destination_well_id: 22}
                            ,93: {destination_plate_number: 3, destination_well_id: 23}
                            ,94: {destination_plate_number: 4, destination_well_id: 23}
                            ,95: {destination_plate_number: 3, destination_well_id: 24}
                            ,96: {destination_plate_number: 4, destination_well_id: 24}
                            ,97: {destination_plate_number: 1, destination_well_id: 25}
                            ,98: {destination_plate_number: 2, destination_well_id: 25}
                            ,99: {destination_plate_number: 1, destination_well_id: 26}
                            ,100: {destination_plate_number: 2, destination_well_id: 26}
                            ,101: {destination_plate_number: 1, destination_well_id: 27}
                            ,102: {destination_plate_number: 2, destination_well_id: 27}
                            ,103: {destination_plate_number: 1, destination_well_id: 28}
                            ,104: {destination_plate_number: 2, destination_well_id: 28}
                            ,105: {destination_plate_number: 1, destination_well_id: 29}
                            ,106: {destination_plate_number: 2, destination_well_id: 29}
                            ,107: {destination_plate_number: 1, destination_well_id: 30}
                            ,108: {destination_plate_number: 2, destination_well_id: 30}
                            ,109: {destination_plate_number: 1, destination_well_id: 31}
                            ,110: {destination_plate_number: 2, destination_well_id: 31}
                            ,111: {destination_plate_number: 1, destination_well_id: 32}
                            ,112: {destination_plate_number: 2, destination_well_id: 32}
                            ,113: {destination_plate_number: 1, destination_well_id: 33}
                            ,114: {destination_plate_number: 2, destination_well_id: 33}
                            ,115: {destination_plate_number: 1, destination_well_id: 34}
                            ,116: {destination_plate_number: 2, destination_well_id: 34}
                            ,117: {destination_plate_number: 1, destination_well_id: 35}
                            ,118: {destination_plate_number: 2, destination_well_id: 35}
                            ,119: {destination_plate_number: 1, destination_well_id: 36}
                            ,120: {destination_plate_number: 2, destination_well_id: 36}
                            ,121: {destination_plate_number: 3, destination_well_id: 25}
                            ,122: {destination_plate_number: 4, destination_well_id: 25}
                            ,123: {destination_plate_number: 3, destination_well_id: 26}
                            ,124: {destination_plate_number: 4, destination_well_id: 26}
                            ,125: {destination_plate_number: 3, destination_well_id: 27}
                            ,126: {destination_plate_number: 4, destination_well_id: 27}
                            ,127: {destination_plate_number: 3, destination_well_id: 28}
                            ,128: {destination_plate_number: 4, destination_well_id: 28}
                            ,129: {destination_plate_number: 3, destination_well_id: 29}
                            ,130: {destination_plate_number: 4, destination_well_id: 29}
                            ,131: {destination_plate_number: 3, destination_well_id: 30}
                            ,132: {destination_plate_number: 4, destination_well_id: 30}
                            ,133: {destination_plate_number: 3, destination_well_id: 31}
                            ,134: {destination_plate_number: 4, destination_well_id: 31}
                            ,135: {destination_plate_number: 3, destination_well_id: 32}
                            ,136: {destination_plate_number: 4, destination_well_id: 32}
                            ,137: {destination_plate_number: 3, destination_well_id: 33}
                            ,138: {destination_plate_number: 4, destination_well_id: 33}
                            ,139: {destination_plate_number: 3, destination_well_id: 34}
                            ,140: {destination_plate_number: 4, destination_well_id: 34}
                            ,141: {destination_plate_number: 3, destination_well_id: 35}
                            ,142: {destination_plate_number: 4, destination_well_id: 35}
                            ,143: {destination_plate_number: 3, destination_well_id: 36}
                            ,144: {destination_plate_number: 4, destination_well_id: 36}
                            ,145: {destination_plate_number: 1, destination_well_id: 37}
                            ,146: {destination_plate_number: 2, destination_well_id: 37}
                            ,147: {destination_plate_number: 1, destination_well_id: 38}
                            ,148: {destination_plate_number: 2, destination_well_id: 38}
                            ,149: {destination_plate_number: 1, destination_well_id: 39}
                            ,150: {destination_plate_number: 2, destination_well_id: 39}
                            ,151: {destination_plate_number: 1, destination_well_id: 40}
                            ,152: {destination_plate_number: 2, destination_well_id: 40}
                            ,153: {destination_plate_number: 1, destination_well_id: 41}
                            ,154: {destination_plate_number: 2, destination_well_id: 41}
                            ,155: {destination_plate_number: 1, destination_well_id: 42}
                            ,156: {destination_plate_number: 2, destination_well_id: 42}
                            ,157: {destination_plate_number: 1, destination_well_id: 43}
                            ,158: {destination_plate_number: 2, destination_well_id: 43}
                            ,159: {destination_plate_number: 1, destination_well_id: 44}
                            ,160: {destination_plate_number: 2, destination_well_id: 44}
                            ,161: {destination_plate_number: 1, destination_well_id: 45}
                            ,162: {destination_plate_number: 2, destination_well_id: 45}
                            ,163: {destination_plate_number: 1, destination_well_id: 46}
                            ,164: {destination_plate_number: 2, destination_well_id: 46}
                            ,165: {destination_plate_number: 1, destination_well_id: 47}
                            ,166: {destination_plate_number: 2, destination_well_id: 47}
                            ,167: {destination_plate_number: 1, destination_well_id: 48}
                            ,168: {destination_plate_number: 2, destination_well_id: 48}
                            ,169: {destination_plate_number: 3, destination_well_id: 37}
                            ,170: {destination_plate_number: 4, destination_well_id: 37}
                            ,171: {destination_plate_number: 3, destination_well_id: 38}
                            ,172: {destination_plate_number: 4, destination_well_id: 38}
                            ,173: {destination_plate_number: 3, destination_well_id: 39}
                            ,174: {destination_plate_number: 4, destination_well_id: 39}
                            ,175: {destination_plate_number: 3, destination_well_id: 40}
                            ,176: {destination_plate_number: 4, destination_well_id: 40}
                            ,177: {destination_plate_number: 3, destination_well_id: 41}
                            ,178: {destination_plate_number: 4, destination_well_id: 41}
                            ,179: {destination_plate_number: 3, destination_well_id: 42}
                            ,180: {destination_plate_number: 4, destination_well_id: 42}
                            ,181: {destination_plate_number: 3, destination_well_id: 43}
                            ,182: {destination_plate_number: 4, destination_well_id: 43}
                            ,183: {destination_plate_number: 3, destination_well_id: 44}
                            ,184: {destination_plate_number: 4, destination_well_id: 44}
                            ,185: {destination_plate_number: 3, destination_well_id: 45}
                            ,186: {destination_plate_number: 4, destination_well_id: 45}
                            ,187: {destination_plate_number: 3, destination_well_id: 46}
                            ,188: {destination_plate_number: 4, destination_well_id: 46}
                            ,189: {destination_plate_number: 3, destination_well_id: 47}
                            ,190: {destination_plate_number: 4, destination_well_id: 47}
                            ,191: {destination_plate_number: 3, destination_well_id: 48}
                            ,192: {destination_plate_number: 4, destination_well_id: 48}
                            ,193: {destination_plate_number: 1, destination_well_id: 49}
                            ,194: {destination_plate_number: 2, destination_well_id: 49}
                            ,195: {destination_plate_number: 1, destination_well_id: 50}
                            ,196: {destination_plate_number: 2, destination_well_id: 50}
                            ,197: {destination_plate_number: 1, destination_well_id: 51}
                            ,198: {destination_plate_number: 2, destination_well_id: 51}
                            ,199: {destination_plate_number: 1, destination_well_id: 52}
                            ,200: {destination_plate_number: 2, destination_well_id: 52}
                            ,201: {destination_plate_number: 1, destination_well_id: 53}
                            ,202: {destination_plate_number: 2, destination_well_id: 53}
                            ,203: {destination_plate_number: 1, destination_well_id: 54}
                            ,204: {destination_plate_number: 2, destination_well_id: 54}
                            ,205: {destination_plate_number: 1, destination_well_id: 55}
                            ,206: {destination_plate_number: 2, destination_well_id: 55}
                            ,207: {destination_plate_number: 1, destination_well_id: 56}
                            ,208: {destination_plate_number: 2, destination_well_id: 56}
                            ,209: {destination_plate_number: 1, destination_well_id: 57}
                            ,210: {destination_plate_number: 2, destination_well_id: 57}
                            ,211: {destination_plate_number: 1, destination_well_id: 58}
                            ,212: {destination_plate_number: 2, destination_well_id: 58}
                            ,213: {destination_plate_number: 1, destination_well_id: 59}
                            ,214: {destination_plate_number: 2, destination_well_id: 59}
                            ,215: {destination_plate_number: 1, destination_well_id: 60}
                            ,216: {destination_plate_number: 2, destination_well_id: 60}
                            ,217: {destination_plate_number: 3, destination_well_id: 49}
                            ,218: {destination_plate_number: 4, destination_well_id: 49}
                            ,219: {destination_plate_number: 3, destination_well_id: 50}
                            ,220: {destination_plate_number: 4, destination_well_id: 50}
                            ,221: {destination_plate_number: 3, destination_well_id: 51}
                            ,222: {destination_plate_number: 4, destination_well_id: 51}
                            ,223: {destination_plate_number: 3, destination_well_id: 52}
                            ,224: {destination_plate_number: 4, destination_well_id: 52}
                            ,225: {destination_plate_number: 3, destination_well_id: 53}
                            ,226: {destination_plate_number: 4, destination_well_id: 53}
                            ,227: {destination_plate_number: 3, destination_well_id: 54}
                            ,228: {destination_plate_number: 4, destination_well_id: 54}
                            ,229: {destination_plate_number: 3, destination_well_id: 55}
                            ,230: {destination_plate_number: 4, destination_well_id: 55}
                            ,231: {destination_plate_number: 3, destination_well_id: 56}
                            ,232: {destination_plate_number: 4, destination_well_id: 56}
                            ,233: {destination_plate_number: 3, destination_well_id: 57}
                            ,234: {destination_plate_number: 4, destination_well_id: 57}
                            ,235: {destination_plate_number: 3, destination_well_id: 58}
                            ,236: {destination_plate_number: 4, destination_well_id: 58}
                            ,237: {destination_plate_number: 3, destination_well_id: 59}
                            ,238: {destination_plate_number: 4, destination_well_id: 59}
                            ,239: {destination_plate_number: 3, destination_well_id: 60}
                            ,240: {destination_plate_number: 4, destination_well_id: 60}
                            ,241: {destination_plate_number: 1, destination_well_id: 61}
                            ,242: {destination_plate_number: 2, destination_well_id: 61}
                            ,243: {destination_plate_number: 1, destination_well_id: 62}
                            ,244: {destination_plate_number: 2, destination_well_id: 62}
                            ,245: {destination_plate_number: 1, destination_well_id: 63}
                            ,246: {destination_plate_number: 2, destination_well_id: 63}
                            ,247: {destination_plate_number: 1, destination_well_id: 64}
                            ,248: {destination_plate_number: 2, destination_well_id: 64}
                            ,249: {destination_plate_number: 1, destination_well_id: 65}
                            ,250: {destination_plate_number: 2, destination_well_id: 65}
                            ,251: {destination_plate_number: 1, destination_well_id: 66}
                            ,252: {destination_plate_number: 2, destination_well_id: 66}
                            ,253: {destination_plate_number: 1, destination_well_id: 67}
                            ,254: {destination_plate_number: 2, destination_well_id: 67}
                            ,255: {destination_plate_number: 1, destination_well_id: 68}
                            ,256: {destination_plate_number: 2, destination_well_id: 68}
                            ,257: {destination_plate_number: 1, destination_well_id: 69}
                            ,258: {destination_plate_number: 2, destination_well_id: 69}
                            ,259: {destination_plate_number: 1, destination_well_id: 70}
                            ,260: {destination_plate_number: 2, destination_well_id: 70}
                            ,261: {destination_plate_number: 1, destination_well_id: 71}
                            ,262: {destination_plate_number: 2, destination_well_id: 71}
                            ,263: {destination_plate_number: 1, destination_well_id: 72}
                            ,264: {destination_plate_number: 2, destination_well_id: 72}
                            ,265: {destination_plate_number: 3, destination_well_id: 61}
                            ,266: {destination_plate_number: 4, destination_well_id: 61}
                            ,267: {destination_plate_number: 3, destination_well_id: 62}
                            ,268: {destination_plate_number: 4, destination_well_id: 62}
                            ,269: {destination_plate_number: 3, destination_well_id: 63}
                            ,270: {destination_plate_number: 4, destination_well_id: 63}
                            ,271: {destination_plate_number: 3, destination_well_id: 64}
                            ,272: {destination_plate_number: 4, destination_well_id: 64}
                            ,273: {destination_plate_number: 3, destination_well_id: 65}
                            ,274: {destination_plate_number: 4, destination_well_id: 65}
                            ,275: {destination_plate_number: 3, destination_well_id: 66}
                            ,276: {destination_plate_number: 4, destination_well_id: 66}
                            ,277: {destination_plate_number: 3, destination_well_id: 67}
                            ,278: {destination_plate_number: 4, destination_well_id: 67}
                            ,279: {destination_plate_number: 3, destination_well_id: 68}
                            ,280: {destination_plate_number: 4, destination_well_id: 68}
                            ,281: {destination_plate_number: 3, destination_well_id: 69}
                            ,282: {destination_plate_number: 4, destination_well_id: 69}
                            ,283: {destination_plate_number: 3, destination_well_id: 70}
                            ,284: {destination_plate_number: 4, destination_well_id: 70}
                            ,285: {destination_plate_number: 3, destination_well_id: 71}
                            ,286: {destination_plate_number: 4, destination_well_id: 71}
                            ,287: {destination_plate_number: 3, destination_well_id: 72}
                            ,288: {destination_plate_number: 4, destination_well_id: 72}
                            ,289: {destination_plate_number: 1, destination_well_id: 73}
                            ,290: {destination_plate_number: 2, destination_well_id: 73}
                            ,291: {destination_plate_number: 1, destination_well_id: 74}
                            ,292: {destination_plate_number: 2, destination_well_id: 74}
                            ,293: {destination_plate_number: 1, destination_well_id: 75}
                            ,294: {destination_plate_number: 2, destination_well_id: 75}
                            ,295: {destination_plate_number: 1, destination_well_id: 76}
                            ,296: {destination_plate_number: 2, destination_well_id: 76}
                            ,297: {destination_plate_number: 1, destination_well_id: 77}
                            ,298: {destination_plate_number: 2, destination_well_id: 77}
                            ,299: {destination_plate_number: 1, destination_well_id: 78}
                            ,300: {destination_plate_number: 2, destination_well_id: 78}
                            ,301: {destination_plate_number: 1, destination_well_id: 79}
                            ,302: {destination_plate_number: 2, destination_well_id: 79}
                            ,303: {destination_plate_number: 1, destination_well_id: 80}
                            ,304: {destination_plate_number: 2, destination_well_id: 80}
                            ,305: {destination_plate_number: 1, destination_well_id: 81}
                            ,306: {destination_plate_number: 2, destination_well_id: 81}
                            ,307: {destination_plate_number: 1, destination_well_id: 82}
                            ,308: {destination_plate_number: 2, destination_well_id: 82}
                            ,309: {destination_plate_number: 1, destination_well_id: 83}
                            ,310: {destination_plate_number: 2, destination_well_id: 83}
                            ,311: {destination_plate_number: 1, destination_well_id: 84}
                            ,312: {destination_plate_number: 2, destination_well_id: 84}
                            ,313: {destination_plate_number: 3, destination_well_id: 73}
                            ,314: {destination_plate_number: 4, destination_well_id: 73}
                            ,315: {destination_plate_number: 3, destination_well_id: 74}
                            ,316: {destination_plate_number: 4, destination_well_id: 74}
                            ,317: {destination_plate_number: 3, destination_well_id: 75}
                            ,318: {destination_plate_number: 4, destination_well_id: 75}
                            ,319: {destination_plate_number: 3, destination_well_id: 76}
                            ,320: {destination_plate_number: 4, destination_well_id: 76}
                            ,321: {destination_plate_number: 3, destination_well_id: 77}
                            ,322: {destination_plate_number: 4, destination_well_id: 77}
                            ,323: {destination_plate_number: 3, destination_well_id: 78}
                            ,324: {destination_plate_number: 4, destination_well_id: 78}
                            ,325: {destination_plate_number: 3, destination_well_id: 79}
                            ,326: {destination_plate_number: 4, destination_well_id: 79}
                            ,327: {destination_plate_number: 3, destination_well_id: 80}
                            ,328: {destination_plate_number: 4, destination_well_id: 80}
                            ,329: {destination_plate_number: 3, destination_well_id: 81}
                            ,330: {destination_plate_number: 4, destination_well_id: 81}
                            ,331: {destination_plate_number: 3, destination_well_id: 82}
                            ,332: {destination_plate_number: 4, destination_well_id: 82}
                            ,333: {destination_plate_number: 3, destination_well_id: 83}
                            ,334: {destination_plate_number: 4, destination_well_id: 83}
                            ,335: {destination_plate_number: 3, destination_well_id: 84}
                            ,336: {destination_plate_number: 4, destination_well_id: 84}
                            ,337: {destination_plate_number: 1, destination_well_id: 85}
                            ,338: {destination_plate_number: 2, destination_well_id: 85}
                            ,339: {destination_plate_number: 1, destination_well_id: 86}
                            ,340: {destination_plate_number: 2, destination_well_id: 86}
                            ,341: {destination_plate_number: 1, destination_well_id: 87}
                            ,342: {destination_plate_number: 2, destination_well_id: 87}
                            ,343: {destination_plate_number: 1, destination_well_id: 88}
                            ,344: {destination_plate_number: 2, destination_well_id: 88}
                            ,345: {destination_plate_number: 1, destination_well_id: 89}
                            ,346: {destination_plate_number: 2, destination_well_id: 89}
                            ,347: {destination_plate_number: 1, destination_well_id: 90}
                            ,348: {destination_plate_number: 2, destination_well_id: 90}
                            ,349: {destination_plate_number: 1, destination_well_id: 91}
                            ,350: {destination_plate_number: 2, destination_well_id: 91}
                            ,351: {destination_plate_number: 1, destination_well_id: 92}
                            ,352: {destination_plate_number: 2, destination_well_id: 92}
                            ,353: {destination_plate_number: 1, destination_well_id: 93}
                            ,354: {destination_plate_number: 2, destination_well_id: 93}
                            ,355: {destination_plate_number: 1, destination_well_id: 94}
                            ,356: {destination_plate_number: 2, destination_well_id: 94}
                            ,357: {destination_plate_number: 1, destination_well_id: 95}
                            ,358: {destination_plate_number: 2, destination_well_id: 95}
                            ,359: {destination_plate_number: 1, destination_well_id: 96}
                            ,360: {destination_plate_number: 2, destination_well_id: 96}
                            ,361: {destination_plate_number: 3, destination_well_id: 85}
                            ,362: {destination_plate_number: 4, destination_well_id: 85}
                            ,363: {destination_plate_number: 3, destination_well_id: 86}
                            ,364: {destination_plate_number: 4, destination_well_id: 86}
                            ,365: {destination_plate_number: 3, destination_well_id: 87}
                            ,366: {destination_plate_number: 4, destination_well_id: 87}
                            ,367: {destination_plate_number: 3, destination_well_id: 88}
                            ,368: {destination_plate_number: 4, destination_well_id: 88}
                            ,369: {destination_plate_number: 3, destination_well_id: 89}
                            ,370: {destination_plate_number: 4, destination_well_id: 89}
                            ,371: {destination_plate_number: 3, destination_well_id: 90}
                            ,372: {destination_plate_number: 4, destination_well_id: 90}
                            ,373: {destination_plate_number: 3, destination_well_id: 91}
                            ,374: {destination_plate_number: 4, destination_well_id: 91}
                            ,375: {destination_plate_number: 3, destination_well_id: 92}
                            ,376: {destination_plate_number: 4, destination_well_id: 92}
                            ,377: {destination_plate_number: 3, destination_well_id: 93}
                            ,378: {destination_plate_number: 4, destination_well_id: 93}
                            ,379: {destination_plate_number: 3, destination_well_id: 94}
                            ,380: {destination_plate_number: 4, destination_well_id: 94}
                            ,381: {destination_plate_number: 3, destination_well_id: 95}
                            ,382: {destination_plate_number: 4, destination_well_id: 95}
                            ,383: {destination_plate_number: 3, destination_well_id: 96}
                            ,384: {destination_plate_number: 4, destination_well_id: 96}
                        }
                    ]
                }
                ,14: {  // keyed to sample_transfer_template_id in the database
                    description: '96 to 2x48'
                    ,type: 'hamilton'
                    ,source: {
                        plateCount: 1
                        ,wellCount: 96
                        ,plateTypeId: 'SPTT_0005'
                        ,variablePlateCount: false
                    }
                    ,destination:{
                        plateCount: 2
                        ,wellCount: 48
                        ,plateTypeId: 'SPTT_0004'
                        ,variablePlateCount: false
                        ,plateTitles: ['Left:&nbsp;&nbsp;','Right:&nbsp;']
                    }
                    ,plateWellToWellMaps: [ // array of source plates
                        {   // index in plate_well_to_well_map array = source_plate_index
                            1: {destination_plate_number: 1 ,destination_well_id: 1}
                            ,2: {destination_plate_number: 1 ,destination_well_id: 2}
                            ,3: {destination_plate_number: 1 ,destination_well_id: 3}
                            ,4: {destination_plate_number: 1 ,destination_well_id: 4}
                            ,5: {destination_plate_number: 1 ,destination_well_id: 5}
                            ,6: {destination_plate_number: 1 ,destination_well_id: 6}
                            ,7: {destination_plate_number: 2 ,destination_well_id: 1}
                            ,8: {destination_plate_number: 2 ,destination_well_id: 2}
                            ,9: {destination_plate_number: 2 ,destination_well_id: 3}
                            ,10: {destination_plate_number: 2 ,destination_well_id: 4}
                            ,11: {destination_plate_number: 2 ,destination_well_id: 5}
                            ,12: {destination_plate_number: 2 ,destination_well_id: 6}
                            ,13: {destination_plate_number: 1 ,destination_well_id: 7}
                            ,14: {destination_plate_number: 1 ,destination_well_id: 8}
                            ,15: {destination_plate_number: 1 ,destination_well_id: 9}
                            ,16: {destination_plate_number: 1 ,destination_well_id: 10}
                            ,17: {destination_plate_number: 1 ,destination_well_id: 11}
                            ,18: {destination_plate_number: 1 ,destination_well_id: 12}
                            ,19: {destination_plate_number: 2 ,destination_well_id: 7}
                            ,20: {destination_plate_number: 2 ,destination_well_id: 8}
                            ,21: {destination_plate_number: 2 ,destination_well_id: 9}
                            ,22: {destination_plate_number: 2 ,destination_well_id: 10}
                            ,23: {destination_plate_number: 2 ,destination_well_id: 11}
                            ,24: {destination_plate_number: 2 ,destination_well_id: 12}
                            ,25: {destination_plate_number: 1 ,destination_well_id: 13}
                            ,26: {destination_plate_number: 1 ,destination_well_id: 14}
                            ,27: {destination_plate_number: 1 ,destination_well_id: 15}
                            ,28: {destination_plate_number: 1 ,destination_well_id: 16}
                            ,29: {destination_plate_number: 1 ,destination_well_id: 17}
                            ,30: {destination_plate_number: 1 ,destination_well_id: 18}
                            ,31: {destination_plate_number: 2 ,destination_well_id: 13}
                            ,32: {destination_plate_number: 2 ,destination_well_id: 14}
                            ,33: {destination_plate_number: 2 ,destination_well_id: 15}
                            ,34: {destination_plate_number: 2 ,destination_well_id: 16}
                            ,35: {destination_plate_number: 2 ,destination_well_id: 17}
                            ,36: {destination_plate_number: 2 ,destination_well_id: 18}
                            ,37: {destination_plate_number: 1 ,destination_well_id: 19}
                            ,38: {destination_plate_number: 1 ,destination_well_id: 20}
                            ,39: {destination_plate_number: 1 ,destination_well_id: 21}
                            ,40: {destination_plate_number: 1 ,destination_well_id: 22}
                            ,41: {destination_plate_number: 1 ,destination_well_id: 23}
                            ,42: {destination_plate_number: 1 ,destination_well_id: 24}
                            ,43: {destination_plate_number: 2 ,destination_well_id: 19}
                            ,44: {destination_plate_number: 2 ,destination_well_id: 20}
                            ,45: {destination_plate_number: 2 ,destination_well_id: 21}
                            ,46: {destination_plate_number: 2 ,destination_well_id: 22}
                            ,47: {destination_plate_number: 2 ,destination_well_id: 23}
                            ,48: {destination_plate_number: 2 ,destination_well_id: 24}
                            ,49: {destination_plate_number: 1 ,destination_well_id: 25}
                            ,50: {destination_plate_number: 1 ,destination_well_id: 26}
                            ,51: {destination_plate_number: 1 ,destination_well_id: 27}
                            ,52: {destination_plate_number: 1 ,destination_well_id: 28}
                            ,53: {destination_plate_number: 1 ,destination_well_id: 29}
                            ,54: {destination_plate_number: 1 ,destination_well_id: 30}
                            ,55: {destination_plate_number: 2 ,destination_well_id: 25}
                            ,56: {destination_plate_number: 2 ,destination_well_id: 26}
                            ,57: {destination_plate_number: 2 ,destination_well_id: 27}
                            ,58: {destination_plate_number: 2 ,destination_well_id: 28}
                            ,59: {destination_plate_number: 2 ,destination_well_id: 29}
                            ,60: {destination_plate_number: 2 ,destination_well_id: 30}
                            ,61: {destination_plate_number: 1 ,destination_well_id: 31}
                            ,62: {destination_plate_number: 1 ,destination_well_id: 32}
                            ,63: {destination_plate_number: 1 ,destination_well_id: 33}
                            ,64: {destination_plate_number: 1 ,destination_well_id: 34}
                            ,65: {destination_plate_number: 1 ,destination_well_id: 35}
                            ,66: {destination_plate_number: 1 ,destination_well_id: 36}
                            ,67: {destination_plate_number: 2 ,destination_well_id: 31}
                            ,68: {destination_plate_number: 2 ,destination_well_id: 32}
                            ,69: {destination_plate_number: 2 ,destination_well_id: 33}
                            ,70: {destination_plate_number: 2 ,destination_well_id: 34}
                            ,71: {destination_plate_number: 2 ,destination_well_id: 35}
                            ,72: {destination_plate_number: 2 ,destination_well_id: 36}
                            ,73: {destination_plate_number: 1 ,destination_well_id: 37}
                            ,74: {destination_plate_number: 1 ,destination_well_id: 38}
                            ,75: {destination_plate_number: 1 ,destination_well_id: 39}
                            ,76: {destination_plate_number: 1 ,destination_well_id: 40}
                            ,77: {destination_plate_number: 1 ,destination_well_id: 41}
                            ,78: {destination_plate_number: 1 ,destination_well_id: 42}
                            ,79: {destination_plate_number: 2 ,destination_well_id: 37}
                            ,80: {destination_plate_number: 2 ,destination_well_id: 38}
                            ,81: {destination_plate_number: 2 ,destination_well_id: 39}
                            ,82: {destination_plate_number: 2 ,destination_well_id: 40}
                            ,83: {destination_plate_number: 2 ,destination_well_id: 41}
                            ,84: {destination_plate_number: 2 ,destination_well_id: 42}
                            ,85: {destination_plate_number: 1 ,destination_well_id: 43}
                            ,86: {destination_plate_number: 1 ,destination_well_id: 44}
                            ,87: {destination_plate_number: 1 ,destination_well_id: 45}
                            ,88: {destination_plate_number: 1 ,destination_well_id: 46}
                            ,89: {destination_plate_number: 1 ,destination_well_id: 47}
                            ,90: {destination_plate_number: 1 ,destination_well_id: 48}
                            ,91: {destination_plate_number: 2 ,destination_well_id: 43}
                            ,92: {destination_plate_number: 2 ,destination_well_id: 44}
                            ,93: {destination_plate_number: 2 ,destination_well_id: 45}
                            ,94: {destination_plate_number: 2 ,destination_well_id: 46}
                            ,95: {destination_plate_number: 2 ,destination_well_id: 47}
                            ,96: {destination_plate_number: 2 ,destination_well_id: 48}
                        }
                    ]
                }
                ,16: {  // keyed to sample_transfer_template_id in the database
                    description: 'Manual picking to nx 96'
                    ,type: 'user_specified'
                    ,source: {
                        plateCount: 1
                        ,plateTypeId: 'SPTT_0004'
                        ,variablePlateCount: true
                    }
                    ,destination: {
                        plateCount: 0
                        ,plateTypeId: 'SPTT_0005'
                        ,variablePlateCount: true
                    }
                }
                ,18: {  // keyed to sample_transfer_template_id in the database
                    description: '4x96 to 384'
                    ,type: 'standard_template'
                    ,source: {
                        plateCount: 4
                        ,wellCount: 96
                        ,plateTypeId: 'SPTT_0005'
                        ,variablePlateCount: false
                        ,plateTitles: ['Quadrant&nbsp;1:&nbsp;','Quadrant&nbsp;2:&nbsp;','Quadrant&nbsp;3:&nbsp;','Quadrant&nbsp;4:&nbsp;']
                    }
                    ,destination:{
                        plateCount: 1
                        ,wellCount: 384
                        ,plateTypeId: 'SPTT_0006'
                        ,variablePlateCount: false
                    }
                    ,plateWellToWellMaps: [
                        {
                            1:{destination_plate_number:1,destination_well_id:1}
                            ,2:{destination_plate_number:1,destination_well_id:3}
                            ,3:{destination_plate_number:1,destination_well_id:5}
                            ,4:{destination_plate_number:1,destination_well_id:7}
                            ,5:{destination_plate_number:1,destination_well_id:9}
                            ,6:{destination_plate_number:1,destination_well_id:11}
                            ,7:{destination_plate_number:1,destination_well_id:13}
                            ,8:{destination_plate_number:1,destination_well_id:15}
                            ,9:{destination_plate_number:1,destination_well_id:17}
                            ,10:{destination_plate_number:1,destination_well_id:19}
                            ,11:{destination_plate_number:1,destination_well_id:21}
                            ,12:{destination_plate_number:1,destination_well_id:23}
                            ,13:{destination_plate_number:1,destination_well_id:49}
                            ,14:{destination_plate_number:1,destination_well_id:51}
                            ,15:{destination_plate_number:1,destination_well_id:53}
                            ,16:{destination_plate_number:1,destination_well_id:55}
                            ,17:{destination_plate_number:1,destination_well_id:57}
                            ,18:{destination_plate_number:1,destination_well_id:59}
                            ,19:{destination_plate_number:1,destination_well_id:61}
                            ,20:{destination_plate_number:1,destination_well_id:63}
                            ,21:{destination_plate_number:1,destination_well_id:65}
                            ,22:{destination_plate_number:1,destination_well_id:67}
                            ,23:{destination_plate_number:1,destination_well_id:69}
                            ,24:{destination_plate_number:1,destination_well_id:71}
                            ,25:{destination_plate_number:1,destination_well_id:97}
                            ,26:{destination_plate_number:1,destination_well_id:99}
                            ,27:{destination_plate_number:1,destination_well_id:101}
                            ,28:{destination_plate_number:1,destination_well_id:103}
                            ,29:{destination_plate_number:1,destination_well_id:105}
                            ,30:{destination_plate_number:1,destination_well_id:107}
                            ,31:{destination_plate_number:1,destination_well_id:109}
                            ,32:{destination_plate_number:1,destination_well_id:111}
                            ,33:{destination_plate_number:1,destination_well_id:113}
                            ,34:{destination_plate_number:1,destination_well_id:115}
                            ,35:{destination_plate_number:1,destination_well_id:117}
                            ,36:{destination_plate_number:1,destination_well_id:119}
                            ,37:{destination_plate_number:1,destination_well_id:145}
                            ,38:{destination_plate_number:1,destination_well_id:147}
                            ,39:{destination_plate_number:1,destination_well_id:149}
                            ,40:{destination_plate_number:1,destination_well_id:151}
                            ,41:{destination_plate_number:1,destination_well_id:153}
                            ,42:{destination_plate_number:1,destination_well_id:155}
                            ,43:{destination_plate_number:1,destination_well_id:157}
                            ,44:{destination_plate_number:1,destination_well_id:159}
                            ,45:{destination_plate_number:1,destination_well_id:161}
                            ,46:{destination_plate_number:1,destination_well_id:163}
                            ,47:{destination_plate_number:1,destination_well_id:165}
                            ,48:{destination_plate_number:1,destination_well_id:167}
                            ,49:{destination_plate_number:1,destination_well_id:193}
                            ,50:{destination_plate_number:1,destination_well_id:195}
                            ,51:{destination_plate_number:1,destination_well_id:197}
                            ,52:{destination_plate_number:1,destination_well_id:199}
                            ,53:{destination_plate_number:1,destination_well_id:201}
                            ,54:{destination_plate_number:1,destination_well_id:203}
                            ,55:{destination_plate_number:1,destination_well_id:205}
                            ,56:{destination_plate_number:1,destination_well_id:207}
                            ,57:{destination_plate_number:1,destination_well_id:209}
                            ,58:{destination_plate_number:1,destination_well_id:211}
                            ,59:{destination_plate_number:1,destination_well_id:213}
                            ,60:{destination_plate_number:1,destination_well_id:215}
                            ,61:{destination_plate_number:1,destination_well_id:241}
                            ,62:{destination_plate_number:1,destination_well_id:243}
                            ,63:{destination_plate_number:1,destination_well_id:245}
                            ,64:{destination_plate_number:1,destination_well_id:247}
                            ,65:{destination_plate_number:1,destination_well_id:249}
                            ,66:{destination_plate_number:1,destination_well_id:251}
                            ,67:{destination_plate_number:1,destination_well_id:253}
                            ,68:{destination_plate_number:1,destination_well_id:255}
                            ,69:{destination_plate_number:1,destination_well_id:257}
                            ,70:{destination_plate_number:1,destination_well_id:259}
                            ,71:{destination_plate_number:1,destination_well_id:261}
                            ,72:{destination_plate_number:1,destination_well_id:263}
                            ,73:{destination_plate_number:1,destination_well_id:289}
                            ,74:{destination_plate_number:1,destination_well_id:291}
                            ,75:{destination_plate_number:1,destination_well_id:293}
                            ,76:{destination_plate_number:1,destination_well_id:295}
                            ,77:{destination_plate_number:1,destination_well_id:297}
                            ,78:{destination_plate_number:1,destination_well_id:299}
                            ,79:{destination_plate_number:1,destination_well_id:301}
                            ,80:{destination_plate_number:1,destination_well_id:303}
                            ,81:{destination_plate_number:1,destination_well_id:305}
                            ,82:{destination_plate_number:1,destination_well_id:307}
                            ,83:{destination_plate_number:1,destination_well_id:309}
                            ,84:{destination_plate_number:1,destination_well_id:311}
                            ,85:{destination_plate_number:1,destination_well_id:337}
                            ,86:{destination_plate_number:1,destination_well_id:339}
                            ,87:{destination_plate_number:1,destination_well_id:341}
                            ,88:{destination_plate_number:1,destination_well_id:343}
                            ,89:{destination_plate_number:1,destination_well_id:345}
                            ,90:{destination_plate_number:1,destination_well_id:347}
                            ,91:{destination_plate_number:1,destination_well_id:349}
                            ,92:{destination_plate_number:1,destination_well_id:351}
                            ,93:{destination_plate_number:1,destination_well_id:353}
                            ,94:{destination_plate_number:1,destination_well_id:355}
                            ,95:{destination_plate_number:1,destination_well_id:357}
                            ,96:{destination_plate_number:1,destination_well_id:359}
                        }
                        ,{
                            1:{destination_plate_number:1,destination_well_id:2}
                            ,2:{destination_plate_number:1,destination_well_id:4}
                            ,3:{destination_plate_number:1,destination_well_id:6}
                            ,4:{destination_plate_number:1,destination_well_id:8}
                            ,5:{destination_plate_number:1,destination_well_id:10}
                            ,6:{destination_plate_number:1,destination_well_id:12}
                            ,7:{destination_plate_number:1,destination_well_id:14}
                            ,8:{destination_plate_number:1,destination_well_id:16}
                            ,9:{destination_plate_number:1,destination_well_id:18}
                            ,10:{destination_plate_number:1,destination_well_id:20}
                            ,11:{destination_plate_number:1,destination_well_id:22}
                            ,12:{destination_plate_number:1,destination_well_id:24}
                            ,13:{destination_plate_number:1,destination_well_id:50}
                            ,14:{destination_plate_number:1,destination_well_id:52}
                            ,15:{destination_plate_number:1,destination_well_id:54}
                            ,16:{destination_plate_number:1,destination_well_id:56}
                            ,17:{destination_plate_number:1,destination_well_id:58}
                            ,18:{destination_plate_number:1,destination_well_id:60}
                            ,19:{destination_plate_number:1,destination_well_id:62}
                            ,20:{destination_plate_number:1,destination_well_id:64}
                            ,21:{destination_plate_number:1,destination_well_id:66}
                            ,22:{destination_plate_number:1,destination_well_id:68}
                            ,23:{destination_plate_number:1,destination_well_id:70}
                            ,24:{destination_plate_number:1,destination_well_id:72}
                            ,25:{destination_plate_number:1,destination_well_id:98}
                            ,26:{destination_plate_number:1,destination_well_id:100}
                            ,27:{destination_plate_number:1,destination_well_id:102}
                            ,28:{destination_plate_number:1,destination_well_id:104}
                            ,29:{destination_plate_number:1,destination_well_id:106}
                            ,30:{destination_plate_number:1,destination_well_id:108}
                            ,31:{destination_plate_number:1,destination_well_id:110}
                            ,32:{destination_plate_number:1,destination_well_id:112}
                            ,33:{destination_plate_number:1,destination_well_id:114}
                            ,34:{destination_plate_number:1,destination_well_id:116}
                            ,35:{destination_plate_number:1,destination_well_id:118}
                            ,36:{destination_plate_number:1,destination_well_id:120}
                            ,37:{destination_plate_number:1,destination_well_id:146}
                            ,38:{destination_plate_number:1,destination_well_id:148}
                            ,39:{destination_plate_number:1,destination_well_id:150}
                            ,40:{destination_plate_number:1,destination_well_id:152}
                            ,41:{destination_plate_number:1,destination_well_id:154}
                            ,42:{destination_plate_number:1,destination_well_id:156}
                            ,43:{destination_plate_number:1,destination_well_id:158}
                            ,44:{destination_plate_number:1,destination_well_id:160}
                            ,45:{destination_plate_number:1,destination_well_id:162}
                            ,46:{destination_plate_number:1,destination_well_id:164}
                            ,47:{destination_plate_number:1,destination_well_id:166}
                            ,48:{destination_plate_number:1,destination_well_id:168}
                            ,49:{destination_plate_number:1,destination_well_id:194}
                            ,50:{destination_plate_number:1,destination_well_id:196}
                            ,51:{destination_plate_number:1,destination_well_id:198}
                            ,52:{destination_plate_number:1,destination_well_id:200}
                            ,53:{destination_plate_number:1,destination_well_id:202}
                            ,54:{destination_plate_number:1,destination_well_id:204}
                            ,55:{destination_plate_number:1,destination_well_id:206}
                            ,56:{destination_plate_number:1,destination_well_id:208}
                            ,57:{destination_plate_number:1,destination_well_id:210}
                            ,58:{destination_plate_number:1,destination_well_id:212}
                            ,59:{destination_plate_number:1,destination_well_id:214}
                            ,60:{destination_plate_number:1,destination_well_id:216}
                            ,61:{destination_plate_number:1,destination_well_id:242}
                            ,62:{destination_plate_number:1,destination_well_id:244}
                            ,63:{destination_plate_number:1,destination_well_id:246}
                            ,64:{destination_plate_number:1,destination_well_id:248}
                            ,65:{destination_plate_number:1,destination_well_id:250}
                            ,66:{destination_plate_number:1,destination_well_id:252}
                            ,67:{destination_plate_number:1,destination_well_id:254}
                            ,68:{destination_plate_number:1,destination_well_id:256}
                            ,69:{destination_plate_number:1,destination_well_id:258}
                            ,70:{destination_plate_number:1,destination_well_id:260}
                            ,71:{destination_plate_number:1,destination_well_id:262}
                            ,72:{destination_plate_number:1,destination_well_id:264}
                            ,73:{destination_plate_number:1,destination_well_id:290}
                            ,74:{destination_plate_number:1,destination_well_id:292}
                            ,75:{destination_plate_number:1,destination_well_id:294}
                            ,76:{destination_plate_number:1,destination_well_id:296}
                            ,77:{destination_plate_number:1,destination_well_id:298}
                            ,78:{destination_plate_number:1,destination_well_id:300}
                            ,79:{destination_plate_number:1,destination_well_id:302}
                            ,80:{destination_plate_number:1,destination_well_id:304}
                            ,81:{destination_plate_number:1,destination_well_id:306}
                            ,82:{destination_plate_number:1,destination_well_id:308}
                            ,83:{destination_plate_number:1,destination_well_id:310}
                            ,84:{destination_plate_number:1,destination_well_id:312}
                            ,85:{destination_plate_number:1,destination_well_id:338}
                            ,86:{destination_plate_number:1,destination_well_id:340}
                            ,87:{destination_plate_number:1,destination_well_id:342}
                            ,88:{destination_plate_number:1,destination_well_id:344}
                            ,89:{destination_plate_number:1,destination_well_id:346}
                            ,90:{destination_plate_number:1,destination_well_id:348}
                            ,91:{destination_plate_number:1,destination_well_id:350}
                            ,92:{destination_plate_number:1,destination_well_id:352}
                            ,93:{destination_plate_number:1,destination_well_id:354}
                            ,94:{destination_plate_number:1,destination_well_id:356}
                            ,95:{destination_plate_number:1,destination_well_id:358}
                            ,96:{destination_plate_number:1,destination_well_id:360}
                        }
                        ,{
                            1:{destination_plate_number:1,destination_well_id:25}
                            ,2:{destination_plate_number:1,destination_well_id:27}
                            ,3:{destination_plate_number:1,destination_well_id:29}
                            ,4:{destination_plate_number:1,destination_well_id:31}
                            ,5:{destination_plate_number:1,destination_well_id:33}
                            ,6:{destination_plate_number:1,destination_well_id:35}
                            ,7:{destination_plate_number:1,destination_well_id:37}
                            ,8:{destination_plate_number:1,destination_well_id:39}
                            ,9:{destination_plate_number:1,destination_well_id:41}
                            ,10:{destination_plate_number:1,destination_well_id:43}
                            ,11:{destination_plate_number:1,destination_well_id:45}
                            ,12:{destination_plate_number:1,destination_well_id:47}
                            ,13:{destination_plate_number:1,destination_well_id:73}
                            ,14:{destination_plate_number:1,destination_well_id:75}
                            ,15:{destination_plate_number:1,destination_well_id:77}
                            ,16:{destination_plate_number:1,destination_well_id:79}
                            ,17:{destination_plate_number:1,destination_well_id:81}
                            ,18:{destination_plate_number:1,destination_well_id:83}
                            ,19:{destination_plate_number:1,destination_well_id:85}
                            ,20:{destination_plate_number:1,destination_well_id:87}
                            ,21:{destination_plate_number:1,destination_well_id:89}
                            ,22:{destination_plate_number:1,destination_well_id:91}
                            ,23:{destination_plate_number:1,destination_well_id:93}
                            ,24:{destination_plate_number:1,destination_well_id:95}
                            ,25:{destination_plate_number:1,destination_well_id:121}
                            ,26:{destination_plate_number:1,destination_well_id:123}
                            ,27:{destination_plate_number:1,destination_well_id:125}
                            ,28:{destination_plate_number:1,destination_well_id:127}
                            ,29:{destination_plate_number:1,destination_well_id:129}
                            ,30:{destination_plate_number:1,destination_well_id:131}
                            ,31:{destination_plate_number:1,destination_well_id:133}
                            ,32:{destination_plate_number:1,destination_well_id:135}
                            ,33:{destination_plate_number:1,destination_well_id:137}
                            ,34:{destination_plate_number:1,destination_well_id:139}
                            ,35:{destination_plate_number:1,destination_well_id:141}
                            ,36:{destination_plate_number:1,destination_well_id:143}
                            ,37:{destination_plate_number:1,destination_well_id:169}
                            ,38:{destination_plate_number:1,destination_well_id:171}
                            ,39:{destination_plate_number:1,destination_well_id:173}
                            ,40:{destination_plate_number:1,destination_well_id:175}
                            ,41:{destination_plate_number:1,destination_well_id:177}
                            ,42:{destination_plate_number:1,destination_well_id:179}
                            ,43:{destination_plate_number:1,destination_well_id:181}
                            ,44:{destination_plate_number:1,destination_well_id:183}
                            ,45:{destination_plate_number:1,destination_well_id:185}
                            ,46:{destination_plate_number:1,destination_well_id:187}
                            ,47:{destination_plate_number:1,destination_well_id:189}
                            ,48:{destination_plate_number:1,destination_well_id:191}
                            ,49:{destination_plate_number:1,destination_well_id:217}
                            ,50:{destination_plate_number:1,destination_well_id:219}
                            ,51:{destination_plate_number:1,destination_well_id:221}
                            ,52:{destination_plate_number:1,destination_well_id:223}
                            ,53:{destination_plate_number:1,destination_well_id:225}
                            ,54:{destination_plate_number:1,destination_well_id:227}
                            ,55:{destination_plate_number:1,destination_well_id:229}
                            ,56:{destination_plate_number:1,destination_well_id:231}
                            ,57:{destination_plate_number:1,destination_well_id:233}
                            ,58:{destination_plate_number:1,destination_well_id:235}
                            ,59:{destination_plate_number:1,destination_well_id:237}
                            ,60:{destination_plate_number:1,destination_well_id:239}
                            ,61:{destination_plate_number:1,destination_well_id:265}
                            ,62:{destination_plate_number:1,destination_well_id:267}
                            ,63:{destination_plate_number:1,destination_well_id:269}
                            ,64:{destination_plate_number:1,destination_well_id:271}
                            ,65:{destination_plate_number:1,destination_well_id:273}
                            ,66:{destination_plate_number:1,destination_well_id:275}
                            ,67:{destination_plate_number:1,destination_well_id:277}
                            ,68:{destination_plate_number:1,destination_well_id:279}
                            ,69:{destination_plate_number:1,destination_well_id:281}
                            ,70:{destination_plate_number:1,destination_well_id:283}
                            ,71:{destination_plate_number:1,destination_well_id:285}
                            ,72:{destination_plate_number:1,destination_well_id:287}
                            ,73:{destination_plate_number:1,destination_well_id:313}
                            ,74:{destination_plate_number:1,destination_well_id:315}
                            ,75:{destination_plate_number:1,destination_well_id:317}
                            ,76:{destination_plate_number:1,destination_well_id:319}
                            ,77:{destination_plate_number:1,destination_well_id:321}
                            ,78:{destination_plate_number:1,destination_well_id:323}
                            ,79:{destination_plate_number:1,destination_well_id:325}
                            ,80:{destination_plate_number:1,destination_well_id:327}
                            ,81:{destination_plate_number:1,destination_well_id:329}
                            ,82:{destination_plate_number:1,destination_well_id:331}
                            ,83:{destination_plate_number:1,destination_well_id:333}
                            ,84:{destination_plate_number:1,destination_well_id:335}
                            ,85:{destination_plate_number:1,destination_well_id:361}
                            ,86:{destination_plate_number:1,destination_well_id:363}
                            ,87:{destination_plate_number:1,destination_well_id:365}
                            ,88:{destination_plate_number:1,destination_well_id:367}
                            ,89:{destination_plate_number:1,destination_well_id:369}
                            ,90:{destination_plate_number:1,destination_well_id:371}
                            ,91:{destination_plate_number:1,destination_well_id:373}
                            ,92:{destination_plate_number:1,destination_well_id:375}
                            ,93:{destination_plate_number:1,destination_well_id:377}
                            ,94:{destination_plate_number:1,destination_well_id:379}
                            ,95:{destination_plate_number:1,destination_well_id:381}
                            ,96:{destination_plate_number:1,destination_well_id:383}
                        }
                        ,{
                            1:{destination_plate_number:1,destination_well_id:26}
                            ,2:{destination_plate_number:1,destination_well_id:28}
                            ,3:{destination_plate_number:1,destination_well_id:30}
                            ,4:{destination_plate_number:1,destination_well_id:32}
                            ,5:{destination_plate_number:1,destination_well_id:34}
                            ,6:{destination_plate_number:1,destination_well_id:36}
                            ,7:{destination_plate_number:1,destination_well_id:38}
                            ,8:{destination_plate_number:1,destination_well_id:40}
                            ,9:{destination_plate_number:1,destination_well_id:42}
                            ,10:{destination_plate_number:1,destination_well_id:44}
                            ,11:{destination_plate_number:1,destination_well_id:46}
                            ,12:{destination_plate_number:1,destination_well_id:48}
                            ,13:{destination_plate_number:1,destination_well_id:74}
                            ,14:{destination_plate_number:1,destination_well_id:76}
                            ,15:{destination_plate_number:1,destination_well_id:78}
                            ,16:{destination_plate_number:1,destination_well_id:80}
                            ,17:{destination_plate_number:1,destination_well_id:82}
                            ,18:{destination_plate_number:1,destination_well_id:84}
                            ,19:{destination_plate_number:1,destination_well_id:86}
                            ,20:{destination_plate_number:1,destination_well_id:88}
                            ,21:{destination_plate_number:1,destination_well_id:90}
                            ,22:{destination_plate_number:1,destination_well_id:92}
                            ,23:{destination_plate_number:1,destination_well_id:94}
                            ,24:{destination_plate_number:1,destination_well_id:96}
                            ,25:{destination_plate_number:1,destination_well_id:122}
                            ,26:{destination_plate_number:1,destination_well_id:124}
                            ,27:{destination_plate_number:1,destination_well_id:126}
                            ,28:{destination_plate_number:1,destination_well_id:128}
                            ,29:{destination_plate_number:1,destination_well_id:130}
                            ,30:{destination_plate_number:1,destination_well_id:132}
                            ,31:{destination_plate_number:1,destination_well_id:134}
                            ,32:{destination_plate_number:1,destination_well_id:136}
                            ,33:{destination_plate_number:1,destination_well_id:138}
                            ,34:{destination_plate_number:1,destination_well_id:140}
                            ,35:{destination_plate_number:1,destination_well_id:142}
                            ,36:{destination_plate_number:1,destination_well_id:144}
                            ,37:{destination_plate_number:1,destination_well_id:170}
                            ,38:{destination_plate_number:1,destination_well_id:172}
                            ,39:{destination_plate_number:1,destination_well_id:174}
                            ,40:{destination_plate_number:1,destination_well_id:176}
                            ,41:{destination_plate_number:1,destination_well_id:178}
                            ,42:{destination_plate_number:1,destination_well_id:180}
                            ,43:{destination_plate_number:1,destination_well_id:182}
                            ,44:{destination_plate_number:1,destination_well_id:184}
                            ,45:{destination_plate_number:1,destination_well_id:186}
                            ,46:{destination_plate_number:1,destination_well_id:188}
                            ,47:{destination_plate_number:1,destination_well_id:190}
                            ,48:{destination_plate_number:1,destination_well_id:192}
                            ,49:{destination_plate_number:1,destination_well_id:218}
                            ,50:{destination_plate_number:1,destination_well_id:220}
                            ,51:{destination_plate_number:1,destination_well_id:222}
                            ,52:{destination_plate_number:1,destination_well_id:224}
                            ,53:{destination_plate_number:1,destination_well_id:226}
                            ,54:{destination_plate_number:1,destination_well_id:228}
                            ,55:{destination_plate_number:1,destination_well_id:230}
                            ,56:{destination_plate_number:1,destination_well_id:232}
                            ,57:{destination_plate_number:1,destination_well_id:234}
                            ,58:{destination_plate_number:1,destination_well_id:236}
                            ,59:{destination_plate_number:1,destination_well_id:238}
                            ,60:{destination_plate_number:1,destination_well_id:240}
                            ,61:{destination_plate_number:1,destination_well_id:266}
                            ,62:{destination_plate_number:1,destination_well_id:268}
                            ,63:{destination_plate_number:1,destination_well_id:270}
                            ,64:{destination_plate_number:1,destination_well_id:272}
                            ,65:{destination_plate_number:1,destination_well_id:274}
                            ,66:{destination_plate_number:1,destination_well_id:276}
                            ,67:{destination_plate_number:1,destination_well_id:278}
                            ,68:{destination_plate_number:1,destination_well_id:280}
                            ,69:{destination_plate_number:1,destination_well_id:282}
                            ,70:{destination_plate_number:1,destination_well_id:284}
                            ,71:{destination_plate_number:1,destination_well_id:286}
                            ,72:{destination_plate_number:1,destination_well_id:288}
                            ,73:{destination_plate_number:1,destination_well_id:314}
                            ,74:{destination_plate_number:1,destination_well_id:316}
                            ,75:{destination_plate_number:1,destination_well_id:318}
                            ,76:{destination_plate_number:1,destination_well_id:320}
                            ,77:{destination_plate_number:1,destination_well_id:322}
                            ,78:{destination_plate_number:1,destination_well_id:324}
                            ,79:{destination_plate_number:1,destination_well_id:326}
                            ,80:{destination_plate_number:1,destination_well_id:328}
                            ,81:{destination_plate_number:1,destination_well_id:330}
                            ,82:{destination_plate_number:1,destination_well_id:332}
                            ,83:{destination_plate_number:1,destination_well_id:334}
                            ,84:{destination_plate_number:1,destination_well_id:336}
                            ,85:{destination_plate_number:1,destination_well_id:362}
                            ,86:{destination_plate_number:1,destination_well_id:364}
                            ,87:{destination_plate_number:1,destination_well_id:366}
                            ,88:{destination_plate_number:1,destination_well_id:368}
                            ,89:{destination_plate_number:1,destination_well_id:370}
                            ,90:{destination_plate_number:1,destination_well_id:372}
                            ,91:{destination_plate_number:1,destination_well_id:374}
                            ,92:{destination_plate_number:1,destination_well_id:376}
                            ,93:{destination_plate_number:1,destination_well_id:378}
                            ,94:{destination_plate_number:1,destination_well_id:380}
                            ,95:{destination_plate_number:1,destination_well_id:382}
                            ,96:{destination_plate_number:1,destination_well_id:384}
                        }
                    ]
                }
                ,20: {  // keyed to sample_transfer_template_id in the database
                    description: 'Hitpick for shipping'
                    ,type: 'user_specified'
                    ,source: {
                        plateCount: 1
                        ,plateTypeId: 'SPTT_0005'
                        ,variablePlateCount: true
                    }
                    ,destination: {
                        plateCount: 0
                        ,variablePlateCount: true
                    }
                }
                ,21: {  // keyed to sample_transfer_template_id in the database
                    description: 'Qpix Log Reading to nx 96'
                    ,type: 'user_specified'
                    ,source: {
                        plateCount: 1
                        ,plateTypeId: 'SPTT_0004'
                        ,variablePlateCount: true
                    }
                    ,destination: {
                        plateCount: 0
                        ,plateTypeId: 'SPTT_0005'
                        ,variablePlateCount: true
                    }
                }
                ,22: {  // keyed to sample_transfer_template_id in the database
                    description: 'Qpix Log Reading to nx 384'
                    ,type: 'user_specified'
                    ,source: {
                        plateCount: 1
                        ,plateTypeId: 'SPTT_0004'
                        ,variablePlateCount: true
                    }
                    ,destination: {
                        plateCount: 0
                        ,plateTypeId: 'SPTT_0006'
                        ,variablePlateCount: true
                    }
                }
                ,23: {  // keyed to sample_transfer_template_id in the database
                    description: 'Plate Merge'
                    ,type: 'standard_template'
                    ,source: {
                        plateCount: 1
                        ,variablePlateCount: true
                    }
                    ,destination: {
                        plateCount: 1
                        ,variablePlateCount: false
                    }
                }
                ,24: {  // keyed to sample_transfer_template_id in the database
                    description: 'Generic Transform'
                    ,type: 'user_specified'
                    ,source: {
                        plateCount: 1
                        ,variablePlateCount: true
                    }
                    ,destination: {
                        plateCount: 1
                        ,variablePlateCount: true
                    }
                }
                ,25: {  // keyed to sample_transfer_template_id in the database
                    description: 'Rebatching for Transformation'
                    ,type: 'standard_template'
                    ,source: {
                        plateCount: 1
                        ,variablePlateCount: true
                        ,plateTypeId: 'SPTT_0006'
                    }
                    ,destination: {
                        plateCount: 0
                        ,variablePlateCount: true
                        ,plateTypeId: 'SPTT_0006'
                    }
                }
                ,26: {  // keyed to sample_transfer_template_id in the database
                    description: 'Fragment Analyzer'
                    ,type: 'standard_template'
                    ,source: {
                        plateCount: 1
                        ,variablePlateCount: true
                    }
                    ,destination: {
                        plateCount: 0
                        ,variablePlateCount: true
                    }
                }
                ,27: {  // keyed to sample_transfer_template_id in the database
                    description: 'NGS QC Pass'
                    ,type: 'standard_template'
                    ,source: {
                        plateCount: 1
                        ,variablePlateCount: true
                    }
                    ,destination: {
                        plateCount: 0
                        ,variablePlateCount: true
                    }
                }
                ,28: {  // keyed to sample_transfer_template_id in the database
                    description: 'Hitpicking for shipping in plates'
                    ,type: 'hamilton'
                    ,source: {
                        plateCount: 5
                        ,variablePlateCount: true
                    }
                    ,destination: {
                        plateCount: 10
                        ,variablePlateCount: true
                    }
                    ,hamiltonDetails: {
                        'HAM04': { // Jupiter 2
                            'left side': {
                                carriers: [
                                    {
                                        startTrack: 13
                                        ,index: 1
                                        ,type: 'L5AC'
                                        ,plates: [
                                            {plateFor: 'source', type: 'SPTT_005', localIndex: 5, dataIndex: 5, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 4, dataIndex: 4, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 3, dataIndex: 3, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 2, dataIndex: 2, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 1, dataIndex: 1}
                                        ]
                                    }
                                    ,{
                                        startTrack: 19
                                        ,index: 2
                                        ,type: 'L5AC'
                                        ,plates: [
                                            {plateFor: 'destination', type: 'SPTT_005', localIndex: 5, dataIndex: 5, optional: true}
                                            ,{plateFor: 'destination', type: 'SPTT_005', localIndex: 4, dataIndex: 4, optional: true}
                                            ,{plateFor: 'destination', type: 'SPTT_005', localIndex: 3, dataIndex: 3, optional: true}
                                            ,{plateFor: 'destination', type: 'SPTT_005', localIndex: 2, dataIndex: 2, optional: true}
                                            ,{plateFor: 'destination', type: 'SPTT_005', localIndex: 1, dataIndex: 1}
                                        ]
                                    }
                                    ,{
                                        startTrack: 25
                                        ,index: 3
                                        ,type: 'L5AC'
                                        ,plates: [
                                            {plateFor: 'destination', type: 'SPTT_005', localIndex: 5, dataIndex: 10, optional: true}
                                            ,{plateFor: 'destination', type: 'SPTT_005', localIndex: 4, dataIndex: 9, optional: true}
                                            ,{plateFor: 'destination', type: 'SPTT_005', localIndex: 3, dataIndex: 8, optional: true}
                                            ,{plateFor: 'destination', type: 'SPTT_005', localIndex: 2, dataIndex: 7, optional: true}
                                            ,{plateFor: 'destination', type: 'SPTT_005', localIndex: 1, dataIndex: 6, optional: true}
                                        ]
                                    }
                                ]
                            }
                        },
                        'HAM01': { // Galactica
                            'main': {
                                carriers: [
                                    {
                                        startTrack: 20
                                        ,index: 1
                                        ,type: 'L5AC'
                                        ,plates: [
                                            {plateFor: 'source', type: 'SPTT_005', localIndex: 5, dataIndex: 5, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 4, dataIndex: 4, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 3, dataIndex: 3, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 2, dataIndex: 2, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 1, dataIndex: 1}
                                        ]
                                    }
                                    ,{
                                        startTrack: 26
                                        ,index: 2
                                        ,type: 'L5AC'
                                        ,plates: [
                                            {plateFor: 'destination', type: 'SPTT_005', localIndex: 5, dataIndex: 5, optional: true}
                                            ,{plateFor: 'destination', type: 'SPTT_005', localIndex: 4, dataIndex: 4, optional: true}
                                            ,{plateFor: 'destination', type: 'SPTT_005', localIndex: 3, dataIndex: 3, optional: true}
                                            ,{plateFor: 'destination', type: 'SPTT_005', localIndex: 2, dataIndex: 2, optional: true}
                                            ,{plateFor: 'destination', type: 'SPTT_005', localIndex: 1, dataIndex: 1}
                                        ]
                                    }
                                    ,{
                                        startTrack: 32
                                        ,index: 3
                                        ,type: 'L5AC'
                                        ,plates: [
                                            {plateFor: 'destination', type: 'SPTT_005', localIndex: 5, dataIndex: 10, optional: true}
                                            ,{plateFor: 'destination', type: 'SPTT_005', localIndex: 4, dataIndex: 9, optional: true}
                                            ,{plateFor: 'destination', type: 'SPTT_005', localIndex: 3, dataIndex: 8, optional: true}
                                            ,{plateFor: 'destination', type: 'SPTT_005', localIndex: 2, dataIndex: 7, optional: true}
                                            ,{plateFor: 'destination', type: 'SPTT_005', localIndex: 1, dataIndex: 6, optional: true}
                                        ]
                                    }
                                ]
                            }
                        }
                        
                    }
                }
                ,29: {  // keyed to sample_transfer_template_id in the database
                    description: 'Reformatting for Purification'
                    ,type: 'standard_template'
                    ,source: {
                        plateCount: 1
                        ,variablePlateCount: true
                    }
                    ,destination: {
                        plateCount: 0
                        ,variablePlateCount: true
                    }
                }
                ,30: {  // keyed to sample_transfer_template_id in the database
                    description: 'NGS Barcoding'
                    ,type: 'standard_template'
                    ,source: {
                        plateCount: 1
                        ,variablePlateCount: true
                    }
                    ,destination: {
                        plateCount: 0
                        ,variablePlateCount: false
                    }
                }
                ,31: {  // keyed to sample_transfer_template_id in the database
                    description: 'NGS: sample sheet generation'
                    ,type: 'standard_template'
                    ,source: {
                        plateCount: 1
                        ,variablePlateCount: true
                    }
                    ,destination: {
                        plateCount: 1
                        ,variablePlateCount: false
                    }
                }
                ,32: {  // keyed to sample_transfer_template_id in the database
                    description: 'Hitpicking for miniprep'
                    ,type: 'hamilton'
                    ,source: {
                        plateCount: 32
                        ,variablePlateCount: true
                    }
                    ,destination: {
                        plateCount: 4
                        ,variablePlateCount: true
                    }
                    ,hamiltonDetails: {
                        'HAM04': { // Jupiter 2
                            'left side': {
                                carriers: [
                                    {
                                        startTrack: 1
                                        ,index: 1
                                        ,type: 'L5AC'
                                        ,plates: [
                                            {plateFor: 'source', type: 'SPTT_005', localIndex: 5, dataIndex: 5, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 4, dataIndex: 4, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 3, dataIndex: 3, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 2, dataIndex: 2, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 1, dataIndex: 1}
                                        ]
                                    }
                                    ,{
                                        startTrack: 7
                                        ,index: 2
                                        ,type: 'L5AC'
                                        ,plates: [
                                            {plateFor: 'source', type: 'SPTT_005', localIndex: 5, dataIndex: 10, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 4, dataIndex: 9, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 3, dataIndex: 8, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 2, dataIndex: 7, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 1, dataIndex: 6, optional: true}
                                        ]
                                    }
                                    ,{
                                        startTrack: 13
                                        ,index: 3
                                        ,type: 'L5AC'
                                        ,plates: [
                                            {plateFor: 'source', type: 'SPTT_005', localIndex: 5, dataIndex: 15, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 4, dataIndex: 14, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 3, dataIndex: 13, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 2, dataIndex: 12, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 1, dataIndex: 11, optional: true}
                                        ]
                                    }
                                    ,{
                                        startTrack: 19
                                        ,index: 4
                                        ,type: 'L5AC'
                                        ,plates: [
                                            {plateFor: 'source', type: 'SPTT_005', localIndex: 5, dataIndex: 20, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 4, dataIndex: 19, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 3, dataIndex: 18, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 2, dataIndex: 17, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 1, dataIndex: 16, optional: true}
                                        ]
                                    }
                                    ,{
                                        startTrack: 25
                                        ,index: 5
                                        ,type: 'L5AC'
                                        ,plates: [
                                            {plateFor: 'source', type: 'SPTT_005', localIndex: 5, dataIndex: 25, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 4, dataIndex: 24, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 3, dataIndex: 23, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 2, dataIndex: 22, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 1, dataIndex: 21, optional: true}
                                        ]
                                    }
                                ]
                            }
                            ,'right side': {
                                carriers: [
                                    {
                                        startTrack: 43
                                        ,index: 6
                                        ,type: 'L5AC'
                                        ,plates: [
                                            {plateFor: 'source', type: 'SPTT_005', localIndex: 5, dataIndex: 30, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 4, dataIndex: 29, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 3, dataIndex: 28, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 2, dataIndex: 27, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 1, dataIndex: 26, optional: true}
                                        ]
                                    }
                                    ,{
                                        startTrack: 49
                                        ,index: 7
                                        ,type: 'L5AC'
                                        ,plates: [
                                            {plateFor: 'source', type: 'SPTT_005', localIndex: 5, dataIndex: 32, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 4, dataIndex: 31, optional: true}
                                            ,{unused: true, localIndex: 3}
                                            ,{unused: true, localIndex: 2}
                                            ,{unused: true, localIndex: 1}
                                        ]
                                    }
                                    ,{
                                        startTrack: 55
                                        ,index: 8
                                        ,type: 'L5AC'
                                        ,plates: [
                                            {unused: true, localIndex: 5}
                                            ,{plateFor: 'destination', type: 'SPTT_005', localIndex: 4, dataIndex: 4, optional: true}
                                            ,{plateFor: 'destination', type: 'SPTT_005', localIndex: 3, dataIndex: 3, optional: true}
                                            ,{plateFor: 'destination', type: 'SPTT_005', localIndex: 2, dataIndex: 2, optional: true}
                                            ,{plateFor: 'destination', type: 'SPTT_005', localIndex: 1, dataIndex: 1}
                                        ]
                                    }
                                ]
                            }
                        }
                        
                    }
                }
                ,33: {  // keyed to sample_transfer_template_id in the database
                    description: 'Hitpicking for shipping in tubes'
                    ,type: 'hamilton'
                    ,source: {
                        plateCount: 5
                        ,variablePlateCount: true
                    }
                    ,destination: {
                        plateCount: 96
                        ,variablePlateCount: true
                    }
                    ,hamiltonDetails: {
                        'HAM04': { // Jupiter 2
                            'left side': {
                                carriers: [
                                    {
                                        startTrack: 13
                                        ,index: 1
                                        ,type: 'L5AC'
                                        ,plates: [
                                            {plateFor: 'source', type: 'SPTT_005', localIndex: 5, dataIndex: 5, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 4, dataIndex: 4, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 3, dataIndex: 3, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 2, dataIndex: 2, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 1, dataIndex: 1}
                                        ]
                                    }
                                    ,{
                                        startTrack: 22
                                        ,index: 2
                                        ,type: Constants.SHIPPING_TUBES_CARRIER_TYPE
                                        ,plates: [
                                            {plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 1, dataIndex: 1}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 2, dataIndex: 2}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 3, dataIndex: 3}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 4, dataIndex: 4}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 5, dataIndex: 5}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 6, dataIndex: 6}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 7, dataIndex: 7}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 8, dataIndex: 8}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 9, dataIndex: 9}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 10, dataIndex: 10}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 11, dataIndex: 11}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 12, dataIndex: 12}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 13, dataIndex: 13}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 14, dataIndex: 14}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 15, dataIndex: 15}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 16, dataIndex: 16}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 17, dataIndex: 17}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 18, dataIndex: 18}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 19, dataIndex: 19}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 20, dataIndex: 20}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 21, dataIndex: 21}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 22, dataIndex: 22}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 23, dataIndex: 23}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 24, dataIndex: 24}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 25, dataIndex: 25}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 26, dataIndex: 26}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 27, dataIndex: 27}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 28, dataIndex: 28}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 29, dataIndex: 29}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 30, dataIndex: 30}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 31, dataIndex: 31}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 32, dataIndex: 32}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 33, dataIndex: 33}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 34, dataIndex: 34}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 35, dataIndex: 35}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 36, dataIndex: 36}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 37, dataIndex: 37}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 38, dataIndex: 38}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 39, dataIndex: 39}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 40, dataIndex: 40}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 41, dataIndex: 41}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 42, dataIndex: 42}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 43, dataIndex: 43}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 44, dataIndex: 44}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 45, dataIndex: 45}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 46, dataIndex: 46}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 47, dataIndex: 47}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 48, dataIndex: 48}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 49, dataIndex: 49}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 50, dataIndex: 50}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 51, dataIndex: 51}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 52, dataIndex: 52}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 53, dataIndex: 53}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 54, dataIndex: 54}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 55, dataIndex: 55}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 56, dataIndex: 56}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 57, dataIndex: 57}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 58, dataIndex: 58}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 59, dataIndex: 59}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 60, dataIndex: 60}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 61, dataIndex: 61}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 62, dataIndex: 62}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 63, dataIndex: 63}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 64, dataIndex: 64}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 65, dataIndex: 65}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 66, dataIndex: 66}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 67, dataIndex: 67}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 68, dataIndex: 68}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 69, dataIndex: 69}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 70, dataIndex: 70}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 71, dataIndex: 71}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 72, dataIndex: 72}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 73, dataIndex: 73}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 74, dataIndex: 74}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 75, dataIndex: 75}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 76, dataIndex: 76}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 77, dataIndex: 77}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 78, dataIndex: 78}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 79, dataIndex: 79}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 80, dataIndex: 80}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 81, dataIndex: 81}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 82, dataIndex: 82}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 83, dataIndex: 83}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 84, dataIndex: 84}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 85, dataIndex: 85}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 86, dataIndex: 86}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 87, dataIndex: 87}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 88, dataIndex: 88}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 89, dataIndex: 89}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 90, dataIndex: 90}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 91, dataIndex: 91}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 92, dataIndex: 92}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 93, dataIndex: 93}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 94, dataIndex: 94}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 95, dataIndex: 95}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 96, dataIndex: 96}
                                        ]
                                    }
                                ]
                            }
                        },
                        'HAM01': { // Galactica
                            'main': {
                                carriers: [
                                    {
                                        startTrack: 20
                                        ,index: 1
                                        ,type: 'L5AC'
                                        ,plates: [
                                            {plateFor: 'source', type: 'SPTT_005', localIndex: 5, dataIndex: 5, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 4, dataIndex: 4, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 3, dataIndex: 3, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 2, dataIndex: 2, optional: true}
                                            ,{plateFor: 'source', type: 'SPTT_005', localIndex: 1, dataIndex: 1}
                                        ]
                                    }
                                    ,{
                                        startTrack: 39
                                        ,index: 2
                                        ,type: Constants.SHIPPING_TUBES_CARRIER_TYPE
                                        ,plates: [
                                            {plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 1, dataIndex: 1}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 2, dataIndex: 2}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 3, dataIndex: 3}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 4, dataIndex: 4}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 5, dataIndex: 5}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 6, dataIndex: 6}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 7, dataIndex: 7}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 8, dataIndex: 8}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 9, dataIndex: 9}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 10, dataIndex: 10}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 11, dataIndex: 11}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 12, dataIndex: 12}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 13, dataIndex: 13}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 14, dataIndex: 14}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 15, dataIndex: 15}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 16, dataIndex: 16}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 17, dataIndex: 17}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 18, dataIndex: 18}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 19, dataIndex: 19}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 20, dataIndex: 20}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 21, dataIndex: 21}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 22, dataIndex: 22}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 23, dataIndex: 23}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 24, dataIndex: 24}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 25, dataIndex: 25}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 26, dataIndex: 26}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 27, dataIndex: 27}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 28, dataIndex: 28}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 29, dataIndex: 29}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 30, dataIndex: 30}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 31, dataIndex: 31}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 32, dataIndex: 32}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 33, dataIndex: 33}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 34, dataIndex: 34}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 35, dataIndex: 35}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 36, dataIndex: 36}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 37, dataIndex: 37}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 38, dataIndex: 38}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 39, dataIndex: 39}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 40, dataIndex: 40}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 41, dataIndex: 41}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 42, dataIndex: 42}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 43, dataIndex: 43}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 44, dataIndex: 44}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 45, dataIndex: 45}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 46, dataIndex: 46}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 47, dataIndex: 47}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 48, dataIndex: 48}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 49, dataIndex: 49}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 50, dataIndex: 50}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 51, dataIndex: 51}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 52, dataIndex: 52}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 53, dataIndex: 53}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 54, dataIndex: 54}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 55, dataIndex: 55}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 56, dataIndex: 56}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 57, dataIndex: 57}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 58, dataIndex: 58}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 59, dataIndex: 59}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 60, dataIndex: 60}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 61, dataIndex: 61}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 62, dataIndex: 62}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 63, dataIndex: 63}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 64, dataIndex: 64}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 65, dataIndex: 65}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 66, dataIndex: 66}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 67, dataIndex: 67}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 68, dataIndex: 68}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 69, dataIndex: 69}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 70, dataIndex: 70}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 71, dataIndex: 71}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 72, dataIndex: 72}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 73, dataIndex: 73}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 74, dataIndex: 74}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 75, dataIndex: 75}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 76, dataIndex: 76}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 77, dataIndex: 77}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 78, dataIndex: 78}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 79, dataIndex: 79}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 80, dataIndex: 80}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 81, dataIndex: 81}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 82, dataIndex: 82}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 83, dataIndex: 83}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 84, dataIndex: 84}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 85, dataIndex: 85}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 86, dataIndex: 86}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 87, dataIndex: 87}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 88, dataIndex: 88}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 89, dataIndex: 89}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 90, dataIndex: 90}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 91, dataIndex: 91}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 92, dataIndex: 92}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 93, dataIndex: 93}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 94, dataIndex: 94}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 95, dataIndex: 95}
                                            ,{plateFor: 'destination', type: Constants.SHIPPING_TUBE_PLATE_TYPE, localIndex: 96, dataIndex: 96}
                                        ]
                                    }
                                ]
                            }
                        }
                        
                    }
                }
                ,34: {  // keyed to sample_transfer_template_id in the database
                    description: 'Titin Extraction'
                    ,type: 'standard_template'
                    ,source: {
                        plateCount: 1
                        ,plateTypeId: 'SPTT_0009'
                        ,variablePlateCount: false
                    }
                    ,destination: {
                        plateCount: 16
                        ,plateTypeId: 'SPTT_0006'
                        ,variablePlateCount: true
                        ,plateTitles: [
                            'Plate&nbsp;01&nbsp;'
                            ,'Plate&nbsp;02&nbsp;'
                            ,'Plate&nbsp;03&nbsp;'
                            ,'Plate&nbsp;04&nbsp;'
                            ,'Plate&nbsp;05&nbsp;'
                            ,'Plate&nbsp;06&nbsp;'
                            ,'Plate&nbsp;07&nbsp;'
                            ,'Plate&nbsp;08&nbsp;'
                            ,'Plate&nbsp;09&nbsp;'
                            ,'Plate&nbsp;10&nbsp;'
                            ,'Plate&nbsp;11&nbsp;'
                            ,'Plate&nbsp;12&nbsp;'
                            ,'Plate&nbsp;13&nbsp;'
                            ,'Plate&nbsp;14&nbsp;'
                            ,'Plate&nbsp;15&nbsp;'
                            ,'Plate&nbsp;16&nbsp;'
                        ]
                    }
                }
                ,35: {  // keyed to sample_transfer_template_id in the database
                    description: 'PCA Pre-Planning'
                    ,type: 'standard_template'
                    ,source: {
                        plateCount: 1
                        ,plateTypeId: 'SPTT_0006'
                        ,variablePlateCount: false
                    }
                    ,destination: {
                        plateCount: 0
                        ,plateTypeId: 'SPTT_0006'
                        ,variablePlateCount: true
                    }
                }

            }
            ,rowColumnMaps: {
                SPTT_0006: {
                    // 384 well plate
                     1: {row:'A', column: 1}
                    ,2: {row:'A', column: 2}
                    ,3: {row:'A', column: 3}
                    ,4: {row:'A', column: 4}
                    ,5: {row:'A', column: 5}
                    ,6: {row:'A', column: 6}
                    ,7: {row:'A', column: 7}
                    ,8: {row:'A', column: 8}
                    ,9: {row:'A', column: 9}
                    ,10: {row:'A', column: 10}
                    ,11: {row:'A', column: 11}
                    ,12: {row:'A', column: 12}
                    ,13: {row:'A', column: 13}
                    ,14: {row:'A', column: 14}
                    ,15: {row:'A', column: 15}
                    ,16: {row:'A', column: 16}
                    ,17: {row:'A', column: 17}
                    ,18: {row:'A', column: 18}
                    ,19: {row:'A', column: 19}
                    ,20: {row:'A', column: 20}
                    ,21: {row:'A', column: 21}
                    ,22: {row:'A', column: 22}
                    ,23: {row:'A', column: 23}
                    ,24: {row:'A', column: 24}
                    ,25: {row:'B', column: 1}
                    ,26: {row:'B', column: 2}
                    ,27: {row:'B', column: 3}
                    ,28: {row:'B', column: 4}
                    ,29: {row:'B', column: 5}
                    ,30: {row:'B', column: 6}
                    ,31: {row:'B', column: 7}
                    ,32: {row:'B', column: 8}
                    ,33: {row:'B', column: 9}
                    ,34: {row:'B', column: 10}
                    ,35: {row:'B', column: 11}
                    ,36: {row:'B', column: 12}
                    ,37: {row:'B', column: 13}
                    ,38: {row:'B', column: 14}
                    ,39: {row:'B', column: 15}
                    ,40: {row:'B', column: 16}
                    ,41: {row:'B', column: 17}
                    ,42: {row:'B', column: 18}
                    ,43: {row:'B', column: 19}
                    ,44: {row:'B', column: 20}
                    ,45: {row:'B', column: 21}
                    ,46: {row:'B', column: 22}
                    ,47: {row:'B', column: 23}
                    ,48: {row:'B', column: 24}
                    ,49: {row:'C', column: 1}
                    ,50: {row:'C', column: 2}
                    ,51: {row:'C', column: 3}
                    ,52: {row:'C', column: 4}
                    ,53: {row:'C', column: 5}
                    ,54: {row:'C', column: 6}
                    ,55: {row:'C', column: 7}
                    ,56: {row:'C', column: 8}
                    ,57: {row:'C', column: 9}
                    ,58: {row:'C', column: 10}
                    ,59: {row:'C', column: 11}
                    ,60: {row:'C', column: 12}
                    ,61: {row:'C', column: 13}
                    ,62: {row:'C', column: 14}
                    ,63: {row:'C', column: 15}
                    ,64: {row:'C', column: 16}
                    ,65: {row:'C', column: 17}
                    ,66: {row:'C', column: 18}
                    ,67: {row:'C', column: 19}
                    ,68: {row:'C', column: 20}
                    ,69: {row:'C', column: 21}
                    ,70: {row:'C', column: 22}
                    ,71: {row:'C', column: 23}
                    ,72: {row:'C', column: 24}
                    ,73: {row:'D', column: 1}
                    ,74: {row:'D', column: 2}
                    ,75: {row:'D', column: 3}
                    ,76: {row:'D', column: 4}
                    ,77: {row:'D', column: 5}
                    ,78: {row:'D', column: 6}
                    ,79: {row:'D', column: 7}
                    ,80: {row:'D', column: 8}
                    ,81: {row:'D', column: 9}
                    ,82: {row:'D', column: 10}
                    ,83: {row:'D', column: 11}
                    ,84: {row:'D', column: 12}
                    ,85: {row:'D', column: 13}
                    ,86: {row:'D', column: 14}
                    ,87: {row:'D', column: 15}
                    ,88: {row:'D', column: 16}
                    ,89: {row:'D', column: 17}
                    ,90: {row:'D', column: 18}
                    ,91: {row:'D', column: 19}
                    ,92: {row:'D', column: 20}
                    ,93: {row:'D', column: 21}
                    ,94: {row:'D', column: 22}
                    ,95: {row:'D', column: 23}
                    ,96: {row:'D', column: 24}
                    ,97: {row:'E', column: 1}
                    ,98: {row:'E', column: 2}
                    ,99: {row:'E', column: 3}
                    ,100: {row:'E', column: 4}
                    ,101: {row:'E', column: 5}
                    ,102: {row:'E', column: 6}
                    ,103: {row:'E', column: 7}
                    ,104: {row:'E', column: 8}
                    ,105: {row:'E', column: 9}
                    ,106: {row:'E', column: 10}
                    ,107: {row:'E', column: 11}
                    ,108: {row:'E', column: 12}
                    ,109: {row:'E', column: 13}
                    ,110: {row:'E', column: 14}
                    ,111: {row:'E', column: 15}
                    ,112: {row:'E', column: 16}
                    ,113: {row:'E', column: 17}
                    ,114: {row:'E', column: 18}
                    ,115: {row:'E', column: 19}
                    ,116: {row:'E', column: 20}
                    ,117: {row:'E', column: 21}
                    ,118: {row:'E', column: 22}
                    ,119: {row:'E', column: 23}
                    ,120: {row:'E', column: 24}
                    ,121: {row:'F', column: 1}
                    ,122: {row:'F', column: 2}
                    ,123: {row:'F', column: 3}
                    ,124: {row:'F', column: 4}
                    ,125: {row:'F', column: 5}
                    ,126: {row:'F', column: 6}
                    ,127: {row:'F', column: 7}
                    ,128: {row:'F', column: 8}
                    ,129: {row:'F', column: 9}
                    ,130: {row:'F', column: 10}
                    ,131: {row:'F', column: 11}
                    ,132: {row:'F', column: 12}
                    ,133: {row:'F', column: 13}
                    ,134: {row:'F', column: 14}
                    ,135: {row:'F', column: 15}
                    ,136: {row:'F', column: 16}
                    ,137: {row:'F', column: 17}
                    ,138: {row:'F', column: 18}
                    ,139: {row:'F', column: 19}
                    ,140: {row:'F', column: 20}
                    ,141: {row:'F', column: 21}
                    ,142: {row:'F', column: 22}
                    ,143: {row:'F', column: 23}
                    ,144: {row:'F', column: 24}
                    ,145: {row:'G', column: 1}
                    ,146: {row:'G', column: 2}
                    ,147: {row:'G', column: 3}
                    ,148: {row:'G', column: 4}
                    ,149: {row:'G', column: 5}
                    ,150: {row:'G', column: 6}
                    ,151: {row:'G', column: 7}
                    ,152: {row:'G', column: 8}
                    ,153: {row:'G', column: 9}
                    ,154: {row:'G', column: 10}
                    ,155: {row:'G', column: 11}
                    ,156: {row:'G', column: 12}
                    ,157: {row:'G', column: 13}
                    ,158: {row:'G', column: 14}
                    ,159: {row:'G', column: 15}
                    ,160: {row:'G', column: 16}
                    ,161: {row:'G', column: 17}
                    ,162: {row:'G', column: 18}
                    ,163: {row:'G', column: 19}
                    ,164: {row:'G', column: 20}
                    ,165: {row:'G', column: 21}
                    ,166: {row:'G', column: 22}
                    ,167: {row:'G', column: 23}
                    ,168: {row:'G', column: 24}
                    ,169: {row:'H', column: 1}
                    ,170: {row:'H', column: 2}
                    ,171: {row:'H', column: 3}
                    ,172: {row:'H', column: 4}
                    ,173: {row:'H', column: 5}
                    ,174: {row:'H', column: 6}
                    ,175: {row:'H', column: 7}
                    ,176: {row:'H', column: 8}
                    ,177: {row:'H', column: 9}
                    ,178: {row:'H', column: 10}
                    ,179: {row:'H', column: 11}
                    ,180: {row:'H', column: 12}
                    ,181: {row:'H', column: 13}
                    ,182: {row:'H', column: 14}
                    ,183: {row:'H', column: 15}
                    ,184: {row:'H', column: 16}
                    ,185: {row:'H', column: 17}
                    ,186: {row:'H', column: 18}
                    ,187: {row:'H', column: 19}
                    ,188: {row:'H', column: 20}
                    ,189: {row:'H', column: 21}
                    ,190: {row:'H', column: 22}
                    ,191: {row:'H', column: 23}
                    ,192: {row:'H', column: 24}
                    ,193: {row:'I', column: 1}
                    ,194: {row:'I', column: 2}
                    ,195: {row:'I', column: 3}
                    ,196: {row:'I', column: 4}
                    ,197: {row:'I', column: 5}
                    ,198: {row:'I', column: 6}
                    ,199: {row:'I', column: 7}
                    ,200: {row:'I', column: 8}
                    ,201: {row:'I', column: 9}
                    ,202: {row:'I', column: 10}
                    ,203: {row:'I', column: 11}
                    ,204: {row:'I', column: 12}
                    ,205: {row:'I', column: 13}
                    ,206: {row:'I', column: 14}
                    ,207: {row:'I', column: 15}
                    ,208: {row:'I', column: 16}
                    ,209: {row:'I', column: 17}
                    ,210: {row:'I', column: 18}
                    ,211: {row:'I', column: 19}
                    ,212: {row:'I', column: 20}
                    ,213: {row:'I', column: 21}
                    ,214: {row:'I', column: 22}
                    ,215: {row:'I', column: 23}
                    ,216: {row:'I', column: 24}
                    ,217: {row:'J', column: 1}
                    ,218: {row:'J', column: 2}
                    ,219: {row:'J', column: 3}
                    ,220: {row:'J', column: 4}
                    ,221: {row:'J', column: 5}
                    ,222: {row:'J', column: 6}
                    ,223: {row:'J', column: 7}
                    ,224: {row:'J', column: 8}
                    ,225: {row:'J', column: 9}
                    ,226: {row:'J', column: 10}
                    ,227: {row:'J', column: 11}
                    ,228: {row:'J', column: 12}
                    ,229: {row:'J', column: 13}
                    ,230: {row:'J', column: 14}
                    ,231: {row:'J', column: 15}
                    ,232: {row:'J', column: 16}
                    ,233: {row:'J', column: 17}
                    ,234: {row:'J', column: 18}
                    ,235: {row:'J', column: 19}
                    ,236: {row:'J', column: 20}
                    ,237: {row:'J', column: 21}
                    ,238: {row:'J', column: 22}
                    ,239: {row:'J', column: 23}
                    ,240: {row:'J', column: 24}
                    ,241: {row:'K', column: 1}
                    ,242: {row:'K', column: 2}
                    ,243: {row:'K', column: 3}
                    ,244: {row:'K', column: 4}
                    ,245: {row:'K', column: 5}
                    ,246: {row:'K', column: 6}
                    ,247: {row:'K', column: 7}
                    ,248: {row:'K', column: 8}
                    ,249: {row:'K', column: 9}
                    ,250: {row:'K', column: 10}
                    ,251: {row:'K', column: 11}
                    ,252: {row:'K', column: 12}
                    ,253: {row:'K', column: 13}
                    ,254: {row:'K', column: 14}
                    ,255: {row:'K', column: 15}
                    ,256: {row:'K', column: 16}
                    ,257: {row:'K', column: 17}
                    ,258: {row:'K', column: 18}
                    ,259: {row:'K', column: 19}
                    ,260: {row:'K', column: 20}
                    ,261: {row:'K', column: 21}
                    ,262: {row:'K', column: 22}
                    ,263: {row:'K', column: 23}
                    ,264: {row:'K', column: 24}
                    ,265: {row:'L', column: 1}
                    ,266: {row:'L', column: 2}
                    ,267: {row:'L', column: 3}
                    ,268: {row:'L', column: 4}
                    ,269: {row:'L', column: 5}
                    ,270: {row:'L', column: 6}
                    ,271: {row:'L', column: 7}
                    ,272: {row:'L', column: 8}
                    ,273: {row:'L', column: 9}
                    ,274: {row:'L', column: 10}
                    ,275: {row:'L', column: 11}
                    ,276: {row:'L', column: 12}
                    ,277: {row:'L', column: 13}
                    ,278: {row:'L', column: 14}
                    ,279: {row:'L', column: 15}
                    ,280: {row:'L', column: 16}
                    ,281: {row:'L', column: 17}
                    ,282: {row:'L', column: 18}
                    ,283: {row:'L', column: 19}
                    ,284: {row:'L', column: 20}
                    ,285: {row:'L', column: 21}
                    ,286: {row:'L', column: 22}
                    ,287: {row:'L', column: 23}
                    ,288: {row:'L', column: 24}
                    ,289: {row:'M', column: 1}
                    ,290: {row:'M', column: 2}
                    ,291: {row:'M', column: 3}
                    ,292: {row:'M', column: 4}
                    ,293: {row:'M', column: 5}
                    ,294: {row:'M', column: 6}
                    ,295: {row:'M', column: 7}
                    ,296: {row:'M', column: 8}
                    ,297: {row:'M', column: 9}
                    ,298: {row:'M', column: 10}
                    ,299: {row:'M', column: 11}
                    ,300: {row:'M', column: 12}
                    ,301: {row:'M', column: 13}
                    ,302: {row:'M', column: 14}
                    ,303: {row:'M', column: 15}
                    ,304: {row:'M', column: 16}
                    ,305: {row:'M', column: 17}
                    ,306: {row:'M', column: 18}
                    ,307: {row:'M', column: 19}
                    ,308: {row:'M', column: 20}
                    ,309: {row:'M', column: 21}
                    ,310: {row:'M', column: 22}
                    ,311: {row:'M', column: 23}
                    ,312: {row:'M', column: 24}
                    ,313: {row:'N', column: 1}
                    ,314: {row:'N', column: 2}
                    ,315: {row:'N', column: 3}
                    ,316: {row:'N', column: 4}
                    ,317: {row:'N', column: 5}
                    ,318: {row:'N', column: 6}
                    ,319: {row:'N', column: 7}
                    ,320: {row:'N', column: 8}
                    ,321: {row:'N', column: 9}
                    ,322: {row:'N', column: 10}
                    ,323: {row:'N', column: 11}
                    ,324: {row:'N', column: 12}
                    ,325: {row:'N', column: 13}
                    ,326: {row:'N', column: 14}
                    ,327: {row:'N', column: 15}
                    ,328: {row:'N', column: 16}
                    ,329: {row:'N', column: 17}
                    ,330: {row:'N', column: 18}
                    ,331: {row:'N', column: 19}
                    ,332: {row:'N', column: 20}
                    ,333: {row:'N', column: 21}
                    ,334: {row:'N', column: 22}
                    ,335: {row:'N', column: 23}
                    ,336: {row:'N', column: 24}
                    ,337: {row:'O', column: 1}
                    ,338: {row:'O', column: 2}
                    ,339: {row:'O', column: 3}
                    ,340: {row:'O', column: 4}
                    ,341: {row:'O', column: 5}
                    ,342: {row:'O', column: 6}
                    ,343: {row:'O', column: 7}
                    ,344: {row:'O', column: 8}
                    ,345: {row:'O', column: 9}
                    ,346: {row:'O', column: 10}
                    ,347: {row:'O', column: 11}
                    ,348: {row:'O', column: 12}
                    ,349: {row:'O', column: 13}
                    ,350: {row:'O', column: 14}
                    ,351: {row:'O', column: 15}
                    ,352: {row:'O', column: 16}
                    ,353: {row:'O', column: 17}
                    ,354: {row:'O', column: 18}
                    ,355: {row:'O', column: 19}
                    ,356: {row:'O', column: 20}
                    ,357: {row:'O', column: 21}
                    ,358: {row:'O', column: 22}
                    ,359: {row:'O', column: 23}
                    ,360: {row:'O', column: 24}
                    ,361: {row:'P', column: 1}
                    ,362: {row:'P', column: 2}
                    ,363: {row:'P', column: 3}
                    ,364: {row:'P', column: 4}
                    ,365: {row:'P', column: 5}
                    ,366: {row:'P', column: 6}
                    ,367: {row:'P', column: 7}
                    ,368: {row:'P', column: 8}
                    ,369: {row:'P', column: 9}
                    ,370: {row:'P', column: 10}
                    ,371: {row:'P', column: 11}
                    ,372: {row:'P', column: 12}
                    ,373: {row:'P', column: 13}
                    ,374: {row:'P', column: 14}
                    ,375: {row:'P', column: 15}
                    ,376: {row:'P', column: 16}
                    ,377: {row:'P', column: 17}
                    ,378: {row:'P', column: 18}
                    ,379: {row:'P', column: 19}
                    ,380: {row:'P', column: 20}
                    ,381: {row:'P', column: 21}
                    ,382: {row:'P', column: 22}
                    ,383: {row:'P', column: 23}
                    ,384: {row:'P', column: 24}

                }
                ,SPTT_0005: {
                    // 96 well plate
                    1:{ row: 'A', column: 1}
                    ,2:{ row: 'A', column: 2}
                    ,3:{ row: 'A', column: 3}
                    ,4:{ row: 'A', column: 4}
                    ,5:{ row: 'A', column: 5}
                    ,6:{ row: 'A', column: 6}
                    ,7:{ row: 'A', column: 7}
                    ,8:{ row: 'A', column: 8}
                    ,9:{ row: 'A', column: 9}
                    ,10: {row: 'A', column: 10}
                    ,11: {row: 'A', column: 11}
                    ,12: {row: 'A', column: 12}
                    ,13: {row: 'B', column: 1}
                    ,14: {row: 'B', column: 2}
                    ,15: {row: 'B', column: 3}
                    ,16: {row: 'B', column: 4}
                    ,17: {row: 'B', column: 5}
                    ,18: {row: 'B', column: 6}
                    ,19: {row: 'B', column: 7}
                    ,20: {row: 'B', column: 8}
                    ,21: {row: 'B', column: 9}
                    ,22: {row: 'B', column: 10}
                    ,23: {row: 'B', column: 11}
                    ,24: {row: 'B', column: 12}
                    ,25: {row: 'C', column: 1}
                    ,26: {row: 'C', column: 2}
                    ,27: {row: 'C', column: 3}
                    ,28: {row: 'C', column: 4}
                    ,29: {row: 'C', column: 5}
                    ,30: {row: 'C', column: 6}
                    ,31: {row: 'C', column: 7}
                    ,32: {row: 'C', column: 8}
                    ,33: {row: 'C', column: 9}
                    ,34: {row: 'C', column: 10}
                    ,35: {row: 'C', column: 11}
                    ,36: {row: 'C', column: 12}
                    ,37: {row: 'D', column: 1}
                    ,38: {row: 'D', column: 2}
                    ,39: {row: 'D', column: 3}
                    ,40: {row: 'D', column: 4}
                    ,41: {row: 'D', column: 5}
                    ,42: {row: 'D', column: 6}
                    ,43: {row: 'D', column: 7}
                    ,44: {row: 'D', column: 8}
                    ,45: {row: 'D', column: 9}
                    ,46: {row: 'D', column: 10}
                    ,47: {row: 'D', column: 11}
                    ,48: {row: 'D', column: 12}
                    ,49: {row: 'E', column: 1}
                    ,50: {row: 'E', column: 2}
                    ,51: {row: 'E', column: 3}
                    ,52: {row: 'E', column: 4}
                    ,53: {row: 'E', column: 5}
                    ,54: {row: 'E', column: 6}
                    ,55: {row: 'E', column: 7}
                    ,56: {row: 'E', column: 8}
                    ,57: {row: 'E', column: 9}
                    ,58: {row: 'E', column: 10}
                    ,59: {row: 'E', column: 11}
                    ,60: {row: 'E', column: 12}
                    ,61: {row: 'F', column: 1}
                    ,62: {row: 'F', column: 2}
                    ,63: {row: 'F', column: 3}
                    ,64: {row: 'F', column: 4}
                    ,65: {row: 'F', column: 5}
                    ,66: {row: 'F', column: 6}
                    ,67: {row: 'F', column: 7}
                    ,68: {row: 'F', column: 8}
                    ,69: {row: 'F', column: 9}
                    ,70: {row: 'F', column: 10}
                    ,71: {row: 'F', column: 11}
                    ,72: {row: 'F', column: 12}
                    ,73: {row: 'G', column: 1}
                    ,74: {row: 'G', column: 2}
                    ,75: {row: 'G', column: 3}
                    ,76: {row: 'G', column: 4}
                    ,77: {row: 'G', column: 5}
                    ,78: {row: 'G', column: 6}
                    ,79: {row: 'G', column: 7}
                    ,80: {row: 'G', column: 8}
                    ,81: {row: 'G', column: 9}
                    ,82: {row: 'G', column: 10}
                    ,83: {row: 'G', column: 11}
                    ,84: {row: 'G', column: 12}
                    ,85: {row: 'H', column: 1}
                    ,86: {row: 'H', column: 2}
                    ,87: {row: 'H', column: 3}
                    ,88: {row: 'H', column: 4}
                    ,89: {row: 'H', column: 5}
                    ,90: {row: 'H', column: 6}
                    ,91: {row: 'H', column: 7}
                    ,92: {row: 'H', column: 8}
                    ,93: {row: 'H', column: 9}
                    ,94: {row: 'H', column: 10}
                    ,95: {row: 'H', column: 11}
                    ,96: {row: 'H', column: 12}
                }
                ,SPTT_0004: {
                    // 48 well plate
                     1: {row: 'A', column: 1}
                    ,2: {row: 'A', column: 2}
                    ,3: {row: 'A', column: 3}
                    ,4: {row: 'A', column: 4}
                    ,5: {row: 'A', column: 5}
                    ,6: {row: 'A', column: 6}
                    ,7: {row: 'B', column: 1}
                    ,8: {row: 'B', column: 2}
                    ,9: {row: 'B', column: 3}
                    ,10: {row: 'B', column: 4}
                    ,11: {row: 'B', column: 5}
                    ,12: {row: 'B', column: 6}
                    ,13: {row: 'C', column: 1}
                    ,14: {row: 'C', column: 2}
                    ,15: {row: 'C', column: 3}
                    ,16: {row: 'C', column: 4}
                    ,17: {row: 'C', column: 5}
                    ,18: {row: 'C', column: 6}
                    ,19: {row: 'D', column: 1}
                    ,20: {row: 'D', column: 2}
                    ,21: {row: 'D', column: 3}
                    ,22: {row: 'D', column: 4}
                    ,23: {row: 'D', column: 5}
                    ,24: {row: 'D', column: 6}
                    ,25: {row: 'E', column: 1}
                    ,26: {row: 'E', column: 2}
                    ,27: {row: 'E', column: 3}
                    ,28: {row: 'E', column: 4}
                    ,29: {row: 'E', column: 5}
                    ,30: {row: 'E', column: 6}
                    ,31: {row: 'F', column: 1}
                    ,32: {row: 'F', column: 2}
                    ,33: {row: 'F', column: 3}
                    ,34: {row: 'F', column: 4}
                    ,35: {row: 'F', column: 5}
                    ,36: {row: 'F', column: 6}
                    ,37: {row: 'G', column: 1}
                    ,38: {row: 'G', column: 2}
                    ,39: {row: 'G', column: 3}
                    ,40: {row: 'G', column: 4}
                    ,41: {row: 'G', column: 5}
                    ,42: {row: 'G', column: 6}
                    ,43: {row: 'H', column: 1}
                    ,44: {row: 'H', column: 2}
                    ,45: {row: 'H', column: 3}
                    ,46: {row: 'H', column: 4}
                    ,47: {row: 'H', column: 5}
                    ,48: {row: 'H', column: 6}
                }
                ,QPIX_SPTT_0004: {
                    // 48 well plate as understood by qpix
                    1: {row: 'F', column: 1}
                    ,2: {row: 'E', column: 1}
                    ,3: {row: 'D', column: 1}
                    ,4: {row: 'C', column: 1}
                    ,5: {row: 'B', column: 1}
                    ,6: {row: 'A', column: 1}
                    ,7: {row: 'F', column: 2}
                    ,8: {row: 'E', column: 2}
                    ,9: {row: 'D', column: 2}
                    ,10: {row: 'C', column: 2}
                    ,11: {row: 'B', column: 2}
                    ,12: {row: 'A', column: 2}
                    ,13: {row: 'F', column: 3}
                    ,14: {row: 'E', column: 3}
                    ,15: {row: 'D', column: 3}
                    ,16: {row: 'C', column: 3}
                    ,17: {row: 'B', column: 3}
                    ,18: {row: 'A', column: 3}
                    ,19: {row: 'F', column: 4}
                    ,20: {row: 'E', column: 4}
                    ,21: {row: 'D', column: 4}
                    ,22: {row: 'C', column: 4}
                    ,23: {row: 'B', column: 4}
                    ,24: {row: 'A', column: 4}
                    ,25: {row: 'F', column: 5}
                    ,26: {row: 'E', column: 5}
                    ,27: {row: 'D', column: 5}
                    ,28: {row: 'C', column: 5}
                    ,29: {row: 'B', column: 5}
                    ,30: {row: 'A', column: 5}
                    ,31: {row: 'F', column: 6}
                    ,32: {row: 'E', column: 6}
                    ,33: {row: 'D', column: 6}
                    ,34: {row: 'C', column: 6}
                    ,35: {row: 'B', column: 6}
                    ,36: {row: 'A', column: 6}
                    ,37: {row: 'F', column: 7}
                    ,38: {row: 'E', column: 7}
                    ,39: {row: 'D', column: 7}
                    ,40: {row: 'C', column: 7}
                    ,41: {row: 'B', column: 7}
                    ,42: {row: 'A', column: 7}
                    ,43: {row: 'F', column: 8}
                    ,44: {row: 'E', column: 8}
                    ,45: {row: 'D', column: 8}
                    ,46: {row: 'C', column: 8}
                    ,47: {row: 'B', column: 8}
                    ,48: {row: 'A', column: 8}
                }

            }
            ,plateTypeInfo: {
                SPTT_0004: {
                    description: 'Generic 48 well plastic plate'
                    ,wellCount: 48
                }
                ,SPTT_0005: {
                    description: 'Generic 96 well plastic plate'
                    ,wellCount: 96
                }
                ,SPTT_0006: {
                    description: 'Generic 384 well plastic plate'
                    ,wellCount: 384
                }
            }
            ,carriers: {
                'L5AC': {
                    label: 'Five 96-well plates'
                    ,trackWidth: 6
                }
                ,'SHIPPING_TUBES_CARRIER': {
                    label: 'Carrier to hold shipping tubes plate (this is a virtual carrier - ie, the tubes rack sits right on the deck)'
                    ,trackWidth: 9
                }
            }

            ,plateTemplates: {
                SPTT_0004: function () {

                    var data = {
                        description: 'Generic 48 well plastic plate'
                        ,wellCount: 48
                        ,rowLength: 6
                        ,addSampleId: function (wellRowColumn, id) {
                            this.wellMap[wellRowColumn].sampleId = id;
                        }
                        ,wellMap: {
                            A1: {
                                row: 1
                                ,col: 1
                                ,index: 1
                            }
                            ,A2: {
                                row: 1
                                ,col: 2
                                ,index: 2
                            }
                            ,A3: {
                                row: 1
                                ,col: 3
                                ,index: 3
                            }
                            ,A4: {
                                row: 1
                                ,col: 4
                                ,index: 4
                            }
                            ,A5: {
                                row: 1
                                ,col: 5
                                ,index: 5
                            }
                            ,A6: {
                                row: 1
                                ,col: 6
                                ,index: 6
                            }
                            ,B1: {
                                row: 2
                                ,col: 1
                                ,index: 7
                            }
                            ,B2: {
                                row: 2
                                ,col: 2
                                ,index: 8
                            }
                            ,B3: {
                                row: 2
                                ,col: 3
                                ,index: 9
                            }
                            ,B4: {
                                row: 2
                                ,col: 4
                                ,index: 10
                            }
                            ,B5: {
                                row: 2
                                ,col: 5
                                ,index: 11
                            }
                            ,B6: {
                                row: 2
                                ,col: 6
                                ,index: 12
                            }
                            ,C1: {
                                row: 3
                                ,col: 1
                                ,index: 13
                            }
                            ,C2: {
                                row: 3
                                ,col: 2
                                ,index: 14
                            }
                            ,C3: {
                                row: 3
                                ,col: 3
                                ,index: 15
                            }
                            ,C4: {
                                row: 3
                                ,col: 4
                                ,index: 16
                            }
                            ,C5: {
                                row: 3
                                ,col: 5
                                ,index: 17
                            }
                            ,C6: {
                                row: 3
                                ,col: 6
                                ,index: 18
                            }
                            ,D1: {
                                row: 4
                                ,col: 1
                                ,index: 19
                            }
                            ,D2: {
                                row: 4
                                ,col: 2
                                ,index: 20
                            }
                            ,D3: {
                                row: 4
                                ,col: 3
                                ,index: 21
                            }
                            ,D4: {
                                row: 4
                                ,col: 4
                                ,index: 22
                            }
                            ,D5: {
                                row: 4
                                ,col: 5
                                ,index: 23
                            }
                            ,D6: {
                                row: 4
                                ,col: 6
                                ,index: 24
                            }
                            ,E1: {
                                row: 5
                                ,col: 1
                                ,index: 25
                            }
                            ,E2: {
                                row: 5
                                ,col: 2
                                ,index: 26
                            }
                            ,E3: {
                                row: 5
                                ,col: 3
                                ,index: 27
                            }
                            ,E4: {
                                row: 5
                                ,col: 4
                                ,index: 28
                            }
                            ,E5: {
                                row: 5
                                ,col: 5
                                ,index: 29
                            }
                            ,E6: {
                                row: 5
                                ,col: 6
                                ,index: 30
                            }
                            ,F1: {
                                row: 6
                                ,col: 1
                                ,index: 31
                            }
                            ,F2: {
                                row: 6
                                ,col: 2
                                ,index: 32
                            }
                            ,F3: {
                                row: 6
                                ,col: 3
                                ,index: 33
                            }
                            ,F4: {
                                row: 6
                                ,col: 4
                                ,index: 34
                            }
                            ,F5: {
                                row: 6
                                ,col: 5
                                ,index: 35
                            }
                            ,F6: {
                                row: 6
                                ,col: 6
                                ,index: 36
                            }
                            ,G1: {
                                row: 7
                                ,col: 1
                                ,index: 37
                            }
                            ,G2: {
                                row: 7
                                ,col: 2
                                ,index: 38
                            }
                            ,G3: {
                                row: 7
                                ,col: 3
                                ,index: 39
                            }
                            ,G4: {
                                row: 7
                                ,col: 4
                                ,index: 40
                            }
                            ,G5: {
                                row: 7
                                ,col: 5
                                ,index: 41
                            }
                            ,G6: {
                                row: 7
                                ,col: 6
                                ,index: 42
                            }
                            ,H1: {
                                row: 8
                                ,col: 1
                                ,index: 43
                            }
                            ,H2: {
                                row: 8
                                ,col: 2
                                ,index: 44
                            }
                            ,H3: {
                                row: 8
                                ,col: 3
                                ,index: 45
                            }
                            ,H4: {
                                row: 8
                                ,col: 4
                                ,index: 46
                            }
                            ,H5: {
                                row: 8
                                ,col: 5
                                ,index: 47
                            }
                            ,H6: {
                                row: 8
                                ,col: 6
                                ,index: 48
                            }
                        }
                    };

                    return data;
                }
                ,SPTT_004_QPIX: function () {

                   var data = {
                        description: 'Qpix view of 48 well plate'
                        ,wellCount: 48
                        ,rowLength: 6
                        ,addSampleId: function (wellRowColumn, id) {
                            this.wellMap[wellRowColumn].sampleId = id;
                        }
                        ,wellMap: {
                            F1: {
                                row: 1
                                ,col: 1
                                ,index: 1
                            }
                            ,E1: {
                                row: 2
                                ,col: 1
                                ,index: 2
                            }
                            ,D1: {
                                row: 3
                                ,col: 1
                                ,index: 3
                            }
                            ,C1: {
                                row: 4
                                ,col: 1
                                ,index: 4
                            }
                            ,B1: {
                                row: 5
                                ,col: 1
                                ,index: 5
                            }
                            ,A1: {
                                row: 6
                                ,col: 1
                                ,index: 6
                            }
                            ,F2: {
                                row: 1
                                ,col: 2
                                ,index: 7
                            }
                            ,E2: {
                                row: 2
                                ,col: 2
                                ,index: 8
                            }
                            ,D2: {
                                row: 3
                                ,col: 2
                                ,index: 9
                            }
                            ,C2: {
                                row: 4
                                ,col: 2
                                ,index: 10
                            }
                            ,B2: {
                                row: 5
                                ,col: 2
                                ,index: 11
                            }
                            ,A2: {
                                row: 6
                                ,col: 2
                                ,index: 12
                            }
                            ,F3: {
                                row: 1
                                ,col: 3
                                ,index: 13
                            }
                            ,E3: {
                                row: 2
                                ,col: 3
                                ,index: 14
                            }
                            ,D3: {
                                row: 3
                                ,col: 3
                                ,index: 15
                            }
                            ,C3: {
                                row: 4
                                ,col: 3
                                ,index: 16
                            }
                            ,B3: {
                                row: 5
                                ,col: 3
                                ,index: 17
                            }
                            ,A3: {
                                row: 6
                                ,col: 3
                                ,index: 18
                            }
                            ,F4: {
                                row: 1
                                ,col: 4
                                ,index: 19
                            }
                            ,E4: {
                                row: 2
                                ,col: 4
                                ,index: 20
                            }
                            ,D4: {
                                row: 3
                                ,col: 4
                                ,index: 21
                            }
                            ,C4: {
                                row: 4
                                ,col: 4
                                ,index: 22
                            }
                            ,B4: {
                                row: 5
                                ,col: 4
                                ,index: 23
                            }
                            ,A4: {
                                row: 6
                                ,col: 4
                                ,index: 24
                            }
                            ,F5: {
                                row: 1
                                ,col: 5
                                ,index: 25
                            }
                            ,E5: {
                                row: 2
                                ,col: 5
                                ,index: 26
                            }
                            ,D5: {
                                row: 3
                                ,col: 5
                                ,index: 27
                            }
                            ,C5: {
                                row: 4
                                ,col: 5
                                ,index: 28
                            }
                            ,B5: {
                                row: 5
                                ,col: 5
                                ,index: 29
                            }
                            ,A5: {
                                row: 6
                                ,col: 5
                                ,index: 30
                            }
                            ,F6: {
                                row: 1
                                ,col: 6
                                ,index: 31
                            }
                            ,E6: {
                                row: 2
                                ,col: 6
                                ,index: 32
                            }
                            ,D6: {
                                row: 3
                                ,col: 6
                                ,index: 33
                            }
                            ,C6: {
                                row: 4
                                ,col: 6
                                ,index: 34
                            }
                            ,B6: {
                                row: 5
                                ,col: 6
                                ,index: 35
                            }
                            ,A6: {
                                row: 6
                                ,col: 6
                                ,index: 36
                            }
                            ,F7: {
                                row: 1
                                ,col: 7
                                ,index: 37
                            }
                            ,E7: {
                                row: 2
                                ,col: 7
                                ,index: 38
                            }
                            ,D7: {
                                row: 3
                                ,col: 7
                                ,index: 39
                            }
                            ,C7: {
                                row: 4
                                ,col: 7
                                ,index: 40
                            }
                            ,B7: {
                                row: 5
                                ,col: 7
                                ,index: 41
                            }
                            ,A7: {
                                row: 6
                                ,col: 7
                                ,index: 42
                            }
                            ,F8: {
                                row: 1
                                ,col: 8
                                ,index: 43
                            }
                            ,E8: {
                                row: 2
                                ,col: 8
                                ,index: 44
                            }
                            ,D8: {
                                row: 3
                                ,col: 8
                                ,index: 45
                            }
                            ,C8: {
                                row: 4
                                ,col: 8
                                ,index: 46
                            }
                            ,B8: {
                                row: 5
                                ,col: 8
                                ,index: 47
                            }
                            ,A8: {
                                row: 6
                                ,col: 8
                                ,index: 48
                            }
                        }
                    }

                    return data;
                }
                ,SPTT_0005: function () {
                    var data = {
                        description: 'Generic 96 well plastic plate'
                        ,wellCount: 96
                        ,rowLength: 12
                        ,addSampleId: function (wellRowColumn, id) {
                            this.wellMap[wellRowColumn].sampleId = id;
                        }
                        ,wellMap: {
                            A1: {
                                row: 1
                                ,col: 1
                                ,index: 1
                            }
                            ,A2: {
                                row: 1
                                ,col: 2
                                ,index: 2
                            }
                            ,A3: {
                                row: 1
                                ,col: 3
                                ,index: 3
                            }
                            ,A4: {
                                row: 1
                                ,col: 4
                                ,index: 4
                            }
                            ,A5: {
                                row: 1
                                ,col: 5
                                ,index: 5
                            }
                            ,A6: {
                                row: 1
                                ,col: 6
                                ,index: 6
                            }
                            ,A7: {
                                row: 1
                                ,col: 7
                                ,index: 7
                            }
                            ,A8: {
                                row: 1
                                ,col: 8
                                ,index: 8
                            }
                            ,A9: {
                                row: 1
                                ,col: 9
                                ,index: 9
                            }
                            ,A10: {
                                row: 1
                                ,col: 10
                                ,index: 10
                            }
                            ,A11: {
                                row: 1
                                ,col: 11
                                ,index: 11
                            }
                            ,A12: {
                                row: 1
                                ,col: 12
                                ,index: 12
                            }
                            ,B1: {
                                row: 2
                                ,col: 1
                                ,index: 13
                            }
                            ,B2: {
                                row: 2
                                ,col: 2
                                ,index: 14
                            }
                            ,B3: {
                                row: 2
                                ,col: 3
                                ,index: 15
                            }
                            ,B4: {
                                row: 2
                                ,col: 4
                                ,index: 16
                            }
                            ,B5: {
                                row: 2
                                ,col: 5
                                ,index: 17
                            }
                            ,B6: {
                                row: 2
                                ,col: 6
                                ,index: 18
                            }
                            ,B7: {
                                row: 2
                                ,col: 7
                                ,index: 19
                            }
                            ,B8: {
                                row: 2
                                ,col: 8
                                ,index: 20
                            }
                            ,B9: {
                                row: 2
                                ,col: 9
                                ,index: 21
                            }
                            ,B10: {
                                row: 2
                                ,col: 10
                                ,index: 22
                            }
                            ,B11: {
                                row: 2
                                ,col: 11
                                ,index: 23
                            }
                            ,B12: {
                                row: 2
                                ,col: 12
                                ,index: 24
                            }
                            ,C1: {
                                row: 3
                                ,col: 1
                                ,index: 25
                            }
                            ,C2: {
                                row: 3
                                ,col: 2
                                ,index: 26
                            }
                            ,C3: {
                                row: 3
                                ,col: 3
                                ,index: 27
                            }
                            ,C4: {
                                row: 3
                                ,col: 4
                                ,index: 28
                            }
                            ,C5: {
                                row: 3
                                ,col: 5
                                ,index: 29
                            }
                            ,C6: {
                                row: 3
                                ,col: 6
                                ,index: 30
                            }
                            ,C7: {
                                row: 3
                                ,col: 7
                                ,index: 31
                            }
                            ,C8: {
                                row: 3
                                ,col: 8
                                ,index: 32
                            }
                            ,C9: {
                                row: 3
                                ,col: 9
                                ,index: 33
                            }
                            ,C10: {
                                row: 3
                                ,col: 10
                                ,index: 34
                            }
                            ,C11: {
                                row: 3
                                ,col: 11
                                ,index: 35
                            }
                            ,C12: {
                                row: 3
                                ,col: 12
                                ,index: 36
                            }
                            ,D1: {
                                row: 4
                                ,col: 1
                                ,index: 37
                            }
                            ,D2: {
                                row: 4
                                ,col: 2
                                ,index: 38
                            }
                            ,D3: {
                                row: 4
                                ,col: 3
                                ,index: 39
                            }
                            ,D4: {
                                row: 4
                                ,col: 4
                                ,index: 40
                            }
                            ,D5: {
                                row: 4
                                ,col: 5
                                ,index: 41
                            }
                            ,D6: {
                                row: 4
                                ,col: 6
                                ,index: 42
                            }
                            ,D7: {
                                row: 4
                                ,col: 7
                                ,index: 43
                            }
                            ,D8: {
                                row: 4
                                ,col: 8
                                ,index: 44
                            }
                            ,D9: {
                                row: 4
                                ,col: 9
                                ,index: 45
                            }
                            ,D10: {
                                row: 4
                                ,col: 10
                                ,index: 46
                            }
                            ,D11: {
                                row: 4
                                ,col: 11
                                ,index: 47
                            }
                            ,D12: {
                                row: 4
                                ,col: 12
                                ,index: 48
                            }
                            ,E1: {
                                row: 5
                                ,col: 1
                                ,index: 49
                            }
                            ,E2: {
                                row: 5
                                ,col: 2
                                ,index: 50
                            }
                            ,E3: {
                                row: 5
                                ,col: 3
                                ,index: 51
                            }
                            ,E4: {
                                row: 5
                                ,col: 4
                                ,index: 52
                            }
                            ,E5: {
                                row: 5
                                ,col: 5
                                ,index: 53
                            }
                            ,E6: {
                                row: 5
                                ,col: 6
                                ,index: 54
                            }
                            ,E7: {
                                row: 5
                                ,col: 7
                                ,index: 55
                            }
                            ,E8: {
                                row: 5
                                ,col: 8
                                ,index: 56
                            }
                            ,E9: {
                                row: 5
                                ,col: 9
                                ,index: 57
                            }
                            ,E10: {
                                row: 5
                                ,col: 10
                                ,index: 58
                            }
                            ,E11: {
                                row: 5
                                ,col: 11
                                ,index: 59
                            }
                            ,E12: {
                                row: 5
                                ,col: 12
                                ,index: 60
                            }
                            ,F1: {
                                row: 6
                                ,col: 1
                                ,index: 61
                            }
                            ,F2: {
                                row: 6
                                ,col: 2
                                ,index: 62
                            }
                            ,F3: {
                                row: 6
                                ,col: 3
                                ,index: 63
                            }
                            ,F4: {
                                row: 6
                                ,col: 4
                                ,index: 64
                            }
                            ,F5: {
                                row: 6
                                ,col: 5
                                ,index: 65
                            }
                            ,F6: {
                                row: 6
                                ,col: 6
                                ,index: 66
                            }
                            ,F7: {
                                row: 6
                                ,col: 7
                                ,index: 67
                            }
                            ,F8: {
                                row: 6
                                ,col: 8
                                ,index: 68
                            }
                            ,F9: {
                                row: 6
                                ,col: 9
                                ,index: 69
                            }
                            ,F10: {
                                row: 6
                                ,col: 10
                                ,index: 70
                            }
                            ,F11: {
                                row: 6
                                ,col: 11
                                ,index: 71
                            }
                            ,F12: {
                                row: 6
                                ,col: 12
                                ,index: 72
                            }
                            ,G1: {
                                row: 7
                                ,col: 1
                                ,index: 73
                            }
                            ,G2: {
                                row: 7
                                ,col: 2
                                ,index: 74
                            }
                            ,G3: {
                                row: 7
                                ,col: 3
                                ,index: 75
                            }
                            ,G4: {
                                row: 7
                                ,col: 4
                                ,index: 76
                            }
                            ,G5: {
                                row: 7
                                ,col: 5
                                ,index: 77
                            }
                            ,G6: {
                                row: 7
                                ,col: 6
                                ,index: 78
                            }
                            ,G7: {
                                row: 7
                                ,col: 7
                                ,index: 79
                            }
                            ,G8: {
                                row: 7
                                ,col: 8
                                ,index: 80
                            }
                            ,G9: {
                                row: 7
                                ,col: 9
                                ,index: 81
                            }
                            ,G10: {
                                row: 7
                                ,col: 10
                                ,index: 82
                            }
                            ,G11: {
                                row: 7
                                ,col: 11
                                ,index: 83
                            }
                            ,G12: {
                                row: 7
                                ,col: 12
                                ,index: 84
                            }
                            ,H1: {
                                row: 8
                                ,col: 1
                                ,index: 85
                            }
                            ,H2: {
                                row: 8
                                ,col: 2
                                ,index: 86
                            }
                            ,H3: {
                                row: 8
                                ,col: 3
                                ,index: 87
                            }
                            ,H4: {
                                row: 8
                                ,col: 4
                                ,index: 88
                            }
                            ,H5: {
                                row: 8
                                ,col: 5
                                ,index: 89
                            }
                            ,H6: {
                                row: 8
                                ,col: 6
                                ,index: 90
                            }
                            ,H7: {
                                row: 8
                                ,col: 7
                                ,index: 91
                            }
                            ,H8: {
                                row: 8
                                ,col: 8
                                ,index: 92
                            }
                            ,H9: {
                                row: 8
                                ,col: 9
                                ,index: 93
                            }
                            ,H10: {
                                row: 8
                                ,col: 10
                                ,index: 94
                            }
                            ,H11: {
                                row: 8
                                ,col: 11
                                ,index: 95
                            }
                            ,H12: {
                                row: 8
                                ,col: 12
                                ,index: 96
                            }
                        }
                    }

                    return data;
                }
                ,SPTT_0006: function () {
                    var data = {
                        description: 'Generic 384 well plastic plate'
                        ,wellCount: 384
                        ,rowLength: 24
                        ,addSampleId: function (wellRowColumn, id) {
                            this.wellMap[wellRowColumn].sampleId = id;
                        }
                        ,wellMap: {
                            A1: {
                                row: 1
                                ,col: 1
                                ,index: 1
                            }
                            ,A2: {
                                row: 1
                                ,col: 2
                                ,index: 2
                            }
                            ,A3: {
                                row: 1
                                ,col: 3
                                ,index: 3
                            }
                            ,A4: {
                                row: 1
                                ,col: 4
                                ,index: 4
                            }
                            ,A5: {
                                row: 1
                                ,col: 5
                                ,index: 5
                            }
                            ,A6: {
                                row: 1
                                ,col: 6
                                ,index: 6
                            }
                            ,A7: {
                                row: 1
                                ,col: 7
                                ,index: 7
                            }
                            ,A8: {
                                row: 1
                                ,col: 8
                                ,index: 8
                            }
                            ,A9: {
                                row: 1
                                ,col: 9
                                ,index: 9
                            }
                            ,A10: {
                                row: 1
                                ,col: 10
                                ,index: 10
                            }
                            ,A11: {
                                row: 1
                                ,col: 11
                                ,index: 11
                            }
                            ,A12: {
                                row: 1
                                ,col: 12
                                ,index: 12
                            }
                            ,A13: {
                                row: 1
                                ,col: 13
                                ,index: 13
                            }
                            ,A14: {
                                row: 1
                                ,col: 14
                                ,index: 14
                            }
                            ,A15: {
                                row: 1
                                ,col: 15
                                ,index: 15
                            }
                            ,A16: {
                                row: 1
                                ,col: 16
                                ,index: 16
                            }
                            ,A17: {
                                row: 1
                                ,col: 17
                                ,index: 17
                            }
                            ,A18: {
                                row: 1
                                ,col: 18
                                ,index: 18
                            }
                            ,A19: {
                                row: 1
                                ,col: 19
                                ,index: 19
                            }
                            ,A20: {
                                row: 1
                                ,col: 20
                                ,index: 20
                            }
                            ,A21: {
                                row: 1
                                ,col: 21
                                ,index: 21
                            }
                            ,A22: {
                                row: 1
                                ,col: 22
                                ,index: 22
                            }
                            ,A23: {
                                row: 1
                                ,col: 23
                                ,index: 23
                            }
                            ,A24: {
                                row: 1
                                ,col: 24
                                ,index: 24
                            }
                            ,B1: {
                                row: 2
                                ,col: 1
                                ,index: 25
                            }
                            ,B2: {
                                row: 2
                                ,col: 2
                                ,index: 26
                            }
                            ,B3: {
                                row: 2
                                ,col: 3
                                ,index: 27
                            }
                            ,B4: {
                                row: 2
                                ,col: 4
                                ,index: 28
                            }
                            ,B5: {
                                row: 2
                                ,col: 5
                                ,index: 29
                            }
                            ,B6: {
                                row: 2
                                ,col: 6
                                ,index: 30
                            }
                            ,B7: {
                                row: 2
                                ,col: 7
                                ,index: 31
                            }
                            ,B8: {
                                row: 2
                                ,col: 8
                                ,index: 32
                            }
                            ,B9: {
                                row: 2
                                ,col: 9
                                ,index: 33
                            }
                            ,B10: {
                                row: 2
                                ,col: 10
                                ,index: 34
                            }
                            ,B11: {
                                row: 2
                                ,col: 11
                                ,index: 35
                            }
                            ,B12: {
                                row: 2
                                ,col: 12
                                ,index: 36
                            }
                            ,B13: {
                                row: 2
                                ,col: 13
                                ,index: 37
                            }
                            ,B14: {
                                row: 2
                                ,col: 14
                                ,index: 38
                            }
                            ,B15: {
                                row: 2
                                ,col: 15
                                ,index: 39
                            }
                            ,B16: {
                                row: 2
                                ,col: 16
                                ,index: 40
                            }
                            ,B17: {
                                row: 2
                                ,col: 17
                                ,index: 41
                            }
                            ,B18: {
                                row: 2
                                ,col: 18
                                ,index: 42
                            }
                            ,B19: {
                                row: 2
                                ,col: 19
                                ,index: 43
                            }
                            ,B20: {
                                row: 2
                                ,col: 20
                                ,index: 44
                            }
                            ,B21: {
                                row: 2
                                ,col: 21
                                ,index: 45
                            }
                            ,B22: {
                                row: 2
                                ,col: 22
                                ,index: 46
                            }
                            ,B23: {
                                row: 2
                                ,col: 23
                                ,index: 47
                            }
                            ,B24: {
                                row: 2
                                ,col: 24
                                ,index: 48
                            }
                            ,C1: {
                                row: 3
                                ,col: 1
                                ,index: 49
                            }
                            ,C2: {
                                row: 3
                                ,col: 2
                                ,index: 50
                            }
                            ,C3: {
                                row: 3
                                ,col: 3
                                ,index: 51
                            }
                            ,C4: {
                                row: 3
                                ,col: 4
                                ,index: 52
                            }
                            ,C5: {
                                row: 3
                                ,col: 5
                                ,index: 53
                            }
                            ,C6: {
                                row: 3
                                ,col: 6
                                ,index: 54
                            }
                            ,C7: {
                                row: 3
                                ,col: 7
                                ,index: 55
                            }
                            ,C8: {
                                row: 3
                                ,col: 8
                                ,index: 56
                            }
                            ,C9: {
                                row: 3
                                ,col: 9
                                ,index: 57
                            }
                            ,C10: {
                                row: 3
                                ,col: 10
                                ,index: 58
                            }
                            ,C11: {
                                row: 3
                                ,col: 11
                                ,index: 59
                            }
                            ,C12: {
                                row: 3
                                ,col: 12
                                ,index: 60
                            }
                            ,C13: {
                                row: 3
                                ,col: 13
                                ,index: 61
                            }
                            ,C14: {
                                row: 3
                                ,col: 14
                                ,index: 62
                            }
                            ,C15: {
                                row: 3
                                ,col: 15
                                ,index: 63
                            }
                            ,C16: {
                                row: 3
                                ,col: 16
                                ,index: 64
                            }
                            ,C17: {
                                row: 3
                                ,col: 17
                                ,index: 65
                            }
                            ,C18: {
                                row: 3
                                ,col: 18
                                ,index: 66
                            }
                            ,C19: {
                                row: 3
                                ,col: 19
                                ,index: 67
                            }
                            ,C20: {
                                row: 3
                                ,col: 20
                                ,index: 68
                            }
                            ,C21: {
                                row: 3
                                ,col: 21
                                ,index: 69
                            }
                            ,C22: {
                                row: 3
                                ,col: 22
                                ,index: 70
                            }
                            ,C23: {
                                row: 3
                                ,col: 23
                                ,index: 71
                            }
                            ,C24: {
                                row: 3
                                ,col: 24
                                ,index: 72
                            }
                            ,D1: {
                                row: 4
                                ,col: 1
                                ,index: 73
                            }
                            ,D2: {
                                row: 4
                                ,col: 2
                                ,index: 74
                            }
                            ,D3: {
                                row: 4
                                ,col: 3
                                ,index: 75
                            }
                            ,D4: {
                                row: 4
                                ,col: 4
                                ,index: 76
                            }
                            ,D5: {
                                row: 4
                                ,col: 5
                                ,index: 77
                            }
                            ,D6: {
                                row: 4
                                ,col: 6
                                ,index: 78
                            }
                            ,D7: {
                                row: 4
                                ,col: 7
                                ,index: 79
                            }
                            ,D8: {
                                row: 4
                                ,col: 8
                                ,index: 80
                            }
                            ,D9: {
                                row: 4
                                ,col: 9
                                ,index: 81
                            }
                            ,D10: {
                                row: 4
                                ,col: 10
                                ,index: 82
                            }
                            ,D11: {
                                row: 4
                                ,col: 11
                                ,index: 83
                            }
                            ,D12: {
                                row: 4
                                ,col: 12
                                ,index: 84
                            }
                            ,D13: {
                                row: 4
                                ,col: 13
                                ,index: 85
                            }
                            ,D14: {
                                row: 4
                                ,col: 14
                                ,index: 86
                            }
                            ,D15: {
                                row: 4
                                ,col: 15
                                ,index: 87
                            }
                            ,D16: {
                                row: 4
                                ,col: 16
                                ,index: 88
                            }
                            ,D17: {
                                row: 4
                                ,col: 17
                                ,index: 89
                            }
                            ,D18: {
                                row: 4
                                ,col: 18
                                ,index: 90
                            }
                            ,D19: {
                                row: 4
                                ,col: 19
                                ,index: 91
                            }
                            ,D20: {
                                row: 4
                                ,col: 20
                                ,index: 92
                            }
                            ,D21: {
                                row: 4
                                ,col: 21
                                ,index: 93
                            }
                            ,D22: {
                                row: 4
                                ,col: 22
                                ,index: 94
                            }
                            ,D23: {
                                row: 4
                                ,col: 23
                                ,index: 95
                            }
                            ,D24: {
                                row: 4
                                ,col: 24
                                ,index: 96
                            }
                            ,E1: {
                                row: 5
                                ,col: 1
                                ,index: 97
                            }
                            ,E2: {
                                row: 5
                                ,col: 2
                                ,index: 98
                            }
                            ,E3: {
                                row: 5
                                ,col: 3
                                ,index: 99
                            }
                            ,E4: {
                                row: 5
                                ,col: 4
                                ,index: 100
                            }
                            ,E5: {
                                row: 5
                                ,col: 5
                                ,index: 101
                            }
                            ,E6: {
                                row: 5
                                ,col: 6
                                ,index: 102
                            }
                            ,E7: {
                                row: 5
                                ,col: 7
                                ,index: 103
                            }
                            ,E8: {
                                row: 5
                                ,col: 8
                                ,index: 104
                            }
                            ,E9: {
                                row: 5
                                ,col: 9
                                ,index: 105
                            }
                            ,E10: {
                                row: 5
                                ,col: 10
                                ,index: 106
                            }
                            ,E11: {
                                row: 5
                                ,col: 11
                                ,index: 107
                            }
                            ,E12: {
                                row: 5
                                ,col: 12
                                ,index: 108
                            }
                            ,E13: {
                                row: 5
                                ,col: 13
                                ,index: 109
                            }
                            ,E14: {
                                row: 5
                                ,col: 14
                                ,index: 110
                            }
                            ,E15: {
                                row: 5
                                ,col: 15
                                ,index: 111
                            }
                            ,E16: {
                                row: 5
                                ,col: 16
                                ,index: 112
                            }
                            ,E17: {
                                row: 5
                                ,col: 17
                                ,index: 113
                            }
                            ,E18: {
                                row: 5
                                ,col: 18
                                ,index: 114
                            }
                            ,E19: {
                                row: 5
                                ,col: 19
                                ,index: 115
                            }
                            ,E20: {
                                row: 5
                                ,col: 20
                                ,index: 116
                            }
                            ,E21: {
                                row: 5
                                ,col: 21
                                ,index: 117
                            }
                            ,E22: {
                                row: 5
                                ,col: 22
                                ,index: 118
                            }
                            ,E23: {
                                row: 5
                                ,col: 23
                                ,index: 119
                            }
                            ,E24: {
                                row: 5
                                ,col: 24
                                ,index: 120
                            }
                            ,F1: {
                                row: 6
                                ,col: 1
                                ,index: 121
                            }
                            ,F2: {
                                row: 6
                                ,col: 2
                                ,index: 122
                            }
                            ,F3: {
                                row: 6
                                ,col: 3
                                ,index: 123
                            }
                            ,F4: {
                                row: 6
                                ,col: 4
                                ,index: 124
                            }
                            ,F5: {
                                row: 6
                                ,col: 5
                                ,index: 125
                            }
                            ,F6: {
                                row: 6
                                ,col: 6
                                ,index: 126
                            }
                            ,F7: {
                                row: 6
                                ,col: 7
                                ,index: 127
                            }
                            ,F8: {
                                row: 6
                                ,col: 8
                                ,index: 128
                            }
                            ,F9: {
                                row: 6
                                ,col: 9
                                ,index: 129
                            }
                            ,F10: {
                                row: 6
                                ,col: 10
                                ,index: 130
                            }
                            ,F11: {
                                row: 6
                                ,col: 11
                                ,index: 131
                            }
                            ,F12: {
                                row: 6
                                ,col: 12
                                ,index: 132
                            }
                            ,F13: {
                                row: 6
                                ,col: 13
                                ,index: 133
                            }
                            ,F14: {
                                row: 6
                                ,col: 14
                                ,index: 134
                            }
                            ,F15: {
                                row: 6
                                ,col: 15
                                ,index: 135
                            }
                            ,F16: {
                                row: 6
                                ,col: 16
                                ,index: 136
                            }
                            ,F17: {
                                row: 6
                                ,col: 17
                                ,index: 137
                            }
                            ,F18: {
                                row: 6
                                ,col: 18
                                ,index: 138
                            }
                            ,F19: {
                                row: 6
                                ,col: 19
                                ,index: 139
                            }
                            ,F20: {
                                row: 6
                                ,col: 20
                                ,index: 140
                            }
                            ,F21: {
                                row: 6
                                ,col: 21
                                ,index: 141
                            }
                            ,F22: {
                                row: 6
                                ,col: 22
                                ,index: 142
                            }
                            ,F23: {
                                row: 6
                                ,col: 23
                                ,index: 143
                            }
                            ,F24: {
                                row: 6
                                ,col: 24
                                ,index: 144
                            }
                            ,G1: {
                                row: 7
                                ,col: 1
                                ,index: 145
                            }
                            ,G2: {
                                row: 7
                                ,col: 2
                                ,index: 146
                            }
                            ,G3: {
                                row: 7
                                ,col: 3
                                ,index: 147
                            }
                            ,G4: {
                                row: 7
                                ,col: 4
                                ,index: 148
                            }
                            ,G5: {
                                row: 7
                                ,col: 5
                                ,index: 149
                            }
                            ,G6: {
                                row: 7
                                ,col: 6
                                ,index: 150
                            }
                            ,G7: {
                                row: 7
                                ,col: 7
                                ,index: 151
                            }
                            ,G8: {
                                row: 7
                                ,col: 8
                                ,index: 152
                            }
                            ,G9: {
                                row: 7
                                ,col: 9
                                ,index: 153
                            }
                            ,G10: {
                                row: 7
                                ,col: 10
                                ,index: 154
                            }
                            ,G11: {
                                row: 7
                                ,col: 11
                                ,index: 155
                            }
                            ,G12: {
                                row: 7
                                ,col: 12
                                ,index: 156
                            }
                            ,G13: {
                                row: 7
                                ,col: 13
                                ,index: 157
                            }
                            ,G14: {
                                row: 7
                                ,col: 14
                                ,index: 158
                            }
                            ,G15: {
                                row: 7
                                ,col: 15
                                ,index: 159
                            }
                            ,G16: {
                                row: 7
                                ,col: 16
                                ,index: 160
                            }
                            ,G17: {
                                row: 7
                                ,col: 17
                                ,index: 161
                            }
                            ,G18: {
                                row: 7
                                ,col: 18
                                ,index: 162
                            }
                            ,G19: {
                                row: 7
                                ,col: 19
                                ,index: 163
                            }
                            ,G20: {
                                row: 7
                                ,col: 20
                                ,index: 164
                            }
                            ,G21: {
                                row: 7
                                ,col: 21
                                ,index: 165
                            }
                            ,G22: {
                                row: 7
                                ,col: 22
                                ,index: 166
                            }
                            ,G23: {
                                row: 7
                                ,col: 23
                                ,index: 167
                            }
                            ,G24: {
                                row: 7
                                ,col: 24
                                ,index: 168
                            }
                            ,H1: {
                                row: 8
                                ,col: 1
                                ,index: 169
                            }
                            ,H2: {
                                row: 8
                                ,col: 2
                                ,index: 170
                            }
                            ,H3: {
                                row: 8
                                ,col: 3
                                ,index: 171
                            }
                            ,H4: {
                                row: 8
                                ,col: 4
                                ,index: 172
                            }
                            ,H5: {
                                row: 8
                                ,col: 5
                                ,index: 173
                            }
                            ,H6: {
                                row: 8
                                ,col: 6
                                ,index: 174
                            }
                            ,H7: {
                                row: 8
                                ,col: 7
                                ,index: 175
                            }
                            ,H8: {
                                row: 8
                                ,col: 8
                                ,index: 176
                            }
                            ,H9: {
                                row: 8
                                ,col: 9
                                ,index: 177
                            }
                            ,H10: {
                                row: 8
                                ,col: 10
                                ,index: 178
                            }
                            ,H11: {
                                row: 8
                                ,col: 11
                                ,index: 179
                            }
                            ,H12: {
                                row: 8
                                ,col: 12
                                ,index: 180
                            }
                            ,H13: {
                                row: 8
                                ,col: 13
                                ,index: 181
                            }
                            ,H14: {
                                row: 8
                                ,col: 14
                                ,index: 182
                            }
                            ,H15: {
                                row: 8
                                ,col: 15
                                ,index: 183
                            }
                            ,H16: {
                                row: 8
                                ,col: 16
                                ,index: 184
                            }
                            ,H17: {
                                row: 8
                                ,col: 17
                                ,index: 185
                            }
                            ,H18: {
                                row: 8
                                ,col: 18
                                ,index: 186
                            }
                            ,H19: {
                                row: 8
                                ,col: 19
                                ,index: 187
                            }
                            ,H20: {
                                row: 8
                                ,col: 20
                                ,index: 188
                            }
                            ,H21: {
                                row: 8
                                ,col: 21
                                ,index: 189
                            }
                            ,H22: {
                                row: 8
                                ,col: 22
                                ,index: 190
                            }
                            ,H23: {
                                row: 8
                                ,col: 23
                                ,index: 191
                            }
                            ,H24: {
                                row: 8
                                ,col: 24
                                ,index: 192
                            }
                            ,I1: {
                                row: 9
                                ,col: 1
                                ,index: 193
                            }
                            ,I2: {
                                row: 9
                                ,col: 2
                                ,index: 194
                            }
                            ,I3: {
                                row: 9
                                ,col: 3
                                ,index: 195
                            }
                            ,I4: {
                                row: 9
                                ,col: 4
                                ,index: 196
                            }
                            ,I5: {
                                row: 9
                                ,col: 5
                                ,index: 197
                            }
                            ,I6: {
                                row: 9
                                ,col: 6
                                ,index: 198
                            }
                            ,I7: {
                                row: 9
                                ,col: 7
                                ,index: 199
                            }
                            ,I8: {
                                row: 9
                                ,col: 8
                                ,index: 200
                            }
                            ,I9: {
                                row: 9
                                ,col: 9
                                ,index: 201
                            }
                            ,I10: {
                                row: 9
                                ,col: 10
                                ,index: 202
                            }
                            ,I11: {
                                row: 9
                                ,col: 11
                                ,index: 203
                            }
                            ,I12: {
                                row: 9
                                ,col: 12
                                ,index: 204
                            }
                            ,I13: {
                                row: 9
                                ,col: 13
                                ,index: 205
                            }
                            ,I14: {
                                row: 9
                                ,col: 14
                                ,index: 206
                            }
                            ,I15: {
                                row: 9
                                ,col: 15
                                ,index: 207
                            }
                            ,I16: {
                                row: 9
                                ,col: 16
                                ,index: 208
                            }
                            ,I17: {
                                row: 9
                                ,col: 17
                                ,index: 209
                            }
                            ,I18: {
                                row: 9
                                ,col: 18
                                ,index: 210
                            }
                            ,I19: {
                                row: 9
                                ,col: 19
                                ,index: 211
                            }
                            ,I20: {
                                row: 9
                                ,col: 20
                                ,index: 212
                            }
                            ,I21: {
                                row: 9
                                ,col: 21
                                ,index: 213
                            }
                            ,I22: {
                                row: 9
                                ,col: 22
                                ,index: 214
                            }
                            ,I23: {
                                row: 9
                                ,col: 23
                                ,index: 215
                            }
                            ,I24: {
                                row: 9
                                ,col: 24
                                ,index: 216
                            }
                            ,J1: {
                                row: 10
                                ,col: 1
                                ,index: 217
                            }
                            ,J2: {
                                row: 10
                                ,col: 2
                                ,index: 218
                            }
                            ,J3: {
                                row: 10
                                ,col: 3
                                ,index: 219
                            }
                            ,J4: {
                                row: 10
                                ,col: 4
                                ,index: 220
                            }
                            ,J5: {
                                row: 10
                                ,col: 5
                                ,index: 221
                            }
                            ,J6: {
                                row: 10
                                ,col: 6
                                ,index: 222
                            }
                            ,J7: {
                                row: 10
                                ,col: 7
                                ,index: 223
                            }
                            ,J8: {
                                row: 10
                                ,col: 8
                                ,index: 224
                            }
                            ,J9: {
                                row: 10
                                ,col: 9
                                ,index: 225
                            }
                            ,J10: {
                                row: 10
                                ,col: 10
                                ,index: 226
                            }
                            ,J11: {
                                row: 10
                                ,col: 11
                                ,index: 227
                            }
                            ,J12: {
                                row: 10
                                ,col: 12
                                ,index: 228
                            }
                            ,J13: {
                                row: 10
                                ,col: 13
                                ,index: 229
                            }
                            ,J14: {
                                row: 10
                                ,col: 14
                                ,index: 230
                            }
                            ,J15: {
                                row: 10
                                ,col: 15
                                ,index: 231
                            }
                            ,J16: {
                                row: 10
                                ,col: 16
                                ,index: 232
                            }
                            ,J17: {
                                row: 10
                                ,col: 17
                                ,index: 233
                            }
                            ,J18: {
                                row: 10
                                ,col: 18
                                ,index: 234
                            }
                            ,J19: {
                                row: 10
                                ,col: 19
                                ,index: 235
                            }
                            ,J20: {
                                row: 10
                                ,col: 20
                                ,index: 236
                            }
                            ,J21: {
                                row: 10
                                ,col: 21
                                ,index: 237
                            }
                            ,J22: {
                                row: 10
                                ,col: 22
                                ,index: 238
                            }
                            ,J23: {
                                row: 10
                                ,col: 23
                                ,index: 239
                            }
                            ,J24: {
                                row: 10
                                ,col: 24
                                ,index: 240
                            }
                            ,K1: {
                                row: 11
                                ,col: 1
                                ,index: 241
                            }
                            ,K2: {
                                row: 11
                                ,col: 2
                                ,index: 242
                            }
                            ,K3: {
                                row: 11
                                ,col: 3
                                ,index: 243
                            }
                            ,K4: {
                                row: 11
                                ,col: 4
                                ,index: 244
                            }
                            ,K5: {
                                row: 11
                                ,col: 5
                                ,index: 245
                            }
                            ,K6: {
                                row: 11
                                ,col: 6
                                ,index: 246
                            }
                            ,K7: {
                                row: 11
                                ,col: 7
                                ,index: 247
                            }
                            ,K8: {
                                row: 11
                                ,col: 8
                                ,index: 248
                            }
                            ,K9: {
                                row: 11
                                ,col: 9
                                ,index: 249
                            }
                            ,K10: {
                                row: 11
                                ,col: 10
                                ,index: 250
                            }
                            ,K11: {
                                row: 11
                                ,col: 11
                                ,index: 251
                            }
                            ,K12: {
                                row: 11
                                ,col: 12
                                ,index: 252
                            }
                            ,K13: {
                                row: 11
                                ,col: 13
                                ,index: 253
                            }
                            ,K14: {
                                row: 11
                                ,col: 14
                                ,index: 254
                            }
                            ,K15: {
                                row: 11
                                ,col: 15
                                ,index: 255
                            }
                            ,K16: {
                                row: 11
                                ,col: 16
                                ,index: 256
                            }
                            ,K17: {
                                row: 11
                                ,col: 17
                                ,index: 257
                            }
                            ,K18: {
                                row: 11
                                ,col: 18
                                ,index: 258
                            }
                            ,K19: {
                                row: 11
                                ,col: 19
                                ,index: 259
                            }
                            ,K20: {
                                row: 11
                                ,col: 20
                                ,index: 260
                            }
                            ,K21: {
                                row: 11
                                ,col: 21
                                ,index: 261
                            }
                            ,K22: {
                                row: 11
                                ,col: 22
                                ,index: 262
                            }
                            ,K23: {
                                row: 11
                                ,col: 23
                                ,index: 263
                            }
                            ,K24: {
                                row: 11
                                ,col: 24
                                ,index: 264
                            }
                            ,L1: {
                                row: 12
                                ,col: 1
                                ,index: 265
                            }
                            ,L2: {
                                row: 12
                                ,col: 2
                                ,index: 266
                            }
                            ,L3: {
                                row: 12
                                ,col: 3
                                ,index: 267
                            }
                            ,L4: {
                                row: 12
                                ,col: 4
                                ,index: 268
                            }
                            ,L5: {
                                row: 12
                                ,col: 5
                                ,index: 269
                            }
                            ,L6: {
                                row: 12
                                ,col: 6
                                ,index: 270
                            }
                            ,L7: {
                                row: 12
                                ,col: 7
                                ,index: 271
                            }
                            ,L8: {
                                row: 12
                                ,col: 8
                                ,index: 272
                            }
                            ,L9: {
                                row: 12
                                ,col: 9
                                ,index: 273
                            }
                            ,L10: {
                                row: 12
                                ,col: 10
                                ,index: 274
                            }
                            ,L11: {
                                row: 12
                                ,col: 11
                                ,index: 275
                            }
                            ,L12: {
                                row: 12
                                ,col: 12
                                ,index: 276
                            }
                            ,L13: {
                                row: 12
                                ,col: 13
                                ,index: 277
                            }
                            ,L14: {
                                row: 12
                                ,col: 14
                                ,index: 278
                            }
                            ,L15: {
                                row: 12
                                ,col: 15
                                ,index: 279
                            }
                            ,L16: {
                                row: 12
                                ,col: 16
                                ,index: 280
                            }
                            ,L17: {
                                row: 12
                                ,col: 17
                                ,index: 281
                            }
                            ,L18: {
                                row: 12
                                ,col: 18
                                ,index: 282
                            }
                            ,L19: {
                                row: 12
                                ,col: 19
                                ,index: 283
                            }
                            ,L20: {
                                row: 12
                                ,col: 20
                                ,index: 284
                            }
                            ,L21: {
                                row: 12
                                ,col: 21
                                ,index: 285
                            }
                            ,L22: {
                                row: 12
                                ,col: 22
                                ,index: 286
                            }
                            ,L23: {
                                row: 12
                                ,col: 23
                                ,index: 287
                            }
                            ,L24: {
                                row: 12
                                ,col: 24
                                ,index: 288
                            }
                            ,M1: {
                                row: 13
                                ,col: 1
                                ,index: 289
                            }
                            ,M2: {
                                row: 13
                                ,col: 2
                                ,index: 290
                            }
                            ,M3: {
                                row: 13
                                ,col: 3
                                ,index: 291
                            }
                            ,M4: {
                                row: 13
                                ,col: 4
                                ,index: 292
                            }
                            ,M5: {
                                row: 13
                                ,col: 5
                                ,index: 293
                            }
                            ,M6: {
                                row: 13
                                ,col: 6
                                ,index: 294
                            }
                            ,M7: {
                                row: 13
                                ,col: 7
                                ,index: 295
                            }
                            ,M8: {
                                row: 13
                                ,col: 8
                                ,index: 296
                            }
                            ,M9: {
                                row: 13
                                ,col: 9
                                ,index: 297
                            }
                            ,M10: {
                                row: 13
                                ,col: 10
                                ,index: 298
                            }
                            ,M11: {
                                row: 13
                                ,col: 11
                                ,index: 299
                            }
                            ,M12: {
                                row: 13
                                ,col: 12
                                ,index: 300
                            }
                            ,M13: {
                                row: 13
                                ,col: 13
                                ,index: 301
                            }
                            ,M14: {
                                row: 13
                                ,col: 14
                                ,index: 302
                            }
                            ,M15: {
                                row: 13
                                ,col: 15
                                ,index: 303
                            }
                            ,M16: {
                                row: 13
                                ,col: 16
                                ,index: 304
                            }
                            ,M17: {
                                row: 13
                                ,col: 17
                                ,index: 305
                            }
                            ,M18: {
                                row: 13
                                ,col: 18
                                ,index: 306
                            }
                            ,M19: {
                                row: 13
                                ,col: 19
                                ,index: 307
                            }
                            ,M20: {
                                row: 13
                                ,col: 20
                                ,index: 308
                            }
                            ,M21: {
                                row: 13
                                ,col: 21
                                ,index: 309
                            }
                            ,M22: {
                                row: 13
                                ,col: 22
                                ,index: 310
                            }
                            ,M23: {
                                row: 13
                                ,col: 23
                                ,index: 311
                            }
                            ,M24: {
                                row: 13
                                ,col: 24
                                ,index: 312
                            }
                            ,N1: {
                                row: 14
                                ,col: 1
                                ,index: 313
                            }
                            ,N2: {
                                row: 14
                                ,col: 2
                                ,index: 314
                            }
                            ,N3: {
                                row: 14
                                ,col: 3
                                ,index: 315
                            }
                            ,N4: {
                                row: 14
                                ,col: 4
                                ,index: 316
                            }
                            ,N5: {
                                row: 14
                                ,col: 5
                                ,index: 317
                            }
                            ,N6: {
                                row: 14
                                ,col: 6
                                ,index: 318
                            }
                            ,N7: {
                                row: 14
                                ,col: 7
                                ,index: 319
                            }
                            ,N8: {
                                row: 14
                                ,col: 8
                                ,index: 320
                            }
                            ,N9: {
                                row: 14
                                ,col: 9
                                ,index: 321
                            }
                            ,N10: {
                                row: 14
                                ,col: 10
                                ,index: 322
                            }
                            ,N11: {
                                row: 14
                                ,col: 11
                                ,index: 323
                            }
                            ,N12: {
                                row: 14
                                ,col: 12
                                ,index: 324
                            }
                            ,N13: {
                                row: 14
                                ,col: 13
                                ,index: 325
                            }
                            ,N14: {
                                row: 14
                                ,col: 14
                                ,index: 326
                            }
                            ,N15: {
                                row: 14
                                ,col: 15
                                ,index: 327
                            }
                            ,N16: {
                                row: 14
                                ,col: 16
                                ,index: 328
                            }
                            ,N17: {
                                row: 14
                                ,col: 17
                                ,index: 329
                            }
                            ,N18: {
                                row: 14
                                ,col: 18
                                ,index: 330
                            }
                            ,N19: {
                                row: 14
                                ,col: 19
                                ,index: 331
                            }
                            ,N20: {
                                row: 14
                                ,col: 20
                                ,index: 332
                            }
                            ,N21: {
                                row: 14
                                ,col: 21
                                ,index: 333
                            }
                            ,N22: {
                                row: 14
                                ,col: 22
                                ,index: 334
                            }
                            ,N23: {
                                row: 14
                                ,col: 23
                                ,index: 335
                            }
                            ,N24: {
                                row: 14
                                ,col: 24
                                ,index: 336
                            }
                            ,O1: {
                                row: 15
                                ,col: 1
                                ,index: 337
                            }
                            ,O2: {
                                row: 15
                                ,col: 2
                                ,index: 338
                            }
                            ,O3: {
                                row: 15
                                ,col: 3
                                ,index: 339
                            }
                            ,O4: {
                                row: 15
                                ,col: 4
                                ,index: 340
                            }
                            ,O5: {
                                row: 15
                                ,col: 5
                                ,index: 341
                            }
                            ,O6: {
                                row: 15
                                ,col: 6
                                ,index: 342
                            }
                            ,O7: {
                                row: 15
                                ,col: 7
                                ,index: 343
                            }
                            ,O8: {
                                row: 15
                                ,col: 8
                                ,index: 344
                            }
                            ,O9: {
                                row: 15
                                ,col: 9
                                ,index: 345
                            }
                            ,O10: {
                                row: 15
                                ,col: 10
                                ,index: 346
                            }
                            ,O11: {
                                row: 15
                                ,col: 11
                                ,index: 347
                            }
                            ,O12: {
                                row: 15
                                ,col: 12
                                ,index: 348
                            }
                            ,O13: {
                                row: 15
                                ,col: 13
                                ,index: 349
                            }
                            ,O14: {
                                row: 15
                                ,col: 14
                                ,index: 350
                            }
                            ,O15: {
                                row: 15
                                ,col: 15
                                ,index: 351
                            }
                            ,O16: {
                                row: 15
                                ,col: 16
                                ,index: 352
                            }
                            ,O17: {
                                row: 15
                                ,col: 17
                                ,index: 353
                            }
                            ,O18: {
                                row: 15
                                ,col: 18
                                ,index: 354
                            }
                            ,O19: {
                                row: 15
                                ,col: 19
                                ,index: 355
                            }
                            ,O20: {
                                row: 15
                                ,col: 20
                                ,index: 356
                            }
                            ,O21: {
                                row: 15
                                ,col: 21
                                ,index: 357
                            }
                            ,O22: {
                                row: 15
                                ,col: 22
                                ,index: 358
                            }
                            ,O23: {
                                row: 15
                                ,col: 23
                                ,index: 359
                            }
                            ,O24: {
                                row: 15
                                ,col: 24
                                ,index: 360
                            }
                            ,P1: {
                                row: 16
                                ,col: 1
                                ,index: 361
                            }
                            ,P2: {
                                row: 16
                                ,col: 2
                                ,index: 362
                            }
                            ,P3: {
                                row: 16
                                ,col: 3
                                ,index: 363
                            }
                            ,P4: {
                                row: 16
                                ,col: 4
                                ,index: 364
                            }
                            ,P5: {
                                row: 16
                                ,col: 5
                                ,index: 365
                            }
                            ,P6: {
                                row: 16
                                ,col: 6
                                ,index: 366
                            }
                            ,P7: {
                                row: 16
                                ,col: 7
                                ,index: 367
                            }
                            ,P8: {
                                row: 16
                                ,col: 8
                                ,index: 368
                            }
                            ,P9: {
                                row: 16
                                ,col: 9
                                ,index: 369
                            }
                            ,P10: {
                                row: 16
                                ,col: 10
                                ,index: 370
                            }
                            ,P11: {
                                row: 16
                                ,col: 11
                                ,index: 371
                            }
                            ,P12: {
                                row: 16
                                ,col: 12
                                ,index: 372
                            }
                            ,P13: {
                                row: 16
                                ,col: 13
                                ,index: 373
                            }
                            ,P14: {
                                row: 16
                                ,col: 14
                                ,index: 374
                            }
                            ,P15: {
                                row: 16
                                ,col: 15
                                ,index: 375
                            }
                            ,P16: {
                                row: 16
                                ,col: 16
                                ,index: 376
                            }
                            ,P17: {
                                row: 16
                                ,col: 17
                                ,index: 377
                            }
                            ,P18: {
                                row: 16
                                ,col: 18
                                ,index: 378
                            }
                            ,P19: {
                                row: 16
                                ,col: 19
                                ,index: 379
                            }
                            ,P20: {
                                row: 16
                                ,col: 20
                                ,index: 380
                            }
                            ,P21: {
                                row: 16
                                ,col: 21
                                ,index: 381
                            }
                            ,P22: {
                                row: 16
                                ,col: 22
                                ,index: 382
                            }
                            ,P23: {
                                row: 16
                                ,col: 23
                                ,index: 383
                            }
                            ,P24: {
                                row: 16
                                ,col: 24
                                ,index: 384
                            }
                        }
                    }

                    return data;
                }
            }
        }
    }
]);
    