const state = {
  report: null,
  selectedId: null,
  selectedSources: new Set(),
  query: "",
  currentContent: "",
  dirty: false,
  lang: localStorage.getItem("oh-my-skills-lang") || "en",
  theme: localStorage.getItem("oh-my-skills-theme") || "light",
  selectedSkill: null,
};

const translations = {
  en: {
    archive: "Archive",
    archiveConfirm: "Archive this skill folder? It will be moved to ~/.oh-my-skills/archive.",
    archiving: "Archiving...",
    archived: "Archived",
    body: "Body",
    bodyPlaceholder: "# Skill Name",
    brandEyebrow: "Local Skill Manager",
    cancel: "Cancel",
    create: "Create",
    creating: "Creating...",
    created: "Created",
    description: "Description",
    discardConfirm: "Discard unsaved changes?",
    duplicates: "Duplicates",
    editable: "Editable",
    editableSkillLoaded: "Editable skill loaded",
    editableTargets: "Editable Targets",
    exportMarkdown: "Export Markdown",
    followUpdates: "제작자 구독하기",
    inventory: "Inventory",
    name: "Name",
    newSkill: "New Skill",
    noDescription: "No description",
    openChannel: "Open channel",
    openSource: "Open Source",
    readOnly: "Read-only",
    readOnlySkillLoaded: "Read-only skill loaded",
    ready: "Ready",
    save: "Save",
    savedWithBackup: "Saved with backup",
    saving: "Saving...",
    scanning: "Scanning...",
    searchPlaceholder: "Search skills",
    selectSkill: "Select a skill",
    selectSkillHint: "Pick a skill to inspect or edit its SKILL.md.",
    skillCount: "{count} skills",
    sources: "Sources",
    target: "Target",
    themeDark: "Dark",
    themeLight: "Light",
    themeToggleLabel: "Toggle color theme",
    total: "Total",
    defaultCtaNote: "Follow the creator on Threads, Instagram, YouTube, or GitHub.",
  },
  ko: {
    archive: "보관",
    archiveConfirm: "이 스킬 폴더를 보관할까요? ~/.oh-my-skills/archive 로 이동됩니다.",
    archiving: "보관 중...",
    archived: "보관 완료",
    body: "본문",
    bodyPlaceholder: "# 스킬 이름",
    brandEyebrow: "로컬 스킬 매니저",
    cancel: "취소",
    create: "생성",
    creating: "생성 중...",
    created: "생성 완료",
    description: "설명",
    discardConfirm: "저장하지 않은 변경사항을 버릴까요?",
    duplicates: "중복",
    editable: "편집 가능",
    editableSkillLoaded: "편집 가능한 스킬을 불러왔어요",
    editableTargets: "편집 가능한 위치",
    exportMarkdown: "Markdown 내보내기",
    followUpdates: "제작자 구독하기",
    inventory: "인벤토리",
    name: "이름",
    newSkill: "새 스킬",
    noDescription: "설명 없음",
    openChannel: "채널 열기",
    openSource: "오픈소스",
    readOnly: "읽기 전용",
    readOnlySkillLoaded: "읽기 전용 스킬을 불러왔어요",
    ready: "준비됨",
    save: "저장",
    savedWithBackup: "백업 후 저장 완료",
    saving: "저장 중...",
    scanning: "스캔 중...",
    searchPlaceholder: "스킬 검색",
    selectSkill: "스킬을 선택하세요",
    selectSkillHint: "스킬을 선택하면 SKILL.md를 확인하거나 편집할 수 있어요.",
    skillCount: "{count}개 스킬",
    sources: "출처",
    target: "대상",
    themeDark: "다크",
    themeLight: "라이트",
    themeToggleLabel: "컬러 테마 전환",
    total: "전체",
    defaultCtaNote: "Threads, Instagram, YouTube, GitHub에서 제작자를 구독해 주세요.",
  },
};

