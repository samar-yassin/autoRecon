#!/usr/bin/python

import sys, getopt,os,requests

#raven IP : 192.168.53.130

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
         print("\n\nrunning nmap...")
         stream = os.popen(command)
         nmapOutput = stream.read()
         
         #console output
         cOutput='';

         #printing out the open ports
         for item in nmapOutput.split("\n"):
            if "open" in item:
               cOutput+=item.strip()+"\n"
         if(cOutput != ''):
            print("\n\n\nopen ports :")
            print (cOutput)
         else :
            print("\n\n\nno open ports")
            sys.exit()

         #check port 80
         if "80" in cOutput:
            command = "dirb http://"+ip
            print("\n\nrunning dirb...")
            stream = os.popen(command)
            dirbOutput = stream.read()
            print("\n\n\ndirb result :\n")
            cOutput='';
            for item in dirbOutput.split("\n"):
               if "==> DIRECTORY: " in item :
                  cOutput+=item.strip()+"\n"

            if(cOutput != ''):
               print("Directories :")
               print (cOutput)


            #check if there's wordpress running
            if "wordpress" in dirbOutput:
               print("\n\nrunning wpscan...")
               command = "wpscan --url "+ip+"/wordpress/ -e --update"
               stream = os.popen(command)
               wpscan = stream.read()
               print("\n\n\nwordpress result :")
               print(wpscan)

            #check robots.txt file
            url = "http://"+ip+"/robots.txt"
            res = requests.get(url)
            if(res.status_code == 200):
               print ("\n\n\nrobots.txt file :")
               print (res.text);



if __name__ == "__main__":
   main(sys.argv[1:])
