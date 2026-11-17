# sales-archive-relay

RouterOS v6 ရဲ့ `/tool fetch` က HTTP 302 redirect ကို လိုက်မပေးဘူး။
Google Apps Script web app က POST တိုင်းကို 302 နဲ့ ပြန်ပို့တော့
router က ချိတ်မရဘူး (`failure: closing connection: <302 Found ...>`)။

ဒီ relay လေးက အလယ်ကနေ ကူးပေးတယ် —
router က ဒီကို POST ပို့တယ် (redirect မရှိ)၊ relay က Google ဆီ
302 အတိုင်း လိုက်ပို့ပြီး ရတဲ့ `{"ok":true,...}` ကို ပြန်ပေးတယ်။

## Deploy (Render Free)

1. GitHub repo `sales-archive-relay` (public) — ဒီ file 4 ခု။
2. Render → New Web Service → repo ကို ရွေး → Free → Deploy။
3. Environment → `ARCHIVE_URL` မှာ Apps Script `/exec` URL ကို ထည့်။
4. URL က `https://sales-archive-relay.onrender.com` — router script
   ထဲက `:local url` ကို ဒီ URL နဲ့ လဲလိုက်ရင် ရပြီ။
5. စမ်းသပ်ရန် — GET `/` က `OK` ပြန်ရမယ်။

Render Free က 15 မိနစ် မသုံးရင် အိပ်သွားတယ် — လစဉ် 1 ရက်နေ့
ပထမဆုံး ပို့တဲ့အခါ 30-60 စက္ကန့် လောက် နိုးဖို့ ကြာနိုင်တယ်။
Router script ထဲမှာ fetch ကို 3 ကြိမ် ပြန်ကြိုးစားဖို့ ထည့်ထားတယ်။
