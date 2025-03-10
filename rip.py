#!/usr/bin/python3
from bs4 import BeautifulSoup
import datetime,fcntl,os, logging, shutil,time,sys
import mysql_lis

#For mysql password
sys.path.append('/var/gmcs_config')
import astm_var_clg as astm_var
logging.basicConfig(filename='/var/log/ehospital.log',level=logging.DEBUG)  

def main():
  field_dictionary={0:'UHID',1:'mobile',2:'prefix',3:'name',4:'middlename',5:'surname',6:'sex',7:'DOB',8:'f8',9:'billing_type',10:'f10',11:'f11',12:'department',13:'unit',14:'address',15:'f15',16:'f16',17:'clinic'}

  try:
    html_file=open("/root/projects/bs/data/NextGen eHospital.html")
    fcntl.flock(html_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    html_data=html_file.read()
    soup=BeautifulSoup(html_data,'lxml')

    data_dictionary={}
    
    
    for i in range(0,18):
      if(soup.find("input",{"id":"mat-input-{}".format(i)})==None):
        data_dictionary[field_dictionary[i]]=''
      else:
        if(soup.find("input",{"id":"mat-input-{}".format(i)}).has_attr("value")==True):
          val=soup.find("input",{"id":"mat-input-{}".format(i)})["value"]
          logging.debug("{}:{}".format(i,val))  
          data_dictionary[field_dictionary[i]]='{}'.format(val)
        else:
          data_dictionary[field_dictionary[i]]=''
    logging.debug('data_dictionary:{}'.format(data_dictionary))
    save_data(data_dictionary)
  except Exception as my_ex:
    logging.debug(my_ex)

   
  #remove folder
  try:
    shutil.rmtree("/root/projects/bs/data/NextGen eHospital_files")
  except Exception as my_ex:
    logging.debug(my_ex)
   
  #remove file
  try:  
    os.remove("/root/projects/bs/data/NextGen eHospital.html")
  except Exception as my_ex:
    logging.debug(my_ex)


def save_data(data_dictionary):

  m=mysql_lis.mysql_lis()
  link=m.get_link(astm_var.my_host,astm_var.my_user,astm_var.my_pass,astm_var.my_db)

  #not that %s becomes %(name)s
  sql='insert into ehospital \
  (\
    `UHID`, `mobile`, `prefix`, `name`, `middlename`, `surname`, `sex`, `DOB`, `f8`, `billing_type`, `f10`, `f11`, `department`, `unit`, `address`, `f15`, `f16`, `clinic` \
  )\
  values\
  (\
   %(UHID)s, %(mobile)s, %(prefix)s, %(name)s, %(middlename)s, %(surname)s, %(sex)s, %(DOB)s, %(f8)s, %(billing_type)s, %(f10)s, %(f11)s, %(department)s, %(unit)s, %(address)s, %(f15)s, %(f16)s, %(clinic)s\
  )\
   on duplicate key update\
  `mobile`=%(mobile)s, `department`=%(department)s, `unit`=%(unit)s, `clinic`=%(clinic)s , `address`=%(address)s \
  '
  cur=m.run_query(link,sql,data_dictionary)
  m.close_cursor(cur)
  m.close_link(link)

if __name__ == '__main__':
  while (3==3):
    main()
    time.sleep(1)

#Some help to understand
#to find save content and analyse
#print(soup.prettify())
#fd=open("pretty.txt","+wt")
#fd.write(soup.prettify())
#uhid=soup.find("input",{"id":"mat-input-1"})["value"]
#print(uhid)

#get data
'''
DEBUG:root:0:20230091722
DEBUG:root:1:8460065913
DEBUG:root:2:Mr.
DEBUG:root:3:DINESHKUMAR
DEBUG:root:4:RAMASANKAR
DEBUG:root:5:GAUTAM
DEBUG:root:6:Male
DEBUG:root:7:22/09/1988 00:09:45
DEBUG:root:9:Prison
DEBUG:root:12:Casualty
DEBUG:root:14:PALI GAM SACHIN SURAT
DEBUG:root:17:Casualty Clinic

DEBUG:root:0:20230091822
DEBUG:root:1:9825683192
DEBUG:root:2:Mr.
DEBUG:root:3:apabhai
DEBUG:root:4:atabhai
DEBUG:root:5:bhammar
DEBUG:root:6:Male
DEBUG:root:7:22/09/1975 08:40:55
DEBUG:root:9:General
DEBUG:root:12:Orthopaedics
DEBUG:root:13:Unit5
DEBUG:root:14:270 bhagirath soc 1 varachha
DEBUG:root:17:OPD-6 (Orthopaedic OPD)




Field Type  Null  Key Default Extra
UHID  varchar(100)  NO  PRI NULL  
mobile  varchar(100)  NO    NULL  
prefix  varchar(100)  NO    NULL  
name  varchar(100)  YES   NULL  
middlename  varchar(100)  YES   NULL  
surname varchar(100)  YES   NULL  
sex varchar(100)  YES   NULL  
DOB varchar(100)  YES   NULL  
billing_type  varchar(100)  YES   NULL  
department  varchar(100)  YES   NULL  
unit  varchar(100)  YES   NULL  
clinic  varchar(100)  YES   NULL  
address varchar(100)  YES   NULL  

DEBUG:root:data_dictionary:{'UHID': '20250079905', 'mobile': '8128477219', 'prefix': 'Mrs.', 'name': 'NASIM', 'middlename': 'SABIR', 
'surname': 'SHAIKH', 'sex': 'Female', 'DOB': '06/03/1991 00:00:00', 'f8': '', 
'billing_type': 'General', 'f10': '', 'f11': '', 'department': 'Dermatology', 'unit': 'Unit1', 'address': 'A22-132- EWS AAWAS KOSAD', 
'f15': '', 'f16': '', 'clinic': 'OPD-24 (Dermatology OPD)'}


`UHID`, `mobile`, `prefix`, `name`, `middlename`, `surname`, `sex`, `DOB`, `f8`, `billing_type`, `f10`, `f11`, `department`, `unit`, `address`, `f15`, `f16`, `clinic`


%(UHID)s, %(mobile)s, %(prefix)s, %(name)s, %(middlename)s, %(surname)s, %(sex)s, %(DOB)s, %(f8)s, %(billing_type)s, %(f10)s, %(f11)s, %(department)s, %(unit)s, %(address)s, %(f15)s, %(f16)s, %(clinic)s

'''
