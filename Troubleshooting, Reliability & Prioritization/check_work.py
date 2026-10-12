"""Pemeriksaan outcome peserta. Tidak mengubah jawaban atau baseline."""
from workspace import tasks
from lab_core.pipeline import FAQApplication
from lab_core.evaluation import load_cases, grade
from lab_core.config import FAQ_URL


def main():
    app=FAQApplication(tasks)
    failures=[]
    if tasks.choose_document_version({'current_version':'v-next','versions':{'v-next':'unused'}}) != 'v-next':
        failures.append('TODO 2: versi harus mengikuti manifest, bukan dipatok ke v2.')
    sample={'request_id':'check','spans':[{'name':'sample'}]}
    updated=tasks.complete_trace(sample, 12.5, 'ok')
    if updated.get('duration_ms')!=12.5 or updated.get('status')!='ok' or updated.get('spans')!=sample['spans']:
        failures.append('TODO 1: complete_trace belum merekam duration_ms/status atau menghapus metadata.')
    for case in load_cases():
        result,trace,events=app.ask(case['question'],case['scenario'],case['id'])
        graded=grade(case,result)
        if not graded['passed']:
            failures.append(case['id']+': '+ '; '.join(graded['reasons']))
        if trace.get('status')!=result['status'] or trace.get('duration_ms')!=result['duration_ms']:
            failures.append(case['id']+': trace total/status belum konsisten dengan hasil request.')
        if case['scenario']=='timeout':
            attempts=[s for s in trace['spans'] if s['name']=='generation']
            if len(attempts)!=2:
                failures.append('Timeout harus berhenti setelah maksimum dua percobaan.')
    # Bukti recovery: timeout sebelumnya tidak memblokir request berikutnya.
    recovered,_,_=app.ask('Apa metode pembayaran?')
    if recovered['status']!='ok':
        failures.append('Request normal setelah timeout tidak pulih.')
    transient,trace,events=app.ask('Apa metode pembayaran?', 'transient_timeout')
    if transient['status']!='ok' or len([s for s in trace['spans'] if s['name']=='generation'])!=2:
        failures.append('Retry sementara harus berhasil pada percobaan kedua.')
    if failures:
        print('BELUM LULUS:\n'+'\n'.join('- '+f for f in failures))
        return 1
    print('LULUS: 10/10 kasus, telemetry lengkap, fallback aman, retry terbatas, dan recovery request berikutnya.')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
