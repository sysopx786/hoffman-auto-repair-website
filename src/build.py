#!/usr/bin/env python3
"""Static site generator for Dave Hoffman Auto Repair. Run: python3 src/build.py  (from site root)"""
import json, re, html, os, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
C=json.load(open(ROOT/'src/site.config.json'))
CATS=json.load(open(ROOT/'src/services.json'))
NAME=C['name']; PH=C['phoneDisplay']; TEL=C['phoneTel']
BASE=C['baseUrl']
esc=lambda s:html.escape(s,quote=True)
def slug(s): return re.sub(r'(^-|-$)','',re.sub(r'[^a-z0-9]+','-',s.lower().replace('&','and')))
# normalize name in titles/meta
for c in CATS:
    c['title']=c['title'].replace('Hoffman Dave Auto Repair',NAME); c['meta']=c['meta'].replace('Hoffman Dave Auto Repair',NAME)
    c['slug']=c['url'].strip('/')
    for s in c['services']: s['slug']=slug(s['name'])
SV={}
for c in CATS:
    for s in c['services']: SV[s['name']]=(c,s)
ICON={'/inspections-emissions':'shield','/towing-hauling':'truck','/roadside-recovery':'lifebuoy','/property-parking-impound':'parking','/recycling-salvage':'recycle','/engine-drivetrain':'gear','/cooling-heating-corrosion':'therm','/tires-wheels-suspension':'tire','/body-glass-imports':'car'}
SHORT={'/inspections-emissions':'Inspections & Emissions','/towing-hauling':'Towing & Hauling','/roadside-recovery':'Roadside & Recovery','/property-parking-impound':'Property, Parking & Impound','/recycling-salvage':'Recycling & Salvage','/engine-drivetrain':'Engine & Drivetrain','/cooling-heating-corrosion':'Cooling, Heating & Corrosion','/tires-wheels-suspension':'Tires, Wheels & Suspension','/body-glass-imports':'Body, Glass & Imports'}
REL={
'Vehicle Safety Inspections':['Pre-Purchase Inspections','Tires','Windshield Wiper Replacement'],
'Emissions Testing':['Emissions Control','On Board Computer Specialists'],
'Emissions Control':['Emissions Testing','On Board Computer Specialists','Spark Plugs'],
'Pre-Purchase Inspections':['Vehicle Safety Inspections','Imports'],
'Engine Service & Repair':['Cylinder Head & Block Repair','Cooling Systems','Spark Plugs','On Board Computer Specialists'],
'Cylinder Head & Block Repair':['Engine Service & Repair','Cooling Systems'],
'Cooling Systems':['Engine Service & Repair','Heating System Service & Repair','Freon & Coolant Recycling'],
'Heating System Service & Repair':['Cooling Systems'],
'Freon & Coolant Recycling':['Cooling Systems','Oil Recycling'],
'Alternator Installation & Repair':['Jump Starts','Battery Recycling'],
'Jump Starts':['Battery Recycling','Roadside Assistance','Alternator Installation & Repair'],
'Battery Recycling':['Jump Starts','Alternator Installation & Repair','Oil Recycling'],
'Oil Recycling':['Battery Recycling','Tire Recycling','Freon & Coolant Recycling'],
'Tire Recycling':['Tires','Oil Recycling'],
'Lockout Services':['Roadside Assistance','Salvage Keys Made'],
'Salvage Keys Made':['Lockout Services','Junk Car Removal'],
'Roadside Assistance':['Jump Starts','Lockout Services','Light Duty Towing'],
'Tires':['Tire Repair','Tire Rotation','Wheels','Tire Recycling'],
'Tire Repair':['Tires','Tire Rotation'],
'Tire Rotation':['Tires','Ball Joints'],
'Wheels':['Wheel Repair','Tires'],'Wheel Repair':['Wheels','Tires'],
'Ball Joints':['Tire Rotation','Tires'],'Retreads':['Tires','Heavy Duty Towing'],
'Collision Services':['Insurance Towing','Auto Glass Installation & Repair','Light Duty Towing'],
'Auto Glass Installation & Repair':['Collision Services','Windshield Wiper Replacement'],
'Windshield Wiper Replacement':['Auto Glass Installation & Repair','Vehicle Safety Inspections'],
'Imports':['On Board Computer Specialists','Pre-Purchase Inspections'],
'Winching':['Four Wheel Drive Vehicle Recovery','Underwater Recovery','Flat Bed Truck Service'],
'Four Wheel Drive Vehicle Recovery':['Winching','Flat Bed Truck Service'],
'Underwater Recovery':['Winching','Insurance Towing'],
'Light Duty Towing':['Flat Bed Truck Service','Wheel Lift Towing','Insurance Towing','Roadside Assistance'],
'Heavy Duty Towing':['Motor Home & RV Recovery','Flat Bed Truck Service','Long Distance Towing'],
'Flat Bed Truck Service':['Rollback Towing','Wheel Lift Towing','Motorcycle Recovery'],
'Rollback Towing':['Flat Bed Truck Service','Wheel Lift Towing'],
'Wheel Lift Towing':['Flat Bed Truck Service','Light Duty Towing'],
'Long Distance Towing':['Heavy Duty Towing','Insurance Towing'],
'Insurance Towing':['Collision Services','Light Duty Towing','Vehicle Storage'],
'Motorcycle Recovery':['Flat Bed Truck Service'],'Motor Home & RV Recovery':['Heavy Duty Towing'],
'Storage Shed Moving':['Heavy Duty Towing'],
'Parking Lot Towing':['Parking Lot Enforcement','Blocked Driveway Towing','Impound Services'],
'Parking Enforcement':['Parking Lot Enforcement','Parking Lot Towing'],
'Parking Lot Enforcement':['Parking Enforcement','Parking Lot Surveillance'],
'Parking Lot Surveillance':['Parking Lot Enforcement','Parking Lot Towing'],
'Blocked Driveway Towing':['Parking Lot Towing','Impound Services'],
'Abandoned Vehicle Recovery':['Junk Car Removal','Impound Services'],
'Impound Services':['Vehicle Storage','Parking Lot Towing'],
'Vehicle Storage':['Impound Services','Insurance Towing'],
'Repossessions':['Impound Services','Vehicle Storage'],
'Junk Car Removal':['Abandoned Vehicle Recovery','Salvage Keys Made'],
'Fuel System Service & Repair':['Gas Tanks','Spark Plugs','Engine Service & Repair'],
'Gas Tanks':['Fuel System Service & Repair'],'Spark Plugs':['Engine Service & Repair','Fuel System Service & Repair'],
'On Board Computer Specialists':['Emissions Testing','Engine Service & Repair'],
'Differential Repair':['Axles'],'Axles':['Differential Repair','Ball Joints'],
'Corrosion Control':['Collision Services','Cooling Systems'],
}
SAFE=re.compile(r'\b(safe|unsafe|dangerous|pull over|stop driving|911|fire|fumes|overheat)',re.I)