const els = {
  totalCount: document.querySelector("#totalCount"),
  duplicateCount: document.querySelector("#duplicateCount"),
  visibleCount: document.querySelector("#visibleCount"),
  sourceFilters: document.querySelector("#sourceFilters"),
  targetList: document.querySelector("#targetList"),
  ctaCard: document.querySelector("#ctaCard"),
  ctaTitle: document.querySelector("#ctaTitle"),
  ctaNote: document.querySelector("#ctaNote"),
  ctaLinks: document.querySelector("#ctaLinks"),
  topCtaButton: document.querySelector("#topCtaButton"),
  topCtaMenu: document.querySelector("#topCtaMenu"),
  themeButton: document.querySelector("#themeButton"),
  themeButtonLabel: document.querySelector("#themeButtonLabel"),
  langEnButton: document.querySelector("#langEnButton"),
  langKoButton: document.querySelector("#langKoButton"),
  skillList: document.querySelector("#skillList"),
  searchInput: document.querySelector("#searchInput"),
  refreshButton: document.querySelector("#refreshButton"),
  newButton: document.querySelector("#newButton"),
  emptyState: document.querySelector("#emptyState"),
  editorState: document.querySelector("#editorState"),
  detailSource: document.querySelector("#detailSource"),
  detailName: document.querySelector("#detailName"),
  detailDescription: document.querySelector("#detailDescription"),
  detailPath: document.querySelector("#detailPath"),
  editBadge: document.querySelector("#editBadge"),
  skillEditor: document.querySelector("#skillEditor"),
  saveButton: document.querySelector("#saveButton"),
  archiveButton: document.querySelector("#archiveButton"),
  statusText: document.querySelector("#statusText"),
  newDialog: document.querySelector("#newDialog"),
  newForm: document.querySelector("#newForm"),
  closeDialogButton: document.querySelector("#closeDialogButton"),
  cancelCreateButton: document.querySelector("#cancelCreateButton"),
  targetSelect: document.querySelector("#targetSelect"),
  skillNameInput: document.querySelector("#skillNameInput"),
  skillDescriptionInput: document.querySelector("#skillDescriptionInput"),
  skillBodyInput: document.querySelector("#skillBodyInput"),
};

els.searchInput.addEventListener("input", () => {
  state.query = els.searchInput.value.trim().toLowerCase();
  renderList();
});

els.langEnButton.addEventListener("click", () => setLanguage("en"));
els.langKoButton.addEventListener("click", () => setLanguage("ko"));
els.themeButton.addEventListener("click", () => toggleTheme());
els.refreshButton.addEventListener("click", () => loadState());
els.newButton.addEventListener("click", () => openNewDialog());
els.topCtaButton.addEventListener("click", () => toggleTopCtaMenu());
els.closeDialogButton.addEventListener("click", () => els.newDialog.close());
els.cancelCreateButton.addEventListener("click", () => els.newDialog.close());
els.saveButton.addEventListener("click", () => saveSelectedSkill());
els.archiveButton.addEventListener("click", () => archiveSelectedSkill());
els.skillEditor.addEventListener("input", () => {
  state.dirty = els.skillEditor.value !== state.currentContent;
  els.saveButton.disabled = !state.dirty || els.saveButton.dataset.editable !== "true";
});
els.newForm.addEventListener("submit", (event) => {
  event.preventDefault();
  createNewSkill();
});
document.addEventListener("click", (event) => {
  if (!event.target.closest(".top-cta-wrap")) setTopCtaMenuOpen(false);
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") setTopCtaMenuOpen(false);
});

applyTheme();
applyLanguage();
await loadState();

async function loadState() {
  setStatus(t("scanning"));
  const report = await fetchJson("/api/state");
  state.report = report;
  state.selectedSources = new Set(Object.keys(report.by_source || {}));
  renderSummary();
  renderFilters();
  renderTargets();
  renderCta();
  renderList();
  setStatus(t("ready"));
}

function renderSummary() {
  els.totalCount.textContent = String(state.report.total_skills || 0);
  els.duplicateCount.textContent = String(Object.keys(state.report.duplicate_names || {}).length);
}

function renderFilters() {
  els.sourceFilters.replaceChildren();
  for (const [source, count] of Object.entries(state.report.by_source || {})) {
    const label = document.createElement("label");
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = state.selectedSources.has(source);
    checkbox.addEventListener("change", () => {
      if (checkbox.checked) state.selectedSources.add(source);
      else state.selectedSources.delete(source);
      renderList();
    });
    label.append(checkbox, `${source} (${count})`);
    els.sourceFilters.append(label);
  }
}

