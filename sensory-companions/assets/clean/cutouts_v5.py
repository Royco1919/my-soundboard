# v5 = v4 with HARD occlusion seams (no wide feather: the 10 px ramp smeared the big sloth's lower arm), a traced small-sloth crown edge,
#      the panda-hand top edge traced for the sloth pair, and a clone-fill of the sloth-fur remnant inside redpanda-small's tail region.
# v4 = v3 (store-photo RGB, snapped alpha) + finishing pass: zone hue-mask for neighbour-fur remnants, wide feather on occlusion seams,
#      1 px alpha erosion, de-fringe (partial-alpha pixels take the colour of the nearest opaque fur), drop alpha islands < 400 px, fill pad holes.
#      Also cuts redpanda-pair (the two red pandas, sloth masked out) with the same TOP/HAND_P seam as redpanda-small.
import numpy as np, sys
from PIL import Image, ImageDraw, ImageFilter
A='/home/user/my-soundboard/sensory-companions/assets/'
OUT=A+'clean/'
PREV='/tmp/claude-0/-home-user-my-soundboard/0bae543d-54b7-5c74-b4f4-c802d116c901/scratchpad/work/final-fix/cut/'
import os; os.makedirs(PREV,exist_ok=True)
from scipy import ndimage as ndi
g=Image.open(A+'group-cutout.png').convert('RGBA'); Wd,Ht=g.size
OX,OY=311,461  # group-cutout origin inside store-photo.jpg (found by patch matching, mean abs diff ~2)
store=np.asarray(Image.open(A+'store-photo.jpg').convert('RGB')).astype(np.float32)[OY:OY+Ht,OX:OX+Wd]
rgb=np.concatenate([store,np.zeros((Ht,Wd,1),np.float32)],2)  # straight (un-premultiplied) colour from the photo
a0=np.asarray(g).astype(np.float32)[...,3]/255.0
hard=a0>0.5
hard=ndi.binary_fill_holes(hard)                      # white felt claws / paw pads that the segmenter punched out
hard=ndi.binary_opening(hard,iterations=1)
alpha=a0.copy(); alpha[hard&(a0<0.5)]=1.0             # filled holes become opaque
inner=ndi.binary_erosion(hard,iterations=5); alpha[inner]=1.0          # no partial alpha deeper than 5 px inside
outer=~ndi.binary_dilation(hard,iterations=5); alpha[outer]=0.0        # ... or further than 5 px outside
alpha=np.where(alpha>=0.96,1.0,alpha)

