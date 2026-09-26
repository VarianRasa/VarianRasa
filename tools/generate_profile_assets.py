"""Generate profile artwork. Requires Pillow and Nimbus Sans fonts (fonts-urw-base35 on Debian)."""
from pathlib import Path
from math import sin, cos, pi, hypot
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)
W, N = 1120, 48
BG = (14, 17, 23)
PANEL = (19, 23, 31)
LINE = (46, 52, 64)
WHITE = (242, 242, 244)
GRAY = (157, 165, 181)
LILAC = (181, 170, 246)
GREEN = (149, 197, 172)
FONT_DIR = Path('/usr/share/fonts/opentype/urw-base35')

def font(size, bold=False):
    return ImageFont.truetype(str(FONT_DIR / ('NimbusSans-Bold.otf' if bold else 'NimbusSans-Regular.otf')), size)

def text(d, xy, value, size=22, color=WHITE, bold=False, anchor='lt'):
    d.text(xy, value, fill=color, font=font(size, bold), anchor=anchor)

def panel(h):
    im = Image.new('RGB', (W, h), BG)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((1, 1, W-2, h-2), radius=20, outline=LINE, width=2)
    return im, d

def arrow(d, x, y, color=LILAC, size=19):
    d.line((x,y+size,x+size,y),fill=color,width=2)
    d.line((x,y,x+size,y,x+size,y+size),fill=color,width=2)

def pulse(d, x, y, phase, color=LILAC):
    r = 4 + 2*(.5+.5*sin(phase*2*pi))
    d.ellipse((x-r,y-r,x+r,y+r),fill=color)

# A fixed palette gives clean text and small, stable GIF frame differences.
colors=[]
for end, count in [(WHITE,28),(LILAC,18),(GREEN,10),(LINE,8)]:
    for i in range(count):
        t=i/(count-1)
        colors.extend(round(a+(b-a)*t) for a,b in zip(BG,end))
palette=Image.new('P',(1,1))
palette.putpalette(colors + [0]*(768-len(colors)))

