"""CLI lab. Jalankan python app.py --help dari folder paket."""
import argparse
import json
from workspace import tasks
from lab_core.pipeline import FAQApplication
from lab_core.storage import create_run, save_request, run_directory, read_jsonl
from lab_core.evaluation import load_cases, grade, metrics
from lab_core.report import write_report


def evaluate(args):
    application = FAQApplication(tasks, args.provider)
    folder = create_run(args.run)
    results, traces = [], []
    for case in load_cases():
        result, trace, events = application.ask(case['question'], case['scenario'], case['id'])
        graded = grade(case, result)
        results.append(graded); traces.append(trace)
        save_request(folder, graded, trace, events)
        print(f"{case['id']}: {'PASS' if graded['passed'] else 'FAIL'} status={result['status']}")
    summary = metrics(results)
    (folder/'metrics.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding='utf-8')
    write_report(folder, summary, results, traces)
    print(f"\nQuality: {summary['quality_pass_count']}/{summary['case_count']}")
    print(f"OK={summary['ok_count']} fallback={summary['degraded_count']} error={summary['error_count']}")
    print('Laporan:', folder/'report.html')


def main():
    parser = argparse.ArgumentParser(description='Hands-on FAQ RAG: diagnosis, reliability, prioritization.')
    commands = parser.add_subparsers(dest='command', required=True)
    ask = commands.add_parser('ask'); ask.add_argument('--question', required=True)
    ask.add_argument('--scenario', choices=['normal','timeout','transient_timeout'], default='normal')
    ask.add_argument('--provider', choices=['mock','openai'], default='mock')
    ask.add_argument('--run', required=True)
    evaluate_parser = commands.add_parser('evaluate')
    evaluate_parser.add_argument('--provider', choices=['mock','openai'], default='mock')
    evaluate_parser.add_argument('--run', required=True)
    inspect = commands.add_parser('inspect'); inspect.add_argument('--run', required=True)
    inspect.add_argument('--request-id')
    compare = commands.add_parser('compare'); compare.add_argument('--before', required=True)
    compare.add_argument('--after', required=True)
    args = parser.parse_args()
    try:
        if args.command == 'evaluate':
            evaluate(args)
        elif args.command == 'ask':
            application = FAQApplication(tasks, args.provider)
            folder = create_run(args.run)
            result, trace, events = application.ask(args.question, args.scenario)
            save_request(folder, result, trace, events)
            print(json.dumps(result, indent=2, ensure_ascii=False))
            print('Trace tersimpan di',folder/'traces.jsonl')
        elif args.command == 'inspect':
            rows = read_jsonl(run_directory(args.run)/'traces.jsonl')
            for row in rows:
                if not args.request_id or row['request_id'] == args.request_id:
                    print(json.dumps(row, indent=2, ensure_ascii=False))
        elif args.command == 'compare':
            before = json.loads((run_directory(args.before)/'metrics.json').read_text(encoding='utf-8'))
            after = json.loads((run_directory(args.after)/'metrics.json').read_text(encoding='utf-8'))
            print(f"{'Metric':25} {'Before':>14} {'After':>14}")
            for key in ('quality_pass_count','ok_count','degraded_count','error_count','served_rate','p95_ok_ms'):
                print(f"{key:25} {str(before[key]):>14} {str(after[key]):>14}")
            print('Durasi adalah hasil lokal. Fallback tidak dihitung sebagai model OK.')
    except (ValueError, OSError, RuntimeError) as error:
        parser.exit(1, f'Error: {error}\n')


if __name__ == '__main__':
    main()
