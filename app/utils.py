import os
from contextlib import contextmanager
__author__ = "Ryan Johnson"
__version_info__ = ('0', '0', '8')
__version__ = '.'.join(__version_info__)
__module_name__ = 'hitpicking-utils-' + __version__

from collections import defaultdict
import math
from collections import defaultdict


def char2num(val):
    """
    Convert the given unicode character into an integer.
    """
    if isinstance(val, int):
        return val

    if not isinstance(val, unicode):
        raise ValueError('invalid argument: {!r}'.format(val))

    val = val.upper()

    if not ((ord(val) >= ord(u'A')) and (ord(val) <= ord(u'Z'))):
        raise ValueError('invalid argument: {!r}'.format(val))

    return (ord(val) - ord(u'A')) + 1


def num2char(val):
    """
    Convert the given integer into a unicode character.
    """
    if isinstance(val, unicode):
        return val

    if not (isinstance(val, int) and (val >= 1) and (val <= 26)):
        raise ValueError('invalid argument: {!r}'.format(val))

    return unichr(ord(u'A') + (val - 1))


def chunked(iterable, size):
    """
    Breaks the iterable into lists of length "size".
    """
    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []

    if chunk:
        yield chunk


def get_path(output_dir, filename, default):
    if output_dir and not os.path.exists(output_dir):
        # Try to make the output directory if it doesn't already exist.
        try:
            os.makedirs(output_dir)
        except os.error:
            pass

    if not output_dir:
        output_dir = os.getcwd()

    if not filename:
        filename = default

    return os.path.join(output_dir, filename)


def write_delimited(filename, data, delimiter='\t'):
    rows = data['rows']
    headers = data['headers']
    with open(filename, 'w') as f:
        f.write(delimiter.join(h for h in headers) + '\n')
        for row in rows:
            f.write(delimiter.join('{!s}'.format(i) for i in row) + '\n')


cached_session_factory = None


def get_session_factory(db_engine=None):
    global cached_session_factory

    if cached_session_factory:
        return cached_session_factory

    from sqlalchemy.orm import sessionmaker

    if not db_engine:
        import sqlalchemy as SA
        db_url = os.getenv('DATABASE_URL')
        if not db_url:
            raise RuntimeError('no database URL provided')
        db_engine = SA.create_engine(db_url, echo=False)

    Session = sessionmaker(bind=db_engine)
    cached_session_factory = Session

    return cached_session_factory


@contextmanager
def scoped_session(db_engine=None):
    """
    Provide a transactional scope around a series of operations.
    """
    session = get_session_factory(db_engine)()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class PrimerSourcePlate:
    """
    container for PCA Primer Source Plate helper methods
    used by pca_create_src and pca_master_mix functions, below
    """
    ALIQ_PER_WELL = 60
    MASTER_MIX_TEMPLATE = {'A1': 'Uni7-F',
                           'B1': 'Uni7-R',}

    @staticmethod
    def populate_row( starting_row, target_ct ):
        """
        @starting_row -- int representing row, eg, ord('A')

        returns [ ['A1','A2', ...], ['B1','B2', ...]]
        """
        container_ct = lambda tot, per: int( math.ceil( float(tot) / per ))
        wells = container_ct( target_ct, PrimerSourcePlate.ALIQ_PER_WELL )
        grid = [[] for _ in range(container_ct( wells, 24 ))]  # in case be need multiple rows
        for i in range( wells ):
            row = chr( starting_row + (i/24) )
            col = 1 + i % 24
            grid[ i/24 ].append("%s%d" % (row,col) )
        return grid

    @staticmethod
    def rows_for_custom_primers( primer_counts ):
        starting_row = ord(max(PrimerSourcePlate.MASTER_MIX_TEMPLATE)[0]) + 1
        l = []
        for primer_name, ct in primer_counts:
            lines = PrimerSourcePlate.populate_row(starting_row, ct)
            l.append( (primer_name, lines) )
            starting_row += len(lines)
        return l

    @staticmethod
    def plate_to_custom_primers(db, plate):
        from twistdb.sampletrack import SamplePlateLayout

        primers = defaultdict(int)
        missing = set()
        for well in db.session.query(SamplePlateLayout) \
                              .filter( SamplePlateLayout.sample_plate == plate ) \
                              .order_by( SamplePlateLayout.well_id ):
            try:
                primers[ well.sample.order_item.primer_pair ] += 1
            except AttributeError as e:
                print e
                missing.add( well )
        return primers, missing

    @staticmethod
    def primer_dict( db, plates ):
        """
        generate a primer map containing both the master template and custom primers
        eg, 'Uni7_F_ex': ['A1,'A2','B1',...]
        """
        dd = defaultdict(list)
        for well, primer in PrimerSourcePlate.MASTER_MIX_TEMPLATE.items():
            dd[primer].append(well)
        for plate in plates:
            primers, _ = PrimerSourcePlate.plate_to_custom_primers( db, plate )
            primer_counts = [ (primer.name, primers[pp])
                              for pp in sorted(primers)
                              for primer in (pp.fwd_primer, pp.rev_primer) ]
            for primer_name, lines in PrimerSourcePlate.rows_for_custom_primers( primer_counts ):
                for wells in lines:
                    dd[primer_name].extend( wells )
        return dict( (primer_name, sorted(l)) for primer_name, l in dd.items() )

    @staticmethod
    def echo_worklist( db, primer_plate_barcode, plates ):
        from twistdb.sampletrack import SamplePlateLayout

        primer_dict = PrimerSourcePlate.primer_dict( db, plates )

        worklist = []
        primer_ct = defaultdict(int)
        for plate in plates:
            for well in db.session.query(SamplePlateLayout) \
                                  .filter( SamplePlateLayout.sample_plate == plate ) \
                                  .order_by( SamplePlateLayout.well_id ):
                for primer_name in (well.sample.order_item.primer_pair.fwd_primer.name,
                                    well.sample.order_item.primer_pair.rev_primer.name):
                    loc = primer_dict[ primer_name ][ primer_ct[ primer_name ] / PrimerSourcePlate.ALIQ_PER_WELL ]
                    primer_ct[ primer_name ] += 1
                    
                    worklist.append( {'from': (primer_plate_barcode, primer_well),
                                      'to': (plate.external_barcode, plate.get_well_name( well.well_id ))
                    } )
        return worklist
