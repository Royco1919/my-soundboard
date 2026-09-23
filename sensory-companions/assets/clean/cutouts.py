# v5 = v4 pipeline with re-traced occlusion seams (no wide-feather zones, no straight cuts):
#  - pandas: seam hugs the big panda's mane / ear (blue bag, sloth ear fluff and the white sloth patch stay out), and the small panda's
#    right arm is cut at its own outline (the big panda's curly paw, the sloth-arm shadow and the store tag stay out)
#  - sloth pair: seam follows the big sloth's arm down and around its three claws, then the small sloth's own body/arm edge;
#    the dark shadow wedge under the claws and the white fluff patch left of the arm are alpha 0
#  - small sloth: right paw + white felt claws restored from the store photo with a hand-traced patch (the segmenter had shredded it)
#  uniform 2.5 px feather, 3 px alpha erosion, de-fringe, no islands < 1500 px, pad holes filled
import numpy as np, sys, os
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage as ndi
A='/home/user/my-soundboard/sensory-companions/assets/'
OUT=A+'clean/'
PREV='/tmp/claude-0/-home-user-my-soundboard/0bae543d-54b7-5c74-b4f4-c802d116c901/scratchpad/work/vfix3/cut/'
os.makedirs(PREV,exist_ok=True)
g=Image.open(A+'group-cutout.png').convert('RGBA'); Wd,Ht=g.size
OX,OY=311,461
store=np.asarray(Image.open(A+'store-photo.jpg').convert('RGB')).astype(np.float32)[OY:OY+Ht,OX:OX+Wd]
rgb=np.concatenate([store,np.zeros((Ht,Wd,1),np.float32)],2)
a0=np.asarray(g).astype(np.float32)[...,3]/255.0
hard=a0>0.5
hard=ndi.binary_fill_holes(hard)
hard=ndi.binary_opening(hard,iterations=1)
alpha=a0.copy(); alpha[hard&(a0<0.5)]=1.0
inner=ndi.binary_erosion(hard,iterations=5); alpha[inner]=1.0
outer=~ndi.binary_dilation(hard,iterations=5); alpha[outer]=0.0
alpha=np.where(alpha>=0.96,1.0,alpha)

# --- seams (group-cutout coordinates) ---
# big panda's right ear + mane right edge, then the small panda's mane right edge (panda side)
MANE=[(540,0),(540,95),(556,110),(566,124),(590,128),(600,140),(606,200),(614,240),(628,270),(642,300),(654,325),(660,350),(662,380),(662,420),(658,450),(644,468),(624,482),(610,500),(603,525),(600,552),(602,575),(612,594),(640,600),(672,612),(688,626),(692,652),(696,700),(702,750),(706,800),(710,850),(716,900),(722,940)]
# small panda's right arm: its own outline against the big panda's curly paw, then the store tag, then its leg against the small sloth's foot
ARM_P=[(720,962),(722,1000),(730,1040),(738,1080),(742,1120),(744,1145),(738,1160),(730,1200),(722,1250),(716,1300),(716,1335),(750,1345),(790,1385),(825,1410),(845,1450),(850,1500),(850,1708)]
# sloth side: big sloth's ear, head and left arm edge, around the three claws, then the small sloth's own body + left arm edge
SLOTH_L=[(560,0),(596,130),(604,160),(606,200),(614,240),(640,262),(660,290),(688,318),(704,335),(710,400),(724,425),(744,442),(754,462),(748,486),(732,505),(720,530),(716,560),(714,600),(716,650),(718,690),(724,712),(730,738),(742,772),(752,800),(766,818),(782,804),(792,786),(806,790),(822,784),(836,766),(846,742),(852,730),(852,770),(850,810),(848,850),(850,885),(856,910),(866,945),(878,978),(890,1012),(896,1040),(895,1050),(892,1100),(890,1112),(888,1130),(880,1140),(860,1148),(830,1152),(800,1160),(780,1172),(765,1195),(756,1225),(748,1250),(740,1280),(736,1310),(738,1335),(770,1350),(805,1365),(838,1400),(848,1450),(850,1500),(850,1708)]
POLYS={
 'redpanda-pair': [(0,0)]+MANE+ARM_P+[(0,1708)],
 'sloth-pair': [(1545,0)]+SLOTH_L+[(1545,1708)],
 'redpanda-small': [(170,700),(185,655),(200,625),(222,600),(248,598),(272,628),(300,622),(350,616),(400,612),(450,610),(500,613),(538,626),(556,600),(578,590),(598,612),(608,650),(612,700),(630,735),(655,765),(680,795),(700,830),(706,860),(710,900),(716,925),(722,940)]
                   +ARM_P+[(0,1708),(0,1200),(60,1080),(120,1030),(175,1020),(160,980),(145,920),(142,860),(148,800),(160,740)],
 'sloth-small': [(802,470),(812,445),(835,428),(870,420),(905,425),(940,448),(968,472),(1000,452),(1040,432),(1090,418),(1140,412),(1190,420),(1240,405),(1300,440),(1330,520),(1545,600),(1545,1708),(900,1708),(880,1450),(860,1415),(846,1380),(843,1335),(848,1305),(858,1285),(875,1265),(897,1247),(912,1230),(912,1190),(905,1160),(898,1140),(902,1115),(903,1060),(906,1000),(900,950),(896,900),(893,850),(893,800),(896,740),(895,690),(885,650),(860,640),(830,640),(808,620),(800,560),(798,500)],
}
# hand-traced opaque patches (the segmenter shredded these): small sloth's right paw with its three white claws
PATCHES={'sloth-small':[[(1250,790),(1300,800),(1340,812),(1360,830),(1378,860),(1392,895),(1400,930),(1402,960),(1395,990),(1385,1000),(1375,1012),(1362,1005),(1355,990),(1345,985),(1338,960),(1330,932),(1310,936),(1290,950),(1275,970),(1262,1000),(1250,1020),(1240,1000),(1238,930),(1240,860)]]}
FEATHER=2.5
HUE_ZONES={
 'sloth-pair': [((880,995,965,1135),'panda')],
 'sloth-small': [((880,995,965,1135),'panda')],
 'redpanda-pair': [((300,0,735,250),'notpanda'),((585,250,735,640),'notpanda-nowhite')],
 'redpanda-small': [((300,0,735,250),'notpanda'),((585,250,735,640),'notpanda-nowhite')],
}
ERODE=3
MIN_ISLAND=1500
def rect_mask(rects):
    m=np.zeros((Ht,Wd),bool)
    for x0,y0,x1,y1 in rects: m[y0:y1,x0:x1]=True
    return m
