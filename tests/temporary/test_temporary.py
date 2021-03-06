from pathlib import Path

import miniflask  # noqa: E402

mf = miniflask.init(
    module_dirs=str(Path(__file__).parent / "modules"),
)


def test_temporary():
    mf.run(modules=["dosomething"], argv=[])