SPRITE='''<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true"><defs>
<symbol id="i-phone" viewBox="0 0 24 24"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></symbol>
<symbol id="i-pin" viewBox="0 0 24 24"><path d="M12 21s7-6.2 7-11a7 7 0 1 0-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/></symbol>
<symbol id="i-clock" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></symbol>
<symbol id="i-search" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></symbol>
<symbol id="i-arrow" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></symbol>
<symbol id="i-check" viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7"/></symbol>
<symbol id="i-chev" viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></symbol>
<symbol id="i-menu" viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></symbol>
<symbol id="i-shield" viewBox="0 0 24 24"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/></symbol>
<symbol id="i-truck" viewBox="0 0 24 24"><path d="M2 7h12v9H2zM14 10h4l3 3v3h-7"/><circle cx="6.5" cy="17.5" r="2"/><circle cx="17.5" cy="17.5" r="2"/></symbol>
<symbol id="i-lifebuoy" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><path d="M5.6 5.6l3.6 3.6M14.8 14.8l3.6 3.6M18.4 5.6l-3.6 3.6M9.2 14.8l-3.6 3.6"/></symbol>
<symbol id="i-parking" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="4"/><path d="M10 16V8h3a2.5 2.5 0 0 1 0 5h-3"/></symbol>
<symbol id="i-recycle" viewBox="0 0 24 24"><path d="M20 12a8 8 0 1 1-2.4-5.7M20 4v4h-4"/></symbol>
<symbol id="i-gear" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3.2"/><circle cx="12" cy="12" r="6.5"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.3 5.3l2.1 2.1M16.6 16.6l2.1 2.1M18.7 5.3l-2.1 2.1M7.4 16.6l-2.1 2.1"/></symbol>
<symbol id="i-therm" viewBox="0 0 24 24"><path d="M10 14.5V5a2 2 0 0 1 4 0v9.5a4 4 0 1 1-4 0z"/><path d="M12 9v7"/></symbol>
<symbol id="i-tire" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/><path d="M12 3v6M12 15v6M3 12h6M15 12h6"/></symbol>
<symbol id="i-car" viewBox="0 0 24 24"><path d="M3 15l2-6a2 2 0 0 1 2-1.5h10a2 2 0 0 1 2 1.5l2 6v3H3z"/><path d="M3 15h18"/><circle cx="7.5" cy="18" r="1.8"/><circle cx="16.5" cy="18" r="1.8"/></symbol>
<symbol id="i-camera" viewBox="0 0 24 24"><path d="M3 8h4l2-3h6l2 3h4v11H3z"/><circle cx="12" cy="13" r="3.5"/></symbol>
<symbol id="i-user" viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></symbol>
<symbol id="i-info" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/></symbol>
<symbol id="i-close" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></symbol>
</defs></svg>'''
def ic(n,cls=''): return f'<svg class="icon {cls}" aria-hidden="true"><use href="#i-{n}"/></svg>'

def rel(depth): return '../'*depth
def pagepath(url): return url.strip('/')
def link(url,depth,frag=''):
    p=pagepath(url)
    return rel(depth)+(p+'/' if p else '')+frag

