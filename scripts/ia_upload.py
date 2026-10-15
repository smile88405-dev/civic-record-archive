# 記録フォルダを Internet Archive に1アイテムとしてアップロード
# 使い方: python3 ia_upload.py <記録フォルダ> <キーファイル(1行目access 2行目secret)> [--dry]
import sys, os, json, hashlib
from internetarchive import upload, get_item
ev, keyf = sys.argv[1], sys.argv[2]; dry='--dry' in sys.argv
m=json.load(open(f'{ev}/metadata.json',encoding='utf-8'))
# SHA256台帳を作り直す
man=[]
for root,_,fs in sorted(os.walk(ev)):
    for f in sorted(fs):
        if f.endswith('.sha256'): continue
        p=os.path.join(root,f); man.append(hashlib.sha256(open(p,'rb').read()).hexdigest()+'  '+os.path.relpath(p,ev))
sh=[f for f in os.listdir(ev) if f.endswith('.sha256')]
open(os.path.join(ev,sh[0] if sh else 'SHA256.sha256'),'w',encoding='utf-8').write('\n'.join(man)+'\n')
files={}
for root,_,fs in os.walk(ev):
    for f in fs:
        p=os.path.join(root,f); files[os.path.relpath(p,ev).replace(os.sep,'/')]=p
md={'mediatype':'image','collection':'opensource_media','title':m['project_title'],
    'date':m['date'],'creator':[c['name'] for c in m['contributors']],
    'description':m['description']+'<br><br>'+m.get('title_en','')+'<br>調査・工事: '+' / '.join(m.get('subjects',[])),
    'subject':m.get('tags',[]),'licenseurl':'https://creativecommons.org/licenses/by/4.0/','language':'jpn',
    'coverage':m['location'],'rights':m['license'].get('credit','')}
print(m['ia_identifier'], len(files),'files', round(sum(os.path.getsize(p) for p in files.values())/1e9,2),'GB')
if dry: sys.exit()
ak,sk=[l.strip() for l in open(keyf,encoding='utf-8-sig') if l.strip()][:2]
import time
budget=float(next((a.split('=')[1] for a in sys.argv if a.startswith('--budget=')),'1e9')); t0=time.time()
item=get_item(m['ia_identifier'],archive_session=None) if False else get_item(m['ia_identifier'])
have={f['name']:int(f.get('size',0)) for f in (item.files or [])}
todo=[(k,v) for k,v in sorted(files.items(),key=lambda x:os.path.getsize(x[1])) if have.get(k)!=os.path.getsize(v)]
print('remaining',len(todo))
for k,v in todo:
    if time.time()-t0>budget: print('budget stop'); break
    s0=time.time(); r=upload(m['ia_identifier'],files={k:v},metadata=md,access_key=ak,secret_key=sk,retries=3,retries_sleep=10,checksum=True,queue_derive=False)
    print('up',k,r[0].status_code if r else 'skip',round(os.path.getsize(v)/1e6/(time.time()-s0+1e-9),1),'MB/s',flush=True)
print('left',len([1 for k,v in todo if k not in have]) )
