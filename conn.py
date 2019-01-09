#!/usr/bin/python3.6

import para
import urllib.request as url_req
import urllib.error
import subprocess
import os, signal

def establish_conn():
   
   subprocess.call(["/usr/bin/screen", "-d", "-m", "-S", "conn", os.path.join(para.home_path, 'tunn')])

def terminate_conn(screen_pid, ssh_pid):

   if not ssh_pid == 0:
      os.kill(ssh_pid, signal.SIGTERM)
   if not screen_pid == 0:
      os.kill(screen_pid, signal.SIGTERM)

def check_conn_establish():
   screen_pid, ssh_pid = get_pids()

   if screen_pid & ssh_pid == 0:
      if not screen_pid == 0 or not ssh_pid == 0:
         # something is wrong
         terminate_conn(screen_pid, ssh_pid)
      return False
   else:
      return True
  
def get_pids():
   screen_pid = 0
   ssh_pid = 0

   with subprocess.Popen(['/usr/bin/ps', 'x'], stdout=subprocess.PIPE) as processes:
      lines = list(processes.stdout)
      header = lines[0]
      pid_pos = header.decode().find('PID')
      comm_pos = header.decode().find('COMMAND')
      for line in lines[1:]:
         comm = line[comm_pos:].decode()
         pid = line[:pid_pos + 3].decode() 
         if comm.startswith('/usr/bin/SCREEN -d -m -S'):
            screen_pid = pid

         if comm.startswith('/usr/bin/ssh -R'):
            ssh_pid = pid
      print(screen_pid, ssh_pid)
      return int(screen_pid), int(ssh_pid)

def check_conn_flag():
   url = 'http://' + para.ip + '/flag'

   try:
      line = url_req.urlopen(url)
   except urllib.error.URLError as E:
      print(E.reason)
   else:
      if line.startswith('1'):
         if not check_conn_establish():
            establish_conn()
      else:
         screen_pid, ssh_pid = get_pids()
         terminate_conn(screen_pid, ssh_pid) 

if __name__ == '__main__':
   print('hi')
   #check_conn_flag()
   #check_conn_establish()
   #establish_conn()
   screen_pid, ssh_pid = get_pids()
   #terminate_conn(screen_pid, ssh_pid) 
