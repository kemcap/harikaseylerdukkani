const fs=require('fs'),vm=require('vm'),assert=require('assert'),path=require('path');
const root=__dirname,voidTags=new Set(['img','input','br','hr','meta','link','source','wbr']);
const decode=s=>String(s).replace(/&amp;/g,'&').replace(/&quot;/g,'"').replace(/&#39;/g,"'").replace(/&lt;/g,'<').replace(/&gt;/g,'>');
class El{
 constructor(tag='div',attrs={}){this.tagName=tag.toUpperCase();this.attrs={...attrs};this.children=[];this.parentNode=null;this.listeners={};this.style={setProperty(k,v){this[k]=v}};this.value=attrs.value||'';this.hidden='hidden' in attrs;this._text='';this._html='';this.classList={add:x=>this.setClass(x,true),remove:x=>this.setClass(x,false),contains:x=>(this.attrs.class||'').split(/\s+/).includes(x),toggle:(x,on)=>{const yes=on===undefined?!this.classList.contains(x):!!on;this.setClass(x,yes);return yes}};this.dataset=new Proxy({},{get:(_,k)=>this.attrs['data-'+String(k).replace(/[A-Z]/g,c=>'-'+c.toLowerCase())],set:(_,k,v)=>{this.attrs['data-'+k]=v;return true}})}
 setClass(x,on){const s=new Set((this.attrs.class||'').split(/\s+/).filter(Boolean));on?s.add(x):s.delete(x);this.attrs.class=[...s].join(' ')}
 set className(v){this.attrs.class=v}get className(){return this.attrs.class||''}get id(){return this.attrs.id}set id(v){this.attrs.id=v}
 set textContent(v){this._text=String(v);this.children=[]}get textContent(){return this._text+this.children.map(x=>x.textContent).join('')}
 get innerText(){return this.textContent}
 set innerHTML(html){this._html=html;this.children=[];this._text='';parse(html,this)}get innerHTML(){return this._html}
 setAttribute(k,v){this.attrs[k]=String(v)}getAttribute(k){return this.attrs[k]??null}
 addEventListener(n,f){(this.listeners[n]??=[]).push(f)}
 appendChild(e){e.parentNode=this;this.children.push(e);return e}before(e){e.parentNode=this.parentNode;this.parentNode.children.splice(this.parentNode.children.indexOf(this),0,e)}
 matches(selector){let s=selector.trim();const attrs=[...s.matchAll(/\[([^\]=]+)(?:="([^"]*)")?\]/g)];for(const a of attrs){if(!(a[1] in this.attrs)||(a[2]!==undefined&&this.attrs[a[1]]!==a[2]))return false}s=s.replace(/\[[^\]]+\]/g,'');if(!s)return true;if(s.startsWith('#'))return this.id===s.slice(1);const cls=[...s.matchAll(/\.([\w-]+)/g)].map(m=>m[1]);if(cls.some(c=>!this.classList.contains(c)))return false;const tag=s.split(/[.#]/)[0];return !tag||this.tagName===tag.toUpperCase()}
 querySelectorAll(s){const selectors=s.split(',');let out=[];for(const c of this.children){if(selectors.some(x=>c.matches(x)))out.push(c);out.push(...c.querySelectorAll(s))}return out}querySelector(s){return this.querySelectorAll(s)[0]||null}
 closest(s){let n=this;while(n){if(s.split(',').some(x=>n.matches(x)))return n;n=n.parentNode}return null}
 focus(){}scrollIntoView(){}getBoundingClientRect(){return {bottom:800}}reset(){this.querySelectorAll('input,textarea').forEach(e=>e.value='')}
}
function parse(html,parent){const stack=[parent];for(const m of html.matchAll(/<\/?[a-zA-Z][^>]*>|[^<]+/g)){const token=m[0];if(token.startsWith('</')){if(stack.length>1)stack.pop();continue}if(token.startsWith('<')){const tag=token.match(/^<([\w-]+)/)[1],attrs={};for(const a of token.matchAll(/([\w:-]+)(?:="([^"]*)"|='([^']*)')?/g)){if(a.index===1)continue;attrs[a[1]]=decode(a[2]??a[3]??'')}const e=new El(tag,attrs);stack[stack.length-1].appendChild(e);if(!voidTags.has(tag)&&!token.endsWith('/>'))stack.push(e)}else stack[stack.length-1]._text+=decode(token)}}
const storage={},session={};let renderedLinks=0;
function open(route,mobile=false){const body=new El('body',{'data-route':route?'/'+route:'/'});const listeners={};const document={body,baseURI:'https://kemcap.github.io/harikaseylerdukkani/entwicklung/',title:'',querySelector:s=>body.querySelector(s),querySelectorAll:s=>body.querySelectorAll(s),getElementById:id=>body.querySelector('#'+id),createElement:t=>new El(t),addEventListener:(n,f)=>(listeners[n]??=[]).push(f)};
 const loc={pathname:'/harikaseylerdukkani/entwicklung/'+route+'/',search:'',hash:'',href:''},window={scrollY:0,addEventListener(){},matchMedia:()=>({matches:mobile,addEventListener(){}})};
 const ctx={document,location:loc,window,URL,URLSearchParams,Intl,setTimeout:f=>{f();return 1},clearTimeout(){},setInterval:()=>1,clearInterval(){},requestAnimationFrame:f=>f(),localStorage:{getItem:k=>storage[k]??null,setItem:(k,v)=>storage[k]=v},sessionStorage:{getItem:k=>session[k]??null,setItem:(k,v)=>session[k]=v},FormData:class{constructor(form){this.form=form}get(k){return this.form.querySelector('[name="'+k+'"]').value}}};
 vm.createContext(ctx);for(const file of ['shop-data.js','layout.js','shop-ui.js'])vm.runInContext(fs.readFileSync(root+'/assets/'+file,'utf8'),ctx,{filename:file});
 function click(el){assert(el,'click target exists');const e={target:el,preventDefault(){}};for(const f of el.listeners.click||[])f(e);for(const f of listeners.click||[])f(e)}
 function submit(selector){const form=document.querySelector(selector);assert(form,selector+' exists');for(const f of form.listeners.submit||[])f({target:form,currentTarget:form,preventDefault(){}})}
 const h1s=body.querySelectorAll('h1');assert.equal(h1s.length,1,route+' must have exactly one main heading');
 for(const el of body.querySelectorAll('a,img,script,link')){const ref=el.attrs.href||el.attrs.src;if(!ref||ref.startsWith('#')||/^[a-z]+:/i.test(ref)||ref==='./')continue;const clean=ref.split(/[?#]/)[0];if(clean.startsWith('${'))continue;assert(!clean.startsWith('/'),route+' absolute path leaks outside preview: '+ref);const target=path.join(root,clean);assert(fs.existsSync(target)||fs.existsSync(path.join(target,'index.html')),route+' missing local link/asset '+ref);renderedLinks++}
 return {ctx,body,document,click,submit,loc,listeners};}
const routes=JSON.parse(fs.readFileSync(root+'/routes.json','utf8'));
for(const r of routes)open(r);
let p=open('');assert.equal(p.document.querySelectorAll('.dark-card').length,3);assert.equal(p.document.querySelectorAll('.dark-cat-btn').length,4);
const heroCards=[...p.document.querySelectorAll('.dark-card')];p.click(p.document.querySelector('[data-theme="light"]'));assert.deepStrictEqual(p.document.querySelectorAll('.dark-card'),heroCards);
p.click(p.document.querySelector('[data-action="add"]'));assert.equal(JSON.parse(storage['harika-demo-cart-v1'])[0].qty,1);
p.click(p.document.querySelector('[data-action="save"]'));assert.equal(JSON.parse(storage['harika-demo-favs-v1']).length,1);
p=open('sepet');assert(p.document.querySelector('.cart-row'),'cart persists across pages');p.click(p.document.querySelector('[data-action="cart-qty"][data-delta="1"]'));assert.equal(JSON.parse(storage['harika-demo-cart-v1'])[0].qty,2);
p=open('odeme');p.submit('#checkout-form');assert(p.loc.href.endsWith('/entwicklung/siparis/'));const selectedCart=JSON.parse(storage['harika-demo-cart-v1']);assert.equal(JSON.parse(session['harika-demo-order']).total,p.ctx.window.Shop.totals(selectedCart).subtotal);
p=open('siparis');assert(p.document.querySelector('.status-box'));
p=open('siparis-takibi');p.document.querySelector('[name="number"]').value='DEMO-001';p.submit('#tracking-form');assert(p.document.querySelector('#tracking-result').innerHTML.includes('Örnek sipariş onaylandı'));
p=open('favoriler');assert.equal(p.document.querySelectorAll('.product-card').length,1);
p=open('giris');p.submit('#auth-form');assert(!Object.keys(storage).some(k=>/password|email/.test(k)));
p=open('');p.ctx.window.scrollY=500;for(const f of p.ctx.window.listeners||[])f();assert(p.document.querySelector('.site-header'));

// Category assignments, collection filters and the persisted gift choice.
p=open('kategoriler');assert.equal(p.document.querySelectorAll('.category-directory-card').length,4);
assert.equal(p.document.querySelectorAll('.category-menu-group').length,4);
assert.equal(p.document.querySelectorAll('.subcategory-toggle').length,4);
const Shop=p.ctx.window.Shop;
for(const c of Shop.categories){assert.equal(c.subcategories.length,6);for(const sub of c.subcategories){const list=Shop.filter(c.id,'','default',sub.id);assert(list.every(x=>x.cat===c.id&&x.subcategories.includes(sub.id)));}}
for(const c of Shop.collections){const list=Shop.filter('','','default','',c.id);assert(list.length>0);assert.equal(new Set(list.map(x=>x.id)).size,list.length);}
p=open('kategori/bijuteri/kupeler');assert.equal(p.document.querySelectorAll('.product-card').length,1);
p=open('kategori/bijuteri/yuzukler');assert.equal(p.document.querySelectorAll('.product-card').length,0);assert(p.document.querySelector('.empty'));
p=open('kampanyali-urunler');assert.equal(p.document.querySelectorAll('.product-card').length,3);assert.equal(p.document.querySelectorAll('del').length,3);
p=open('urun/masa-lambasi');const wrap=p.document.querySelector('#gift-wrap'),note=p.document.querySelector('#gift-note');wrap.checked=true;for(const f of p.listeners.change||[])f({target:wrap});note.value='<b>İyi ki varsın!</b>';for(const f of p.listeners.input||[])f({target:note});
p=open('sepet');assert(p.document.querySelector('#gift-wrap').attrs.checked!==undefined);assert(p.document.querySelector('#gift-note').textContent.includes('<b>İyi ki varsın!</b>'));p=open('odeme');p.submit('#checkout-form');assert.equal(JSON.parse(session['harika-demo-order']).gift.wrap,true);p=open('siparis');assert(p.body.textContent.includes('İyi ki varsın!'));assert(p.body.innerHTML.includes('&lt;b&gt;İyi ki varsın!&lt;/b&gt;'));
p=open('kategoriler',true);const mobileToggles=p.document.querySelectorAll('.subcategory-toggle');assert(mobileToggles.every(b=>b.getAttribute('aria-expanded')==='false'));assert(p.document.querySelectorAll('.submenu-links').every(e=>e.hidden));p.click(mobileToggles[0]);assert.equal(mobileToggles[0].getAttribute('aria-expanded'),'true');assert.equal(p.document.querySelector('#menu-bijuteri').hidden,false);assert.equal(p.document.querySelector('#menu-oyuncak').hidden,true);p.click(mobileToggles[0]);assert.equal(p.document.querySelector('#menu-bijuteri').hidden,true);
console.log('PASS:',routes.length,'rendered routes;',renderedLinks,'local links/assets; persistent cart/favorites, quantity, checkout, order tracking, shared hero theme, auth demo.');