function renderTargets() {
  els.targetList.replaceChildren();
  els.targetSelect.replaceChildren();
  for (const [target, path] of Object.entries(state.report.editable_targets || {})) {
    const item = document.createElement("div");
    item.innerHTML = `<strong>${escapeHtml(target)}</strong><br><code>${escapeHtml(path)}</code>`;
    els.targetList.append(item);

    const option = document.createElement("option");
    option.value = target;
    option.textContent = target;
    els.targetSelect.append(option);
  }
}

function renderCta() {
  const cta = state.report.cta || {};
  const url = cta.url || "";
  const reportLinks = Array.isArray(cta.links) ? cta.links : [];
  const links = reportLinks.length ? reportLinks : url ? [{ label: cta.label, url }] : [];
  const hasLinks = links.some((item) => item && item.url);
  const label =
    cta.label === "Follow updates" || cta.label === "제작자 구독하기"
      ? t("followUpdates")
      : cta.label || t("followUpdates");
  const note =
    cta.note === translations.en.defaultCtaNote ? t("defaultCtaNote") : cta.note || "";

  els.ctaTitle.textContent = label;
  els.ctaNote.textContent = note;
  els.topCtaButton.textContent = label;
  renderCtaLinks(links, label, els.ctaLinks);
  renderCtaLinks(links, label, els.topCtaMenu, true);

  els.topCtaButton.classList.toggle("disabled", !hasLinks);
  els.topCtaButton.disabled = !hasLinks;
  els.topCtaButton.setAttribute("aria-disabled", hasLinks ? "false" : "true");

  els.ctaCard.classList.toggle("hidden", !hasLinks);
  els.topCtaButton.classList.toggle("hidden", !hasLinks);
  if (!hasLinks) setTopCtaMenuOpen(false);
}

function renderCtaLinks(links, fallbackLabel, container, menuMode = false) {
  container.replaceChildren();
  const safeLinks = Array.isArray(links) ? links : [];
  for (const item of safeLinks) {
    if (!item || !item.url) continue;
    const link = document.createElement("a");
    link.className = menuMode ? "cta-link menu-link" : "cta-link";
    link.href = item.url;
    link.target = "_blank";
    link.rel = "noreferrer";
    if (menuMode) link.setAttribute("role", "menuitem");
    link.textContent = item.label || fallbackLabel;
    link.addEventListener("click", () => setTopCtaMenuOpen(false));
    container.append(link);
  }
}

function toggleTopCtaMenu() {
  if (els.topCtaButton.disabled) return;
  setTopCtaMenuOpen(els.topCtaMenu.classList.contains("hidden"));
}

function setTopCtaMenuOpen(open) {
  els.topCtaMenu.classList.toggle("hidden", !open);
  els.topCtaButton.setAttribute("aria-expanded", open ? "true" : "false");
}

function renderList() {
  const skills = filteredSkills();
  els.visibleCount.textContent = t("skillCount", { count: skills.length });
  els.skillList.replaceChildren();

  for (const skill of skills) {
    const row = document.createElement("button");
    row.className = `skill-row${skill.id === state.selectedId ? " active" : ""}`;
    row.type = "button";
    row.innerHTML = `
      <span>
        <strong>${escapeHtml(skill.name)}</strong>
        <p>${escapeHtml(skill.description || t("noDescription"))}</p>
      </span>
      <span class="tag">${escapeHtml(skill.source)}</span>
    `;
    row.addEventListener("click", () => selectSkill(skill.id));
    els.skillList.append(row);
  }
}

function filteredSkills() {
  const query = state.query;
  return (state.report.skills || []).filter((skill) => {
    if (!state.selectedSources.has(skill.source)) return false;
    if (!query) return true;
    return [skill.name, skill.description, skill.path, skill.source]
      .join(" ")
      .toLowerCase()
      .includes(query);
  });
}