def export(name, base, animate):
    frames=[]
    for i in range(N):
        im=base.copy(); d=ImageDraw.Draw(im)
        animate(d,i/N)
        frames.append(im.quantize(palette=palette,dither=Image.Dither.NONE))
    frames[0].save(OUT/f'{name}.gif',save_all=True,append_images=frames[1:],duration=100,loop=0,disposal=1,optimize=False)
    frames[N//3].convert('RGB').save(ROOT/f'{name}-preview.png')
    print(name, (OUT/f'{name}.gif').stat().st_size)

# HERO
base,d=panel(390)
text(d,(48,34),'VARIAN / WARRICK',16,LILAC,True)
text(d,(1072,34),'DESIGN & DEVELOPMENT',15,GRAY,anchor='rt')
d.line((48,73,1072,73),fill=LINE,width=1)
text(d,(46,110),'Muhammad Varian',65,WHITE,True)
text(d,(46,183),'Warrick.',65,WHITE,True)
text(d,(49,276),'UI/UX Designer  ·  Flutter Developer',25,GRAY)
d.line((48,327,1072,327),fill=LINE,width=1)
text(d,(65,347),'OPEN TO UI/UX OPPORTUNITIES',15,GRAY)
text(d,(1072,347),'EXPLORE MY WORK',15,LILAC,anchor='rt')
points=[(778,117),(836,264),(902,167),(970,264),(1026,117)]
lens=[hypot(b[0]-a[0],b[1]-a[1]) for a,b in zip(points,points[1:])]
total=sum(lens)
d.line(points,fill=LINE,width=3,joint='curve')
def hero(d,p):
    pulse(d,52,354,p,GREEN)
    distance=total*(.5-.5*cos(p*2*pi))
    for a,b,length in zip(points,points[1:],lens):
        ratio=min(1,max(0,distance/length))
        end=(a[0]+(b[0]-a[0])*ratio,a[1]+(b[1]-a[1])*ratio)
        d.line([a,end],fill=LILAC,width=4)
        if distance<=length:
            d.ellipse((end[0]-5,end[1]-5,end[0]+5,end[1]+5),fill=WHITE)
            break
        distance-=length
export('profile-cover',base,hero)

# ABOUT
base,d=panel(240)
text(d,(48,31),'01 / ABOUT',15,LILAC,True)
text(d,(48,67),'Thoughtful design. Working products.',39,WHITE,True)
text(d,(48,124),'I connect user needs, clear interfaces, and hands-on development.',23,GRAY)
d.line((48,168,1072,168),fill=LINE,width=1)
text(d,(48,194),'UPN Veteran Jakarta',20,WHITE,True)
text(d,(410,194),'Jakarta Smart City',20,WHITE,True)
text(d,(790,194),'Figma · Flutter · Dart',20,WHITE,True)
def about(d,p):
    x=48+1024*(.5-.5*cos(2*pi*p))
    d.line((x-13,168,x+13,168),fill=LILAC,width=2)
export('about',base,about)

projects=[
 ('project-var','02.1 / PRODUCTIVITY','Var','A calendar that opens into a canvas.','Tasks, plans, and connected ideas — built with Flutter.','OPEN APP'),
 ('project-timer','02.2 / FITNESS','Warrieck Timer','A little structure for every workout.','AMRAP · For Time · Tabata · EMOM','OPEN APP'),
 ('project-studio','02.3 / CREATIVE TOOLS','Warrieck Studio','Upload. Refine. Share.','Edit photos and videos, then publish a public link.','OPEN APP'),
 ('project-portfolio','02.4 / PERSONAL','Portfolio','The work, and the thinking behind it.','A responsive Flutter portfolio with project detail pages.','VIEW SOURCE'),
]
for index,(name,label,title,line1,line2,action) in enumerate(projects):
    base,d=panel(244)
    text(d,(48,30),label,15,LILAC,True)
    text(d,(48,65),title,42,WHITE,True)
    text(d,(48,124),line1,25,WHITE)
    text(d,(48,163),line2,21,GRAY)
    text(d,(48,207),action,14,LILAC,True)
    arrow(d,149 if action=='OPEN APP' else 182,207,size=12)
    d.line((818,31,818,211),fill=LINE,width=1)
    # Small conceptual illustrations, not screenshots of the apps.
    if index==0:
        d.rounded_rectangle((873,57,1054,194),radius=12,fill=PANEL,outline=LINE,width=2)
        d.line((873,90,1054,90),fill=LINE,width=2)
        for x in (919,964,1009): d.line((x,91,x,194),fill=LINE,width=1)
        for y in (125,160): d.line((873,y,1054,y),fill=LINE,width=1)
        d.line((900,47,900,67),fill=GRAY,width=3);d.line((1027,47,1027,67),fill=GRAY,width=3)
        def motion(d,p):
            col=int(p*4)%4
            x=880+45*col
            d.rounded_rectangle((x,134,x+31,151),radius=5,fill=LILAC)
            pulse(d,1030,176,p,GREEN)
    elif index==1:
        d.ellipse((890,58,1036,204),outline=LINE,width=4)
        d.rounded_rectangle((946,38,980,44),radius=3,fill=GRAY)
        text(d,(963,112),'12:00',28,WHITE,True,anchor='mt')
        text(d,(963,150),'AMRAP',12,GRAY,anchor='mt')
        def motion(d,p):
            d.arc((890,58,1036,204),start=-90,end=-90+330*(.5-.5*cos(2*pi*p)),fill=LILAC,width=5)
    elif index==2:
        d.rounded_rectangle((872,55,1054,193),radius=12,fill=PANEL,outline=LINE,width=2)
        d.ellipse((1000,77,1020,97),outline=LILAC,width=2)
        d.line((886,170,932,111,977,167,1002,133,1040,170),fill=GRAY,width=3)
        def motion(d,p):
            x=881+163*(.5-.5*cos(2*pi*p))
            d.line((x,64,x,184),fill=LILAC,width=2)
            pulse(d,x,64,p)
    else:
        d.rounded_rectangle((891,52,1050,180),radius=10,outline=LINE,width=2)
        def motion(d,p):
            shift=round(4*sin(p*2*pi))
            d.rounded_rectangle((872,72+shift,1031,200+shift),radius=10,fill=PANEL,outline=GRAY,width=2)
            d.rounded_rectangle((888,89+shift,1015,124+shift),radius=4,fill=LINE)
            d.line((888,143+shift,1008,143+shift),fill=LILAC,width=3)
            d.line((888,160+shift,966,160+shift),fill=GRAY,width=2)
            d.line((888,177+shift,987,177+shift),fill=LINE,width=2)
    export(name,base,motion)

# CONTACT
base,d=panel(218)
text(d,(48,30),'03 / CONTACT',15,LILAC,True)
text(d,(48,74),"Let's make something useful.",44,WHITE,True)
text(d,(48,142),'UI/UX opportunities · Product ideas · Collaborations',23,GRAY)
text(d,(48,184),'M.VARIANWARRICK04@GMAIL.COM',16,LILAC)
d.ellipse((970,70,1050,150),outline=LINE,width=2)
def contact(d,p):
    shift=3*sin(p*2*pi)
    arrow(d,996+shift,96-shift,size=28)
export('contact',base,contact)

# A compact contact sheet is used only for local visual review.
names=['profile-cover','about']+[p[0] for p in projects]+['contact']
imgs=[Image.open(ROOT/f'{n}-preview.png') for n in names]
sheet=Image.new('RGB',(W,sum(im.height+24 for im in imgs)+24),(13,17,23))
y=24
for im in imgs:
    sheet.paste(im,(0,y)); y+=im.height+24
sheet.resize((700,round(sheet.height*700/W)),Image.Resampling.LANCZOS).save(ROOT/'landing-preview.png')
