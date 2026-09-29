// PromptCraft AI - Frontend Application Logic

const API_BASE = "http://localhost:8000/api/v1";

// DOM Elements
const arabicInput = document.getElementById("arabic-input");
const englishOutput = document.getElementById("english-output");
const charCounter = document.getElementById("char-counter");
const domainSelect = document.getElementById("domain-select");
const frameworkSelect = document.getElementById("framework-select");
const providerSelect = document.getElementById("provider-select");
const detectedDomainBadge = document.getElementById("detected-domain-badge");
const speedStat = document.getElementById("speed-stat");
const btnOptimize = document.getElementById("btn-optimize");
const btnCopy = document.getElementById("btn-copy");
const btnExecute = document.getElementById("btn-execute");
const btnLoadSample = document.getElementById("btn-load-sample");
const samplesGrid = document.getElementById("samples-grid");
const executionCard = document.getElementById("execution-card");
const executionOutput = document.getElementById("execution-output");
const apiStatus = document.getElementById("api-status");
const toast = document.getElementById("toast");

let lastOptimizedPrompt = "";

// Show Toast Notification
function showToast(message, duration = 3000) {
  toast.textContent = message;
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), duration);
}

// Update Character Counter
arabicInput.addEventListener("input", () => {
  charCounter.textContent = `${arabicInput.value.length} حرف`;
});

// Load Pre-configured Sample
const SAMPLE_PROMPT = "سوي لي كود فلاتر يربط مع الفايربيس للتحقق من هوية المستخدم برقم الهاتف";

btnLoadSample.addEventListener("click", () => {
  arabicInput.value = SAMPLE_PROMPT;
  charCounter.textContent = `${arabicInput.value.length} حرف`;
  domainSelect.value = "software_engineering";
  frameworkSelect.value = "CO-STAR";
  showToast("تم تحميل نموذج فلاتر الجاهز!");
});

// Check API Health
async function checkApiHealth() {
  try {
    const res = await fetch("http://localhost:8000/health");
    if (res.ok) {
      apiStatus.innerHTML = '<span class="dot"></span> الخادم متصل وجاهز';
      apiStatus.classList.remove("error");
    }
  } catch (err) {
    apiStatus.innerHTML = '<span class="dot" style="background:#ef4444;box-shadow:0 0 8px #ef4444"></span> الخادم غير متصل (تأكد من تشغيل FastAPI)';
  }
}

// Fetch Preset Templates
async function loadTemplates() {
  try {
    const res = await fetch(`${API_BASE}/prompt/templates`);
    if (res.ok) {
      const templates = await res.json();
      renderTemplates(templates);
    }
  } catch (err) {
    console.warn("Could not load templates from API, rendering fallback presets.");
    renderFallbackTemplates();
  }
}

function renderTemplates(templates) {
  samplesGrid.innerHTML = "";
  templates.forEach(t => {
    const card = document.createElement("div");
    card.className = "sample-card";
    card.innerHTML = `
      <div class="sample-title">${t.title_ar}</div>
      <div class="sample-snippet">${t.arabic_prompt}</div>
    `;
    card.addEventListener("click", () => {
      arabicInput.value = t.arabic_prompt;
      domainSelect.value = t.domain;
      frameworkSelect.value = t.framework;
      charCounter.textContent = `${arabicInput.value.length} حرف`;
      showToast(`تم اختيار: ${t.title_ar}`);
      window.scrollTo({ top: 150, behavior: "smooth" });
    });
    samplesGrid.appendChild(card);
  });
}

function renderFallbackTemplates() {
  const fallback = [
    { title_ar: "تطوير فلاتر مع فايربيس", domain: "software_engineering", arabic_prompt: "سوي لي كود فلاتر يربط مع الفايربيس للتحقق من هوية المستخدم برقم الهاتف", framework: "CO-STAR" },
    { title_ar: "نموذج تعلم عميق لتصنيف الصور", domain: "data_science_ai", arabic_prompt: "اريد موديل بايتورش لتصنيف الصور باستخدام كود نظيف وتدريب على GPU", framework: "CO-STAR" },
    { title_ar: "حماية API من هجمات الحقن", domain: "cybersecurity", arabic_prompt: "كيف أحمي مسارات الباك إند بواسطة توكن JWT وأمنع هجمات XSS و CSRF", framework: "CRISPE" },
    { title_ar: "كتابة إطار نظري لبحث التخرج", domain: "academic_research", arabic_prompt: "ساعدني في كتابة مشكلة البحث والمنهجية لدراسة تأثير الذكاء الاصطناعي في التعليم الجامعي", framework: "CO-STAR" }
  ];
  renderTemplates(fallback);
}

