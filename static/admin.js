    (function () {
      const unitPanel = document.getElementById("unit-panel");
      const bootstrap = window.__ADMIN_BOOTSTRAP__ || {};
      const problemMeta = Array.isArray(bootstrap.problemMeta) ? bootstrap.problemMeta : [];
      const problemMetaById = new Map(problemMeta.map((row) => [row.id, row]));
      const unitTreeData = Array.isArray(bootstrap.unitTreeData) ? bootstrap.unitTreeData : [];

      const setChecked = (panelId, inputName, checked) => {
        const panel = document.getElementById(panelId);
        if (!panel || !inputName) return;
        panel.querySelectorAll(`input[type="checkbox"][name="${inputName}"]`).forEach((box) => {
          box.checked = checked;
        });
      };

      document.querySelectorAll(".js-select-all").forEach((btn) => {
        btn.addEventListener("click", () => {
          setChecked(btn.dataset.targetPanel, btn.dataset.targetName, true);
        });
      });

      document.querySelectorAll(".js-clear-all").forEach((btn) => {
        btn.addEventListener("click", () => {
          setChecked(btn.dataset.targetPanel, btn.dataset.targetName, false);
        });
      });

      const buildUnitMaps = () => {
        if (!unitPanel) return null;
        const boxes = Array.from(unitPanel.querySelectorAll('input[type="checkbox"][name="unit_nodes"]'));
        const byId = new Map();
        const childrenMap = new Map();
        const parentMap = new Map();

        boxes.forEach((box) => {
          const nodeId = box.dataset.nodeId || "";
          const parentId = box.dataset.parentId || "";
          if (!nodeId) return;
          byId.set(nodeId, box);
          parentMap.set(nodeId, parentId);
          if (parentId) {
            if (!childrenMap.has(parentId)) childrenMap.set(parentId, []);
            childrenMap.get(parentId).push(nodeId);
          }
        });

        return { byId, childrenMap, parentMap };
      };

      const unitMaps = buildUnitMaps();

      const setDescendantsChecked = (nodeId, checked) => {
        if (!unitMaps) return;
        const stack = [nodeId];
        while (stack.length > 0) {
          const current = stack.pop();
          const children = unitMaps.childrenMap.get(current) || [];
          children.forEach((childId) => {
            const childBox = unitMaps.byId.get(childId);
            if (!childBox) return;
            childBox.checked = checked;
            childBox.indeterminate = false;
            stack.push(childId);
          });
        }
      };

      const refreshAncestorState = (nodeId) => {
        if (!unitMaps) return;
        let parentId = unitMaps.parentMap.get(nodeId) || "";
        while (parentId) {
          const parentBox = unitMaps.byId.get(parentId);
          const childIds = unitMaps.childrenMap.get(parentId) || [];
          const childBoxes = childIds.map((id) => unitMaps.byId.get(id)).filter(Boolean);
          if (!parentBox || childBoxes.length === 0) break;

          const allChecked = childBoxes.every((box) => box.checked && !box.indeterminate);
          const noneChecked = childBoxes.every((box) => !box.checked && !box.indeterminate);
          if (allChecked) {
            parentBox.checked = true;
            parentBox.indeterminate = false;
          } else if (noneChecked) {
            parentBox.checked = false;
            parentBox.indeterminate = false;
          } else {
            parentBox.checked = false;
            parentBox.indeterminate = true;
          }
          parentId = unitMaps.parentMap.get(parentId) || "";
        }
      };

      const initUnitTree = () => {
        if (!unitMaps) return;
        unitMaps.byId.forEach((box, nodeId) => {
          if (box.checked) {
            setDescendantsChecked(nodeId, true);
          }
        });
        unitMaps.byId.forEach((box, nodeId) => {
          box.addEventListener("change", () => {
            setDescendantsChecked(nodeId, box.checked);
            refreshAncestorState(nodeId);
          });
        });
        unitMaps.byId.forEach((_, nodeId) => refreshAncestorState(nodeId));
      };

      const setAllUnitNodes = (checked) => {
        if (!unitMaps) return;
        unitMaps.byId.forEach((box) => {
          box.checked = checked;
          box.indeterminate = false;
        });
      };

      document.querySelectorAll(".js-select-all-unit").forEach((btn) => {
        btn.addEventListener("click", () => setAllUnitNodes(true));
      });

      document.querySelectorAll(".js-clear-all-unit").forEach((btn) => {
        btn.addEventListener("click", () => setAllUnitNodes(false));
      });

      initUnitTree();

      const selectorIdsInput = document.getElementById("selector_ids");
      const selectorPatternInput = document.getElementById("selector_pattern");
      const manualOrderIdsInput = document.getElementById("manual_order_ids");
      const manualSelectedIdsInput = document.getElementById("manual_selected_ids");
      const manualOrderList = document.getElementById("manual-order-list");
      const manualOrderWrap = document.querySelector(".manual-order-wrap");
      const manualOrderMain = manualOrderWrap ? manualOrderWrap.querySelector(".manual-order-main") : null;
      const manualPaneResizer = document.getElementById("manual-pane-resizer");
      const manualPaneColumnResizer = document.getElementById("manual-pane-column-resizer");
      const manualPreviewTitle = document.getElementById("manual-preview-title");
      const manualPreviewSubtitle = document.getElementById("manual-preview-subtitle");
      const manualPreviewContent = document.getElementById("manual-preview-content");
      const manualEditorSubtitle = document.getElementById("manual-editor-subtitle");
      const manualEditorStatus = document.getElementById("manual-editor-status");
      const manualEditorReloadBtn = document.getElementById("manual-editor-reload");
      const manualEditorOpenFolderBtn = document.getElementById("manual-editor-open-folder");
      const manualEditorPreviewBtn = document.getElementById("manual-editor-preview");
      const manualEditorSaveBtn = document.getElementById("manual-editor-save");
      const manualEditorQInput = document.getElementById("manual-editor-q");
      const manualEditorChoicesInput = document.getElementById("manual-editor-choices");
      const manualEditorAnswerInput = document.getElementById("manual-editor-answer");
      const manualEditorSolutionInput = document.getElementById("manual-editor-solution");
      const sortFieldInput1 = document.getElementById("sort_field_1");
      const sortFieldInput2 = document.getElementById("sort_field_2");
      const sortFieldInput3 = document.getElementById("sort_field_3");
      const sortFieldInputs = [sortFieldInput1, sortFieldInput2, sortFieldInput3].filter(Boolean);
      const sortOrderInput = document.getElementById("sort_order");
      const renderForm = document.querySelector('form[action="/render"]');
      const loadFilteredOrderBtn = document.querySelector(".js-load-filtered-order");
      const clearManualOrderBtn = document.querySelector(".js-clear-manual-order");
      const manualCheckAllBtn = document.querySelector(".js-manual-check-all");
      const manualUncheckAllBtn = document.querySelector(".js-manual-uncheck-all");
      const defaultPreviewMessage = "문항을 마우스로 클릭하거나, 선택된 문항에서 방향키로 이동하면 미리보기가 갱신됩니다.";
      const metaEditorBackdrop = document.getElementById("meta-editor-backdrop");
      const metaEditorSubtitle = document.getElementById("meta-editor-subtitle");
      const metaEditorStatus = document.getElementById("meta-editor-status");
      const metaEditorDeleteBtn = document.getElementById("meta-editor-delete");
      const metaEditorOpenFolderBtn = document.getElementById("meta-editor-open-folder");
      const metaEditorSaveBtn = document.getElementById("meta-editor-save");
      const metaEditorCancelBtn = document.getElementById("meta-editor-cancel");
      const metaSchoolInput = document.getElementById("meta_school");
      const metaYearInput = document.getElementById("meta_year");
      const metaGradeInput = document.getElementById("meta_grade");
      const metaSemesterInput = document.getElementById("meta_semester");
      const metaExamInput = document.getElementById("meta_exam");
      const metaSubjectInput = document.getElementById("meta_subject");
      const metaSourceNoInput = document.getElementById("meta_source_no");
      const metaSourceKindInput = document.getElementById("meta_source_kind");
      const metaSourceLabelInput = document.getElementById("meta_source_label");
      const metaTypeInput = document.getElementById("meta_type");
      const metaLevelInput = document.getElementById("meta_level");
      const metaDifficultyInput = document.getElementById("meta_difficulty");
      const metaUnitL1Input = document.getElementById("meta_unit_l1");
      const metaUnitL2Input = document.getElementById("meta_unit_l2");
      const metaUnitL3Input = document.getElementById("meta_unit_l3");
      let selectedManualOrderId = "";
      let editingProblemId = "";
      let previewAbortController = null;
      let contentAbortController = null;
      const previewCache = new Map();
      const contentCache = new Map();
      let editorProblemId = "";
      let editorDirty = false;

      const parseIds = (raw) => {
        const token = (raw || "").trim();
        if (!token) return [];
        return token.split(/[\s,]+/).filter(Boolean);
      };

      const MANUAL_PANE_SPLIT_STORAGE_KEY = "manual-pane-preview-height";
      const MANUAL_PANE_COLUMN_SPLIT_STORAGE_KEY = "manual-pane-list-width";
      const MANUAL_PANE_MIN_PREVIEW = 180;
      const MANUAL_PANE_MIN_EDITOR = 280;
      const MANUAL_PANE_MIN_LIST = 280;
      const MANUAL_PANE_MIN_RIGHT = 440;
      const DESKTOP_MANUAL_LAYOUT_QUERY = window.matchMedia("(min-width: 1051px)");

      const parsePx = (raw, fallback = 0) => {
        const value = Number.parseFloat(String(raw || "").trim());
        return Number.isFinite(value) ? value : fallback;
      };

      const getManualPaneMetrics = () => {
        if (!manualOrderWrap || !manualOrderMain) return null;
        const wrapStyle = window.getComputedStyle(manualOrderWrap);
        const mainStyle = window.getComputedStyle(manualOrderMain);
        const totalHeight =
          manualOrderMain.clientHeight ||
          parsePx(wrapStyle.getPropertyValue("--manual-workbench-height"), 1200);
        const rowGap =
          parsePx(mainStyle.rowGap, NaN) ||
          parsePx(mainStyle.gap, NaN) ||
          parsePx(wrapStyle.getPropertyValue("--manual-grid-gap"), 8);
        const resizerHeight = parsePx(wrapStyle.getPropertyValue("--manual-resizer-height"), 12);
        const availableHeight = Math.max(320, totalHeight - rowGap * 2 - resizerHeight);
        const minPreviewHeight = Math.min(MANUAL_PANE_MIN_PREVIEW, availableHeight - 120);
        const maxPreviewHeight = Math.max(minPreviewHeight, availableHeight - MANUAL_PANE_MIN_EDITOR);
        return {
          availableHeight,
          minPreviewHeight,
          maxPreviewHeight,
        };
      };

      const getCurrentManualPreviewHeight = (fallback = 0) => {
        if (!manualOrderWrap) return fallback;
        return parsePx(window.getComputedStyle(manualOrderWrap).getPropertyValue("--manual-top-row-height"), fallback);
      };

      const applyManualPaneSplit = (nextPreviewHeight) => {
        if (!manualOrderWrap) return null;
        const metrics = getManualPaneMetrics();
        if (!metrics) return null;
        let previewHeight = Number(nextPreviewHeight);
        if (!Number.isFinite(previewHeight)) {
          previewHeight = getCurrentManualPreviewHeight(metrics.maxPreviewHeight);
        }
        previewHeight = Math.min(metrics.maxPreviewHeight, Math.max(metrics.minPreviewHeight, previewHeight));
        const editorHeight = Math.max(120, metrics.availableHeight - previewHeight);
        manualOrderWrap.style.setProperty("--manual-top-row-height", `${previewHeight}px`);
        manualOrderWrap.style.setProperty("--manual-editor-row-height", `${editorHeight}px`);

        const baseTopHeight = parsePx(
          window.getComputedStyle(manualOrderWrap).getPropertyValue("--manual-top-row-height-base"),
          previewHeight
        );
        const previewShrinkSize = Math.max(0, baseTopHeight - previewHeight);
        manualOrderWrap.style.setProperty("--manual-preview-shrink-size", `${previewShrinkSize}px`);
        manualOrderWrap.style.setProperty("--manual-q-solution-grow", `${previewShrinkSize / 2}px`);
        return previewHeight;
      };

      const saveManualPaneSplit = (previewHeight) => {
        if (!Number.isFinite(previewHeight)) return;
        try {
          window.localStorage.setItem(MANUAL_PANE_SPLIT_STORAGE_KEY, String(Math.round(previewHeight)));
        } catch (_) {}
      };

      const loadManualPaneSplit = () => {
        try {
          const raw = window.localStorage.getItem(MANUAL_PANE_SPLIT_STORAGE_KEY);
          if (!raw) return null;
          const parsed = Number.parseFloat(raw);
          return Number.isFinite(parsed) ? parsed : null;
        } catch (_) {
          return null;
        }
      };

      const getManualPaneColumnMetrics = () => {
        if (!manualOrderWrap || !manualOrderMain) return null;
        const wrapStyle = window.getComputedStyle(manualOrderWrap);
        const mainStyle = window.getComputedStyle(manualOrderMain);
        const totalWidth = manualOrderMain.clientWidth || manualOrderWrap.clientWidth || 1200;
        const columnGap =
          parsePx(mainStyle.columnGap, NaN) ||
          parsePx(mainStyle.gap, NaN) ||
          parsePx(wrapStyle.getPropertyValue("--manual-grid-gap"), 8);
        const columnResizerWidth = parsePx(wrapStyle.getPropertyValue("--manual-col-resizer-width"), 12);
        const availableWidth = Math.max(560, totalWidth - columnGap * 2 - columnResizerWidth);
        const minListWidth = Math.max(180, Math.min(MANUAL_PANE_MIN_LIST, availableWidth - 180));
        const maxListWidth = Math.max(minListWidth, availableWidth - MANUAL_PANE_MIN_RIGHT);
        return {
          minListWidth,
          maxListWidth,
        };
      };

      const getCurrentManualListWidth = (fallback = 0) => {
        if (!manualOrderWrap) return fallback;
        const fromStyle = parsePx(
          window.getComputedStyle(manualOrderWrap).getPropertyValue("--manual-list-pane-width"),
          Number.NaN
        );
        if (Number.isFinite(fromStyle) && fromStyle > 0) return fromStyle;
        const measured = manualOrderList ? manualOrderList.getBoundingClientRect().width : 0;
        if (Number.isFinite(measured) && measured > 0) return measured;
        return fallback;
      };

      const applyManualPaneColumnSplit = (nextListWidth) => {
        if (!manualOrderWrap) return null;
        const metrics = getManualPaneColumnMetrics();
        if (!metrics) return null;
        let listWidth = Number(nextListWidth);
        if (!Number.isFinite(listWidth)) {
          listWidth = getCurrentManualListWidth((metrics.minListWidth + metrics.maxListWidth) / 2);
        }
        listWidth = Math.min(metrics.maxListWidth, Math.max(metrics.minListWidth, listWidth));
        manualOrderWrap.style.setProperty("--manual-list-pane-width", `${listWidth}px`);
        return listWidth;
      };

      const saveManualPaneColumnSplit = (listWidth) => {
        if (!Number.isFinite(listWidth)) return;
        try {
          window.localStorage.setItem(MANUAL_PANE_COLUMN_SPLIT_STORAGE_KEY, String(Math.round(listWidth)));
        } catch (_) {}
      };

      const loadManualPaneColumnSplit = () => {
        try {
          const raw = window.localStorage.getItem(MANUAL_PANE_COLUMN_SPLIT_STORAGE_KEY);
          if (!raw) return null;
          const parsed = Number.parseFloat(raw);
          return Number.isFinite(parsed) ? parsed : null;
        } catch (_) {
          return null;
        }
      };

      const initManualPaneResizer = () => {
        if (!manualPaneResizer || !manualOrderWrap || !manualOrderMain) return;

        const activateDesktopSplit = () => {
          if (!DESKTOP_MANUAL_LAYOUT_QUERY.matches) return;
          const stored = loadManualPaneSplit();
          const defaultHeight = getCurrentManualPreviewHeight(480);
          const applied = applyManualPaneSplit(stored ?? defaultHeight);
          if (applied !== null) {
            saveManualPaneSplit(applied);
          }
        };

        let dragging = false;
        let startY = 0;
        let startPreviewHeight = 0;

        const clearDraggingState = () => {
          dragging = false;
          manualPaneResizer.classList.remove("is-dragging");
          document.body.classList.remove("manual-pane-resizing-row");
          window.removeEventListener("pointermove", onPointerMove);
          window.removeEventListener("pointerup", onPointerUp);
          window.removeEventListener("pointercancel", onPointerUp);
        };

        const onPointerMove = (event) => {
          if (!dragging) return;
          const deltaY = event.clientY - startY;
          const applied = applyManualPaneSplit(startPreviewHeight + deltaY);
          if (applied !== null) {
            saveManualPaneSplit(applied);
          }
        };

        const onPointerUp = () => {
          if (!dragging) return;
          clearDraggingState();
        };

        manualPaneResizer.addEventListener("pointerdown", (event) => {
          if (event.button !== 0) return;
          if (!DESKTOP_MANUAL_LAYOUT_QUERY.matches) return;
          event.preventDefault();
          const current = applyManualPaneSplit(getCurrentManualPreviewHeight(480));
          startPreviewHeight = Number.isFinite(current) ? current : 480;
          startY = event.clientY;
          dragging = true;
          manualPaneResizer.classList.add("is-dragging");
          document.body.classList.add("manual-pane-resizing-row");
          window.addEventListener("pointermove", onPointerMove);
          window.addEventListener("pointerup", onPointerUp);
          window.addEventListener("pointercancel", onPointerUp);
        });

        manualPaneResizer.addEventListener("keydown", (event) => {
          if (!DESKTOP_MANUAL_LAYOUT_QUERY.matches) return;
          const step = event.shiftKey ? 48 : 24;
          let delta = 0;
          if (event.key === "ArrowUp") delta = -step;
          if (event.key === "ArrowDown") delta = step;
          if (!delta) return;
          event.preventDefault();
          const current = getCurrentManualPreviewHeight(480);
          const applied = applyManualPaneSplit(current + delta);
          if (applied !== null) {
            saveManualPaneSplit(applied);
          }
        });

        window.addEventListener("resize", () => {
          if (!DESKTOP_MANUAL_LAYOUT_QUERY.matches) return;
          const current = getCurrentManualPreviewHeight(480);
          const applied = applyManualPaneSplit(current);
          if (applied !== null) {
            saveManualPaneSplit(applied);
          }
        });

        activateDesktopSplit();
      };

      const initManualPaneColumnResizer = () => {
        if (!manualPaneColumnResizer || !manualOrderWrap || !manualOrderMain) return;

        const activateDesktopColumnSplit = () => {
          if (!DESKTOP_MANUAL_LAYOUT_QUERY.matches) return;
          const stored = loadManualPaneColumnSplit();
          const metrics = getManualPaneColumnMetrics();
          const defaultWidth = getCurrentManualListWidth(
            metrics ? (metrics.minListWidth + metrics.maxListWidth) / 2 : 480
          );
          const applied = applyManualPaneColumnSplit(stored ?? defaultWidth);
          if (applied !== null) {
            saveManualPaneColumnSplit(applied);
          }
        };

        let dragging = false;
        let startX = 0;
        let startListWidth = 0;

        const clearDraggingState = () => {
          dragging = false;
          manualPaneColumnResizer.classList.remove("is-dragging");
          document.body.classList.remove("manual-pane-resizing-col");
          window.removeEventListener("pointermove", onPointerMove);
          window.removeEventListener("pointerup", onPointerUp);
          window.removeEventListener("pointercancel", onPointerUp);
        };

        const onPointerMove = (event) => {
          if (!dragging) return;
          const deltaX = event.clientX - startX;
          const applied = applyManualPaneColumnSplit(startListWidth + deltaX);
          if (applied !== null) {
            saveManualPaneColumnSplit(applied);
          }
        };

        const onPointerUp = () => {
          if (!dragging) return;
          clearDraggingState();
        };

        manualPaneColumnResizer.addEventListener("pointerdown", (event) => {
          if (event.button !== 0) return;
          if (!DESKTOP_MANUAL_LAYOUT_QUERY.matches) return;
          event.preventDefault();
          const current = applyManualPaneColumnSplit(getCurrentManualListWidth(480));
          startListWidth = Number.isFinite(current) ? current : 480;
          startX = event.clientX;
          dragging = true;
          manualPaneColumnResizer.classList.add("is-dragging");
          document.body.classList.add("manual-pane-resizing-col");
          window.addEventListener("pointermove", onPointerMove);
          window.addEventListener("pointerup", onPointerUp);
          window.addEventListener("pointercancel", onPointerUp);
        });

        manualPaneColumnResizer.addEventListener("keydown", (event) => {
          if (!DESKTOP_MANUAL_LAYOUT_QUERY.matches) return;
          const step = event.shiftKey ? 64 : 32;
          let delta = 0;
          if (event.key === "ArrowLeft") delta = -step;
          if (event.key === "ArrowRight") delta = step;
          if (!delta) return;
          event.preventDefault();
          const current = getCurrentManualListWidth(480);
          const applied = applyManualPaneColumnSplit(current + delta);
          if (applied !== null) {
            saveManualPaneColumnSplit(applied);
          }
        });

        window.addEventListener("resize", () => {
          if (!DESKTOP_MANUAL_LAYOUT_QUERY.matches) return;
          const current = getCurrentManualListWidth(480);
          const applied = applyManualPaneColumnSplit(current);
          if (applied !== null) {
            saveManualPaneColumnSplit(applied);
          }
        });

        activateDesktopColumnSplit();
      };

      initManualPaneResizer();
      initManualPaneColumnResizer();

      const uniqueIds = (ids) => {
        const rows = [];
        const seen = new Set();
        ids.forEach((id) => {
          if (!id || seen.has(id)) return;
          seen.add(id);
          rows.push(id);
        });
        return rows;
      };

      const toInt = (value, fallback) => {
        const token = String(value || "").trim();
        return /^[0-9]+$/.test(token) ? Number(token) : fallback;
      };

      const normalizeSortField = (value, slotIndex) => {
        const token = String(value || "").trim().toLowerCase();
        const allFields = new Set(["default", "unit", "school", "year", "source", "manual"]);
        if (slotIndex <= 1) {
          return allFields.has(token) ? token : "default";
        }
        if (token === "none") return "none";
        if (allFields.has(token) && token !== "manual") return token;
        return "none";
      };

      const getSortFieldSlots = () => [
        normalizeSortField(sortFieldInput1 ? sortFieldInput1.value : "default", 1),
        normalizeSortField(sortFieldInput2 ? sortFieldInput2.value : "none", 2),
        normalizeSortField(sortFieldInput3 ? sortFieldInput3.value : "none", 3),
      ];

      const getEffectiveSortFields = () => {
        const ordered = [];
        const slots = getSortFieldSlots();
        for (let index = 0; index < slots.length; index += 1) {
          const field = slots[index];
          const normalized = normalizeSortField(field, index + 1);
          if (normalized === "none") continue;
          if (ordered.includes(normalized)) continue;
          ordered.push(normalized);
          if (normalized === "manual") break;
        }
        return ordered.length ? ordered : ["default"];
      };

      const setMetaEditorStatus = (message, isError = false) => {
        if (!metaEditorStatus) return;
        metaEditorStatus.textContent = String(message || "");
        metaEditorStatus.style.color = isError ? "#b91c1c" : "#334155";
      };

      const SUBJECT_VALUES = ["COM1", "COM2", "ALG", "CAL1", "STAT"];
      const SUBJECT_SET = new Set(SUBJECT_VALUES);
      const normalizeSubjectToken = (value) =>
        String(value || "")
          .trim()
          .replace(/Ⅰ/g, "I")
          .replace(/\s+/g, "")
          .toUpperCase();
      const SUBJECT_ALIASES = new Map(
        [
          ["공통수학1", "COM1"],
          ["공통수학1(2022개정)", "COM1"],
          ["COM1", "COM1"],
          ["COMMON1", "COM1"],
          ["공통수학2", "COM2"],
          ["공통수학2(2022개정)", "COM2"],
          ["COM2", "COM2"],
          ["COMMON2", "COM2"],
          ["대수", "ALG"],
          ["대수(2022개정)", "ALG"],
          ["ALG", "ALG"],
          ["미적분1", "CAL1"],
          ["미적분I", "CAL1"],
          ["미적분Ⅰ", "CAL1"],
          ["미적분I(2022개정)", "CAL1"],
          ["미적분Ⅰ(2022개정)", "CAL1"],
          ["CAL1", "CAL1"],
          ["CALC1", "CAL1"],
          ["확률과통계", "STAT"],
          ["확률과 통계", "STAT"],
          ["확률통계", "STAT"],
          ["확통", "STAT"],
          ["확률과 통계(2022개정)", "STAT"],
          ["STAT", "STAT"],
        ].map(([raw, canonical]) => [normalizeSubjectToken(raw), canonical])
      );
      const inferSubjectFromUnitL1 = (unitL1) => {
        const token = String(unitL1 || "").trim();
        if (!token) return "";
        if (token.startsWith("공통수학1")) return "COM1";
        if (token.startsWith("공통수학2")) return "COM2";
        if (token.startsWith("대수")) return "ALG";
        if (token.startsWith("미적분")) return "CAL1";
        if (token.startsWith("확률과 통계")) return "STAT";
        return "";
      };
      const normalizeSubjectForSelect = (subject, unitL1 = "") => {
        const token = normalizeSubjectToken(subject);
        if (token) {
          const mapped = SUBJECT_ALIASES.get(token);
          if (mapped) return mapped;
        }
        const inferred = inferSubjectFromUnitL1(unitL1);
        if (inferred) return inferred;
        return "";
      };

      const setSelectOptions = (selectEl, options, selectedValue) => {
        if (!selectEl) return;
        const selected = String(selectedValue || "").trim();
        const rows = Array.isArray(options) ? options : [];
        selectEl.innerHTML = rows
          .map((entry) => {
            const value = String((entry && entry.value) || "").trim();
            const label = String((entry && entry.label) || value).trim();
            const picked = value && value === selected ? " selected" : "";
            return `<option value="${escapeHtml(value)}"${picked}>${escapeHtml(label)}</option>`;
          })
          .join("");
        if (rows.length === 0) {
          selectEl.innerHTML = '<option value="">-</option>';
        } else if (!rows.some((entry) => String((entry && entry.value) || "").trim() === selected) && rows[0]) {
          selectEl.value = String((rows[0] && rows[0].value) || "");
        }
      };

      const unitL1Nodes = Array.isArray(unitTreeData) ? unitTreeData : [];
      const stripPrefix = (value, prefix) => {
        const token = String(value || "");
        return token.startsWith(prefix) ? token.slice(prefix.length) : token;
      };
      const unitL1Entries = unitL1Nodes.map((node) => ({
        value: stripPrefix(node.id, "S::"),
        label: String(node.label || ""),
        node,
      }));
      const unitL1Map = new Map(unitL1Entries.map((entry) => [entry.value, entry.node]));

      const syncUnitSelectors = (target = {}) => {
        const selectedL1 = String(target.unit_l1 || (metaUnitL1Input ? metaUnitL1Input.value : "") || "").trim();
        setSelectOptions(metaUnitL1Input, unitL1Entries, selectedL1);

        const currentL1 = metaUnitL1Input ? String(metaUnitL1Input.value || "").trim() : "";
        const l1Node = unitL1Map.get(currentL1) || null;
        const l2Rows = l1Node && Array.isArray(l1Node.children) ? l1Node.children : [];
        const selectedL2 = String(target.unit_l2 || (metaUnitL2Input ? metaUnitL2Input.value : "") || "").trim();
        const l2Entries = l2Rows.map((node) => ({
          value: String(node.label || ""),
          label: String(node.label || ""),
          node,
        }));
        setSelectOptions(metaUnitL2Input, l2Entries, selectedL2);

        const currentL2 = metaUnitL2Input ? String(metaUnitL2Input.value || "").trim() : "";
        const l2Node = l2Entries.find((entry) => String(entry.value || "") === currentL2)?.node || null;
        const l3Rows = l2Node && Array.isArray(l2Node.children) ? l2Node.children : [];
        const selectedL3 = String(target.unit_l3 || (metaUnitL3Input ? metaUnitL3Input.value : "") || "").trim();
        const l3Entries = l3Rows.map((node) => ({
          value: String(node.label || ""),
          label: String(node.label || ""),
        }));
        setSelectOptions(metaUnitL3Input, l3Entries, selectedL3);
      };

      const closeMetaEditor = () => {
        editingProblemId = "";
        if (metaEditorBackdrop) {
          metaEditorBackdrop.classList.remove("open");
          metaEditorBackdrop.setAttribute("aria-hidden", "true");
        }
      };

      const parseGeneratedProblemUiId = (problemId) => {
        const token = String(problemId || "").trim();
        const matched = /^GEN::([^:]+)::(.+)$/.exec(token);
        if (!matched) return null;
        return {
          batchId: String(matched[1] || "").trim(),
          candidateId: String(matched[2] || "").trim(),
        };
      };

      const upsertProblemMetaRow = (row) => {
        if (!row || !row.id) return;
        problemMetaById.set(row.id, row);
        const idx = problemMeta.findIndex((item) => item.id === row.id);
        if (idx >= 0) {
          problemMeta[idx] = row;
        } else {
          problemMeta.push(row);
        }
      };

      const refreshManualListPreservingState = (focusId = "") => {
        const orderIds = getManualListIds();
        const checkedIds = getManualCheckedIds();
        renderManualOrderList(orderIds, { checkedIds, defaultChecked: false });
        if (focusId) {
          selectManualOrderItem(focusId);
          const target = manualOrderList
            ? manualOrderList.querySelector(`.manual-order-item[data-id="${focusId}"]`)
            : null;
          if (target) target.focus();
        }
      };

      const openMetaEditor = async (problemId) => {
        if (!problemId || !metaEditorBackdrop) return;
        const row = problemMetaById.get(problemId) || null;
        const generatedRef = parseGeneratedProblemUiId(problemId);
        editingProblemId = problemId;
        metaEditorBackdrop.classList.add("open");
        metaEditorBackdrop.setAttribute("aria-hidden", "false");
        if (metaEditorSubtitle) {
          metaEditorSubtitle.textContent = row
            ? displayProblemId(row)
            : generatedRef
              ? generatedRef.candidateId
              : problemId;
        }
        setMetaEditorStatus("메타정보를 불러오는 중입니다...");
        if (metaEditorSaveBtn) metaEditorSaveBtn.disabled = true;
        if (metaEditorDeleteBtn) {
          metaEditorDeleteBtn.disabled = true;
          metaEditorDeleteBtn.title = "문항을 삭제합니다.";
        }
        if (metaEditorOpenFolderBtn) {
          metaEditorOpenFolderBtn.disabled = true;
          metaEditorOpenFolderBtn.title = "problem.md 폴더를 엽니다.";
        }

        try {
          const response = await fetch(`/api/problem-meta?id=${encodeURIComponent(problemId)}`);
          if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
          }
          const payload = await response.json();
          const meta = payload && payload.meta ? payload.meta : {};

          if (metaSchoolInput) metaSchoolInput.value = String(meta.school || "");
          if (metaYearInput) metaYearInput.value = String(meta.year || "");
          if (metaGradeInput) metaGradeInput.value = String(meta.grade || "");
          if (metaSemesterInput) metaSemesterInput.value = String(meta.semester || "");
          if (metaExamInput) metaExamInput.value = String(meta.exam || "");
          if (metaSubjectInput) {
            metaSubjectInput.value = normalizeSubjectForSelect(meta.subject, meta.unit_l1);
          }
          if (metaSourceNoInput) metaSourceNoInput.value = String(meta.source_question_no || "");
          if (metaSourceKindInput) metaSourceKindInput.value = String(meta.source_question_kind || "objective");
          if (metaSourceLabelInput) metaSourceLabelInput.value = String(meta.source_question_label || "");
          if (metaTypeInput) metaTypeInput.value = String(meta.type || "");
          if (metaLevelInput) metaLevelInput.value = String(meta.level || "");
          if (metaDifficultyInput) metaDifficultyInput.value = String(meta.difficulty || "");
          syncUnitSelectors({
            unit_l1: meta.unit_l1,
            unit_l2: meta.unit_l2,
            unit_l3: meta.unit_l3,
          });
          setMetaEditorStatus("값을 수정한 뒤 저장하세요.");
        } catch (error) {
          const message = error && error.message ? error.message : "알 수 없는 오류";
          setMetaEditorStatus(`메타정보 로드 실패: ${message}`, true);
        } finally {
          if (metaEditorSaveBtn) metaEditorSaveBtn.disabled = false;
          if (metaEditorDeleteBtn) metaEditorDeleteBtn.disabled = false;
          if (metaEditorOpenFolderBtn) metaEditorOpenFolderBtn.disabled = false;
        }
      };

      const globToRegex = (pattern) => {
        const escaped = String(pattern || "")
          .replace(/[.+^${}()|[\]\\]/g, "\\$&")
          .replace(/\*/g, ".*")
          .replace(/\?/g, ".");
        return new RegExp(`^${escaped}$`);
      };

      const displayProblemId = (row) =>
        String((row && (row.display_id || row.problem_id || row.id)) || "").trim();

      const patternCandidates = (row) => {
        if (!row) return [];
        const id = String(row.id || "").trim();
        const displayId = displayProblemId(row);
        const problemId = String(row.problem_id || "").trim();
        const rootKind = String(row.root_kind || "").trim();
        const batchId = String(row.batch_id || "").trim();
        const school = String(row.school || "").trim();
        const year = String(row.year || "").trim();
        const grade = String(row.grade || "").trim();
        const semester = String(row.semester || "").trim();
        const exam = String(row.exam || "").trim();
        const subject = String(row.subject || "").trim();
        const sourceLabel = String(row.source_label || "").trim();
        const examToken = `${school}.${year}.G${grade}.S${semester}.${exam}${subject ? `(${subject})` : ""}`;
        const examTokenDash = `${school}-${year}-G${grade}-S${semester}-${exam}${subject ? `(${subject})` : ""}`;
        const examTokenSpace = `${school} ${year} G${grade} S${semester} ${exam}${subject ? `(${subject})` : ""}`.trim();
        const idNoNumber = id.replace(/-\d{3}$/, "");
        return [
          id,
          displayId,
          problemId,
          idNoNumber,
          examToken,
          examTokenDash,
          examTokenSpace,
          sourceLabel,
          rootKind,
          batchId,
          batchId && problemId ? `${batchId}/${problemId}` : "",
        ].filter(Boolean);
      };

      const getCheckedValues = (name) =>
        Array.from(document.querySelectorAll(`input[type="checkbox"][name="${name}"]:checked`)).map(
          (box) => box.value
        );

      const unitNodeMatches = (unitPath, nodeId) => {
        if (!unitPath || !nodeId) return false;
        if (nodeId.startsWith("L3::")) {
          return unitPath === nodeId.slice(4);
        }
        if (nodeId.startsWith("L2::")) {
          const prefix = nodeId.slice(4);
          return unitPath === prefix || unitPath.startsWith(`${prefix}>`);
        }
        if (nodeId.startsWith("S::")) {
          const prefix = nodeId.slice(3);
          return unitPath === prefix || unitPath.startsWith(`${prefix}>`);
        }
        return false;
      };

      const unitMatches = (unitPath, selectedNodes) => {
        if (!selectedNodes.length) return true;
        return selectedNodes.some((nodeId) => unitNodeMatches(unitPath, nodeId));
      };

      const syncManualInput = (ids) => {
        if (!manualOrderIdsInput) return;
        manualOrderIdsInput.value = ids.join(" ");
      };

      const syncManualSelectedInput = (ids) => {
        if (!manualSelectedIdsInput) return;
        manualSelectedIdsInput.value = ids.join(" ");
      };

      const getManualListIds = () => {
        if (!manualOrderList) return [];
        return Array.from(manualOrderList.querySelectorAll(".manual-order-item"))
          .map((node) => node.dataset.id || "")
          .filter(Boolean);
      };

      const getManualCheckedIds = () => {
        if (!manualOrderList) return [];
        return Array.from(
          manualOrderList.querySelectorAll('.manual-order-item input.manual-order-check[type="checkbox"]:checked')
        )
          .map((box) => (box.closest(".manual-order-item")?.dataset.id || "").trim())
          .filter(Boolean);
      };

      const syncManualSelectionInputs = () => {
        const orderIds = getManualListIds();
        const selectedIds = getManualCheckedIds();
        syncManualInput(orderIds);
        syncManualSelectedInput(selectedIds);
      };

      const setAllManualChecks = (checked) => {
        if (!manualOrderList) return;
        manualOrderList
          .querySelectorAll('.manual-order-item input.manual-order-check[type="checkbox"]')
          .forEach((box) => {
            box.checked = !!checked;
          });
        syncManualSelectionInputs();
      };

      const escapeHtml = (raw) =>
        String(raw || "")
          .replace(/&/g, "&amp;")
          .replace(/</g, "&lt;")
          .replace(/>/g, "&gt;")
          .replace(/"/g, "&quot;")
          .replace(/'/g, "&#39;");

      const stripCurriculumSuffix = (raw) =>
        String(raw || "")
          .replace(/\s*\(2022개정\)\s*/g, "")
          .replace(/\s+/g, " ")
          .trim();

      const displayUnitPath = (raw) => {
        const token = String(raw || "").trim();
        if (!token) return "";
        return token
          .split(">")
          .map((part) => stripCurriculumSuffix(part))
          .join(">");
      };

      const setPreviewAreaEmpty = (
        titleEl,
        subtitleEl,
        contentEl,
        titleText,
        message,
        subtitle = "문항을 선택하면 미리보기가 표시됩니다."
      ) => {
        if (titleEl) titleEl.textContent = titleText;
        if (subtitleEl) subtitleEl.textContent = subtitle;
        if (contentEl) {
          contentEl.innerHTML = `<p class="manual-preview-empty">${escapeHtml(message)}</p>`;
        }
      };

      const buildPreviewSubtitle = (problemId) => {
        const row = problemMetaById.get(problemId);
        if (!row) return problemId;
        const subject = String(row.subject || "").trim();
        const examInfo = `${row.school} ${row.year} G${row.grade} S${row.semester} ${row.exam}${subject ? `(${subject})` : ""}`;
        const pieces = [examInfo];
        if (String(row.root_kind || "").trim() === "generated") {
          const batchId = String(row.batch_id || "").trim();
          pieces.unshift(batchId ? `유사문항/${batchId}` : "유사문항");
        }
        if (row.source_label) {
          pieces.push(`기출번호 ${row.source_label}`);
        }
        if (row.unit) {
          pieces.push(displayUnitPath(row.unit));
        }
        return pieces.join(" | ");
      };

      const buildPreviewBlocks = (payload) => {
        const questionHtml = String((payload && payload.question_html) || "").trim();
        const choicesHtml = String((payload && payload.choices_html) || "").trim();
        const answerHtml = String((payload && payload.answer_html) || "").trim();
        const solutionHtml = String((payload && payload.solution_html) || "").trim();
        const rows = [
          `
            <section class="manual-preview-block">
              <div class="manual-preview-label">문항</div>
              ${questionHtml || '<p class="manual-preview-empty">문항 본문이 비어 있습니다.</p>'}
            </section>
          `,
        ];
        if (choicesHtml) {
          rows.push(`
            <section class="manual-preview-block">
              <div class="manual-preview-label">선택지</div>
              ${choicesHtml}
            </section>
          `);
        }
        if (answerHtml) {
          rows.push(`
            <section class="manual-preview-block">
              <div class="manual-preview-label">정답</div>
              ${answerHtml}
            </section>
          `);
        }
        rows.push(`
          <section class="manual-preview-block">
            <div class="manual-preview-label">해설</div>
            ${solutionHtml || '<p class="manual-preview-empty">해설 본문이 비어 있습니다.</p>'}
          </section>
        `);
        return rows.join("");
      };

      const renderPreviewInto = (problemId, payload, titleEl, subtitleEl, contentEl, titleText) => {
        if (titleEl) titleEl.textContent = titleText;
        if (subtitleEl) subtitleEl.textContent = buildPreviewSubtitle(problemId);
        if (!contentEl) return;
        contentEl.innerHTML = buildPreviewBlocks(payload);
        if (window.MathJax && typeof window.MathJax.typesetPromise === "function") {
          window.MathJax.typesetPromise([contentEl]).catch(() => {});
        }
      };

      const setPreviewEmpty = (message, subtitle = "문항을 선택하면 미리보기가 표시됩니다.") => {
        setPreviewAreaEmpty(
          manualPreviewTitle,
          manualPreviewSubtitle,
          manualPreviewContent,
          "미리보기",
          message,
          subtitle
        );
      };

      const renderSavedPreviewPayload = (problemId, payload) => {
        renderPreviewInto(
          problemId,
          payload,
          manualPreviewTitle,
          manualPreviewSubtitle,
          manualPreviewContent,
          "미리보기"
        );
      };

      const setEditorStatus = (message, isError = false) => {
        if (!manualEditorStatus) return;
        manualEditorStatus.textContent = String(message || "");
        manualEditorStatus.style.color = isError ? "#b91c1c" : "#475569";
      };

      const openProblemFolderById = async (problemId) => {
        const targetId = String(problemId || "").trim();
        if (!targetId) {
          throw new Error("문항을 먼저 선택하세요.");
        }
        const response = await fetch("/api/problem-open-folder", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ id: targetId }),
        });
        const payload = await response.json().catch(() => ({}));
        if (!response.ok) {
          const detail = payload && payload.detail ? payload.detail : `HTTP ${response.status}`;
          throw new Error(detail);
        }
        return payload;
      };

      const setEditorFields = (sections) => {
        if (manualEditorQInput) manualEditorQInput.value = String((sections && sections.q) || "");
        if (manualEditorChoicesInput) manualEditorChoicesInput.value = String((sections && sections.choices) || "");
        if (manualEditorAnswerInput) manualEditorAnswerInput.value = String((sections && sections.answer) || "");
        if (manualEditorSolutionInput) manualEditorSolutionInput.value = String((sections && sections.solution) || "");
      };

      const getEditorSections = () => ({
        q: manualEditorQInput ? manualEditorQInput.value : "",
        choices: manualEditorChoicesInput ? manualEditorChoicesInput.value : "",
        answer: manualEditorAnswerInput ? manualEditorAnswerInput.value : "",
        solution: manualEditorSolutionInput ? manualEditorSolutionInput.value : "",
      });

      const setEditorDirty = (dirty) => {
        editorDirty = !!dirty;
        if (!manualEditorSubtitle) return;
        if (!editorProblemId) {
          manualEditorSubtitle.textContent = "문항을 선택하면 problem.md 본문을 불러옵니다.";
          return;
        }
        manualEditorSubtitle.textContent = `${editorProblemId}${editorDirty ? " | 미저장 변경 있음" : " | 저장됨"}`;
      };

      const clearEditorPane = () => {
        editorProblemId = "";
        setEditorFields({ q: "", choices: "", answer: "", solution: "" });
        setEditorDirty(false);
        setEditorStatus("문항을 선택하면 편집할 수 있습니다.");
      };

      const loadProblemPreview = async (problemId) => {
        if (!problemId) {
          setPreviewEmpty(defaultPreviewMessage);
          return;
        }

        if (previewCache.has(problemId)) {
          const cached = previewCache.get(problemId);
          renderSavedPreviewPayload(problemId, cached);
          return;
        }

        if (previewAbortController) {
          previewAbortController.abort();
        }
        previewAbortController = new AbortController();

        if (manualPreviewTitle) manualPreviewTitle.textContent = "미리보기";
        if (manualPreviewSubtitle) manualPreviewSubtitle.textContent = buildPreviewSubtitle(problemId);
        if (manualPreviewContent) {
          manualPreviewContent.innerHTML = '<p class="manual-preview-empty">미리보기를 불러오는 중입니다...</p>';
        }

        try {
          const response = await fetch(`/api/problem-preview?id=${encodeURIComponent(problemId)}`, {
            signal: previewAbortController.signal,
          });
          if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
          }
          const payload = await response.json();
          previewCache.set(problemId, payload);
          if (selectedManualOrderId !== problemId) return;
          renderSavedPreviewPayload(problemId, payload);
        } catch (error) {
          if (error && error.name === "AbortError") return;
          if (selectedManualOrderId !== problemId) return;
          const message = error && error.message ? error.message : "알 수 없는 오류";
          setPreviewEmpty(`미리보기를 불러오지 못했습니다. (${message})`, buildPreviewSubtitle(problemId));
        }
      };

      const loadProblemContent = async (problemId, force = false) => {
        if (!problemId) {
          clearEditorPane();
          return;
        }
        if (!force && contentCache.has(problemId)) {
          const cached = contentCache.get(problemId);
          setEditorFields(cached);
          editorProblemId = problemId;
          setEditorDirty(false);
          setEditorStatus("본문 로드 완료");
          if (previewCache.has(problemId)) {
            renderSavedPreviewPayload(problemId, previewCache.get(problemId));
          }
          return;
        }

        if (contentAbortController) {
          contentAbortController.abort();
        }
        contentAbortController = new AbortController();
        setEditorStatus("본문을 불러오는 중입니다...");
        editorProblemId = problemId;
        setEditorDirty(false);

        try {
          const response = await fetch(`/api/problem-content?id=${encodeURIComponent(problemId)}`, {
            signal: contentAbortController.signal,
          });
          if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
          }
          const payload = await response.json();
          if (selectedManualOrderId !== problemId) return;
          const sections = {
            q: String((payload && payload.q) || ""),
            choices: String((payload && payload.choices) || ""),
            answer: String((payload && payload.answer) || ""),
            solution: String((payload && payload.solution) || ""),
          };
          contentCache.set(problemId, sections);
          setEditorFields(sections);
          editorProblemId = problemId;
          setEditorDirty(false);
          setEditorStatus("본문 로드 완료");
          if (previewCache.has(problemId)) {
            renderSavedPreviewPayload(problemId, previewCache.get(problemId));
          }
        } catch (error) {
          if (error && error.name === "AbortError") return;
          const message = error && error.message ? error.message : "알 수 없는 오류";
          setEditorStatus(`본문 로드 실패: ${message}`, true);
        }
      };

      const renderDraftPreviewFromEditor = async () => {
        if (!editorProblemId) {
          setPreviewEmpty("문항을 먼저 선택하세요.");
          return;
        }
        const sections = getEditorSections();
        setEditorStatus("편집 미리보기를 렌더링하는 중입니다...");
        if (manualPreviewTitle) manualPreviewTitle.textContent = "미리보기";
        if (manualPreviewSubtitle) manualPreviewSubtitle.textContent = buildPreviewSubtitle(editorProblemId);
        if (manualPreviewContent) {
          manualPreviewContent.innerHTML = '<p class="manual-preview-empty">편집 미리보기를 불러오는 중입니다...</p>';
        }

        try {
          const response = await fetch("/api/problem-preview-render", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              id: editorProblemId,
              q: sections.q,
              choices: sections.choices,
              answer: sections.answer,
              solution: sections.solution,
            }),
          });
          if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
          }
          const payload = await response.json();
          renderSavedPreviewPayload(editorProblemId, payload);
          setEditorStatus("편집 미리보기 갱신 완료");
        } catch (error) {
          const message = error && error.message ? error.message : "알 수 없는 오류";
          setEditorStatus(`편집 미리보기 실패: ${message}`, true);
          setPreviewEmpty(`편집 미리보기를 불러오지 못했습니다. (${message})`, buildPreviewSubtitle(editorProblemId));
        }
      };

      const saveProblemContent = async () => {
        if (!editorProblemId) {
          setEditorStatus("문항을 먼저 선택하세요.", true);
          return;
        }
        const sections = getEditorSections();
        if (manualEditorSaveBtn) manualEditorSaveBtn.disabled = true;
        if (manualEditorReloadBtn) manualEditorReloadBtn.disabled = true;
        if (manualEditorOpenFolderBtn) manualEditorOpenFolderBtn.disabled = true;
        if (manualEditorPreviewBtn) manualEditorPreviewBtn.disabled = true;
        setEditorStatus("problem.md 저장 중입니다...");

        try {
          const response = await fetch("/api/problem-content", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              id: editorProblemId,
              q: sections.q,
              choices: sections.choices,
              answer: sections.answer,
              solution: sections.solution,
            }),
          });
          const payload = await response.json().catch(() => ({}));
          if (!response.ok) {
            const detail = payload && payload.detail ? payload.detail : `HTTP ${response.status}`;
            throw new Error(detail);
          }

          contentCache.set(editorProblemId, sections);
          if (payload && payload.preview) {
            previewCache.set(editorProblemId, payload.preview);
            renderSavedPreviewPayload(editorProblemId, payload.preview);
          } else {
            previewCache.delete(editorProblemId);
            await loadProblemPreview(editorProblemId);
          }
          setEditorDirty(false);
          setEditorStatus("저장 완료");
        } catch (error) {
          const message = error && error.message ? error.message : "알 수 없는 오류";
          setEditorStatus(`저장 실패: ${message}`, true);
        } finally {
          if (manualEditorSaveBtn) manualEditorSaveBtn.disabled = false;
          if (manualEditorReloadBtn) manualEditorReloadBtn.disabled = false;
          if (manualEditorOpenFolderBtn) manualEditorOpenFolderBtn.disabled = false;
          if (manualEditorPreviewBtn) manualEditorPreviewBtn.disabled = false;
        }
      };

      const applyManualSelectionState = () => {
        if (!manualOrderList) return;
        manualOrderList.querySelectorAll(".manual-order-item").forEach((node) => {
          const itemId = node.dataset.id || "";
          const selected = !!selectedManualOrderId && itemId === selectedManualOrderId;
          node.classList.toggle("selected", selected);
          node.setAttribute("aria-selected", selected ? "true" : "false");
        });
      };

      const selectManualOrderItem = (problemId) => {
        const nextId = problemId || "";
        if (editorDirty && editorProblemId && nextId && editorProblemId !== nextId) {
          const proceed = window.confirm("저장되지 않은 변경사항이 있습니다. 저장하지 않고 다른 문항으로 이동할까요?");
          if (!proceed) return;
        }

        selectedManualOrderId = nextId;
        applyManualSelectionState();
        if (!selectedManualOrderId) {
          setPreviewEmpty(defaultPreviewMessage);
          clearEditorPane();
          return;
        }
        loadProblemContent(selectedManualOrderId);
        loadProblemPreview(selectedManualOrderId);
      };

      const renderManualOrderList = (ids, options = {}) => {
        if (!manualOrderList) return;
        const hadExistingItems = manualOrderList.querySelectorAll(".manual-order-item").length > 0;
        const explicitCheckedIds = Array.isArray(options.checkedIds) ? uniqueIds(options.checkedIds) : null;
        let checkedSet = explicitCheckedIds ? new Set(explicitCheckedIds) : new Set(getManualCheckedIds());
        if (!hadExistingItems && checkedSet.size === 0 && options.defaultChecked !== false) {
          checkedSet = new Set(ids);
        }

        manualOrderList.setAttribute("role", "listbox");
        manualOrderList.innerHTML = "";
        if (selectedManualOrderId && !ids.includes(selectedManualOrderId)) {
          selectedManualOrderId = "";
        }

        if (!ids.length) {
          const empty = document.createElement("li");
          empty.className = "muted";
          empty.textContent = "정렬할 문항 목록이 없습니다. '필터 결과 불러오기'를 눌러주세요.";
          manualOrderList.appendChild(empty);
          syncManualInput([]);
          syncManualSelectedInput([]);
          setPreviewEmpty(defaultPreviewMessage);
          clearEditorPane();
          return;
        }

        let draggingId = "";
        ids.forEach((id, index) => {
          const row = problemMetaById.get(id);
          const examLabel = row
            ? `${row.school} ${row.year} G${row.grade} S${row.semester} ${row.exam}${String(row.subject || "").trim() ? `(${String(row.subject || "").trim()})` : ""} ${row.source_label || ""}`
            : "메타정보 없음";
          const unitLabel = row && row.unit ? displayUnitPath(row.unit) : "";
          const shownId = row ? displayProblemId(row) : id;
          const canEditMeta = !!row;

          const item = document.createElement("li");
          item.className = "manual-order-item";
          item.draggable = true;
          item.dataset.id = id;
          item.tabIndex = 0;
          item.setAttribute("role", "option");
          item.setAttribute("aria-selected", "false");
          item.innerHTML = `
            <input class="manual-order-check" type="checkbox" aria-label="출제 선택" ${checkedSet.has(id) ? "checked" : ""} />
            <span class="manual-order-handle">${index + 1}.</span>
            <span class="manual-order-id">${escapeHtml(shownId)}</span>
            <span class="manual-order-meta">${examLabel}${unitLabel ? ` | ${unitLabel}` : ""}</span>
            ${
              canEditMeta
                ? `<button class="btn manual-order-edit" type="button" data-edit-id="${id}">수정</button>`
                : '<span class="manual-order-meta" style="font-size:11px;">메타수정불가</span>'
            }
          `;

          const checkBox = item.querySelector(".manual-order-check");
          if (checkBox) {
            checkBox.setAttribute("draggable", "false");
            checkBox.addEventListener("click", (event) => {
              event.stopPropagation();
            });
            checkBox.addEventListener("change", () => {
              syncManualSelectionInputs();
            });
          }

          const editButton = item.querySelector(".manual-order-edit");
          if (editButton) {
            editButton.setAttribute("draggable", "false");
            editButton.addEventListener("click", (event) => {
              event.preventDefault();
              event.stopPropagation();
              openMetaEditor(id);
            });
          }

          item.addEventListener("click", () => {
            selectManualOrderItem(id);
          });

          item.addEventListener("keydown", (event) => {
            if (event.key !== "ArrowDown" && event.key !== "ArrowUp" && event.key !== "Enter" && event.key !== " ") {
              return;
            }

            if (event.key === "Enter" || event.key === " ") {
              event.preventDefault();
              selectManualOrderItem(id);
              return;
            }

            const currentIds = getManualListIds();
            const currentIndex = currentIds.indexOf(id);
            if (currentIndex < 0) return;
            const nextIndex = event.key === "ArrowDown"
              ? Math.min(currentIds.length - 1, currentIndex + 1)
              : Math.max(0, currentIndex - 1);
            if (nextIndex === currentIndex) return;

            event.preventDefault();
            const nextId = currentIds[nextIndex];
            selectManualOrderItem(nextId);
            const nextItem = manualOrderList.querySelector(`.manual-order-item[data-id="${nextId}"]`);
            if (nextItem) {
              nextItem.focus();
            }
          });

          item.addEventListener("dragstart", (event) => {
            draggingId = id;
            item.classList.add("dragging");
            if (event.dataTransfer) {
              event.dataTransfer.effectAllowed = "move";
              event.dataTransfer.setData("text/plain", id);
            }
          });

          item.addEventListener("dragend", () => {
            item.classList.remove("dragging");
          });

          item.addEventListener("dragover", (event) => {
            event.preventDefault();
            if (event.dataTransfer) {
              event.dataTransfer.dropEffect = "move";
            }
          });

          item.addEventListener("drop", (event) => {
            event.preventDefault();
            const fromId =
              draggingId || (event.dataTransfer ? event.dataTransfer.getData("text/plain") : "");
            if (!fromId || fromId === id) return;
            const checkedIds = getManualCheckedIds();
            const current = getManualListIds();
            const fromIndex = current.indexOf(fromId);
            const toIndex = current.indexOf(id);
            if (fromIndex < 0 || toIndex < 0) return;
            const [moved] = current.splice(fromIndex, 1);
            current.splice(toIndex, 0, moved);
            renderManualOrderList(current, { checkedIds, defaultChecked: false });
          });

          manualOrderList.appendChild(item);
        });

        applyManualSelectionState();
        syncManualSelectionInputs();
      };

      const collectFilteredProblemIds = () => {
        const selectedDataSourceInput = document.querySelector('input[name="data_source"]:checked');
        const selectedDataSource = selectedDataSourceInput
          ? String(selectedDataSourceInput.value || "").trim().toLowerCase()
          : "official";
        const selectedSchools = new Set(getCheckedValues("schools"));
        const selectedYears = new Set(getCheckedValues("years"));
        const selectedGrades = new Set(getCheckedValues("grades"));
        const selectedSemesters = new Set(getCheckedValues("semesters"));
        const selectedExams = new Set(getCheckedValues("exams"));
        const selectedUnitNodes = getCheckedValues("unit_nodes");
        const selectedLevels = new Set(getCheckedValues("levels"));
        const selectedSourceNos = new Set(getCheckedValues("source_numbers"));

        const selectorIds = uniqueIds(parseIds(selectorIdsInput ? selectorIdsInput.value : ""));
        const patternText = selectorPatternInput ? selectorPatternInput.value.trim() : "";
        const patternRegex = patternText ? globToRegex(patternText) : null;
        const rowMatches = (row) => {
          if (!row) return false;
          const rootKind = String(row.root_kind || "official").trim().toLowerCase() || "official";
          if (selectedDataSource && rootKind !== selectedDataSource) {
            return false;
          }
          if (selectedSchools.size && !selectedSchools.has(row.school)) return false;
          if (selectedYears.size && !selectedYears.has(String(row.year))) return false;
          if (selectedGrades.size && !selectedGrades.has(String(row.grade))) return false;
          if (selectedSemesters.size && !selectedSemesters.has(String(row.semester))) return false;
          if (selectedExams.size && !selectedExams.has(row.exam)) return false;
          if (!unitMatches(String(row.unit || ""), selectedUnitNodes)) return false;
          if (selectedLevels.size && !selectedLevels.has(String(row.level || ""))) return false;
          if (selectedSourceNos.size && !selectedSourceNos.has(String(row.source_label || ""))) return false;
          return true;
        };

        let rows = [];
        if (selectorIds.length) {
          rows = selectorIds
            .map((id) => problemMetaById.get(id))
            .filter((row) => rowMatches(row));
        } else {
          rows = problemMeta.filter((row) => rowMatches(row));
        }

        if (patternRegex) {
          rows = rows.filter((row) => patternCandidates(row).some((token) => patternRegex.test(token)));
        }

        const sortFieldSlots = getSortFieldSlots();
        const primarySortField = sortFieldSlots[0];
        const effectiveSortFields = getEffectiveSortFields();
        const sortOrder = sortOrderInput ? sortOrderInput.value : "asc";
        const desc = sortOrder === "desc";
        if (primarySortField !== "manual" && rows.length > 1) {
          const keyOf = (row, sortField) => {
            const school = String(row.school || "").trim();
            const year = toInt(row.year, 9999);
            const grade = toInt(row.grade, 99);
            const semester = toInt(row.semester, 99);
            const exam = String(row.exam || "").trim();
            const subject = String(row.subject || "").trim();
            const unit = String(row.unit || "").trim();
            const number = toInt(row.number, 999);
            const sourceNo = toInt(row.source_no, 999);
            const sourceKindBaseRank =
              String(row.source_kind || "").trim().toLowerCase() === "subjective" ? 1 : 0;
            // Keep objective block before subjective block even when sort_order is desc.
            const sourceKindRank =
              sortField === "source" && desc ? 1 - sourceKindBaseRank : sourceKindBaseRank;
            // Multi-key sorting: each slot compares only its own dimension.
            // Remaining ties are resolved by the next sort slots and final id.
            if (sortField === "unit") return [unit];
            if (sortField === "school") return [school];
            if (sortField === "year") return [year];
            if (sortField === "source") return [sourceKindRank, sourceNo];
            return [row.id];
          };
          const compareKeys = (ka, kb) => {
            const maxLen = Math.max(ka.length, kb.length);
            for (let i = 0; i < maxLen; i += 1) {
              if (ka[i] < kb[i]) return desc ? 1 : -1;
              if (ka[i] > kb[i]) return desc ? -1 : 1;
            }
            return 0;
          };
          rows.sort((a, b) => {
            for (const field of effectiveSortFields) {
              const result = compareKeys(keyOf(a, field), keyOf(b, field));
              if (result !== 0) return result;
            }
            return compareKeys([a.id], [b.id]);
          });
        }

        return uniqueIds(rows.map((row) => row.id));
      };

      const refreshSortControls = () => {
        if (!sortOrderInput) return;
        const manual = normalizeSortField(sortFieldInput1 ? sortFieldInput1.value : "default", 1) === "manual";
        sortOrderInput.disabled = manual;
        sortOrderInput.title = manual ? "직접 지정 순서에서는 정렬 방향이 적용되지 않습니다." : "";
        [sortFieldInput2, sortFieldInput3].forEach((fieldInput) => {
          if (!fieldInput) return;
          fieldInput.disabled = manual;
          fieldInput.title = manual ? "직접 지정 순서에서는 정렬 기준2/3이 적용되지 않습니다." : "";
        });
      };

      sortFieldInputs.forEach((fieldInput) => {
        fieldInput.addEventListener("change", refreshSortControls);
      });
      refreshSortControls();

      if (loadFilteredOrderBtn) {
        loadFilteredOrderBtn.addEventListener("click", () => {
          const ids = collectFilteredProblemIds();
          renderManualOrderList(ids, { checkedIds: ids, defaultChecked: true });
          refreshSortControls();
        });
      }

      if (clearManualOrderBtn) {
        clearManualOrderBtn.addEventListener("click", () => {
          syncManualInput([]);
          syncManualSelectedInput([]);
          selectedManualOrderId = "";
          renderManualOrderList([]);
        });
      }

      if (manualCheckAllBtn) {
        manualCheckAllBtn.addEventListener("click", () => {
          setAllManualChecks(true);
        });
      }

      if (manualUncheckAllBtn) {
        manualUncheckAllBtn.addEventListener("click", () => {
          setAllManualChecks(false);
        });
      }

      if (renderForm) {
        renderForm.addEventListener("submit", () => {
          syncManualSelectionInputs();
        });
      }

      if (metaUnitL1Input) {
        metaUnitL1Input.addEventListener("change", () => {
          syncUnitSelectors({
            unit_l1: metaUnitL1Input.value,
          });
        });
      }
      if (metaUnitL2Input) {
        metaUnitL2Input.addEventListener("change", () => {
          syncUnitSelectors({
            unit_l1: metaUnitL1Input ? metaUnitL1Input.value : "",
            unit_l2: metaUnitL2Input.value,
          });
        });
      }

      if (metaEditorCancelBtn) {
        metaEditorCancelBtn.addEventListener("click", () => {
          closeMetaEditor();
        });
      }
      if (metaEditorBackdrop) {
        metaEditorBackdrop.addEventListener("click", (event) => {
          if (event.target === metaEditorBackdrop) {
            closeMetaEditor();
          }
        });
      }

      if (metaEditorOpenFolderBtn) {
        metaEditorOpenFolderBtn.addEventListener("click", async () => {
          if (!editingProblemId) {
            setMetaEditorStatus("문항을 먼저 선택하세요.", true);
            return;
          }
          metaEditorOpenFolderBtn.disabled = true;
          setMetaEditorStatus("문항 폴더를 여는 중입니다...");
          try {
            const payload = await openProblemFolderById(editingProblemId);
            setMetaEditorStatus(`문항 폴더 열기 완료: ${payload.path || editingProblemId}`);
          } catch (error) {
            const message = error && error.message ? error.message : "알 수 없는 오류";
            setMetaEditorStatus(`문항 폴더 열기 실패: ${message}`, true);
          } finally {
            metaEditorOpenFolderBtn.disabled = false;
          }
        });
      }

      const removeProblemMetaRow = (problemId) => {
        if (!problemId) return;
        problemMetaById.delete(problemId);
        const idx = problemMeta.findIndex((item) => item.id === problemId);
        if (idx >= 0) {
          problemMeta.splice(idx, 1);
        }
      };

      if (metaEditorDeleteBtn) {
        metaEditorDeleteBtn.addEventListener("click", async () => {
          if (!editingProblemId) return;
          const targetId = editingProblemId;
          const generatedRef = parseGeneratedProblemUiId(targetId);
          const agreed = window.confirm(
            generatedRef
              ? "이 유사문항 후보 폴더(problem.md 포함)가 삭제됩니다. 실행하시겠습니까?"
              : "이 문항이 DB에서 삭제됩니다. 실행하시겠습니까?"
          );
          if (!agreed) return;

          metaEditorDeleteBtn.disabled = true;
          if (metaEditorSaveBtn) metaEditorSaveBtn.disabled = true;
          if (metaEditorOpenFolderBtn) metaEditorOpenFolderBtn.disabled = true;
          setMetaEditorStatus("삭제 중입니다...");

          try {
            const requestUrl = generatedRef ? "/api/similar-delete" : "/api/problem-delete";
            const requestBody = generatedRef
              ? { batch_id: generatedRef.batchId, candidate_id: generatedRef.candidateId }
              : { id: targetId };
            const response = await fetch(requestUrl, {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(requestBody),
            });
            const payload = await response.json().catch(() => ({}));
            if (!response.ok) {
              const detail = payload && payload.detail ? payload.detail : `HTTP ${response.status}`;
              throw new Error(detail);
            }

            removeProblemMetaRow(targetId);
            previewCache.delete(targetId);
            contentCache.delete(targetId);
            if (editorProblemId === targetId) {
              clearEditorPane();
              setPreviewEmpty("삭제된 문항입니다.");
            }

            const orderIds = getManualListIds().filter((id) => id !== targetId);
            const checkedIds = getManualCheckedIds().filter((id) => id !== targetId);
            renderManualOrderList(orderIds, { checkedIds, defaultChecked: false });
            document.dispatchEvent(
              new CustomEvent("problem-meta-row-deleted", {
                detail: {
                  id: targetId,
                  rootKind: generatedRef ? "generated" : "official",
                  batchId: generatedRef ? generatedRef.batchId : "",
                  candidateId: generatedRef ? generatedRef.candidateId : "",
                },
              })
            );
            closeMetaEditor();
          } catch (error) {
            const message = error && error.message ? error.message : "알 수 없는 오류";
            setMetaEditorStatus(`삭제 실패: ${message}`, true);
          } finally {
            metaEditorDeleteBtn.disabled = false;
            if (metaEditorSaveBtn) metaEditorSaveBtn.disabled = false;
            if (metaEditorOpenFolderBtn) metaEditorOpenFolderBtn.disabled = false;
          }
        });
      }

      if (metaEditorSaveBtn) {
        metaEditorSaveBtn.addEventListener("click", async () => {
          if (!editingProblemId) return;
          metaEditorSaveBtn.disabled = true;
          if (metaEditorDeleteBtn) metaEditorDeleteBtn.disabled = true;
          if (metaEditorOpenFolderBtn) metaEditorOpenFolderBtn.disabled = true;
          setMetaEditorStatus("저장 중입니다...");

          const body = {
            id: editingProblemId,
            school: metaSchoolInput ? metaSchoolInput.value : "",
            year: metaYearInput ? metaYearInput.value : "",
            grade: metaGradeInput ? metaGradeInput.value : "",
            semester: metaSemesterInput ? metaSemesterInput.value : "",
            exam: metaExamInput ? metaExamInput.value : "",
            subject: metaSubjectInput ? metaSubjectInput.value : "",
            source_question_no: metaSourceNoInput ? metaSourceNoInput.value : "",
            source_question_kind: metaSourceKindInput ? metaSourceKindInput.value : "",
            source_question_label: metaSourceLabelInput ? metaSourceLabelInput.value : "",
            type: metaTypeInput ? metaTypeInput.value : "",
            level: metaLevelInput ? metaLevelInput.value : "",
            difficulty: metaDifficultyInput ? metaDifficultyInput.value : "",
            unit_l1: metaUnitL1Input ? metaUnitL1Input.value : "",
            unit_l2: metaUnitL2Input ? metaUnitL2Input.value : "",
            unit_l3: metaUnitL3Input ? metaUnitL3Input.value : "",
          };

          if (!SUBJECT_SET.has(String(body.subject || "").trim())) {
            setMetaEditorStatus("subject를 선택하세요.", true);
            metaEditorSaveBtn.disabled = false;
            if (metaEditorDeleteBtn) metaEditorDeleteBtn.disabled = false;
            if (metaEditorOpenFolderBtn) metaEditorOpenFolderBtn.disabled = false;
            return;
          }

          try {
            const response = await fetch("/api/problem-meta", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(body),
            });
            const payload = await response.json().catch(() => ({}));
            if (!response.ok) {
              const detail = payload && payload.detail ? payload.detail : `HTTP ${response.status}`;
              throw new Error(detail);
            }
            const row = payload && payload.row ? payload.row : null;
            if (row && row.id) {
              upsertProblemMetaRow(row);
            }
            previewCache.delete(editingProblemId);
            refreshManualListPreservingState(editingProblemId);
            setMetaEditorStatus("저장 완료");
            setTimeout(() => {
              closeMetaEditor();
            }, 150);
          } catch (error) {
            const message = error && error.message ? error.message : "알 수 없는 오류";
            setMetaEditorStatus(`저장 실패: ${message}`, true);
          } finally {
            metaEditorSaveBtn.disabled = false;
            if (metaEditorDeleteBtn) metaEditorDeleteBtn.disabled = false;
            if (metaEditorOpenFolderBtn) metaEditorOpenFolderBtn.disabled = false;
          }
        });
      }

      [manualEditorQInput, manualEditorChoicesInput, manualEditorAnswerInput, manualEditorSolutionInput]
        .filter(Boolean)
        .forEach((inputEl) => {
          inputEl.addEventListener("input", () => {
            if (!editorProblemId) return;
            setEditorDirty(true);
            setEditorStatus("미저장 변경이 있습니다.");
          });
        });

      if (manualEditorReloadBtn) {
        manualEditorReloadBtn.addEventListener("click", async () => {
          if (!editorProblemId) {
            setEditorStatus("문항을 먼저 선택하세요.", true);
            return;
          }
          await loadProblemContent(editorProblemId, true);
          previewCache.delete(editorProblemId);
          await loadProblemPreview(editorProblemId);
          setEditorStatus("원본 다시불러오기 완료");
        });
      }

      if (manualEditorOpenFolderBtn) {
        manualEditorOpenFolderBtn.addEventListener("click", async () => {
          if (!editorProblemId) {
            setEditorStatus("문항을 먼저 선택하세요.", true);
            return;
          }
          manualEditorOpenFolderBtn.disabled = true;
          setEditorStatus("문항 폴더를 여는 중입니다...");
          try {
            const payload = await openProblemFolderById(editorProblemId);
            setEditorStatus(`문항 폴더 열기 완료: ${payload.path || editorProblemId}`);
          } catch (error) {
            const message = error && error.message ? error.message : "알 수 없는 오류";
            setEditorStatus(`문항 폴더 열기 실패: ${message}`, true);
          } finally {
            manualEditorOpenFolderBtn.disabled = false;
          }
        });
      }

      if (manualEditorPreviewBtn) {
        manualEditorPreviewBtn.addEventListener("click", async () => {
          await renderDraftPreviewFromEditor();
        });
      }

      if (manualEditorSaveBtn) {
        manualEditorSaveBtn.addEventListener("click", async () => {
          await saveProblemContent();
        });
      }

      setPreviewEmpty(defaultPreviewMessage);
      clearEditorPane();
      const initialManualOrderIds = uniqueIds(parseIds(manualOrderIdsInput ? manualOrderIdsInput.value : ""));
      const initialManualSelectedIds = uniqueIds(parseIds(manualSelectedIdsInput ? manualSelectedIdsInput.value : ""));
      const initialCheckedIds = initialManualSelectedIds.length ? initialManualSelectedIds : initialManualOrderIds;
      renderManualOrderList(initialManualOrderIds, { checkedIds: initialCheckedIds, defaultChecked: true });

      const officialProblemMeta = problemMeta.filter(
        (row) => String(row.root_kind || "official").trim().toLowerCase() !== "generated"
      );
      window.mathKichulAdmin = window.mathKichulAdmin || {};
      window.mathKichulAdmin.problemMeta = officialProblemMeta.slice();
      window.mathKichulAdmin.openMetaEditor = (problemId) => {
        openMetaEditor(problemId);
      };
      window.mathKichulAdmin.buildGeneratedProblemId = (batchId, candidateId) => {
        const batchToken = String(batchId || "").trim();
        const candidateToken = String(candidateId || "").trim();
        if (!batchToken || !candidateToken) return "";
        return `GEN::${batchToken}::${candidateToken}`;
      };
      window.mathKichulAdmin.getDistinctMetaValues = () => {
        const distinct = (key) =>
          Array.from(new Set(officialProblemMeta.map((row) => String(row[key] || "").trim()).filter(Boolean))).sort();
        return {
          schools: distinct("school"),
          years: distinct("year"),
          grades: distinct("grade"),
          semesters: distinct("semester"),
          exams: distinct("exam"),
          subjects: distinct("subject"),
        };
      };
      window.mathKichulAdmin.filterProblemMeta = (criteria = {}) => {
        const school = String(criteria.school || "").trim();
        const year = String(criteria.year || "").trim();
        const grade = String(criteria.grade || "").trim();
        const semester = String(criteria.semester || "").trim();
        const exam = String(criteria.exam || "").trim();
        const subject = String(criteria.subject || "").trim();
        const pattern = String(criteria.pattern || "").trim();
        const unitKeyword = String(criteria.unit_keyword || "").trim().toLowerCase();
        const patternRegex = pattern ? globToRegex(pattern) : null;

        const rows = officialProblemMeta.filter((row) => {
          if (school && String(row.school || "").trim() !== school) return false;
          if (year && String(row.year || "").trim() !== year) return false;
          if (grade && String(row.grade || "").trim() !== grade) return false;
          if (semester && String(row.semester || "").trim() !== semester) return false;
          if (exam && String(row.exam || "").trim() !== exam) return false;
          if (subject && String(row.subject || "").trim() !== subject) return false;
          if (unitKeyword && !String(row.unit || "").toLowerCase().includes(unitKeyword)) return false;
          if (patternRegex && !patternCandidates(row).some((token) => patternRegex.test(token))) return false;
          return true;
        });
        rows.sort((a, b) => String(a.id || "").localeCompare(String(b.id || "")));
        return rows.map((row) => ({ ...row }));
      };
      window.mathKichulAdmin.getSeedProblemIds = () => {
        const officialOnly = (ids) =>
          ids.filter((id) => {
            const row = problemMetaById.get(id);
            return String((row && row.root_kind) || "official").trim().toLowerCase() !== "generated";
          });
        const checkedIds = getManualCheckedIds();
        if (checkedIds.length) return officialOnly(checkedIds);
        const manualIds = getManualListIds();
        if (manualIds.length) return officialOnly(manualIds);
        return officialOnly(collectFilteredProblemIds());
      };

    })();
