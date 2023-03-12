import time
import subprocess
import sys
import socket
import argparse
import os

TPSLIMIT = 3
TRANSFERS = 3
# bandiwidth limits for gd
BWLIMIT = "8.5M"
# one to one correspondence
SOURCE_PATH_LIST = ["/your/source/path/a/", "/your/source/path/b/"]
DESTINATION_PATH_LIST = ["remote_drive_a:remote/path/a/", "remote_drive_b:remote/path/b/"]

def check_port_in_use(port, host='127.0.0.1'):
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, int(port)))
        s.settimeout(1)
        s.shutdown(2)
        return True
    except socket.error:
        return False
    finally:
        if s:
            s.close()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-sp", "--source_path", type=str, default="")
    parser.add_argument("-dp", "--destination_path", type=str, default="")
    args = parser.parse_args()
    return args

def get_file_size(filePath, size=0):
    size = 0
    for root, dirs, files in os.walk(filePath):
        for f in files:
            size += os.path.getsize(os.path.join(root, f))
    return size

def main():
    if check_port_in_use(port="5572"):
        return 0
    else:
        args = parse_args()
        # select no-empty folder
        source_path = ""
        destination_path = ""
        for i in range(len(SOURCE_PATH_LIST)):
            if get_file_size(SOURCE_PATH_LIST[i]) > 1:
                source_path = SOURCE_PATH_LIST[i]
                destination_path = DESTINATION_PATH_LIST[i]

        if args.source_path and args.destination_path:
            source_path = args.source_path
            destination_path = args.destination_path

        if source_path == "":
            return 0

        # create rclone cmd
        rclone_cmd = "/usr/bin/rclone --config /root/.config/rclone/rclone.conf move --drive-server-side-across-configs --rc --rc-addr=\"127.0.0.1:5572\" -vP --ignore-existing "
        rclone_cmd += "--tpslimit {} --transfers {} --bwlimit {} --drive-chunk-size 32M ".format(TPSLIMIT, TRANSFERS, BWLIMIT)
        rclone_cmd += "--drive-acknowledge-abuse --log-file=\"/root/log_rclone.txt\" \"{}\" \"{}\" ".format(source_path, destination_path)
        # exclude unfinished qbittorrent files
        rclone_cmd += "--exclude \"*.!qB\"  & "
        print(rclone_cmd)
        subprocess.check_call(rclone_cmd, shell=True)

if __name__ == "__main__":
    main()
