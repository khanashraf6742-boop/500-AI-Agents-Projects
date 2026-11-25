(function(){
'use strict';
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>Array.from(r.querySelectorAll(s));
const LS={get(k,d){try{const v=localStorage.getItem('cghs_'+k);return v===null?d:JSON.parse(v)}catch(e){return d}},set(k,v){try{localStorage.setItem('cghs_'+k,JSON.stringify(v))}catch(e){}}};
let studied=new Set(LS.get('studied',[])), bm=new Set(LS.get('bm',[])), known=LS.get('known',{});
const cards=$$('details.card');
/* theme */
function setTheme(t){document.documentElement.dataset.theme=t;LS.set('theme',t);$('#bTheme').textContent=t==='dark'?'☀️':'🌙'}
setTheme(LS.get('theme',matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light'));
$('#bTheme').onclick=()=>setTheme(document.documentElement.dataset.theme==='dark'?'light':'dark');
/* hinglish mode: 0 collapsed, 1 expanded, 2 hidden */
let hmode=LS.get('hmode',0);
function applyH(){document.body.classList.toggle('hing-off',hmode===2);$$('details.hing').forEach(d=>d.open=hmode===1);$('#bHing').textContent=['🗣️ Hinglish: collapsed','🗣️ Hinglish: expanded','🗣️ Hinglish: hidden'][hmode]}
$('#bHing').onclick=()=>{hmode=(hmode+1)%3;LS.set('hmode',hmode);applyH()};applyH();
/* font size */
let fs=LS.get('fs',16.5);function applyFs(){document.body.style.fontSize=fs+'px';LS.set('fs',fs)}applyFs();
$('#bFp').onclick=()=>{fs=Math.min(22,fs+1);applyFs()};$('#bFm').onclick=()=>{fs=Math.max(13,fs-1);applyFs()};
/* views / routing */
const views=$$('.view');
function showView(id){views.forEach(v=>v.classList.toggle('active',v.id==='v-'+id));$$('#side a[data-view]').forEach(a=>a.classList.toggle('cur',a.dataset.view===id&&!a.dataset.card));window.scrollTo(0,0);document.body.classList.remove('nav')}
function curNav(id){$$('#side a[data-card]').forEach(a=>a.classList.toggle('cur',a.dataset.card===id))}
function go(){
  const h=location.hash.slice(1)||'about';
  const el=document.getElementById(h);
  if(el&&el.matches('details.card')){const v=el.closest('.view');showView(v.id.slice(2));el.open=true;setTimeout(()=>{el.scrollIntoView({block:'start'});curNav(h)},30);}
  else if(document.getElementById('v-'+h))showView(h);
  else showView('about');
}
window.addEventListener('hashchange',go);go();
$('#menu').onclick=()=>document.body.classList.toggle('nav');$('#scrim').onclick=()=>document.body.classList.remove('nav');
/* scrollspy */
if('IntersectionObserver' in window){const io=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting)curNav(e.target.id)})},{rootMargin:'-60px 0px -75% 0px'});cards.forEach(c=>io.observe(c));}
/* collapse / expand */
$$('[data-act=expand]').forEach(b=>b.onclick=()=>$$('details.card',b.closest('.view')).forEach(d=>d.open=true));
$$('[data-act=collapse]').forEach(b=>b.onclick=()=>$$('details.card',b.closest('.view')).forEach(d=>d.open=false));
/* studied + bookmark */
function refresh(){
  cards.forEach(c=>{const s=studied.has(c.id),b=bm.has(c.id);const bs=$('.bStudy',c),bb=$('.bBm',c);bs.classList.toggle('on',s);bs.textContent=s?'✓ Studied':'Mark studied';bb.classList.toggle('on',b);bb.textContent=b?'★':'☆'});
  $$('#side a[data-card]').forEach(a=>{a.classList.toggle('done',studied.has(a.dataset.card));a.classList.toggle('bm',bm.has(a.dataset.card))});
  const n=studied.size;$('#prog i').style.width=(100*n/cards.length)+'%';$('#progt').textContent=n+'/'+cards.length;
  LS.set('studied',[...studied]);LS.set('bm',[...bm]);
}
cards.forEach(c=>{
  $('.bStudy',c).onclick=e=>{e.preventDefault();e.stopPropagation();studied.has(c.id)?studied.delete(c.id):studied.add(c.id);refresh()};
  $('.bBm',c).onclick=e=>{e.preventDefault();e.stopPropagation();bm.has(c.id)?bm.delete(c.id):bm.add(c.id);refresh()};
});
$('#bOnlyBm').onclick=function(){this.classList.toggle('on');const on=this.classList.contains('on');$$('#side a[data-card]').forEach(a=>a.classList.toggle('hide',on&&!bm.has(a.dataset.card)))};
refresh();
/* search (rule no., OM no., keyword, amount) */
const idx=cards.map(c=>({id:c.id,title:$('.rinfo h2',c).textContent,text:(function(){const w=document.createTreeWalker(c,NodeFilter.SHOW_TEXT);let t,o=[];while(t=w.nextNode()){if(!t.parentNode.closest('script,style,svg'))o.push(t.nodeValue)}return o.join(' ').replace(/\s+/g,' ')})()}));
const q=$('#q'),res=$('#results');let tm;
function clearMarks(){$$('mark').forEach(m=>{const p=m.parentNode;p.replaceChild(document.createTextNode(m.textContent),m);p.normalize()})}
function markIn(root,term){let n=0;const w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);const hits=[];let t;while(t=w.nextNode()){if(t.parentNode.closest('script,style,svg'))continue;if(t.nodeValue.toLowerCase().includes(term))hits.push(t)}
  hits.slice(0,200).forEach(t=>{const v=t.nodeValue,l=v.toLowerCase();let i=0,p;const frag=document.createDocumentFragment();while((p=l.indexOf(term,i))>=0){frag.append(v.slice(i,p));const m=document.createElement('mark');m.textContent=v.slice(p,p+term.length);frag.append(m);i=p+term.length;n++}frag.append(v.slice(i));t.parentNode.replaceChild(frag,t)});return n}
