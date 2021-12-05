import myconn

connection1 = myconn.myconn()

cursor1 = connection1.cursor()

try:
    cursor1.execute('create database if not exists highedu')
    print('highedu database created')
except:
    print('highedu database not created')

cursor1.execute('use highedu')


try:
    cursor1.execute('create table if not exists user(userid varchar(8) not null unique, name varchar(30) not null, schoolname varchar(100), phymark int(3) not null, chemark int(3) not null, mathmark int(3) not null, biomark int(3) not null, cutoff float(5,2), compexam float(5,2), caste varchar(3) not null default "OC", city varchar(30), pincode int(6))')
    print('user table created')
except:
    print('user table not created')


try:
    cursor1.execute('create table if not exists admin(userid varchar(20) not null unique, name varchar(30) not null, password char(32) not null, secretkey varchar(20) not null)')
    print('admin table created')
except:
    print('admin table not created')


try:
    cursor1.execute('create table if not exists college(collegeid varchar(10) primary key, collegename varchar(264) not null ,collegetype char(1) not null, ranking int(6), city varchar(30), state varchar(30), pincode int(6) not null )')
    print('college table created')
except:
    print('college table not created')


try:
    cursor1.execute('create table if not exists course(collegeid varchar(10) not null , courseid varchar(4) not null, OC float(5,2) not null , BC float(5,2) not null , BCM float(5,2) not null , MBC float(5,2) not null , SC float(5,2) not null , SCA float(5,2) not null , ST float(5,2) not null , primary key (collegeid , courseid) )')
    print('course table created')
except:
    print('course table not created')


try:
    cursor1.execute('create table if not exists codes(keyname varchar(4) not null unique, valname varchar(100) not null)')
    print('codes table created')
except:
    print('codes table not created')

name = input('Enter admin name: ')
userid = input('Enter admin userid: ')
password = input('Enter admin password: ')
secretkey = input('Enter admin secretkey: ')

try:
    cursor1.execute(f"insert into admin values('{userid}', '{name}', (select md5('{password}')), '{secretkey}')")
    connection1.commit()
    print('Success')
except:
    print('Failed to enter admin details')

cursor1.close()
connection1.close()
