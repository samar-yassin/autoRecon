#!/usr/bin/python

import sys, getopt,os,requests

def main(argv):
   try:
      opts, args = getopt.getopt(argv,"h:i:")
   except :
      print 'usage : scan.py -i <IP>'
      sys.exit()

   for opt, arg in opts:
      if opt == '-h':
         print 'usage : scan.py -i <IP>'
         sys.exit()  
      elif opt  == '-i':
         ip=arg;
         #first command to run "nmap"
         command = "nmap -A "+ip;
         stream = os.popen(command)
         nmapOutput = stream.read()
         
         #console output
         cOutput='';

         #printing out the open ports
         for item in nmapOutput.split("\n"):
            if "open" in item:
               cOutput+=item.strip()+"\n"
         if(cOutput != ''):
            print("open ports :")
            print (cOutput)
         else :
            print("no open ports")
            sys.exit()

         #check port 80
         if "80" in cOutput:
            command = "dirb http://"+ip
            stream = os.popen(command)
            scan80 = stream.read()

            #check if there's wordpress running
            if "wordpress" in scan80:
               command = "wpscan --url "+ip+"/wordpress/ -e"
               stream = os.popen(command)
               wpscan = stream.read()
               print("wordpress scan :")
               print(wpscan)

            #check robots.txt file
            url = "http://"+ip+"/robots.txt"
            res = requests.get(url)
            if(res.status_code == 200)
               print res.text;



if __name__ == "__main__":
   main(sys.argv[1:])
