"""Constants used in the Sample Tracker application."""

# ------------------------------
# Transform template IDs
# ------------------------------
TRANS_TPL_SAME_TO_SAME = 1
TRANS_TPL_SAME_PLATE = 2
TRANS_TPL_MULTIPLEX_SAME_PLATE = 4
TRANS_TPL_96_TO_384 = 18
TRANS_TPL_PLATE_MERGE = 23
TRANS_TPL_REBATCH_FOR_TRANSFORM = 25
TRANS_TPL_FRAG_ANALYZER = 26
TRANS_TPL_NGS_QC_PASSING = 27
TRANS_TPL_EXTRACTION_TITIN = 34
TRANS_TPL_PCA_PREPLANNING = 35
TRANS_TPL_PCR_PRIMER_HITPICK = 36
TRANS_TPL_NGS_INDEX_HITPICKING = 30
TRANS_TPL_NGS_POOLING = 31
TRANS_TPL_MIN_HITPICKING_FOR_MINIPREP = 32
TRANS_TPL_PCA_PCR_PURIFICATION = 42
TRANS_TPL_ECR_PCR_PLANNING = 39
TRANS_TPL_ECR_PCR_SOURCE_PLATE_CREATION = 44
TRANS_TPL_ECR_PCR_PRIMER_HITPICKING = 40
TRANS_TPL_ECR_PCR_MASTER_MIX_ADDITION = 45

# ------------------------------
# Transform type IDs
# ------------------------------
TRANS_TYPE_CLO_INSERT_HITPICK = 2

TRANS_TYPE_QPIX_PICK_COLONIES = 15
TRANS_TYPE_QPIX_TO_384_WELL = 16

TRANS_TYPE_HITPICK_MINIPREP = 39
TRANS_TYPE_HITPICK_SHIP_PLATES = 48
TRANS_TYPE_HITPICK_SHIP_TUBES = 51

TRANS_TYPE_PRIMER_HITPICK_CREATE_SRC = 54
TRANS_TYPE_ADD_PCA_MASTER_MIX = 55
TRANS_TYPE_PCA_THERMOCYCLE = 56
TRANS_TYPE_PCR_PRIMER_HITPICK = 57
TRANS_TYPE_PCA_PCR_ADD_MMIX = 58
TRANS_TYPE_PCA_PCR_THERMOCYCLE = 59
TRANS_TYPE_UPLOAD_QUANT = 60
TRANS_TYPE_POST_PCA_NORM = 61
TRANS_TYPE_PCA_PREPLANNING = 53
TRANS_TYPE_NGS_INDEX_HITPICKING = 26
TRANS_TYPE_NGS_MASTERMIX_ADDITION = 82
TRANS_TYPE_NGS_THERMOCYCLE = 27
TRANS_TYPE_NGS_LOAD_ON_SEQUENCER = 84
TRANS_TYPE_REBATCH_FOR_TRANSFORM = 45
TRANS_TYPE_ECR_PCR_PLANNING = 67
TRANS_TYPE_ECR_PCR_SOURCE_PLATE_CREATION = 68
TRANS_TYPE_ECR_PCR_PRIMER_HITPICKING = 69
TRANS_TYPE_ECR_PCR_MASTER_MIX_ADDITION = 70
TRANS_TYPE_ECR_PCR_THERMOCYCLE = 71
TRANS_TYPE_ECR_PCR_UPLOAD_QUANT = 74
TRANS_TYPE_PLS_DILUTION = 77


# -------------------------------
# BARCODED OBJECTS ETC
# -------------------------------

