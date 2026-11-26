(function(){
'use strict';
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>Array.from(r.querySelectorAll(s));
const LS={get(k,d){try{const v=localStorage.getItem('cghs_'+k);return v===null?d:JSON.parse(v)}catch(e){return d}},set(k,v){try{localStorage.setItem('cghs_'+k,JSON.stringify(v))}catch(e){}}};
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const cards=$$('details.card');
const title=id=>{const c=document.getElementById(id);return c?$('.rinfo h2',c).textContent:''};
const shuffle=a=>{a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a};

/* ---------- revision mode ---------- */
let rev=LS.get('rev',false);
function applyRev(){document.body.classList.toggle('rev',rev);const b=$('#bRev');if(b){b.classList.toggle('on',rev);b.textContent=rev?'⚡ Revision: on':'⚡ Revision'}}
if($('#bRev')){$('#bRev').onclick=()=>{rev=!rev;LS.set('rev',rev);applyRev()};applyRev();}

/* ---------- notes ---------- */
let notes=LS.get('notes',{});
$$('textarea[data-note]').forEach(t=>{t.value=notes[t.dataset.note]||'';t.addEventListener('input',()=>{const v=t.value.trim();if(v)notes[t.dataset.note]=t.value;else delete notes[t.dataset.note];LS.set('notes',notes);renderNotes()})});
function renderNotes(){const el=$('#notesList');if(!el)return;const ids=Object.keys(notes);el.innerHTML=ids.length?ids.map(id=>`<div class="listitem"><b><a href="#${id}">${esc(title(id))}</a></b><br>${esc(notes[id]).replace(/\n/g,'<br>')}</div>`).join(''):'<p class="lead">No notes yet — write them at the bottom of any section.</p>'}
renderNotes();

/* ---------- export / import / reset ---------- */
const KEYS=['studied','bm','known','notes','qhist','qstat','plan','fs','hmode','rev','theme'];
const bExp=$('#bExport');if(bExp)bExp.onclick=()=>{const o={};KEYS.forEach(k=>{o[k]=LS.get(k,null)});o._saved=new Date().toISOString();const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(o,null,1)],{type:'application/json'}));a.download='cghs-study-progress.json';a.click()};
const fImp=$('#fImport');if(fImp)fImp.onchange=()=>{const f=fImp.files[0];if(!f)return;f.text().then(t=>{try{const o=JSON.parse(t);KEYS.forEach(k=>{if(o[k]!==null&&o[k]!==undefined)LS.set(k,o[k])});alert('Progress imported. The page will reload.');location.reload()}catch(e){alert('Not a valid progress file.')}})};
const bRes=$('#bReset');if(bRes)bRes.onclick=()=>{if(confirm('Delete ALL saved progress, notes, quiz history and flashcard status from this browser?')){KEYS.forEach(k=>localStorage.removeItem('cghs_'+k));location.reload()}};

/* ---------- study plan ---------- */
const idx=cards.map(c=>({id:c.id,t:$('.rinfo h2',c).textContent,len:c.textContent.length,part:c.closest('.view').id.slice(2)}));
function buildPlan(days,start){
  const tot=idx.reduce((s,x)=>s+x.len,0), per=tot/(days-1||1), plan=[];let cur=[],acc=0;
  idx.forEach(x=>{cur.push(x);acc+=x.len;if(acc>=per&&plan.length<days-2){plan.push(cur);cur=[];acc=0}});
  if(cur.length)plan.push(cur);
  while(plan.length<days-1)plan.push([]);
  return {days,start,plan:plan.map(d=>d.map(x=>x.id))};
}
function renderPlan(){
  const el=$('#planOut');if(!el)return;const P=LS.get('plan',null);
  if(!P){el.innerHTML='<p class="lead">Pick a length and press “Create plan”.</p>';return}
  const studied=new Set(LS.get('studied',[]));const today=Math.floor((Date.now()-new Date(P.start).getTime())/864e5)+1;
  let h=`<p class="lead">Started ${new Date(P.start).toDateString()} · day ${Math.min(Math.max(today,1),P.days)} of ${P.days}</p>`;
  P.plan.forEach((d,i)=>{const done=d.filter(id=>studied.has(id)).length;h+=`<details class="listitem" ${i+1===today?'open':''}><summary><b>Day ${i+1}</b> — ${d.length} sections · ${done}/${d.length} studied ${i+1===today?'<span class="tag">today</span>':''}</summary><ul>${d.map(id=>`<li>${studied.has(id)?'✓ ':''}<a href="#${id}">${esc(title(id))}</a></li>`).join('')}</ul></details>`});
  h+=`<details class="listitem" ${today>=P.days?'open':''}><summary><b>Day ${P.days}</b> — revision day</summary><ul><li>Turn on ⚡ Revision mode and re-read the <a href="#memory">Memory sheet</a></li><li>Take a 30-question <a href="#quiz">mock test</a></li><li>Go through flashcards that are due</li><li>Read the <a href="#verify">Verify tab</a></li></ul></details>`;
  el.innerHTML=h;
}
const bPlan=$('#bPlan');if(bPlan)bPlan.onclick=()=>{const d=parseInt($('#planDays').value,10);LS.set('plan',buildPlan(d,Date.now()));renderPlan()};
renderPlan();window.addEventListener('hashchange',()=>{if(location.hash==='#plan')renderPlan()});

