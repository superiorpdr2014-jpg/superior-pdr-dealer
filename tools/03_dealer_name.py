# -*- coding: utf-8 -*-
"""車行版第三階段：頁面掛上「某某車行 專用估價計算器」抬頭。
   名稱來源：config.js 的 brand.dealerName，也可用網址 ?d= 覆蓋（一站服務多家車行）。"""
import io, sys

DST = r"C:\Users\User\Downloads\superior-pdr-dealer\index.html"
s = io.open(DST, encoding="utf-8-sig").read()

def rep(old, new, n, tag):
    global s
    c = s.count(old)
    if c != n:
        sys.exit("FAIL[%s] expected %d, found %d" % (tag, n, c))
    s = s.replace(old, new)
    print("ok  ", tag)

# 1) 車行抬頭列的樣式（手機也看得到——header 的 hdr-title 在手機是隱藏的）
rep(u"    .hdr-title{font-size:12px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:#bcbcbc;}",
u"""    .hdr-title{font-size:12px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:#bcbcbc;}
    /* 車行抬頭列：某某車行 專用估價計算器 */
    .dealer-bar{display:none;align-items:center;justify-content:center;gap:10px;flex-wrap:wrap;
      padding:11px 18px;background:linear-gradient(90deg,rgba(204,0,0,.10),rgba(204,0,0,.03));
      border-bottom:1px solid rgba(255,68,68,.18);text-align:center;}
    .dealer-bar.on{display:flex;}
    .dealer-bar .db-name{font-size:15px;font-weight:900;letter-spacing:.5px;color:#fff;}
    .dealer-bar .db-sub{font-size:12px;font-weight:700;letter-spacing:2px;color:#ff8080;text-transform:uppercase;}
    @media(max-width:640px){
      .dealer-bar{padding:9px 14px;gap:4px;flex-direction:column;}
      .dealer-bar .db-name{font-size:14px;}
      .dealer-bar .db-sub{font-size:10.5px;letter-spacing:1.5px;}
    }""", 1, "dealer-bar css")

# 2) 抬頭列本體，放在 header 正下方
rep(u"""  </div>
</div>

<!-- ═══ SHARED: Client & Vehicle ═══ -->""",
u"""  </div>
</div>

<div class="dealer-bar" id="dealer-bar"></div>

<!-- ═══ SHARED: Client & Vehicle ═══ -->""", 1, "dealer-bar markup")

# 3) 帶入車行名稱：config.js 的 dealerName，網址 ?d= 可覆蓋
rep(u"    document.title = CONFIG.companyName + ' \\u2014 ' + t('subtitle');",
u"""    // 車行抬頭：config.js 的 dealerName 為主，網址 ?d=車行名稱 可臨時覆蓋
    var _dealer = '';
    try { _dealer = (new URLSearchParams(location.search)).get('d') || ''; } catch(e) {}
    if (!_dealer) _dealer = CONFIG.dealerName || '';
    var _db = document.getElementById('dealer-bar');
    if (_db && _dealer) {
      _db.innerHTML = '<span class="db-name"></span><span class="db-sub">專用估價計算器</span>';
      _db.querySelector('.db-name').textContent = _dealer;
      _db.classList.add('on');
    }
    document.title = _dealer ? (_dealer + ' 專用估價計算器')
                             : (CONFIG.companyName + ' \\u2014 ' + t('subtitle'));""",
1, "dealer name render")

io.open(DST, "w", encoding="utf-8-sig", newline="").write(s)
print("\npatched", DST)
