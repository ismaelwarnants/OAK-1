import pysftp

# Source: https://stackoverflow.com/questions/33751854/upload-file-via-sftp-with-python

srv = pysftp.Connection(host="192.168.1.100", username="ismael",log="pysftp.log")

with srv.cd('demo'): #chdir to public
    srv.put('Clipped_detection_2022-05-08_15-41-15.avi') #upload file to nodejs/

# Closes the connection
srv.close()