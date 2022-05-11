import pysftp

# Source: https://stackoverflow.com/questions/33751854/upload-file-via-sftp-with-python

server_ip = "192.168.1.100"
username = "ismael"

def send(filepath):
    srv = pysftp.Connection(host=server_ip, username=username,log="pysftp.log")
    print("sftp is ready to send: "+filepath)
    with srv.cd('demo'):
        srv.put(filepath)

    srv.close()