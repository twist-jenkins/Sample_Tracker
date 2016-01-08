from twistdb import *
from twistdb.sampletrack import *
from twistdb.public import *
from twistdb.ngs import *
from twistdb.frag import *
import twistdb.ngs
from collections import defaultdict
from app import app, db

from flask import g, make_response, request, Response, session, jsonify
import json
from json_tricks.nonp import loads # json w/ support for comments

import logging
logger = logging.getLogger()


class WebError(Exception):
    """
    not the purest approach, but I'm using this for flow-control, to
    short-circuit bad requests
    """

def merge_transform( sources, dests ):
    assert len(dests) == 1

    dest_barcode = dests[0]['details']['id']
    if db.session.query(SamplePlate) \
                 .filter(SamplePlate.external_barcode == dest_barcode) \
                 .count():
        raise WebError('destinate plate barcode "%s" already exists' % dest_barcode)

    rows, seen = [], set()
    for src in sources:
        barcode = src['details']['id']
        print '@@ merge:', barcode

        try:
            plate = db.session.query(SamplePlate) \
                              .filter(SamplePlate.external_barcode == barcode) \
                              .one()
        except MultipleResultsFound:
            raise WebError('multiple plates found with barcode %s' % barcode)

        for well in db.session.query(SamplePlateLayout) \
                      .filter( SamplePlateLayout.sample_plate == plate ) \
                      .order_by( SamplePlateLayout.well_id ):

            if well.well_id in seen:
                raise WebError('multiple source plates have occupied wells at %s' % plate.type.get_well_name( well.well_id ))
            seen.add( well.well_id )

            rows.append( {'source_plate_barcode':           barcode,
                          'source_well_name':               well.well_name,
                          'source_sample_id':               well.sample_id,
                          'destination_plate_barcode':      dest_barcode,
                          'destination_well_name':          plate.type.get_well_name( well.well_id ),
                          'destination_plate_well_count':   plate.type.number_clusters,
            })
    print rows
    return rows

def filter_transform( transfer_template_id, sources, dests ):
    # current constraints:
    #   1. source plates are 384 well plates full of CS's
    #   2. destination plates are 96 well

    dest_barcodes = [x['details'].get('id','') for x in request.json['destinations']]

    dest_type = db.session.query(SamplePlateType).get('SPTT_0005')  # FIXME: hard-coded to 96 well
    dest_ctr = 1

    if transfer_template_id == 26:
        # frag analyzer
        def filter_wells( barcode ):
            well_scores = defaultdict(lambda: {'well': None, 'scores':set()})
            for plate, orig_well, sample, fa_well in db.session.query( SamplePlate, SamplePlateLayout, Sample, FraganalyzerRunSampleSummaryJoin ) \
                                                               .filter( SamplePlate.external_barcode == barcode ) \
                                                               .join( SamplePlateLayout ) \
                                                               .join( Sample ) \
                                                               .join( FraganalyzerRunSampleSummaryJoin ) \
                                                               .filter( FraganalyzerRunSampleSummaryJoin.measurement_tag == 'post_ecrpcr'):
                    if fa_well.human_classification:
                        [hum] = fa.human_classification
                        score = hum.qc_call
                    else:
                        if fa_well.ok_to_ship():
                            score = 'Pass'
                        elif fa_well.borderline_to_ship():
                            score = 'Warn'
                        else:
                            score = 'Fail'
                    well_scores[ orig_well.well_id ]['well'] = orig_well
                    well_scores[ orig_well.well_id ]['scores'].add( score )

            well_to_passfail = {}
            for well_id, d in well_scores.items():
                if d['scores'] == set(['Warn']):
                    well_to_passfail[ well_id ] = d['well']
            return well_to_passfail

    elif transfer_template_id == 27:
        # NGS pass/fail
        def filter_wells( barcode ):
            well_to_passfail = {}
            for plate, well, cs, nps, summ in db.session.query( SamplePlate, SamplePlateLayout, ClonedSample, NGSPreppedSample, CallerSummary ) \
                                                        .filter( SamplePlate.external_barcode == barcode ) \
                                                        .join( SamplePlateLayout, SamplePlateLayout.sample_plate_id == SamplePlate.sample_plate_id ) \
                                                        .join( ClonedSample, ClonedSample.sample_id == SamplePlateLayout.sample_id ) \
                                                        .join( NGSPreppedSample, NGSPreppedSample.parent_sample_id == SamplePlateLayout.sample_id ) \
                                                        .join( CallerSummary, CallerSummary.sample_id == NGSPreppedSample.sample_id ) \
                                                        .filter( CallerSummary.caller_stage == 'calling'):
                if well.well_id in well_to_passfail:
                    # we only store wells when they pass, so if it's there we don't need to look further
                    continue

                if plate.type_id != 'SPTT_0006':
                    # FIXME: hard-coded for now
                    raise WebError('selected source plates should be plain 384 well plates, while plate %s is %s / "%s"'
                                   % (barcode, plate.type_id, plate.sample_plate_type.name))

                # this is an implicit OR: for a given parent CS plate well, we often have multiple NPS samples
                if json.loads(summ.value)['OK to Ship'] == "Yes":
                    well_to_passfail[ well.well_id ] = well

            return well_to_passfail
    else:
        raise WebError("What transform id is %s??" % transfer_template_id)

    rows = []
    for src in sources:
        barcode = src['details']['id']
        well_to_passfail = filter_wells( barcode )
                                                     
        for well_id in sorted( well_to_passfail ):
            well = well_to_passfail[well_id]
            dest_plate_idx = dest_ctr / 96
            dest_well = dest_ctr % 96
            dest_ctr += 1

            if dest_plate_idx >= len(dest_barcodes):
                raise WebError('we need at least %d destination plates, but only %d were provided'
                               % (dest_plate_idx + 1, len(dest_barcodes)))
            rows.append( {'source_plate_barcode':           barcode,
                          'source_well_name':               well.well_name,
                          'source_sample_id':               well.sample_id,
                          'destination_plate_barcode':      dest_barcodes[dest_plate_idx],
                          'destination_well_name':          dest_type.get_well_name( dest_well ),
                          'destination_plate_well_count':   dest_type.number_clusters
            })
    return rows

def sample_data_determined_transform(transfer_template_id, sources, dests):
    assert transfer_template_id == 25

    dest_type = db.session.query(SamplePlateType).get('SPTT_0006')

    by_marker = defaultdict(list)
    for src in sources:
        barcode = src['details']['id']

        for plate, well, cs in db.session.query( SamplePlate, SamplePlateLayout, ClonedSample ) \
                                                    .filter( SamplePlate.external_barcode == barcode ) \
                                                    .join( SamplePlateLayout, SamplePlateLayout.sample_plate_id == SamplePlate.sample_plate_id ) \
                                                    .join( ClonedSample, ClonedSample.sample_id == SamplePlateLayout.sample_id ):
            try:
                marker = cs.parent_process.vector.resistance_marker
            except:
                marker = None
            by_marker[ marker ].append( well )

    # FIXME: dest_X is undefined and needs work
    marker_group_index = 1

    groups = []

    for marker in sorted( by_marker ):
        new_group = {"id": marker_group_index, "marker_value" : marker, "rows": []}
        for well in by_marker[ marker ]:
            new_group["rows"].append( {
                'source_plate_barcode': barcode,
                'source_well_name': well.well_name,
                'source_sample_id': well.sample_id
            })
        groups.append(new_group);
        marker_group_index += 1

    return groups

def preview():
    assert request.method == 'POST'

    print '@@ template_id:', request.json['transfer_template_id']

    responseCommands = []
    rows = []

    try:
        if str(request.json['transfer_template_id']) not in TRANSFER_MAP:
            raise WebError('Unknown transfer template id: %s' % request.json['transfer_template_id'])

        xfer = TRANSFER_MAP[ str(request.json['transfer_template_id']) ]
        
        if request.json['transfer_template_id'] == 2:
            # identity function
            dest_barcodes = [x['details'].get('id','') for x in request.json['sources']]
        else:
            dest_barcodes = [x['details'].get('id','') for x in request.json['destinations']]

            # FIXME: 26 and 27 demand 0 destination plates
            if request.json['transfer_template_id'] not in (26, 27) \
               and xfer['destination']['plateCount'] != len(set(dest_barcodes)):

                raise WebError('Expected %d distinct destination plate barcodes; got %d'
                               % (xfer['destination']['plateCount'], len(set(dest_barcodes))))
    
        if request.json['transfer_template_id'] == 23:
            # merge source plate(s) into single destination plate
            rows = merge_transform( request.json['sources'], request.json['destinations'] )

        elif request.json['transfer_template_id'] == 25:
            groups = sample_data_determined_transform(request.json['transfer_template_id'], request.json['sources'], request.json['destinations']);

            # to do: create the dest 

            for group in groups:
                logger.info("[[[[[[[[[[[[[[[[[[[[[[[[[ %s" % group["marker_value"]);
                logger.info("+++++++++++++++++++++++++ %s" % len(group["rows"]));

            '''

            rows = {
                "rows": rowsAndGroups.rows
                ,"responseCommands": []
            }

            rows["responseCommands"].append(
                {
                    "type": "SET_DESTINATIONS"
                    ,"plates": [
                        {"type": "SPTT_0006", "details": {"title": "GRP1"}}
                        ,{"type": "SPTT_0006", "details": {"title": "GRP2"}}
                        ,{"type": "SPTT_0006", "details": {"title": "GRP3"}}
                    ]
                }
            );

            '''
        elif request.json['transfer_template_id'] in (26, 27):
            rows = filter_transform( request.json['transfer_template_id'], request.json['sources'], request.json['destinations'] )

        else:
            if request.json['transfer_template_id'] in (1,2):
                src_plate_type = request.json['sources'][0]['details']['plateDetails']['type']
                dest_plate_type = db.session.query(SamplePlateType).get(src_plate_type)

                dest_lookup = lambda src_idx, well_id: (dest_barcodes[src_idx], well_id)

            else:
                if xfer['destination']['plateCount'] != len(set(dest_barcodes)):
                    raise WebError('Expected %d distinct destination plate barcodes; got %d'
                                   % (xfer['destination']['plateCount'], len(set(dest_barcodes))))

                if xfer['source']['plateCount'] != len(request.json['sources']):
                    raise WebError('Expected %d source plates; got %d'
                                   % (xfer['source']['plateCount'], len(request.json['sources'])))

                dest_plate_type = db.session.query(SamplePlateType).get(xfer['destination']['plateTypeId'])

                def dest_lookup( src_idx, well_id ):
                    dest = xfer['plateWellToWellMaps'][ src_idx ][ str(well_id) ]
                    dest_barcode = dest_barcodes[ dest['destination_plate_number'] - 1]
                    dest_well = dest['destination_well_id']
                    return dest_barcode, dest_well

            if not dest_plate_type:
                raise WebError('Unknown destination plate type: '+xfer['destination']['plateTypeId'])

            for src_idx, src in enumerate(request.json['sources']):
                barcode = src['details']['id']
                try:
                    plate = db.session.query(SamplePlate) \
                                      .filter(SamplePlate.external_barcode == barcode) \
                                      .one()
                except MultipleResultsFound:
                    raise WebError('multiple plates found with barcode %s' % barcode)

                for well in db.session.query(SamplePlateLayout) \
                              .filter( SamplePlateLayout.sample_plate == plate ) \
                              .order_by( SamplePlateLayout.well_id ):
                    dest_barcode, dest_well = dest_lookup( src_idx, well.well_id )

                    rows.append( {'source_plate_barcode':           barcode,
                                  'source_well_name':               well.well_name,
                                  'source_sample_id':               well.sample_id,
                                  'destination_plate_barcode':      dest_barcode,
                                  'destination_well_name':          dest_plate_type.get_well_name( dest_well ),
                                  'destination_plate_well_count':   dest_plate_type.number_clusters,
                                  })

    except WebError as e:
        return Response( response=json.dumps({'success': False,
                                              'message': str(e),
                                              'data': None}),
                         status=200,
                         mimetype="application/json")
    else:
        return Response( response=json.dumps({'success': True,
                                              'message': '',
                                              'data': rows,
                                              'responseCommands': responseCommands}),
                         status=200,
                         mimetype="application/json")

