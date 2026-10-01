// Extension Popup Script

document.addEventListener("DOMContentLoaded", async () => {
  const domainSelect = document.getElementById("popup-domain");
  const frameworkSelect = document.getElementById("popup-framework");
  const autoReplaceToggle = document.getElementById("auto-replace-toggle");
  const serverUrlInput = document.getElementById("popup-server-url");
  const serverDot = document.getElementById("server-dot");
  const btnDashboard = document.getElementById("btn-open-dashboard");

  let currentServerUrl = "http://localhost:8000";

  async function checkServerHealth(url) {
    serverDot.style.background = "#eab308";
    serverDot.title = "جاري فحص الاتصال...";
    try {
      const normalizedUrl = url.replace(/\/+$/, "");
      const res = await fetch(`${normalizedUrl}/health`, { signal: AbortSignal.timeout(3500) });
      if (res.ok) {
        serverDot.style.background = "#10b981";
        serverDot.title = "الخادم متصل بنجاح";
        return;
      }
    } catch (e) {
      // server unreachable
    }
    serverDot.style.background = "#ef4444";
    serverDot.title = "الخادم غير متاح";
  }

  // Load saved preferences
  chrome.storage.sync.get(["preferredDomain", "preferredFramework", "autoReplace", "serverUrl"], (items) => {
    if (items.preferredDomain) domainSelect.value = items.preferredDomain;
    if (items.preferredFramework) frameworkSelect.value = items.preferredFramework;
    if (typeof items.autoReplace !== "undefined") autoReplaceToggle.checked = items.autoReplace;
    if (items.serverUrl) {
      currentServerUrl = items.serverUrl;
      serverUrlInput.value = items.serverUrl;
    } else {
      serverUrlInput.value = currentServerUrl;
    }
    checkServerHealth(currentServerUrl);
  });

  // Save changes
  domainSelect.addEventListener("change", () => {
    chrome.storage.sync.set({ preferredDomain: domainSelect.value });
  });

  frameworkSelect.addEventListener("change", () => {
    chrome.storage.sync.set({ preferredFramework: frameworkSelect.value });
  });

  autoReplaceToggle.addEventListener("change", () => {
    chrome.storage.sync.set({ autoReplace: autoReplaceToggle.checked });
  });

  serverUrlInput.addEventListener("change", () => {
    const val = serverUrlInput.value.trim().replace(/\/+$/, "") || "http://localhost:8000";
    currentServerUrl = val;
    chrome.storage.sync.set({ serverUrl: val });
    checkServerHealth(val);
  });

  // Open web dashboard in a new tab
  btnDashboard.addEventListener("click", () => {
    chrome.tabs.create({ url: currentServerUrl });
  });
});
