/* Local visual-review harness; injected by the preview server, never published. */
(()=>{
 const bounded=(promise,ms=2000)=>Promise.race([promise,new Promise(resolve=>setTimeout(resolve,ms))]);
 const ready=async()=>{
  await bounded(document.fonts.ready);
  const visible=[...document.images].filter(img=>{const r=img.getBoundingClientRect();return img.getAttribute('src')&&r.width>0&&r.height>0&&r.top<innerHeight&&r.bottom>0;});
  await bounded(Promise.allSettled(visible.map(img=>img.decode())));
  await bounded(new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))),250);
  document.documentElement.dataset.previewReady='true';document.documentElement.dataset.previewPath=location.pathname;
 };
 if(document.readyState==='complete')ready();else addEventListener('load',ready,{once:true});
})();
