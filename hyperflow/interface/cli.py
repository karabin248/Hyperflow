import argparse
import json
from pathlib import Path

from hyperflow.checkpoint.history import build_checkpoint_history
from hyperflow.checkpoint.snapshot import save_architecture_snapshot
from hyperflow.runtime_kernel import run
from hyperflow.language.command_builder import build_command
from hyperflow.memory.graph_analytics import analyze_graph
from hyperflow.memory.graph_memory import graph_summary
from hyperflow.memory.graph_reasoning import reason_over_graph
from hyperflow.memory.graph_visualizer import render_graph_ascii, render_graph_mermaid
from hyperflow.memory.self_profile import build_self_profile
from hyperflow.memory.session_memory import SESSION_MEMORY
from hyperflow.memory.status_report import build_status_report
from hyperflow.memory.traces import load_recent_traces
from hyperflow.output.run_payload import serialize_run_payload
from hyperflow.version import get_version
from hyperflow.runtime_paths import get_checkpoint_file
from hyperflow.metadata.worker_stubs import list_live_worker_specs


def _write_text_file(path: str | Path, content: str, *, label: str) -> None:
    target = Path(path)
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    except OSError as exc:
        raise SystemExit(f"Unable to save {label} to {target}: {exc}") from exc


def _print_checkpoint_history(limit: int = 10) -> None:
    history = build_checkpoint_history(limit=limit)

    print("=" * 50)
    print("HYPERFLOW CHECKPOINT HISTORY")
    print("=" * 50)
    print(f"count:          {history['count']}")
    print()

    latest = history["latest"]
    previous = history["previous"]

    print("latest:")
    if latest:
        print(f"  - file: {latest['file_name']}")
        print(f"  - generated_at: {latest['generated_at']}")
        print(f"  - version: {latest['version']}")
        print(f"  - status: {latest['status']}")
        print(f"  - phase: {latest['development_phase']}")
        print(f"  - work_style: {latest['dominant_work_style']}")
    else:
        print("  - none")
    print()

    print("previous:")
    if previous:
        print(f"  - file: {previous['file_name']}")
        print(f"  - generated_at: {previous['generated_at']}")
        print(f"  - version: {previous['version']}")
        print(f"  - status: {previous['status']}")
        print(f"  - phase: {previous['development_phase']}")
        print(f"  - work_style: {previous['dominant_work_style']}")
    else:
        print("  - none")
    print()

    print("timeline:")
    if history["timeline"]:
        for item in history["timeline"]:
            print(
                f"  - {item['file_name']} | {item['generated_at']} | "
                f"{item['status']} | {item['development_phase']} | {item['dominant_work_style']}"
            )
    else:
        print("  - none")
    print()

    print("evolution:")
    for item in history["evolution"]:
        print(f"  - {item}")


def _print_status_report(limit_runs: int = 10) -> None:
    report = build_status_report(limit_runs=limit_runs)

    print("=" * 50)
    print("HYPERFLOW STATUS REPORT")
    print("=" * 50)
    print(f"system:         {report['system_name']}")
    print(f"version:        {report['version']}")
    print(f"status:         {report['status']}")
    print(f"phase:          {report['development_phase']}")
    print(f"work style:     {report['dominant_work_style']}")
    print(f"dominant intent:{' ' if report['dominant_intent'] else ''}{report['dominant_intent']}")
    print(f"dominant mode:  {report['dominant_mode']}")
    print()

    print("core operating kernel:")
    if report["core_operating_kernel"]:
        for item in report["core_operating_kernel"]:
            print(f"  - {item}")
    else:
        print("  - none")
    print()

    print("satellite modes:")
    if report["satellite_modes"]:
        for item in report["satellite_modes"]:
            print(f"  - {item}")
    else:
        print("  - none")
    print()

    print("recent summaries:")
    if report["recent_activity"]["recent_summaries"]:
        for item in report["recent_activity"]["recent_summaries"]:
            print(f"  - {item}")
    else:
        print("  - none")
    print()

    print("reasoning findings:")
    for item in report["reasoning_findings"]:
        print(f"  - {item}")
    print()

    print("recommendations:")
    for item in report["recommendations"]:
        print(f"  - {item}")
    print()

    print("short self-description:")
    print(f"  {report['short_self_description']}")
    print()

    print("narrative summary:")
    print(f"  {report['narrative_summary']}")


