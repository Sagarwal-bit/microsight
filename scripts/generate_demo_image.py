"""Generate synthetic, non-clinical microscopy-style pixels for MicroSight demos."""
from pathlib import Path
import argparse, numpy as np, cv2
from PIL import Image, ImageFilter
p=argparse.ArgumentParser();p.add_argument('-o','--output',default='work/demo-microscopy.png');p.add_argument('--size',type=int,default=2048);a=p.parse_args(); rng=np.random.default_rng(42); size=a.size
img=np.full((size,size,3),(235,218,225),np.uint8)
for _ in range(1500):
 x,y=rng.integers(0,size,2); r=int(rng.integers(3,15)); cv2.ellipse(img,(int(x),int(y)),(r,max(2,r//2)),int(rng.integers(0,180)),0,360,(int(rng.integers(60,150)),int(rng.integers(30,100)),int(rng.integers(90,180))),-1)
for _ in range(18):
 x,y=rng.integers(0,size,2); cv2.ellipse(img,(int(x),int(y)),(int(rng.integers(100,300)),int(rng.integers(80,240))),0,0,360,(190,130,170),-1)
out=Image.fromarray(img); out=out.filter(ImageFilter.GaussianBlur(2)); Path(a.output).parent.mkdir(parents=True,exist_ok=True); out.save(a.output); print(Path(a.output).resolve())
