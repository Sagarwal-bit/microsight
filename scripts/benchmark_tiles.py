import time,urllib.request,json
url='http://localhost:8000/api/metrics/'
try:
 start=time.perf_counter(); print(json.loads(urllib.request.urlopen(url,timeout=3).read())); print(f'metrics request_ms={(time.perf_counter()-start)*1000:.2f}')
except Exception as e: print('Start the backend before benchmarking:',e)
