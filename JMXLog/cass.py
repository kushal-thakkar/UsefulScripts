# Inspired from here: http://rostislav-matl.blogspot.in/2011/02/monitoring-tomcat-with-jmxterm.html
import time
import pexpect

all_hosts = [line.strip() for line in open('hosts.txt')]

all_commands = [line.strip() for line in open('attributes.txt')]

output_file = open("log.txt","w")

while True:
   for host in all_hosts:
      connection = host
      connection_timeout = 2
      
      try:
         jmxterm = pexpect.spawn("java -jar jmxterm-1.0-alpha-4-uber.jar")
         jmxterm.expect_exact("$>") # got prompt, we can continue
         jmxterm.sendline("open " + connection)
         jmxterm.expect_exact("#Connection to "+connection+" is opened")

         print_string = "["+time.ctime()+"] " + "host=" + connection.split(".")[0] + ","
         #print "["+time.ctime()+"]", "host=" + connection.split(".")[0] + ",",
         for command in all_commands:
            jmxterm.sendline(command)

            response_lines = []
            response_lines.append(jmxterm.readline())
            response_lines.append(jmxterm.readline())
            response_lines.append(jmxterm.readline())
            response_lines.append(jmxterm.readline())

            result = response_lines[3].replace(";"," ").strip().split(" ")
            del result[1]
            name,value = result

            print_string += name.strip() + "=" + value.strip() + ","
            #print print_string,

         #print
         output_file.write(print_string + "\n")
         output_file.flush()
         jmxterm.sendline("quit")
      except:
         pass

   time.sleep(200)