async function selectSkill(skillId) {
  if (state.dirty && !confirm(t("discardConfirm"))) return;
  state.selectedId = skillId;
  renderList();

  const payload = await fetchJson(`/api/skill?id=${encodeURIComponent(skillId)}`);
  const skill = payload.skill;
  state.selectedSkill = skill;
  state.currentContent = payload.content;
  state.dirty = false;

  els.emptyState.classList.add("hidden");
  els.editorState.classList.remove("hidden");
  els.detailSource.textContent = skill.source;
  els.detailName.textContent = skill.name;
  els.detailDescription.textContent = skill.description || t("noDescription");
  els.detailPath.textContent = skill.path;
  els.skillEditor.value = payload.content;
  els.skillEditor.readOnly = !payload.editable;
  els.editBadge.textContent = payload.editable ? t("editable") : t("readOnly");
  els.editBadge.classList.toggle("editable", Boolean(payload.editable));
  els.saveButton.dataset.editable = payload.editable ? "true" : "false";
  els.saveButton.disabled = true;
  els.archiveButton.disabled = !payload.editable;
  setStatus(payload.editable ? t("editableSkillLoaded") : t("readOnlySkillLoaded"));
}

async function saveSelectedSkill() {
  if (!state.selectedId || !state.dirty) return;
  setStatus(t("saving"));
  await fetchJson(`/api/skill?id=${encodeURIComponent(state.selectedId)}`, {
    method: "PUT",
    body: JSON.stringify({ content: els.skillEditor.value }),
  });
  state.currentContent = els.skillEditor.value;
  state.dirty = false;
  els.saveButton.disabled = true;
  await loadState();
  await selectSkill(state.selectedId);
  setStatus(t("savedWithBackup"));
}

async function archiveSelectedSkill() {
  if (!state.selectedId) return;
  if (!confirm(t("archiveConfirm"))) return;
  setStatus(t("archiving"));
  await fetchJson("/api/skill/archive", {
    method: "POST",
    body: JSON.stringify({ id: state.selectedId }),
  });
  state.selectedId = null;
  state.selectedSkill = null;
  state.currentContent = "";
  state.dirty = false;
  els.editorState.classList.add("hidden");
  els.emptyState.classList.remove("hidden");
  await loadState();
  setStatus(t("archived"));
}

function openNewDialog() {
  els.newForm.reset();
  els.newDialog.showModal();
}

async function createNewSkill() {
  setStatus(t("creating"));
  const payload = {
    target: els.targetSelect.value,
    name: els.skillNameInput.value,
    description: els.skillDescriptionInput.value,
    body: els.skillBodyInput.value,
  };
  const response = await fetchJson("/api/skills", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  els.newDialog.close();
  await loadState();
  await selectSkill(response.skill.id);
  setStatus(t("created"));
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.error || response.statusText);
  }
  return payload;
}

function setStatus(message) {
  els.statusText.textContent = message;
}

function setLanguage(lang) {
  state.lang = lang;
  localStorage.setItem("oh-my-skills-lang", lang);
  applyLanguage();
  renderList();
  if (state.report) renderCta();
  if (state.selectedId) {
    const editable = els.saveButton.dataset.editable === "true";
    els.editBadge.textContent = editable ? t("editable") : t("readOnly");
    els.detailDescription.textContent = state.selectedSkill?.description || t("noDescription");
  }
}

function toggleTheme() {
  setTheme(state.theme === "dark" ? "light" : "dark");
}

function setTheme(theme) {
  state.theme = theme === "dark" ? "dark" : "light";
  localStorage.setItem("oh-my-skills-theme", state.theme);
  applyTheme();
}

function applyTheme() {
  document.documentElement.dataset.theme = state.theme;
  els.themeButton.dataset.marker = state.theme === "dark" ? "[x]" : "[ ]";
  els.themeButtonLabel.textContent = state.theme === "dark" ? t("themeLight") : t("themeDark");
  els.themeButton.setAttribute("aria-label", t("themeToggleLabel"));
}

function applyLanguage() {
  document.documentElement.lang = state.lang === "ko" ? "ko" : "en";
  els.langEnButton.classList.toggle("active", state.lang === "en");
  els.langKoButton.classList.toggle("active", state.lang === "ko");
  applyTheme();

  for (const element of document.querySelectorAll("[data-i18n]")) {
    element.textContent = t(element.dataset.i18n);
  }
  for (const element of document.querySelectorAll("[data-i18n-placeholder]")) {
    element.placeholder = t(element.dataset.i18nPlaceholder);
  }
}

function t(key, values = {}) {
  const dictionary = translations[state.lang] || translations.en;
  let value = dictionary[key] || translations.en[key] || key;
  for (const [name, replacement] of Object.entries(values)) {
    value = value.replace(`{${name}}`, String(replacement));
  }
  return value;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
