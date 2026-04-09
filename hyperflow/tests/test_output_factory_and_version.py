from hyperflow.memory.status_report import build_status_report
from hyperflow.output.factory import build_output_object
from hyperflow.version import get_version


def test_factory_preserves_supported_semantic_kinds() -> None:
    base_kwargs = dict(
        intent="documentation",
        mode="standard",
        summary="ok",
        confidence="high",
        observer_status="OK",
        next_step="none",
    )

    spec_output = build_output_object(output_type="spec", **base_kwargs)
    map_output = build_output_object(output_type="map", **base_kwargs)
    json_output = build_output_object(output_type="json", **base_kwargs)

    assert spec_output.kind == "spec"
    assert map_output.kind == "map"
    assert json_output.kind == "json"


def test_status_report_uses_runtime_version_source() -> None:
    report = build_status_report(limit_runs=1)
    assert report["version"] == get_version()

