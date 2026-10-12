import html
import json

def write_report(folder, summary, results, traces):
    esc = lambda value: html.escape(str(value))
    rows = []
    for result, trace in zip(results, traces):
        spans = ''.join('<tr><td>'+esc(s['name'])+'</td><td>'+esc(s.get('attempt',''))+
                        '</td><td>'+esc(s['status'])+'</td><td>'+esc(s['duration_ms'])+
                        '</td><td>'+esc(s.get('index_version', s.get('error_type','')))+
                        '</td></tr>' for s in trace['spans'])
        rows.append('<section><h2>'+esc(result.get('case_id',result['request_id']))+
                    ' — '+('PASS' if result.get('passed') else 'FAIL')+'</h2><p>'+esc(result['question'])+
                    '</p><p><strong>Status:</strong> '+esc(result['status'])+
                    ' <strong>Trace status:</strong> '+esc(trace.get('status'))+
                    ' <strong>Trace total:</strong> '+esc(trace.get('duration_ms'))+' ms</p><p>'+esc(result['answer'])+
                    '</p><p>'+esc('; '.join(result.get('reasons',[])))+'</p><table><thead><tr><th>Stage</th>'
                    '<th>Attempt</th><th>Status</th><th>Durasi (ms)</th><th>Versi/error</th></tr></thead><tbody>'+
                    spans+'</tbody></table></section>')
    stats = ''.join('<tr><th>'+esc(k)+'</th><td>'+esc(v)+'</td></tr>' for k,v in summary.items())
    document = '<!doctype html><html lang="id"><meta charset="utf-8"><meta name="viewport" content="width=device-width">'
    document += '<title>Hasil Lab FAQ AIEN</title><style>body{font:16px system-ui,sans-serif;max-width:1040px;margin:32px auto;padding:0 20px;color:#203044}h1,h2{color:#1d417f}table{border-collapse:collapse;width:100%;margin:16px 0}td,th{border:1px solid #d4dce5;padding:9px;text-align:left;vertical-align:top}thead{background:#edf2f8}section{border-top:2px solid #d4dce5;margin-top:28px;padding-top:12px}p{line-height:1.6;overflow-wrap:anywhere}</style>'
    document += '<h1>Hasil Lab FAQ AIEN</h1><p>Data kebijakan fiktif. Mode mock bukan inferensi LLM. Durasi diukur saat aplikasi berjalan. Token mock berupa estimasi karakter/4.</p><table>'+stats+'</table>'+''.join(rows)+'</html>'
    (folder/'report.html').write_text(document, encoding='utf-8')