HAMILTONS = {
    "iHAM03": {
        "label": "Jupiter 2 - STAR Plus",
        "type": "Star Plus",
        "barcode": "iHAM03",
        "trackCount": 68,
        "deckRegions": {
            "left side": {
                "trackWidth": 30,
                "startTrack": 1
            },
            "middle partition": {
                "trackWidth": 12,
                "startTrack": 31
            },
            "right side": {
                "trackWidth": 24,
                "startTrack": 43
            }
        }
    },
    "iHAM04": {
        "label": "Galactica - STAR",
        "type": "Star Plus",
        "barcode": "iHAM04",
        "trackCount": 54,
        "deckRegions": {
            "main": {
                "trackWidth": 54,
                "startTrack": 1
            }
        }
    },
    "iHAM02": {
        "label": "Enterprise - STAR",
        "type": "Star",
        "barcode": "iHAM02",
        "trackCount": 54,
        "deckRegions": {
            "main": {
                "trackWidth": 54,
                "startTrack": 1
            }
        }
    },
    "iHAM01": {
        "label": "Millenium Falcon - STAR",
        "type": "Star",
        "barcode": "iHAM01",
        "trackCount": 54,
        "deckRegions": {
            "main": {
                "trackWidth": 54,
                "startTrack": 1
            }
        }
    }
}

