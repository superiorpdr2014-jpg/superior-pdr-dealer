/* =====================================================================
   車行專用估價計算器 CONFIG — SUPERIOR PDR（卓越凹痕修復中心）

   與正式（店內）版的差異：
     · 服務分類只留 PDR 凹痕修復 + 重機油箱/土除
       （已移除 保險桿與鈑金烤漆、汽機車車牌）
     · 修復因素移除：加固鈑件 / 經典古董車金屬 / 稀有車款 / 側向張力
     · 修復模式鎖定「精緻修復 - 大概修復」× 範圍模式
     · 不提供 預覽估價單 / 估價訊息內容 / 保險估價單 / 簡訊 / Email / LINE 傳送
       車行只用「儲存／下載」把估價圖存下來
   ===================================================================== */
window.SHOP_CONFIG = {

  locale: 'zh',
  shopId: 'superior-pdr-dealer',

  // ---- BRANDING ----------------------------------------------------
  brand: {
    companyName:  'Superior PDR',
    // 車行名稱 — 會顯示成「XXX 專用估價計算器」抬頭。
    // 換車行改這一行即可；也可用網址 ?d=車行名稱 臨時覆蓋。
    dealerName:   'BMW 台北汎德濱江服務中心',
    logoUrl:      'logo.png',
    phone:        '0901242511',
    phonePretty:  '0901-242-511',
    website:      'https://www.tar-tw.com/',
    accentColor:  '#cc0000',
    imageAccent:  '#cc0000',
    currencySymbol: 'NT$',
    validityDays: 30,

    experienceLine: 'Superior 提供專業免烤漆凹痕修復服務，保留原漆與原板件，維持車體結構與保值性。',
    guaranteeShort: '滿意保證，不滿意不收費。',
    guaranteeLong:  '我們保證您對修復結果完全滿意，否則不收取任何費用。',

    // 車行版不走伺服器傳送，只產圖下載
    sending:       'manual',
    apiBase:       '',
    smsEndpoint:   '',
    emailEndpoint: '',

    // 鋁合金 / 高強度鋼自動判別（共用 Supabase 車款表）
    aluminum: {
      enabled:     true,
      supabaseUrl: 'https://ffavrtepcitlbmgmrpyu.supabase.co',
      supabaseKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZmYXZydGVwY2l0bGJtZ21ycHl1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDk5MzA5NTYsImV4cCI6MjA2NTUwNjk1Nn0.xFIfrif_6lVOQpg8rCKAEevQGyaEm0CY0EoxFR6A7w4'
    }
  },

  // ---- PRICING (TWD) ------------------------------------------------
  pricing: {
    pdrSizes: [1500,2000,2600,3200,3800,4400,5100,5700,6300,6900,7500,8100,8800,9400,10000,10600,11200,11800,12400,13100,13700,14300,14900,15500],
    pdrSizeLabels: [3,5,8,10,13,15,18,20,23,25,28,30,33,35,38,40,43,45,48,50,53,55,58,60],

    // ⚠ 車行版已移除：braced 加固鈑件 / classic 經典古董車金屬 /
    //                exotic 稀有車款 / lateral 側向張力
    pdrGroups: [
      { id:'access',   factors:[ {id:'edge',pct:25}, {id:'obstructed',pct:25}, {id:'bodyline',pct:50}, {id:'curvature',pct:10}, {id:'lowerbody',pct:20,minPct:10,maxPct:30} ] },
      { id:'severity', factors:[ {id:'shallow',pct:0}, {id:'medium',pct:15}, {id:'deep',pct:30}, {id:'crease',pct:25} ] },
      { id:'material', factors:[ {id:'aluminum',pct:50}, {id:'glue',pct:50}, {id:'structural',pct:35}, {id:'laminated',pct:25}, {id:'sound',pct:25}, {id:'stretch',flat:4000,min:2500,max:8500} ] }
    ],

    // 保險桿／鈑金烤漆分類在車行版已關閉，保留空定義避免引擎取值出錯
    bumperFactors: [],

    paint: [ { id:'flat', price:0 }, { id:'tricoat', price:2500 } ],

    tiers: { practical:0.7, improvement:0.6 },

    panelMinPrices: {
      'Roof': 900,
      'Hood': 900,
      'Left Quarter': 900,
      'Right Quarter': 900,
      'Trunk': 900,
      'Tailgate': 900
    }
  }
};
