#!/usr/bin/env python

# input
# -u user -p password -ip ip_address -port ssh_port
# (il file_locale.zip contiene il client da installare e i file di configurazione. alla fine riavvia il servizio)
#
#su win32 sshd installato come servizio (openssh server)

import paramiko
import sys

ip_server = "10.10.0.50"

def parse(r):
	#print("S.O. Windows >> " + r)  #test con un openssh funzionante su windows <-----------
	#print("S.O. Linux >> " + r)
	c = ""
	#al primo contatto scarica la configurazione dal c2 / oppure variante .zip contente il file ossec.conf
	if r.find("Ubuntu") > 0:
		c = "curl -so wazuh-agent-ubuntu.deb http://" + ip_server + "/release && sudo WAZUH_MANAGER='" + ip_server + "' dpkg -i ./azuh-agent-ubuntu.deb"
	if r.find("Windows") > 0:
		c = ".exe"
	#se c non viene valorizzato la funzione chiamante rileva c = "" e termina	
	return c
	


def main():
	try:
		w_username = sys.argv[1]
		w_password = sys.argv[2]
		w_ip = sys.argv[3]
		w_ssh_port = sys.argv[4]
		try:
			print("Connessione in corso....")
			paramiko.util.log_to_file("paramiko.log")
			s = paramiko.SSHClient()
			s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			s.load_system_host_keys()
			s.connect(w_ip, w_ssh_port, w_username, w_password)
			print("Connessione avvenuta")
			
			#primo tentativo cerchiamo windows
			stdin, stdout, stderr = s.exec_command("cat /proc/version")
			response = stdout.readlines()
			r = ""
			
			
			for line in response:
				r += line
			if r == "":
				#se è vuoto significa che ha generato un errore e quindi non è linux like e comunque bisogna provare i windows command
				stdin, stdout, stderr = s.exec_command("cmd /c ver")
				response = stdout.readlines()
				r = ""
				for line in response:
					r += line
				if r == "":
					print("Sistema operativo non rilevato")
					exit()
				else:
					#parsa perchè ha funzionato il comando
					cmd = parse(r)
			else:
				#parsa perchè ha funzionato il comando
				cmd = parse(r)
				
			print(cmd)	
				
				
			
		except:
			print("Errore di connessione")
	except:
		print("-u user -p password -ip ip_address -port ssh_port")
		
	
if __name__ == '__main__':
	main()

