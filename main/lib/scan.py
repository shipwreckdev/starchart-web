import nmap


def Scan(addresses, scan_args, port_range):
    """Take the list of subject addresses and options and perform nmap scans against targets."""

    nm = nmap.PortScanner()

    report = []

    for a in addresses:
        nm.scan(hosts=a, arguments=scan_args, ports=port_range)

        open_port_list = []

        for host in nm.all_hosts():
            individual_scan_results = []

            if nm[host].hostname() != '':
                hostname = nm[host].hostname()
                state = nm[host].state()

            for proto in nm[host].all_protocols():
                lport = sorted(nm[host][proto].keys())

                # Build a list of open ports based on discovery.
                for port in lport:
                    port_state = nm[host][proto][port]['state']

                    if port_state == 'open':
                        open_port_list.append(port)

            # Only scan the open ports.
            noports = False
            port_info = []

            if len(open_port_list) != 0:
                for open_port in open_port_list:
                    svc = nm[host][proto][open_port]['name']
                    port = str(open_port)
                    port_state = port_state

                    port_info.append(
                        dict({"service": svc, "port": port, "state": port_state}))
            else:
                noports = True

            individual_scan_results.append(dict(
                {'port_info': port_info, 'noports': noports}))

        report.append(dict({"address": a, "details": individual_scan_results}))

    return report
