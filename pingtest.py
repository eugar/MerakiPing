import meraki
import platform    # For getting the operating system
import subprocess

#returns true if host responds to ping
def ping(host):

    param = '-n' if platform.system().lower()=='windows' else '-c'

    # building the command with 1 packet
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0

def main():
    API_KEY = '' # Meraki dashboard API key here

    dashboard = meraki.DashboardAPI(API_KEY)

    offline_devices = []

    organization_id = '' # Your organization ID here

    response = dashboard.organizations.getOrganizationDevicesStatuses(
        organization_id, total_pages='all', statuses="offline", productTypes="wireless"
    )

    counter = 0
    repeater = 0

    for device in response:
        counter += 1
        if (device['lanIp']):
            if ping(device['lanIp']):
                print()
                pass
            else:
                offline_devices.append(device)
        else:
            print("\n\nDevice in repeater mode:")
            print(device)
            repeater += 1



    print(f"\n\nMeraki shows {counter} devices offline")
    print(f"There are actually {offline_devices.__len__()} devices offline")

    if repeater > 0:
        print(f"There are {repeater} devices in repeater mode")

    if offline_devices.__len__() > 0:
        print(f"These are the devices that don't respond to ping: \n")

    for d in offline_devices:
        print(d)

if __name__ == '__main__':
    main()
    print(f'\nScript complete')