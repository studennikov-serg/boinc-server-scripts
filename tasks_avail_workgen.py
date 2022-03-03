#!/usr/bin/env python
# Copyright (C) Serg, creator of https://rnma.xyz/boinc
import os
import subprocess
import time
import json
import jobs_avail as ja

def batch_metadata():
 j = json.load(open('.metadata.json', 'r'))
 return(j['app_version_num'], j['batch'])
#def write_file(name, content):
# with(f=open(name,mode='w'))
# f.write(content)

def trim_extension_from(name):
 return os.path.splitext(name)[0]

def create_work_commandline(filename):
 name = trim_extension_from(os.path.basename(filename))
 return (f"--wu_name RNM_{name} {filename}")

def to_jobs_commandlines(files):
 return("\n".join(map(create_work_commandline, files)))

def dirmap():
 return(os.scandir('data/input'))

def filteredmap(dm):
 return(filter(lambda f: f is not None and f.name.endswith('.7z') and not f.is_dir() and f.is_file(), dm))

def firstfile():
 try:
  return(next(filteredmap(dirmap()))).name
 except StopIteration:
  return None

def run0(cmd):
 return(subprocess.run(['bash','-c',cmd], check = False).returncode)

def run(cmd, stdin):
 return(subprocess.run(['bash','-c',cmd], check=False, input=stdin.encode()).returncode)

def main():
 while True:
  curdir = os.getcwd()
  os.chdir('..')
  loop_step()
  os.chdir(curdir)
  time.sleep(480)

def loop_step():
 ja_ = ja.jobs_avail()
 if ja_ > 2000:
  return
 arc = firstfile()
 if arc is None:
  print('No archive in input folder, exiting.')
  return(0)

 inp = 'data/input/'
 input_buf = 'data/input-buffer'
 run0(f"7z e -aos {inp}{arc} -o{input_buf}")
 jobcreatelines = to_jobs_commandlines(os.listdir(input_buf))
 #print('asdf'+jobcreatelines+'fdsa')
 #write_file('jtest', f"command lines to create jobs:\n{jobcreatelines}"))
 run0(f"bin/stage_file {input_buf}")
 app_version_num, batch = batch_metadata()
 run(f"bin/create_work --appname rmach --app_version_num {app_version_num} --batch {batch} --continue_on_error --stdin", jobcreatelines)
 os.rename(f"{inp}{arc}", f"__data/input-backup/{arc}")
 print('Clearing input buffer')
 run0(f"rm {input_buf}/*")

if __name__ == "__main__":
 main()
