from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import re
import sys

credentials = GoogleCredentials.get_application_default()
service = discovery.build('compute', 'v1', credentials=credentials)

if len(sys.argv) >= 4:
    project = sys.argv[1]
    instance = sys.argv[2]
    zone = sys.argv[3]

    # Get instance details
    request = service.instances().get(project=project, zone=zone, instance=instance)
    response = request.execute()

    # Get machine type
    mtype = response['machineType'].split('/')[-1]

    # Get operating system name
    osu = response['disks'][0]['licenses'][0]
    os = osu.split('/')[-1]

    # Get disk size
    dsize = str(response['disks'][0]['diskSizeGb']) + ' GB'

    # Use machine type to get cpu count & memory size
    mrequest = service.machineTypes().get(project=project, zone=zone, machineType=mtype)
    mresponse = mrequest.execute()

    # Get cpu count
    cpu = mresponse['guestCpus']

    # Get memory size
    megabyte = mresponse['memoryMb']
    gigabyte = 1.0 / 1024
    memory = str(gigabyte * megabyte) + ' GB'

    print(f'{project},{instance},{zone},{mtype},{os},{cpu},{memory},{dsize}')
