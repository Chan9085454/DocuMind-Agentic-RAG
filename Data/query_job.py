import requests
jid = 'b5196e36-c1d9-42ca-813d-6125535544b8'
try:
    r = requests.get('http://127.0.0.1:8000/upload/result', params={'job_id': jid}, timeout=150)
    print('STATUS', r.status_code)
    print(r.text)
except Exception as e:
    print('ERROR', e)
