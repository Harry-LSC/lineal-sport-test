/* LSC tennis live update runtime
   Frozen historical HTML remains the publication snapshot.
   This module applies future workbook-driven updates from data/tennis-data.json.
*/
(async()=>{
  const lineage=document.documentElement.dataset.tennisLineage;
  if(!lineage) return;
  let payload;
  try{
    const r=await fetch('data/tennis-data.json',{cache:'no-store'});
    if(!r.ok) throw new Error('HTTP '+r.status);
    payload=await r.json();
  }catch(e){
    console.error('LSC tennis data load failed',e);
    return;
  }
  const state=(payload.lineages||[]).find(x=>x.lineage===lineage);
  const updates=(payload.lineage_updates||[]).filter(x=>x.lineage===lineage);
  if(!state) return;

  // Expose validated operational state to the frozen page.
  window.LSC_TENNIS_LIVE={state,updates,players:payload.players||[]};

  // Current-holder hero and top-level totals use stable semantic hooks when present.
  const set=(sel,val)=>{const el=document.querySelector(sel);if(el&&val!==undefined&&val!==null)el.textContent=val};
  set('[data-live-current-holder]',state.current_holder);
  set('[data-live-current-defences]',Number(state.current_defences).toLocaleString());
  set('[data-live-transfers]',Number(state.transfers).toLocaleString());
  set('[data-live-total-defences]',Number(state.total_defences).toLocaleString());
  set('[data-live-played-title-matches]',Number(state.played_title_matches).toLocaleString());

  const p=(payload.players||[]).find(x=>x.player===state.current_holder);
  const flag=document.querySelector('[data-live-current-flag]');
  if(flag&&p?.flag){flag.textContent=p.flag;flag.title=p.country||'';}

  document.dispatchEvent(new CustomEvent('lsc-tennis-data-ready',{detail:window.LSC_TENNIS_LIVE}));
})();