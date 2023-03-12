from cli_devops.cpx_client import get_servers, get_server_status
import requests_mock
import unittest
from requests.exceptions import RequestException
from cli_devops.utils import Status, ServerStatus, CONFIG

SERVERS = [
    "10.58.1.19",
    "10.58.1.32",
    "10.58.1.54",
    "10.58.1.9",
    "10.58.1.60",
    "10.58.1.12",
    "10.58.1.4",
    "10.58.1.137",
    "10.58.1.139",
    "10.58.1.144",
    "10.58.1.39",
]

SERVER_STAT = {"cpu": "11%", "memory": "6%", "service": "RoleService"}

BASE_URL = "http://localhost:8081"


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        CONFIG["CP_URL"] = BASE_URL
        CONFIG["CPU_THRESHOLD"] = 90
        CONFIG["MEM_THRESHOLD"] = 90

    def test_get_servers(self):
        with requests_mock.Mocker() as m:
            m.get(f"{BASE_URL}/servers", json=SERVERS)
            assert get_servers(f"{BASE_URL}") == SERVERS

    def test_get_servers_not_ok(self):
        with requests_mock.Mocker() as m:
            m.get(f"{BASE_URL}/servers", status_code=404)
            with self.assertRaises(RequestException):
                get_servers(f"{BASE_URL}")

    def test_get_server_status_to_type(self):
        with requests_mock.Mocker() as m:
            ip = SERVERS[0]
            m.get(f"{BASE_URL}/{ip}", json=SERVER_STAT)

            stat = get_server_status(f"{BASE_URL}", ip)

            assert stat == ServerStatus(
                ip, SERVER_STAT["service"], Status.HEALTHY, 11, 6
            )