# shared seam: panda hand top edge -> sloth foot / panda leg boundary (used by sloth-pair and redpanda-small)
HAND_S=[(738,934),(752,940),(768,946),(782,930),(800,915),(820,905),(845,898),(870,898),(882,905),(893,928),(897,975),(895,1050),(892,1100),(890,1112),(888,1130),(880,1140),(860,1148),(830,1152),(800,1160),(780,1172),(765,1195),(756,1225),(748,1250),(740,1280),(736,1310),(738,1335),(770,1350),(805,1365),(838,1400),(848,1450),(850,1500),(850,1708)]  # sloth side: runs through the transparent gap right of the panda hand/arm
HAND_P=[(738,946),(790,950),(840,952),(880,960),(899,995),(895,1050),(890,1100),(872,1118),(860,1128),(840,1140),(805,1150),(792,1160),(783,1170),(755,1180),(748,1200),(741,1220),(733,1240),(727,1260),(721,1280),(718,1300),(716,1335),(750,1345),(790,1385),(825,1410),(845,1450),(850,1500),(850,1708)]  # panda side: follows the panda arm's real edge along the gap
# sloth pair: top seam between the big panda's right ear and the big sloth's left ear, then the sloth arm's left edge
TOP=[(560,0),(592,80),(600,95),(596,130),(622,140),(634,165),(632,195),(624,225),(621,255),(628,270),(630,290),(645,300),(665,308),(692,330),(694,392),(725,400),(745,440),(748,500),(740,530),(730,555),(716,590),(718,620),(722,650),(724,700),(725,750),(724,800),(721,850),(726,900)]
POLYS={
 'redpanda-pair': [(0,0)]+TOP+HAND_P+[(0,1708)],
 'sloth-pair': [(1545,0)]+TOP+HAND_S+[(1545,1708)],
 'redpanda-small': [(170,700),(185,655),(200,625),(222,600),(248,598),(272,628),(300,622),(350,616),(400,612),(450,610),(500,613),(538,626),(556,600),(578,590),(598,612),(608,650),(612,700),(630,735),(655,765),(680,800),(695,850),(703,900),(712,935)]
                   +HAND_P+[(0,1708),(0,1200),(60,1080),(120,1030),(175,1020),(160,980),(145,920),(142,860),(148,800),(160,740)],
 'sloth-small': [(802,470),(812,445),(835,428),(870,420),(905,425),(940,448),(968,472),(1000,450),(1040,446),(1070,442),(1100,436),(1140,430),(1170,426),(1200,420),(1240,410),(1300,440),(1330,520),(1545,600),(1545,1708),(900,1708),(880,1450),(860,1415),(846,1380),(843,1335),(848,1305),(858,1285),(875,1265),(897,1247),(912,1230),(912,1190),(905,1160),(898,1140),(902,1115),(903,1060),(906,1000),(900,950),(896,900),(893,850),(893,800),(896,740),(895,690),(885,650),(860,640),(830,640),(808,620),(800,560),(798,500)],
}
FEATHER=0.9         # sigma of the polygon edge: ramp <= 2 px
WIDE=None           # v5: no wide feather on occlusion seams
# group-coordinate rectangles (x0,y0,x1,y1)
SOFT_ZONES={}       # v5: none
SOLID_ZONES={       # occlusion seams where the polygon IS the edge: inside the polygon the segmenter's uncertain matte is forced opaque
 'sloth-pair': [(696,560,760,990),(720,900,905,990)],
 'sloth-small': [(876,670,930,1245)],
}
CLONE_FILL={        # (polygon in group coords, (dx,dy)): a remnant of neighbour fur inside the silhouette is replaced by fur cloned from (dx,dy) px away
 'redpanda-small': [([(730,944),(745,940),(790,942),(806,950),(810,970),(796,992),(770,1000),(744,996),(732,980)],(58,14))],
}
HUE_ZONES={         # neighbour-fur remnants to knock out: (rect, kind)
 'sloth-pair': [((880,995,965,1135),'panda')],          # red-panda hand fur showing through the gap under the small sloth's claws
 'sloth-small': [((880,995,965,1135),'panda')],
 'redpanda-pair': [((590,60,790,250),'notpanda'),((590,250,790,760),'notpanda-nowhite')],    # strip of blue bag / grey counter / sloth chest fluff between the mane and the TOP seam (white ear inside allowed only at the top)
 'redpanda-small': [((590,60,790,250),'notpanda'),((590,250,790,760),'notpanda-nowhite')],
}
ERODE=4             # px of extra alpha erosion: the segmenter's matte kept a 2-3 px rim of counter/background inside the opaque area
MIN_ISLAND=1500   # anything detached and smaller than this is a fleck of counter or neighbour fur
def rect_mask(rects):
    m=np.zeros((Ht,Wd),bool)
    for x0,y0,x1,y1 in rects: m[y0:y1,x0:x1]=True
    return m
def hue_mask(kind):
    R,G,B=rgb[...,0]/255,rgb[...,1]/255,rgb[...,2]/255
    mx=np.maximum(np.maximum(R,G),B); mn=np.minimum(np.minimum(R,G),B); d=mx-mn+1e-6
    S=np.where(mx>0,d/(mx+1e-6),0); V=mx
    H=np.where(mx==R,((G-B)/d)%6,np.where(mx==G,(B-R)/d+2,(R-G)/d+4))*60
    if kind=='panda': return (H<=31)&(S>=0.42)&(V<=0.40)     # dark rust panda fur; sloth taupe shadow is H>=32 / S<0.46
    if kind=='notpanda':                                     # anything that is neither warm fur nor white ear: blue bag, grey/black counter
        warm=(H>=5)&(H<=48)&(S>=0.42); white=(V>=0.78)&(S<=0.22)   # sloth taupe is S 0.25-0.40
        return ~(warm|white)
    if kind=='notpanda-nowhite':
        return ~((H>=5)&(H<=48)&(S>=0.42))
    raise ValueError(kind)
