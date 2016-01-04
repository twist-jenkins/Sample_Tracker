from flask.ext.script import Command
import sys, os
import csv
#import unicodecsv
import unicodecsv, StringIO, cStringIO
import codecs, cStringIO
from app import db
#from app import (BlogPostSectionType, UserSegment, CalendarEventType, NewsArticleType, MediaType, PublicationType)
from sqlalchemy import or_, and_
from twistdb.sampletrack import SampleTransfer, SampleTransferType, SampleTransferDetail, \
    SamplePlate, SamplePlateLayout, SamplePlateType
from twistdb.public import Operator, SampleType, Sample, SampleType

"""

sample_plate_type

type_id  |                  name                  |                                             description                                              | reference_pdf_name | reference_thumbnail_name | number_clusters | sample_plate_type | status  |    rows_alpha    | cols_num 
-----------+----------------------------------------+------------------------------------------------------------------------------------------------------+--------------------+--------------------------+-----------------+-------------------+---------+------------------+----------


----------+----------------------------------------+----------------------------------------+--------------------+--------------------------+-----------------+-------------------+--------+------------------+----------
 SPTT_0004 | 48 well, plastic                       | Generic 48 well plastic plate          |                    |                          |              48 | plastic_48        | active |                  |         
 SPTT_0005 | 96 well, plastic                       | Generic 96 well plastic plate          | SPTT_0005.pdf      | SPTT_0005.png            |              96 | plastic_96        | active | ABCDEFGH         |       12
 SPTT_0006 | 384 well, plastic                      | Generic 384 well plastic plate         | SPTT_0006.pdf      | SPTT_0006.png            |             384 | plastic_384       | active | ABCDEFGHIJKLMNOP |       24
 SPTT_0007 | 1536 well, plastic                     | Generic 1536 well plastic plate        | SPTT_0007.pdf      | SPTT_0007.png            |            1536 | plastic_1536      | active |                  |         
 SPTT_0010 | 30 well, plastic (Twist NW)            | Twist Custom Plastic NW 30 well plate  | SPTT_0010.pdf      | SPTT_0010.png            |              30 | custom_plastic_30 | active |                  |         
 SPTT_0025 | 16 well, Nectin plastic 4x4 (Twist NW) | 16 well, Nectin plastic 4x4 (Twist NW) |                    |                          |              16 | custom_plastic_16 | active |                  |         
(6 rows)


sample_plate 

sample_plate_id        |  type_id  |    date_created    |          name           |               description               | external_barcode | status | operator_id | storage_location_id 
-------------------------------+-----------+--------------------+-------------------------+-----------------------------------------+------------------+--------+-------------+---------------------
 SPLT_0000001                  | SPTT_0004 | 04-AUG-14 14:50:00 | Cell Plate Master 1     | Frozen cell stocks master plate 1       |                  | in_use | ET          | LOC_0004
 SPLT_0000002                  | SPTT_0004 | 04-AUG-14 14:50:00 | Cell Plate Working 1    | Frozen cell stocks working plate 1      |                  | in_use | ET          | LOC_0004
 SPLT_5457fcf1e208466dd16d3b08 | SPTT_0010 | 03-NOV-14 14:08:00 | SRN_000160 OEX Plate 1  | SRN_000160 Oligo Extraction Plate: 1    |                  | in_use | CT          | LOC_0001
 SPLT_546bc9677993058485ebe117 | SPTT_0010 | 18-NOV-14 14:34:00 | SRN_000170 OEX Plate 1  | SRN_000170 Oligo Extraction Plate: 1    |                  | in_use | CT          | LOC_0001
 SPLT_546d09c77993058485ebe124 | SPTT_0010 | 19-NOV-14 13:21:00 | SRN_000171 OEX Plate 1  | SRN_000171 Oligo Extraction Plate: 1    |                  | in_use | CT          | LOC_0013
 SPLT_54dcff9e79930551833dc066 | SPTT_0006 | 12-FEB-15 11:31:42 | SRN_000190 OEX Plate 1  | SRN_000190 Oligo Extraction Plate: '1'  |                  | in_use | SC          | LOC_0064
 SPLT_54e13c6c7993050cd5f01591 | SPTT_0006 | 15-FEB-15 16:40:00 | SRN_000192 OEX Plate 1  | SRN_000192 Oligo Extraction Plate: '1'  |                  | in_use | SC          | LOC_0064
 SPLT_54e4e665799305280bff8107 | SPTT_0005 | 18-FEB-15 11:22:13 | SRN_000194 OEX Plate 1  | SRN_000194 Oligo Extraction Plate: '1'  |                  | in_use | SC          | LOC_0064
 SPLT_54fd464c799305befe027d88 | SPTT_0010 | 09-MAR-15 00:05:48 | SRN_000206 OEX Plate 2  | SRN_000206 Oligo Extraction Plate: '2'  |                  | in_use | RA          | LOC_0064
 SPLT_54fd44f3799305bf03025513 | SPTT_0010 | 09-MAR-15 00:00:03 | SRN_000206 OEX Plate 1  | SRN_000206 Oligo Extraction Plate: '1'  |                  | in_use | RA          | LOC_0064
 SPLT_54fe09a9799305befe027dac | SPTT_0006 | 09-MAR-15 13:59:21 | SRN_000195 OEX Plate 1  | SRN_000195 Oligo Extraction Plate: '1'  |                  | in_use | LS          | LOC_0064
 SPLT_54fe2cd8799305bf03025524 | SPTT_0005 | 09-MAR-15 16:29:28 | SRN_000198 OEX Plate 1  | SRN_000198 Oligo Extraction Plate: '1'  |                  | in_use | MH          | LOC_0064
 SPLT_54ff8e8b79930535e1f73701 | SPTT_0005 | 10-MAR-15 17:38:35 | SRN_000192 OEX Plate 1  | SRN_000192 Oligo Extraction Plate: '1'  |                  | in_use | LS          | LOC_0064
 SPLT_54ff26d279930535e1f7369b | SPTT_0005 | 10-MAR-15 10:16:02 | SRN_000195 OEX Plate 1  | SRN_000195 Oligo Extraction Plate: '1'  |                  | in_use | LS          | LOC_0064
 SPLT_5500a08f79930535ddf73683 | SPTT_0005 | 11-MAR-15 13:07:43 | SRN_000215 OEX Plate 1  | SRN_000215 Oligo Extraction Plate: '1'  |                  | in_use | SC          | LOC_0064
 SPLT_55020bef79930535ddf7368c | SPTT_0010 | 12-MAR-15 14:58:07 | SRN_000193 OEX Plate 1  | SRN_000193 Oligo Extraction Plate: '1'  |                  | in_use | CT          | LOC_0064
 SPLT_55020bef79930535ddf7368d | SPTT_0010 | 12-MAR-15 14:58:07 | SRN_000193 OEX Plate 2  | SRN_000193 Oligo Extraction Plate: '2'  |                  | in_use | CT          | LOC_0064
 SPLT_55020bef79930535ddf7368e | SPTT_0010 | 12-MAR-15 14:58:07 | SRN_000193 OEX Plate 3  | SRN_000193 Oligo Extraction Plate: '3'  |                  | in_use | CT          | LOC_0064
 SPLT_55020bef79930535ddf7368f | SPTT_0010 | 12-MAR-15 14:58:07 | SRN_000193 OEX Plate 4  | SRN_000193 Oligo Extraction Plate: '4'  |                  | in_use | CT          | LOC_0064
 SPLT_5507990c79930596545c4158 | SPTT_0010 | 16-MAR-15 20:01:32 | SRN_000211 OEX Plate 1  | SRN_000211 Oligo Extraction Plate: '1'  |                  | in_use | RA          | LOC_0064
 SPLT_55089eb579930596565bace3 | SPTT_0010 | 17-MAR-15 14:37:57 | SRN_000221 OEX Plate 1  | SRN_000221 Oligo Extraction Plate: '1'  |                  | in_use | SC          | LOC_0064
 SPLT_55089eb579930596565bace4 | SPTT_0010 | 17-MAR-15 14:37:57 | SRN_000221 OEX Plate 9  | SRN_000221 Oligo Extraction Plate: '9'  |                  | in_use | SC          | LOC_0064
 SPLT_550f96917993056d44934af0 | SPTT_0005 | 22-MAR-15 21:29:05 | SRN_000192 OEX Plate 1  | SRN_000192 Oligo Extraction Plate: '1'  |                  | in_use | MH          | LOC_0064
 SPLT_5510d8b07993056d49934d85 | SPTT_0010 | 23-MAR-15 20:23:28 | SRN_000211 OEX Plate 1  | SRN_000211 Oligo Extraction Plate: '1'  |                  | in_use | RA          | LOC_0064
 SPLT_5510d8b07993056d49934d86 | SPTT_0010 | 23-MAR-15 20:23:28 | SRN_000211 OEX Plate 2  | SRN_000211 Oligo Extraction Plate: '2'  |                  | in_use | RA          | LOC_0064
 SPLT_5510db897993056d4a934cea | SPTT_0010 | 23-MAR-15 20:35:37 | SRN_000211 OEX Plate 1  | SRN_000211 Oligo Extraction Plate: '1'  |                  | in_use | RA          | LOC_0064
 SPLT_5510ff897993053d20832c1c | SPTT_0010 | 23-MAR-15 23:09:13 | SRN_000212 OEX Plate 1  | SRN_000212 Oligo Extraction Plate: '1'  |                  | in_use | RA          | LOC_0064
 SPLT_551155f07993053d20832c20 | SPTT_0025 | 24-MAR-15 05:17:52 | SRN_000212 OEX Plate 1  | SRN_000212 Oligo Extraction Plate: '1'  |                  | in_use | RA          | LOC_0064
 SPLT_551159137993053d1b832c1c | SPTT_0025 | 24-MAR-15 05:31:15 | SRN_000212 OEX Plate 3  | SRN_000212 Oligo Extraction Plate: '3'  |                  | in_use | RA          | LOC_0064
 SPLT_55115af07993053d1d832c1c | SPTT_0025 | 24-MAR-15 05:39:12 | SRN_000212 OEX Plate 1  | SRN_000212 Oligo Extraction Plate: '1'  |                  | in_use | RA          | LOC_0064
 SPLT_55115d6a7993053d20832c25 | SPTT_0025 | 24-MAR-15 05:49:46 | SRN_000218 OEX Plate 1  | SRN_000218 Oligo Extraction Plate: '1'  |                  | in_use | RA          | LOC_0064
 SPLT_5511f4d07993053d1d832c22 | SPTT_0025 | 24-MAR-15 16:35:44 | SRN_000212 OEX Plate 1  | SRN_000212 Oligo Extraction Plate: '1'  |                  | in_use | RA          | LOC_0064
 SPLT_5511f5ae7993053d20832c65 | SPTT_0025 | 24-MAR-15 16:39:26 | SRN_000212 OEX Plate 3  | SRN_000212 Oligo Extraction Plate: '3'  |                  | in_use | RA          | LOC_0064
 SPLT_551447ea799305f35369e21e | SPTT_0005 | 26-MAR-15 10:54:50 | SRN_000229 OEX Plate 1  | SRN_000229 Oligo Extraction Plate: '1'  |                  | in_use | SC          | LOC_0064
 SPLT_551af7e9799305f3536af39b | SPTT_0025 | 31-MAR-15 12:39:21 | SRN_000231 OEX Plate 1  | SRN_000231 Oligo Extraction Plate: '1'  |                  | in_use | CT          | LOC_0064
 SPLT_551c3923799305f3536af3b9 | SPTT_0005 | 01-APR-15 11:29:55 | SRN_000231 OEX Plate 1  | SRN_000231 Oligo Extraction Plate: '1'  |                  | in_use | SC          | LOC_0064
 SPLT_551dd1f4799305f3536b50db | SPTT_0005 | 02-APR-15 16:34:12 | SRN_000213 OEX Plate 1  | SRN_000213 Oligo Extraction Plate: '1'  |                  | in_use | ST          | LOC_0064
 SPLT_551dd1f4799305f3536b50dc | SPTT_0005 | 02-APR-15 16:34:12 | SRN_000213 OEX Plate 2  | SRN_000213 Oligo Extraction Plate: '2'  |                  | in_use | ST          | LOC_0064
 SPLT_551dd1f4799305f3536b50dd | SPTT_0005 | 02-APR-15 16:34:12 | SRN_000213 OEX Plate 3  | SRN_000213 Oligo Extraction Plate: '3'  |                  | in_use | ST          | LOC_0064
 SPLT_551dd1f4799305f3536b50de | SPTT_0005 | 02-APR-15 16:34:12 | SRN_000213 OEX Plate 4  | SRN_000213 Oligo Extraction Plate: '4'  |                  | in_use | ST          | LOC_0064
 SPLT_55241823799305f3536bea69 | SPTT_0005 | 07-APR-15 10:47:15 | SRN_000240 OEX Plate 1  | SRN_000240 Oligo Extraction Plate: '1'  |                  | in_use | SC          | LOC_0064
 SPLT_55294d0e799305f3536c649e | SPTT_0006 | 11-APR-15 09:34:22 | SRN_000246 OEX Plate 1  | SRN_000246 Oligo Extraction Plate: '1'  |                  | in_use | LS          | LOC_0064
 SPLT_5529984e799305f3536c659f | SPTT_0005 | 11-APR-15 14:55:26 | SRN_000244 OEX Plate 1  | SRN_000244 Oligo Extraction Plate: '1'  |                  | in_use | SC          | LOC_0064
 SPLT_552d7d9579930533ba3c4e8d | SPTT_0005 | 14-APR-15 13:50:29 | SRN_000248 OEX Plate 1  | SRN_000248 Oligo Extraction Plate: '1'  |                  | in_use | KB          | LOC_0064
 SPLT_552e9d1679930533b63c4e74 | SPTT_0005 | 15-APR-15 10:17:10 | SRN_000247 OEX Plate 1  | SRN_000247 Oligo Extraction Plate: '1'  |                  | in_use | KB          | LOC_0064
 SPLT_553143d67993059e450bb2dd | SPTT_0005 | 17-APR-15 10:33:10 | SRN_000249 OEX Plate 1  | SRN_000249 Oligo Extraction Plate: '1'  |                  | in_use | KB          | LOC_0064
:


sample 

sample_id |    type_id    |    date_created    | operator_id |             name              |                                               description                                                | external_barcode | parent_process_id | parent_transfer_process_id | status | fwd_primer_ps_id | rev_primer_ps_id | reagent_type_set_lot_id 
-----------+---------------+--------------------+-------------+-------------------------------+----------------------------------------------------------------------------------------------------------+------------------+-------------------+----------------------------+--------+------------------+------------------+-------------------------
 GA_0001   | gene_assembly | 20-OCT-13 00:00:00 | CW          | Q5-GFP-PCA-PCR_TCH-15Cycles   | Q5; 15 cycles of touchdown PCA followed by 30 cycles of PCR (using 1/25 of PCA reaction).Old SAN_00001   |                  | PCR_0001          |                            | active | PS_49            | PS_50            | 
 GA_0002   | gene_assembly | 20-OCT-13 00:00:00 | CW          | Q5-GFP-PCA-PCR_TCH-20Cycles   | Q5; 20 cycles of touchdown PCA followed by 30 cycles of PCR (using 1/25 of PCA reaction).Old SAN_00001   |                  | PCR_0001          |                            | active | PS_49            | PS_50            | 
 GA_0003   | gene_assembly | 20-OCT-13 00:00:00 | CW          | Q5-GFP-PCA-PCR_TCH-25Cycles   | Q5: 25 cycles of touchdown PCA followed by 30 cycles of PCR (using 1/25 of PCA reaction).Old SAN_00001   |                  | PCR_0001          |                            | active | PS_49            | PS_50            | 
 GA_0004   | gene_assembly | 20-OCT-13 00:00:00 | CW          | Q5-GFP-PCA-PCR_52C_15Cycles   | Q5; 15 cycles of PCA followed by 30 cycles of PCR (using 1/25 of PCA reaction).Old SAN_00001             |                  | PCR_0001          |                            | active | PS_49            | PS_50            | 
 GA_0005   | gene_assembly | 20-OCT-13 00:00:00 | CW          | Q5-GFP-PCA-PCR_52C_20Cycles   | Q5; 20 cycles of PCA followed by 30 cycles of PCR (using 1/25 of PCA reaction).Old SAN_00001             |                  | PCR_0001          |                            | active | PS_49            | PS_50            | 
 GA_0006   | gene_assembly | 20-OCT-13 00:00:00 | CW          | Q5-GFP-PCA-PCR_52C_25Cycles   | Q5: 25 cycles of PCA followed by 30 cycles of PCR (using 1/25 of PCA reaction).Old SAN_00001             |                  | PCR_0001          |                            | active | PS_49            | PS_50            | 
 GA_0007   | gene_assembly | 20-OCT-13 00:00:00 | CW          | Vent-GFP-PCA-PCR_TCH-15Cycles | Vent; 15 cycles of touchdown PCA followed by 30 cycles of PCR (using 1/25 of PCA reaction).Old SAN_00001 |                  | PCR_0002          |                            | active | PS_49            | PS_50            | 
 GA_0008   | gene_assembly | 20-OCT-13 00:00:00 | CW          | Vent-GFP-PCA-PCR_TCH-20Cycles | Vent; 20 cycles of touchdown PCA followed by 30 cycles of PCR (using 1/25 of PCA reaction).Old SAN_00001 |                  | PCR_0002          |                            | active | PS_49            | PS_50            | 
 GA_0009   | gene_assembly | 20-OCT-13 00:00:00 | CW          | Vent-GFP-PCA-PCR_TCH-25Cycles | Vent: 25 cycles of touchdown PCA followed by 30 cycles of PCR (using 1/25 of PCA reaction).Old SAN_00001 |                  | PCR_0002          |                            | active | PS_49            | PS_50            | 
 GA_0010   | gene_assembly | 20-OCT-13 00:00:00 | CW          | Vent-GFP-PCA-PCR_43C_15Cycles | Vent:15 cycles of PCA followed by 30 cycles of PCR (using 1/25 of PCA reaction).Old SAN_00001            |                  | PCR_0002          |                            | active | PS_49            | PS_50            | 
(10 rows)



operator 

operator_id |    jira_username     |                  email                   |       user_id        | first_name  | middle_initial |   last_name   | role |         last_seen         | initials |  ip_addr  | login_count 
-------------+----------------------+------------------------------------------+----------------------+-------------+----------------+---------------+------+---------------------------+----------+-----------+-------------
 CW          | cwu                  | cwu@twistbioscience.com                  | cwu                  | Cheng-Hsien |                | Wu            |    2 | 17-JUN-15 18:03:42.320391 | CW       | 127.0.0.1 |        1687
 RJ          | rjohnson             | rjohnson@twistbioscience.com             | rjohnson             | Ryan        |                | Johnson       |  268 |                           | RJ       |           |           0
 MS          | msalman              | msalman@twistbioscience.com              | msalman              | Salman      |                | Muhammad      |    8 |                           | SM       |           |           0
 EL          | eleproust            | eleproust@twistbioscience.com            | eleproust            | Emily       |                | Leproust      |    6 |                           | EL       |           |           0
 BB          | bbanyai              | bbanyai@twistbioscience.com              | bbanyai              | Bill        |                | Banyai        |    6 |                           | BB       |           |           0
 BP          | bpeck                | bpeck@twistbioscience.com                | bpeck                | Bill        |                | Peck          |    6 |                           | BP       |           |           0
 PH          | pheilman             | pheilman@twistbioscience.com             | pheilman             | Paul        |                | Heilman       |   34 |                           | PH       |           |           0
 RR          | rrudoff              | rrudoff@twistbioscience.com              | rrudoff              | Roger       |                | Rudoff        |    2 |                           | RR       |           |           0
 AD          | adelacruz            | adelacruz@twistbioscience.com            | adelacruz            | Anthony     |                | Delacruz      |    2 |                           | AD       |           |           0
 EG          | egwerder             | egwerder@twistbioscience.com             | egwerder             | Eric        |                | Gwerder       |    2 |                           | EG       |           |           0
 KC          | kchi                 | kchi@twistbioscience.com                 | kchi                 | Kai         |                | Chi           |    2 |                           | KC       |           |           0
 NH          | nhowells             | nhowells@twistbioscience.com             | nhowells             | Nick        |                | Howells       |    2 |                           | NH       |           |           0
 SW          | swilliams            | swilliams@twistbioscience.com            | swilliams            | Scott       |                | Williams      |  262 | 09-JUN-15 16:18:05.508901 | SW       | 127.0.0.1 |          12
 ET          | etoro                | etoro@twistbioscience.com                | etoro                | Esteban     |                | Toro          |    2 | 09-JUN-15 15:41:44.882367 | ET       | 127.0.0.1 |        1209
 KL          | klee                 | klee@twistbioscience.com                 | klee                 | KJ          |                | Lee           |  511 | 22-JUN-15 17:39:29.072501 | KL       | 127.0.0.1 |        1530
 LZ          | labuser_zebra        | labuser_zebra@twistbioscience.com        | labuser_zebra        | Labuser     |                | Zebra         |    8 | 16-JUN-15 09:19:00.23638  | LZ       | 127.0.0.1 |         447
 PF          | pfinn                | pfinn@twistbioscience.com                | pfinn                | Patrick     |                | Finn          |   12 |                           | PF       |           |           0
 WM          | wmcginn-straub       | wmcginn-straub@twistbioscience.com       | wmcginn-straub       | Wesley      |                | McGInn-Straub |   12 |                           | WM       |           |           0
 SMC         | smccuine             | smccuine@twistbioscience.com             | smccuine             | Scott       |                | McCuine       |   12 |                           | SM       |           |           0
 EK          | ekwok                | ekwok@twistbioscience.com                | ekwok                | Edwin       |                | Kwok          |    8 | 22-JUN-15 14:54:35.62461  | EK       | 127.0.0.1 |         277
 LN          | labuser_nikon        | labuser_nikon@twistbioscience.com        | labuser_nikon        | Labuser     |                | Nikon         |    8 |                           | LN       |           |           0
 LK          | labuser_kruss        | labuser_kruss@twistbioscience.com        | labuser_kruss        | Labuser     |                | Kruss         |    8 |                           | LK       |           |           0
 TP          | tperalta             | tperalta@twistbioscience.com             | tperalta             | Tiffany     |                | Peralta       |    8 | 22-JUN-15 11:16:50.249612 | TP       | 127.0.0.1 |         171
 LS1         | labuser_syn1         | labuser_syn1@twistbioscience.com         | labuser_syn1         | Labuser     |                | Syn1          |    8 |                           | LS       |           |           0
 LS2         | labuser_syn2         | labuser_syn2@twistbioscience.com         | labuser_syn2         | Labuser     |                | Syn2          |    8 |                           | LS       |           |           0
 LS3         | labuser_syn3         | labuser_syn3@twistbioscience.com         | labuser_syn3         | Labuser     |                | Syn3          |    8 |                           | LS       |           |           0
 CL          | cledogar             | cledogar@twistbioscience.com             | cledogar             | Charlie     |                | Ledogar       |  262 | 19-JUN-15 17:09:37.61744  | CL       | 127.0.0.1 |         890
 LVP         | labuser_veriti_prod  | labuser_veriti_prod@twistbioscience.com  | labuser_veriti_prod  | Labuser     |                | Veriti Prod   |    8 |                           | LV       |           |           0
 LC          | labuser_comsol       | labuser_comsol@twistbioscience.com       | labuser_comsol       | Labuser     |                | Comsol        |    8 |                           | LC       |           |           0
 PI          | pindermuhle          | pindermuhle@twistbioscience.com          | pindermuhle          | Pierre      |                | Indermuhle    |    2 | 09-JUN-15 08:15:09.666654 | PI       | 127.0.0.1 |          11
 MK          | mkrause              | mkrause@twistbioscience.com              | mkrause              | Mike        |                | Krause        |    2 |                           | MK       |           |           0
 KR          | krosendahl           | krosendahl@twistbioscience.com           | krosendahl           | Kristee     |                | Rosendahl     |   12 |                           | KR       |           |           0
 SM          | smonteclaro          | smonteclaro@twistbioscience.com          | smonteclaro          | Stephen     |                | Monteclaro    |    8 |                           | SM       |           |           0
 GL          | glinshiz             | glinshiz@twistbioscience.com             | glinshiz             | Gregory     |                | Linshiz       |  326 | 22-JUN-15 16:39:29.185799 | GL       | 127.0.0.1 |        2651
 LSH         | labuser_shipping     | labuser_shipping@twistbioscience.com     | labuser_shipping     | Labuser     |                | Shipping      |   12 | 08-JUN-15 12:38:59.898549 | LS       | 127.0.0.1 |         297
 NK          | ekovach              | ekovach@twistbioscience.com              | ekovach              | Ned         |                | Kovach        |    8 | 04-JUN-15 10:25:24.589521 | NK       | 127.0.0.1 |           1
 KB          | kbutcher             | kbutcher@twistbioscience.com             | kbutcher             | Kristin     |                | Butcher       |    8 | 22-JUN-15 11:11:14.309494 | KB       | 127.0.0.1 |        1569
 SK          | skeeney              | skeeney@twistbioscience.com              | skeeney              | Shastine    |                | Keeney        |    2 | 01-JUN-15 10:51:16.640683 | SK       | 127.0.0.1 |          21
 LM          | labuser_miseq        | labuser_miseq@twistbioscience.com        | labuser_miseq        | Labuser     |                | MiSeq         |    8 | 19-JUN-15 18:11:30.821864 | LM       | 127.0.0.1 |         288
 SS          | ssingh               | ssingh@twistbioscience.com               | ssingh               | Santok      |                | Singh         |    2 | 17-JUN-15 10:37:30.790801 | SS       | 127.0.0.1 |          30
 JM          | jmartin              | jmartin@twistbioscience.com              | jmartin              | John        |                | Martin        |  262 | 22-JUN-15 14:48:54.674976 | JM       | 127.0.0.1 |         275
 EQ          | equan                | equan@twistbioscience.com                | equan                | Emerson     |                | Quan          |    6 | 04-JUN-15 10:51:45.630198 | EQ       | 127.0.0.1 |          15
 MU          | murias               | murias@twistbioscience.com               | murias               | Marcos      |                | Urias         |    8 | 22-JUN-15 10:34:41.323034 | MU       | 127.0.0.1 |        1034
 JF          | jfidanza             | jfidanza@twistbioscience.com             | jfidanza             | Jackie      |                | Fidanza       |   70 | 21-JUN-15 23:22:29.18956  | JF       | 127.0.0.1 |        2052
 JH          | jhorsfall            | jhorsfall@twistbioscience.com            | jhorsfall            | James       |                | Horsfall      |    8 | 22-JUN-15 14:59:40.764647 | JH       | 127.0.0.1 |         965
 AH          | ahsiao               | ahsiao@twistbioscience.com               | ahsiao               | Austin      |                | Hsiao         |    8 | 16-JUN-15 20:51:02.981402 | AH       | 127.0.0.1 |         185
 NS          | nsrivastava          | nsrivastava@twistbioscience.com          | nsrivastava          | Nimisha     |                | Srivastava    |    2 | 09-JUN-15 09:27:07.375024 | NS       | 127.0.0.1 |           9
 WO          | woldham              | woldham@twistbioscience.com              | woldham              | William     |                | Oldham        |    8 | 16-JUN-15 15:59:57.638013 | WO       | 127.0.0.1 |          89
 DB          | dbibl                | dbibl@twistbioscience.com                | dbibl                | Daniel      |                | Bibl          |    2 | 16-JUN-15 12:38:22.934554 | DB       | 127.0.0.1 |         179
 EM          | emarsh               | emarsh@twistbioscience.com               | emarsh               | EP          |                | Marsh         |    2 | 22-JUN-15 08:08:07.486512 | EM       | 127.0.0.1 |         208
 PL          | plucero              | plucero@twistbioscience.com              | plucero              | Phillip     |                | Lucero        |    8 | 22-JUN-15 08:40:16.300649 | PL       | 127.0.0.1 |         635
 LPR         | labuser_plate_reader | labuser_plate_reader@twistbioscience.com | labuser_plate_reader | Labuser     |                | Plate Reader  |    8 | 04-JUN-15 16:46:03.224744 | LP       | 127.0.0.1 |         348
 RP          | rpark                | rpark@twistbioscience.com                | rpark                | Roy         |                | Park          |    8 | 22-JUN-15 14:03:28.098077 | RP       | 127.0.0.1 |         150
 AF          | afernandez           | afernandez@twistbioscience.com           | afernandez           | Andres      |                | Fernandez     |  130 | 22-JUN-15 15:55:18.949942 | AF       | 127.0.0.1 |         994
 ST          | streusch             | streusch@twistbioscience.com             | streusch             | Sebastian   |                | Treusch       |    2 | 17-JUN-15 18:44:46.528273 | ST       | 127.0.0.1 |        1468
 SI          | sindermuehle         | sindermuehle@twistbioscience.com         | sindermuehle         | Scott       |                | Indermuehle   |    2 | 18-JUN-15 08:23:50.298539 | SI       | 127.0.0.1 |          24
 DW          | dwang                | dwang@twistbioscience.com                | dwang                | David       |                | Wang          |    8 |                           | DW       |           |           0
 AG          | agonzalez            | agonzalez@twistbioscience.com            | agonzalez            | Art         |                | Gonzalez      |    0 |                           | AG       |           |           0
 TT          | ttran                | ttran.consulting@gmail.com               | ttran.consulting     | Tony        |                | Tran          |    0 |                           | TT       |           |           0
 BW          | bwan                 | bwan@twistbioscience.com                 | bwan                 | Brian       |                | Wan           |   72 | 22-JUN-15 14:37:26.022631 | BW       | 127.0.0.1 |        3534
 PW          | pweiss               | pweiss@twistbioscience.com               | pweiss               | Patrick     |                | Weiss         |  262 | 20-JUN-15 15:08:43.419166 | PW       | 127.0.0.1 |         669
 LS          | lstanton             | lstanton@twistbioscience.com             | lstanton             | Leslie      |                | Stanton       |    6 | 22-JUN-15 18:52:39.168163 | LS       | 127.0.0.1 |        9856
 LB          | labuser_bioanalyzer  | labuser_bioanalyzer@twistbioscience.com  | labuser_bioanalyzer  | Labuser     |                | Bioanalyzer   |    8 | 19-JUN-15 18:03:35.244024 | LB       | 127.0.0.1 |         739
 CT          | cthompson            | cthompson@twistbioscience.com            | cthompson            | Christina   |                | Thompson      |  118 | 22-JUN-15 16:04:24.961864 | CT       | 127.0.0.1 |        4119
 LSL         | labuser_silicon      | labuser_silicon@twistbioscience.com      | labuser_silicon      | Silicon     |                | Labuser       |    8 | 22-JUN-15 17:06:10.299534 | SL       | 127.0.0.1 |        8065
 LF          | labuser_fraganalyzer | labuser_fraganalyzer@twistbioscience.com | labuser_fraganalyzer | Labuser     |                | FragAnalyzer  |    8 | 12-JUN-15 10:40:35.663766 | LF       | 127.0.0.1 |        3059
 SC          | schen                | schen@twistbioscience.com                | schen                | Siyuan      |                | Chen          |    6 | 22-JUN-15 20:47:36.252224 | SC       | 127.0.0.1 |        8840
 TC          | tcox                 | tcox@twistbioscience.com                 | tcox                 | Tony        |                | Cox           |    8 | 09-JUN-15 09:27:14.937058 | TC       | 127.0.0.1 |        1710
 JD          | jdiggans             | jdiggans@twistbioscience.com             | jdiggans             | James       |                | Diggans       |   12 | 22-JUN-15 14:32:12.478062 | JD       | 127.0.0.1 |        4444
 MH          | hamady               | mhamady@twistbioscience.com              | mhamady              | Mike        |                | Hamady        |    1 | 22-JUN-15 17:30:40.890899 | MH       | 127.0.0.1 |        6924
 AUD         | adecker              | adecker@twistbioscience.com              | adecker              | Aubianna    |                | Decker        |    2 | 17-JUN-15 10:37:30.790801 | AUD      | 127.0.0.1 |           1
 NB          | nbach                | nbach@twistbioscience.com                | nbach                | Nathan      |                | Bach          |    6 | 22-JUN-15 10:28:41.666702 | NB       | 127.0.0.1 |         354
 JW          | jworrall             | jworrall@twistbioscience.com             | jworrall             | Joe         |                | Worrall       |    2 | 22-JUN-15 11:07:19.086769 | JW       | 127.0.0.1 |         857
 RA          | ragayan              | ragayan@twistbioscience.com              | ragayan              | Rodney      |                | Agayan        |   66 | 23-JUN-15 01:01:26.989706 | RA       | 127.0.0.1 |        3832



storage_location 

 storage_location_id | parent_storage_location_id |                  name                  |                                      description                                       | location_type |  status  
---------------------+----------------------------+----------------------------------------+----------------------------------------------------------------------------------------+---------------+----------
 LOC_0001            |                            | UNKNOWN                                | Unknown location, somewhere in 455 Mission Bay Blvd S                                  | storage       | active
 LOC_0002            |                            | FREEZER 01: -20C                       | Small -20C freezer in the wet lab, near the stand up fume hood (white)                 | storage       | active
 LOC_0003            |                            | FREEZER 02: -30C                       | Large -30C freezer in low copy lab                                                     | storage       | active
 LOC_0004            |                            | FREEZER 03: -80C                       | Large -80C Thermo freezer in main lab hallway                                          | storage       | active
 LOC_0005            |                            | FREEZER 04: 4C                         | Large 4C freezer in main lab hallway                                                   | storage       | active
 LOC_0009            |                            | ROOM TEMP: 01                          | Above-bench shelf #1 (Above Fragment Analyzer) in wet lab                              | storage       | active
 LOC_0010            |                            | ROOM TEMP: 02-4C                       | Above-bench shelf #2 (Above Cheng's bench) in wet lab                                  | storage       | active
 LOC_0011            |                            | ROOM TEMP: 03-2B                       | Above-bench shelf #3 (Above Siyuan's bench) in wet lab                                 | storage       | active
 LOC_0012            |                            | ROOM TEMP: 04-3B                       | Above-bench shelf #4 (Closest to ABI waste hood) in wet lab                            | storage       | active
 LOC_0013            |                            | ROOM TEMP: UNKNOWN                     | Unknown room temperature location in wet lab, not in flammable cabinets nor fume hoods | storage       | active
 LOC_0018            |                            | FLAMMABLES 1: WET LAB                  | Flammable cabinet #1 (beneath silanization hood) in wet lab                            | storage       | active
 LOC_0019            |                            | FLAMMABLES 2: WET LAB                  | Flammable cabinet #2 (beneath ABI disposal hood) in wet lab                            | storage       | active
 LOC_0020            |                            | FLAMMABLES 3: WET LAB                  | Flammable cabinet #3 (beneath ABI) in wet lab                                          | storage       | active
 LOC_0021            |                            | FLAMMABLES 4: WET LAB                  | Flammable cabinet #4 (beneath acid hood) in wet lab                                    | storage       | active
 LOC_0022            |                            | LEFT DEWAR: 5TH FLOOR CLOSET           | Left Dewar in 5th floor closet                                                         | storage       | active
 LOC_0023            |                            | DISPOSED/RETURNED                      | Bottle disposed to trash or recycled/Dewar or cylinder returned to vendor              | disposal      | active
 LOC_0024            |                            | MIXED WASTE: WET LAB                   | Mixed waste disposal container in wet lab                                              | disposal      | inactive
 LOC_0025            |                            | CLEANER WASTE: WET LAB                 | Cleaner waste disposal container in wet lab                                            | disposal      | inactive
 LOC_0026            |                            | BIOHAZARD WASTE                        | Biohazard waste                                                                        | disposal      | inactive
 LOC_0027            |                            | FLAMMABLES: 1.0                        | Cage, inside flammables cabinet                                                        | storage       | active
 LOC_0028            |                            | GAS CYLINDER RACK: WET LAB             | Rack of gas cylinders in wet lab                                                       | storage       | active
 LOC_0029            |                            | OPEN: ENGINEERING ROOM                 | Engineering room, outside flammables cabinet                                           | storage       | active
 LOC_0030            |                            | CAGE: 1.0                              | Cage, outside flammables cabinet                                                       | storage       | active
 LOC_0031            |                            | SYNTHESIZER: ENGINEERING ROOM          | Engineering room: Inside the Chemical Delivery Unit of Synthesizer 1                   | storage       | active
 LOC_0032            |                            | FLAMMABLES 5: WET LAB                  | Flammable cabinet #5 (beneath base hood) in wet lab                                    | storage       | active
 LOC_0033            |                            | FLAMMABLES 1: CHIP LAB                 | Flammable cabinet #1 (beneath fluorination hood) in chip lab                           | storage       | active
 LOC_0034            |                            | FLAMMABLES 2: CHIP LAB                 | Flammable cabinet #2 (beneath fluorination hood) in chip lab                           | storage       | active
 LOC_0035            |                            | FLAMMABLES 3: CHIP LAB                 | Flammable cabinet #3 (beneath right side hood) in chip lab                             | storage       | active
 LOC_0036            |                            | FLAMMABLES 4: CHIP LAB                 | Flammable cabinet #4 (beneath right side hood) in chip lab                             | storage       | active
 LOC_0037            |                            | SILANE WASTE: WET LAB                  | Silane mixed waste disposal container in silanization hood in wet lab                  | disposal      | inactive
 LOC_0038            |                            | FLAMMABLES 6: WET LAB                  | Flammable cabinet #6 (beneath base hood) in wet lab                                    | storage       | active
 LOC_0039            |                            | FLAMMABLES 7: WET LAB                  | Flammable cabinet #7 (beneath base hood) in wet lab                                    | storage       | active
 LOC_0040            |                            | FLAMMABLES 8: WET LAB                  | Flammable cabinet #8 (beneath base hood) in wet lab                                    | storage       | active
 LOC_0041            |                            | FLAMMABLES 9: WET LAB                  | Flammable cabinet #9 (beneath base hood) in wet lab                                    | storage       | active
 LOC_0042            |                            | FLAMMABLES 10: WET LAB                 | Flammable cabinet #10 (beneath base hood) in wet lab                                   | storage       | active
 LOC_0043            |                            | GAS CYLINDER RACK: CHIP LAB            | Rack for single gas cylinder in chip lab                                               | storage       | active
 LOC_0044            |                            | MIXED WASTE: CHIP LAB                  | Mixed waste disposal container in chip lab                                             | disposal      | inactive
 LOC_0045            |                            | RIGHT DEWAR: 5TH FLOOR CLOSET          | Right Dewar in 5th floor closet                                                        | storage       | active
 LOC_0046            |                            | OPEN: CHIP LAB                         | Chip lab, outside flammables cabinet                                                   | storage       | active
 LOC_0047            |                            | SYNTHESIZER WASTE: ENGINEERING ROOM    | Mixed waste disposal container in flammables cabinet of synthesizer (Room 509)         | disposal      | inactive
 LOC_0048            |                            | CORROSIVES: 1.0                        | Cage, inside corrosives cabinet                                                        | storage       | active
 LOC_0049            | LOC_0045                   | RESERVE DEWAR: 5TH FLOOR CLOSET        | Reserve dewar in 5th floor closet                                                      | storage       | active
 LOC_0050            |                            | POLYPROPYLENE ROLLING CART 1           | Polypropylene rolling cart #1 in chip lab                                              | storage       | active
 LOC_0051            |                            | RESERVE DEWARS: 1.0 MACHINE ROOM       | Reserve Dewars in 1st floor Machine Room                                               | storage       | active
 LOC_0052            |                            | DEWAR 5: 1.0 MACHINE ROOM              | Dewar 5 in 1st floor Machine Room                                                      | storage       | inactive
 LOC_0053            |                            | DEWAR 6: 1.0 MACHINE ROOM              | Dewar 6 in 1st floor Machine Room                                                      | storage       | inactive
 LOC_0054            |                            | DEWAR 7: 1.0 MACHINE ROOM              | Dewar 7 in 1st floor Machine Room                                                      | storage       | inactive
 LOC_0055            |                            | OPEN: WET LAB                          | Wet lab, outside flammables cabinet                                                    | storage       | active
 LOC_0056            |                            | FREEZER 05: -20C                       | Small -20C freezer in the low copy lab, near the door                                  | storage       | active
 LOC_0057            |                            | LOW COPY LAB BIOLOGICAL SAFETY CABINET | Biological Saftey hood in the low copy lab -Prep Station                               | storage       | active
 LOC_0058            |                            | FREEZER 06: -30C                       | Large Panasonic -30C two door freezer in main lab hallway                              | storage       | active
 LOC_0059            |                            | FREEZER 07: -20C                       | Small -20C freezer in the wet lab, near the stand up fume hood (black)                 | storage       | active
 LOC_0060            | LOC_0059                   | FREEZER 07: -20C, SHELF 1              | Small -20C freezer in the wet lab, near the stand up fume hood (black), shelf 1        | storage       | active
 LOC_0061            | LOC_0059                   | FREEZER 07: -20C, SHELF 2              | Small -20C freezer in the wet lab, near the stand up fume hood (black), shelf 2        | storage       | active
 LOC_0062            | LOC_0059                   | FREEZER 07: -20C, SHELF 3              | Small -20C freezer in the wet lab, near the stand up fume hood (black), shelf 3        | storage       | active
 LOC_0063            | LOC_0059                   | FREEZER 07: -20C, SHELF 4              | Small -20C freezer in the wet lab, near the stand up fume hood (black), shelf 4        | storage       | active
 LOC_0064            |                            | FAKE PLATE STORAGE 1                   | Fake plate storage location 1                                                          | plate_storage | active
 LOC_0065            |                            | FAKE PLATE STORAGE 2                   | Fake plate storage location 2                                                          | plate_storage | active
 LOC_0066            |                            | FAKE WORKSTATION 1                     | Fake workstation location 1                                                            | work_station  | active
 LOC_0067            |                            | FAKE WORKSTATION 2                     | Fake workstation location 2                                                            | work_station  | active
 LOC_0068            |                            | 5th floor backend production materials | All materials used for backend production on the 5th floor of 455 MBBS                 | storage       | active
(61 rows)


"""


