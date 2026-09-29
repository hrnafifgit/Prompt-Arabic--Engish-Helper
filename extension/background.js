// PromptCraft AI - Background Service Worker (Manifest V3)

chrome.runtime.onInstalled.addListener(() => {
  console.log("PromptCraft AI Extension installed successfully.");

  // Create context menu item for selected Arabic text
  chrome.contextMenus.create({
    id: "promptcraft-optimize-selection",
    title: "⚡ تحسين البرومبت عبر PromptCraft AI",
    contexts: ["selection"]
  });
});

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId === "promptcraft-optimize-selection" && info.selectionText) {
    try {
      const response = await fetch("http://localhost:8000/api/v1/prompt/optimize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          prompt: info.selectionText,
          domain: "auto",
          framework: "CO-STAR"
        })
      });

      if (response.ok) {
        const data = await response.json();
        // Send message to active tab to display or insert optimized prompt
        chrome.tabs.sendMessage(tab.id, {
          action: "PROMPT_OPTIMIZED",
          data: data
        });
      }
    } catch (err) {
      console.error("Background optimization error:", err);
    }
  }
});
