from check_results import run_checks
checks = run_checks()
failed = [r['pemeriksaan'] for r in checks if r['status'] == 'FAIL']
if failed:
    raise AssertionError('Pemeriksaan gagal: ' + ', '.join(failed))
print('PASS: seluruh pemeriksaan hasil terpenuhi.')
