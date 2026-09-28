'use strict';
const {rows, catalog, mapping} = window.PMS_DATA;
const $ = id => document.getElementById(id);
const normalize = value => value.normalize('NFKC').toLowerCase().replaceAll('℟','r').replace(/[^\p{L}\p{N}]/gu,'');
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const safeURL = value => { try { const u = new URL(value); return /^https?:$/.test(u.protocol) ? u.href : ''; } catch { return ''; } };
const link = (url, label) => safeURL(url) ? `<a href="${esc(safeURL(url))}" target="_blank" rel="noopener">${esc(label)} ↗</a>` : '';
const songs = new Map(catalog.map(s => [s.name,s]));
$('total').textContent = rows.length;
$('songs').textContent = catalog.filter(s=>s.count).length;
$('coverage-count').textContent = `${catalog.filter(s=>s.count).length} matched / ${catalog.length} checked`;
const levels = [...new Set(rows.map(r=>r.level))].sort((a,b)=>parseFloat(a)-parseFloat(b)||(a.endsWith('+')?1:-1));
for (const level of levels) { const option = document.createElement('option'); option.value=level;option.textContent=`Lv ${level}`;$('level').append(option); }
const searchable = rows.map(row=>({row,text:normalize([row.title,row.artist,mapping[row.md5],...songs.get(mapping[row.md5]).aliases].join(' '))}));
function render(){
 const query=normalize($('search').value);const level=$('level').value;
 const filtered=searchable.filter(x=>(!level||x.row.level===level)&&(!query||x.text.includes(query))).map(x=>x.row);
 const songCount = new Set(filtered.map(r=>mapping[r.md5])).size;
 $('results').textContent=`${filtered.length} chart${filtered.length===1?'':'s'} · ${songCount} song${songCount===1?'':'s'}`;
 $('empty').hidden=filtered.length>0;
 $('rows').innerHTML=filtered.map(r=>{
  const canonical=mapping[r.md5];const song=songs.get(canonical);const five=r.title.includes('[5BUTTONS]');
  const alias=normalize(r.title.replace(' [5BUTTONS]',''))!==normalize(canonical)?`<span class="alias">Pump: ${esc(canonical)}</span>`:'';
  const videos=[r.video1,r.video2].filter(Boolean).map((v,i)=>link(/^https?:/.test(v)?v:`https://www.youtube.com/watch?v=${encodeURIComponent(v)}`,i?'Video 2':'Video')).join('');
  return `<tr><td><span class="badge ${r.level==='45+'?'boundary':''}">${esc(r.level)}</span></td><td><div class="song-name">${esc(r.title)}${five?'<span class="tag">5 buttons</span>':''}</div>${alias}<span class="artist">${esc(r.artist)}</span>${song.note?`<span class="comment">${esc(song.note)}</span>`:''}</td><td><div class="chart-name">${esc(r.name_diff||'—')}</div><span class="chart-meta">${esc(r.notes||'—')} notes · TOTAL ${esc(r.total||'—')}</span>${r.comment?`<span class="comment">${esc(r.comment)}</span>`:''}</td><td><div class="links">${link(r.url,'Song / package')}${link(r.url_diff,'Chart')}${videos}${link(`https://www.dream-pro.info/~lavalse/LR2IR/search.cgi?mode=ranking&bmsmd5=${encodeURIComponent(r.md5)}`,'IR')}</div>${!r.url_diff?'<span class="bundled">See package / chart notes for the PMS file.</span>':''}</td></tr>`;
 }).join('');
}
$('search').addEventListener('input',render);$('level').addEventListener('change',render);
$('coverage').innerHTML=[...catalog].sort((a,b)=>a.name.localeCompare(b.name)).map(s=>`<tr><td><strong>${esc(s.name)}</strong>${s.aliases.length?`<span class="alias">${esc(s.aliases.join(' / '))}</span>`:''}</td><td>${s.count?esc(s.levels.join(' / ')):'<span class="missing">No normal chart</span>'}</td><td>${esc(s.basis)}${s.source?'<br>'+link(s.source,'Reference'):''}</td></tr>`).join('');
render();
