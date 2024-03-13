import os
import ansible_runner
import requests

# Define the inventory file
inventory = "/workspaces/ensf400-lab5-ansible/hosts.yml"

# Define the playbook file
playbookpath = "/workspaces/ensf400-lab5-ansible/hello.yml"

r = ansible_runner.run(playbook=playbookpath, quiet=True)
print("{}: {}".format(r.status, r.rc))
# successful: 0
for each_host_event in r.events:
    print(each_host_event['event'])

# Read and verify response from NodeJS servers
nodejs_ports = ['3000',"3001", "3002"]  # Replace with actual IP addresses of your NodeJS servers

for server_ip in nodejs_ports:
    url = f"http://0.0.0.0:{server_ip}/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Response from {server_ip}: {response.text}")
        else:
            print(f"Failed to get response from {server_ip}")
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")

