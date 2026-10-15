# RAW(ARW) -> 16bit非圧縮TIFF / 最高画質JPEG / SHA-256台帳 / metadata.json
# 使い方: python3 raw_archive.py <元フォルダ> <案件フォルダ> <接頭辞> <撮影日YYYY:MM:DD>
import sys, os, shutil, hashlib, json, glob
import rawpy, tifffile, numpy as np
from PIL import Image
src, dst, prefix, day = sys.argv[1:5]
limit=int(sys.argv[5]) if len(sys.argv)>5 else 999; did=0
finalize=limit==0
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()
for d in ['RAW','カメラJPEG','TIFF_16bit','JPEG_max']: os.makedirs(f'{dst}/{d}',exist_ok=True)
files=[]; n=0
for arw in sorted(glob.glob(f'{src}/*.ARW')):
    stem=os.path.splitext(os.path.basename(arw))[0]; jpg=f'{src}/{stem}.JPG'
    ex=Image.open(jpg).getexif() if os.path.exists(jpg) else None
    e=ex.get_ifd(0x8769) if ex else {}
    if e.get(36867,'')[:10]!=day: continue
    n+=1; base=f'{prefix}_一眼_{n:02d}_{stem}'
    out={'id':base,'original_filename':os.path.basename(arw),'datetime':e.get(36867),
         'exposure':f"1/{round(1/float(e.get(33434)))}s F{float(e.get(33437))} ISO{e.get(34855)} {float(e.get(37386))}mm"}
    r=f'{dst}/RAW/{base}.ARW'; t=f'{dst}/TIFF_16bit/{base}.tif'
    out['raw']=f'RAW/{base}.ARW'; out['camera_jpeg']=f'カメラJPEG/{base}.jpg'; out['tiff']=f'TIFF_16bit/{base}.tif'; out['jpeg']=f'JPEG_max/{base}_max.jpg'
    if os.path.exists(f'{dst}/JPEG_max/{base}_max.jpg') or finalize:
        files.append(out); continue
    if did>=limit: continue
    did+=1
    shutil.copy2(arw,r)
    assert sha(arw)==sha(r), arw
    out['raw']=f'RAW/{base}.ARW'
    t=f'{dst}/TIFF_16bit/{base}.tif'
    if os.path.exists(jpg):
        shutil.copy2(jpg,f'{dst}/カメラJPEG/{base}.jpg'); out['camera_jpeg']=f'カメラJPEG/{base}.jpg'
    with rawpy.imread(arw) as raw:
        rgb=raw.postprocess(output_bps=16,use_camera_wb=True,output_color=rawpy.ColorSpace.sRGB)
    tifffile.imwrite(t,rgb,photometric='rgb',compression=None,
        description=f'{stem} / Photo: Shingo Hatakeyama / CC BY 4.0',software='rawpy(LibRaw)+tifffile')
    out['tiff']=f'TIFF_16bit/{base}.tif'; out['size_px']=[int(rgb.shape[1]),int(rgb.shape[0])]
    Image.fromarray((rgb>>8).astype(np.uint8)).save(f'{dst}/JPEG_max/{base}_max.jpg',quality=95,subsampling=0)
    out['jpeg']=f'JPEG_max/{base}_max.jpg'
    files.append(out); print('done',base,flush=True)
if not finalize: sys.exit(0)
man=[]
for root,_,fs in os.walk(dst):
    for f in sorted(fs):
        if f.endswith('.sha256'): continue
        p=os.path.join(root,f); man.append(f'{sha(p)}  {os.path.relpath(p,dst)}')
open(f'{dst}/{prefix}_SHA256_v01.sha256','w',encoding='utf-8').write('\n'.join(man)+'\n')
json.dump({'files':files},open(f'{dst}/_files_auto.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('ALL DONE',n)
