from django.shortcuts import render


def about(request):
    return render(request, 'main/about.html')


def aws(request):
    from .lib import ec2 as ec2
    from .lib import scan as Scanner

    instances = ec2.InstancePublicIPs()
    instances_count = len(instances)

    return render(request, 'main/aws.html', {'instances': instances, 'instances_count': instances_count})


def inspect(request):
    from .lib import ec2 as ec2
    from .lib import scan as Scanner

    if request.GET.get('ec2'):
        data = ec2.Instances()
        resource_types = 'ec2'

    if request.GET.get('vpc'):
        idata = ec2.Instances()

        for d in idata:
            vpc_list = []
            vpc_list.append(d['vpc'])

        data = ec2.VPCDetails(vpc_list)
        resource_types = 'vpc'

    return render(request, 'main/inspect.html', {'data': data, 'resource_types': resource_types})


def main(request):
    return render(request, 'main/main.html')


def scan(request):
    from .lib import ec2 as ec2
    from .lib import scan as Scanner

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
