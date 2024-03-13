import ansible_runner
import json


def load_inventory_and_ping_hosts(inventories):
    # Get inventory details
    response, error = ansible_runner.interface.get_inventory(action='list', inventories=inventories, quiet = True)

    if error:
        print(f"Error fetching inventory: {error}")
        return

    # Parse the JSON response into a dictionary
    try:
        inventory_data = json.loads(response)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        return

    # Extract host details from the inventory data
    all_hosts = inventory_data.get('_meta', {}).get('hostvars', {})
    groups = inventory_data.get('all', {}).get('children', [])

    # Print names, IP addresses, and group names of all hosts
    for group in groups:
        print(f"Group: {group}")
        hosts = inventory_data.get(group, {}).get('hosts', [])
        for host in hosts:
            details = all_hosts.get(host, {})
            print(f"  Host: {host}")
            print(f"    IP Address: {details.get('ansible_host', 'N/A')}")
            print(f"    Ansible Port: {details.get('ansible_port', 'N/A')}")
            print(f"    Ansible User: {details.get('ansible_user', 'N/A')}")

            # Ping the host
            ping_response= ansible_runner.interface.run(host_pattern=host, module='ping', quiet = True)

            print("The ping response to the host", host, "was:", ping_response.status)
            print()



# Define the list of inventory host paths
inventory_paths = ['/workspaces/ensf400-lab5-ansible/hosts.yml']  # Update with actual inventory paths

# Load inventory and ping hosts
load_inventory_and_ping_hosts(inventory_paths)
