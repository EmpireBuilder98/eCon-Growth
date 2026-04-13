from pathlib import Path
import re

ROOT = Path('/home/ubuntu/econ-growth')
FILES = sorted(ROOT.glob('*.html'))

CSS_BLOCK = r'''
/* ═══ MOBILE NAV ═══ */
.nav-actions{display:flex;align-items:center;gap:14px;flex-shrink:0}
.nav-toggle{display:none;align-items:center;justify-content:center;width:42px;height:42px;border-radius:10px;border:1px solid rgba(234,240,255,.12);background:rgba(234,240,255,.04);color:var(--text);cursor:pointer;transition:background .2s,border-color .2s,transform .2s}
.nav-toggle:hover{background:rgba(33,230,138,.08);border-color:rgba(33,230,138,.22)}
.nav-toggle:focus-visible{outline:2px solid rgba(33,230,138,.55);outline-offset:3px}
.nav-toggle-bars,.nav-toggle-bars::before,.nav-toggle-bars::after{display:block;position:relative;width:18px;height:2px;border-radius:999px;background:currentColor;transition:transform .25s ease,opacity .2s ease,top .25s ease}
.nav-toggle-bars::before,.nav-toggle-bars::after{content:'';position:absolute;left:0}
.nav-toggle-bars::before{top:-6px}
.nav-toggle-bars::after{top:6px}
.body-menu-open .nav-toggle-bars{background:transparent}
.body-menu-open .nav-toggle-bars::before{top:0;transform:rotate(45deg)}
.body-menu-open .nav-toggle-bars::after{top:0;transform:rotate(-45deg)}
.mobile-menu-overlay{position:fixed;inset:0;background:rgba(4,7,12,.68);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);opacity:0;pointer-events:none;transition:opacity .25s ease;z-index:540}
.mobile-menu{position:fixed;top:0;right:-340px;width:min(88vw,320px);height:100vh;height:100dvh;padding:88px 22px 28px;background:rgba(7,10,15,.98);border-left:1px solid rgba(234,240,255,.08);box-shadow:-24px 0 60px rgba(0,0,0,.35);display:flex;flex-direction:column;gap:18px;transition:right .3s ease;z-index:550}
.mobile-menu-title{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--green)}
.mobile-menu-links{display:flex;flex-direction:column;gap:8px}
.mobile-menu-links a{display:block;padding:13px 14px;border-radius:10px;background:rgba(234,240,255,.03);border:1px solid rgba(234,240,255,.06);color:var(--text);text-decoration:none;font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase;transition:background .2s,border-color .2s,color .2s}
.mobile-menu-links a:hover,.mobile-menu-links a.active{background:rgba(33,230,138,.08);border-color:rgba(33,230,138,.2);color:var(--green)}
.mobile-menu-links .nav-cta,.mobile-menu-cta{margin-top:10px;display:block;width:100%;text-align:center;padding:14px 18px;font-size:14px;border-radius:10px}
.body-menu-open{overflow:hidden}
.body-menu-open .mobile-menu-overlay{opacity:1;pointer-events:auto}
.body-menu-open .mobile-menu{right:0}
@media(max-width:900px){.nav{padding:0 20px}.nav-links,.nav-actions .nav-cta{display:none}.nav-toggle{display:inline-flex}}
'''

SCRIPT_BLOCK = r'''
<script>
(function(){
  const body=document.body;
  const nav=document.getElementById('nav');
  const toggle=document.getElementById('navToggle');
  const drawer=document.getElementById('mobileMenu');
  const overlay=document.getElementById('mobileMenuOverlay');
  const linksTarget=document.getElementById('mobileMenuLinks');

  if(nav&&linksTarget){
    const desktopLinks=nav.querySelector('.nav-links');
    const desktopCta=nav.querySelector('.nav-cta');
    if(desktopLinks){ linksTarget.innerHTML=desktopLinks.innerHTML; }
    if(desktopCta){
      const mobileCta=desktopCta.cloneNode(true);
      mobileCta.classList.add('mobile-menu-cta');
      linksTarget.appendChild(mobileCta);
    }
  }

  window.toggleMobileMenu=function(force){
    const shouldOpen=typeof force==='boolean'?force:!body.classList.contains('body-menu-open');
    body.classList.toggle('body-menu-open',shouldOpen);
    if(toggle){
      toggle.setAttribute('aria-expanded',shouldOpen?'true':'false');
      toggle.setAttribute('aria-label',shouldOpen?'Close navigation menu':'Open navigation menu');
    }
    if(drawer){ drawer.setAttribute('aria-hidden',shouldOpen?'false':'true'); }
  };

  window.closeMobileMenu=function(){ window.toggleMobileMenu(false); };

  if(toggle){
    toggle.addEventListener('click',function(){ window.toggleMobileMenu(); });
  }

  if(overlay){
    overlay.addEventListener('click',window.closeMobileMenu);
  }

  if(linksTarget){
    linksTarget.addEventListener('click',function(event){
      const target=event.target.closest('a');
      if(target){ window.closeMobileMenu(); }
    });
  }

  window.addEventListener('resize',function(){
    if(window.innerWidth>900){ window.closeMobileMenu(); }
  });

  document.addEventListener('keydown',function(event){
    if(event.key==='Escape'){ window.closeMobileMenu(); }
  });
})();
</script>
'''

NAV_REPLACEMENT = '''<div class="nav-actions">
  <a href="book.html" class="nav-cta">Book Your Growth Call</a>
  <button class="nav-toggle" id="navToggle" type="button" aria-label="Open navigation menu" aria-expanded="false" aria-controls="mobileMenu">
    <span class="nav-toggle-bars"></span>
  </button>
</div>
</nav>
<div class="mobile-menu-overlay" id="mobileMenuOverlay"></div>
<aside class="mobile-menu" id="mobileMenu" aria-hidden="true">
  <div class="mobile-menu-title">Navigation</div>
  <nav class="mobile-menu-links" id="mobileMenuLinks" aria-label="Mobile navigation"></nav>
</aside>'''

pattern = re.compile(r'<a\s+href="book\.html"\s+class="nav-cta">Book Your Growth Call</a>\s*</nav>', re.MULTILINE)

updated = []
for path in FILES:
    text = path.read_text()
    if '<nav class="nav"' not in text or 'id="navToggle"' in text:
        continue
    original = text
    text, count = pattern.subn(NAV_REPLACEMENT, text, count=1)
    if count != 1:
        continue
    if '/* ═══ MOBILE NAV ═══ */' not in text and '</style>' in text:
        text = text.replace('</style>', CSS_BLOCK + '\n</style>', 1)
    if 'window.toggleMobileMenu' not in text and '</body>' in text:
        text = text.replace('</body>', SCRIPT_BLOCK + '\n</body>', 1)
    path.write_text(text)
    updated.append(path.name)

print('\n'.join(updated))