def svc_index(depth):
    out=[]
    for c in CATS:
        for s in c['services']:
            out.append({'n':esc(s['name']),'c':esc(SHORT[c['url']]),'u':f"{c['slug']}/#{s['slug']}"})
    return out

def head(page,depth,title,desc,url,ld=None,og_type='website'):
    r=rel(depth); canon=BASE+(url if url!='/' else '/')+('' if url.endswith('/') else '/') if url!='/' else BASE+'/'
    ld_s=''.join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False)}</script>\n' for x in (ld or []))
    return f'''<!doctype html>
<html lang="en" data-base="{r}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#1B2D4F">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{BASE}/assets/img/og-image.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{BASE}/assets/img/og-image.jpg">
<link rel="icon" href="{r}assets/img/favicon.svg" type="image/svg+xml"><link rel="icon" href="{r}assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{r}assets/img/apple-touch-icon.png">
<link rel="preload" href="{r}assets/fonts/bricolage.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{r}assets/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{r}assets/css/site.css">
<script>document.documentElement.classList.add('js')</script>
{ld_s}</head>
'''

def header(depth,current):
    r=rel(depth)
    def a(label,url,key): 
        cur=' aria-current="page"' if current==key else ''
        return f'<a href="{link(url,depth)}"{cur}>{label}</a>'
    mega=''.join(f'<a href="{link(c["url"],depth)}">{ic(ICON[c["url"]])}<span><b>{esc(SHORT[c["url"]])}</b><small>{len(c["services"])} services</small></span></a>' for c in CATS)
    return f'''<body>
<a class="skip" href="#main">Skip to content</a>
{SPRITE}
<header class="hdr"><div class="wrap">
<a class="brand" href="{link('/',depth)}" aria-label="{NAME}, home"><picture><source media="(prefers-color-scheme: dark)" srcset="{r}assets/img/logo-flat-dark.svg"><img src="{r}assets/img/logo-flat.svg" alt="{NAME}" width="236" height="77"></picture></a>
<nav class="nav" id="nav" aria-label="Main">
{a('Home','/','home')}
<div class="has-mega"><button type="button" aria-expanded="false" aria-controls="mega"{' aria-current="true"' if current=='services' else ''}>Services {ic('chev')}</button>
<div class="mega" id="mega">{mega}<a class="all" href="{link('/services',depth)}"><span><b>See all services</b><small>Browse by category or search the list</small></span>{ic('arrow')}</a></div></div>
{a('PA Inspections','/inspections-emissions','insp')}
{a('About','/about','about')}
{a('Reviews','/reviews','reviews')}
{a('Contact','/contact','contact')}
</nav>
<div class="hdr-actions">
<button class="kbd-btn" type="button" data-open-pal aria-label="Find a service (shortcut: slash)">{ic('search')}<span class="lbl">Find a service</span><kbd>/</kbd></button>
<a class="btn btn-call btn-sm" href="tel:{TEL}">{ic('phone')} Call {PH}</a>
<button class="burger" type="button" aria-expanded="false" aria-controls="nav" aria-label="Open menu">{ic('menu')}</button>
</div></div></header>
'''

def footer(depth):
    r=rel(depth)
    cl=''.join(f'<li><a href="{link(c["url"],depth)}">{esc(SHORT[c["url"]])}</a></li>' for c in CATS[:5])
    cl2=''.join(f'<li><a href="{link(c["url"],depth)}">{esc(SHORT[c["url"]])}</a></li>' for c in CATS[5:])
    idx=json.dumps(svc_index(depth),ensure_ascii=False)
    return f'''
<nav class="mbar" aria-label="Quick contact"><a class="btn btn-call" href="tel:{TEL}">{ic('phone')} Call {PH}</a><a class="btn btn-ghost" href="https://www.google.com/maps/dir/?api=1&amp;destination={C['lat']},{C['lng']}" rel="noopener">{ic('pin')} Directions</a></nav>
<footer class="ftr"><div class="wrap"><div class="ftr-grid">
<div><a class="brand" href="{link('/',depth)}" aria-label="{NAME}, home"><img src="{r}assets/img/logo-flat-dark.svg" alt="{NAME}" width="172" height="56"></a>
<p style="margin-top:1rem">{C['street']}<br>{C['city']}, {C['region']} {C['zip']}</p>
<p><a href="tel:{TEL}">{PH}</a><br>{C['hoursShort']}<br>Closed Sat–Sun</p></div>
<div><h2>Services</h2><ul>{cl}</ul></div>
<div><h2>More services</h2><ul>{cl2}</ul></div>
<div><h2>Company</h2><ul><li><a href="{link('/about',depth)}">About</a></li><li><a href="{link('/reviews',depth)}">Reviews</a></li><li><a href="{link('/contact',depth)}">Contact</a></li><li><a href="{link('/services',depth)}">All services</a></li><li><a href="{link('/privacy',depth)}">Privacy</a></li></ul></div>
</div><div class="legal"><span>© <span id="yr">2026</span> {NAME}. Official Pennsylvania inspection station (OIS #{C['ois']}).</span><span>{C['street']}, {C['city']}, {C['region']}</span></div></div></footer>
<dialog class="pal" id="pal" aria-label="Find a service"><div class="pal-in">{ic('search')}<input type="text" placeholder="Search 58 services…" aria-label="Search services" autocomplete="off"><button class="kbd-btn" type="button" onclick="this.closest('dialog').close()" aria-label="Close search">{ic('close')}</button></div><ul class="pal-list"></ul></dialog>
<script>window.__SERVICES={idx};document.getElementById('yr').textContent=new Date().getFullYear()</script>
<script src="{r}assets/js/site.js" defer></script>
</body></html>
'''

