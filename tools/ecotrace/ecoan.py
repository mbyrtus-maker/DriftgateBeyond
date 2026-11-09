import json,collections,statistics as st,sys,re
d=json.load(open(sys.argv[1]))
def kindOf(id):
  m=re.match(r'(mp|mq|sy)_([a-z]+)_([a-z]+)',id or '')
  if not m:return '?'
  return 'sys_'+m.group(3) if m.group(1)=='sy' else m.group(3)
tot=collections.Counter();over=[];notover=[];allch=[];pxone=0;pxn=0;ceo=0;fails=[];durs=[];react=[];lifes=[]
for gi,g in enumerate(d):
  rows=g['rows'];H=len(rows);ev=[e for r in rows for e in r['ev']]
  S=[r['sales'] for r in rows]
  def share(h,m,k,S=S):
    if not(0<=h<len(S)):return None
    t=sum(v[0] for kk,v in S[h].items() if kk.split('|')[1]==k);return S[h].get(m+'|'+k,[0])[0]/t if t else None
  def leader(h,k,S=S):
    if not(0<=h<len(S)):return None
    b=max(((kk.split('|')[0],v[0]) for kk,v in S[h].items() if kk.split('|')[1]==k),key=lambda x:x[1],default=None);return b[0] if b else None
  def px(h,m,rows=rows):
    if 0<=h<len(rows) and m in rows[h]['m'] and not rows[h]['m'][m]['dead']:return rows[h]['m'][m]['px']
  # hourly px changes for all makers (the market's baseline)
  base=collections.defaultdict(list)
  for h in range(1,H):
    for m in rows[h]['m']:
      a,b=px(h-1,m),px(h,m)
      if a and b and a>1:base[h].append((b-a)/a);allch.append((b-a)/a)
      if b:pxn+=1;pxone+=(b<=1)
    for m in rows[h]['m']:
      if rows[h]['m'][m]['ceo']!=rows[h-1]['m'][m]['ceo'] and not rows[h]['m'][m]['dead'] and rows[h]['m'][m]['gen']==rows[h-1]['m'][m]['gen']:ceo+=1
  # rows[i] is the snapshot at the end of hour i+1: an event at minute T sits in row T//60
  firstLose={}
  for e in ev:
    if e['k']=='tweak':firstLose.setdefault((e['m'],e['id']),e['T'])
    if e['k']=='rdstart':
      t0=firstLose.get((e['m'],e['id']))
      if t0 is not None:react.append(e['T']-t0)
    if e['k']=='fail':fails.append((gi,e))
    if e['k']=='launch':
      durs.append(e['T']-e.get('t0',e['T']));k=kindOf(e.get('id'));h=e['T']//60
      lb,la=leader(h-1,k),leader(h+1,k)
      sb=[share(x,e['m'],k) for x in (h-1,)];sa=[share(x,e['m'],k) for x in (h+1,h+2)]
      a,b=px(h-1,e['m']),px(min(h+2,H-1),e['m'])
      ch=(b-a)/a if a and b and a>1 else None
      mk=[st.mean(base[x]) for x in (h,h+1,h+2) if base.get(x)]
      rec=dict(g=gi,m=e['m'],id=e.get('id'),k=k,T=e['T'],ch=ch,mkt=sum(mk) if mk else None,sb=sb[0],sa=[x for x in sa if x is not None])
      if lb and la==e['m'] and lb!=e['m']:over.append(rec)
      else:notover.append(rec)
  # a maker's life: revenue, launches, tweaks, how it ended
  for m in rows[-1]['m']:
    rev=sum(v[1] for r in S for kk,v in r.items() if kk.startswith(m+'|'))
    tot[m]+=rev
    lifes.append(dict(g=gi,m=m,rev=rev,launch=sum(1 for e in ev if e['k']=='launch' and e['m']==m),tweak=sum(1 for e in ev if e['k']=='tweak' and e['m']==m),fail=sum(1 for e in ev if e['k']=='fail' and e['m']==m),px0=px(0,m),px1=px(H-1,m),cash1=rows[-1]['m'][m]['cash']))
def f(x):return 'n/a' if x is None else f"{100*x:+.0f}%"
print(f"{len(d)} galaxies x {len(d[0]['rows'])} h; makers' lives {len(lifes)}")
print(f"failures: {len(fails)}  ({len(fails)/len(d):.2f} a galaxy)")
for gi,e in fails:print(f"  g{gi} {e['m']} at {e['T']//60}h{e['T']%60:02d}: cash {e['cash']}, running costs {e['up']} cr/h, last share prices {e['pxH']}, R&D {e['rd']}")
print(f"R&D launches: {len(durs)} ({len(durs)/len(d):.1f} a galaxy); project length median {st.median(durs)} min, 90th pct {sorted(durs)[int(.9*len(durs))]} min")
print(f"reaction: first tweak of a line -> R&D on it: median {st.median(react) if react else 'n/a'} min (n={len(react)})")
print(f"share price: hourly change median {f(st.median(allch))}, |change| median {100*st.median([abs(x) for x in allch]):.0f}%; at the floor (1.0) {100*pxone/max(1,pxn):.0f}% of maker-hours; CEO replacements {ceo} ({ceo/len(d):.1f} a galaxy)")
def summ(L,name):
  ch=[r['ch'] for r in L if r['ch'] is not None];rel=[r['ch']-(r['mkt'] or 0) for r in L if r['ch'] is not None]
  print(f"{name}: {len(L)}; share price 2 h after vs 1 h before: median {f(st.median(ch)) if ch else 'n/a'}, vs the market {f(st.median(rel)) if rel else 'n/a'}; rose in {sum(1 for x in ch if x>0)}/{len(ch)}")
summ(over,'launches that made the maker the top seller of its kind (overtook the leader)')
summ(notover,'other launches')
# do the makers that launch more earn more and end richer?
L=sorted(lifes,key=lambda x:x['launch'])
q=len(L)//3
for name,part in (('fewest launches',L[:q]),('middle',L[q:2*q]),('most launches',L[2*q:])):
  print(f"  {name:16} launches {st.mean(x['launch'] for x in part):4.1f}  revenue {st.mean(x['rev'] for x in part):7.0f}  end cash {st.mean(x['cash1'] for x in part):6.0f}  end px {st.mean((x['px1'] or 0) for x in part):5.1f}  failures {sum(x['fail'] for x in part)}")
R=sorted(lifes,key=lambda x:x['rev'])
for name,part in (('lowest sellers',R[:q]),('top sellers',R[2*q:])):
  print(f"  {name:16} revenue {st.mean(x['rev'] for x in part):7.0f}  end cash {st.mean(x['cash1'] for x in part):6.0f}  end px {st.mean((x['px1'] or 0) for x in part):5.1f}  failures {sum(x['fail'] for x in part)}")
