
"""

SampleTransferTemplate

    name = db.Column(db.String(100))
    is_one_to_one_transfer = db.Column(db.String(1),default="N", nullable=True)
    from_plate_size = db.Column(db.Integer,default=1,nullable=False)
    destination_plate_size = db.Column(db.Integer,default=1,nullable=False)

"""

from sqlalchemy.sql import table, column

from sqlalchemy import String, Integer, Date, Text

def import_template(op,template):

    template_name = template["template_name"]
    source_plate_well_count = int(template["from_plate_size"])
    destination_plate_well_count = int(template["destination_plate_size"])
    

    sql = "INSERT INTO sample_transfer_template(name,is_one_to_one_transfer,source_plate_well_count,destination_plate_well_count) "
    sql += " VALUES('%s','%s',%d,%d) " % (template_name,'N',source_plate_well_count,destination_plate_well_count)

    op.execute(sql)

    connection = op.get_bind()

    sample_transfer_template_id = None 

    select = 'select max(id) from sample_transfer_template'
    results = connection.execute(select)
    for result in results:
        sample_transfer_template_id = int(result[0])


    """

    sample_transfer_template_id = db.Column(db.Integer, db.ForeignKey('sample_transfer_template.id'))
    source_plate_number = db.Column(db.Integer, default=1, nullable=False)
    source_plate_well_id = db.Column(db.Integer, nullable=False)
    source_plate_well_id_string = db.Column(db.String(10),default="",nullable=True)

    destination_plate_number = db.Column(db.Integer, default=1, nullable=False)
    destination_plate_well_id = db.Column(db.Integer, nullable=False)
    destination_plate_well_id_string = db.Column(db.String(10),default="",nullable=True)

   template_details.append({
                        "source_well_id":row[1],
                        "source_plate_number":row[2],
                        "destination_well_id":row[4],
                        "destination_plate_number":row[5]
                    })

    """


    #
    # Create the template details rows here
    #
    for detail in template["details"]:
        print "DETAIL: ", detail

        source_plate_number = int(detail["source_plate_number"])
        source_well_id = int(detail["source_well_id"])
        destination_plate_number = int(detail["destination_plate_number"])
        destination_well_id = int(detail["destination_well_id"])
        

        sql = "INSERT INTO sample_transfer_template_details "
        sql += " (sample_transfer_template_id, source_plate_number, source_plate_well_id, "
        sql += " destination_plate_number, destination_plate_well_id, source_plate_well_id_string, destination_plate_well_id_string ) "
        sql += " VALUES(%d,%d,%d,%d,%d,'','') " % (sample_transfer_template_id, source_plate_number, source_well_id, destination_plate_number, destination_well_id )

        op.execute(sql)