def cta(depth,title='Need your car looked at?',text=None):
    text=text or f'Call us {C["hoursShort"]}.'
    return f'''<div class="cta rv"><div><h2>{title}</h2><p>{text}</p></div><div class="cta-row" style="margin:0"><a class="btn btn-call" href="tel:{TEL}">{ic('phone')} Call {PH}</a><a class="btn btn-ghost btn-onDark" href="https://www.google.com/maps/dir/?api=1&amp;destination={C['lat']},{C['lng']}" rel="noopener">{ic('pin')} Get directions</a></div></div>'''

def crumbs(items):
    return '<nav aria-label="Breadcrumb"><ol class="crumbs">'+''.join((f'<li><a href="{u}">{esc(t)}</a></li>' if u else f'<li aria-current="page">{esc(t)}</li>') for t,u in items)+'</ol></nav>'
def bc_ld(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":t,"item":BASE+u} for i,(t,u) in enumerate(items)]}

def write(url,content):
    p=ROOT/(pagepath(url)) if url!='/' else ROOT
    p.mkdir(parents=True,exist_ok=True); (p/'index.html').write_text(content,encoding='utf-8')

def autolink_phone(t):
    return esc(t).replace(PH,f'<a href="tel:{TEL}">{PH}</a>')

# ---------------- pages ----------------
def local_ld():
    return {"@context":"https://schema.org","@type":"AutoRepair","name":NAME,"url":BASE+"/","image":BASE+"/assets/img/og-image.jpg","telephone":"+1-484-921-0715",
     "address":{"@type":"PostalAddress","streetAddress":C['street'],"addressLocality":C['city'],"addressRegion":C['region'],"postalCode":C['zip'],"addressCountry":"US"},
     "geo":{"@type":"GeoCoordinates","latitude":C['lat'],"longitude":C['lng']},
     "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"08:00","closes":"18:00"}]}

def page_home():
    d=0
    title='Auto Repair, Towing & PA Inspections in Phoenixville, PA | Dave Hoffman Auto Repair'
    desc='Family-run auto repair, towing, and Pennsylvania inspections at 42 Ridge Rd, Phoenixville. Honest advice, fair pricing. Open Mon–Fri 8–6.'
    h=head('home',d,title,desc,'/',[local_ld()])+header(d,'home')
    cards=''
    for c in CATS:
        smp=''.join(f'<li>{esc(s["name"])}</li>' for s in c['services'][:3])
        cards+=f'''<a class="card rv" href="{link(c['url'],d)}"><span class="ico">{ic(ICON[c['url']])}</span><span class="meta">{len(c['services'])} services</span><h3>{esc(SHORT[c['url']])}</h3><p>{esc(c['intro'])}</p><ul class="samples">{smp}</ul><span class="more">Explore {ic('arrow')}</span></a>'''
    names=[s['name'] for c in CATS for s in c['services']]
    mq=''.join(f'<span>{esc(n)}</span>' for n in names)
    h+=f'''<main id="main">
<section class="hero"><div class="wrap hero-grid">
<div><span class="eyebrow">Phoenixville, Pennsylvania</span>
<h1>Honest auto repair <span class="hl">in Phoenixville.</span></h1>
<p class="lede">A family-run shop where you get a clear explanation, a fair price, and no work you didn't agree to.</p>
<div class="cta-row"><a class="btn btn-call" href="tel:{TEL}">{ic('phone')} Call the shop</a><a class="btn btn-ghost btn-onDark" href="https://www.google.com/maps/dir/?api=1&amp;destination={C['lat']},{C['lng']}" rel="noopener">{ic('pin')} Get directions</a></div>
<p style="margin-top:1.4rem"><span class="status" data-status><i></i><span class="t">{C['hoursShort']}</span></span></p></div>
<div class="hero-card"><picture><img src="assets/img/logo-dimensional-720.webp" srcset="assets/img/logo-dimensional-540.webp 540w, assets/img/logo-dimensional-720.webp 720w, assets/img/logo-dimensional-1440.webp 1440w" sizes="(max-width:900px) 90vw, 520px" width="720" height="{round(720*1289/2471)}" alt="{NAME} logo"></picture>
<span class="chip c2">{ic('shield')} Official PA inspection station · OIS #{C['ois']}</span>
<span class="chip c1">{ic('pin')} {C['street']}, {C['city']}</span></div>
</div></section>
<div class="wrap"><div class="strip rv">
<div><b>Straight answers.</b><p>We explain what's wrong and what it takes to fix it.</p></div>
<div><b>Fair pricing.</b><p>Customers tell us it's a big reason they come back.</p></div>
<div><b>Family trust.</b><p>Some customers have brought their cars here for decades, and now bring their kids.</p></div></div></div>
<section><div class="wrap"><div class="sec-head rv"><div><span class="eyebrow">What we do</span><h2>One shop for the whole car.</h2></div><p>Repair, inspection, and towing at one Ridge Road location.</p></div>
<div class="bento">
<a class="card tall w3 rv" href="{link('/engine-drivetrain',d)}"><span class="ico">{ic('gear')}</span><h3>Auto repair, major and minor</h3><p>Engine, fuel, drivetrain, cooling, tires, and body work.</p><span class="more">Engine &amp; drivetrain {ic('arrow')}</span></a>
<a class="card tall w3 rv" href="{link('/inspections-emissions',d)}"><span class="ico">{ic('shield')}</span><h3>Pennsylvania state inspection and emissions (OBD) testing</h3><p>Official inspection station, OIS #{C['ois']}.</p><span class="more">PA inspections {ic('arrow')}</span></a>
<a class="card w3 rv" href="{link('/services',d)}"><span class="ico">{ic('tire')}</span><h3>Routine maintenance</h3><p>Tires, rotation, wipers, spark plugs, and more. Call to confirm your job.</p><span class="more">See all services {ic('arrow')}</span></a>
<a class="card w3 rv" href="{link('/towing-hauling',d)}"><span class="ico">{ic('truck')}</span><h3>Towing, roadside help, and vehicle recovery</h3><p>Light and heavy duty, flatbed, winching, jump starts, and lockouts.</p><span class="more">Towing &amp; hauling {ic('arrow')}</span></a>
</div></div></section>
<div class="marquee"><div class="marquee-track" aria-hidden="true">{mq}{mq}</div></div>
<section><div class="wrap"><div class="sec-head rv"><div><span class="eyebrow">Services</span><h2>Nine categories. Fifty-eight services.</h2></div><p>Find your job by category, or press <b>/</b> to search the full list.</p></div>
<div class="grid3">{cards}</div>
<p style="margin-top:2rem" class="rv"><a class="btn btn-ghost" href="{link('/services',d)}">Browse all services {ic('arrow')}</a></p></div></section>
<section class="band"><div class="wrap split">
<div class="rv"><span class="eyebrow" style="color:#9BD6E3">PA inspections</span><h2>Pennsylvania inspections, done here.</h2>
<p>We're an official Pennsylvania inspection station (OIS #{C['ois']}). We offer OBD emissions testing and trailer inspections. Call to confirm we can inspect your vehicle type.</p>
<p><a class="btn btn-call" href="{link('/inspections-emissions',d)}">Inspections &amp; emissions {ic('arrow')}</a></p></div>
<div class="glass rv"><div class="big">OIS #{C['ois']}</div><p style="margin:.4rem 0 0">Official Pennsylvania inspection station</p>
<ul class="ticks"><li>{ic('check')}<span>OBD emissions testing</span></li><li>{ic('check')}<span>Trailer inspections</span></li><li>{ic('check')}<span>Inspection fees cover the inspection only. Repairs cost extra.</span></li></ul></div></div></section>
<section><div class="wrap split">
<blockquote class="quote-card rv"><p class="quote">I've been going to Dave and Mel for close to 30 years… My grandfather trusted them, I trust them, and now my son does too.</p><p class="byline">A customer review. <a href="{link('/reviews',d)}">Read more reviews</a></p></blockquote>
<div class="card rv"><span class="ico">{ic('clock')}</span><h3>Visit the shop</h3><p>{C['street']}, {C['city']}, {C['region']} {C['zip']}<br>{C['hoursLine']} · Closed Sat–Sun</p><p style="margin-top:.8rem"><a class="btn btn-ghost btn-sm" href="{link('/contact',d)}">Hours &amp; map {ic('arrow')}</a></p></div></div></section>
<section style="padding-top:0"><div class="wrap">{cta(d)}</div></section>
</main>'''+footer(d)
    write('/',h)

def page_services():
    d=1; url='/services'
    title='Auto Repair, Towing & PA Inspections in Phoenixville, PA | Dave Hoffman Auto Repair'
    desc='Browse auto repair, towing, roadside, recycling, tire, and PA inspection services at Dave Hoffman Auto Repair in Phoenixville. Call 484-921-0715.'
    items=[('Home','/'),('Services',None)]
    h=head('services',d,title,desc,url,[bc_ld([('Home','/'),('Services','/services')])])+header(d,'services')
    cards=''
    for c in CATS:
        lis=''.join(f'<li><a href="{link(c["url"],d,"#"+s["slug"])}">{esc(s["name"])}</a></li>' for s in c['services'])
        cards+=f'''<div class="card hub-card rv"><a class="card-top" href="{link(c['url'],d)}"><span class="ico">{ic(ICON[c['url']])}</span><span class="meta">{len(c['services'])} services</span><h3>{esc(SHORT[c['url']])}</h3><p>{esc(c['intro'])}</p></a>
<details><summary>Show the list {ic('chev')}</summary><ul>{lis}</ul></details></div>'''
    h+=f'''<main id="main"><div class="phero"><div class="wrap">{crumbs([('Home',link('/',d)),('Services',None)])}
<span class="eyebrow">Services</span><h1>Repair, inspection, towing: one shop.</h1>
<p class="lede">From routine repairs and Pennsylvania inspections to towing and roadside help, we handle a wide range of work at one Ridge Road location. Don't see what you need? Call and ask.</p>
<div class="finder"><label class="vh" for="finder-in">Search services</label>{ic('search')}<input id="finder-in" type="search" placeholder="Try “jump start”, “tires”, “inspection”…" autocomplete="off"><div id="finder-out" class="finder-out" aria-live="polite"></div></div></div></div>
<section style="padding-top:clamp(32px,5vw,56px)"><div class="wrap"><h2 class="vh">Service categories</h2><div class="grid3">{cards}</div>
<p class="note rv" style="margin-top:2rem">This list shows some of the services we offer. Not sure if we cover your repair? Call us {C['hoursShort']}.</p>
<div style="margin-top:2rem">{cta(d)}</div></div></section></main>'''+footer(d)
    write(url,h)

def faq_html(s,cat_slug):
    out=[]
    for i,f in enumerate(s['faqs']):
        safety=' safety' if SAFE.search(f['a']) else ''
        out.append(f'<details name="faq-{s["slug"]}"><summary>{esc(f["q"])}{ic("chev")}</summary><div class="ans{safety}">{autolink_phone(f["a"])}</div></details>')
    return '<div class="acc">'+''.join(out)+'</div>'

def page_category(c):
    d=1; url=c['url']; sh=SHORT[url]
    ld=[{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":f['q'],"acceptedAnswer":{"@type":"Answer","text":f['a']}} for s in c['services'] for f in s['faqs']]},
        bc_ld([('Home','/'),('Services','/services'),(sh,url)])]
    h=head('cat',d,c['title'],c['meta'],url,ld)+header(d,'insp' if url=='/inspections-emissions' else 'services')
    rail=''.join(f'<li><a href="#{s["slug"]}">{esc(s["name"])}</a></li>' for s in c['services'])
    chips=''.join(f'<a href="#{s["slug"]}">{esc(s["name"])}</a>' for s in c['services'])
    extra=''
    if url=='/inspections-emissions':
        extra=f'''<div class="callout rv" style="margin-bottom:2rem">{ic('shield')}<div><p><b>Official Pennsylvania inspection station (OIS #{C['ois']}).</b> OBD emissions testing and trailer inspections. Call to confirm we can inspect your vehicle type.</p><p class="note" style="margin-top:.5rem">Bring your current registration and proof of insurance. Call <a href="tel:{TEL}">{PH}</a> to book.</p></div></div>'''
    body=''
    for s in c['services']:
        rl=''
        if s['name'] in REL:
            ls=[]
            for n in REL[s['name']]:
                if n in SV:
                    cc,ss=SV[n]; ls.append(f'<a href="{link(cc["url"],d,"#"+ss["slug"]) if cc is not c else "#"+ss["slug"]}">{esc(n)}</a>')
            if ls: rl=f'<div class="rel"><span>Related:</span>{"".join(ls)}</div>'
        faqs=f'<h3 class="q">Questions about {esc(s["name"].lower() if False else s["name"])}</h3>'+faq_html(s,c['slug']) if s['faqs'] else ''
        body+=f'<article class="svc rv" id="{s["slug"]}"><h2>{esc(s["name"])}</h2><p>{esc(s["desc"])}</p>{faqs}{rl}</article>'
    others=''.join(f'<a href="{link(o["url"],d)}">{ic(ICON[o["url"]])}{esc(SHORT[o["url"]])}</a>' for o in CATS if o is not c)
    h+=f'''<main id="main"><div class="phero"><div class="wrap">{crumbs([('Home',link('/',d)),('Services',link('/services',d)),(sh,None)])}
<span class="eyebrow">{len(c['services'])} services</span><h1>{esc(sh)}</h1><p class="lede">{esc(c['intro'])}</p>
<div class="meta-row"><span class="pill">{ic('pin')} {C['street']}, {C['city']}</span><span class="pill">{ic('clock')} {C['hoursShort']}</span><a class="btn btn-call btn-sm" href="tel:{TEL}">{ic('phone')} Call {PH}</a></div></div></div>
<nav class="chips" data-spy aria-label="Services in this category">{chips}</nav>
<div class="wrap cat-layout"><aside class="rail" data-spy><h2>In this category</h2><ol>{rail}</ol><a class="btn btn-call btn-sm call" href="tel:{TEL}">{ic('phone')} Call {PH}</a></aside>
<div>{extra}{body}</div></div>
<section><div class="wrap">{cta(d,f'Questions about {sh.lower()}?',f'Call us {C["hoursShort"]}. We will tell you what we can do.')}
<h2 style="font-size:1.4rem;margin:3rem 0 1rem">Other services</h2><div class="others">{others}</div></div></section></main>'''+footer(d)
    write(url,h)

def page_about():
    d=1; url='/about'
    t='About Dave Hoffman Auto Repair | Family-Run Shop in Phoenixville'
    desc='Dave Hoffman Auto Repair is a small, family-run shop at 42 Ridge Rd in Phoenixville. Honest advice, fair pricing, and clear explanations.'
    h=head('about',d,t,desc,url,[bc_ld([('Home','/'),('About','/about')])])+header(d,'about')
    lab='<small>Photo coming</small>' if C['showPhotoComingLabel'] else ''
    slots=''.join(f'<div class="photo-slot" data-slot="{n}" role="img" aria-label="Placeholder for photo: {n}">{ic("camera")}{lab}</div>' for n in ['shop exterior','Dave','the team','the bays'])
    h+=f'''<main id="main"><div class="phero"><div class="wrap">{crumbs([('Home',link('/',d)),('About',None)])}<span class="eyebrow">About</span><h1>A family shop on Ridge Road.</h1></div></div>
<section><div class="wrap split"><div class="prose rv"><p>Dave Hoffman Auto Repair is a small, family-run shop at 42 Ridge Rd in Phoenixville. Our customers describe us the same way: honest, fair, and easy to talk to.</p>
<p>We take the time to explain what's going on with your car. We fix what's broken, and we don't add work you haven't agreed to.</p>
<p>Many of our customers have been with us for years. Some tell us their parents and grandparents came here first. That's the kind of shop we want to be.</p>
<p><a class="btn btn-call" href="tel:{TEL}">{ic('phone')} Call {PH}</a></p></div>
<div class="grid3" style="grid-template-columns:1fr">
<div class="card rv"><span class="ico">{ic('info')}</span><h2 style="font-size:1.25rem">Straight answers</h2><p>We explain what's wrong and what it takes to fix it.</p></div>
<div class="card rv"><span class="ico">{ic('check')}</span><h2 style="font-size:1.25rem">Fair pricing</h2><p>Customers tell us it's a big reason they come back.</p></div>
<div class="card rv"><span class="ico">{ic('user')}</span><h2 style="font-size:1.25rem">Family trust</h2><p>Some customers have brought their cars here for decades, and now bring their kids.</p></div></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="slots rv">{slots}</div></div></section>
<section style="padding-top:0"><div class="wrap">{cta(d,'Stop by or call.',f'{C["street"]}, {C["city"]} · {C["hoursShort"]}')}</div></section></main>'''+footer(d)
    write(url,h)

def page_reviews():
    d=1; url='/reviews'
    t='Customer Reviews | Dave Hoffman Auto Repair in Phoenixville'
    desc='What customers say about Dave Hoffman Auto Repair in Phoenixville, PA.'
    h=head('reviews',d,t,desc,url,[bc_ld([('Home','/'),('Reviews','/reviews')])])+header(d,'reviews')
    rv=[("I've been going to Dave and Mel for close to 30 years, and that kind of loyalty doesn't happen by accident. My grandfather trusted them, I trust them, and now my son does too.",'w4'),("Reliable and trustworthy.",''),("I've known Dave for years. He's one of the best mechanics in Phoenixville.",'')]
    cards=''.join(f'<figure class="card rv {w}" style="margin:0"><blockquote><p class="quote" style="font-size:{"1.7rem" if w else "1.35rem"}">“{esc(q)}”</p></blockquote><figcaption class="byline">Customer review</figcaption></figure>' for q,w in rv)
    url_r=C['googleReviewUrl'] or f"https://www.google.com/maps/search/?api=1&query={C['lat']},{C['lng']}"
    lab='Leave us a Google review' if C['googleReviewUrl'] else 'Find us on Google Maps'
    h+=f'''<main id="main"><div class="phero"><div class="wrap">{crumbs([('Home',link('/',d)),('Reviews',None)])}<span class="eyebrow">Reviews</span><h1>What our customers say</h1></div></div>
<section><div class="wrap"><div class="bento" style="grid-template-columns:repeat(3,1fr)">{cards}</div>
<p style="margin-top:2rem"><a class="btn btn-ghost" href="{url_r}" rel="noopener">{lab} {ic('arrow')}</a></p></div></section>
<section style="padding-top:0"><div class="wrap">{cta(d)}</div></section></main>'''+footer(d)
    h=h.replace('class="bento" style="grid-template-columns:repeat(3,1fr)"','class="bento"')
    write(url,h)

def page_contact():
    d=1; url='/contact'
    t='Contact Dave Hoffman Auto Repair | 42 Ridge Rd, Phoenixville PA'
    desc='Call 484-921-0715 or stop by 42 Ridge Rd, Phoenixville, PA 19460. Open Mon–Fri 8:00 AM–6:00 PM.'
    h=head('contact',d,t,desc,url,[bc_ld([('Home','/'),('Contact','/contact')])])+header(d,'contact')
    days=[('Mon','Monday'),('Tue','Tuesday'),('Wed','Wednesday'),('Thu','Thursday'),('Fri','Friday')]
    rows=''.join(f'<tr data-d="{a}"><th scope="row">{b}</th><td>8:00 AM–6:00 PM</td></tr>' for a,b in days)+'<tr data-d="Sat"><th scope="row">Saturday</th><td>Closed</td></tr><tr data-d="Sun"><th scope="row">Sunday</th><td>Closed</td></tr>'
    emb=f"https://www.google.com/maps?q={C['lat']},{C['lng']}&output=embed"
    h+=f'''<main id="main"><div class="phero"><div class="wrap">{crumbs([('Home',link('/',d)),('Contact',None)])}<span class="eyebrow">Contact</span><h1>Call or stop by.</h1><p style="margin-top:1rem"><span class="status" style="border-color:var(--line);background:var(--surface)" data-status><i></i><span class="t">{C['hoursShort']}</span></span></p></div></div>
<section><div class="wrap contact-grid"><div class="rv">
<a class="big-phone" href="tel:{TEL}">{PH}</a>
<dl class="dl"><div><dt>Address</dt><dd>{C['street']}<br>{C['city']}, {C['region']} {C['zip']}</dd></div>
<div><dt>Another number</dt><dd><a href="tel:{C['phoneSecondaryTel']}">{C['phoneSecondaryDisplay']}</a></dd></div></dl>
<div class="cta-row" style="margin:0 0 2rem"><a class="btn btn-call" href="tel:{TEL}">{ic('phone')} Call the shop</a><a class="btn btn-ghost" href="https://www.google.com/maps/dir/?api=1&amp;destination={C['lat']},{C['lng']}" rel="noopener">{ic('pin')} Get directions</a></div>
<h2 style="font-size:1.4rem">Hours</h2><table class="hours"><caption class="vh">Opening hours</caption><tbody>{rows}</tbody></table></div>
<div class="mapbox rv" data-map="{emb}"><div class="gridbg"></div><div class="inner">{ic('pin')}<p><b>{C['street']}, {C['city']}</b></p><button class="btn btn-ghost" type="button">Load the map</button><p class="note" style="margin-top:.8rem">Loading the map connects to Google.</p></div></div></div></section></main>'''+footer(d)
    write(url,h)

def page_privacy():
    d=1; url='/privacy'
    t='Privacy | Dave Hoffman Auto Repair'
    h=head('privacy',d,t,'How this website handles your information.',url,None)+header(d,'privacy')
    h=h.replace('<meta name="description"','<meta name="robots" content="noindex,follow"><meta name="description"',1)
    h+=f'''<main id="main"><div class="phero"><div class="wrap">{crumbs([('Home',link('/',d)),('Privacy',None)])}<h1>Privacy</h1></div></div>
<section><div class="wrap prose"><p>This website does not use cookies, analytics, advertising trackers, contact forms, or accounts. We do not collect your name, email, or phone number through the site.</p>
<p>The map on the Contact page loads only when you press “Load the map.” When you load it, Google receives your request under Google's own privacy terms.</p>
<p>If you call the shop at <a href="tel:{TEL}">{PH}</a>, the information you give us stays with the shop and is used to help with your vehicle.</p>
<p class="note">Questions? Call us {C['hoursShort']}.</p></div></section></main>'''+footer(d)
    write(url,h)

def page_404():
    d=0
    h=head('404',d,f'Page not found | {NAME}','That page does not exist.','/404.html',None)
    h=h.replace('<meta name="description"','<meta name="robots" content="noindex"><meta name="description"',1)
    h=h.replace('<head>','<head><base href="/">',1)
    h+=header(d,'')+f'''<main id="main"><div class="wrap err"><div><div class="n" aria-hidden="true">404</div><h1 style="font-size:clamp(1.8rem,3vw,2.6rem)">This page took a wrong turn.</h1><p class="lede" style="margin-inline:auto">Try the services list, or call us at <a href="tel:{TEL}">{PH}</a>.</p><div class="cta-row" style="justify-content:center"><a class="btn btn-call" href="./">Back to home</a><a class="btn btn-ghost" href="services/">Browse services</a></div></div></div></main>'''+footer(d)
    # 404 is served from any depth on GitHub Pages: make asset/links absolute-from-root-safe via <base>
    (ROOT/'404.html').write_text(h,encoding='utf-8')

def misc():
    urls=['/','/services','/about','/reviews','/contact']+[c['url'] for c in CATS]
    sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{BASE}{u}{"" if u=="/" else "/"}</loc></url>\n' for u in urls)+'</urlset>\n'
    (ROOT/'sitemap.xml').write_text(sm)
    bots=['GPTBot','OAI-SearchBot','ChatGPT-User','ClaudeBot','Claude-SearchBot','Claude-User','PerplexityBot','Google-Extended','Applebot-Extended']
    rb='User-agent: *\nAllow: /\n\n'+''.join(f'User-agent: {b}\nAllow: /\n\n' for b in bots)+f'Sitemap: {BASE}/sitemap.xml\n'
    (ROOT/'robots.txt').write_text(rb); (ROOT/'.nojekyll').write_text('')

if __name__=='__main__':
    page_home(); page_services()
    for c in CATS: page_category(c)
    page_about(); page_reviews(); page_contact(); page_privacy(); page_404(); misc()
    print('built', 5+len(CATS)+2)
