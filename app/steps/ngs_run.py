
from app.routes.transform import WebError


def preview_ngs_load(session, request):
    rows, cmds = [{}], []
    # TO DO   based on source barcode, present the target sequencer

    details = request.json['details']

    # DEV Only remove when code exists to set sequencer
    sequencer = "MiSeq";

    cmds.append({
        "type": "PRESENT_DATA",
        "item": {
            "type": "text",
            "title": "Target Sequencer",
            "data": "<strong>" + sequencer + "</strong>"
        }
    })

    reqData = {
        "sequencerBarcode": None,
        "inputCartridgeBarcode": None,
        "flowCellBarcode": None
    }

    if "requestedData" in details:
        data = details["requestedData"]
        if "sequencerBarcode" in data:
            reqData["sequencerBarcode"] = data["sequencerBarcode"]
        if "inputCartridgeBarcode" in data:
            reqData["inputCartridgeBarcode"] = data["inputCartridgeBarcode"]
        if "flowCellBarcode" in data:
            reqData["flowCellBarcode"] = data["flowCellBarcode"]

    cmds.extend([
        {"type": "REQUEST_DATA",
         "item": {'type': "barcode.INSTRUMENT",
                  "title": "Sequencer Barcode",
                  "forProperty": "sequencerBarcode",
                  # "value": reqData["sequencerBarcode"]
         }},
        {"type": "REQUEST_DATA",
         "item": {
             "type": "barcode.CARTRIDGE",
             "title": "Input Cartridge Barcode",
             "forProperty": "inputCartridgeBarcode",
             # "value": reqData["inputCartridgeBarcode"]
         }},
        {"type": "REQUEST_DATA",
         "item": {
             "type": "barcode.FLOWCELL",
             "title": "Flowcell Barcode",
             "forProperty": "flowCellBarcode",
             # "value": reqData["flowCellBarcode"]
         }}, ])
    return rows, cmds
