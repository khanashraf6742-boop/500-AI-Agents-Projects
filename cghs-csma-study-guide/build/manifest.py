import re,json,sys
from bs4 import BeautifulSoup
SRC=sys.argv[1]; OUT=sys.argv[2]
s=BeautifulSoup(open(SRC,encoding='utf8').read(),'lxml')
for sc in s.find_all('script'): sc.decompose()
txt=lambda e: re.sub(r'\s+',' ',e.get_text(' ',strip=True))
body=txt(s.body)
RS=r'(?:Rs\.?|₹)\s?[\d,]+(?:\.\d+)?(?:\s?(?:lakh|crore|per day|/day|/month))?'
m={
 'cards':len(s.select('.rule-card')),
 'official_boxes':len(s.select('.official-box')),
 'hinglish_blocks':len(s.select('.hinglish')),
 'paired_units':len(s.select('.paired-unit')),
 'gd_boxes':len(s.select('.gd-box')),
 'amend_boxes':len(s.select('.amend-box')),
 'trap_boxes':len(s.select('.trap-box')),
 'trap_items':sum(len(t.select('li')) for t in s.select('.trap-box')),
 'key_boxes':len(s.select('.key-box')),
 'tables':len(s.select('table')),
 'qa_cards':len(s.select('.qa-card')),
 'worked_examples':len(s.select('.auto-worked-example')),
 'oms':sorted(set(re.findall(r'OM\s+No\.?\s*[\w\.\-/\(\)]+',body))),
 'dates':sorted(set(re.findall(r'\b\d{2}\.\d{2}\.\d{4}\b',body))),
 'amounts':sorted(set(re.findall(RS,body))),
 'rule_refs':sorted(set(re.findall(r'Rule\s+\d+(?:\(\w+\))*(?:\(\w+\))*',body))),
 'gd_items':sorted(set(re.findall(r'GD\(\d+\)',body))),
}
# every text leaf-block (li/p/td/th) as normalized string for exact presence check
leaves=[]
for e in s.select('li,p,td,th,h1,h2,h3,.otag,.htag,.ttag,.gdtag,.ktag,.atag,.rule-tag,.rule-om,.qlabel,.alabel'):
    if e.find(['li','p','td','th']) and e.name not in('li',): 
        pass
    t=txt(e)
    if len(t)>2: leaves.append(t)
m['leaf_count']=len(set(leaves))
m['leaves']=sorted(set(leaves))
m['words']=len(body.split())
json.dump(m,open(OUT,'w'),ensure_ascii=False)
print({k:(len(v) if isinstance(v,list) else v) for k,v in m.items() if k!='leaves'})
