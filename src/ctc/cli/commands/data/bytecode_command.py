from __future__ import annotations

import toolcli

from ctc import rpc


def get_command_spec() -> toolcli.CommandSpec:
    return {
        'f': async_bytecode_command,
        'help': 'get raw bytecode stored at address',
        'args': [
            {'name': 'address', 'help': 'address where bytecode is stored'},
        ],
    }


async def async_bytecode_command(address: str) -> None:
    bytecode = await rpc.async_eth_get_code(address)
    print(bytecode)