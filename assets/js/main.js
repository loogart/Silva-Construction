/* Shared behavior. Page text and image lists live in each page's HTML. */
(() => {
  'use strict';
  const english = document.documentElement.lang.startsWith('en');
  const text = english ? {close:'Close', previous:'Previous image', next:'Next image', play:'Play slideshow', pause:'Pause slideshow', original:'Open original image', unavailable:'This local preview cannot send messages. Please use the email or telephone link.'} : {close:'Fermer',previous:'Image précédente',next:'Image suivante',play:'Démarrer le diaporama',pause:'Arrêter le diaporama',original:'Ouvrir l’image originale',unavailable:'Cet aperçu local ne peut pas envoyer de messages. Veuillez utiliser le lien courriel ou téléphone.'};
  const arrow = (left=false) => `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="${left?'m15 5-7 7 7 7':'m9 5 7 7-7 7'}"/></svg>`;
  const header=document.querySelector('.main-header'); let last=0;
  const onScroll=()=>{const y=window.scrollY;header?.classList.toggle('scrollmin',y>0);header?.classList.toggle('scrolled',y>200);header?.classList.toggle('scrollup',y<last);document.querySelector('.back-to-top')?.classList.toggle('visible',y>200);last=y;};
  window.addEventListener('scroll',onScroll,{passive:true}); onScroll();
  document.querySelectorAll('.main-menu .menu-item-has-children > a').forEach(a=>{
    a.setAttribute('aria-expanded','false');
    a.addEventListener('click',e=>{if(a.hash==='#'||a.href.endsWith('#')){e.preventDefault();const open=a.parentElement.classList.toggle('submenuopen');a.setAttribute('aria-expanded',String(open));}});
  });
  document.addEventListener('click',e=>{if(!e.target.closest('.menu-item-has-children'))document.querySelectorAll('.submenuopen').forEach(e=>{e.classList.remove('submenuopen');e.querySelector('a')?.setAttribute('aria-expanded','false');});});
  document.addEventListener('keydown',e=>{if(e.key==='Escape')document.querySelectorAll('.submenuopen').forEach(e=>{e.classList.remove('submenuopen');e.querySelector('a')?.setAttribute('aria-expanded','false');});});
  document.querySelectorAll('[data-contact-form]').forEach(form=>form.addEventListener('submit',e=>{
    e.preventDefault();const note=form.querySelector('.contact-note');note.textContent=text.unavailable;note.setAttribute('role','status');note.scrollIntoView({behavior:'smooth',block:'center'});
  }));
  const links=[...document.querySelectorAll('[data-lightbox]')];
  if(links.length){
    const modal=document.createElement('div');modal.className='modal fade silva-lightbox';modal.id='photo-viewer';modal.tabIndex=-1;modal.setAttribute('aria-label',english?'Photo gallery':'Galerie de photos');
    modal.innerHTML=`<div class="modal-dialog modal-dialog-centered modal-xl"><div class="modal-content"><div class="lightbox-toolbar"><span class="lightbox-counter" aria-live="polite"></span><a class="lightbox-original" target="_blank" rel="noopener noreferrer">${text.original}</a><button type="button" class="lightbox-play">${text.play}</button><button type="button" data-bs-dismiss="modal" aria-label="${text.close}"><svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m6 6 12 12M6 18 18 6"/></svg></button></div><div class="lightbox-stage"><button type="button" class="lightbox-prev" aria-label="${text.previous}">${arrow(true)}</button><img class="lightbox-image" alt=""><button type="button" class="lightbox-next" aria-label="${text.next}">${arrow()}</button></div><p class="lightbox-caption"></p></div></div>`;
    document.body.append(modal);const viewer=new bootstrap.Modal(modal);let index=0,timer,opener;
    const photo=modal.querySelector('.lightbox-image');
    const show=i=>{index=(i+links.length)%links.length;const a=links[index];photo.src=a.href;photo.alt=a.querySelector('img')?.alt||a.title||document.querySelector('h2')?.textContent.trim()||'';modal.querySelector('.lightbox-caption').textContent=a.title||'';modal.querySelector('.lightbox-counter').textContent=`${index+1} / ${links.length}`;modal.querySelector('.lightbox-original').href=a.href;};
    const stop=()=>{clearInterval(timer);timer=null;modal.querySelector('.lightbox-play').textContent=text.play;};
    links.forEach((a,i)=>a.addEventListener('click',e=>{e.preventDefault();opener=a;show(i);viewer.show();}));
    modal.querySelector('.lightbox-prev').addEventListener('click',()=>show(index-1));modal.querySelector('.lightbox-next').addEventListener('click',()=>show(index+1));
    modal.querySelector('.lightbox-play').addEventListener('click',()=>{if(timer)stop();else{timer=setInterval(()=>show(index+1),4500);modal.querySelector('.lightbox-play').textContent=text.pause;}});
    modal.addEventListener('keydown',e=>{if(e.key==='ArrowLeft'){e.preventDefault();show(index-1);}if(e.key==='ArrowRight'){e.preventDefault();show(index+1);}});
    let touchX;photo.addEventListener('touchstart',e=>{touchX=e.changedTouches[0].clientX;},{passive:true});photo.addEventListener('touchend',e=>{const delta=e.changedTouches[0].clientX-touchX;if(Math.abs(delta)>40)show(index+(delta<0?1:-1));},{passive:true});
    modal.addEventListener('hidden.bs.modal',()=>{stop();photo.removeAttribute('src');opener?.focus();});
  }
  // Preserve the existing chat integration on an approved production hostname.
  // Local review never contacts the chat service or sends analytics events.
  if(['silvaconstruction.ca','www.silvaconstruction.ca'].includes(location.hostname)){
    const integration=document.querySelector('[data-integration="tawk"]');
    if(integration){const script=document.createElement('script');script.textContent=integration.textContent;document.body.append(script);}
  }
})();
