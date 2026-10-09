"""Infrastruktur latihan. Peserta mengubah aturan dan fungsi normalisasi di notebook."""
from pathlib import Path
from datetime import datetime, timezone
import json
import tempfile
import os
os.environ["GX_ANALYTICS_ENABLED"] = "False"
import pandas as pd
import great_expectations as gx
from great_expectations.checkpoint import UpdateDataDocsAction
from great_expectations.core import RunIdentifier

def load_data(root):
    root = Path(root)
    def read(name):
        return pd.read_csv(root / 'data' / name, dtype={
            'customer_id': 'string', 'snapshot_date': 'string'})
    return read('customer_snapshot.csv'), read('customer_source.csv'), read('usage_source.csv')

def profile(df):
    return pd.DataFrame({
        'dtype': df.dtypes.astype(str),
        'missing_count': df.isna().sum(),
        'missing_percent': (df.isna().mean()*100).round(2),
        'distinct_count': df.nunique(dropna=True),
    })

def legacy_normalize(customers):
    ids = customers['customer_id'].astype('string').copy()
    legacy = customers['source_system'].eq('legacy') & ids.notna()
    ids.loc[legacy] = ids.loc[legacy].astype(int).astype('string')
    return ids

def build_snapshot(customers, usage, normalize_id=legacy_normalize):
    left = customers.copy()
    left['customer_id'] = normalize_id(left)
    right = usage.copy()
    right['customer_id'] = right['customer_id'].astype('string').str.strip()
    merged = left.merge(right, on=['customer_id', 'snapshot_date'],
        how='left', validate='many_to_one')
    # Simulasi insiden ingestion terpisah. Perbaikan join tidak menghapus insiden ini.
    replay = merged.loc[merged['customer_id'].isin(['00030','00040'])]
    return pd.concat([merged, replay], ignore_index=True)

def create_checkpoint(root, expectations):
    root = Path(root)
    runs = root / 'reports' / 'gx_runs'
    runs.mkdir(parents=True, exist_ok=True)
    run_dir = Path(tempfile.mkdtemp(prefix='session_', dir=runs))
    # File context lokal menyimpan suite, hasil, serta Data Docs; tidak memakai GX Cloud.
    context = gx.get_context(mode='file', project_root_dir=str(run_dir))
    source = context.data_sources.add_pandas(name='churn_source')
    asset = source.add_dataframe_asset(name='customer_snapshot')
    batch = asset.add_batch_definition_whole_dataframe(name='whole_snapshot')
    suite = context.suites.add(gx.ExpectationSuite(name='churn_quality'))
    for expectation in expectations:
        suite.add_expectation(expectation)
    validation = context.validation_definitions.add(gx.ValidationDefinition(
        name='validate_churn', data=batch, suite=suite))
    checkpoint = context.checkpoints.add(gx.Checkpoint(
        name='churn_checkpoint', validation_definitions=[validation],
        actions=[UpdateDataDocsAction(name='update_local_docs')],
        result_format={'result_format':'SUMMARY'}))
    return context, checkpoint

def validate(context, checkpoint, df, label, root):
    result = checkpoint.run(batch_parameters={'dataframe': df},
        run_id=RunIdentifier(run_name=label, run_time=datetime.now(timezone.utc)))
    rows = []
    for validation in result.run_results.values():
        for item in validation.results:
            expectation = item.expectation_config
            metadata = expectation.meta or {}
            rows.append({
                'rule_id': metadata.get('rule_id', expectation.type),
                'expectation': expectation.type,
                'success': bool(item.success),
                'unexpected_count': item.result.get('unexpected_count'),
                'unexpected_percent': item.result.get('unexpected_percent'),
                'owner': metadata.get('owner'),
                'severity_policy': metadata.get('severity_policy'),
                'action_on_failure': metadata.get('action_on_failure'),
            })
    summary = pd.DataFrame(rows)
    reports = Path(root) / 'reports'
    reports.mkdir(parents=True, exist_ok=True)
    summary.to_csv(reports / f'{label}_summary.csv', index=False)
    payload = {'checkpoint': checkpoint.name, 'run_name': label,
        'success': bool(result.success),
        'validation_results': [v.to_json_dict() for v in result.run_results.values()]}
    (reports / f'{label}_checkpoint.json').write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    sites = context.get_docs_sites_urls()
    docs = [x.get('site_url') for x in sites if x.get('site_url')]
    (reports / 'data_docs_locations.json').write_text(json.dumps(docs, indent=2), encoding='utf-8')
    return summary, docs
