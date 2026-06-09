"""
Generate a test report from Echo-Sync interaction logs.

Reads the CSV interaction log and generates a summary markdown report.

Usage:
    python scripts/generate_test_report.py
    python scripts/generate_test_report.py --log-file logs/interaction_logs.csv
"""

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path


def generate_report(log_file: Path) -> str:
    """Generate a markdown report from the interaction log CSV."""
    if not log_file.exists():
        return "# Test Report\n\nNo interaction log found. Run Echo-Sync first.\n"

    rows = []
    with open(log_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    if not rows:
        return "# Test Report\n\nNo interactions logged yet.\n"

    # Compute statistics
    total = len(rows)
    intent_counts = Counter(r.get("intent_type", "unknown") for r in rows)
    action_counts = Counter(r.get("action", "unknown") for r in rows)
    success_count = sum(1 for r in rows if r.get("success") == "yes")
    fail_count = total - success_count
    context_counts = Counter(
        r.get("interpreted_context", "none")
        for r in rows
        if r.get("interpreted_context") and r["interpreted_context"] != "none"
    )

    # Build report
    report = []
    report.append("# Echo-Sync Test Report\n")
    report.append(f"**Total interactions:** {total}\n")
    report.append(f"**Successful:** {success_count} ({success_count/total*100:.0f}%)\n")
    report.append(f"**Failed:** {fail_count} ({fail_count/total*100:.0f}%)\n")

    report.append("\n## Intent Distribution\n")
    report.append("| Intent Type | Count | Percentage |")
    report.append("|---|---:|---:|")
    for intent, count in intent_counts.most_common():
        pct = count / total * 100
        report.append(f"| {intent} | {count} | {pct:.0f}% |")

    report.append("\n## Action Distribution\n")
    report.append("| Action | Count |")
    report.append("|---|---:|")
    for action, count in action_counts.most_common():
        report.append(f"| {action} | {count} |")

    if context_counts:
        report.append("\n## Interpreted Contexts\n")
        report.append("| Context | Count |")
        report.append("|---|---:|")
        for ctx, count in context_counts.most_common():
            report.append(f"| {ctx} | {count} |")

    report.append("\n## Recent Interactions\n")
    report.append("| Timestamp | Transcript | Intent | Action | Success |")
    report.append("|---|---|---|---|---|")
    for row in rows[-10:]:  # Last 10
        report.append(
            f"| {row.get('timestamp', '')[:19]} "
            f"| {row.get('transcript', '')[:40]} "
            f"| {row.get('intent_type', '')} "
            f"| {row.get('action', '')} "
            f"| {row.get('success', '')} |"
        )

    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description="Generate test report")
    parser.add_argument(
        "--log-file",
        type=str,
        default="logs/interaction_logs.csv",
        help="Path to interaction log CSV",
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="Output file (default: print to stdout)",
    )
    args = parser.parse_args()

    log_path = Path(args.log_file)
    report = generate_report(log_path)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"Report saved to: {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
