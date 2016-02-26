from collections import defaultdict
import datetime
import math
import csv
import random
import string

from app.routes.transform import WebError

from twistdb.sampletrack import Plate
from app.constants import TRANS_TYPE_VECTOR_HITPICK as VECTOR_HITPICK


def pooling_cmds(db, request, source_samples):

    sequencer = None

    basePairMax = 0;
    currentBasePairTotal = 0;
    previousBasePairTotal = 0;
    cmds = []

    details = request.json["details"]

    if "requestedData" in details:
        reqData = details["requestedData"]

    if not reqData or "sequencer" not in reqData or reqData["sequencer"] == "":
        cmds.append({
            "type": "REQUEST_DATA",
            "item": {
                "type": 'radio'
                ,"title": 'Select Sequencer:'
                ,"forProperty": 'sequencer'
                ,"data": [
                    {"option": 'MiSeq'}
                    ,{"option": 'NextSeq'}
                ]
            }
        })

    sources = request.json['sources'];

    sourcesSet = [];

    for sourceIndex, source in enumerate(sources):
        sourcesSet.append({
            "type": "SPTT_0006"
            ,"details" : {
                "id" : source["details"]["id"]
            }
        });

    if "sequencer" in reqData:
        # TO DO  Derive the max BP count for this sequencer
        #        AND
        #        Return total count of basepairs on source plate(s)
        basePairMax = 14000000;

        '''
        currentBasePairTotal = total of BPs in all source plates
        previousBasePairTotal = total BPS on all plates but the last one
        '''

        # DEV ONLY - remove when real basepair counting is done
        previousBasePairTotal = 500;
        #currentBasePairTotal = basePairMax - 3 + len(sources);

        currentBasePairTotal = sum([len(sample.order_item.sequence)
                                   for sample in source_samples
                                   if sample.order_item
                                   and sample.order_item.sequence])
        reponseTally = currentBasePairTotal

        if currentBasePairTotal < basePairMax:
            #and add another source input to indicate there's more room
            sourcesSet.append({
                "type": "SPTT_0006"
            });

        elif basePairMax and currentBasePairTotal == basePairMax:
            cmds.append({
                "type": "PRESENT_DATA",
                "item": {
                    "type": "text",
                    "title": "<strong class=\"twst-warn-text\">Pooling Run FULL</strong>",
                    "data": "No more plates will fit in this run."
                }
            })

        else :
            cmds.append({
                "type": "PRESENT_DATA",
                "item": {
                    "type": "text",
                    "title": "<strong class=\"twst-error-text\">Basepair Limit Overrun</strong>",
                    "data":  ("Return plate <strong>"
                              + request.json['sources'][len(request.json['sources']) - 1]["details"]["id"]
                              + "</strong> to the pooling bin.")
                }
            })

            reponseTally = previousBasePairTotal

            #remove the last added source from the list
            sourcesSet.remove(sourcesSet[len(sourcesSet) - 1])

        cmds.append({
            "type": "PRESENT_DATA",
            "item": {
                "type": "text",
                "title": "Base Pair Tally",
                "data": "<strong>" + str(reponseTally) + "</strong>/" + str(basePairMax) + " so far"
            }
        })

    cmds.append({
        "type": "SET_SOURCES",
        "plates": sourcesSet
    })

    return cmds


def get_source_samples(db, sources):

    from sqlalchemy.orm.exc import NoResultFound

    s_samples = []
    for source in sources:
        if source is None:
            continue
        bc = source["details"]["id"]
        try:
            plate = db.query(Plate).filter(Plate.external_barcode == bc).one()
        except NoResultFound:
            raise NoResultFound("barcode = %s" % bc)
        s_samples.extend(plate.current_well_contents(db))
    return s_samples


def pooling_transform(db, source_samples):

    def random_tube_barcode():
        return 'miseq_tube_' + ''.join([random.choice(string.letters)
                                        for _ in range(8)])

    dest_tube_barcode = random_tube_barcode()
    rows = []

    for s_sample in source_samples:
        plate_size = s_sample.plate.plate_type.layout.feature_count
        rows.append({
            'source_plate_barcode':         s_sample.plate.id,
            'source_well_name':             s_sample.well.well_label,
            'source_well_number':           s_sample.well.well_number,
            'source_sample_id':             s_sample.id,
            'source_plate_well_count':      plate_size,
            'destination_plate_barcode':    dest_tube_barcode,
            'destination_well_name':        'A1',
            'destination_well_number':      1,
            'destination_plate_well_count': 1,
            #'destination_sample_id':        d_sample.id,
            'destination_plate_type':       'SPTT_2048',
        })

    return rows

