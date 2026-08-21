I’m reading the core plugin flow first: scanner, plugin entrypoint, model tool manager, and one concrete tool (`Contact`) so the architecture summary is tied to the actual control path rather than guesses.

I have the top-level flow. Next I’m reading the base tool abstractions and the lower half of the scanner, because that’s where the XML-to-GUI and GUI-to-XML contracts are actually defined.

I’ve got the data model and scanner pieces. I’m pulling the tool invocation and XML rewrite path next, because that determines how far this design can scale to full CC3D coverage.

The XML rewrite path is in place. I’m checking the rest of the editor integration plus the screenshots you attached so the summary covers both the code structure and the user-facing workflow.

The screenshots line up with the code path: cursor-sensitive context menu on the XML side, then a tool-specific dialog backed by parsed module data. I’m reading the base dialog lifecycle and one more dependency-aware tool so the improvement recommendations are specific.

I have enough context for the architecture review. I’m pulling exact line references for the main risks so the recommendations map cleanly back to the code.

I’ve got the failure points and the core patterns. I’m pulling one tool dialog and one parse-data class with line numbers so the final summary can show the intended extensibility model, not just the current gaps.

**Findings**

- High: block detection and rewrite are text-based and brittle, which will make broad CC3D coverage unreliable. The plugin identifies modules by normalizing line text and matching regexes against raw XML strings in [PluginCCDGUIDesign.py](/Users/m/src/conda-build-repos/cc3d-twedit5/cc3d/twedit5/Plugins/PluginCCDGUIDesign.py:625) and [CC3DMLScannerTools.py](/Users/m/src/conda-build-repos/cc3d-twedit5/cc3d/twedit5/Plugins/CC3DGUIDesign/CC3DMLScannerTools.py:15). That works for simple `<Plugin Name="...">` blocks, but it is fragile around formatting variation, nested content, repeated elements, comments, and future plugin-specific XML shapes.
- High: the tool contract is split across too many mutable representations, and some tools are already partially diverged. `CC3DModelToolBase` carries `_sim_dicts`, tool-local fields, generated XML, and dialog state at once [CC3DModelToolBase.py](/Users/m/src/conda-build-repos/cc3d-twedit5/cc3d/twedit5/Plugins/CC3DGUIDesign/ModelTools/CC3DModelToolBase.py:38). `ContactTool` still validates against legacy fields like `self.cell_type_names` / `self.contact_matrix` that are not populated in the current `ContactPluginData` path [ContactTool.py](/Users/m/src/conda-build-repos/cc3d-twedit5/cc3d/twedit5/Plugins/CC3DGUIDesign/ModelTools/Contact/ContactTool.py:71). `VolumeTool.validate_dicts()` returns `False` immediately and `update_dicts()` is a no-op [VolumeTool.py](/Users/m/src/conda-build-repos/cc3d-twedit5/cc3d/twedit5/Plugins/CC3DGUIDesign/ModelTools/Volume/VolumeTool.py:84). That is a scaling problem, not just cleanup.

- Medium: discovery is convention-based and import-driven instead of schema-driven. `ModelToolsManager` recursively imports every `*Tool.py`, mutates `sys.path`, and extracts header variables dynamically [ModelToolsManager.py](/Users/m/src/conda-build-repos/cc3d-twedit5/cc3d/twedit5/Plugins/CC3DGUIDesign/ModelTools/ModelToolsManager.py:63). That makes tools easy to add by hand, but hard to validate, test, or reason about when you want complete plugin coverage.

- Medium: the docked module list is hard-coded and disconnected from the actual registry. [cc3d_modules_model.py](/Users/m/src/conda-build-repos/cc3d-twedit5/cc3d/twedit5/Plugins/CC3DGUIDesign/helpers/cc3d_modules_model.py:11) contains a static table with only a few plugins and even duplicates `DiffusionSolverFE`. That means the UI cannot become “support all CC3D plugins” without manual edits in multiple places.

- Medium: initialization failure handling is too permissive. `CC3DGUIDesign.__init__` catches all exceptions and keeps the plugin object alive [PluginCCDGUIDesign.py](/Users/m/src/conda-build-repos/cc3d-twedit5/cc3d/twedit5/Plugins/PluginCCDGUIDesign.py:109), but later code assumes a valid `model_tools_manager`, active tools, and context menu state. That produces partial activation and secondary crashes instead of one clean failure.