def _print_self_profile(limit_runs: int = 10) -> None:
    profile = build_self_profile(limit_runs=limit_runs)

    print("=" * 50)
    print("HYPERFLOW SELF PROFILE")
    print("=" * 50)
    print(f"dominant work style: {profile['dominant_work_style']}")
    print(f"development phase:   {profile['development_phase']}")
    print()

    print("core operating kernel:")
    if profile["core_operating_kernel"]:
        for item in profile["core_operating_kernel"]:
            print(f"  - {item}")
    else:
        print("  - none")
    print()

    print("satellite modes:")
    if profile["satellite_modes"]:
        for item in profile["satellite_modes"]:
            print(f"  - {item}")
    else:
        print("  - none")
    print()

    print("short self-description:")
    print(f"  {profile['short_self_description']}")
    print()

    print("narrative summary:")
    print(f"  {profile['narrative_summary']}")
    print()

    print("reasoning findings:")
    for item in profile["reasoning_findings"]:
        print(f"  - {item}")


def _pretty_print(payload: dict) -> None:
    command = payload["command"]
    result = payload["result"]

    print("=" * 50)
    print("HYPERFLOW COMMAND")
    print("=" * 50)
    print(f"intent:         {command['intent']}")
    print(f"mode:           {command['mode']}")
    print(f"output_type:    {command['output_type']}")
    print(f"intensity:      {command['intensity']}")
    print(f"tokens:         {' '.join(command['tokens'])}")
    print(f"operations:     {', '.join(command['operations'])}")
    print()

    print("=" * 50)
    print("HYPERFLOW RESULT")
    print("=" * 50)
    print(f"summary:        {result['summary']}")
    print(f"confidence:     {result['confidence']}")
    print(f"observer:       {result['observer_status']}")
    print(f"next_step:      {result['next_step']}")
    print()

    print("plan:")
    for step in result["plan"]:
        print(f"  - {step}")

    print()
    print("insights:")
    for item in result["insights"]:
        print(f"  - {item}")

    print()
    print("actions:")
    for item in result["actions"]:
        print(f"  - {item}")


def _print_recent(limit: int = 5) -> None:
    trace_records = load_recent_traces(limit=limit)
    memory_records = SESSION_MEMORY.get_recent(limit=limit)

    print("=" * 50)
    print("HYPERFLOW RECENT RUNS")
    print("=" * 50)

    if trace_records:
        print("[persistent traces]")
        print()

        for item in trace_records:
            print(f"- run_id: {item.get('run_id', '')}")
            print(f"  timestamp: {item.get('timestamp', '')}")
            print(f"  intent: {item.get('intent', '')}")
            print(f"  mode: {item.get('mode', '')}")
            print(f"  observer: {item.get('observer_status', '')}")
            print(f"  confidence: {item.get('confidence', '')}")
            print(f"  summary: {item.get('summary', '')}")
            print()
        return

    if memory_records:
        print("[in-memory session]")
        print()

        for item in memory_records:
            print(f"- run_id: {item.run_id}")
            print(f"  intent: {item.intent}")
            print(f"  mode: {item.mode}")
            print(f"  observer: {item.observer_status}")
            print(f"  summary: {item.summary}")
            print()
        return

    print("No recent records found.")


def _print_graph_summary() -> None:
    summary = graph_summary()

    print("=" * 50)
    print("HYPERFLOW GRAPH MEMORY")
    print("=" * 50)
    print(f"nodes:          {summary['node_count']}")
    print(f"edges:          {summary['edge_count']}")
    print()

    print("node types:")
    for key, value in summary["node_types"].items():
        print(f"  - {key}: {value}")
    print()

    print("top intents:")
    for label, count in summary["top_intents"]:
        print(f"  - {label}: {count}")
    print()

    print("top modes:")
    for label, count in summary["top_modes"]:
        print(f"  - {label}: {count}")
    print()

    print("top operations:")
    for label, count in summary["top_operations"]:
        print(f"  - {label}: {count}")
    print()

    print("recent summaries:")
    for item in summary["recent_summaries"]:
        print(f"  - {item}")


