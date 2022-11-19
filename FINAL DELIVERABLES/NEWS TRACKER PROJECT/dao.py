from ibm_db import connect,exec_immediate,fetch_assoc
dbCon = connect('DATABASE=BLUDB;'
                     'HOSTNAME=0c77d6f2-5da9-48a9-81f8-86b520b87518.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;'  
                     'PORT=31198;'
                     'PROTOCOL=TCPIP;'
                     'SECURITY=SSL;'
                     'SSLServerCertificate=DigiCertGlobalRootCA.crt;'
                     'UID=qxs11302;'
                     'PWD=fAzshxOdUOA2I4HJ;','','')