import urllib.request
import urllib.error
import json

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QHRlc3QuY29tIiwiZXhwIjoxNzcyNTI4ODUzfQ.tdQrhkKZVcDIficB-aSxkKFAt2g5P97tzBxJekpfzIQ"

req = urllib.request.Request(
    'http://localhost:8000/api/habits/1/log?value=100',
    method='POST',
    headers={'Authorization': f'Bearer {token}'}
)

try:
    response = urllib.request.urlopen(req)
    print('Status:', response.status)
    print('Response:', response.read().decode())
except urllib.error.HTTPError as e:
    print('Status:', e.code)
    print('Headers:', e.headers)
    print('Response:', e.read().decode())
except Exception as e:
    print('Exception:', type(e).__name__, str(e))
