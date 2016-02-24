"""Constants used in the Sample Tracker application."""

# ------------------------------
# Transform template IDs
# ------------------------------
TRANS_TPL_SAME_TO_SAME = 1
TRANS_TPL_SAME_PLATE = 2
TRANS_TPL_96_TO_384 = 18
TRANS_TPL_PLATE_MERGE = 23
TRANS_TPL_REBATCH_FOR_TRANSFORM = 25
TRANS_TPL_FRAG_ANALYZER = 26
TRANS_TPL_NGS_QC_PASSING = 27
TRANS_TPL_EXTRACTION_TITIN = 34
TRANS_TPL_PCA_PREPLANNING = 35
TRANS_TPL_PCR_PRIMER_HITPICK = 36
TRANS_TPL_NGS_POOLING = 31
TRANS_TPL_MIN_HITPICKING_FOR_MINIPREP = 32
TRANS_TPL_PCA_PCR_PURIFICATION = 42

# ------------------------------
# Transform type IDs
# ------------------------------
TRANS_TYPE_CLO_INSERT_HITPICK = 2

TRANS_TYPE_QPIX_PICK_COLONIES = 15
TRANS_TYPE_QPIX_TO_384_WELL = 16

TRANS_TYPE_NGS_HITPICK_INDEXING = 26

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



# -------------------------------
# BARCODED OBJECTS ETC
# -------------------------------

