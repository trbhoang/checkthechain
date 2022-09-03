from __future__ import annotations

import typing

from ctc import spec
from .. import hashes
from .. import formats
from . import secp256k1_utils

if typing.TYPE_CHECKING:
    from typing_extensions import Literal


def sign_text_message(
    message: str,
    *,
    private_key: spec.Data,
    mode: Literal['eth_sign', 'personal_sign'],
    chain_id: int | None = None,
) -> tuple[int, int, int]:

    message_hash = create_text_message_hash(
        message=message,
        mode=mode,
    )

    return sign_message_hash(
        message_hash=message_hash,
        private_key=private_key,
        chain_id=chain_id,
    )


def sign_data_message(
    message: spec.Data,
    *,
    private_key: spec.Data,
    mode: Literal['eth_sign', 'personal_sign'],
    chain_id: int | None = None,
) -> tuple[int, int, int]:

    message_hash = create_data_message_hash(
        message=message,
        mode=mode,
    )

    return sign_message_hash(
        message_hash=message_hash,
        private_key=private_key,
        chain_id=chain_id,
    )


def sign_message_hash(
    message_hash: spec.Data,
    *,
    private_key: spec.Data,
    chain_id: int | None = None,
) -> tuple[int, int, int]:

    message_hash = formats.convert(message_hash, 'binary')

    # compute signature
    private_binary = formats.convert(private_key, 'binary')
    v, r, s = secp256k1_utils.ecdsa_raw_sign(
        message_hash,
        priv=private_binary,
    )

    # alter v with chain_id
    if chain_id is not None:
        v = v - 27 + chain_id * 2 + 35

    return v, r, s


def create_text_message_hash(
    message: str,
    mode: Literal['eth_sign', 'personal_sign'],
) -> bytes:

    # add prefix
    if mode == 'eth_sign':
        full_message = message
    elif mode == 'personal_sign':
        full_message = (
            '\x19Ethereum Signed Message:\n'
            + str(len(message.encode()))
            + message
        )
    else:
        raise Exception('unrecognized signing mode: ' + str(mode))

    # compute message hash
    message_hash = hashes.keccak_text(full_message, output_format='binary')

    return message_hash


def create_data_message_hash(
    message: spec.Data,
    mode: Literal['eth_sign', 'personal_sign'],
) -> bytes:

    message = formats.convert(message, 'binary')

    # add prefix
    if mode == 'eth_sign':
        full_message = message
    elif mode == 'personal_sign':
        prefix = '\x19Ethereum Signed Message:\n' + str(len(message))
        full_message = prefix.encode() + message
    else:
        raise Exception('unrecognized signing mode: ' + str(mode))

    # compute message hash
    message_hash = hashes.keccak(full_message, output_format='binary')

    return message_hash
