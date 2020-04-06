from django.shortcuts import render
from .lib import ec2 as ec2
from .lib import scan as Scanner


def about(request):
    return render(request, 'main/about.html')


def aws(request):
    return render(request, 'main/aws.html')


def inspect(request):
    instances = ec2.Instances()

    return render(request, 'main/inspect.html', {'instances': instances})


def main(request):
    return render(request, 'main/main.html')


def scan(request):
    if request.GET.get('public_ip'):
        instances = ec2.InstancePublicIPs()
        scan_type = 'public'

        ips = []

        for i in instances:
            ips.append(i['ip'])
    elif request.GET.get('private_ip'):
        instances = ec2.InstancePrivateIPs()
        scan_type = 'private'

        ips = []

        for i in instances:
            ips.append(i['ip'])

    nmap_options = request.GET.get('nmap_options')
    port_range = request.GET.get('port_range')

    report = Scanner.Scan(ips, nmap_options, port_range)

    return render(request, 'main/scan.html', {'instances': instances, 'scan_type': scan_type, 'port_range': port_range, 'nmap_options': nmap_options, 'report': report})


def usage(request):
    return render(request, 'main/usage.html')