def save():
    pass

def execute():
    pass



TRANSFER_MAP = loads("""
{
                "1": {  // keyed to sample_transfer_template_id in the database
                    "description": "Source and destination have SAME LAYOUT"
                    ,"type": "same-same"
                    ,"source": {
                        "plateCount": 1
                        ,"variablePlateCount": false
                    }
                    ,"destination": {
                        "plateCount": 1
                        ,"variablePlateCount": false
                    }
                }
                ,"2": {  // keyed to sample_transfer_template_id in the database
                    "description": "Source and destination plate are SAME PLATE"
                    ,"type": "same-same"
                    ,"source": {
                        "plateCount": 1
                        ,"variablePlateCount": false
                    }
                    ,"destination": {
                        "plateCount": 0
                        ,"variablePlateCount": false
                    }
                }
                ,"13": {  // keyed to sample_transfer_template_id in the database
                    "description": "384 to 4x96"
                    ,"type": "standard"
                    ,"source": {
                        "plateCount": 1
                        ,"wellCount": 384
                        ,"plateTypeId": "SPTT_0006"
                        ,"variablePlateCount": false
                    }
                    ,"destination":{
                        "plateCount": 4
                        ,"wellCount": 96
                        ,"plateTypeId": "SPTT_0005"
                        ,"variablePlateCount": false
                        ,"plateTitles": ["Quadrant&nbsp;1:&nbsp;","Quadrant&nbsp;2:&nbsp;","Quadrant&nbsp;3:&nbsp;","Quadrant&nbsp;4:&nbsp;"]
                    }
                    ,"plateWellToWellMaps": [ // index in plate_well_to_well_map array = source_plate_index
                        {   // key= sopurce plate well id
                            "1": {"destination_plate_number": 1, "destination_well_id": 1}
                            ,"2": {"destination_plate_number": 2, "destination_well_id": 1}
                            ,"3": {"destination_plate_number": 1, "destination_well_id": 2}
                            ,"4": {"destination_plate_number": 2, "destination_well_id": 2}
                            ,"5": {"destination_plate_number": 1, "destination_well_id": 3}
                            ,"6": {"destination_plate_number": 2, "destination_well_id": 3}
                            ,"7": {"destination_plate_number": 1, "destination_well_id": 4}
                            ,"8": {"destination_plate_number": 2, "destination_well_id": 4}
                            ,"9": {"destination_plate_number": 1, "destination_well_id": 5}
                            ,"10": {"destination_plate_number": 2, "destination_well_id": 5}
                            ,"11": {"destination_plate_number": 1, "destination_well_id": 6}
                            ,"12": {"destination_plate_number": 2, "destination_well_id": 6}
                            ,"13": {"destination_plate_number": 1, "destination_well_id": 7}
                            ,"14": {"destination_plate_number": 2, "destination_well_id": 7}
                            ,"15": {"destination_plate_number": 1, "destination_well_id": 8}
                            ,"16": {"destination_plate_number": 2, "destination_well_id": 8}
                            ,"17": {"destination_plate_number": 1, "destination_well_id": 9}
                            ,"18": {"destination_plate_number": 2, "destination_well_id": 9}
                            ,"19": {"destination_plate_number": 1, "destination_well_id": 10}
                            ,"20": {"destination_plate_number": 2, "destination_well_id": 10}
                            ,"21": {"destination_plate_number": 1, "destination_well_id": 11}
                            ,"22": {"destination_plate_number": 2, "destination_well_id": 11}
                            ,"23": {"destination_plate_number": 1, "destination_well_id": 12}
                            ,"24": {"destination_plate_number": 2, "destination_well_id": 12}
                            ,"25": {"destination_plate_number": 3, "destination_well_id": 1}
                            ,"26": {"destination_plate_number": 4, "destination_well_id": 1}
                            ,"27": {"destination_plate_number": 3, "destination_well_id": 2}
                            ,"28": {"destination_plate_number": 4, "destination_well_id": 2}
                            ,"29": {"destination_plate_number": 3, "destination_well_id": 3}
                            ,"30": {"destination_plate_number": 4, "destination_well_id": 3}
                            ,"31": {"destination_plate_number": 3, "destination_well_id": 4}
                            ,"32": {"destination_plate_number": 4, "destination_well_id": 4}
                            ,"33": {"destination_plate_number": 3, "destination_well_id": 5}
                            ,"34": {"destination_plate_number": 4, "destination_well_id": 5}
                            ,"35": {"destination_plate_number": 3, "destination_well_id": 6}
                            ,"36": {"destination_plate_number": 4, "destination_well_id": 6}
                            ,"37": {"destination_plate_number": 3, "destination_well_id": 7}
                            ,"38": {"destination_plate_number": 4, "destination_well_id": 7}
                            ,"39": {"destination_plate_number": 3, "destination_well_id": 8}
                            ,"40": {"destination_plate_number": 4, "destination_well_id": 8}
                            ,"41": {"destination_plate_number": 3, "destination_well_id": 9}
                            ,"42": {"destination_plate_number": 4, "destination_well_id": 9}
                            ,"43": {"destination_plate_number": 3, "destination_well_id": 10}
                            ,"44": {"destination_plate_number": 4, "destination_well_id": 10}
                            ,"45": {"destination_plate_number": 3, "destination_well_id": 11}
                            ,"46": {"destination_plate_number": 4, "destination_well_id": 11}
                            ,"47": {"destination_plate_number": 3, "destination_well_id": 12}
                            ,"48": {"destination_plate_number": 4, "destination_well_id": 12}
                            ,"49": {"destination_plate_number": 1, "destination_well_id": 13}
                            ,"50": {"destination_plate_number": 2, "destination_well_id": 13}
                            ,"51": {"destination_plate_number": 1, "destination_well_id": 14}
                            ,"52": {"destination_plate_number": 2, "destination_well_id": 14}
                            ,"53": {"destination_plate_number": 1, "destination_well_id": 15}
                            ,"54": {"destination_plate_number": 2, "destination_well_id": 15}
                            ,"55": {"destination_plate_number": 1, "destination_well_id": 16}
                            ,"56": {"destination_plate_number": 2, "destination_well_id": 16}
                            ,"57": {"destination_plate_number": 1, "destination_well_id": 17}
                            ,"58": {"destination_plate_number": 2, "destination_well_id": 17}
                            ,"59": {"destination_plate_number": 1, "destination_well_id": 18}
                            ,"60": {"destination_plate_number": 2, "destination_well_id": 18}
                            ,"61": {"destination_plate_number": 1, "destination_well_id": 19}
                            ,"62": {"destination_plate_number": 2, "destination_well_id": 19}
                            ,"63": {"destination_plate_number": 1, "destination_well_id": 20}
                            ,"64": {"destination_plate_number": 2, "destination_well_id": 20}
                            ,"65": {"destination_plate_number": 1, "destination_well_id": 21}
                            ,"66": {"destination_plate_number": 2, "destination_well_id": 21}
                            ,"67": {"destination_plate_number": 1, "destination_well_id": 22}
                            ,"68": {"destination_plate_number": 2, "destination_well_id": 22}
                            ,"69": {"destination_plate_number": 1, "destination_well_id": 23}
                            ,"70": {"destination_plate_number": 2, "destination_well_id": 23}
                            ,"71": {"destination_plate_number": 1, "destination_well_id": 24}
                            ,"72": {"destination_plate_number": 2, "destination_well_id": 24}
                            ,"73": {"destination_plate_number": 3, "destination_well_id": 13}
                            ,"74": {"destination_plate_number": 4, "destination_well_id": 13}
                            ,"75": {"destination_plate_number": 3, "destination_well_id": 14}
                            ,"76": {"destination_plate_number": 4, "destination_well_id": 14}
                            ,"77": {"destination_plate_number": 3, "destination_well_id": 15}
                            ,"78": {"destination_plate_number": 4, "destination_well_id": 15}
                            ,"79": {"destination_plate_number": 3, "destination_well_id": 16}
                            ,"80": {"destination_plate_number": 4, "destination_well_id": 16}
                            ,"81": {"destination_plate_number": 3, "destination_well_id": 17}
                            ,"82": {"destination_plate_number": 4, "destination_well_id": 17}
                            ,"83": {"destination_plate_number": 3, "destination_well_id": 18}
                            ,"84": {"destination_plate_number": 4, "destination_well_id": 18}
                            ,"85": {"destination_plate_number": 3, "destination_well_id": 19}
                            ,"86": {"destination_plate_number": 4, "destination_well_id": 19}
                            ,"87": {"destination_plate_number": 3, "destination_well_id": 20}
                            ,"88": {"destination_plate_number": 4, "destination_well_id": 20}
                            ,"89": {"destination_plate_number": 3, "destination_well_id": 21}
                            ,"90": {"destination_plate_number": 4, "destination_well_id": 21}
                            ,"91": {"destination_plate_number": 3, "destination_well_id": 22}
                            ,"92": {"destination_plate_number": 4, "destination_well_id": 22}
                            ,"93": {"destination_plate_number": 3, "destination_well_id": 23}
                            ,"94": {"destination_plate_number": 4, "destination_well_id": 23}
                            ,"95": {"destination_plate_number": 3, "destination_well_id": 24}
                            ,"96": {"destination_plate_number": 4, "destination_well_id": 24}
                            ,"97": {"destination_plate_number": 1, "destination_well_id": 25}
                            ,"98": {"destination_plate_number": 2, "destination_well_id": 25}
                            ,"99": {"destination_plate_number": 1, "destination_well_id": 26}
                            ,"100": {"destination_plate_number": 2, "destination_well_id": 26}
                            ,"101": {"destination_plate_number": 1, "destination_well_id": 27}
                            ,"102": {"destination_plate_number": 2, "destination_well_id": 27}
                            ,"103": {"destination_plate_number": 1, "destination_well_id": 28}
                            ,"104": {"destination_plate_number": 2, "destination_well_id": 28}
                            ,"105": {"destination_plate_number": 1, "destination_well_id": 29}
                            ,"106": {"destination_plate_number": 2, "destination_well_id": 29}
                            ,"107": {"destination_plate_number": 1, "destination_well_id": 30}
                            ,"108": {"destination_plate_number": 2, "destination_well_id": 30}
                            ,"109": {"destination_plate_number": 1, "destination_well_id": 31}
                            ,"110": {"destination_plate_number": 2, "destination_well_id": 31}
                            ,"111": {"destination_plate_number": 1, "destination_well_id": 32}
                            ,"112": {"destination_plate_number": 2, "destination_well_id": 32}
                            ,"113": {"destination_plate_number": 1, "destination_well_id": 33}
                            ,"114": {"destination_plate_number": 2, "destination_well_id": 33}
                            ,"115": {"destination_plate_number": 1, "destination_well_id": 34}
                            ,"116": {"destination_plate_number": 2, "destination_well_id": 34}
                            ,"117": {"destination_plate_number": 1, "destination_well_id": 35}
                            ,"118": {"destination_plate_number": 2, "destination_well_id": 35}
                            ,"119": {"destination_plate_number": 1, "destination_well_id": 36}
                            ,"120": {"destination_plate_number": 2, "destination_well_id": 36}
                            ,"121": {"destination_plate_number": 3, "destination_well_id": 25}
                            ,"122": {"destination_plate_number": 4, "destination_well_id": 25}
                            ,"123": {"destination_plate_number": 3, "destination_well_id": 26}
                            ,"124": {"destination_plate_number": 4, "destination_well_id": 26}
                            ,"125": {"destination_plate_number": 3, "destination_well_id": 27}
                            ,"126": {"destination_plate_number": 4, "destination_well_id": 27}
                            ,"127": {"destination_plate_number": 3, "destination_well_id": 28}
                            ,"128": {"destination_plate_number": 4, "destination_well_id": 28}
                            ,"129": {"destination_plate_number": 3, "destination_well_id": 29}
                            ,"130": {"destination_plate_number": 4, "destination_well_id": 29}
                            ,"131": {"destination_plate_number": 3, "destination_well_id": 30}
                            ,"132": {"destination_plate_number": 4, "destination_well_id": 30}
                            ,"133": {"destination_plate_number": 3, "destination_well_id": 31}
                            ,"134": {"destination_plate_number": 4, "destination_well_id": 31}
                            ,"135": {"destination_plate_number": 3, "destination_well_id": 32}
                            ,"136": {"destination_plate_number": 4, "destination_well_id": 32}
                            ,"137": {"destination_plate_number": 3, "destination_well_id": 33}
                            ,"138": {"destination_plate_number": 4, "destination_well_id": 33}
                            ,"139": {"destination_plate_number": 3, "destination_well_id": 34}
                            ,"140": {"destination_plate_number": 4, "destination_well_id": 34}
                            ,"141": {"destination_plate_number": 3, "destination_well_id": 35}
                            ,"142": {"destination_plate_number": 4, "destination_well_id": 35}
                            ,"143": {"destination_plate_number": 3, "destination_well_id": 36}
                            ,"144": {"destination_plate_number": 4, "destination_well_id": 36}
                            ,"145": {"destination_plate_number": 1, "destination_well_id": 37}
                            ,"146": {"destination_plate_number": 2, "destination_well_id": 37}
                            ,"147": {"destination_plate_number": 1, "destination_well_id": 38}
                            ,"148": {"destination_plate_number": 2, "destination_well_id": 38}
                            ,"149": {"destination_plate_number": 1, "destination_well_id": 39}
                            ,"150": {"destination_plate_number": 2, "destination_well_id": 39}
                            ,"151": {"destination_plate_number": 1, "destination_well_id": 40}
                            ,"152": {"destination_plate_number": 2, "destination_well_id": 40}
                            ,"153": {"destination_plate_number": 1, "destination_well_id": 41}
                            ,"154": {"destination_plate_number": 2, "destination_well_id": 41}
                            ,"155": {"destination_plate_number": 1, "destination_well_id": 42}
                            ,"156": {"destination_plate_number": 2, "destination_well_id": 42}
                            ,"157": {"destination_plate_number": 1, "destination_well_id": 43}
                            ,"158": {"destination_plate_number": 2, "destination_well_id": 43}
                            ,"159": {"destination_plate_number": 1, "destination_well_id": 44}
                            ,"160": {"destination_plate_number": 2, "destination_well_id": 44}
                            ,"161": {"destination_plate_number": 1, "destination_well_id": 45}
                            ,"162": {"destination_plate_number": 2, "destination_well_id": 45}
                            ,"163": {"destination_plate_number": 1, "destination_well_id": 46}
                            ,"164": {"destination_plate_number": 2, "destination_well_id": 46}
                            ,"165": {"destination_plate_number": 1, "destination_well_id": 47}
                            ,"166": {"destination_plate_number": 2, "destination_well_id": 47}
                            ,"167": {"destination_plate_number": 1, "destination_well_id": 48}
                            ,"168": {"destination_plate_number": 2, "destination_well_id": 48}
                            ,"169": {"destination_plate_number": 3, "destination_well_id": 37}
                            ,"170": {"destination_plate_number": 4, "destination_well_id": 37}
                            ,"171": {"destination_plate_number": 3, "destination_well_id": 38}
                            ,"172": {"destination_plate_number": 4, "destination_well_id": 38}
                            ,"173": {"destination_plate_number": 3, "destination_well_id": 39}
                            ,"174": {"destination_plate_number": 4, "destination_well_id": 39}
                            ,"175": {"destination_plate_number": 3, "destination_well_id": 40}
                            ,"176": {"destination_plate_number": 4, "destination_well_id": 40}
                            ,"177": {"destination_plate_number": 3, "destination_well_id": 41}
                            ,"178": {"destination_plate_number": 4, "destination_well_id": 41}
                            ,"179": {"destination_plate_number": 3, "destination_well_id": 42}
                            ,"180": {"destination_plate_number": 4, "destination_well_id": 42}
                            ,"181": {"destination_plate_number": 3, "destination_well_id": 43}
                            ,"182": {"destination_plate_number": 4, "destination_well_id": 43}
                            ,"183": {"destination_plate_number": 3, "destination_well_id": 44}
                            ,"184": {"destination_plate_number": 4, "destination_well_id": 44}
                            ,"185": {"destination_plate_number": 3, "destination_well_id": 45}
                            ,"186": {"destination_plate_number": 4, "destination_well_id": 45}
                            ,"187": {"destination_plate_number": 3, "destination_well_id": 46}
                            ,"188": {"destination_plate_number": 4, "destination_well_id": 46}
                            ,"189": {"destination_plate_number": 3, "destination_well_id": 47}
                            ,"190": {"destination_plate_number": 4, "destination_well_id": 47}
                            ,"191": {"destination_plate_number": 3, "destination_well_id": 48}
                            ,"192": {"destination_plate_number": 4, "destination_well_id": 48}
                            ,"193": {"destination_plate_number": 1, "destination_well_id": 49}
                            ,"194": {"destination_plate_number": 2, "destination_well_id": 49}
                            ,"195": {"destination_plate_number": 1, "destination_well_id": 50}
                            ,"196": {"destination_plate_number": 2, "destination_well_id": 50}
                            ,"197": {"destination_plate_number": 1, "destination_well_id": 51}
                            ,"198": {"destination_plate_number": 2, "destination_well_id": 51}
                            ,"199": {"destination_plate_number": 1, "destination_well_id": 52}
                            ,"200": {"destination_plate_number": 2, "destination_well_id": 52}
                            ,"201": {"destination_plate_number": 1, "destination_well_id": 53}
                            ,"202": {"destination_plate_number": 2, "destination_well_id": 53}
                            ,"203": {"destination_plate_number": 1, "destination_well_id": 54}
                            ,"204": {"destination_plate_number": 2, "destination_well_id": 54}
                            ,"205": {"destination_plate_number": 1, "destination_well_id": 55}
                            ,"206": {"destination_plate_number": 2, "destination_well_id": 55}
                            ,"207": {"destination_plate_number": 1, "destination_well_id": 56}
                            ,"208": {"destination_plate_number": 2, "destination_well_id": 56}
                            ,"209": {"destination_plate_number": 1, "destination_well_id": 57}
                            ,"210": {"destination_plate_number": 2, "destination_well_id": 57}
                            ,"211": {"destination_plate_number": 1, "destination_well_id": 58}
                            ,"212": {"destination_plate_number": 2, "destination_well_id": 58}
                            ,"213": {"destination_plate_number": 1, "destination_well_id": 59}
                            ,"214": {"destination_plate_number": 2, "destination_well_id": 59}
                            ,"215": {"destination_plate_number": 1, "destination_well_id": 60}
                            ,"216": {"destination_plate_number": 2, "destination_well_id": 60}
                            ,"217": {"destination_plate_number": 3, "destination_well_id": 49}
                            ,"218": {"destination_plate_number": 4, "destination_well_id": 49}
                            ,"219": {"destination_plate_number": 3, "destination_well_id": 50}
                            ,"220": {"destination_plate_number": 4, "destination_well_id": 50}
                            ,"221": {"destination_plate_number": 3, "destination_well_id": 51}
                            ,"222": {"destination_plate_number": 4, "destination_well_id": 51}
                            ,"223": {"destination_plate_number": 3, "destination_well_id": 52}
                            ,"224": {"destination_plate_number": 4, "destination_well_id": 52}
                            ,"225": {"destination_plate_number": 3, "destination_well_id": 53}
                            ,"226": {"destination_plate_number": 4, "destination_well_id": 53}
                            ,"227": {"destination_plate_number": 3, "destination_well_id": 54}
                            ,"228": {"destination_plate_number": 4, "destination_well_id": 54}
                            ,"229": {"destination_plate_number": 3, "destination_well_id": 55}
                            ,"230": {"destination_plate_number": 4, "destination_well_id": 55}
                            ,"231": {"destination_plate_number": 3, "destination_well_id": 56}
                            ,"232": {"destination_plate_number": 4, "destination_well_id": 56}
                            ,"233": {"destination_plate_number": 3, "destination_well_id": 57}
                            ,"234": {"destination_plate_number": 4, "destination_well_id": 57}
                            ,"235": {"destination_plate_number": 3, "destination_well_id": 58}
                            ,"236": {"destination_plate_number": 4, "destination_well_id": 58}
                            ,"237": {"destination_plate_number": 3, "destination_well_id": 59}
                            ,"238": {"destination_plate_number": 4, "destination_well_id": 59}
                            ,"239": {"destination_plate_number": 3, "destination_well_id": 60}
                            ,"240": {"destination_plate_number": 4, "destination_well_id": 60}
                            ,"241": {"destination_plate_number": 1, "destination_well_id": 61}
                            ,"242": {"destination_plate_number": 2, "destination_well_id": 61}
                            ,"243": {"destination_plate_number": 1, "destination_well_id": 62}
                            ,"244": {"destination_plate_number": 2, "destination_well_id": 62}
                            ,"245": {"destination_plate_number": 1, "destination_well_id": 63}
                            ,"246": {"destination_plate_number": 2, "destination_well_id": 63}
                            ,"247": {"destination_plate_number": 1, "destination_well_id": 64}
                            ,"248": {"destination_plate_number": 2, "destination_well_id": 64}
                            ,"249": {"destination_plate_number": 1, "destination_well_id": 65}
                            ,"250": {"destination_plate_number": 2, "destination_well_id": 65}
                            ,"251": {"destination_plate_number": 1, "destination_well_id": 66}
                            ,"252": {"destination_plate_number": 2, "destination_well_id": 66}
                            ,"253": {"destination_plate_number": 1, "destination_well_id": 67}
                            ,"254": {"destination_plate_number": 2, "destination_well_id": 67}
                            ,"255": {"destination_plate_number": 1, "destination_well_id": 68}
                            ,"256": {"destination_plate_number": 2, "destination_well_id": 68}
                            ,"257": {"destination_plate_number": 1, "destination_well_id": 69}
                            ,"258": {"destination_plate_number": 2, "destination_well_id": 69}
                            ,"259": {"destination_plate_number": 1, "destination_well_id": 70}
                            ,"260": {"destination_plate_number": 2, "destination_well_id": 70}
                            ,"261": {"destination_plate_number": 1, "destination_well_id": 71}
                            ,"262": {"destination_plate_number": 2, "destination_well_id": 71}
                            ,"263": {"destination_plate_number": 1, "destination_well_id": 72}
                            ,"264": {"destination_plate_number": 2, "destination_well_id": 72}
                            ,"265": {"destination_plate_number": 3, "destination_well_id": 61}
                            ,"266": {"destination_plate_number": 4, "destination_well_id": 61}
                            ,"267": {"destination_plate_number": 3, "destination_well_id": 62}
                            ,"268": {"destination_plate_number": 4, "destination_well_id": 62}
                            ,"269": {"destination_plate_number": 3, "destination_well_id": 63}
                            ,"270": {"destination_plate_number": 4, "destination_well_id": 63}
                            ,"271": {"destination_plate_number": 3, "destination_well_id": 64}
                            ,"272": {"destination_plate_number": 4, "destination_well_id": 64}
                            ,"273": {"destination_plate_number": 3, "destination_well_id": 65}
                            ,"274": {"destination_plate_number": 4, "destination_well_id": 65}
                            ,"275": {"destination_plate_number": 3, "destination_well_id": 66}
                            ,"276": {"destination_plate_number": 4, "destination_well_id": 66}
                            ,"277": {"destination_plate_number": 3, "destination_well_id": 67}
                            ,"278": {"destination_plate_number": 4, "destination_well_id": 67}
                            ,"279": {"destination_plate_number": 3, "destination_well_id": 68}
                            ,"280": {"destination_plate_number": 4, "destination_well_id": 68}
                            ,"281": {"destination_plate_number": 3, "destination_well_id": 69}
                            ,"282": {"destination_plate_number": 4, "destination_well_id": 69}
                            ,"283": {"destination_plate_number": 3, "destination_well_id": 70}
                            ,"284": {"destination_plate_number": 4, "destination_well_id": 70}
                            ,"285": {"destination_plate_number": 3, "destination_well_id": 71}
                            ,"286": {"destination_plate_number": 4, "destination_well_id": 71}
                            ,"287": {"destination_plate_number": 3, "destination_well_id": 72}
                            ,"288": {"destination_plate_number": 4, "destination_well_id": 72}
                            ,"289": {"destination_plate_number": 1, "destination_well_id": 73}
                            ,"290": {"destination_plate_number": 2, "destination_well_id": 73}
                            ,"291": {"destination_plate_number": 1, "destination_well_id": 74}
                            ,"292": {"destination_plate_number": 2, "destination_well_id": 74}
                            ,"293": {"destination_plate_number": 1, "destination_well_id": 75}
                            ,"294": {"destination_plate_number": 2, "destination_well_id": 75}
                            ,"295": {"destination_plate_number": 1, "destination_well_id": 76}
                            ,"296": {"destination_plate_number": 2, "destination_well_id": 76}
                            ,"297": {"destination_plate_number": 1, "destination_well_id": 77}
                            ,"298": {"destination_plate_number": 2, "destination_well_id": 77}
                            ,"299": {"destination_plate_number": 1, "destination_well_id": 78}
                            ,"300": {"destination_plate_number": 2, "destination_well_id": 78}
                            ,"301": {"destination_plate_number": 1, "destination_well_id": 79}
                            ,"302": {"destination_plate_number": 2, "destination_well_id": 79}
                            ,"303": {"destination_plate_number": 1, "destination_well_id": 80}
                            ,"304": {"destination_plate_number": 2, "destination_well_id": 80}
                            ,"305": {"destination_plate_number": 1, "destination_well_id": 81}
                            ,"306": {"destination_plate_number": 2, "destination_well_id": 81}
                            ,"307": {"destination_plate_number": 1, "destination_well_id": 82}
                            ,"308": {"destination_plate_number": 2, "destination_well_id": 82}
                            ,"309": {"destination_plate_number": 1, "destination_well_id": 83}
                            ,"310": {"destination_plate_number": 2, "destination_well_id": 83}
                            ,"311": {"destination_plate_number": 1, "destination_well_id": 84}
                            ,"312": {"destination_plate_number": 2, "destination_well_id": 84}
                            ,"313": {"destination_plate_number": 3, "destination_well_id": 73}
                            ,"314": {"destination_plate_number": 4, "destination_well_id": 73}
                            ,"315": {"destination_plate_number": 3, "destination_well_id": 74}
                            ,"316": {"destination_plate_number": 4, "destination_well_id": 74}
                            ,"317": {"destination_plate_number": 3, "destination_well_id": 75}
                            ,"318": {"destination_plate_number": 4, "destination_well_id": 75}
                            ,"319": {"destination_plate_number": 3, "destination_well_id": 76}
                            ,"320": {"destination_plate_number": 4, "destination_well_id": 76}
                            ,"321": {"destination_plate_number": 3, "destination_well_id": 77}
                            ,"322": {"destination_plate_number": 4, "destination_well_id": 77}
                            ,"323": {"destination_plate_number": 3, "destination_well_id": 78}
                            ,"324": {"destination_plate_number": 4, "destination_well_id": 78}
                            ,"325": {"destination_plate_number": 3, "destination_well_id": 79}
                            ,"326": {"destination_plate_number": 4, "destination_well_id": 79}
                            ,"327": {"destination_plate_number": 3, "destination_well_id": 80}
                            ,"328": {"destination_plate_number": 4, "destination_well_id": 80}
                            ,"329": {"destination_plate_number": 3, "destination_well_id": 81}
                            ,"330": {"destination_plate_number": 4, "destination_well_id": 81}
                            ,"331": {"destination_plate_number": 3, "destination_well_id": 82}
                            ,"332": {"destination_plate_number": 4, "destination_well_id": 82}
                            ,"333": {"destination_plate_number": 3, "destination_well_id": 83}
                            ,"334": {"destination_plate_number": 4, "destination_well_id": 83}
                            ,"335": {"destination_plate_number": 3, "destination_well_id": 84}
                            ,"336": {"destination_plate_number": 4, "destination_well_id": 84}
                            ,"337": {"destination_plate_number": 1, "destination_well_id": 85}
                            ,"338": {"destination_plate_number": 2, "destination_well_id": 85}
                            ,"339": {"destination_plate_number": 1, "destination_well_id": 86}
                            ,"340": {"destination_plate_number": 2, "destination_well_id": 86}
                            ,"341": {"destination_plate_number": 1, "destination_well_id": 87}
                            ,"342": {"destination_plate_number": 2, "destination_well_id": 87}
                            ,"343": {"destination_plate_number": 1, "destination_well_id": 88}
                            ,"344": {"destination_plate_number": 2, "destination_well_id": 88}
                            ,"345": {"destination_plate_number": 1, "destination_well_id": 89}
                            ,"346": {"destination_plate_number": 2, "destination_well_id": 89}
                            ,"347": {"destination_plate_number": 1, "destination_well_id": 90}
                            ,"348": {"destination_plate_number": 2, "destination_well_id": 90}
                            ,"349": {"destination_plate_number": 1, "destination_well_id": 91}
                            ,"350": {"destination_plate_number": 2, "destination_well_id": 91}
                            ,"351": {"destination_plate_number": 1, "destination_well_id": 92}
                            ,"352": {"destination_plate_number": 2, "destination_well_id": 92}
                            ,"353": {"destination_plate_number": 1, "destination_well_id": 93}
                            ,"354": {"destination_plate_number": 2, "destination_well_id": 93}
                            ,"355": {"destination_plate_number": 1, "destination_well_id": 94}
                            ,"356": {"destination_plate_number": 2, "destination_well_id": 94}
                            ,"357": {"destination_plate_number": 1, "destination_well_id": 95}
                            ,"358": {"destination_plate_number": 2, "destination_well_id": 95}
                            ,"359": {"destination_plate_number": 1, "destination_well_id": 96}
                            ,"360": {"destination_plate_number": 2, "destination_well_id": 96}
                            ,"361": {"destination_plate_number": 3, "destination_well_id": 85}
                            ,"362": {"destination_plate_number": 4, "destination_well_id": 85}
                            ,"363": {"destination_plate_number": 3, "destination_well_id": 86}
                            ,"364": {"destination_plate_number": 4, "destination_well_id": 86}
                            ,"365": {"destination_plate_number": 3, "destination_well_id": 87}
                            ,"366": {"destination_plate_number": 4, "destination_well_id": 87}
                            ,"367": {"destination_plate_number": 3, "destination_well_id": 88}
                            ,"368": {"destination_plate_number": 4, "destination_well_id": 88}
                            ,"369": {"destination_plate_number": 3, "destination_well_id": 89}
                            ,"370": {"destination_plate_number": 4, "destination_well_id": 89}
                            ,"371": {"destination_plate_number": 3, "destination_well_id": 90}
                            ,"372": {"destination_plate_number": 4, "destination_well_id": 90}
                            ,"373": {"destination_plate_number": 3, "destination_well_id": 91}
                            ,"374": {"destination_plate_number": 4, "destination_well_id": 91}
                            ,"375": {"destination_plate_number": 3, "destination_well_id": 92}
                            ,"376": {"destination_plate_number": 4, "destination_well_id": 92}
                            ,"377": {"destination_plate_number": 3, "destination_well_id": 93}
                            ,"378": {"destination_plate_number": 4, "destination_well_id": 93}
                            ,"379": {"destination_plate_number": 3, "destination_well_id": 94}
                            ,"380": {"destination_plate_number": 4, "destination_well_id": 94}
                            ,"381": {"destination_plate_number": 3, "destination_well_id": 95}
                            ,"382": {"destination_plate_number": 4, "destination_well_id": 95}
                            ,"383": {"destination_plate_number": 3, "destination_well_id": 96}
                            ,"384": {"destination_plate_number": 4, "destination_well_id": 96}
                        }
                    ]
                }
                ,"14": {  // keyed to sample_transfer_template_id in the database
                    "description": "96 to 2x48"
                    ,"type": "standard"
                    ,"source": {
                        "plateCount": 1
                        ,"wellCount": 96
                        ,"plateTypeId": "SPTT_0005"
                        ,"variablePlateCount": false
                    }
                    ,"destination":{
                        "plateCount": 2
                        ,"wellCount": 48
                        ,"plateTypeId": "SPTT_0004"
                        ,"variablePlateCount": false
                        ,"plateTitles": ["Left:&nbsp;&nbsp;","Right:&nbsp;"]
                    }
                    ,"plateWellToWellMaps": [ // array of source plates
                        {   // index in plate_well_to_well_map array = source_plate_index
                            "1": {"destination_plate_number": 1 ,"destination_well_id": 1}
                            ,"2": {"destination_plate_number": 1 ,"destination_well_id": 2}
                            ,"3": {"destination_plate_number": 1 ,"destination_well_id": 3}
                            ,"4": {"destination_plate_number": 1 ,"destination_well_id": 4}
                            ,"5": {"destination_plate_number": 1 ,"destination_well_id": 5}
                            ,"6": {"destination_plate_number": 1 ,"destination_well_id": 6}
                            ,"7": {"destination_plate_number": 2 ,"destination_well_id": 1}
                            ,"8": {"destination_plate_number": 2 ,"destination_well_id": 2}
                            ,"9": {"destination_plate_number": 2 ,"destination_well_id": 3}
                            ,"10": {"destination_plate_number": 2 ,"destination_well_id": 4}
                            ,"11": {"destination_plate_number": 2 ,"destination_well_id": 5}
                            ,"12": {"destination_plate_number": 2 ,"destination_well_id": 6}
                            ,"13": {"destination_plate_number": 1 ,"destination_well_id": 7}
                            ,"14": {"destination_plate_number": 1 ,"destination_well_id": 8}
                            ,"15": {"destination_plate_number": 1 ,"destination_well_id": 9}
                            ,"16": {"destination_plate_number": 1 ,"destination_well_id": 10}
                            ,"17": {"destination_plate_number": 1 ,"destination_well_id": 11}
                            ,"18": {"destination_plate_number": 1 ,"destination_well_id": 12}
                            ,"19": {"destination_plate_number": 2 ,"destination_well_id": 7}
                            ,"20": {"destination_plate_number": 2 ,"destination_well_id": 8}
                            ,"21": {"destination_plate_number": 2 ,"destination_well_id": 9}
                            ,"22": {"destination_plate_number": 2 ,"destination_well_id": 10}
                            ,"23": {"destination_plate_number": 2 ,"destination_well_id": 11}
                            ,"24": {"destination_plate_number": 2 ,"destination_well_id": 12}
                            ,"25": {"destination_plate_number": 1 ,"destination_well_id": 13}
                            ,"26": {"destination_plate_number": 1 ,"destination_well_id": 14}
                            ,"27": {"destination_plate_number": 1 ,"destination_well_id": 15}
                            ,"28": {"destination_plate_number": 1 ,"destination_well_id": 16}
                            ,"29": {"destination_plate_number": 1 ,"destination_well_id": 17}
                            ,"30": {"destination_plate_number": 1 ,"destination_well_id": 18}
                            ,"31": {"destination_plate_number": 2 ,"destination_well_id": 13}
                            ,"32": {"destination_plate_number": 2 ,"destination_well_id": 14}
                            ,"33": {"destination_plate_number": 2 ,"destination_well_id": 15}
                            ,"34": {"destination_plate_number": 2 ,"destination_well_id": 16}
                            ,"35": {"destination_plate_number": 2 ,"destination_well_id": 17}
                            ,"36": {"destination_plate_number": 2 ,"destination_well_id": 18}
                            ,"37": {"destination_plate_number": 1 ,"destination_well_id": 19}
                            ,"38": {"destination_plate_number": 1 ,"destination_well_id": 20}
                            ,"39": {"destination_plate_number": 1 ,"destination_well_id": 21}
                            ,"40": {"destination_plate_number": 1 ,"destination_well_id": 22}
                            ,"41": {"destination_plate_number": 1 ,"destination_well_id": 23}
                            ,"42": {"destination_plate_number": 1 ,"destination_well_id": 24}
                            ,"43": {"destination_plate_number": 2 ,"destination_well_id": 19}
                            ,"44": {"destination_plate_number": 2 ,"destination_well_id": 20}
                            ,"45": {"destination_plate_number": 2 ,"destination_well_id": 21}
                            ,"46": {"destination_plate_number": 2 ,"destination_well_id": 22}
                            ,"47": {"destination_plate_number": 2 ,"destination_well_id": 23}
                            ,"48": {"destination_plate_number": 2 ,"destination_well_id": 24}
                            ,"49": {"destination_plate_number": 1 ,"destination_well_id": 25}
                            ,"50": {"destination_plate_number": 1 ,"destination_well_id": 26}
                            ,"51": {"destination_plate_number": 1 ,"destination_well_id": 27}
                            ,"52": {"destination_plate_number": 1 ,"destination_well_id": 28}
                            ,"53": {"destination_plate_number": 1 ,"destination_well_id": 29}
                            ,"54": {"destination_plate_number": 1 ,"destination_well_id": 30}
                            ,"55": {"destination_plate_number": 2 ,"destination_well_id": 25}
                            ,"56": {"destination_plate_number": 2 ,"destination_well_id": 26}
                            ,"57": {"destination_plate_number": 2 ,"destination_well_id": 27}
                            ,"58": {"destination_plate_number": 2 ,"destination_well_id": 28}
                            ,"59": {"destination_plate_number": 2 ,"destination_well_id": 29}
                            ,"60": {"destination_plate_number": 2 ,"destination_well_id": 30}
                            ,"61": {"destination_plate_number": 1 ,"destination_well_id": 31}
                            ,"62": {"destination_plate_number": 1 ,"destination_well_id": 32}
                            ,"63": {"destination_plate_number": 1 ,"destination_well_id": 33}
                            ,"64": {"destination_plate_number": 1 ,"destination_well_id": 34}
                            ,"65": {"destination_plate_number": 1 ,"destination_well_id": 35}
                            ,"66": {"destination_plate_number": 1 ,"destination_well_id": 36}
                            ,"67": {"destination_plate_number": 2 ,"destination_well_id": 31}
                            ,"68": {"destination_plate_number": 2 ,"destination_well_id": 32}
                            ,"69": {"destination_plate_number": 2 ,"destination_well_id": 33}
                            ,"70": {"destination_plate_number": 2 ,"destination_well_id": 34}
                            ,"71": {"destination_plate_number": 2 ,"destination_well_id": 35}
                            ,"72": {"destination_plate_number": 2 ,"destination_well_id": 36}
                            ,"73": {"destination_plate_number": 1 ,"destination_well_id": 37}
                            ,"74": {"destination_plate_number": 1 ,"destination_well_id": 38}
                            ,"75": {"destination_plate_number": 1 ,"destination_well_id": 39}
                            ,"76": {"destination_plate_number": 1 ,"destination_well_id": 40}
                            ,"77": {"destination_plate_number": 1 ,"destination_well_id": 41}
                            ,"78": {"destination_plate_number": 1 ,"destination_well_id": 42}
                            ,"79": {"destination_plate_number": 2 ,"destination_well_id": 37}
                            ,"80": {"destination_plate_number": 2 ,"destination_well_id": 38}
                            ,"81": {"destination_plate_number": 2 ,"destination_well_id": 39}
                            ,"82": {"destination_plate_number": 2 ,"destination_well_id": 40}
                            ,"83": {"destination_plate_number": 2 ,"destination_well_id": 41}
                            ,"84": {"destination_plate_number": 2 ,"destination_well_id": 42}
                            ,"85": {"destination_plate_number": 1 ,"destination_well_id": 43}
                            ,"86": {"destination_plate_number": 1 ,"destination_well_id": 44}
                            ,"87": {"destination_plate_number": 1 ,"destination_well_id": 45}
                            ,"88": {"destination_plate_number": 1 ,"destination_well_id": 46}
                            ,"89": {"destination_plate_number": 1 ,"destination_well_id": 47}
                            ,"90": {"destination_plate_number": 1 ,"destination_well_id": 48}
                            ,"91": {"destination_plate_number": 2 ,"destination_well_id": 43}
                            ,"92": {"destination_plate_number": 2 ,"destination_well_id": 44}
                            ,"93": {"destination_plate_number": 2 ,"destination_well_id": 45}
                            ,"94": {"destination_plate_number": 2 ,"destination_well_id": 46}
                            ,"95": {"destination_plate_number": 2 ,"destination_well_id": 47}
                            ,"96": {"destination_plate_number": 2 ,"destination_well_id": 48}
                        }
                    ]
                }
                ,"16": {  // keyed to sample_transfer_template_id in the database
                    "description": "Manual picking to nx 96"
                    ,"type": "user_specified"
                    ,"source": {
                        "plateCount": 1
                        ,"plateTypeId": "SPTT_0004"
                        ,"variablePlateCount": true
                    }
                    ,"destination": {
                        "plateCount": 0
                        ,"plateTypeId": "SPTT_0005"
                        ,"variablePlateCount": true
                    }
                }
                ,"18": {  // keyed to sample_transfer_template_id in the database
                    "description": "4x96 to 384"
                    ,"type": "standard"
                    ,"source": {
                        "plateCount": 4
                        ,"wellCount": 96
                        ,"plateTypeId": "SPTT_0005"
                        ,"variablePlateCount": false
                        ,"plateTitles": ["Quadrant&nbsp;1:&nbsp;","Quadrant&nbsp;2:&nbsp;","Quadrant&nbsp;3:&nbsp;","Quadrant&nbsp;4:&nbsp;"]
                    }
                    ,"destination":{
                        "plateCount": 1
                        ,"wellCount": 384
                        ,"plateTypeId": "SPTT_0006"
                        ,"variablePlateCount": false
                    }
                    ,"plateWellToWellMaps": [
                        {
                            "1":{"destination_plate_number":1,"destination_well_id":1}
                            ,"2":{"destination_plate_number":1,"destination_well_id":3}
                            ,"3":{"destination_plate_number":1,"destination_well_id":5}
                            ,"4":{"destination_plate_number":1,"destination_well_id":7}
                            ,"5":{"destination_plate_number":1,"destination_well_id":9}
                            ,"6":{"destination_plate_number":1,"destination_well_id":11}
                            ,"7":{"destination_plate_number":1,"destination_well_id":13}
                            ,"8":{"destination_plate_number":1,"destination_well_id":15}
                            ,"9":{"destination_plate_number":1,"destination_well_id":17}
                            ,"10":{"destination_plate_number":1,"destination_well_id":19}
                            ,"11":{"destination_plate_number":1,"destination_well_id":21}
                            ,"12":{"destination_plate_number":1,"destination_well_id":23}
                            ,"13":{"destination_plate_number":1,"destination_well_id":49}
                            ,"14":{"destination_plate_number":1,"destination_well_id":51}
                            ,"15":{"destination_plate_number":1,"destination_well_id":53}
                            ,"16":{"destination_plate_number":1,"destination_well_id":55}
                            ,"17":{"destination_plate_number":1,"destination_well_id":57}
                            ,"18":{"destination_plate_number":1,"destination_well_id":59}
                            ,"19":{"destination_plate_number":1,"destination_well_id":61}
                            ,"20":{"destination_plate_number":1,"destination_well_id":63}
                            ,"21":{"destination_plate_number":1,"destination_well_id":65}
                            ,"22":{"destination_plate_number":1,"destination_well_id":67}
                            ,"23":{"destination_plate_number":1,"destination_well_id":69}
                            ,"24":{"destination_plate_number":1,"destination_well_id":71}
                            ,"25":{"destination_plate_number":1,"destination_well_id":97}
                            ,"26":{"destination_plate_number":1,"destination_well_id":99}
                            ,"27":{"destination_plate_number":1,"destination_well_id":101}
                            ,"28":{"destination_plate_number":1,"destination_well_id":103}
                            ,"29":{"destination_plate_number":1,"destination_well_id":105}
                            ,"30":{"destination_plate_number":1,"destination_well_id":107}
                            ,"31":{"destination_plate_number":1,"destination_well_id":109}
                            ,"32":{"destination_plate_number":1,"destination_well_id":111}
                            ,"33":{"destination_plate_number":1,"destination_well_id":113}
                            ,"34":{"destination_plate_number":1,"destination_well_id":115}
                            ,"35":{"destination_plate_number":1,"destination_well_id":117}
                            ,"36":{"destination_plate_number":1,"destination_well_id":119}
                            ,"37":{"destination_plate_number":1,"destination_well_id":145}
                            ,"38":{"destination_plate_number":1,"destination_well_id":147}
                            ,"39":{"destination_plate_number":1,"destination_well_id":149}
                            ,"40":{"destination_plate_number":1,"destination_well_id":151}
                            ,"41":{"destination_plate_number":1,"destination_well_id":153}
                            ,"42":{"destination_plate_number":1,"destination_well_id":155}
                            ,"43":{"destination_plate_number":1,"destination_well_id":157}
                            ,"44":{"destination_plate_number":1,"destination_well_id":159}
                            ,"45":{"destination_plate_number":1,"destination_well_id":161}
                            ,"46":{"destination_plate_number":1,"destination_well_id":163}
                            ,"47":{"destination_plate_number":1,"destination_well_id":165}
                            ,"48":{"destination_plate_number":1,"destination_well_id":167}
                            ,"49":{"destination_plate_number":1,"destination_well_id":193}
                            ,"50":{"destination_plate_number":1,"destination_well_id":195}
                            ,"51":{"destination_plate_number":1,"destination_well_id":197}
                            ,"52":{"destination_plate_number":1,"destination_well_id":199}
                            ,"53":{"destination_plate_number":1,"destination_well_id":201}
                            ,"54":{"destination_plate_number":1,"destination_well_id":203}
                            ,"55":{"destination_plate_number":1,"destination_well_id":205}
                            ,"56":{"destination_plate_number":1,"destination_well_id":207}
                            ,"57":{"destination_plate_number":1,"destination_well_id":209}
                            ,"58":{"destination_plate_number":1,"destination_well_id":211}
                            ,"59":{"destination_plate_number":1,"destination_well_id":213}
                            ,"60":{"destination_plate_number":1,"destination_well_id":215}
                            ,"61":{"destination_plate_number":1,"destination_well_id":241}
                            ,"62":{"destination_plate_number":1,"destination_well_id":243}
                            ,"63":{"destination_plate_number":1,"destination_well_id":245}
                            ,"64":{"destination_plate_number":1,"destination_well_id":247}
                            ,"65":{"destination_plate_number":1,"destination_well_id":249}
                            ,"66":{"destination_plate_number":1,"destination_well_id":251}
                            ,"67":{"destination_plate_number":1,"destination_well_id":253}
                            ,"68":{"destination_plate_number":1,"destination_well_id":255}
                            ,"69":{"destination_plate_number":1,"destination_well_id":257}
                            ,"70":{"destination_plate_number":1,"destination_well_id":259}
                            ,"71":{"destination_plate_number":1,"destination_well_id":261}
                            ,"72":{"destination_plate_number":1,"destination_well_id":263}
                            ,"73":{"destination_plate_number":1,"destination_well_id":289}
                            ,"74":{"destination_plate_number":1,"destination_well_id":291}
                            ,"75":{"destination_plate_number":1,"destination_well_id":293}
                            ,"76":{"destination_plate_number":1,"destination_well_id":295}
                            ,"77":{"destination_plate_number":1,"destination_well_id":297}
                            ,"78":{"destination_plate_number":1,"destination_well_id":299}
                            ,"79":{"destination_plate_number":1,"destination_well_id":301}
                            ,"80":{"destination_plate_number":1,"destination_well_id":303}
                            ,"81":{"destination_plate_number":1,"destination_well_id":305}
                            ,"82":{"destination_plate_number":1,"destination_well_id":307}
                            ,"83":{"destination_plate_number":1,"destination_well_id":309}
                            ,"84":{"destination_plate_number":1,"destination_well_id":311}
                            ,"85":{"destination_plate_number":1,"destination_well_id":337}
                            ,"86":{"destination_plate_number":1,"destination_well_id":339}
                            ,"87":{"destination_plate_number":1,"destination_well_id":341}
                            ,"88":{"destination_plate_number":1,"destination_well_id":343}
                            ,"89":{"destination_plate_number":1,"destination_well_id":345}
                            ,"90":{"destination_plate_number":1,"destination_well_id":347}
                            ,"91":{"destination_plate_number":1,"destination_well_id":349}
                            ,"92":{"destination_plate_number":1,"destination_well_id":351}
                            ,"93":{"destination_plate_number":1,"destination_well_id":353}
                            ,"94":{"destination_plate_number":1,"destination_well_id":355}
                            ,"95":{"destination_plate_number":1,"destination_well_id":357}
                            ,"96":{"destination_plate_number":1,"destination_well_id":359}
                        }
                        ,{
                            "1":{"destination_plate_number":1,"destination_well_id":2}
                            ,"2":{"destination_plate_number":1,"destination_well_id":4}
                            ,"3":{"destination_plate_number":1,"destination_well_id":6}
                            ,"4":{"destination_plate_number":1,"destination_well_id":8}
                            ,"5":{"destination_plate_number":1,"destination_well_id":10}
                            ,"6":{"destination_plate_number":1,"destination_well_id":12}
                            ,"7":{"destination_plate_number":1,"destination_well_id":14}
                            ,"8":{"destination_plate_number":1,"destination_well_id":16}
                            ,"9":{"destination_plate_number":1,"destination_well_id":18}
                            ,"10":{"destination_plate_number":1,"destination_well_id":20}
                            ,"11":{"destination_plate_number":1,"destination_well_id":22}
                            ,"12":{"destination_plate_number":1,"destination_well_id":24}
                            ,"13":{"destination_plate_number":1,"destination_well_id":50}
                            ,"14":{"destination_plate_number":1,"destination_well_id":52}
                            ,"15":{"destination_plate_number":1,"destination_well_id":54}
                            ,"16":{"destination_plate_number":1,"destination_well_id":56}
                            ,"17":{"destination_plate_number":1,"destination_well_id":58}
                            ,"18":{"destination_plate_number":1,"destination_well_id":60}
                            ,"19":{"destination_plate_number":1,"destination_well_id":62}
                            ,"20":{"destination_plate_number":1,"destination_well_id":64}
                            ,"21":{"destination_plate_number":1,"destination_well_id":66}
                            ,"22":{"destination_plate_number":1,"destination_well_id":68}
                            ,"23":{"destination_plate_number":1,"destination_well_id":70}
                            ,"24":{"destination_plate_number":1,"destination_well_id":72}
                            ,"25":{"destination_plate_number":1,"destination_well_id":98}
                            ,"26":{"destination_plate_number":1,"destination_well_id":100}
                            ,"27":{"destination_plate_number":1,"destination_well_id":102}
                            ,"28":{"destination_plate_number":1,"destination_well_id":104}
                            ,"29":{"destination_plate_number":1,"destination_well_id":106}
                            ,"30":{"destination_plate_number":1,"destination_well_id":108}
                            ,"31":{"destination_plate_number":1,"destination_well_id":110}
                            ,"32":{"destination_plate_number":1,"destination_well_id":112}
                            ,"33":{"destination_plate_number":1,"destination_well_id":114}
                            ,"34":{"destination_plate_number":1,"destination_well_id":116}
                            ,"35":{"destination_plate_number":1,"destination_well_id":118}
                            ,"36":{"destination_plate_number":1,"destination_well_id":120}
                            ,"37":{"destination_plate_number":1,"destination_well_id":146}
                            ,"38":{"destination_plate_number":1,"destination_well_id":148}
                            ,"39":{"destination_plate_number":1,"destination_well_id":150}
                            ,"40":{"destination_plate_number":1,"destination_well_id":152}
                            ,"41":{"destination_plate_number":1,"destination_well_id":154}
                            ,"42":{"destination_plate_number":1,"destination_well_id":156}
                            ,"43":{"destination_plate_number":1,"destination_well_id":158}
                            ,"44":{"destination_plate_number":1,"destination_well_id":160}
                            ,"45":{"destination_plate_number":1,"destination_well_id":162}
                            ,"46":{"destination_plate_number":1,"destination_well_id":164}
                            ,"47":{"destination_plate_number":1,"destination_well_id":166}
                            ,"48":{"destination_plate_number":1,"destination_well_id":168}
                            ,"49":{"destination_plate_number":1,"destination_well_id":194}
                            ,"50":{"destination_plate_number":1,"destination_well_id":196}
                            ,"51":{"destination_plate_number":1,"destination_well_id":198}
                            ,"52":{"destination_plate_number":1,"destination_well_id":200}
                            ,"53":{"destination_plate_number":1,"destination_well_id":202}
                            ,"54":{"destination_plate_number":1,"destination_well_id":204}
                            ,"55":{"destination_plate_number":1,"destination_well_id":206}
                            ,"56":{"destination_plate_number":1,"destination_well_id":208}
                            ,"57":{"destination_plate_number":1,"destination_well_id":210}
                            ,"58":{"destination_plate_number":1,"destination_well_id":212}
                            ,"59":{"destination_plate_number":1,"destination_well_id":214}
                            ,"60":{"destination_plate_number":1,"destination_well_id":216}
                            ,"61":{"destination_plate_number":1,"destination_well_id":242}
                            ,"62":{"destination_plate_number":1,"destination_well_id":244}
                            ,"63":{"destination_plate_number":1,"destination_well_id":246}
                            ,"64":{"destination_plate_number":1,"destination_well_id":248}
                            ,"65":{"destination_plate_number":1,"destination_well_id":250}
                            ,"66":{"destination_plate_number":1,"destination_well_id":252}
                            ,"67":{"destination_plate_number":1,"destination_well_id":254}
                            ,"68":{"destination_plate_number":1,"destination_well_id":256}
                            ,"69":{"destination_plate_number":1,"destination_well_id":258}
                            ,"70":{"destination_plate_number":1,"destination_well_id":260}
                            ,"71":{"destination_plate_number":1,"destination_well_id":262}
                            ,"72":{"destination_plate_number":1,"destination_well_id":264}
                            ,"73":{"destination_plate_number":1,"destination_well_id":290}
                            ,"74":{"destination_plate_number":1,"destination_well_id":292}
                            ,"75":{"destination_plate_number":1,"destination_well_id":294}
                            ,"76":{"destination_plate_number":1,"destination_well_id":296}
                            ,"77":{"destination_plate_number":1,"destination_well_id":298}
                            ,"78":{"destination_plate_number":1,"destination_well_id":300}
                            ,"79":{"destination_plate_number":1,"destination_well_id":302}
                            ,"80":{"destination_plate_number":1,"destination_well_id":304}
                            ,"81":{"destination_plate_number":1,"destination_well_id":306}
                            ,"82":{"destination_plate_number":1,"destination_well_id":308}
                            ,"83":{"destination_plate_number":1,"destination_well_id":310}
                            ,"84":{"destination_plate_number":1,"destination_well_id":312}
                            ,"85":{"destination_plate_number":1,"destination_well_id":338}
                            ,"86":{"destination_plate_number":1,"destination_well_id":340}
                            ,"87":{"destination_plate_number":1,"destination_well_id":342}
                            ,"88":{"destination_plate_number":1,"destination_well_id":344}
                            ,"89":{"destination_plate_number":1,"destination_well_id":346}
                            ,"90":{"destination_plate_number":1,"destination_well_id":348}
                            ,"91":{"destination_plate_number":1,"destination_well_id":350}
                            ,"92":{"destination_plate_number":1,"destination_well_id":352}
                            ,"93":{"destination_plate_number":1,"destination_well_id":354}
                            ,"94":{"destination_plate_number":1,"destination_well_id":356}
                            ,"95":{"destination_plate_number":1,"destination_well_id":358}
                            ,"96":{"destination_plate_number":1,"destination_well_id":360}
                        }
                        ,{
                            "1":{"destination_plate_number":1,"destination_well_id":25}
                            ,"2":{"destination_plate_number":1,"destination_well_id":27}
                            ,"3":{"destination_plate_number":1,"destination_well_id":29}
                            ,"4":{"destination_plate_number":1,"destination_well_id":31}
                            ,"5":{"destination_plate_number":1,"destination_well_id":33}
                            ,"6":{"destination_plate_number":1,"destination_well_id":35}
                            ,"7":{"destination_plate_number":1,"destination_well_id":37}
                            ,"8":{"destination_plate_number":1,"destination_well_id":39}
                            ,"9":{"destination_plate_number":1,"destination_well_id":41}
                            ,"10":{"destination_plate_number":1,"destination_well_id":43}
                            ,"11":{"destination_plate_number":1,"destination_well_id":45}
                            ,"12":{"destination_plate_number":1,"destination_well_id":47}
                            ,"13":{"destination_plate_number":1,"destination_well_id":73}
                            ,"14":{"destination_plate_number":1,"destination_well_id":75}
                            ,"15":{"destination_plate_number":1,"destination_well_id":77}
                            ,"16":{"destination_plate_number":1,"destination_well_id":79}
                            ,"17":{"destination_plate_number":1,"destination_well_id":81}
                            ,"18":{"destination_plate_number":1,"destination_well_id":83}
                            ,"19":{"destination_plate_number":1,"destination_well_id":85}
                            ,"20":{"destination_plate_number":1,"destination_well_id":87}
                            ,"21":{"destination_plate_number":1,"destination_well_id":89}
                            ,"22":{"destination_plate_number":1,"destination_well_id":91}
                            ,"23":{"destination_plate_number":1,"destination_well_id":93}
                            ,"24":{"destination_plate_number":1,"destination_well_id":95}
                            ,"25":{"destination_plate_number":1,"destination_well_id":121}
                            ,"26":{"destination_plate_number":1,"destination_well_id":123}
                            ,"27":{"destination_plate_number":1,"destination_well_id":125}
                            ,"28":{"destination_plate_number":1,"destination_well_id":127}
                            ,"29":{"destination_plate_number":1,"destination_well_id":129}
                            ,"30":{"destination_plate_number":1,"destination_well_id":131}
                            ,"31":{"destination_plate_number":1,"destination_well_id":133}
                            ,"32":{"destination_plate_number":1,"destination_well_id":135}
                            ,"33":{"destination_plate_number":1,"destination_well_id":137}
                            ,"34":{"destination_plate_number":1,"destination_well_id":139}
                            ,"35":{"destination_plate_number":1,"destination_well_id":141}
                            ,"36":{"destination_plate_number":1,"destination_well_id":143}
                            ,"37":{"destination_plate_number":1,"destination_well_id":169}
                            ,"38":{"destination_plate_number":1,"destination_well_id":171}
                            ,"39":{"destination_plate_number":1,"destination_well_id":173}
                            ,"40":{"destination_plate_number":1,"destination_well_id":175}
                            ,"41":{"destination_plate_number":1,"destination_well_id":177}
                            ,"42":{"destination_plate_number":1,"destination_well_id":179}
                            ,"43":{"destination_plate_number":1,"destination_well_id":181}
                            ,"44":{"destination_plate_number":1,"destination_well_id":183}
                            ,"45":{"destination_plate_number":1,"destination_well_id":185}
                            ,"46":{"destination_plate_number":1,"destination_well_id":187}
                            ,"47":{"destination_plate_number":1,"destination_well_id":189}
                            ,"48":{"destination_plate_number":1,"destination_well_id":191}
                            ,"49":{"destination_plate_number":1,"destination_well_id":217}
                            ,"50":{"destination_plate_number":1,"destination_well_id":219}
                            ,"51":{"destination_plate_number":1,"destination_well_id":221}
                            ,"52":{"destination_plate_number":1,"destination_well_id":223}
                            ,"53":{"destination_plate_number":1,"destination_well_id":225}
                            ,"54":{"destination_plate_number":1,"destination_well_id":227}
                            ,"55":{"destination_plate_number":1,"destination_well_id":229}
                            ,"56":{"destination_plate_number":1,"destination_well_id":231}
                            ,"57":{"destination_plate_number":1,"destination_well_id":233}
                            ,"58":{"destination_plate_number":1,"destination_well_id":235}
                            ,"59":{"destination_plate_number":1,"destination_well_id":237}
                            ,"60":{"destination_plate_number":1,"destination_well_id":239}
                            ,"61":{"destination_plate_number":1,"destination_well_id":265}
                            ,"62":{"destination_plate_number":1,"destination_well_id":267}
                            ,"63":{"destination_plate_number":1,"destination_well_id":269}
                            ,"64":{"destination_plate_number":1,"destination_well_id":271}
                            ,"65":{"destination_plate_number":1,"destination_well_id":273}
                            ,"66":{"destination_plate_number":1,"destination_well_id":275}
                            ,"67":{"destination_plate_number":1,"destination_well_id":277}
                            ,"68":{"destination_plate_number":1,"destination_well_id":279}
                            ,"69":{"destination_plate_number":1,"destination_well_id":281}
                            ,"70":{"destination_plate_number":1,"destination_well_id":283}
                            ,"71":{"destination_plate_number":1,"destination_well_id":285}
                            ,"72":{"destination_plate_number":1,"destination_well_id":287}
                            ,"73":{"destination_plate_number":1,"destination_well_id":313}
                            ,"74":{"destination_plate_number":1,"destination_well_id":315}
                            ,"75":{"destination_plate_number":1,"destination_well_id":317}
                            ,"76":{"destination_plate_number":1,"destination_well_id":319}
                            ,"77":{"destination_plate_number":1,"destination_well_id":321}
                            ,"78":{"destination_plate_number":1,"destination_well_id":323}
                            ,"79":{"destination_plate_number":1,"destination_well_id":325}
                            ,"80":{"destination_plate_number":1,"destination_well_id":327}
                            ,"81":{"destination_plate_number":1,"destination_well_id":329}
                            ,"82":{"destination_plate_number":1,"destination_well_id":331}
                            ,"83":{"destination_plate_number":1,"destination_well_id":333}
                            ,"84":{"destination_plate_number":1,"destination_well_id":335}
                            ,"85":{"destination_plate_number":1,"destination_well_id":361}
                            ,"86":{"destination_plate_number":1,"destination_well_id":363}
                            ,"87":{"destination_plate_number":1,"destination_well_id":365}
                            ,"88":{"destination_plate_number":1,"destination_well_id":367}
                            ,"89":{"destination_plate_number":1,"destination_well_id":369}
                            ,"90":{"destination_plate_number":1,"destination_well_id":371}
                            ,"91":{"destination_plate_number":1,"destination_well_id":373}
                            ,"92":{"destination_plate_number":1,"destination_well_id":375}
                            ,"93":{"destination_plate_number":1,"destination_well_id":377}
                            ,"94":{"destination_plate_number":1,"destination_well_id":379}
                            ,"95":{"destination_plate_number":1,"destination_well_id":381}
                            ,"96":{"destination_plate_number":1,"destination_well_id":383}
                        }
                        ,{
                            "1":{"destination_plate_number":1,"destination_well_id":26}
                            ,"2":{"destination_plate_number":1,"destination_well_id":28}
                            ,"3":{"destination_plate_number":1,"destination_well_id":30}
                            ,"4":{"destination_plate_number":1,"destination_well_id":32}
                            ,"5":{"destination_plate_number":1,"destination_well_id":34}
                            ,"6":{"destination_plate_number":1,"destination_well_id":36}
                            ,"7":{"destination_plate_number":1,"destination_well_id":38}
                            ,"8":{"destination_plate_number":1,"destination_well_id":40}
                            ,"9":{"destination_plate_number":1,"destination_well_id":42}
                            ,"10":{"destination_plate_number":1,"destination_well_id":44}
                            ,"11":{"destination_plate_number":1,"destination_well_id":46}
                            ,"12":{"destination_plate_number":1,"destination_well_id":48}
                            ,"13":{"destination_plate_number":1,"destination_well_id":74}
                            ,"14":{"destination_plate_number":1,"destination_well_id":76}
                            ,"15":{"destination_plate_number":1,"destination_well_id":78}
                            ,"16":{"destination_plate_number":1,"destination_well_id":80}
                            ,"17":{"destination_plate_number":1,"destination_well_id":82}
                            ,"18":{"destination_plate_number":1,"destination_well_id":84}
                            ,"19":{"destination_plate_number":1,"destination_well_id":86}
                            ,"20":{"destination_plate_number":1,"destination_well_id":88}
                            ,"21":{"destination_plate_number":1,"destination_well_id":90}
                            ,"22":{"destination_plate_number":1,"destination_well_id":92}
                            ,"23":{"destination_plate_number":1,"destination_well_id":94}
                            ,"24":{"destination_plate_number":1,"destination_well_id":96}
                            ,"25":{"destination_plate_number":1,"destination_well_id":122}
                            ,"26":{"destination_plate_number":1,"destination_well_id":124}
                            ,"27":{"destination_plate_number":1,"destination_well_id":126}
                            ,"28":{"destination_plate_number":1,"destination_well_id":128}
                            ,"29":{"destination_plate_number":1,"destination_well_id":130}
                            ,"30":{"destination_plate_number":1,"destination_well_id":132}
                            ,"31":{"destination_plate_number":1,"destination_well_id":134}
                            ,"32":{"destination_plate_number":1,"destination_well_id":136}
                            ,"33":{"destination_plate_number":1,"destination_well_id":138}
                            ,"34":{"destination_plate_number":1,"destination_well_id":140}
                            ,"35":{"destination_plate_number":1,"destination_well_id":142}
                            ,"36":{"destination_plate_number":1,"destination_well_id":144}
                            ,"37":{"destination_plate_number":1,"destination_well_id":170}
                            ,"38":{"destination_plate_number":1,"destination_well_id":172}
                            ,"39":{"destination_plate_number":1,"destination_well_id":174}
                            ,"40":{"destination_plate_number":1,"destination_well_id":176}
                            ,"41":{"destination_plate_number":1,"destination_well_id":178}
                            ,"42":{"destination_plate_number":1,"destination_well_id":180}
                            ,"43":{"destination_plate_number":1,"destination_well_id":182}
                            ,"44":{"destination_plate_number":1,"destination_well_id":184}
                            ,"45":{"destination_plate_number":1,"destination_well_id":186}
                            ,"46":{"destination_plate_number":1,"destination_well_id":188}
                            ,"47":{"destination_plate_number":1,"destination_well_id":190}
                            ,"48":{"destination_plate_number":1,"destination_well_id":192}
                            ,"49":{"destination_plate_number":1,"destination_well_id":218}
                            ,"50":{"destination_plate_number":1,"destination_well_id":220}
                            ,"51":{"destination_plate_number":1,"destination_well_id":222}
                            ,"52":{"destination_plate_number":1,"destination_well_id":224}
                            ,"53":{"destination_plate_number":1,"destination_well_id":226}
                            ,"54":{"destination_plate_number":1,"destination_well_id":228}
                            ,"55":{"destination_plate_number":1,"destination_well_id":230}
                            ,"56":{"destination_plate_number":1,"destination_well_id":232}
                            ,"57":{"destination_plate_number":1,"destination_well_id":234}
                            ,"58":{"destination_plate_number":1,"destination_well_id":236}
                            ,"59":{"destination_plate_number":1,"destination_well_id":238}
                            ,"60":{"destination_plate_number":1,"destination_well_id":240}
                            ,"61":{"destination_plate_number":1,"destination_well_id":266}
                            ,"62":{"destination_plate_number":1,"destination_well_id":268}
                            ,"63":{"destination_plate_number":1,"destination_well_id":270}
                            ,"64":{"destination_plate_number":1,"destination_well_id":272}
                            ,"65":{"destination_plate_number":1,"destination_well_id":274}
                            ,"66":{"destination_plate_number":1,"destination_well_id":276}
                            ,"67":{"destination_plate_number":1,"destination_well_id":278}
                            ,"68":{"destination_plate_number":1,"destination_well_id":280}
                            ,"69":{"destination_plate_number":1,"destination_well_id":282}
                            ,"70":{"destination_plate_number":1,"destination_well_id":284}
                            ,"71":{"destination_plate_number":1,"destination_well_id":286}
                            ,"72":{"destination_plate_number":1,"destination_well_id":288}
                            ,"73":{"destination_plate_number":1,"destination_well_id":314}
                            ,"74":{"destination_plate_number":1,"destination_well_id":316}
                            ,"75":{"destination_plate_number":1,"destination_well_id":318}
                            ,"76":{"destination_plate_number":1,"destination_well_id":320}
                            ,"77":{"destination_plate_number":1,"destination_well_id":322}
                            ,"78":{"destination_plate_number":1,"destination_well_id":324}
                            ,"79":{"destination_plate_number":1,"destination_well_id":326}
                            ,"80":{"destination_plate_number":1,"destination_well_id":328}
                            ,"81":{"destination_plate_number":1,"destination_well_id":330}
                            ,"82":{"destination_plate_number":1,"destination_well_id":332}
                            ,"83":{"destination_plate_number":1,"destination_well_id":334}
                            ,"84":{"destination_plate_number":1,"destination_well_id":336}
                            ,"85":{"destination_plate_number":1,"destination_well_id":362}
                            ,"86":{"destination_plate_number":1,"destination_well_id":364}
                            ,"87":{"destination_plate_number":1,"destination_well_id":366}
                            ,"88":{"destination_plate_number":1,"destination_well_id":368}
                            ,"89":{"destination_plate_number":1,"destination_well_id":370}
                            ,"90":{"destination_plate_number":1,"destination_well_id":372}
                            ,"91":{"destination_plate_number":1,"destination_well_id":374}
                            ,"92":{"destination_plate_number":1,"destination_well_id":376}
                            ,"93":{"destination_plate_number":1,"destination_well_id":378}
                            ,"94":{"destination_plate_number":1,"destination_well_id":380}
                            ,"95":{"destination_plate_number":1,"destination_well_id":382}
                            ,"96":{"destination_plate_number":1,"destination_well_id":384}
                        }
                    ]
                }
                ,"20": {  // keyed to sample_transfer_template_id in the database
                    "description": "Hitpick for shipping"
                    ,"type": "user_specified"
                    ,"source": {
                        "plateCount": 1
                        ,"plateTypeId": "SPTT_0005"
                        ,"variablePlateCount": true
                    }
                    ,"destination": {
                        "plateCount": 0
                        ,"variablePlateCount": true
                    }
                }
                ,"21": {  // keyed to sample_transfer_template_id in the database
                    "description": "Qpix Log Reading to nx 96"
                    ,"type": "user_specified"
                    ,"source": {
                        "plateCount": 1
                        ,"plateTypeId": "SPTT_0004"
                        ,"variablePlateCount": true
                    }
                    ,"destination": {
                        "plateCount": 0
                        ,"plateTypeId": "SPTT_0005"
                        ,"variablePlateCount": true
                    }
                }
                ,"22": {  // keyed to sample_transfer_template_id in the database
                    "description": "Qpix Log Reading to nx 384"
                    ,"type": "user_specified"
                    ,"source": {
                        "plateCount": 1
                        ,"plateTypeId": "SPTT_0004"
                        ,"variablePlateCount": true
                    }
                    ,"destination": {
                        "plateCount": 0
                        ,"plateTypeId": "SPTT_0006"
                        ,"variablePlateCount": true
                    }
                }
                ,"23": {  // keyed to sample_transfer_template_id in the database
                    "description": "Plate Merge"
                    ,"type": "standard"
                    ,"source": {
                        "plateCount": 1
                        ,"variablePlateCount": true
                    }
                    ,"destination": {
                        "plateCount": 1
                        ,"variablePlateCount": false
                    }
                }
                ,"24": {  // keyed to sample_transfer_template_id in the database
                    "description": "Generic Transform"
                    ,"type": "user_specified"
                    ,"source": {
                        "plateCount": 1
                        ,"variablePlateCount": true
                    }
                    ,"destination": {
                        "plateCount": 1
                        ,"variablePlateCount": true
                    }
                }
                ,"25": {  // keyed to sample_transfer_template_id in the database
                    "description": "Rebatching for Transformation"
                    ,"type": "standard"
                    ,"source": {
                        "plateCount": 1
                        ,"variablePlateCount": true
                        ,"plateTypeId": "SPTT_0006"
                    }
                    ,"destination": {
                        "plateCount": 0
                        ,"variablePlateCount": true
                        ,"plateTypeId": "SPTT_0006"
                    }
                }
                ,"26": {  // keyed to sample_transfer_template_id in the database
                    "description": "Fragment Analyzer"
                    ,"type": "standard"
                    ,"source": {
                        "plateCount": 1
                        ,"variablePlateCount": true
                    }
                    ,"destination": {
                        "plateCount": 0
                        ,"variablePlateCount": true
                    }
                }
                ,"27": {  // keyed to sample_transfer_template_id in the database
                    "description": "NGS QC Pass"
                    ,"type": "standard"
                    ,"source": {
                        "plateCount": 1
                        ,"variablePlateCount": true
                    }
                    ,"destination": {
                        "plateCount": 0
                        ,"variablePlateCount": true
                    }
                }
                ,"28": {  // keyed to sample_transfer_template_id in the database
                    "description": "Shipping"
                    ,"type": "standard"
                    ,"source": {
                        "plateCount": 1
                        ,"variablePlateCount": true
                    }
                    ,"destination": {
                        "plateCount": 0
                        ,"variablePlateCount": true
                    }
                }
                ,"29": {  // keyed to sample_transfer_template_id in the database
                    "description": "Reformatting for Purification"
                    ,"type": "standard"
                    ,"source": {
                        "plateCount": 1
                        ,"variablePlateCount": true
                    }
                    ,"destination": {
                        "plateCount": 0
                        ,"variablePlateCount": true
                    }
                }
            }
""")
