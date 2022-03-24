from __future__ import annotations

import asyncio
import typing

from ctc import spec
from . import yields_spec


async def async_get_fei_yield_data(
    block_numbers: typing.Sequence[spec.BlockNumberReference],
) -> typing.Mapping[str, yields_spec.YieldSourceData]:

    # get yield sources
    yields_sources = get_yields_sources()

    # get data
    coroutines = []
    for yield_source in yields_sources:
        coroutine = yield_source(block_numbers=block_numbers)
        coroutines.append(coroutine)
    yield_datas = await asyncio.gather(*coroutines)

    # package data
    return {
        yield_datum['name']: yield_datum
        for yield_data in yield_datas
        for name, yield_datum in yield_data.items()
    }


def get_yields_sources() -> list[
    typing.Callable[
        [typing.Mapping[str, spec.BlockNumberReference]],
        yields_spec.YieldSourceData,
    ]
]:

    from .yields_sources import aave_yields
    from .yields_sources import compound_yields
    from .yields_sources import curve_yields
    from .yields_sources import g_uni_yields
    # from .yields_sources import rari_yields

    yield_source_groups = [
        aave_yields.async_get_fei_yield_data,
        compound_yields.async_get_fei_yield_data,
        curve_yields.async_get_fei_yield_data,
        g_uni_yields.async_get_fei_yield_data,
        # rari_fuse_yields.async_get_fei_yield_data,
    ]

    return yield_source_groups
