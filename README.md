# nextgen_ehospital_beautiful_soup
Python script to get nextgen ehospital patient demography from saved pages and insert into mysql database
1. go to search menu of nextgen ehospital
2. search using an UHID
3. save page to a folder specified in the project
4. The python script
    - will read it using Beautiful Soup library (loop sleep for 1 second )
    - save data to mysql table
    - It can be used by other softwares to minimize manual data entry of patient demographics
### Project###
download
go to utility
./COPY_SERVICE
./INSTALL_SERVICE
./mk_folders
./reset_everything
Note: copy ehospital (it is logrotate file) to /etc/logrotate.d (if Debian)

