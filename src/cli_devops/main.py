import time
import click
import cli_devops.commands as commands
from tabulate import tabulate
from cli_devops.utils import CONFIG


DEFAULTS = {
    "CP_URL": "http://localhost:8081",
    "CPU_THRESHOLD": 90,
    "MEM_THRESHOLD": 90,
}

SERVICE_HEADERS = ["Service", "Status", "CPU", "Memory"]
SERVER_HEADERS = ["IP"] + SERVICE_HEADERS


def _get_styled_status(status: commands.Status):
    return click.style(
        f"{status}", fg="green" if status is commands.Status.HEALTHY else "red"
    )


def health_check():
    try:
        commands.connection_check()
    except:
        print(
            "This CLI can't continue without access to the cpx server data. Please check command options and try again"
        )
        exit()


@click.group()
@click.option(
    "--cp-url", default=DEFAULTS["CP_URL"], help="Base URL of the cloud providder"
)
@click.option(
    "--cpu-threshold",
    default=DEFAULTS["CPU_THRESHOLD"],
    help="CPU threshold to determine an unhealthy service that could scale",
)
@click.option(
    "--mem-threshold",
    default=DEFAULTS["MEM_THRESHOLD"],
    help="RAM Memory threshold to determine an unhealthy service that could scale",
)
def cli(cp_url: str, cpu_threshold: int, mem_threshold: int):
    """CLI to query Cloud Provider X and check status of our services"""
    CONFIG["CP_URL"] = cp_url
    CONFIG["CPU_THRESHOLD"] = cpu_threshold
    CONFIG["MEM_THRESHOLD"] = mem_threshold
    health_check()


@cli.command()
def services():
    """Print running services to stdout (similar to the table below)"""
    servers = commands.get_servers_stats(CONFIG["CP_URL"])

    servers = [
        [
            s.ip,
            s.service,
            _get_styled_status(s.status),
            f"{s.cpu:.2f}%",
            f"{s.mem:.2f}%",
        ]
        for s in servers
    ]

    click.echo(tabulate(servers, SERVER_HEADERS, tablefmt="orgtbl"))


@cli.command()
@click.option("--service", default=None, help="Only for a specific service")
def status(service):
    """Print out average CPU/Memory of services of the same type"""
    services_status = commands.status(service)
    services = [
        [
            s.service,
            _get_styled_status(s.status),
            f"{s.avg_cpu:.2f}%",
            f"{s.avg_mem:.2f}%",
        ]
        for s in services_status
    ]

    click.echo(tabulate(services, SERVICE_HEADERS, tablefmt="orgtbl"))


@cli.command()
def unhealthy_services():
    """Flag services which have fewer than 2 healthy instances running"""
    services = commands.unhealthy_services()
    headers = ["Service", "Healthy servers"]

    click.echo(tabulate(services, headers, tablefmt="orgtbl"))


@cli.command()
@click.option("--interval", default=3, help="Interval between queries")
@click.argument("service")
def service_track(service, interval):
    """Have the ability to track and print CPU/Memory of all instances of a given service over
    time (until the command is stopped, e.g. ctrl + c)."""
    servers = commands.service_track(service)
    while True:
        click.clear()
        click.echo(f"Servers for service '{service}'\n")
        click.echo(f"{time.asctime()}\n")

        servers = [
            [s.ip, s.service, _get_styled_status(s.status), f"{s.cpu}%", f"{s.mem}%"]
            for s in servers
        ]

        click.echo(tabulate(servers, SERVER_HEADERS, tablefmt="orgtbl"))

        time.sleep(interval)
        servers = commands.service_track(service)
