#!/usr/bin/python3.6

import para
import urllib.request as url_req
import urllib.error
import subprocess

def establish_conn():

   pass

def terminate_conn():

   pass


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
      print(pid_pos, comm_pos)
      for line in lines[1:]:
         comm = line[comm_pos:].decode()
         pid = line[:pid_pos + 3].decode() 
         if comm.startswith('SCREEN -dmS'):
            screen_pid = pid

         if comm.startswith('ssh -R'):
            ssh_pid = pid

      return screen_pid, ssh_pid

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
   check_conn_establish()