def hue_mask(kind):
    R,G,B=rgb[...,0]/255,rgb[...,1]/255,rgb[...,2]/255
    mx=np.maximum(np.maximum(R,G),B); mn=np.minimum(np.minimum(R,G),B); d=mx-mn+1e-6
    S=np.where(mx>0,d/(mx+1e-6),0); V=mx
    H=np.where(mx==R,((G-B)/d)%6,np.where(mx==G,(B-R)/d+2,(R-G)/d+4))*60
    if kind=='dark': return V<=0.30
    if kind=='panda': return (H<=31)&(S>=0.42)&(V<=0.40)
    if kind=='notpanda':
        warm=(H>=5)&(H<=48)&(S>=0.42); white=(V>=0.78)&(S<=0.22)
        return ~(warm|white)
    if kind=='notpanda-nowhite':
        return ~((H>=5)&(H<=48)&(S>=0.42))
    raise ValueError(kind)
def poly_mask(poly,blur):
    m=Image.new('L',(Wd,Ht),0); ImageDraw.Draw(m).polygon(poly,fill=255)
    return np.asarray(m.filter(ImageFilter.GaussianBlur(blur))).astype(np.float32)/255
def cut(name,poly):
    soft=poly_mask(poly,FEATHER)
    al=alpha.copy()
    for p in PATCHES.get(name,[]):   # restore shredded parts: fully opaque inside the traced patch
        pm=poly_mask(p,0.01); al=np.maximum(al,np.where(pm>0.5,1.0,0.0))
    a=al*soft
    a=np.where(a<10/255,0.0,a)
    sil0=a>0.5; a[ndi.binary_erosion(sil0,iterations=5)]=1.0; a[~ndi.binary_dilation(sil0,iterations=5)]=0.0
    for rect,kind in HUE_ZONES.get(name,[]):
        km=hue_mask(kind)&rect_mask([rect])
        km=ndi.binary_closing(km,iterations=1)
        lab_k,nk=ndi.label(km); touch=np.unique(lab_k[ndi.binary_dilation(a<0.5,iterations=3)&km]); km=np.isin(lab_k,touch[touch>0])
        km=ndi.binary_dilation(km,iterations=3)
        a=a*(1-ndi.gaussian_filter(km.astype(np.float32),1.0))
    a=ndi.grey_erosion(a,size=(2*ERODE+1,2*ERODE+1))
    a=ndi.gaussian_filter(a,0.9)
    a=np.where(a>=0.985,1.0,np.where(a<8/255,0.0,a))
    lab,n=ndi.label(a>0); sizes=ndi.sum(np.ones_like(a),lab,range(1,n+1)); keep=np.zeros(n+1,bool); keep[1:]=sizes>=MIN_ISLAND
    a=np.where(keep[lab],a,0.0)
    holes=ndi.binary_fill_holes(a>0.5)&~(a>0.5)
    hl,hn=ndi.label(holes); hs=ndi.sum(np.ones_like(a),hl,range(1,hn+1)); hk=np.zeros(hn+1,bool); hk[1:]=hs<=2500
    a=np.where(hk[hl]&holes,1.0,a)
    out=rgb.copy()
    M=ndi.binary_erosion(a>=0.985,iterations=2).astype(np.float32)
    num=np.stack([ndi.gaussian_filter(rgb[...,i]*M,4.0) for i in range(3)],2); den=ndi.gaussian_filter(M,4.0)[...,None]
    fill=num/np.maximum(den,1e-4)
    part=((a>0)&(a<0.985)&(den[...,0]>0.02))[...,None]
    out[...,:3]=np.where(part,fill,rgb[...,:3])
    out[...,3]=np.clip(np.round(a*255),0,255)
    full=Image.fromarray(out.astype(np.uint8),'RGBA')
    bbox=Image.fromarray((a>0).astype(np.uint8)*255).getbbox()
    full.crop(bbox).save(OUT+name+'.png')
    pv=Image.new('RGBA',g.size,(247,241,232,255)); pv.alpha_composite(full); pv=pv.crop(bbox).convert('RGB')
    dk=Image.new('RGBA',g.size,(31,24,19,255)); dk.alpha_composite(full); dk=dk.crop(bbox).convert('RGB')
    sheet=Image.new('RGB',(pv.width*2+10,pv.height),'magenta'); sheet.paste(pv,(0,0)); sheet.paste(dk,(pv.width+10,0)); sheet.save(PREV+name+'-prev.png')
    pv.save(PREV+name+'-cream.png')
    lab,n=ndi.label(a>0); print(name,full.crop(bbox).size,bbox,'islands',n,'islands dropped:',int((~keep[1:]).sum()))
names=sys.argv[1:] or list(POLYS)
for n in names: cut(n,POLYS[n])
