# -*- coding: utf-8 -*-
"""車行版第二階段：車身圖與部位清單也把「前／後保險桿」拿掉（保險桿不做 PDR）。"""
import io, sys

DST = r"C:\Users\User\Downloads\superior-pdr-dealer\index.html"
s = io.open(DST, encoding="utf-8-sig").read()

def rep(old, new, n, tag):
    global s
    c = s.count(old)
    if c != n:
        sys.exit("FAIL[%s] expected %d, found %d" % (tag, n, c))
    s = s.replace(old, new)
    print("ok  ", tag, "x%d" % n)

# 1) 部位清單：移除 前保險桿 / 後保險桿 三個角落選項（三種車型各一組）
rep(u"""    { label:'Front Bumper', items:[
      { id:'fb-drv',  label:'Driver Corner', diag:'Front Bumper \u2014 DRV' },
      { id:'fb-mid',  label:'Middle',        diag:'Front Bumper \u2014 MID' },
      { id:'fb-pass', label:'Pass Corner',   diag:'Front Bumper \u2014 PASS'},
    ]},
""", u"", 3, "panel list front bumper")

rep(u"""    { label:'Rear Bumper', items:[
      { id:'rb-drv',  label:'Driver Corner', diag:'Rear Bumper \u2014 DRV' },
      { id:'rb-mid',  label:'Middle',        diag:'Rear Bumper \u2014 MID' },
      { id:'rb-pass', label:'Pass Corner',   diag:'Rear Bumper \u2014 PASS'},
    ]},
""", u"", 3, "panel list rear bumper")

# 2) 車身圖：不再把保險桿切成三段，直接把保險桿區塊藏起來、不可點
rep(u"""    splitBumper(svgEl, 'Front Bumper');
    splitBumper(svgEl, 'Rear Bumper');""",
u"""    hideBumpers(svgEl);   // 車行版：保險桿不做 PDR，從車身圖上移除""",
1, "diagram hide bumpers")

rep(u"""function loadDiagram(type) {""",
u"""// 車行版：把前／後保險桿從車身圖移除（連同標籤），避免被誤點成 PDR 項目
function hideBumpers(svgEl) {
  ['Front Bumper','Rear Bumper'].forEach(function(p){
    svgEl.querySelectorAll('.panel-shape[data-panel="'+p+'"]').forEach(function(el){
      el.style.display = 'none';
      el.style.pointerEvents = 'none';
      var g = el.parentNode;
      var lbl = g && g.querySelector ? g.querySelector('.panel-label') : null;
      if (lbl) lbl.setAttribute('opacity','0');
    });
  });
}

function loadDiagram(type) {""", 1, "hideBumpers helper")

io.open(DST, "w", encoding="utf-8-sig", newline="").write(s)
print("\npatched", DST)