**Architecture**

The design is conceptually solid. It is a three-layer plugin:

- Editor integration in [PluginCCDGUIDesign.py](/Users/m/src/conda-build-repos/cc3d-twedit5/cc3d/twedit5/Plugins/PluginCCDGUIDesign.py:127). This layer tracks the active XML editor, detects the module under the cursor, builds the context menu you showed in the screenshot, launches the appropriate tool dialog, and writes XML back into the document.

- Scanner/recognizer in [CC3DMLCodeScanner.py](/Users/m/src/conda-build-repos/cc3d-twedit5/cc3d/twedit5/Plugins/CC3DGUIDesign/CC3DMLCodeScanner.py:18) and [CC3DMLScannerTools.py](/Users/m/src/conda-build-repos/cc3d-twedit5/cc3d/twedit5/Plugins/CC3DGUIDesign/CC3DMLScannerTools.py:154). This layer parses the XML text into coarse `ScannedBlock` regions, marks recognized vs unrecognized blocks, checks requisites, and enables cursor-sensitive detection.

- Per-module tools under `ModelTools`. Each supported CC3D construct is implemented as:
  - a `*Tool.py` wrapper with metadata, dependencies, XML entrypoint, and dialog launch
  - an `*PluginData` parser/generator data model
  - a Qt dialog widget and `.ui` file
`Contact` is the clearest example:
- [ContactTool.py](/Users/m/src/conda-build-repos/cc3d-twedit5/cc3d/twedit5/Plugins/CC3DGUIDesign/ModelTools/Contact/ContactTool.py:39) declares that it edits `<Plugin Name="Contact">`, depends on `CellType`, and delegates actual XML parsing/generation to `ContactPluginData`.
- [ContactPluginData.py](/Users/m/src/conda-build-repos/cc3d-twedit5/cc3d/twedit5/Plugins/CC3DGUIDesign/ModelTools/Contact/ContactPluginData.py:12) parses `Energy` entries and `NeighborOrder`, stores them in a generic `ModuleData` matrix, and can regenerate the XML.
- [contactdlg.py](/Users/m/src/conda-build-repos/cc3d-twedit5/cc3d/twedit5/Plugins/CC3DGUIDesign/ModelTools/Contact/contactdlg.py:14) updates the parsed contact matrix from dependent `CellType` data before drawing the table, which is why the GUI can stay aligned with current cell types.

That pattern is the right one. The core idea is: cursor selects module, scanner identifies block, tool parses XML to structured data, dialog edits the structured data, tool regenerates XML.

**What To Improve**

- Make the registry explicit. Each tool should register a typed descriptor: XML selector, CC3D category, dependencies, parser class, dialog class, and coverage status. Stop inferring capability from filename and ad hoc header globals.

- Collapse the state model around `XMLParseData`. Right now the real source of truth should be the parse-data classes like `ContactPluginData`; the older `_sim_dicts` and tool-local mirror fields should either be removed or made purely derived. That will reduce drift and make adding new plugins much faster.

- Replace line-based rewrite with structured block replacement. The scanner already identifies block ranges; the next step is to make replacement operate on parsed block spans, not regex matches against normalized strings. That is the main architectural change needed for reliable coverage.

- Separate “parser/generator coverage” from “GUI coverage”. Many CC3D plugins can be supported in phases:
  1. recognize and validate XML
  2. parse and regenerate losslessly
  3. expose a GUI editor
  4. support dependency-aware editing

- Generate the dock UI from the registry, not from [cc3d_modules_model.py](/Users/m/src/conda-build-repos/cc3d-twedit5/cc3d/twedit5/Plugins/CC3DGUIDesign/helpers/cc3d_modules_model.py:11). Then unsupported plugins can still appear as recognized but “read-only” or “no GUI yet”.

- Add golden tests per plugin type. For each plugin XML snippet: parse -> open data model -> generate -> compare normalized XML. That is the only practical way to scale to full CC3D coverage without regressions.

- Add dependency contract tests. `Contact`, `Volume`, and similar tools depend on `CellType`; those relationships should be verified automatically with fixture XML files.

My recommendation is to treat `XMLParseData` plus a typed tool registry as the long-term architecture, and demote the current `sim_dicts` workflow to legacy compatibility. That gives you a clean path to cover all CC3D plugins without rewriting the entire Twedit integration layer.