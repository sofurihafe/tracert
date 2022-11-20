import sys
import re
from scapy.layers.inet import (IP, ICMP)
from scapy.sendrecv import (sr1)

ADDRESS_REGEX = "[a-zA-Z]+.[a-zA-Z]+"
SUPPORTED_FLAGS = ["-h"]
TIMEOUT = 5
MAXIMUM_HOPS = 30
HELP = """
   tracert.py <optional flag> <optional value> target
   
   See the usage examples below:
   1. tracert.py duckduckgo.com
   2. tracert.py -h 5 duckduckgo.com
"""
ERRORS = {
    0: "Abort: unsupported address type",
    1: "Abort: unsupported flag type",
    2: "Abort: unsupported arguments number",
    3: "Abort: value has a non-integer type"
}


def _exit_with_error(error_id):
    raise Exception(ERRORS[error_id])


def _check_destination(target: str):
    if not re.search(ADDRESS_REGEX, target):
        _exit_with_error(0)


def _check_flag(flag: str):
    if flag not in SUPPORTED_FLAGS:
        _exit_with_error(1)


def _read_configuration(args: list[str]):
    match len(args):
        case 1:
            print(HELP)
            exit(0)
        case 2:
            (_, target) = args

            _check_destination(target)

            return target, None, None
        case 4:
            (_, flag, value, target) = args

            _check_destination(target)
            _check_flag(flag)

            return target, flag, value
        case _:
            _exit_with_error(2)


def _send_packet_and_get_reply(target: str, ttl: int):
    packet = IP(dst=target, ttl=ttl) / ICMP()
    return sr1(packet, verbose=0, timeout=TIMEOUT)


def _match_reply(target: str, hops_number: int = None):
    hops_number = hops_number if hops_number else MAXIMUM_HOPS
    for i in range(hops_number):
        reply = _send_packet_and_get_reply(target, i)

        if reply is None:
            print(f"{i} timeout")
            continue
        elif reply.type == 0:
            print(f"{i} {reply.src}")
            break
        else:
            print(f"{i} {reply.src}")


def _run_tracert(target: str, flag: str = None, value: str = None):
    match flag:
        case "-h":
            try:
                value = int(value)
            except ValueError:
                _exit_with_error(3)
    _match_reply(target, value)


def _run(args: list[str]):
    _run_tracert(*_read_configuration(args))


if __name__ == '__main__':
    _run(sys.argv)
