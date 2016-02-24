from collections import defaultdict
import datetime
import math


def calculate_volume_foreach_sample(samples):

    by_marker = defaultdict(list)
    d = {}
    qpix_plates =[]

    for marker in ('AMP','KAN'):
        d[ marker ] = ['sample-%d' % i for i in range(50)]

    for marker in sorted (d):
        tmp = defaultdict(list)
        for i, sample in enumerate(d[marker]):
            tmp[i // 48].append(sample)
            for plate_no in sorted (tmp):
                qpix_plates.append( (marker,tmp[plate_no]) )



        print len(qpix_plates), qpix_plates[0] ,qpix_plates[1]
        dest_tmp = defaultdict(lambda: defaultdict(int))
        for i, (marker, samples) in enumerate(qpix_plates):
            dest_tmp[i // 8][ marker ] += len( samples )

        destination_plates = []
        for i, (_, markers) in enumerate(sorted(dest_tmp.items())):
            title = []
            for marker, d in sorted(markers.items()):
                title.append("%d samples of %s" % (len(d), marker))
            destination_plates.append( {"type": "SPTT_0006",
                                        "first_in_group": i+1,
                                        "details": {
                                            "title": ', '.join(title)}} )



        return destination_plates
