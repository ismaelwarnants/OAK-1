import pysftp, configparser

config = configparser.ConfigParser()
config.read('config.txt')

# Source: https://stackoverflow.com/questions/33751854/upload-file-via-sftp-with-python

server_ip = str(config['NODE']['ServerIP'])
username = str(config['NODE']['ServerUsername'])
video_destination = str(config['NODE']['VideoDestination'])

def send(filepath):
    srv = pysftp.Connection(host=server_ip, username=username,log="pysftp.log")
    print("sftp is ready to send: "+filepath)
    with srv.cd(video_destination):
        srv.put(filepath)

    srv.close()