HAMILTONS = {
    "iHAM04": {
        "label": "Jupiter 2 - STAR Plus",
        "type": "Star Plus",
        "barcode": "iHAM04",
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
    "iHAM01": {
        "label": "Galactica - STAR",
        "type": "Star Plus",
        "barcode": "iHAM01",
        "trackCount": 54,
        "deckRegions": {
            "main": {
                "trackWidth": 54,
                "startTrack": 1
            }
        }
    },
    "iHAM0X": {
        "label": "Enterprise - STAR",
        "type": "Star",
        "barcode": "iHAM0X",
        "trackCount": 54,
        "deckRegions": {
            "main": {
                "trackWidth": 54,
                "startTrack": 1
            }
        }
    },
    "iHAM0Y": {
        "label": "Millenium Falcon - STAR",
        "type": "Star",
        "barcode": "iHAM0Y",
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
            "cL5A001-01": {
                "index": 1
            },
            "cL5A001-02": {
                "index": 2
            },"cL5A001-03": {
                "index": 3
            },
            "cL5A001-04": {
                "index": 4
            },
            "cL5A001-05": {
                "index": 5
            }

        }
    },
    "cL5A002": {
        "type": "L5AC",
        "positions": {
            "cL5A002-01": {
                "index": 1
            },
            "cL5A002-02": {
                "index": 2
            },
            "cL5A002-03": {
                "index": 3
            },
            "cL5A002-04": {
                "index": 4
            },
            "cL5A002-05": {
                "index": 5
            }

        }
    },
    "cL5A003": {
        "type": "L5AC",
        "positions": {
            "cL5A003-01": {
                "index": 1
            },
            "cL5A003-02": {
                "index": 2
            },
            "cL5A003-03": {
                "index": 3
            },
            "cL5A003-04": {
                "index": 4
            },
            "cL5A003-05": {
                "index": 5
            }

        }
    },
    "cL5A004": {
        "type": "L5AC",
        "positions": {
            "cL5A004-01": {
                "index": 1
            },"cL5A004-02": {
                "index": 2
            },
            "cL5A004-03": {
                "index": 3
            },
            "cL5A004-04": {
                "index": 4
            },
            "cL5A004-05": {
                "index": 5
            }

        }
    },
    "cL5A005": {
        "type": "L5AC",
        "positions": {
            "cL5A005-01": {
                "index": 1
            },
            "cL5A005-02": {
                "index": 2
            },
            "cL5A005-03": {
                "index": 3
            },
            "cL5A005-04": {
                "index": 4
            },
            "cL5A005-05": {
                "index": 5
            }

        }
    },
    "cL5A006": {
        "type": "L5AC",
        "positions": {
            "cL5A006-01": {
                "index": 1
            },
            "cL5A006-02": {
                "index": 2
            },
            "cL5A006-03": {
                "index": 3
            },
            "cL5A006-04": {
                "index": 4
            },
            "cL5A006-05": {
                "index": 5
            }
        }
    },
    "cL5A007": {
        "type": "L5AC",
        "positions": {
            "cL5A007-01": {
                "index": 1
            },
            "cL5A007-02": {
                "index": 2
            },
            "cL5A007-03": {
                "index": 3
            },
            "cL5A007-04": {
                "index": 4
            },
            "cL5A007-05": {
                "index": 5
            }
        }
    },
    "cL5A008": {
        "type": "L5AC",
        "positions": {
            "cL5A008-01": {
                "index": 1
            },
            "cL5A008-02": {
                "index": 2
            },
            "cL5A008-03": {
                "index": 3
            },
            "cL5A008-04": {
                "index": 4
            }
            ,"cL5A008-05": {
                "index": 5
            }

        }
    },
    "cL5A009": {
        "type": "L5AC",
        "positions": {
            "cL5A009-01": {
                "index": 1
            },
            "cL5A009-02": {
                "index": 2
            },
            "cL5A009-03": {
                "index": 3
            },
            "cL5A009-04": {
                "index": 4
            }
            ,"cL5A009-05": {
                "index": 5
            }

        }
    },
    "cL5A010": {
        "type": "L5AC",
        "positions": {
            "cL5A010-01": {
                "index": 1
            },
            "cL5A010-02": {
                "index": 2
            },
            "cL5A010-03": {
                "index": 3
            },
            "cL5A010-04": {
                "index": 4
            }
            ,"cL5A010-05": {
                "index": 5
            }

        }
    },
    "cL5A011": {
        "type": "L5AC",
        "positions": {
            "cL5A011-01": {
                "index": 1
            },
            "cL5A011-02": {
                "index": 2
            },
            "cL5A011-03": {
                "index": 3
            },
            "cL5A011-04": {
                "index": 4
            }
            ,"cL5A011-05": {
                "index": 5
            }

        }
    },
    "cL5A012": {
        "type": "L5AC",
        "positions": {
            "cL5A012-01": {
                "index": 1
            },
            "cL5A012-02": {
                "index": 2
            },
            "cL5A012-03": {
                "index": 3
            },
            "cL5A012-04": {
                "index": 4
            }
            ,"cL5A012-05": {
                "index": 5
            }

        }
    },
    "cL5A013": {
        "type": "L5AC",
        "positions": {
            "cL5A013-01": {
                "index": 1
            },
            "cL5A013-02": {
                "index": 2
            },
            "cL5A013-03": {
                "index": 3
            },
            "cL5A013-04": {
                "index": 4
            }
            ,"cL5A013-05": {
                "index": 5
            }

        }
    },
    "cL5A014": {
        "type": "L5AC",
        "positions": {
            "cL5A014-01": {
                "index": 1
            },
            "cL5A014-02": {
                "index": 2
            },
            "cL5A014-03": {
                "index": 3
            },
            "cL5A014-04": {
                "index": 4
            }
            ,"cL5A014-05": {
                "index": 5
            }

        }
    },
    "cL5A015": {
        "type": "L5AC",
        "positions": {
            "cL5A015-01": {
                "index": 1
            },
            "cL5A015-02": {
                "index": 2
            },
            "cL5A015-03": {
                "index": 3
            },
            "cL5A015-04": {
                "index": 4
            }
            ,"cL5A015-05": {
                "index": 5
            }

        }
    },
    "cL5A016": {
        "type": "L5AC",
        "positions": {
            "cL5A016-01": {
                "index": 1
            },
            "cL5A016-02": {
                "index": 2
            },
            "cL5A016-03": {
                "index": 3
            },
            "cL5A016-04": {
                "index": 4
            }
            ,"cL5A016-05": {
                "index": 5
            }

        }
    },
    "cAPE001": {
        "type": "APE",
        "positions": {
            "cAPE001-01": {
                "index": 1
            },
            "cAPE001-02": {
                "index": 2
            },
            "cAPE001-03": {
                "index": 3
            },
            "cAPE001-04": {
                "index": 4
            }
            ,"cAPE001-05": {
                "index": 5
            }

        }
    },
    "cAPE002": {
        "type": "APE",
        "positions": {
            "cAPE002-01": {
                "index": 1
            },
            "cAPE002-02": {
                "index": 2
            },
            "cAPE002-03": {
                "index": 3
            },
            "cAPE002-04": {
                "index": 4
            }
            ,"cAPE002-05": {
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
            "c384P001-01": {
                "index": 1
            },
            "c384P001-02": {
                "index": 2
            },
            "c384P001-03": {
                "index": 3
            },
            "c384P001-04": {
                "index": 4
            }
            ,"c384P001-05": {
                "index": 5
            }
        }
    },
    "c384P002": {
        "type": "PCR_L5_384",
        "positions": {
            "c384P002-01": {
                "index": 1
            },
            "c384P002-02": {
                "index": 2
            },
            "c384P002-03": {
                "index": 3
            },
            "c384P002-04": {
                "index": 4
            }
            ,"c384P002-05": {
                "index": 5
            }
        }
    },
    "c384P003": {
        "type": "PCR_L5_384",
        "positions": {
            "c384P003-01": {
                "index": 1
            },
            "c384P003-02": {
                "index": 2
            },
            "c384P003-03": {
                "index": 3
            },
            "c384P003-04": {
                "index": 4
            }
            ,"c384P003-05": {
                "index": 5
            }
        }
    },
    "c384P004": {
        "type": "PCR_L5_384",
        "positions": {
            "c384P004-01": {
                "index": 1
            },
            "c384P004-02": {
                "index": 2
            },
            "c384P004-03": {
                "index": 3
            },
            "c384P004-04": {
                "index": 4
            }
            ,"c384P004-05": {
                "index": 5
            }
        }
    },
    "c96P001": {
        "type": "PCR_L5_96",
        "positions": {
            "c96P001-01": {
                "index": 1
            },
            "c96P001-02": {
                "index": 2
            },
            "c96P001-03": {
                "index": 3
            },
            "c96P001-04": {
                "index": 4
            }
            ,"c96P001-05": {
                "index": 5
            }
        }
    },
    "c96P002": {
        "type": "PCR_L5_96",
        "positions": {
            "c96P002-01": {
                "index": 1
            },
            "c96P002-02": {
                "index": 2
            },
            "c96P002-03": {
                "index": 3
            },
            "c96P002-04": {
                "index": 4
            }
            ,"c96P002-05": {
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
            "cQTRY001-01": {
                "index": 1
            },
            "cQTRY001-02": {
                "index": 2
            },
            "cQTRY001-03": {
                "index": 3
            },
            "cQTRY001-04": {
                "index": 4
            }
        }
    },
    "cQTRY002": {
        "type": "QTRY",
        "positions": {
            "cQTRY002-01": {
                "index": 1
            },
            "cQTRY002-02": {
                "index": 2
            },
            "cQTRY002-03": {
                "index": 3
            },
            "cQTRY002-04": {
                "index": 4
            }
        }
    },
    "cQTRY003": {
        "type": "QTRY",
        "positions": {
            "cQTRY003-01": {
                "index": 1
            },
            "cQTRY003-02": {
                "index": 2
            },
            "cQTRY003-03": {
                "index": 3
            },
            "cQTRY003-04": {
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
            "cHPC001-01": {
                "index": 1
            },
            "cHPC001-02": {
                "index": 2
            },
            "cHPC001-03": {
                "index": 3
            },
            "cHPC001-04": {
                "index": 4
            }
            ,"cHPC001-05": {
                "index": 5
            }
        }
    },
    "cHPC002": {
        "type": "HPC",
        "positions": {
            "cHPC002-01": {
                "index": 1
            },
            "cHPC002-02": {
                "index": 2
            },
            "cHPC002-03": {
                "index": 3
            },
            "cHPC002-04": {
                "index": 4
            }
            ,"cHPC002-05": {
                "index": 5
            }
        }
    },
    "cHPC003": {
        "type": "HPC",
        "positions": {
            "cHPC003-01": {
                "index": 1
            },
            "cHPC003-02": {
                "index": 2
            },
            "cHPC003-03": {
                "index": 3
            },
            "cHPC003-04": {
                "index": 4
            }
            ,"cHPC003-05": {
                "index": 5
            }
        }
    }

}
