// ===== Wandering Turtle =====
(function() {
  // ไม่ใส่ซ้ำถ้ามีอยู่แล้ว
  if (document.getElementById('wander-turtle')) return;

  // สร้าง img element
  const el = document.createElement('img');
  el.id = 'wander-turtle';
  el.src = 'turtle.gif';
  el.alt = 'turtle';
  el.title = 'คลิกดูมีม!';
  el.style.cssText = 'position:fixed;z-index:5;width:130px;pointer-events:none;transition:transform 0.1s;';
  document.body.appendChild(el);

  let x = Math.random() * (window.innerWidth - 170);
  let y = Math.random() * (window.innerHeight - 120);
  let vx = (Math.random() * 1.2 + 0.4) * (Math.random() < 0.5 ? 1 : -1);
  let vy = (Math.random() * 0.8 + 0.2) * (Math.random() < 0.5 ? 1 : -1);
  let paused = false, rafId = null;

  function wander() {
    if (paused) return;
    const W = window.innerWidth, H = window.innerHeight, w = 160, h = 114;
    vx += (Math.random() - 0.5) * 0.08;
    vy += (Math.random() - 0.5) * 0.08;
    const spd = Math.sqrt(vx*vx + vy*vy);
    if (spd > 1.8) { vx=vx/spd*1.8; vy=vy/spd*1.8; }
    if (spd < 0.5) { vx=vx/spd*0.5; vy=vy/spd*0.5; }
    x += vx; y += vy;
    if (x < 0)     { x = 0;     vx =  Math.abs(vx) + Math.random()*0.3; }
    if (x > W - w) { x = W - w; vx = -(Math.abs(vx) + Math.random()*0.3); }
    if (y < 0)     { y = 0;     vy =  Math.abs(vy) + Math.random()*0.3; }
    if (y > H - h) { y = H - h; vy = -(Math.abs(vy) + Math.random()*0.3); }
    el.style.left = x + 'px';
    el.style.top  = y + 'px';
    el.style.transform = vx < 0 ? 'scaleX(-1)' : 'scaleX(1)';
    rafId = requestAnimationFrame(wander);
  }

  function resumeWalking() {
    el.src = 'turtle.gif';
    el.style.width = '160px';
    el.style.pointerEvents = 'none';
    vx = (Math.random() * 1.2 + 0.5) * (Math.random() < 0.5 ? 1 : -1);
    vy = (Math.random() * 0.8 + 0.3) * (Math.random() < 0.5 ? 1 : -1);
    paused = false;
    rafId = requestAnimationFrame(wander);
  }

  // Parse GIF binary หา duration จริง
  async function getGifDuration(url) {
    try {
      const res = await fetch(url, { cache: 'force-cache' });
      const buf = new Uint8Array(await res.arrayBuffer());
      let totalMs = 0, gceFrames = 0, imgFrames = 0, nextHasGce = false;
      let i = 13;
      if (buf[10] & 0x80) i += 3 * (2 << (buf[10] & 0x07));
      while (i < buf.length) {
        if (buf[i] === 0x3B) break;
        if (buf[i] === 0x21) {
          i++;
          const lbl = buf[i++];
          if (lbl === 0xF9) {
            i++; i++;
            let d = buf[i] | (buf[i+1] << 8);
            if (d <= 1) d = 10;
            totalMs += d * 10; gceFrames++; nextHasGce = true; i += 4;
          } else { while (i < buf.length && buf[i] !== 0) i += buf[i] + 1; i++; }
        } else if (buf[i] === 0x2C) {
          imgFrames++;
          if (!nextHasGce) totalMs += 100;
          nextHasGce = false;
          i += 9;
          const packed = buf[i]; i++;
          if (packed & 0x80) i += 3 * (2 << (packed & 0x07));
          i++;
          while (i < buf.length && buf[i] !== 0) i += buf[i] + 1; i++;
        } else { i++; }
      }
      const dur = totalMs > 0 ? totalMs : imgFrames * 100;
      console.log('[Turtle] frames:', imgFrames, '| duration:', dur, 'ms');
      return Math.max(dur, 3000);
    } catch(e) { return 10000; }
  }

  let cachedDur = null;
  getGifDuration('turtle-ai.gif').then(d => { cachedDur = d; });

  // click detection ผ่าน document เพราะ pointer-events:none
  document.addEventListener('click', function(e) {
    const r = el.getBoundingClientRect();
    if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) return;
    if (paused) return;
    paused = true;
    cancelAnimationFrame(rafId);
    el.src = 'turtle-ai.gif?t=' + Date.now();
    el.style.transform = 'scaleX(1)';
    el.style.width = '200px';
    el.style.pointerEvents = 'none';
    const dur = cachedDur || 10000;
    setTimeout(resumeWalking, dur);
  });

  wander();
})();
