# Driftgate Beyond: the makers' logos for review (7 Nov 2026): the twelve makers' marks in their accents, then the twelve spare
# marks a reborn maker takes (each in three makers' accents), every one also at the 20 px size the game's icons use.
# Usage: python3 tools/previews/corp_logos_sheet.py  ->  tools/previews/beyond_corp_logos.png
import os,sys,re
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from beyond_corp import LOGOS,SPARE_LOGOS,MAKERS,logo_names
HERE=os.path.dirname(os.path.abspath(__file__))
NAMES=logo_names()
BG=(10,12,20);INK=(220,224,232);DIM=(140,146,164)
def hexc(h):return tuple(int(h[i:i+2],16) for i in (1,3,5))
def board(logo,col,px,rim=True):
    # the game's look: a dark board with an accent rim and the glyph lit in the accent (drawn 4x and scaled down)
    S=4;W=px*S;im=Image.new('RGB',(W,W),(14,18,30));d=ImageDraw.Draw(im);c=hexc(col)
    if rim:d.rectangle([0,0,W-1,W-1],outline=c,width=max(S,W//22))
    k=W/2*.78
    for P in LOGOS[logo]:d.polygon([(W/2+x*k,W/2-y*k) for x,y in P],fill=c)
    return im.resize((px,px),Image.LANCZOS)
def font(n):
    for f in ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/usr/share/fonts/dejavu/DejaVuSans.ttf'):
        if os.path.exists(f):return ImageFont.truetype(f,n)
    return ImageFont.load_default()
F1,F2,F3=font(22),font(13),font(11)
BIG,SMALL=104,20;CELL=150;COLS=6
cur=[(m,name,col) for m,name,home,col in MAKERS]
ACC=[c for _,_,_,c in MAKERS]
# each spare in three accents from different homes
TRIO=[('#3fb8e6','#e8583a','#e9dc9a'),('#72efbe','#9b7bff','#f2a24e'),('#ffa040','#d6a4ff','#c6d28e')]
sp=list(SPARE_LOGOS)
rows1=(len(cur)+COLS-1)//COLS;rows2=(len(sp)+3)//4
H=70+rows1*(CELL+44)+60+rows2*(CELL+40)+20;W=COLS*CELL+40
sheet=Image.new('RGB',(max(W,4*(3*112+60)+40),H),BG);d=ImageDraw.Draw(sheet)
d.text((20,16),"The makers' marks: the twelve in use, in their accents (with the 20 px icon)",fill=INK,font=F1)
y0=60
for i,(m,name,col) in enumerate(cur):
    x=20+(i%COLS)*CELL;y=y0+(i//COLS)*(CELL+44)
    sheet.paste(board(m,col,BIG),(x,y));sheet.paste(board(m,col,SMALL),(x+BIG+8,y+BIG-SMALL))
    d.text((x,y+BIG+6),name,fill=INK,font=F2);w=NAMES[m].split(' ');l1=' '.join(w[:3]);l2=' '.join(w[3:])
    d.text((x,y+BIG+22),l1,fill=DIM,font=F3);d.text((x,y+BIG+35),l2,fill=DIM,font=F3)
y0+=rows1*(CELL+44)+10
d.text((20,y0),"Spare marks for a reborn maker (each in three makers' accents, with the 20 px icon)",fill=INK,font=F1);y0+=44
CW=3*112+60
for i,k in enumerate(sp):
    x=20+(i%4)*CW;y=y0+(i//4)*(CELL+40);cols=TRIO[i%3]
    for j,c in enumerate(cols):
        sheet.paste(board(k,c,96),(x+j*104,y));sheet.paste(board(k,c,SMALL),(x+j*104+38,y+102))
    d.text((x,y+128),f"{k}: {NAMES[k]}",fill=INK,font=F2)
out=os.path.join(HERE,'beyond_corp_logos.png');sheet.save(out);print('wrote',out)
