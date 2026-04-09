from __future__ import annotations

import json
from pathlib import Path

import hyperflow.config as config_module


_CACHE_FNS = ['load_json_config']



def _clear_config_caches() -> None:
    for name in _CACHE_FNS:
        fn = getattr(config_module, name)
        if hasattr(fn, 'cache_clear'):
            fn.cache_clear()



def test_env_config_dir_has_priority(tmp_path: Path, monkeypatch) -> None:
    custom_dir = tmp_path / 'custom-configs'
    custom_dir.mkdir(parents=True, exist_ok=True)
    (custom_dir / 'edde-core.json').write_text(
        json.dumps({'schema': 'hyperflow/edde-core/test-env', 'modes': []}),
        encoding='utf-8',
    )

    monkeypatch.setenv('HYPERFLOW_CONFIG_DIR', str(custom_dir))
    _clear_config_caches()
    try:
        assert config_module.get_edde_core_config()['schema'] == 'hyperflow/edde-core/test-env'
    finally:
        monkeypatch.delenv('HYPERFLOW_CONFIG_DIR', raising=False)
        _clear_config_caches()
