# -*- coding: utf-8 -*-
# 凹痕深度（淺／中度／深）防呆：三選一，選了一個自動取消另外兩個。折痕(crease)不受影響。
import io, sys
for p in sys.argv[1:]:
    s = io.open(p, encoding='utf-8').read()
    if 'DEPTH_EXCL' in s: print(p, 'already'); continue
    a1 = "  else { var d = PDR_FDEF[id] || {}; S.pdrFactors[id] = {"
    a2 = "  else { S.motoFactors[id]={amount:motoFactorDefault(id)};"
    assert s.count(a1) == 1 and s.count(a2) == 1, p
    s = s.replace(a1, "  else { clearOtherDepth(S.pdrFactors, '#pdr-factors', id); var d = PDR_FDEF[id] || {}; S.pdrFactors[id] = {")
    s = s.replace(a2, "  else { clearOtherDepth(S.motoFactors, '#moto-factors', id); S.motoFactors[id]={amount:motoFactorDefault(id)};")
    a3 = "function pdrToggleFactor(id) {"
    fn = ("// 凹痕深度防呆：淺／中度／深只能選一個，選了新的就自動取消另外兩個（折痕可以另外疊加）\n"
          "var DEPTH_EXCL = ['shallow','medium','deep'];\n"
          "function clearOtherDepth(store, scope, id) {\n"
          "  if (DEPTH_EXCL.indexOf(id) < 0) return;\n"
          "  DEPTH_EXCL.forEach(function(o){\n"
          "    if (o === id || !store[o]) return;\n"
          "    delete store[o];\n"
          "    var e = document.querySelector(scope + ' .pdr-f[data-fid=\"' + o + '\"]'); if (e) e.classList.remove('on');\n"
          "  });\n"
          "}\n")
    assert s.count(a3) == 1, p
    s = s.replace(a3, fn + a3)
    io.open(p, 'w', encoding='utf-8', newline='').write(s); print(p, 'ok')
