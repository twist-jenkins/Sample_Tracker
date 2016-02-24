from collections import defaultdict
import datetime
import math
from twistdb.sampletrack import Plate, Sample, PlateWell, PlateType
from flask import request, Response


def calculate_volume_foreach_sample(db):

    by_marker = defaultdict(list)
    d = {}
    qpix_plates =[]


    dest_type = db.session.query(PlateType).get('SPTT_0006')
    for src_idx, src in enumerate(request.json['sources']):
        plate_barcode = src['details']['id']
        samples = db.session.query(Plate).filter(Plate.external_barcode  == plate_barcode).one().current_well_contents(db.session)

    for sample in samples:
        concentration = sample.conc_ng_ul
        cloning_process= sample.cloning_process.resistance_marker.code
        #sequence = sample.order_item.sequence
        if cloning_process is None :
            marker = "NOMARKER"
        else:
            marker = cloning_process
        by_marker[ marker ].append(sample)

        qpix_plates =[]


        for marker in sorted (by_marker):
            tmp = defaultdict(list)
            for i, sample in enumerate(by_marker[marker]):
                tmp[i // 48].append(sample)
            for plate_no in sorted (tmp):
                qpix_plates.append( (marker,tmp[plate_no]) )



        #print len(qpix_plates), qpix_plates[0] ,qpix_plates[1]
        dest_tmp = defaultdict(lambda: defaultdict(int))
        for i, (marker, samples) in enumerate(qpix_plates):
            dest_tmp[i // 8][ marker ] += len( samples )

        destination_plates = []
        for i, (_, markers) in enumerate(sorted(dest_tmp.items())):
            title = []
            for marker1, d in sorted(markers.items()):

                thisPlate = {"type": "SPTT_0006",
                             "first_in_group": i+1,
                             "details": {
                                 "title": "<strong> %s </strong> resistance - Plate <strong> %s </strong> of %s" %
                                          (str(marker1), (i + 1), d)}}
            '''destination_plates.append( {"type": "SPTT_0006",
                                        "first_in_group": i+1,
                                        "details": {
                                            "title": ', '.join(title)}} )'''


        destination_plates.append(thisPlate)
        print destination_plates

        return destination_plates
