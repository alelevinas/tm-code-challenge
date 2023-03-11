from typing import List
import requests

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

from cli_devops.utils import Status, ServiceStatus, ServerStatus, resolve_status


def get_servers(base_url: str) -> List[str]:
    with requests.get(f"{base_url}/servers") as r:
        return r.json()


def get_server_status(base_url: str, ip: str) -> ServerStatus:
    """
    Args:
        ip (str): gets stats from server

    Returns:
        _type_: {"cpu":"61%","service":"UserService","memory":"4%"}
    """
    with requests.get(f"{base_url}/{ip}") as r:
        stats = r.json()
        cpu = float(stats['cpu'].strip('%'))
        memory = float(stats['memory'].strip('%'))
        status = resolve_status(cpu, memory)

        return ServerStatus(ip, stats['service'], status, cpu, memory)


def get_servers_stats(base_url: str) -> List[ServerStatus]:
    ips = get_servers(base_url)
    stats = []
    with ThreadPoolExecutor(5) as executor:
        # download each url and save as a local file
        futures = [executor.submit(
            get_server_status, base_url, ip) for ip in ips]
        # process each result as it is available
        for future in as_completed(futures):
            # get the downloaded url data
            stats.append(future.result())
    return stats
