# -*- coding: utf-8 -*-
"""從正式估價計算器產生「車行專用版」。來源不動，只輸出到 superior-pdr-dealer。"""
import io, os, sys

SRC = r"C:\Users\User\Downloads\superior-pdr-calc-deploy\index.html"
DST = r"C:\Users\User\Downloads\superior-pdr-dealer\index.html"
KEY = "sp-dealer-7412"

s = io.open(SRC, encoding="utf-8-sig").read()

def rep(old, new, n=1, tag=""):
    global s
    c = s.count(old)
    if c != n:
        sys.exit("FAIL[%s] expected %d occurrence(s), found %d\n---\n%s" % (tag, n, c, old[:200]))
    s = s.replace(old, new)
    print("ok  ", tag)

# ── 1. 標題 + 門禁 + 車行版樣式覆蓋 ──────────────────────────────────────────
GATE = u'''  <title>車行專用估價計算器 — SUPERIOR PDR</title>
  <meta name="robots" content="noindex,nofollow,noarchive">
  <script>
  /* 門禁：網址必須帶 ?k=<金鑰>，否則整頁只顯示上鎖畫面（不含任何估價內容） */
  (function(){
    try{
      var k = (new URLSearchParams(location.search)).get('k') || '';
      if (k !== ''' + repr(str(KEY)) + u''') {
        document.documentElement.setAttribute('data-locked','1');
        document.addEventListener('DOMContentLoaded', function(){
          var d = document.createElement('div');
          d.id = 'lock-screen';
          d.innerHTML = '<div class="lk-box">'
            + '<div class="lk-ico">&#128274;</div>'
            + '<div class="lk-t">此估價工具需要授權連結</div>'
            + '<div class="lk-s">請向卓越凹痕修復中心索取您的專屬網址</div>'
            + '<a class="lk-a" href="https://www.tar-tw.com/" target="_blank" rel="noopener">SUPERIOR PDR 官方網站</a>'
            + '</div>';
          document.body.appendChild(d);
        });
      }
    }catch(e){}
  })();
  </script>
  <style>
    html[data-locked] body > *{display:none !important;}
    html[data-locked] body > #lock-screen{display:flex !important;position:fixed;inset:0;align-items:center;justify-content:center;background:#0d0d0d;z-index:99999;}
    #lock-screen .lk-box{text-align:center;padding:40px 28px;font-family:'Inter',system-ui,sans-serif;}
    #lock-screen .lk-ico{font-size:40px;margin-bottom:16px;}
    #lock-screen .lk-t{color:#fff;font-size:18px;font-weight:800;letter-spacing:.5px;margin-bottom:8px;}
    #lock-screen .lk-s{color:#999;font-size:13px;line-height:1.7;margin-bottom:22px;}
    #lock-screen .lk-a{display:inline-block;padding:10px 22px;border:1px solid rgba(255,68,68,.5);border-radius:4px;color:#ff6666;font-size:12px;font-weight:700;letter-spacing:1px;text-decoration:none;}
    /* ── 車行版：所有步驟固定展開，一頁到底（不用一層層點開） ── */
    .r-card .drawer-body{max-height:none !important;overflow:visible !important;}
    .r-card .drawer-head{margin-bottom:16px;padding-bottom:13px;border-bottom-color:var(--line);cursor:default;}
    .r-card .chev{display:none !important;}
    /* ── 車行版：修復模式固定「精緻修復 - 大概修復」，不給切換 ── */
    .mode-row-locked{display:flex;align-items:center;gap:10px;flex-wrap:wrap;}
    .mode-locked-lbl{font-size:11px;font-weight:800;letter-spacing:1.2px;text-transform:uppercase;color:#8a8a8a;}
    .mode-locked-val{padding:6px 14px;border:1px solid rgba(255,68,68,.35);border-radius:4px;background:rgba(255,68,68,.08);color:#fff;font-size:13px;font-weight:800;letter-spacing:.5px;}
    .qual-note{margin:0 0 16px;padding:11px 13px;border:1px solid rgba(255,255,255,.09);border-left:2px solid var(--accent);border-radius:4px;background:rgba(255,255,255,.02);}
    .qual-note .qn-t{display:block;font-size:12px;color:#bdbdbd;line-height:1.65;margin-bottom:7px;}
    .qual-note a{display:inline-block;color:#ff7a7a;font-size:12px;font-weight:700;text-decoration:none;border-bottom:1px solid rgba(255,122,122,.4);}
    .qual-note a:hover{color:#fff;border-bottom-color:#fff;}
  </style>'''
rep(u'  <title>鈑金烤漆修復估價計算器 — Superior PDR</title>', GATE, 1, "title+gate+css")

# ── 2. 服務分類：拿掉「保險桿與鈑金烤漆」「汽機車車牌」 ──────────────────────
rep(u'''      <button class="svc-btn"    data-svc="bumper" onclick="switchService('bumper')" data-i18n="svc_bumper">Bumper &amp; Panel</button>\n''',
    u'', 1, "remove bumper tab")
rep(u'''      <button class="svc-btn"    data-svc="plate"  onclick="switchService('plate')">汽機車車牌</button>\n''',
    u'', 1, "remove plate tab")

# ── 3. 模式名稱：精緻 - 實用+  →  精緻修復 - 大概修復 ─────────────────────────
rep(u"    view_2opt:'精緻 - 實用', view_3tier:'精緻 - 實用+', view_flat:'固定',",
    u"    view_2opt:'精緻修復 - 平整修復', view_3tier:'精緻修復 - 大概修復', view_flat:'固定',",
    1, "zh view labels")

