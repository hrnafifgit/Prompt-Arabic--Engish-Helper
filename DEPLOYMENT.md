# ☁️ دليل النشر السحابي لنظام PromptCraft AI (Cloud Deployment Guide)

يوضح هذا الدليل كيفية رفع وتشغيل نظام **PromptCraft AI** (الباك إند FastAPI + لوحة التحكم Web Dashboard) على خادم سحابي ليعمل على مدار الساعة عبر الإنترنت برابط دائم ومحمي بشهادة SSL (HTTPS)، ثم ربط إضافة المتصفح به.

---

## 🎯 الخيارات المتاحة للنشر السحابي

| الطريقة | التكلفة | الصعوبة | رابط HTTPS | مناسب لـ |
|---|---|---|---|---|
| **Render.com** | مجاني | سهل جداً (مستودع GitHub) | نعم (تلقائي) | الطلاب، العروض التقديمية، الاستخدام الشخصي |
| **Railway.app** | خطة مجانية/رخيصة | سهل جداً | نعم (تلقائي) | المطورين وفرق العمل |
| **VPS (Ubuntu + Docker)** | 4-5$ شهرياً | متوسط | نعم (عبر Certbot) | الإنتاج الكامل والتحكم الشامل |

---

## 🚀 الخيار الأول: النشر السريع والمجاني عبر Render.com (موصى به)

منصة [Render](https://render.com) توفر استضافة سحابية مجانية تدعم بايثون مباشرة من GitHub دون الحاجة لإدارة سيرفر.

### الخطوات:
1. **رفع المشروع إلى GitHub:**
   تأكد من أن جميع التعديلات مرفوعة إلى مستودعك الخاص أو العام على GitHub.
   
2. **إنشاء حساب وتسجيل الدخول في Render:**
   ادخل إلى [dashboard.render.com](https://dashboard.render.com) وسجل الدخول بحساب GitHub.

3. **إنشاء Web Service جديد:**
   - اضغط على زر **New +** ثم اختر **Web Service**.
   - اختر مستودع مشروعك `Prompt-Arabic--Engish-Helper` واضغط **Connect**.

4. **ضبط إعدادات التشغيل (Configuration):**
   - **Name:** `promptcraft-ai` (أو أي اسم تفضله).
   - **Region:** Frankfurt (EU) أو أقرب منطقة لك.
   - **Branch:** `main`.
   - **Root Directory:** اتركه فارغاً.
   - **Runtime:** `Python 3`.
   - **Build Command:**
     ```bash
     pip install -r backend/requirements.txt
     ```
   - **Start Command:**
     ```bash
     uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Instance Type:** `Free`.

5. **إضافة المتغيرات البيئية (Environment Variables):**
   في قسم **Environment Variables**، أضف المفاتيح التالية:
   - `GEMINI_API_KEY`: ضع مفتاحك الخاص بـ Google Gemini.
   - `OPENAI_API_KEY`: (اختياري) في حال رغبت بتفعيل نماذج GPT.
   - `ANTHROPIC_API_KEY`: (اختياري).
   - `APP_ENV`: `production`
   - `ALLOWED_ORIGINS`: `*`

6. **بدء النشر:**
   اضغط على **Create Web Service**. سيقوم Render ببناء التطبيق وتشغيله خلال دقيقة واحدة، وسيعطيك رابطاً سحابياً مثل:
   `https://promptcraft-ai.onrender.com`

7. **التحقق من عمل السيرفر:**
   افتح الرابط في المتصفح، ستظهر لوحة التحكم مباشرة، ويمكنك التأكد من الـ Health Check عبر:
   `https://promptcraft-ai.onrender.com/health`

---

## 🐳 الخيار الثاني: النشر باستخدام Docker على أي سيرفر سحابي (VPS)

إذا كان لديك خادم افتراضي VPS (DigitalOcean, Linode, Hetzner, AWS, Oracle Cloud):

### 1. استنساخ المشروع على السيرفر:
```bash
git clone https://github.com/hrnafifgit/Prompt-Arabic--Engish-Helper.git
cd Prompt-Arabic--Engish-Helper
```

### 2. تجهيز ملف الإعدادات `.env`:
```bash
cp backend/.env.example backend/.env
nano backend/.env
# قم بكتابة مفاتيح الـ API وحفظ الملف (Ctrl+O ثم Ctrl+X)
```

### 3. التشغيل بواسطة Docker Compose:
```bash
docker compose up -d --build
```
سيعمل السيرفر فورياً على المنفذ `8000`.

---

## 🔌 ربط إضافة المتصفح (Chrome Extension) بالسيرفر السحابي

بعد الحصول على رابط سيرفرك السحابي (سواء من Render أو VPS):

1. اضغط على أيقونة إضافة **PromptCraft AI** في شريط المتصفح.
2. في حقل **🌐 رابط السيرفر (Server URL)**، قم بإدخال الرابط السحابي الجديد الخاص بك:
   - مثال: `https://promptcraft-ai.onrender.com`
3. ستلاحظ تحول النقطة في أعلى الإضافة إلى **اللون الأخضر 🟢 (الخادم متصل بنجاح)**.
4. الآن أصبحت الإضافة في متصفحك تعمل مباشرة عبر خادمك السحابي دون الحاجة لتشغيل أي أوامر محلياً على جهازك!
