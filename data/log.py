import subprocess

# Ask the user for input
host = input("Enter a node or a list of nodes to ping: ")	
output = ''

# The user provided a list of nodes
if len(host.split(',')) > 1:
	for h in host.split(','):
		output += str(subprocess.Popen(['ping', '-c 30', h], stdout=subprocess.PIPE).communicate()[0]) + ' \n '
# The user provided a single node
else:
	output += str(subprocess.Popen(['ping', '-c 10', host], stdout=subprocess.PIPE).communicate()[0]) + ' \n '

# Write the results on file
with open('ping.log', 'a') as log:
	log.write(output)