def _print_graph_analytics(limit_runs: int = 10) -> None:
    analytics = analyze_graph(limit_runs=limit_runs)

    print("=" * 50)
    print("HYPERFLOW GRAPH ANALYTICS")
    print("=" * 50)
    print(f"runs:           {analytics['run_count']}")
    print(f"nodes:          {analytics['node_count']}")
    print(f"edges:          {analytics['edge_count']}")
    print()

    print("top intents:")
    for label, count in analytics["top_intents"]:
        print(f"  - {label}: {count}")
    print()

    print("top modes:")
    for label, count in analytics["top_modes"]:
        print(f"  - {label}: {count}")
    print()

    print("top operations:")
    for label, count in analytics["top_operations"]:
        print(f"  - {label}: {count}")
    print()

    print("top output types:")
    for label, count in analytics["top_output_types"]:
        print(f"  - {label}: {count}")
    print()

    print("top intent -> mode pairs:")
    for item in analytics["top_intent_mode_pairs"]:
        print(f"  - {item['intent']} -> {item['mode']}: {item['count']}")
    print()

    print("top intent -> operation pairs:")
    for item in analytics["top_intent_operation_pairs"]:
        print(f"  - {item['intent']} -> {item['operation']}: {item['count']}")
    print()

    print("interpretation:")
    for item in analytics["interpretation"]:
        print(f"  - {item}")




def _load_json_file(path: str) -> dict:
    target = Path(path)
    try:
        return json.loads(target.read_text(encoding="utf-8"))
    except OSError as exc:
        raise SystemExit(f"Unable to read JSON payload from {target}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {target}: {exc}") from exc


