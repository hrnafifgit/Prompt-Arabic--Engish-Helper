// PromptCraft AI - Content Script Injector for ChatGPT, Claude, and Gemini

(function () {
  "use strict";

  console.log("PromptCraft AI Content Script loaded.");

  // Target selectors across various LLM web interfaces
  const TARGET_INPUT_SELECTORS = [
    // ChatGPT
    "#prompt-textarea",
    "textarea[data-id='root']",
    "div[contenteditable='true'][id='prompt-textarea']",
    // Claude
    "div[contenteditable='true'][data-placeholder*='Claude']",
    "div.ProseMirror",
    // Gemini
    "rich-textarea textarea",
    ".ql-editor"
  ];

  function showToast(message) {
    const toast = document.createElement("div");
    toast.className = "promptcraft-toast";
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3500);
  }

  function getActiveInputElement() {
    for (const selector of TARGET_INPUT_SELECTORS) {
      const el = document.querySelector(selector);
      if (el) return el;
    }
    // Fallback to active focused textarea
    const active = document.activeElement;
    if (active && (active.tagName === "TEXTAREA" || active.isContentEditable)) {
      return active;
    }
    return null;
  }

  function getInputText(element) {
    if (!element) return "";
    if (element.tagName === "TEXTAREA" || element.tagName === "INPUT") {
      return element.value;
    }
    return element.innerText || element.textContent || "";
  }

  function setInputText(element, text) {
    if (!element) return;
    if (element.tagName === "TEXTAREA" || element.tagName === "INPUT") {
      element.value = text;
      element.dispatchEvent(new Event("input", { bubbles: true }));
      element.dispatchEvent(new Event("change", { bubbles: true }));
    } else if (element.isContentEditable) {
      element.focus();
      document.execCommand("selectAll", false, null);
      document.execCommand("insertText", false, text);
    }
  }

  function injectButton() {
    if (document.getElementById("promptcraft-btn")) return;

    const inputEl = getActiveInputElement();
    if (!inputEl) return;

    const container = inputEl.closest("form") || inputEl.parentElement;
    if (!container) return;

    const btn = document.createElement("button");
    btn.id = "promptcraft-btn";
    btn.className = "promptcraft-floating-btn";
    btn.innerHTML = `<span>⚡</span><span>PromptCraft AI</span>`;
    btn.title = "تحويل الأمر العربي فورياً إلى برومبت إنجليزي فائق الاحترافية";
    btn.type = "button";

    btn.addEventListener("click", async (e) => {
      e.preventDefault();
      e.stopPropagation();

      const rawText = getInputText(inputEl).trim();
      if (!rawText) {
        showToast("⚠️ يرجى كتابة الأمر باللغة العربية أولاً!");
        return;
      }

      btn.classList.add("loading");
      btn.innerHTML = `<span>⏳</span><span>جاري التحسين...</span>`;

      try {
        const config = await new Promise((resolve) => {
          chrome.storage.sync.get(["serverUrl", "preferredDomain", "preferredFramework"], (res) => {
            resolve({
              serverUrl: (res.serverUrl || "http://localhost:8000").replace(/\/+$/, ""),
              domain: res.preferredDomain || "auto",
              framework: res.preferredFramework || "CO-STAR"
            });
          });
        });

        // Send request directly to backend API
        const response = await fetch(`${config.serverUrl}/api/v1/prompt/optimize`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            prompt: rawText,
            domain: config.domain,
            framework: config.framework
          })
        });

        if (!response.ok) {
          throw new Error("فشل الاتصال بالخادم");
        }

        const data = await response.json();
        setInputText(inputEl, data.optimized_prompt);
        showToast(`🎉 تم تعزيز البرومبت بنجاح! (${data.domain_name_ar})`);
      } catch (err) {
        console.error("PromptCraft Optimization Error:", err);
        showToast("⚠️ تعذر الاتصال بالخادم السحابي/المحلي. تحقق من الرابط في الإضافة!");
      } finally {
        btn.classList.remove("loading");
        btn.innerHTML = `<span>⚡</span><span>PromptCraft AI</span>`;
      }
    });

    container.style.position = "relative";
    container.appendChild(btn);
  }

  // Periodic check to attach button when user enters chat page
  setInterval(injectButton, 2000);
})();
