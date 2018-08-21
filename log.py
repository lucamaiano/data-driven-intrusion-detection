# Import the module
import subprocess

# Ask the user for input
host = input("Enter a host to ping: ")	

# Set up the echo command and direct the output to a pipe

output = subprocess.Popen(['ping', '-c 2', host], stdout=subprocess.PIPE).communicate()

print(output)