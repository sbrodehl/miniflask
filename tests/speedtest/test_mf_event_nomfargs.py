from pathlib import Path

import miniflask  # noqa: E402

mf = miniflask.init(
    module_dirs=str(Path(__file__).parent / "modules"),
)


def test_mf_event_nomfargs():
    event = mf.event
    mf.load("modulenomfargs")

    a = 0
    for i in range(10000000):
        a += event.func(42)
