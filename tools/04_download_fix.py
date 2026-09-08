# -*- coding: utf-8 -*-
"""車行版第四階段：
   1) 修好「儲存／下載」按了沒反應 —— 原本會先呼叫系統分享（navigator.share），
      桌機叫出分享面板後就卡在「Generating…」、檔案根本沒存下來。車行版一律直接存檔。
   2) 估價單圖片加上車行公司抬頭。
   3) 沒有後端就不要打 /api/estimates/save（會噴 405 錯誤）。
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

# ── 1) 儲存／下載：不要走系統分享，直接存檔 ────────────────────────────────
rep(u"""  if (!canvas.toBlob) { download(null); return; }
  canvas.toBlob(function(blob){
    if (!blob) { download(null); return; }
    try {
      var file = new File([blob], fname, { type:'image/png' });
      if (navigator.canShare && navigator.canShare({ files:[file] }) && navigator.share) {
        navigator.share({ files:[file], title:(CONFIG.companyName||'Superior PDR')+' 估價單' })
          .then(function(){ done(); })
          .catch(function(e){ if (e && e.name === 'AbortError') { done(); } else { download(blob); } });
        return;
      }
    } catch(e) {}
    download(blob);
  }, 'image/png');""",
u"""  // 車行版：一律直接存檔。原本會先試 navigator.share，桌機叫出分享面板後
  // 既沒回呼也沒存檔，按鈕就卡在「Generating…」——這就是「下載沒出現單子」的原因。
  if (!canvas.toBlob) { download(null); return; }
  var _blobDone = false;
  canvas.toBlob(function(blob){
    _blobDone = true;
    download(blob || null);
  }, 'image/png');
  // toBlob 沒回來就用 dataURL 兜底，不讓按鈕永遠卡住
  setTimeout(function(){ if (!_blobDone) { _blobDone = true; download(null); } }, 8000);""",
1, "download always (no share)")

# iOS Safari 不認 a[download]，改開新分頁讓使用者長按儲存
rep(u"""  function download(blob){
    var url = blob ? URL.createObjectURL(blob) : canvas.toDataURL('image/png');
    var a = document.createElement('a'); a.href = url; a.download = fname;
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    if (blob) setTimeout(function(){ URL.revokeObjectURL(url); }, 1500);
    done();
  }""",
u"""  function download(blob){
    var url = blob ? URL.createObjectURL(blob) : canvas.toDataURL('image/png');
    var isIOS = /iP(hone|ad|od)/.test(navigator.userAgent);
    if (isIOS) {
      // iOS Safari 會忽略 a[download]，直接開新分頁讓使用者長按「加入照片」
      window.open(url, '_blank');
    } else {
      var a = document.createElement('a'); a.href = url; a.download = fname;
      document.body.appendChild(a); a.click(); document.body.removeChild(a);
    }
    if (blob) setTimeout(function(){ URL.revokeObjectURL(url); }, 30000);
    done();
  }""", 1, "iOS fallback + longer revoke")

# ── 2) 估價單圖片加上車行公司抬頭 ──────────────────────────────────────────
rep(u"""  h += '.btext{line-height:1.6;color:#555;font-size:.8em}';""",
u"""  h += '.btext{line-height:1.6;color:#555;font-size:.8em}';
  h += '.dlr{background:#fff;padding:13px 22px 12px;text-align:center;border-bottom:1px solid #ececec}';
  h += '.dlr .n{font-size:.95em;font-weight:bold;color:#111;letter-spacing:.5px;line-height:1.35}';
  h += '.dlr .s{display:block;font-size:.6em;color:#cc0000;font-weight:bold;letter-spacing:2px;margin-top:4px}';""",
1, "estimate dealer css")

rep(u"""  h += '<div class="hd"><img src="'+DT_LOGO+'" alt="'+CONFIG.companyName+'"><div class="t">'+t('est_repairEstimate')+'</div></div>';""",
u"""  h += '<div class="hd"><img src="'+DT_LOGO+'" alt="'+CONFIG.companyName+'"><div class="t">'+t('est_repairEstimate')+'</div></div>';
  // 車行公司抬頭（config.js 的 dealerName，或網址 ?d= 覆蓋）
  var _dlrName = '';
  try { _dlrName = (new URLSearchParams(location.search)).get('d') || ''; } catch(e) {}
  if (!_dlrName) _dlrName = CONFIG.dealerName || '';
  if (_dlrName) h += '<div class="dlr"><div class="n">'+esc(_dlrName)+'</div><span class="s">專用估價單</span></div>';""",
1, "estimate dealer header")

# ── 3) 沒有後端就別打 /api/estimates/save ──────────────────────────────────
rep(u"""function saveEstimateRecord(extraFields) {
  var reps = collectRepairs();
  if (!reps.length) return;""",
u"""function saveEstimateRecord(extraFields) {
  var reps = collectRepairs();
  if (!reps.length) return;
  // 車行版沒有後端（apiBase 為空），不要打不存在的端點，否則每次下載都噴 405
  if (!(typeof CONFIG !== 'undefined' && CONFIG.apiBase)) return;""",
1, "skip save endpoint")

io.open(DST, "w", encoding="utf-8-sig", newline="").write(s)
print("\npatched", DST)