/* ---------- compare any two sections ---------- */
const sa=$('#cmpA'),sb=$('#cmpB');
if(sa&&sb){const opts=cards.map(c=>`<option value="${c.id}">${esc($('.rtag',c).textContent+' — '+$('.rinfo h2',c).textContent.slice(0,70))}</option>`).join('');sa.innerHTML=opts;sb.innerHTML=opts;sb.selectedIndex=Math.min(1,cards.length-1);
  const show=()=>{[['cmpOutA',sa],['cmpOutB',sb]].forEach(([o,s])=>{const c=document.getElementById(s.value);const out=$('#'+o);out.innerHTML='';if(!c)return;const cl=$('.cbody',c).cloneNode(true);$$('textarea,.notes,details.hing,.hinglish',cl).forEach(n=>n.remove());$$('details',cl).forEach(d=>d.open=true);$$('[id]',cl).forEach(n=>n.removeAttribute('id'));out.innerHTML=`<h3><a href="#${c.id}">${esc($('.rinfo h2',c).textContent)}</a></h3>`;out.appendChild(cl)})};
  sa.onchange=show;sb.onchange=show;show();}

/* ---------- quiz ---------- */
const BANK=JSON.parse(($('#qdata')||{textContent:'[]'}).textContent);
let Q=null;
function startQuiz(wrongOnly){
  let pool;
  if(wrongOnly&&Q){pool=Q.items.filter(i=>i.ans!==i.right).map(i=>i.src)}
  else{const kind=$('#qKind').value,part=$('#qPart').value;pool=BANK.filter(q=>(kind==='all'||q.k===kind)&&(part==='all'||q.p===part));pool=shuffle(pool).slice(0,parseInt($('#qCount').value,10))}
  if(!pool.length){alert('No questions match that selection.');return}
  const items=pool.map(q=>{let opts,right;if(q.k==='tf'){opts=['True','False'];right=q.a===0?0:1}else{const t=shuffle(q.o);opts=t;right=t.indexOf(q.o[0])}return {src:q,q:q.q,opts,right,ans:null,why:q.why,c:q.c,s:q.s}});
  const mins=parseInt($('#qTime').value,10);
  Q={items,pos:0,mode:$('#qMode').value,end:mins?Date.now()+mins*60000:0,done:false};
  $('#qSetup').classList.add('hide');$('#qRun').classList.remove('hide');$('#qResult').classList.add('hide');
  tick();drawQ();
}
let tmr=null;
function tick(){clearInterval(tmr);if(!Q||!Q.end){$('#qTimer').textContent='';return}tmr=setInterval(()=>{const left=Q.end-Date.now();if(left<=0){clearInterval(tmr);finishQuiz();return}const m=Math.floor(left/60000),s=Math.floor(left/1000)%60;$('#qTimer').textContent='⏱ '+m+':'+String(s).padStart(2,'0')},500)}
function drawQ(){
  const it=Q.items[Q.pos];$('#qProg').textContent=`Question ${Q.pos+1} of ${Q.items.length}`;
  $('#qText').textContent=it.q;
  const box=$('#qOpts');box.innerHTML='';
  it.opts.forEach((o,i)=>{const b=document.createElement('button');b.className='qopt';b.textContent=o;
    if(it.ans===i)b.classList.add('sel');
    if(Q.mode==='practice'&&it.ans!==null){b.disabled=true;if(i===it.right)b.classList.add('ok');else if(i===it.ans)b.classList.add('bad')}
    b.onclick=()=>{if(Q.mode==='practice'&&it.ans!==null)return;it.ans=i;drawQ()};box.appendChild(b)});
  const fb=$('#qFeedback');fb.innerHTML='';
  if(Q.mode==='practice'&&it.ans!==null){fb.innerHTML=`<div class="listitem ${it.ans===it.right?'okbox':'badbox'}"><b>${it.ans===it.right?'Correct':'Not quite'}</b> — ${esc(it.why)}${it.c?` <a href="#${it.c}">open section</a>`:''}</div>`}
  $('#qPrev').disabled=Q.pos===0;$('#qNext').textContent=Q.pos===Q.items.length-1?'Finish ✔':'Next ▶';
}
function finishQuiz(){
  if(!Q||Q.done)return;Q.done=true;clearInterval(tmr);
  const n=Q.items.length;let right=0;const by={};
  Q.items.forEach(i=>{const ok=i.ans===i.right;if(ok)right++;const k=i.s||'Other';(by[k]=by[k]||[0,0])[1]++;if(ok)by[k][0]++});
  const stat=LS.get('qstat',{});Object.keys(by).forEach(k=>{const s=stat[k]||[0,0];s[0]+=by[k][0];s[1]+=by[k][1];stat[k]=s});LS.set('qstat',stat);
  const hist=LS.get('qhist',[]);hist.unshift({d:Date.now(),r:right,n,m:Q.mode});LS.set('qhist',hist.slice(0,30));
  $('#qRun').classList.add('hide');$('#qResult').classList.remove('hide');
  const pct=Math.round(100*right/n);
  let h=`<h3>Score: ${right} / ${n} (${pct}%)</h3><div class="bar"><i style="width:${pct}%"></i></div>`;
  h+='<h4>By section</h4>'+Object.entries(by).sort((a,b)=>a[1][0]/a[1][1]-b[1][0]/b[1][1]).map(([k,v])=>`<div class="rowline"><span>${esc(k)}</span><b>${v[0]}/${v[1]}</b></div>`).join('');
  const wrong=Q.items.filter(i=>i.ans!==i.right);
  h+=`<h4>${wrong.length?'Review — '+wrong.length+' to revisit':'All correct!'}</h4>`+wrong.map(i=>`<div class="listitem badbox"><b>${esc(i.q)}</b><br>Your answer: ${i.ans===null?'<i>not answered</i>':esc(i.opts[i.ans])}<br>Correct: <b>${esc(i.opts[i.right])}</b><br>${esc(i.why)} ${i.c?`<a href="#${i.c}">open section</a>`:''}</div>`).join('');
  $('#qResultBody').innerHTML=h;$('#qRetryWrong').classList.toggle('hide',!wrong.length);renderHistory();
}
function renderHistory(){
  const el=$('#qHist');if(!el)return;const hist=LS.get('qhist',[]),stat=LS.get('qstat',{});
  const weak=Object.entries(stat).filter(([k,v])=>v[1]>=3).sort((a,b)=>a[1][0]/a[1][1]-b[1][0]/b[1][1]).slice(0,6);
  el.innerHTML=(hist.length?'<h4>Recent attempts</h4>'+hist.slice(0,6).map(h=>`<div class="rowline"><span>${new Date(h.d).toLocaleString()} · ${h.m}</span><b>${h.r}/${h.n}</b></div>`).join(''):'')+(weak.length?'<h4>Weakest sections so far</h4>'+weak.map(([k,v])=>`<div class="rowline"><span>${esc(k)}</span><b>${Math.round(100*v[0]/v[1])}%</b></div>`).join(''):'');
}
if($('#qStart')){
  $('#qBank').textContent=BANK.length;
  $('#qStart').onclick=()=>startQuiz(false);
  $('#qPrev').onclick=()=>{if(Q.pos>0){Q.pos--;drawQ()}};
  $('#qNext').onclick=()=>{if(Q.pos<Q.items.length-1){Q.pos++;drawQ()}else{finishQuiz()}};
  $('#qFinish').onclick=()=>{if(confirm('Finish the test now?'))finishQuiz()};
  $('#qRetryWrong').onclick=()=>startQuiz(true);
  $('#qAgain').onclick=()=>{clearInterval(tmr);$('#qResult').classList.add('hide');$('#qSetup').classList.remove('hide')};
  renderHistory();
}
})();