// Optimize Prompt Action
btnOptimize.addEventListener("click", async () => {
  const text = arabicInput.value.trim();
  if (!text) {
    showToast("⚠️ يرجى إدخال نص أو فكرة باللغة العربية أولاً!");
    arabicInput.focus();
    return;
  }

  btnOptimize.disabled = true;
  btnOptimize.innerHTML = '<span class="btn-icon">⏳</span><span>جاري التحليل والهندسة...</span>';
  englishOutput.textContent = "// جاري الاتصال بمحرك الوساطة وهندسة البرومبت بأحدث الأطر...\n// يرجى الانتظار ثوانٍ معدودة...";

  const payload = {
    prompt: text,
    domain: domainSelect.value,
    framework: frameworkSelect.value,
    provider: providerSelect.value
  };

  try {
    const res = await fetch(`${API_BASE}/prompt/optimize`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      throw new Error(`خطأ في الخادم (${res.status})`);
    }

    const data = await res.json();
    lastOptimizedPrompt = data.optimized_prompt;
    englishOutput.textContent = data.optimized_prompt;
    detectedDomainBadge.textContent = `المجال: ${data.domain_name_ar}`;
    speedStat.textContent = `⏱️ وقت المعالجة: ${data.processing_time_ms}ms (مزود: ${data.provider})`;
    showToast("🎉 تم تحسين وهندسة البرومبت بنجاح!");
  } catch (err) {
    console.error(err);
    // Offline simulated response
    lastOptimizedPrompt = generateLocalMockOptimization(text, domainSelect.value, frameworkSelect.value);
    englishOutput.textContent = lastOptimizedPrompt;
    detectedDomainBadge.textContent = "المجال: محاكي محلي ذكي (Offline)";
    speedStat.textContent = "⏱️ وقت المعالجة: محاكاة فورية";
    showToast("⚠️ تم التوليد عبر المحاكي الداخلي (الخادم غير نشط)");
  } finally {
    btnOptimize.disabled = false;
    btnOptimize.innerHTML = '<span class="btn-icon">⚡</span><span>هندسة وتحسين البرومبت</span>';
  }
});

// Copy Prompt to Clipboard
btnCopy.addEventListener("click", async () => {
  if (!lastOptimizedPrompt) {
    showToast("⚠️ لا يوجد برومبت منسوخ بعد! قم بالتحسين أولاً.");
    return;
  }

  try {
    await navigator.clipboard.writeText(lastOptimizedPrompt);
    showToast("📋 تم نسخ البرومبت الإنجليزي إلى الحافظة بنجاح!");
  } catch (err) {
    showToast("فشل النسخ التلقائي، يمكنك نسخه يدوياً.");
  }
});

// Execute Prompt against Target Model
btnExecute.addEventListener("click", async () => {
  if (!lastOptimizedPrompt) {
    showToast("⚠️ قم بهندسة البرومبت أولاً قبل اختباره!");
    return;
  }

  btnExecute.disabled = true;
  btnExecute.textContent = "⏳ جاري استدعاء النموذج...";
  executionCard.style.display = "block";
  executionOutput.textContent = "جاري تنفيذ البرومبت على النموذج الهدف... تفكير بالإنجليزية وصياغة المخرج بالعربية...";
  executionCard.scrollIntoView({ behavior: "smooth" });

  try {
    const res = await fetch(`${API_BASE}/prompt/execute`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        prompt: lastOptimizedPrompt,
        provider: providerSelect.value
      })
    });

    if (res.ok) {
      const data = await res.json();
      executionOutput.textContent = data.result;
      showToast("✅ اكتملت إجابة النموذج الهدف بنجاح!");
    } else {
      throw new Error("فشل تنفيذ النموذج");
    }
  } catch (err) {
    executionOutput.textContent = "ملاحظة: لتنفيذ الإجابة الحية، تأكد من وضع مفتاح GEMINI_API_KEY أو OPENAI_API_KEY في ملف .env وتشغيل خادم FastAPI. يمكنك أيضاً نسخ البرومبت ولصقه مباشرة في ChatGPT أو Claude أو Gemini لمشاهدة النتيجة الفائقة فورياً!";
  } finally {
    btnExecute.disabled = false;
    btnExecute.textContent = "🤖 تجربة البرومبت الآن";
  }
});

// Local Fallback Generator
function generateLocalMockOptimization(prompt, domain, framework) {
  return `[ROLE & PERSONA]
Act as an Elite Specialist and Technical Architect.

[CONTEXT]
The user requires a solution for: "${prompt}"

[TASK]
1. Comprehensively analyze the user's intent and architectural constraints.
2. Formulate a modular, production-ready solution adhering strictly to ${framework} framework.
3. Provide full edge case handling, robust error recovery, and clear documentation.

[CONSTRAINTS & QUALITY STANDARDS]
- Ensure all technical terms, code snippets, syntax, and variable names remain in standard English.
- Adhere to enterprise best practices and clean code principles.

[OUTPUT FORMAT]
Provide clean, structured blocks followed by an explanation of key design choices.

[LANGUAGE & RESPONSE DIRECTIVE]
CRITICAL INSTRUCTION FOR THE LLM: 
Analyze, reason, and process the task using your full English technical capability. However, write your entire final output and response in clear, fluent, professional Arabic. Keep all code blocks, commands, technical terms, and variable names in standard English.`;
}

// Initializing
checkApiHealth();
loadTemplates();
