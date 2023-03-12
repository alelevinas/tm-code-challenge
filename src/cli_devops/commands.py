from collections import defaultdict
from typing import List, NamedTuple, Dict
from enum import Enum
import cli_devops.cpx_client as cpx_client
from cli_devops.utils import CONFIG

from cli_devops.utils import Status, ServiceStatus, ServerStatus, resolve_status


def connection_check():
    cpx_client.get_servers(CONFIG['CP_URL'])


def get_servers_stats(url: str) -> List[ServerStatus]:
    """
    Returns a list of servers' information: ip, service, status, cpu, memory
    """
    return cpx_client.get_servers_stats(url)


def status(service: str) -> List[ServiceStatus]:
    """Prints out average CPU/Memory of services of the same type

    Args:
        service (str): [Optional] The service to query for

    Returns:
        List[ServiceStatus]: A list of each services' CPU and Memory averaged
    """
    Stat = NamedTuple('Stat', [('cpu', float), ('mem', float)])

    servers = get_servers_stats(CONFIG['CP_URL'])
    services = defaultdict(list)
    for s in servers:
        if service is not None and service != s.service:
            continue
        services[s.service].append(Stat(s.cpu, s.mem))

    service_stats = []
    for service, data in services.items():
        avg_cpu = sum([x.cpu for x in data]) / len(data)
        avg_mem = sum([x.mem for x in data]) / len(data)
        status = resolve_status(avg_cpu, avg_mem)
        service_stats.append(ServiceStatus(service, status, avg_cpu, avg_mem))

    return service_stats


def unhealthy_services() -> Dict[str, ServerStatus]:
    """Services which have fewer than 2 healthy instances running 

    Returns:
        Dict[str, ServerStatus]: A dictionary with the unhealthy service as a key and a list of all its server's status
    """
    servers = get_servers_stats(CONFIG['CP_URL'])
    healthy_servers_per_service = defaultdict(int)
    for s in servers:
        if s.status is Status.HEALTHY:
            healthy_servers_per_service[s.service] += 1

    # TODO: extraer a conf
    return [(service, n) for service, n in healthy_servers_per_service.items() if n < 100]


def service_track(service) -> List[ServerStatus]:
    """ Get CPU/Memory of all instances of a given service

    Args:
        service (str): [Optional] The service to query for

    Returns:
        List[ServerStatus]: _description_
    """
    servers = get_servers_stats(CONFIG['CP_URL'])
    service_servers = []
    for s in servers:
        if service is not None and service != s.service:
            continue
        service_servers.append(s)

    return service_servers