const esc=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;');
q.addEventListener('input',()=>{clearTimeout(tm);tm=setTimeout(()=>{const term=q.value.trim().toLowerCase();res.innerHTML='';if(term.length<2){res.style.display='none';return}
  const out=[];idx.forEach(r=>{const l=r.text.toLowerCase();const i=l.indexOf(term);if(i>=0){out.push({r,i,cnt:l.split(term).length-1})}});
  out.sort((a,b)=>b.cnt-a.cnt);
  res.innerHTML=out.slice(0,40).map(o=>{const s=esc(o.r.text.slice(Math.max(0,o.i-50),o.i+90));return `<a href="#${o.r.id}" data-term="${esc(term)}"><b>${esc(o.r.title)}</b> <small>${o.cnt} match${o.cnt>1?'es':''} · …${s}…</small></a>`}).join('')||'<a>No match</a>';res.style.display='block'},160)});
res.addEventListener('click',e=>{const a=e.target.closest('a[data-term]');if(!a)return;const term=a.dataset.term;res.style.display='none';setTimeout(()=>{clearMarks();const c=document.getElementById(a.getAttribute('href').slice(1));if(c){c.open=true;$$('details.hing',c).forEach(d=>d.open=true);markIn(c,term);const m=$('mark',c);if(m)m.scrollIntoView({block:'center'})}},150)});
document.addEventListener('click',e=>{if(!e.target.closest('#results,#q'))res.style.display='none'});
document.addEventListener('keydown',e=>{const tag=(e.target.tagName||'').toLowerCase();if(tag==='input')return;
  if(e.key==='/'){e.preventDefault();q.focus()}
  else if(e.key==='Escape'){clearMarks()}
  else if(e.key==='j'||e.key==='k'){const vis=$$('.view.active details.card');const y=window.scrollY+90;let i=vis.findIndex(c=>c.getBoundingClientRect().top+window.scrollY>y);if(e.key==='k'){i=(i<0?vis.length:i)-2}if(vis[i]){vis[i].scrollIntoView({block:'start'})}}});
/* generic filters */
$$('[data-filter]').forEach(inp=>inp.addEventListener('input',()=>{const t=inp.value.toLowerCase();$$(inp.dataset.filter).forEach(r=>r.classList.toggle('hide',!!t&&!r.textContent.toLowerCase().includes(t)))}));
/* sortable tables */
$$('table.sortable th').forEach((th,ci)=>th.addEventListener('click',()=>{const tb=th.closest('table').tBodies[0];const rows=Array.from(tb.rows);const asc=th.dataset.asc!=='1';th.dataset.asc=asc?'1':'0';rows.sort((a,b)=>{const x=(a.cells[ci].dataset.k||a.cells[ci].textContent),y=(b.cells[ci].dataset.k||b.cells[ci].textContent);return asc?x.localeCompare(y,undefined,{numeric:true}):y.localeCompare(x,undefined,{numeric:true})});rows.forEach(r=>tb.appendChild(r))}));
/* flashcards */
const FC=JSON.parse($('#fcdata').textContent);let deck=[],pos=0,flipped=false;
function build(){const kind=$('#fkind').value,only=$('#fonly').value;deck=FC.map((f,i)=>Object.assign({},f,{i})).filter(f=>(kind==='all'||f.t===kind)&&(only==='all'||(only==='unknown'?known[f.i]!==1:known[f.i]===1)));if($('#fshuf').checked)deck.sort(()=>Math.random()-.5);pos=0;show()}
function show(){const c=$('#fcard');const kc=Object.values(known).filter(v=>v===1).length;if(!deck.length){c.innerHTML='<small>No cards in this selection</small>';$('#fcount').textContent='0 cards';return}const f=deck[pos];flipped=false;c.innerHTML=`<small>${f.t==='trap'?'EXAM TRAP — right or wrong?':'RECALL'} · ${f.s}</small><div>${f.q}</div><small style="margin-top:14px">tap to reveal</small>`;$('#fcount').textContent=`${pos+1}/${deck.length} · known ${kc}/${FC.length}`}
$('#fcard').onclick=()=>{if(!deck.length)return;const f=deck[pos];flipped=!flipped;$('#fcard').innerHTML=flipped?`<small>ANSWER · <a href="#${f.c}">open section</a></small><div>${f.a}</div>`:`<small>${f.s}</small><div>${f.q}</div>`};
function mark(v){if(!deck.length)return;known[deck[pos].i]=v;LS.set('known',known);pos=(pos+1)%deck.length;show()}
$('#fKnow').onclick=()=>mark(1);$('#fNo').onclick=()=>mark(0);
$('#fNext').onclick=()=>{pos=(pos+1)%Math.max(1,deck.length);show()};$('#fPrev').onclick=()=>{pos=(pos-1+deck.length)%Math.max(1,deck.length);show()};
$('#fReset').onclick=()=>{if(confirm('Reset known/unknown status of all flashcards?')){known={};LS.set('known',known);build()}};
['#fkind','#fonly','#fshuf'].forEach(s=>$(s).onchange=build);build();
/* print */
window.addEventListener('beforeprint',()=>{$$('details.card,details.visual').forEach(d=>d.open=true)});
$('#bPrint').onclick=()=>window.print();
})();