def _print_graph_reasoning(limit_runs: int = 10) -> None:
    reasoning = reason_over_graph(limit_runs=limit_runs)

    print("=" * 50)
    print("HYPERFLOW GRAPH REASONING")
    print("=" * 50)
    print(f"profile:        {reasoning['profile']}")
    print(f"dominant_intent: {reasoning['dominant_intent']}")
    print(f"dominant_mode:  {reasoning['dominant_mode']}")
    print(f"secondary:      {reasoning['secondary_intent']}")
    print()

    print("stable core operations:")
    if reasoning["stable_core_operations"]:
        for item in reasoning["stable_core_operations"]:
            print(f"  - {item}")
    else:
        print("  - none")
    print()

    print("satellite intents:")
    if reasoning["satellite_intents"]:
        for item in reasoning["satellite_intents"]:
            print(f"  - {item}")
    else:
        print("  - none")
    print()

    print("findings:")
    for item in reasoning["findings"]:
        print(f"  - {item}")
    print()

    print(f"summary:        {reasoning['high_level_summary']}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="hyperflow",
        description="Hyperflow MVP CLI",
        allow_abbrev=False,
    )
    parser.add_argument("input", nargs="*", default=[], help="Raw Hyperflow input")
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument("--json", action="store_true", help="Print JSON output (default)")
    output_group.add_argument("--pretty", action="store_true", help="Print human-friendly output")
    parser.add_argument("--save", type=str, default="", help="Save output payload to JSON file")
    parser.add_argument("--recent", action="store_true", help="Show recent runs")
    parser.add_argument("--recent-limit", type=int, default=5, help="Number of recent runs to show")

    parser.add_argument("--graph-summary", action="store_true", help="Show graph memory summary")
    parser.add_argument("--graph-analytics", action="store_true", help="Show graph analytics for recent runs")
    parser.add_argument("--graph-reasoning", action="store_true", help="Show reasoning over recent graph patterns")
    parser.add_argument("--self-profile", action="store_true", help="Show Hyperflow self profile")

    parser.add_argument("--status-report", action="store_true", help="Show Hyperflow status report")
    parser.add_argument(
        "--status-report-save",
        type=str,
        default="",
        help="Save Hyperflow status report to JSON file",
    )

    parser.add_argument(
        "--checkpoint",
        action="store_true",
        help="Create Hyperflow architecture checkpoint",
    )
    parser.add_argument(
        "--checkpoint-name",
        type=str,
        default="checkpoint",
        help="Checkpoint name suffix",
    )
    parser.add_argument(
        "--checkpoint-save",
        type=str,
        default="",
        help="Custom checkpoint JSON output path",
    )
    parser.add_argument(
        "--checkpoint-limit",
        type=int,
        default=10,
        help="Number of recent runs to use for checkpoint",
    )

    parser.add_argument(
        "--checkpoint-history",
        action="store_true",
        help="Show Hyperflow checkpoint history",
    )
    parser.add_argument(
        "--checkpoint-history-limit",
        type=int,
        default=10,
        help="Number of checkpoints to include in history",
    )
    parser.add_argument(
        "--checkpoint-history-save",
        type=str,
        default="",
        help="Save checkpoint history to JSON file",
    )

    parser.add_argument("--graph-mermaid", action="store_true", help="Print graph memory as Mermaid diagram")
    parser.add_argument("--graph-ascii", action="store_true", help="Print graph memory as ASCII view")
    parser.add_argument(
        "--graph-run-limit",
        type=int,
        default=5,
        help="Number of recent runs to include in graph views",
    )
    parser.add_argument("--graph-mermaid-save", type=str, default="", help="Save Mermaid graph to file")
    parser.add_argument("--graph-ascii-save", type=str, default="", help="Save ASCII graph to file")
    parser.add_argument("--version", action="store_true", help="Show Hyperflow version")
    parser.add_argument("--list-workers", action="store_true", help="List live worker inventory")

    args = parser.parse_args()
    raw_input = " ".join(args.input).strip()

    if args.version:
        print(f"Hyperflow {get_version()}")
        return

    if args.list_workers:
        print(json.dumps({"items": list_live_worker_specs()}, ensure_ascii=False, indent=2))
        return

    if args.checkpoint:
        checkpoint_name = args.checkpoint_name.strip().replace(" ", "_") or "checkpoint"

        output_path = args.checkpoint_save
        if not output_path:
            output_path = str(get_checkpoint_file(checkpoint_name))

        snapshot = save_architecture_snapshot(
            output_path=output_path,
            limit_runs=args.checkpoint_limit,
        )

        print("=" * 50)
        print("HYPERFLOW CHECKPOINT")
        print("=" * 50)
        print(f"name:           {checkpoint_name}")
        print(f"output_path:    {output_path}")
        print(f"version:        {snapshot['version']}")
        print(f"status:         {snapshot['status']}")
        print(f"phase:          {snapshot['development_phase']}")
        print(f"work_style:     {snapshot['dominant_work_style']}")
        return

    if args.checkpoint_history:
        history = build_checkpoint_history(limit=args.checkpoint_history_limit)

        if args.checkpoint_history_save:
            _write_text_file(
                args.checkpoint_history_save,
                json.dumps(history, ensure_ascii=False, indent=2),
                label="checkpoint history",
            )

        _print_checkpoint_history(limit=args.checkpoint_history_limit)
        return

    if args.graph_summary:
        _print_graph_summary()
        return

    if args.graph_analytics:
        _print_graph_analytics(limit_runs=args.graph_run_limit)
        return

    if args.graph_reasoning:
        _print_graph_reasoning(limit_runs=args.graph_run_limit)
        return

    if args.self_profile:
        _print_self_profile(limit_runs=args.graph_run_limit)
        return

    if args.status_report:
        report = build_status_report(limit_runs=args.graph_run_limit)

        if args.status_report_save:
            _write_text_file(
                args.status_report_save,
                json.dumps(report, ensure_ascii=False, indent=2),
                label="status report",
            )

        _print_status_report(limit_runs=args.graph_run_limit)
        return

    if args.graph_mermaid:
        output = render_graph_mermaid(limit_runs=args.graph_run_limit)
        if args.graph_mermaid_save:
            _write_text_file(args.graph_mermaid_save, output, label="Mermaid graph")
        print(output)
        return

    if args.graph_ascii:
        output = render_graph_ascii(limit_runs=args.graph_run_limit)
        if args.graph_ascii_save:
            _write_text_file(args.graph_ascii_save, output, label="ASCII graph")
        print(output)
        return

    if args.recent:
        _print_recent(limit=args.recent_limit)
        return

    if not raw_input:
        raise SystemExit(
            "Input is required unless using --recent, --graph-summary, "
            "--graph-analytics, --graph-reasoning, --self-profile, "
            "--status-report, --checkpoint, --checkpoint-history, "
            "--graph-mermaid, --graph-ascii, or --list-workers."
        )

    command = build_command(raw_input)
    result = run(command)

    payload = serialize_run_payload(command, result)

    if args.save:
        _write_text_file(
            args.save,
            json.dumps(payload, ensure_ascii=False, indent=2),
            label="output payload",
        )

    if args.pretty:
        _pretty_print(payload)
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