# 估價單上的方案說明附上差異說明網址
rep(u"    intro_3tier:'以下提供三種專業修復方案供您選擇最適合的成果與價值。每種方案都是品質修復，差異在於精緻程度，而非品質。',",
    u"    intro_3tier:'以下提供三種專業修復方案供您選擇最適合的成果與價值。每種方案都是品質修復，差異在於精緻程度，而非品質。各修復等級的差異說明：https://tar-tw.com/quality/',",
    1, "intro_3tier + url")

# ── 4. 只給「範圍模式 × 精緻修復-大概修復」 ─────────────────────────────────
rep(u"""function presentationPlan(reps) {
  var tier = hasTierWork(reps);
  var view = (S.service === 'bumper' || S.service === 'moto' || S.service === 'plate' || !tier) ? 'itemized' : S.pdrView;
  return { view: view, exact: !!S.exact };
}""",
u"""function presentationPlan(reps) {
  // 車行版：固定「精緻修復 - 大概修復」三方案 × 範圍模式，不提供切換
  var tier = hasTierWork(reps);
  var view = (S.service === 'moto' || !tier) ? 'itemized' : '3tier';
  return { view: view, exact: false };
}""", 1, "presentationPlan locked")

rep(u"""function renderModeButtons() {
  var row = document.getElementById('mode-row');
  if (!row) return;
  // Range / Exact toggle (Bumper calls the exact side "Flat")
  var exactLabel = (S.service === 'bumper') ? t('flat') : t('exact');
  var toggle =
      '<button class="mode-btn'+(!S.exact?' on':'')+'" onclick="setExact(false)">'+t('range')+'</button>'
    + '<button class="mode-btn'+( S.exact?' on':'')+'" onclick="setExact(true)">'+exactLabel+'</button>';

  // When the estimate spans BOTH services we always group by service, so the
  // PDR tier presentation picker doesn't apply — show only Range / Exact.
  var both = serviceCounts(collectRepairs()).both;
  var itemizedSvc = (S.service === 'bumper' || S.service === 'moto' || S.service === 'plate');

  if (itemizedSvc || both) {
    row.className = 'mode-row';
    row.innerHTML = (both ? '<span class="mode-note">'+t('shownByService')+'</span>' : '') + toggle;
  } else {
    row.className = 'mode-row mode-row-select';
    row.innerHTML = '<span class="mode-select-lbl">'+t('repairModes')+'</span>'
      + '<select id="mode-select" class="mode-select" onchange="setPdrView(this.value)">'
      + PDR_VIEWS.map(function(x){ return '<option value="'+x.v+'"'+(x.v===S.pdrView?' selected':'')+'>'+x.label+'</option>'; }).join('')
      + '</select>'
      + '<div class="exact-toggle">' + toggle + '</div>';
  }
}""",
u"""function renderModeButtons() {
  // 車行版：模式鎖定，只顯示目前使用的呈現方式
  var row = document.getElementById('mode-row');
  if (!row) return;
  S.exact = false;
  S.pdrView = '3tier';
  row.className = 'mode-row mode-row-locked';
  row.innerHTML = '<span class="mode-locked-lbl">'+t('repairModes')+'</span>'
                + '<span class="mode-locked-val">'+t('view_3tier')+'</span>';
}""", 1, "renderModeButtons locked")

rep(u"    lblEl.textContent = t('view_3tier') + ' — ' + (exact?t('exact'):t('range'));",
    u"    lblEl.textContent = t('view_3tier');", 1, "3tier breakdown label")

# 預設狀態 & Reset 後都停在 3tier
rep(u"          pdrView:'itemized', exact:false, items:[],",
    u"          pdrView:'3tier', exact:false, items:[],", 1, "default pdrView")
rep(u"  S.pdrView = '2opt'; S.exact = false;",
    u"  S.pdrView = '3tier'; S.exact = false;", 1, "resetAll pdrView")

# ── 5. 修復等級差異說明連結（固定顯示在總價卡上方） ─────────────────────────
rep(u'    <div class="mode-row" id="mode-row"></div>',
u'''    <div class="qual-note">
      <span class="qn-t">三種方案的差異在「精緻程度」，不是品質：精緻修復（完整還原）／平整修復（外觀平整）／大概修復（明顯改善）。</span>
      <a href="https://tar-tw.com/quality/" target="_blank" rel="noopener">看各修復等級的實際差異 ↗</a>
    </div>
    <div class="mode-row" id="mode-row"></div>''', 1, "quality link block")

# ── 6. 拿掉：估價訊息內容 / 預覽估價單 / 傳送類按鈕 / 保險估價單 ─────────────
i = s.index(u'  <!-- Ready-to-send SMS message')
j = s.index(u'  <button class="reset-btn" id="reset-btn"')
assert i < j, "block bounds"
s = s[:i] + u'''  <div class="action-row">
    <button class="dl-btn" id="dl-btn" onclick="downloadPNG()">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
      <span id="dl-btn-label" data-i18n="save">Save / Download</span>
    </button>
  </div>

''' + s[j:]
print("ok   strip msg-card/preview/send/insurance buttons")

io.open(DST, "w", encoding="utf-8-sig", newline="").write(s)
print("\nwrote", DST, os.path.getsize(DST), "bytes")
