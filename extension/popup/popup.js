// Extension Popup Script

document.addEventListener("DOMContentLoaded", async () => {
  const domainSelect = document.getElementById("popup-domain");
  const frameworkSelect = document.getElementById("popup-framework");
  const autoReplaceToggle = document.getElementById("auto-replace-toggle");
  const serverDot = document.getElementById("server-dot");
  const btnDashboard = document.getElementById("btn-open-dashboard");

  // Load saved preferences
  chrome.storage.sync.get(["preferredDomain", "preferredFramework", "autoReplace"], (items) => {
    if (items.preferredDomain) domainSelect.value = items.preferredDomain;
    if (items.preferredFramework) frameworkSelect.value = items.preferredFramework;
    if (typeof items.autoReplace !== "undefined") autoReplaceToggle.checked = items.autoReplace;
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

  // Check backend server status
  try {
    const res = await fetch("http://localhost:8000/health");
    if (res.ok) {
      serverDot.style.background = "#10b981";
      serverDot.title = "الخادم متصل بنجاح";
    }
  } catch (e) {
    serverDot.style.background = "#ef4444";
    serverDot.title = "الخادم غير متاح";
  }

  // Open web dashboard in a new tab
  btnDashboard.addEventListener("click", () => {
    chrome.tabs.create({ url: "http://localhost:8000" });
  });
});
