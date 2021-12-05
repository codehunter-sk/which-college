import myconn as myconn
import csv
import sys

def cnxac():
    global connection, cursor, ds
    connection = myconn.myconn()
    cursor = connection.cursor()
    cursor.execute('use highedu')
    ds = myconn.ds

def upload_coldata(csvfile_name):
    cnxac()
    returnmsg = "Uploading.."

    try:
        with open(csvfile_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    try:
                        query = "INSERT INTO college (collegeid, collegename, collegetype, ranking, city, state, pincode) \
                        VALUES (%s,%s,%s,%s,%s,%s,%s)"
                        val = (row[0], row[1], row[2], row[3], row[4],row[5],row[6])
                        cursor.execute(query, val)
                        line_count += 1
                    except ds.IntegrityError :
                        pass                    
            returnmsg = f'Processed {line_count-1} rows.'

        connection.commit()
    except Exception as e1:
        returnmsg = "Upload error, check the consol log"
    return returnmsg

def upload_coursedata(csvfile_name):
    cnxac()
    returnmsg = "Uploading.."
    try:
        with open(csvfile_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    try:
                        query = "INSERT INTO course (collegeid, courseid, oc, bc, bcm, mbc, sc, sca, st) \
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        val = (row[0], row[1], row[2], row[3], row[4],row[5],row[6],row[7],row[8])
                        cursor.execute(query, val)
                        line_count += 1
                    except ds.IntegrityError :
                        pass
            returnmsg = f'Processed {line_count-1} rows.'

        connection.commit()
    except Exception as e1:
        returnmsg = "Upload error, check the consol log"
    return returnmsg

def upload_courseid(csvfile_name):
    cnxac()
    returnmsg = "Uploading.."
    try:
        with open(csvfile_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    try:
                        query = "INSERT INTO codes (keyname, valname) VALUES (%s,%s)"
                        val = (row[0], row[1])
                        cursor.execute(query, val)
                        line_count += 1
                    except ds.IntegrityError :
                        pass
            returnmsg = f'Processed {line_count-1} rows.'

        connection.commit()
    except Exception as e1:
        returnmsg = "Upload error, check the consol log"
    return returnmsg


