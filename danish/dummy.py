import MySQLdb
from urllib2 import urlopen

INSERT_RESTO = """
INSERT INTO resto 
(name, rating, type, capacity, staff, lon, lat, addr, city, zip)  
VALUES 
('%s', %d,      '%s',   %d,     %d,    '%s','%s','%s','%s', %d) 
"""

def insert(name, rating, rtype, capacity, staff, lon, lat, addr, city, zipcode):
    try:
        db=MySQLdb.connect(host="localhost",user="root", passwd="root", db="sp")
        cur=db.cursor()
        print(INSERT_RESTO % ( name, rating, rtype, capacity, staff, lon, lat, addr, city, zipcode ))
        cur.execute(INSERT_RESTO % ( name, rating, rtype, capacity, staff, lon, lat, addr, city, zipcode ))
        cur.close()
        db.commit()
        db.close()
    except MySQLdb.Error,e:
        print str(e)
        cur.close()
        db.commit()
        db.close()

def main():
    #insert('Subway', 4, 'Fastfood', 10, 4, '0', '0', 'Financial District', 'San Francisco', 94131)
    insert('Appleseed', 3, 'Restobar', 20, 8, '0', '0', 'Financial District', 'San Francisco', 94131)
    insert('Amber', 4, 'Restaurant', 30, 8, '0', '0', 'Financial District', 'San Francisco', 94131)

main()

