# -*- coding: utf-8 -*-
"""車行版第五階段：
   風險3 → 估價單加註「技術執行：SUPERIOR 卓越凹痕修復」，品牌不被架空。
   風險5 → ?d= 改白名單制，只認 config.js dealerAllow 裡指定的店家。
"""
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

# ── 統一的車行名稱來源（白名單制）─────────────────────────────────────────
rep(u"function applyConfig(){",
u"""// 車行名稱唯一來源。網址 ?d= 只接受 config.js dealerAllow 白名單裡的店家，
// 不在名單上（或沒帶）一律退回 dealerName——避免任何拿到連結的人自己冠上公司名。
function currentDealerName(){
  var d = '';
  try { d = (new URLSearchParams(location.search)).get('d') || ''; } catch(e) {}
  var allow = (typeof CONFIG !== 'undefined' && CONFIG.dealerAllow) || [];
  if (d && allow.indexOf(d) >= 0) return d;
  return (typeof CONFIG !== 'undefined' && CONFIG.dealerName) || '';
}

function applyConfig(){""", 1, "currentDealerName helper")

# ── 頁面抬頭改用白名單函式 ────────────────────────────────────────────────
rep(u"""    // 車行抬頭：config.js 的 dealerName 為主，網址 ?d=車行名稱 可臨時覆蓋
    var _dealer = '';
    try { _dealer = (new URLSearchParams(location.search)).get('d') || ''; } catch(e) {}
    if (!_dealer) _dealer = CONFIG.dealerName || '';
    var _db = document.getElementById('dealer-bar');""",
u"""    // 車行抬頭（名稱走白名單，見 currentDealerName）
    var _dealer = currentDealerName();
    var _db = document.getElementById('dealer-bar');""", 1, "header uses whitelist")

# ── 估價單抬頭改用白名單函式，並加上「技術執行」一行 ──────────────────────
rep(u"""  // 車行公司抬頭（config.js 的 dealerName，或網址 ?d= 覆蓋）
  var _dlrName = '';
  try { _dlrName = (new URLSearchParams(location.search)).get('d') || ''; } catch(e) {}
  if (!_dlrName) _dlrName = CONFIG.dealerName || '';
  if (_dlrName) h += '<div class="dlr"><div class="n">'+esc(_dlrName)+'</div><span class="s">專用估價單</span></div>';""",
u"""  // 車行公司抬頭 ＋ 技術執行方（品牌不被架空）
  var _dlrName = currentDealerName();
  if (_dlrName) h += '<div class="dlr"><div class="n">'+esc(_dlrName)+'</div><span class="s">專用估價單</span>'
                   + '<span class="by">技術執行：SUPERIOR 卓越凹痕修復</span></div>';""",
1, "estimate header + tech-by line")

rep(u"""  h += '.dlr .s{display:block;font-size:.6em;color:#cc0000;font-weight:bold;letter-spacing:2px;margin-top:4px}';""",
u"""  h += '.dlr .s{display:block;font-size:.6em;color:#cc0000;font-weight:bold;letter-spacing:2px;margin-top:4px}';
  h += '.dlr .by{display:block;font-size:.62em;color:#666;letter-spacing:.5px;margin-top:8px;padding-top:7px;border-top:1px solid #f0f0f0}';""",
1, "tech-by css")

# ── 下載檔名也走白名單 ────────────────────────────────────────────────────
rep(u"""  // 車行版：檔名用車行 + 卓越，不要留美國原版的 Dent-Time
  var _dn = '';
  try { _dn = (new URLSearchParams(location.search)).get('d') || ''; } catch(e) {}
  if (!_dn) _dn = CONFIG.dealerName || '';
  var fname = (_dn ? _dn + '-' : '') + 'SUPERIOR-PDR-估價單' + slug + '.png';""",
u"""  // 車行版：檔名用車行 + 卓越，不要留美國原版的 Dent-Time
  var _dn = currentDealerName();
  var fname = (_dn ? _dn + '-' : '') + 'SUPERIOR-PDR-估價單' + slug + '.png';""",
1, "filename uses whitelist")

io.open(DST, "w", encoding="utf-8-sig", newline="").write(s)
print("\npatched", DST)
