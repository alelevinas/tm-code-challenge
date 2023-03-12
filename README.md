# Thought Machine SRE Code Challenge

## Requirements

- python 3.7+
- [optional] virtualenv
    - `pip install virtualenv`

## Installation

This is as simple as `pip install . `

### Virtual Env

If you don't want to install libraries globally, you can create a local virtualenv.

```bash
virtualenv venv
source .venv/bin/activate
pip install .
```

## Usage

### Services per server

```
(venv) ➜  SRE_take_home_challenge git:(main) ✗ cli_devops --cp-url "http://localhost:8081" services
| IP          | Service            | Status    | CPU     | Memory   |
|-------------+--------------------+-----------+---------+----------|
| 10.58.1.31  | UserService        | Healthy   | 3.00%   | 43.00%   |
| 10.58.1.138 | GeoService         | Healthy   | 21.00%  | 42.00%   |
| 10.58.1.117 | IdService          | Healthy   | 32.00%  | 40.00%   |
| 10.58.1.46  | AuthService        | Healthy   | 62.00%  | 49.00%   |
| 10.58.1.99  | StorageService     | Healthy   | 30.00%  | 6.00%    |
| 10.58.1.128 | PermissionsService | Healthy   | 1.00%   | 0.00%    |
| 10.58.1.110 | TimeService        | Healthy   | 48.00%  | 7.00%    |
| 10.58.1.2   | TimeService        | Healthy   | 40.00%  | 27.00%   |
| 10.58.1.135 | TicketService      | Unhealthy | 93.00%  | 31.00%   |
| 10.58.1.88  | AuthService        | Healthy   | 35.00%  | 52.00%   |
| 10.58.1.108 | GeoService         | Healthy   | 19.00%  | 29.00%   |
| 10.58.1.63  | MLService          | Unhealthy | 48.00%  | 97.00%   |
```

### Service Status
```
(venv) ➜  SRE_take_home_challenge git:(main) ✗ cli_devops status --service MLService                
| Service   | Status   | CPU    | Memory   |
|-----------+----------+--------+----------|
| MLService | Healthy  | 49.19% | 36.06%   |
```

### Unhealthy Services
```
(venv) ➜  SRE_take_home_challenge git:(main) ✗ cli_devops unhealthy-services
| Service            |   Healthy servers |
|--------------------+-------------------|
| GeoService         |                 1 |
| UserService        |                 1 |
```

### Periodically track Service
```
Servers for service 'UserService'

Sun Mar 12 09:45:43 2023

| IP          | Service     | Status    | CPU   | Memory   |
|-------------+-------------+-----------+-------+----------|
| 10.58.1.143 | UserService | Healthy   | 11.0% | 11.0%    |
| 10.58.1.141 | UserService | Healthy   | 63.0% | 52.0%    |
| 10.58.1.98  | UserService | Unhealthy | 92.0% | 40.0%    |
| 10.58.1.131 | UserService | Unhealthy | 90.0% | 95.0%    |
```

## Design

This basic CLI is organized in 3 main files.

- *main.py*: Which is responsible for user input and presentation. 
    - I leverage the ["Click"](asd) framework to simplify CLI standard operations like providing a `--help` or extracting and casting of parameters.
    - I also made use of the ["tabulate"](url) library for pretty printing of the resulting tables getting some very clean code with just a few lines.

- *cpx_client.py*: Which is responsible for fetching data from the cps server.
    - This is a very basic client whith only two GET operations.

- *commands.py*: Which is responsible for querying, filtering, organizing and returning the data to the main routine.


## Asumptions

- This CLI will be packed and distributed to employee laptops and machines

- A service is considered unhealthy when either its CPU usage or memmory usage is > 90%
    - This can be configurable with the `--cpu-threshold` and `--mem-threshold` options.


## trade-offs and future improvements

- Configuration: Since I assume this CLI will be packaged and distributed to employees machines, a configuration file would be unusable. That's why we should allow as many options as necessary to it. Since it's a fire-and-forget CLI, and for simplicity, I just added the configuration to a global dictionary. I wouldn't do this in a stateful application and would make them immutable.

- Client: For simplicity sake, the client is just that basic and simple. If there were to be more intense usage of it, like multiple types of requests, with more options, authentication configuration, sessions, SSL, etc. I'd probably wrap it up under a class that can be used in commands.py

- Concurrency: Since the most common usage is to make multiple "URL/{ip}" requests. Concurrency is a good performance improver candidate. I initially went for asyncio, but since cpx_client.py is just secuentially responding to every request, the event loop got really slow. I went for a localized multithreading routine instead. In a real world scenario, with a cloud provider service that can handle multiple requests at a time, I'd have gone for async/await in general and would leave multithreading just to simple, specific heavy operations.

- Logging: is limited and only local. On internal devops tools I like showing the full stack trace when there's an exception. If this CLI would be used by a good amount of engineers, I'd also add some external logging to gather data on its usage (and most common errors/bugs)

- Presentation / Data handling: I know I'm sometimes loosing a bit of performance by casting CPU/mem percentages to float and then to a string again, but I prefer that tradeoff for cleaner code by having typed data structures to do the filtering and calculations without having to cast values many times.