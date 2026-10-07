"""Periksa ekspor peserta terhadap dataset sumber. Hanya memakai standard library."""
from pathlib import Path
from collections import Counter
import csv, math, statistics, argparse, sys
ROOT=Path(__file__).resolve().parents[1]

def read_csv(path):
    with path.open(encoding='utf-8-sig',newline='') as handle:
        return list(csv.DictReader(handle))

def quantile(values,q=.95):
    values=sorted(values); position=(len(values)-1)*q
    lo=math.floor(position);hi=math.ceil(position)
    return values[lo]+(values[hi]-values[lo])*(position-lo)

def run_checks(output=None, save=True):
    out=Path(output) if output else ROOT/'output'
    source=read_csv(ROOT/'data/chatbot_evaluation.csv')
    checks=[]
    def check(name,actual,target,ok):
        checks.append({'pemeriksaan':name,'aktual':str(actual),'target':str(target),'status':'PASS' if ok else 'FAIL'})
    def near(actual,target,tolerance=1e-7):
        try:
            value=float(actual)
            return math.isfinite(value) and abs(value-target)<=tolerance
        except (TypeError,ValueError):return False
    tables={}
    for name in ['summary.csv','category_summary.csv','failed_cases.csv']:
        path=out/name
        try:
            tables[name]=read_csv(path)
            check('file_'+name,'tersedia','CSV terbaca',True)
        except (OSError,UnicodeError,csv.Error) as exc:
            check('file_'+name,type(exc).__name__,'CSV terbaca',False)
    rows=tables.get('summary.csv',[])
    if rows:
        check('summary_unique_versions',[r.get('model_version') for r in rows],['A','B'],Counter(r.get('model_version') for r in rows)==Counter(['A','B']))
        for version in ['A','B']:
            subset=[r for r in source if r['model_version']==version]
            matches=[r for r in rows if r.get('model_version')==version]
            got=matches[0] if len(matches)==1 else {}
            expected={'n':len(subset),
                'pass_rate_pct':100*statistics.mean(int(r['answer_pass']) for r in subset),
                'resolution_rate_pct':100*statistics.mean(int(r['resolved']) for r in subset),
                'median_latency_s':statistics.median(float(r['latency_seconds']) for r in subset),
                'p95_latency_s':quantile([float(r['latency_seconds']) for r in subset]),
                'avg_cost_usd':statistics.mean(float(r['cost_usd']) for r in subset)}
            for col,target in expected.items():check(version+'_'+col,got.get(col,'missing'),target,near(got.get(col),target))
    elif 'summary.csv' in tables:check('summary_nonempty',0,2,False)
    rows=tables.get('category_summary.csv',[])
    if rows:
        expected_keys={(r['model_version'],r['category']) for r in source}
        actual_keys=[(r.get('model_version'),r.get('category')) for r in rows]
        check('category_unique_keys',len(actual_keys),8,len(actual_keys)==8 and set(actual_keys)==expected_keys)
        for version,category in sorted(expected_keys):
            subset=[r for r in source if (r['model_version'],r['category'])==(version,category)]
            matches=[r for r in rows if (r.get('model_version'),r.get('category'))==(version,category)]
            got=matches[0] if len(matches)==1 else {}
            for col,target in [('n',len(subset)),('pass_rate_pct',100*statistics.mean(int(r['answer_pass']) for r in subset))]:
                check(f'{version}_{category}_{col}',got.get(col,'missing'),target,near(got.get(col),target))
    elif 'category_summary.csv' in tables:check('category_nonempty',0,8,False)
    if 'failed_cases.csv' in tables:
        rows=tables['failed_cases.csv'];expected=[r for r in source if r['answer_pass']=='0']
        fields=['question_id','model_version','category','failure_reason']
        signature=lambda r:tuple(r.get(c) or '' for c in fields)
        check('failed_case_keys_and_reasons',len(rows),len(expected),Counter(map(signature,rows))==Counter(map(signature,expected)))
        check('failed_labels',[r.get('answer_pass') for r in rows][:5],'semua 0',all(near(r.get('answer_pass'),0) for r in rows))
    png=out/'dashboard.png'
    ok=png.exists() and png.read_bytes()[:8]==b'\x89PNG\r\n\x1a\n'
    check('dashboard_png','tersedia' if ok else 'missing/invalid','PNG valid',ok)
    if save:
        out.mkdir(parents=True,exist_ok=True)
        with (out/'checks.csv').open('w',newline='',encoding='utf-8') as handle:
            writer=csv.DictWriter(handle,fieldnames=['pemeriksaan','aktual','target','status']);writer.writeheader();writer.writerows(checks)
    return checks

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=None)
    args=parser.parse_args();checks=run_checks(args.output)
    for row in checks:print(f"{row['status']:4} {row['pemeriksaan']}: aktual={row['aktual']}, target={row['target']}")
    failures=sum(row['status']=='FAIL' for row in checks)
    print(f'\n{len(checks)-failures}/{len(checks)} PASS. Pemeriksaan visual dan narasi tetap memerlukan review instruktur.')
    return 1 if failures else 0
if __name__=='__main__':sys.exit(main())
