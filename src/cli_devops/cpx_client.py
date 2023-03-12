from typing import List
import requests
from requests.exceptions import RequestException, Timeout

import logging

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

from cli_devops.utils import ServerStatus, resolve_status


def get_servers(base_url: str) -> List[str]:
    try:
        with requests.get(f"{base_url}/servers") as r:
            if not r.ok:
                r.raise_for_status()
            return r.json()
    except Timeout as e:
        logging.error("The request timed out", exc_info=True)
        raise e
    except RequestException as e:
        logging.error(
            "There was an error retrieving data from the server", exc_info=True
        )
        raise e


def get_server_status(base_url: str, ip: str) -> ServerStatus:
    """
    Args:
        ip (str): gets stats from server

    Returns:
        ServerStatus: that server's stats
    """
    try:
        with requests.get(f"{base_url}/{ip}") as r:
            stats = r.json()
            cpu = float(stats["cpu"].strip("%"))
            memory = float(stats["memory"].strip("%"))
            status = resolve_status(cpu, memory)

            return ServerStatus(ip, stats["service"], status, cpu, memory)
    except Timeout as e:
        logging.error("The request timed out", exc_info=True)
    except RequestException as e:
        logging.error(
            "There was an error retrieving data from the server", exc_info=True
        )


def get_servers_stats(base_url: str) -> List[ServerStatus]:
    """Fetches all servers' stats

    Args:
        base_url (str)

    Returns:
        List[ServerStatus]
    """
    ips = get_servers(base_url)
    stats = []
    with ThreadPoolExecutor(5) as executor:
        futures = [executor.submit(get_server_status, base_url, ip) for ip in ips]
        for future in as_completed(futures):
            stats.append(future.result())
    return stats