def cut(name,poly):
    m=Image.new('L',(Wd,Ht),0); ImageDraw.Draw(m).polygon(poly,fill=255)
    soft=np.asarray(m.filter(ImageFilter.GaussianBlur(FEATHER))).astype(np.float32)/255
    if name in SOFT_ZONES:
        wide=np.asarray(m.filter(ImageFilter.GaussianBlur(WIDE))).astype(np.float32)/255
        z=ndi.gaussian_filter(rect_mask(SOFT_ZONES[name]).astype(np.float32),3)   # soft-edged zone so the two feathers blend
        soft=soft*(1-z)+wide*z
    a=alpha*soft
    if name in SOLID_ZONES:
        zm=rect_mask(SOLID_ZONES[name])&(soft>0.999)&(alpha>0.25)
        a=np.where(zm,1.0,a)
    a=np.where(a<10/255,0.0,a)
    sil0=a>0.5; a[ndi.binary_erosion(sil0,iterations=5)]=1.0; a[~ndi.binary_dilation(sil0,iterations=5)]=0.0
    # wide-feather zones: let the long ramp through again (the snap above clamps it to 5 px)
    if name in SOFT_ZONES:
        a=np.where(z>0.5,alpha*soft,a)
    # 1) neighbour-fur remnants inside the silhouette
    for rect,kind in HUE_ZONES.get(name,[]):
        km=hue_mask(kind)&rect_mask([rect])
        km=ndi.binary_closing(km,iterations=1)
        # only knock out what is connected to the outside (the seam side): never punch holes into shadowed fur deeper inside
        lab_k,nk=ndi.label(km); touch=np.unique(lab_k[ndi.binary_dilation(a<0.5,iterations=3)&km]); km=np.isin(lab_k,touch[touch>0])
        km=ndi.binary_dilation(km,iterations=3)
        a=a*(1-ndi.gaussian_filter(km.astype(np.float32),1.0))
    # 2) erode ERODE px (kills the grey background rim inside the matte), then smooth the ramp
    a=ndi.grey_erosion(a,size=(2*ERODE+1,2*ERODE+1))
    a=ndi.gaussian_filter(a,0.7)
    a=np.where(a>=0.985,1.0,np.where(a<8/255,0.0,a))
    # 2b) occlusion seams: re-snap to a hard edge (ramp ~2 px) - the matte + erosion + blur otherwise leave an 8-10 px ramp
    if name in SOLID_ZONES:
        snap=ndi.gaussian_filter((a>0.5).astype(np.float32),0.6)
        a=np.where(rect_mask(SOLID_ZONES[name]),snap,a)
    # 3) drop detached alpha islands, fill small holes (toe pads)
    lab,n=ndi.label(a>0); sizes=ndi.sum(np.ones_like(a),lab,range(1,n+1)); keep=np.zeros(n+1,bool); keep[1:]=sizes>=MIN_ISLAND
    a=np.where(keep[lab],a,0.0)
    holes=ndi.binary_fill_holes(a>0.5)&~(a>0.5)
    hl,hn=ndi.label(holes); hs=ndi.sum(np.ones_like(a),hl,range(1,hn+1)); hk=np.zeros(hn+1,bool); hk[1:]=hs<=2500
    a=np.where(hk[hl]&holes,1.0,a)
    # 3b) clone-fill remnants of neighbour fur inside the silhouette
    for poly_c,(dx,dy) in CLONE_FILL.get(name,[]):
        cm=Image.new('L',(Wd,Ht),0); ImageDraw.Draw(cm).polygon(poly_c,fill=255)
        cmf=np.asarray(cm.filter(ImageFilter.GaussianBlur(2.0))).astype(np.float32)/255
        shifted=np.roll(np.roll(rgb,-dy,axis=0),-dx,axis=1)
        rgb[...,:3]=rgb[...,:3]*(1-cmf[...,None])+shifted[...,:3]*cmf[...,None]
    # 4) de-fringe: partial pixels take the colour of nearby opaque fur
    out=rgb.copy()
    M=ndi.binary_erosion(a>=0.985,iterations=2).astype(np.float32)   # colour source: fur at least 2 px inside the opaque area
    num=np.stack([ndi.gaussian_filter(rgb[...,i]*M,4.0) for i in range(3)],2); den=ndi.gaussian_filter(M,4.0)[...,None]
    fill=num/np.maximum(den,1e-4)
    part=((a>0)&(a<0.985)&(den[...,0]>0.02))[...,None]
    out[...,:3]=np.where(part,fill,rgb[...,:3])
    out[...,3]=np.clip(np.round(a*255),0,255)
    im=Image.fromarray(out.astype(np.uint8),'RGBA')
    bbox=Image.fromarray((a>0).astype(np.uint8)*255).getbbox()
    im=im.crop(bbox); im.save(OUT+name+'.png')
    pv=Image.new('RGBA',g.size,(247,241,232,255)); pv.alpha_composite(Image.fromarray(out.astype(np.uint8),'RGBA')); pv=pv.crop(bbox).convert('RGB')
    dk=Image.new('RGBA',g.size,(31,24,19,255)); dk.alpha_composite(Image.fromarray(out.astype(np.uint8),'RGBA')); dk=dk.crop(bbox).convert('RGB')
    al=Image.fromarray(out[...,3].astype(np.uint8)).crop(bbox).convert('RGB')
    sheet=Image.new('RGB',(pv.width*3+20,pv.height),'magenta'); sheet.paste(pv,(0,0)); sheet.paste(dk,(pv.width+10,0)); sheet.paste(al,(pv.width*2+20,0)); sheet.save(PREV+name+'-prev.png')
    pg=Image.new('RGBA',g.size,(247,241,232,255)); pg.alpha_composite(g); ImageDraw.Draw(pg).line(poly+[poly[0]],fill=(255,0,0,255),width=3); pg.crop(bbox).convert('RGB').save(PREV+name+'-poly.png')
    aa=out[...,3]; partial=((aa>0)&(aa<255)).mean()*100
    print(name,im.size,bbox,'partial-alpha %',round(partial,2),'islands dropped:',int((~keep[1:]).sum()))
names=sys.argv[1:] or list(POLYS)
for n in names: cut(n,POLYS[n])
