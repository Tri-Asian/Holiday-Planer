import random
from datetime import date
from unittest import skip
import mysql.connector
import webview

mydb=mysql.connector.connect(host="localhost",user="root",passwd="",database="tests")
mycursor=mydb.cursor()


if mydb.is_connected():
    print()
else:
    print("Connection Failed.")

print("-------------*Welcome to Holiday Planner!*-------------")
    
mycursor.execute("show tables")
x = mycursor.fetchall()

if ("booking",) not in x:
    mycursor.execute("create table booking(Booking_No integer primary key,Destination varchar(20),Date_Of_Travel date,No_of_days integer,Airline varchar(20),Hotel varchar(20),No_of_guests integer);")
    mydb.commit()
    
if ("hotel",) not in x:
    mycursor.execute("create table hotel(Booking_No integer primary key,Destination varchar(20),Hotel varchar(30),Date_of_CheckIn date,No_of_Nights integer,No_of_Guests integer);")
    mydb.commit()
    
if ("flight",) not in x:
    mycursor.execute("create table flight(Booking_No integer primary key,Airline varchar(20),Departure_Destination varchar(20),Arrival_Destination varchar(20),Date_of_Departure date,No_of_Travellers integer);")
    mydb.commit()
    
if ("query",) not in x:
    mycursor.execute("create table query(Phone integer,Email_ID varchar(30),Query varchar(200))")
    mydb.commit()


#creating JavaScript Classs(object-self)
class Api:

    def book(self,dest,dot,nod,air,h,nog):
        bn=random.randint(100000,999999)
        mycursor.execute("insert into booking values({},'{}','{}',{},'{}','{}',{});".format(bn,dest,dot,nod,air,h,nog))
        mydb.commit()
        return"Thank You for booking, You will receive a confirmation shortly.\nFollow up on your booking using your booking reference -"+str(bn)

    def enquire(self,c,bn): 
        text=''
        if int(c)==1:
            mycursor.execute("select * from booking where Booking_No={}".format(bn))
            x=mycursor.fetchall()
            for i in x:
                l=list(i)
                l[2]=date.isoformat(l[2])
                for r in l:
                    text=text+'\n'+str(r)+'\n'
        elif int(c)==2:
            mycursor.execute("select * from hotel where Booking_No={}".format(bn))
            x=mycursor.fetchall()
            for i in x:
                l=list(i)
                l[3]=date.isoformat(l[3])
                for r in l:
                    text=text+'\n'+str(r)+'\n'
        elif int(c)==3:
            mycursor.execute("select * from flight where Booking_No={}".format(bn))
            x=mycursor.fetchall()
            for i in x:
                l=list(i)
                l[4]=date.isoformat(l[4])
                for r in l:
                    text=text+'\n'+str(r)+'\n'

        return text

    def book_hotel(self,dest,hc,doc,non,nog):
        bn=random.randint(100000,999999)
        mycursor.execute("insert into hotel values({},'{}','{}','{}',{},{});".format(bn,dest,hc,doc,non,nog))
        mydb.commit()
        return "Thank You for booking, You will receive a confirmation shortly.\nFollow up on your booking using your booking reference - "+str(bn)

    def book_flight(self,air,dd,ad,dod,Not):
        bn=random.randint(100000,999999)
        mycursor.execute("insert into flight values({},'{}','{}','{}','{}',{});".format(bn,air,dd,ad,dod,Not))
        mydb.commit()
        return "Thank You for booking, You will receive a confirmation shortly.\nFollow up on your booking using your booking reference -"+str(bn)

    def delete(self,c,bn):
        if int(c)==1:
            mycursor.execute("delete from booking where booking_No={};".format(bn))
        elif int(c)==2:
            mycursor.execute("delete from hotel where booking_No={};".format(bn))
        elif int(c)==3:
            mycursor.execute("delete from flight where booking_No={};".format(bn))
        mydb.commit()
        return"Your Booking has been Canceled Successfully"

    def query(self,pn,eid,q):
        return "Thank You for query, One of our Holiday Planner agent will contact you within 2-4 working days."


#creating a window Object
webview.create_window(title="Holiday Planner!",html=open("index.html").read(),js_api=Api())
#starting the object create
webview.start(debug=True)
