import numpy as np, potrace
from PIL import Image
from scipy import ndimage as ndi
SRC='/mnt/user-data/uploads/1000868500.jpg'
OUT='/home/claude/site/assets/img/'
im=Image.open(SRC).convert('RGB'); a=np.array(im).astype(int)
bg=np.array([244,243,239]); d=np.abs(a-bg).sum(2)
# --- transparent full mark (flood from border; interior white text stays) ---
near=d<14
lab,n=ndi.label(near)
border=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
bgmask=np.isin(lab,list(border))
alpha=np.where(bgmask,0,255).astype(np.uint8)
# soften shadow: pixels outside the bar/name that are only faintly different
alpha=ndi.gaussian_filter(alpha.astype(float),0.8).clip(0,255).astype(np.uint8)
rgba=np.dstack([a.clip(0,255).astype(np.uint8),alpha])
full=Image.fromarray(rgba,'RGBA')
ys,xs=np.where(alpha>20)
box=(max(xs.min()-24,0),max(ys.min()-24,0),xs.max()+24,ys.max()+24)
full=full.crop(box); print('full size',full.size)
full.save(OUT+'logo-original-transparent.png')
for w in (360,540,720,1440):
    h=round(full.size[1]*w/full.size[0]); full.resize((w,h),Image.LANCZOS).save(OUT+f'logo-dimensional-{w}.webp',quality=92)
# --- sample colors ---
dark=(a.sum(2)<250); navy=np.median(a[dark],axis=0).astype(int)
print('navy',navy, '#%02x%02x%02x'%tuple(navy))
bar_top,bar_bot=536,897
cols=np.where((d[700,:]>60))[0]; bx0,bx1=cols.min(),cols.max(); print('bar x',bx0,bx1)
cy=(bar_top+bar_bot)//2
print('teal center','#%02x%02x%02x'%tuple(a[560,1280]), 'edge','#%02x%02x%02x'%tuple(a[cy,bx0+60]))
print('cream','#%02x%02x%02x'%tuple(a[cy,bx0+8]))
# --- trace name text (rows 255-505) ---
def trace(mask,ox=0,oy=0,turd=4):
    bm=potrace.Bitmap(~mask); pl=bm.trace(turdsize=turd,alphamax=1.0,opticurve=True,opttolerance=0.3)
    parts=[]
    for c in pl:
        sp=c.start_point; p=[f'M{sp.x+ox:.1f} {sp.y+oy:.1f}']
        for s in c.segments:
            if s.is_corner: p.append(f'L{s.c.x+ox:.1f} {s.c.y+oy:.1f}L{s.end_point.x+ox:.1f} {s.end_point.y+oy:.1f}')
            else: p.append(f'C{s.c1.x+ox:.1f} {s.c1.y+oy:.1f} {s.c2.x+ox:.1f} {s.c2.y+oy:.1f} {s.end_point.x+ox:.1f} {s.end_point.y+oy:.1f}')
        p.append('Z'); parts.append(''.join(p))
    return ''.join(parts)
lum=a.mean(2)
y0,y1=250,510
name_mask=np.zeros(lum.shape,bool); name_mask[y0:y1]=(lum[y0:y1]<135)
nx=np.where(name_mask.any(0))[0]; print('name x',nx.min(),nx.max())
name_d=trace(name_mask)
# white text inside bar
inner=np.zeros(lum.shape,bool); inner[bar_top+40:bar_bot-40,bx0+40:bx1-40]=True
white=inner&(a.min(2)>200)
wy,wx=np.where(white); print('white bbox',wx.min(),wx.max(),wy.min(),wy.max())
text_d=trace(white,turd=60)
# crop frame
X0,X1=140,2500; Y0=140; Y1=910
W=X1-X0; H=Y1-Y0
def svg(name_fill,rule_fill,flat=True):
    cx=(bx0+bx1)/2
    grad='''<radialGradient id="g" cx="50%" cy="8%" r="90%"><stop offset="0" stop-color="#2a6a78"/><stop offset=".55" stop-color="#1f3f5e"/><stop offset="1" stop-color="#16264a"/></radialGradient>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{X0} {Y0} {W} {H}" role="img" aria-label="Dave Hoffman Auto Repair"><defs>{grad}</defs>
<path d="M156 163 L1320 158 L2487 163 L1320 168 Z" fill="{rule_fill}"/>
<path d="{name_d}" fill="{name_fill}" fill-rule="evenodd"/>
<rect x="{bx0+6}" y="{bar_top+6}" width="{bx1-bx0-12}" height="{bar_bot-bar_top-12}" rx="64" fill="url(#g)" stroke="#d6cfb8" stroke-width="12"/>
<path d="{text_d}" fill="#fff" fill-rule="evenodd"/></svg>'''
open(OUT+'logo-flat.svg','w').write(svg('#1b2d4f','#1b2d4f'))
open(OUT+'logo-flat-dark.svg','w').write(svg('#f5f3ef','#f5f3ef'))
print('svg done', len(name_d), len(text_d))