class LoadLookupTables(Command):

    def truncate_lookup_tables(self):
        """
        db.session.query(BlogPostSectionType).delete()
        db.session.query(UserSegment).delete()
        db.session.query(CalendarEventType).delete()
        db.session.query(NewsArticleType).delete()
        db.session.query(MediaType).delete()
        db.session.query(PublicationType).delete()
        """
        db.session.query(SampleTransferType).delete()

    def load_sample_transfer_type_table(self):
        for row_data in [
            "Add PCR Master Mix", "Transfer Aliquot", "Move Specimen"
        ]:
            row = SampleTransferType(row_data)
            db.session.add(row)

        db.session.commit()


    """

    def load_block_post_section_type_table(self):

        for row_data in [
            "text_only", "text_and_image", "image_only", "pullquote"
        ]:
            row = BlogPostSectionType(row_data)
            db.session.add(row)

        db.session.commit()


    def load_user_segment_table(self):

        for row_data in [
            "segmentA", "segmentB"
        ]:
            row = UserSegment(row_data)
            db.session.add(row)

        db.session.commit()


    def load_calendar_event_type_table(self):

        for row_data in [
            "conference", "presentation", "hiring event"
        ]:
            row = CalendarEventType(row_data)
            db.session.add(row)

        db.session.commit()


    def load_news_article_type_table(self):

        for row_data in [
            "pr", "news", "journal article", "interview"
        ]:
            row = NewsArticleType(row_data)
            db.session.add(row)

        db.session.commit()



    def load_media_type_table(self):

        for row_data in [
            "newspaper", "magazine", "webpage", "audio", "video", "tweet"
        ]:
            row = MediaType(row_data)
            db.session.add(row)

        db.session.commit()




    def load_publication_type_table(self):

        for row_data in [
            "newspaper", "magazine", "website", "book", "radio", "podcast", "television"
        ]:
            row = PublicationType(row_data)
            db.session.add(row)

        db.session.commit()
    """



    def run(self):
        
        print "Reloading the lookup tables..."

        self.truncate_lookup_tables()

        self.load_sample_transfer_type_table()

        """

        self.truncate_lookup_tables()

        self.load_block_post_section_type_table()

        self.load_calendar_event_type_table()

        self.load_news_article_type_table()

        self.load_media_type_table()

        self.load_publication_type_table()
        """