CARRIERS = {
    "cL5A001": {
        "type": "L5AC",
        "positions": {
            "cL5A001_01": {
                "index": 1
            },
            "cL5A001_02": {
                "index": 2
            },"cL5A001_03": {
                "index": 3
            },
            "cL5A001_04": {
                "index": 4
            },
            "cL5A001_05": {
                "index": 5
            }

        }
    },
    "cL5A002": {
        "type": "L5AC",
        "positions": {
            "cL5A002_01": {
                "index": 1
            },
            "cL5A002_02": {
                "index": 2
            },
            "cL5A002_03": {
                "index": 3
            },
            "cL5A002_04": {
                "index": 4
            },
            "cL5A002_05": {
                "index": 5
            }

        }
    },
    "cL5A003": {
        "type": "L5AC",
        "positions": {
            "cL5A003_01": {
                "index": 1
            },
            "cL5A003_02": {
                "index": 2
            },
            "cL5A003_03": {
                "index": 3
            },
            "cL5A003_04": {
                "index": 4
            },
            "cL5A003_05": {
                "index": 5
            }

        }
    },
    "cL5A004": {
        "type": "L5AC",
        "positions": {
            "cL5A004_01": {
                "index": 1
            },"cL5A004_02": {
                "index": 2
            },
            "cL5A004_03": {
                "index": 3
            },
            "cL5A004_04": {
                "index": 4
            },
            "cL5A004_05": {
                "index": 5
            }

        }
    },
    "cL5A005": {
        "type": "L5AC",
        "positions": {
            "cL5A005_01": {
                "index": 1
            },
            "cL5A005_02": {
                "index": 2
            },
            "cL5A005_03": {
                "index": 3
            },
            "cL5A005_04": {
                "index": 4
            },
            "cL5A005_05": {
                "index": 5
            }

        }
    },
    "cL5A006": {
        "type": "L5AC",
        "positions": {
            "cL5A006_01": {
                "index": 1
            },
            "cL5A006_02": {
                "index": 2
            },
            "cL5A006_03": {
                "index": 3
            },
            "cL5A006_04": {
                "index": 4
            },
            "cL5A006_05": {
                "index": 5
            }
        }
    },
    "cL5A007": {
        "type": "L5AC",
        "positions": {
            "cL5A007_01": {
                "index": 1
            },
            "cL5A007_02": {
                "index": 2
            },
            "cL5A007_03": {
                "index": 3
            },
            "cL5A007_04": {
                "index": 4
            },
            "cL5A007_05": {
                "index": 5
            }
        }
    },
    "cL5A008": {
        "type": "L5AC",
        "positions": {
            "cL5A008_01": {
                "index": 1
            },
            "cL5A008_02": {
                "index": 2
            },
            "cL5A008_03": {
                "index": 3
            },
            "cL5A008_04": {
                "index": 4
            }
            ,"cL5A008_05": {
                "index": 5
            }

        }
    },
    "cL5A009": {
        "type": "L5AC",
        "positions": {
            "cL5A009_01": {
                "index": 1
            },
            "cL5A009_02": {
                "index": 2
            },
            "cL5A009_03": {
                "index": 3
            },
            "cL5A009_04": {
                "index": 4
            }
            ,"cL5A009_05": {
                "index": 5
            }

        }
    },
    "cL5A010": {
        "type": "L5AC",
        "positions": {
            "cL5A010_01": {
                "index": 1
            },
            "cL5A010_02": {
                "index": 2
            },
            "cL5A010_03": {
                "index": 3
            },
            "cL5A010_04": {
                "index": 4
            }
            ,"cL5A010_05": {
                "index": 5
            }

        }
    },
    "cL5A011": {
        "type": "L5AC",
        "positions": {
            "cL5A011_01": {
                "index": 1
            },
            "cL5A011_02": {
                "index": 2
            },
            "cL5A011_03": {
                "index": 3
            },
            "cL5A011_04": {
                "index": 4
            }
            ,"cL5A011_05": {
                "index": 5
            }

        }
    },
    "cL5A012": {
        "type": "L5AC",
        "positions": {
            "cL5A012_01": {
                "index": 1
            },
            "cL5A012_02": {
                "index": 2
            },
            "cL5A012_03": {
                "index": 3
            },
            "cL5A012_04": {
                "index": 4
            }
            ,"cL5A012_05": {
                "index": 5
            }

        }
    },
    "cL5A013": {
        "type": "L5AC",
        "positions": {
            "cL5A013_01": {
                "index": 1
            },
            "cL5A013_02": {
                "index": 2
            },
            "cL5A013_03": {
                "index": 3
            },
            "cL5A013_04": {
                "index": 4
            }
            ,"cL5A013_05": {
                "index": 5
            }

        }
    },
    "cL5A014": {
        "type": "L5AC",
        "positions": {
            "cL5A014_01": {
                "index": 1
            },
            "cL5A014_02": {
                "index": 2
            },
            "cL5A014_03": {
                "index": 3
            },
            "cL5A014_04": {
                "index": 4
            }
            ,"cL5A014_05": {
                "index": 5
            }

        }
    },
    "cL5A015": {
        "type": "L5AC",
        "positions": {
            "cL5A015_01": {
                "index": 1
            },
            "cL5A015_02": {
                "index": 2
            },
            "cL5A015_03": {
                "index": 3
            },
            "cL5A015_04": {
                "index": 4
            }
            ,"cL5A015_05": {
                "index": 5
            }

        }
    },
    "cL5A016": {
        "type": "L5AC",
        "positions": {
            "cL5A016_01": {
                "index": 1
            },
            "cL5A016_02": {
                "index": 2
            },
            "cL5A016_03": {
                "index": 3
            },
            "cL5A016_04": {
                "index": 4
            }
            ,"cL5A016_05": {
                "index": 5
            }

        }
    },
    "cAPE001": {
        "type": "APE",
        "positions": {
            "cAPE001_01": {
                "index": 1
            },
            "cAPE001_02": {
                "index": 2
            },
            "cAPE001_03": {
                "index": 3
            },
            "cAPE001_04": {
                "index": 4
            }
            ,"cAPE001_05": {
                "index": 5
            }

        }
    },
    "cAPE002": {
        "type": "APE",
        "positions": {
            "cAPE002_01": {
                "index": 1
            },
            "cAPE002_02": {
                "index": 2
            },
            "cAPE002_03": {
                "index": 3
            },
            "cAPE002_04": {
                "index": 4
            }
            ,"cAPE002_05": {
                "index": 5
            }
        }
    },
    "cNTR001": {
        "type": "NTR"
    },
    "cNTR002": {
        "type": "NTR"
    },
    "cNTR003": {
        "type": "NTR"
    },
    "cNTR004": {
        "type": "NTR"
    },
    "cNTR005": {
        "type": "NTR"
    },
    "cNTR006": {
        "type": "NTR"
    },
    "cNTR007": {
        "type": "NTR"
    },
    "cNTR008": {
        "type": "NTR"
    },
    "c384P001": {
        "type": "PCR_L5_384",
        "positions": {
            "c384P001_01": {
                "index": 1
            },
            "c384P001_02": {
                "index": 2
            },
            "c384P001_03": {
                "index": 3
            },
            "c384P001_04": {
                "index": 4
            }
            ,"c384P001_05": {
                "index": 5
            }
        }
    },
    "c384P002": {
        "type": "PCR_L5_384",
        "positions": {
            "c384P002_01": {
                "index": 1
            },
            "c384P002_02": {
                "index": 2
            },
            "c384P002_03": {
                "index": 3
            },
            "c384P002_04": {
                "index": 4
            }
            ,"c384P002_05": {
                "index": 5
            }
        }
    },
    "c384P003": {
        "type": "PCR_L5_384",
        "positions": {
            "c384P003_01": {
                "index": 1
            },
            "c384P003_02": {
                "index": 2
            },
            "c384P003_03": {
                "index": 3
            },
            "c384P003_04": {
                "index": 4
            }
            ,"c384P003_05": {
                "index": 5
            }
        }
    },
    "c384P004": {
        "type": "PCR_L5_384",
        "positions": {
            "c384P004_01": {
                "index": 1
            },
            "c384P004_02": {
                "index": 2
            },
            "c384P004_03": {
                "index": 3
            },
            "c384P004_04": {
                "index": 4
            }
            ,"c384P004_05": {
                "index": 5
            }
        }
    },
    "c96P001": {
        "type": "PCR_L5_96",
        "positions": {
            "c96P001_01": {
                "index": 1
            },
            "c96P001_02": {
                "index": 2
            },
            "c96P001_03": {
                "index": 3
            },
            "c96P001_04": {
                "index": 4
            }
            ,"c96P001_05": {
                "index": 5
            }
        }
    },
    "c96P002": {
        "type": "PCR_L5_96",
        "positions": {
            "c96P002_01": {
                "index": 1
            },
            "c96P002_02": {
                "index": 2
            },
            "c96P002_03": {
                "index": 3
            },
            "c96P002_04": {
                "index": 4
            }
            ,"c96P002_05": {
                "index": 5
            }
        }
    },
    "c480T001": {
        "type": "TIP_480"
    },
    "c480T002": {
        "type": "TIP_480"
    },
    "c480T003": {
        "type": "TIP_480"
    },
    "c480T004": {
        "type": "TIP_480"
    },
    "cQTRY001": {
        "type": "QTRY",
        "positions": {
            "cQTRY001_01": {
                "index": 1
            },
            "cQTRY001_02": {
                "index": 2
            },
            "cQTRY001_03": {
                "index": 3
            },
            "cQTRY001_04": {
                "index": 4
            }
        }
    },
    "cQTRY002": {
        "type": "QTRY",
        "positions": {
            "cQTRY002_01": {
                "index": 1
            },
            "cQTRY002_02": {
                "index": 2
            },
            "cQTRY002_03": {
                "index": 3
            },
            "cQTRY002_04": {
                "index": 4
            }
        }
    },
    "cQTRY003": {
        "type": "QTRY",
        "positions": {
            "cQTRY003_01": {
                "index": 1
            },
            "cQTRY003_02": {
                "index": 2
            },
            "cQTRY003_03": {
                "index": 3
            },
            "cQTRY003_04": {
                "index": 4
            }
        }
    },
    "c5T001": {
        "type": "TIP_5POS"
    },
    "c96TH001": {
        "type": "96_TUBE"
    },
    "cHPC001": {
        "type": "HPC",
        "positions": {
            "cHPC001_01": {
                "index": 1
            },
            "cHPC001_02": {
                "index": 2
            },
            "cHPC001_03": {
                "index": 3
            },
            "cHPC001_04": {
                "index": 4
            }
            ,"cHPC001_05": {
                "index": 5
            }
        }
    },
    "cHPC002": {
        "type": "HPC",
        "positions": {
            "cHPC002_01": {
                "index": 1
            },
            "cHPC002_02": {
                "index": 2
            },
            "cHPC002_03": {
                "index": 3
            },
            "cHPC002_04": {
                "index": 4
            }
            ,"cHPC002_05": {
                "index": 5
            }
        }
    },
    "cHPC003": {
        "type": "HPC",
        "positions": {
            "cHPC003_01": {
                "index": 1
            },
            "cHPC003_02": {
                "index": 2
            },
            "cHPC003_03": {
                "index": 3
            },
            "cHPC003_04": {
                "index": 4
            }
            ,"cHPC003_05": {
                "index": 5
            }
        }
    }

}
