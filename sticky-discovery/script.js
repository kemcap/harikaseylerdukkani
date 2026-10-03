'use strict';
(() => {
 const chapters = [...document.querySelectorAll('.chapter')];
 const images = [...document.querySelectorAll('.stage-images img')];
 const dock = document.querySelector('.story-dock');
 const links = [...dock.querySelectorAll('a')];
 const story = document.querySelector('.story');
 const header = document.querySelector('.header');
 const progress = document.getElementById('stage-progress');
 const label = document.querySelector('.stage-label');
 const detail = document.querySelector('.stage-detail');
 const title = document.getElementById('stage-title');
 const kicker = document.getElementById('stage-kicker');
 const number = document.getElementById('stage-number');
 const detailImage = document.getElementById('stage-detail');
 const detailLabel = document.getElementById('detail-label');
 const reduced = matchMedia('(prefers-reduced-motion: reduce)');
 const desktop = matchMedia('(min-width: 761px)');
 const root = document.documentElement;
 const data = [
  {title:'Hediye dünyası.', kicker:'Küçük sürprizler', color:'#93703b', detail:'cup.jpg', note:'Severek seç.'},
  {title:'Yeni fikirler.', kicker:'Yaz. Çiz. Üret.', color:'#567654', detail:'stationery.jpg', note:'Bir fikirle başlar.'},
  {title:'Zarif detaylar.', kicker:'Sana benzeyen bir parça', color:'#8b6c38', detail:'jewelry.jpg', note:'Kendin gibi.'},
  {title:'Oyun zamanı.', kicker:'Kocaman hayaller', color:'#526e46', detail:'teddy.jpg', note:'Biraz neşe.'}
 ];
 let current = -1, frame = 0, swapTimer, geometry = [], storyTop = 0, storyHeight = 1, isVisible = false;
 let headerAnchor = window.scrollY, headerDirection = 0;
 const clamp = (n,min=0,max=1) => Math.max(min,Math.min(max,n));
 function measure() {
  const y = window.scrollY;
  geometry = chapters.map(chapter => {const r=chapter.getBoundingClientRect();return {top:r.top+y,height:r.height};});
  const r = story.getBoundingClientRect();
  storyTop = r.top+y;
  storyHeight = r.height;
  requestUpdate();
 }
 function activate(index) {
  if (index===current) return;
  current=index;
  images.forEach((image,i)=>image.classList.toggle('active',i===index));
  links.forEach((link,i)=>{link.classList.toggle('active',i===index);if(i===index)link.setAttribute('aria-current','location');else link.removeAttribute('aria-current');});
  root.style.setProperty('--accent',data[index].color);
  label.classList.add('changing');
  clearTimeout(swapTimer);
  const apply = () => {
   title.textContent=data[index].title;
   kicker.textContent=data[index].kicker;
   number.textContent=String(index+1).padStart(2,'0')+' / 04';
   detailImage.src='assets/'+data[index].detail;
   detailLabel.textContent=data[index].note;
   label.classList.remove('changing');
  };
  if(reduced.matches)apply();else swapTimer=setTimeout(apply,160);
 }
 function update() {
  frame=0;
  if(!geometry.length)return;
  const y=window.scrollY, vh=window.innerHeight, focus=y+vh*.45;
  header.classList.toggle('scrolled',y>24);
  const delta = y-headerAnchor;
  const direction = Math.sign(delta);
  if(y<25){
   root.classList.remove('header-compact');
   headerAnchor=y;
   headerDirection=0;
  }else if(direction!==headerDirection){
   headerDirection=direction;
   headerAnchor=y;
  }else if(Math.abs(delta)>12){
   root.classList.toggle('header-compact',direction>0 && y>80);
   headerAnchor=y;
  }
  let index=0;
  for(let i=1;i<geometry.length;i++){if(focus>=geometry[i].top)index=i;}
  activate(index);
  const top=storyTop-y, bottom=top+storyHeight;
  const show=top<vh*.35 && bottom>vh*.55;
  if(show!==isVisible){
   isVisible=show;
   dock.classList.toggle('visible',show);
   dock.inert=!show;
   dock.setAttribute('aria-hidden',String(!show));
  }
  const ratio=clamp((y-storyTop)/Math.max(1,storyHeight-vh));
  progress.style.width=(ratio*100)+'%';
  if(reduced.matches){
   root.style.setProperty('--float-one','0px');
   root.style.setProperty('--float-two','0px');
   detail.style.setProperty('--detail-shift','0px');
   detail.style.setProperty('--detail-opacity','1');
   return;
  }
  if(y<1200){
   root.style.setProperty('--float-one',(Math.min(y,900)*.065)+'px');
   root.style.setProperty('--float-two',(-Math.min(y,900)*.04)+'px');
  }
  if(desktop.matches&&show){
   const phase=clamp((focus-geometry[index].top)/Math.max(1,geometry[index].height));
   detail.style.setProperty('--detail-shift',((phase-.5)*34)+'px');
   detail.style.setProperty('--detail-rotation',(3+phase*5)+'deg');
   detail.style.setProperty('--detail-opacity',String(clamp(Math.min(phase*7,(1-phase)*7),.25,1)));
  }
 }
 function requestUpdate(){if(!frame)frame=requestAnimationFrame(update);}
 if('IntersectionObserver' in window){
  const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('seen');observer.unobserve(entry.target);}}),{threshold:.08});
  document.querySelectorAll('.chapter-copy,.intro-heading,.intro-side,.closer-copy').forEach(el=>observer.observe(el));
  root.classList.add('js-ready');
 }
 window.addEventListener('scroll',requestUpdate,{passive:true});
 window.addEventListener('resize',measure);
 window.addEventListener('load',measure);
 window.addEventListener('pageshow',measure);
 desktop.addEventListener('change',measure);
 reduced.addEventListener('change',requestUpdate);
 if('ResizeObserver' in window){const observer=new ResizeObserver(measure);chapters.forEach(chapter=>observer.observe(chapter));}
 document.getElementById('year').textContent=String(new Date().getFullYear());
 measure();
})();
