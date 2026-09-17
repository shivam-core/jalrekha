# JALREKHA — complete Codex build prompt

**Owner:** Shivam Kore (`shivam-core`)  
**Team:** Team Advantage  
**Repository:** https://github.com/shivam-core/jalrekha  
**Build environment:** local Codex, authenticated with the owner's existing ChatGPT account  
**Deployment:** Vercel Hobby; GitHub stores source and authentic commit history  
**Target:** a working, polished, single-corridor hackathon prototype in approximately four focused hours, subject to the actual submission deadline, authentication, data availability, and usage limits.

## How to use this document

Open the local `jalrekha` repository in Codex, attach this Markdown file, and send:

> Read this entire document and execute its build instructions. Implement, test, commit, push, and deploy JALREKHA to the specified GitHub repository and Vercel. Begin by inspecting the repository and checking the time, authentication, and real-data feasibility. Continue through the milestones without asking me to approve routine implementation decisions. Report actual blockers precisely. Do not stop after writing a plan.

Alternatively, paste this document's full contents into Codex. It is self-contained; the earlier conversation and Claude PDFs are not required. The Claude guide is optional supporting material, not an instruction to preserve its bugs or outdated deployment choices.

Before starting, sign into GitHub and Vercel through their normal browser/device authentication flows when prompted. Grant Codex access to this project folder and the terminal through its actual settings. This document cannot grant operating-system permissions or bypass platform approval controls.

No passwords, access tokens, or session cookies belong in this document or repository. If a password was previously posted in a chat, rotate it through the provider's own account settings. Do not copy chat credentials into commands or files.

---

## 1. Your task and authorised scope

You are the implementation engineer for JALREKHA. Build the application, not another proposal. You are authorised to edit project files, install project-local dependencies, run the terminal and tests, prepare public geographic data, make meaningful commits, push project changes to `shivam-core/jalrekha`, and deploy the verified prototype to the owner's Vercel Hobby project. Use the existing authenticated account sessions and respect all platform permissions.

Do not purchase services, enable paid upgrades, use a separately billed LLM API, delete unrelated files, overwrite teammates' work, rewrite published history, force-push, or expose secrets. Do not change global Git identity or account settings. Do not send messages to organisers or submit the competition entry on the user's behalf. Prepare the submission materials and links for the user.

Make routine design and implementation decisions yourself. Ask only for something genuinely blocking, such as browser login, an unknown Git author identity, a protected branch that prevents the authorised push, or conflicting existing work. Continue independent local work while an external connection is blocked. Do not repeatedly ask for permissions already provided here; never circumvent actual permission restrictions.

Use one implementation agent by default. Additional agents are not required. Keep context and usage economical: inspect relevant files, execute focused checks, and avoid broad repeated searches or endless cosmetic passes.

### Deadline and provenance

The supplied Hack2Ignite rulebook states a development window from **16 September 2026, 09:00 IST to 18 September 2026, 09:00 IST**. The deadline is **2026-09-18T03:30:00Z**. The minute shown on Unstop does not extend that rulebook deadline.

At startup, report current time in `Asia/Kolkata`, actual time remaining, and the feasible scope. If the organiser has supplied a newer deadline, use that verified instruction. If the deadline is already past, say so immediately and do not represent subsequent development as competition-window work; ask whether to continue as a post-deadline project. Never alter timestamps or backdate commits. If less than four hours remain, compress optional work and reserve the final 30–45 minutes for submission preparation. Stop substantial competition development by the applicable deadline.

AI use is permitted by the supplied rulebook and must be disclosed in the README or PPT. Maintain genuine incremental Git history. The supplied instructions require a PPT using the organisers' template and the repository link; deployment and a demo video are optional but desirable.

## 2. Product definition and exact scope

**Name:** JALREKHA / जलरेखा  
**Tagline:** When routes change, plans should too.  
**Mission:** Help planners explore how assumed flood conditions and road closures affect access to limited shelter capacity.  
**Primary user:** a disaster-planning coordinator conducting a scenario exercise.  
**Primary problem statement:** AI for Good, **AI-05 — Develop an intelligent system for optimizing resource allocation in healthcare, education, or disaster management.**

The prototype is a **what-if planning simulator**, using terrain analysis, graph algorithms, and constrained allocation. Do not claim a trained flood-prediction model, operationally safe navigation, official shelter status, validated population exposure, or lives saved.

Build one small Pune Mula–Mutha corridor. Start with a study area approximately 5 km across, centred near the confluence around longitude 73.87, latitude 18.53. Confirm the actual river alignment on downloaded data before fixing the bounds. The centre and bounds are proposed engineering inputs, not validated hazard boundaries. An initial working box may be `west=73.845, south=18.505, east=73.895, north=18.550`; adjust once if data coverage or connectivity requires it, documenting why.

Use approximately six explicitly defined origin/assembly points and four to six candidate shelter locations. Population and capacities are editable scenario assumptions. Include one additional candidate shelter initially closed, so opening it produces a meaningful intervention when the graph permits it.

### Required end-to-end experience

1. Open the public URL and immediately see a usable map and an example scenario.
2. Adjust a water-level scenario from 0 to 8 m, normally in 0.5 m steps. This is a relative HAND scenario parameter, not a forecast or universal river-gauge reading.
3. See approximate inundation, affected road segments, candidate shelter status, and allocation results change together.
4. Manually close a road segment and recompute routes and allocations.
5. Open the additional candidate shelter or change an assumed capacity and recompute.
6. Compare a feasible nearest-available-shelter baseline against the capacity-constrained optimiser.
7. Select an origin or shelter to inspect routes, assumptions, travel-time estimates, and allocation explanations.
8. Export the current scenario and allocation as JSON and CSV.
9. Reset reliably to the original demonstration scenario.

All displayed statistics must come from the engine. Empty and infeasible outcomes are valid results. Do not fabricate an improvement to make the demo attractive.

### Keep out of the first release

No chatbot, authentication system for end users, database, payments, SMS alerts, live GPS, training jobs, whole-India city selector, real-time emergency instructions, elaborate landing-page funnel, or mandatory 3D terrain. These are outside the deadline scope. Avoid adding another hosting provider.

## 3. Architecture: compatible from the first deployment

Use the architecture below unless inspection reveals an already-working equivalent worth preserving. Do not rewrite an existing functioning application solely to match a directory preference.

| Layer | Chosen implementation | Where it runs |
|---|---|---|
| Interface | HTML, CSS, modular JavaScript; MapLibre GL JS | Browser; static assets on Vercel |
| HTTP API | FastAPI with Pydantic validation | Vercel Python Function |
| Routing and allocation | NetworkX; deterministic Python modules | Same function, using compact prepared data |
| Flood overlay | Precomputed PNGs and extent metadata | Vercel static assets |
| Geographic preparation | Python: Rasterio, PySheds, OSMnx, Shapely, PyProj as needed | Local machine only |
| State | Request payload plus browser state/local storage | Browser; no server persistence |
| Source and audit trail | GitHub repository | GitHub |

There is no Next.js/Node server and no Docker service in this first release. A static frontend can still have excellent design and interactive behaviour. Keep frontend and API on the same Vercel origin, with relative `/api/...` requests. This avoids a second service, CORS configuration, and separate deployment lifecycles.

The Python function loads only small prepared JSON tables. Do not import Rasterio, GDAL, OSMnx, SciPy, GeoPandas, or PySheds into the runtime import graph. Do not download geographic data or compute HAND in function startup or API requests. Do not write to the deployment filesystem or rely on a persistent process/cache.

Use Python **3.12** for the deployment runtime and preferably local preparation too. Confirm availability in the actual environment. The supplied guide's Docker Python 3.11 is not the target runtime. Pin compatible versions after an import smoke test; record the versions actually installed. Do not blindly install the newest NumPy with an older hydrology library.

Runtime dependencies should be small: FastAPI, Pydantic, NetworkX, and local-development Uvicorn. Use the standard library for JSON and CSV. Add NumPy/Pillow at runtime only if genuinely needed; precomputed overlays normally remove that need. Heavy preparation and test dependencies belong in separate requirement files.

### Repository layout

Use these paths as the contract; document any justified changes:

```text
app.py
pyproject.toml
.python-version
requirements.txt
requirements-prep.txt
requirements-dev.txt
vercel.json
.gitignore
.vercelignore
README.md
LICENSE / THIRD_PARTY_NOTICES.md, as appropriate to ownership
config/pune.json
engine/__init__.py
engine/schemas.py
engine/load.py
engine/roads.py
engine/routes.py
engine/allocate.py
engine/scenario.py
scripts/prepare_dem.py
scripts/prepare_roads.py
scripts/prepare_scenarios.py
scripts/validate_data.py
scripts/export_fallbacks.py
scripts/check_deployment.py
scripts/dev_server.py
data/processed/network.json
data/processed/locations.json
data/processed/hazards.json
data/processed/manifest.json
public/index.html
public/styles.css
public/js/main.js
public/js/api.js
public/js/map.js
public/js/state.js
public/js/panels.js
public/vendor/...
public/assets/mark.svg
public/data/map.geojson
public/data/manifest.json
public/data/scenarios/...
public/data/water/...
tests/test_routes.py
tests/test_allocation.py
tests/test_api.py
tests/test_data.py
tests/browser/...
docs/BUILD_SPEC.md
docs/STATUS.md
docs/method.md
docs/limitations.md
docs/data-sources.md
docs/deployment.md
docs/validation.md
docs/ai-disclosure.md
docs/demo-script.md
docs/submission.md
docs/presentation-content.md
```

Raw downloads, caches, environments, browser profiles, credentials, large images, and notebook outputs must be ignored. Use `data/raw/` and `data/cache/` locally, excluded from Git and Vercel. Keep the repository lightweight. Aim for compact prepared runtime data below roughly 15 MB and public demonstration assets below roughly 30 MB; these are project targets, not provider limits.

Save this specification or its implementation-relevant content in `docs/BUILD_SPEC.md`. Maintain `docs/STATUS.md` with current milestone, real blockers, commands that worked, and next action so work survives context resets.

## 4. Startup, access, and repository handling

The remote repository was reachable when this handoff was prepared; `main` existed at commit `458854c07b713944400eb039f91d7091b235a969`. This is an observation, not a commit to reset to. Its files were not audited for this handoff. Inspect its current state before editing.

1. Inspect current directory, applicable `AGENTS.md` instructions, repository status, remotes, branches, and existing files. Never assume the repo is empty.
2. If no checkout exists, clone `https://github.com/shivam-core/jalrekha.git` into an appropriate project directory. If a checkout exists, use it; do not create conflicting copies.
3. Verify the remote points to `shivam-core/jalrekha`. Check `git status --short`, `git branch --show-current`, `git remote -v`, and recent commits. Do not expose credential-bearing URLs.
4. Check `gh auth status` if GitHub CLI is present. If login is needed, use `gh auth login --hostname github.com --git-protocol https --web` and let the user complete the provider flow. Never use the password from chat, request a password in the terminal, or print tokens.
5. Use the authenticated user's Git identity. Inspect repository-local identity and resolve a missing author email through the user's verified GitHub identity or one brief clarification. Do not invent an email or impersonate teammates.
6. Fetch safely. On a clean `main`, fast-forward from `origin/main`. If there are local changes, preserve them and inspect conflicts before proceeding. Use a new project branch when necessary to isolate existing work; do not silently discard it.
7. Check Python, Git, Node/npm for tooling, and Vercel CLI. Install dependencies into a virtual environment. A project-local CLI installation or `npx` is preferable to unapproved system-wide changes.
8. Check Vercel login with `vercel whoami` or its installed equivalent. If needed, use `vercel login` and browser authentication. Choose the owner's personal Hobby scope. If that scope is not identifiable, ask only for that selection.

Run ordinary shell commands without `sudo`. Do not put credentials in Git remotes, `.env` committed files, command arguments, README examples, screenshots, or logs. `.env.example` may contain variable names and harmless placeholders only.

## 5. First milestone: deploy a vertical slice early

Within the first 30–40 minutes, make one narrow path work locally and in a Vercel preview: homepage → `/api/health` → a tiny scenario fixture → visible result. Mark this fixture as synthetic and replace it with real geography later. This early deployment is a compatibility check, not a claim that the application is complete.

### Exact deployment entrypoint

Define the FastAPI instance as `app` in root `app.py`. Use `/api/health`, `/api/meta`, and `/api/scenario` for API routes. Resolve data paths with `Path(__file__).resolve().parent`; never depend on a developer-specific working directory.

Place frontend files under root `public/`. Vercel serves them as static assets. Do not mount the whole `public/` folder over `/` in the deployed app. A root `GET /` may redirect to `/index.html`, while static assets use `/styles.css`, `/js/main.js`, and `/data/...` URLs. Verify the deployed root URL, not just the HTML file URL.

Prefer this minimal configuration, validating it against the current Vercel CLI before committing:

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "framework": "fastapi",
  "functions": {
    "app.py": {
      "maxDuration": 60,
      "excludeFiles": "{data/raw/**,data/cache/**,scripts/**,tests/**,docs/**,.venv/**,.venv-prep/**,**/__pycache__/**,**/*.ipynb}"
    }
  }
}
```

Do not exclude `engine/**` or `data/processed/**`. Do not set an Output Directory to `public` as though the whole project were a static-only build. Do not add a catch-all rewrite that swallows `/api` routes. Use the native FastAPI framework integration; do not combine it with legacy `builds` configurations or an unrelated Node server.

Put `3.12` in `.python-version`. In `pyproject.toml`, declare the project's Python requirement as `>=3.12,<3.13` and use a single consistent runtime dependency source. An initial runtime `requirements.txt` is acceptable; avoid contradictory dependency declarations. Keep preparation dependencies separate and never install them in the Vercel build command.

For local development, use `vercel dev` to exercise the same static/API routing. If temporarily unavailable, provide a development-only runner that combines Uvicorn and explicit static serving without altering the production entrypoint contract. Never declare local route success as proof that Vercel works.

Deploy through the authenticated CLI or import the GitHub repository in Vercel. Link an existing `jalrekha` project if appropriate; otherwise create one in the owner's personal Hobby scope. If the globally unique project name is unavailable, use `jalrekha-shivam-core` and record the returned URL. Do not invent the final deployment URL.

## 6. Real-data preparation and the feasibility gate

### Data sources and provenance

- Elevation: publicly accessible Copernicus GLO-30 Cloud Optimized GeoTIFFs; select only relevant windows. Validate current tile URLs before coding against an assumed naming pattern.
- Roads and waterways: OpenStreetMap, obtained through OSMnx/Overpass with a small bounding box, local cache, bounded timeout and retries.
- Candidate shelters: selected OSM buildings or manually specified locations identified on real geography. They are candidate sites, not verified designated shelters.
- Origins: six assembly-point locations on verified graph nodes; populations are scenario inputs.
- Basemap: a permitted, attributed tile/style source verified at build time. If a provider requires credentials or payment, use a plain map style displaying the locally prepared roads, waterway and locations. Do not bypass access restrictions.

For every source record source URL, retrieval timestamp, bounds, CRS, licensing/attribution, preprocessing, and whether the field is observed, derived, or assumed. Preserve OSM attribution and data licence obligations separately from the team's code licence. Do not label third-party geographic data MIT merely because the application code is MIT.

### Feasibility gate

In the first 60–90 minutes, obtain and validate:

1. A real cropped elevation raster with sensible bounds and valid cells.
2. A real road graph aligned with that raster.
3. A HAND-derived overlay at two levels that aligns with the river corridor.
4. One graph path that changes or becomes unavailable after a clearly defined closure.

Network retries must be bounded. If Overpass fails, use a lawful cached/public extract with recorded provenance or reduce the box once. If the full hydrology stack is blocked, first deliver the honest real-road closure/shelter-allocation mode and show flood estimation as unavailable. Synthetic fixtures may support tests or a labelled demo mode, but must never masquerade as Pune flood results. Report a failed gate and narrow JALREKHA's scope; do not silently switch products or spend hours trying identical failing commands.

### Geographic processing

Read a buffered area for hydrology and crop the final display afterward. A small buffer reduces immediate boundary artefacts but does not represent the whole upstream basin; document the limitation. Avoid processing whole 1-degree tiles in memory on an 8 GB laptop. Inspect raster dimensions, nodata, bounds, and CRS before allocating large arrays. Process one crop at a time.

Use an appropriate projected metric CRS for operations that require metres; Pune lies in UTM zone 43N (`EPSG:32643`). Verify transforms and raster alignment. Export GeoJSON in WGS84 longitude/latitude. Never mix `[lat, lon]` and `[lon, lat]`.

The preparation pipeline should perform pit/depression treatment, flat resolution, flow direction, accumulation, drainage-mask selection, and HAND computation using compatible library APIs. Capture the stream threshold and any river-mask adjustment in the manifest. Visually inspect the output, including a cross-check against the river geometry. Do not fill extensive missing terrain with invented elevation. Keep nodata explicitly unknown; do not turn invalid HAND cells into confident “never floods” results.

PySheds compatibility must be tested on the actual installed NumPy version. Prefer a supported pin over a global monkey-patch. Any necessary workaround must be documented and narrowly tested. A library importing successfully is not validation of the hydrological output.

Compute levels 0.0, 0.5, …, 8.0 m as a finite scenario set. Export consistent masks, PNG overlays, and edge/shelter/origin hazard statuses for each. At h=0, show the permanent river separately; avoid a spurious full emergency state caused solely by zero-valued channel cells.

PNG overlays must have correct georeferencing. If the source uses a projected CRS, warp to an appropriate display grid before assigning MapLibre image coordinates. Check top-left, top-right, bottom-right, bottom-left order. Do not make an image “fit” by guessing coordinate order.

## 7. Roads, origins and shelter semantics

Use a drivable road network for this version and label travel times as vehicle-network scenario estimates. Preserve one-way directions and parallel edges. Store stable edge IDs including the OSM edge key. If simplifying a multigraph, document the rule and retain the selected real edge geometry and travel time.

Sample road geometry along its length against the scenario mask, rather than deciding from junction elevations alone. Validate the sampling interval and use vectorised preprocessing. Bridge and tunnel deck elevations are not established by a coarse surface raster: identify those edges, show uncertainty, and allow explicit scenario closure. Do not automatically assert that a bridge is flooded merely because water lies beneath it. The UI must distinguish estimated road impacts from user-imposed closures.

Route geometry must follow the actual selected graph edges. Do not draw straight lines between junctions and imply these are the road geometry. Do not count both directions of the same segment as two distinct physical roads without explaining the metric. Prefer the explicit metric label “Unavailable directed links” if counting graph edges.

Origins represent people assumed to be already at the chosen assembly node. That assumption excludes the journey from homes to that point. If the assembly point is estimated inundated, lacks valid terrain, or has no usable outgoing path, report the limitation. Never snap people across water to the next dry node and call them evacuated.

Distinguish:

- assembly point unavailable/unknown;
- no route to any open, usable candidate shelter;
- reachable candidate shelters but insufficient capacity;
- allocated in the scenario.

Do not label every isolated node a “helicopter zone”; the model cannot prescribe the required rescue mode.

Candidate shelter records contain explicit source and assumption fields. Only use sites with a graph connection and appropriate scenario status. A flooded/closed candidate contributes zero capacity. Capacity can be zero without causing division-by-zero. Never show a school or hospital as officially available without confirmation.

For this time-limited version, keep each origin's assumed population fixed across water-level changes. Thus the app compares allocation of the same scenario population under changing accessibility. Do not label it a census-based estimate of “people at risk.” Use “Scenario population” and “People allocated.” More complex spatial exposure estimation is deferred.

## 8. Optimisation and comparison

The optimisation objective is lexicographic:

1. Maximise the number of people assigned to reachable, usable shelter capacity.
2. Among those solutions, minimise total assumed travel time, measured in person-seconds.

Implement this with a source → origin → shelter → sink flow network. Use integer capacities and integer travel-time costs. Compute maximum feasible flow first, then a minimum-cost flow constrained to that amount, or use the appropriate verified max-flow/min-cost routine. Avoid an arbitrary overflow penalty whose adequacy is unproven.

Origin→shelter arcs exist only when a path exists within the configured scenario travel-time ceiling, initially 45 minutes. Evaluate all candidate shelters in this small prototype, not just an arbitrary nearest-eight truncation. Use consistent directed graph distances and non-negative edge weights. Keep shelter nodes distinct even if two sites snap to the same road node.

Allocation may split a population group across shelters; disclose that the model counts individuals and does not preserve family groups or model vehicle capacity/congestion. Do not claim these features.

The baseline is deterministic **nearest-available-shelter allocation**: process origins in a documented stable order, assign to the nearest feasible shelter with remaining capacity, then continue until assigned or capacity exhausted. Both baseline and optimiser use identical roads, closed links, population, capacities, and travel cutoff. A nearest-shelter plan that ignores capacity may be a labelled explanatory illustration, but it is not the benchmark for claiming superiority.

Compute and display allocation differences and travel time from actual outputs. If optimal allocation assigns more people, its total travel cost may be higher because it transports more people; explain that comparison. Only compare cost optimality at equal allocated population. Never claim an improvement when there is a tie.

Explanations should be deterministic, grounded in constraints, and short: “Nearest shelter full; assigned 40 people to Candidate C via the remaining route.” Avoid asserting a specific binding cause unless verified from the result; a safe generic explanation is “Chosen by the capacity-constrained plan; route and receiving capacity are feasible.” No LLM is required.

## 9. Shared data and API contract

Define Pydantic models and document matching JavaScript structures before implementing UI integrations. IDs should be strings to avoid JavaScript precision issues with OSM identifiers. Coordinates are `[longitude, latitude]`; travel times are seconds internally; displayed minutes are rounded only in the UI.

Every response includes `schema_version`, `dataset_version`, `scenario_id`, the exact applied input, and assumptions. Use a content-derived dataset version. Never mix old overlays with new graph results.

### Prepared inputs

- `network.json`: nodes and directed edges with stable IDs, coordinates, geometry, and travel seconds.
- `locations.json`: origins with assembly node/population, candidate shelters with node/capacity/default-open status, and sources/assumptions.
- `hazards.json`: per-level unusable/unknown road IDs, origin and shelter statuses, overlay URL, and display bounds.
- `manifest.json`: bounding box, CRS, levels, data version, retrieval dates, licences, algorithm settings, and known limitations.

### Endpoints

| Endpoint | Behaviour |
|---|---|
| `GET /api/health` | Service/version readiness; no secrets or machine paths |
| `GET /api/meta` | Valid bounds, levels, limits, data version, candidate IDs, provenance summary |
| `GET /api/scenario?h=2.5` | Default scenario at one supported level |
| `POST /api/scenario` | Compute an edited scenario with validated closures/capacities/open states |

Example POST request; these are illustrative IDs to replace with actual prepared IDs:

```json
{
  "level_m": 2.5,
  "closed_edge_ids": ["edge-17"],
  "shelter_overrides": {
    "shelter-4": {"open": true, "capacity": 200}
  }
}
```

Reject unknown IDs, negative capacities, excessive capacities, NaN/infinity, malformed numbers, oversized payloads, and unsupported levels. Validate level via integer decimetres to avoid floating-point membership errors. Return helpful 4xx errors; never round a requested level to a different one silently. Cap input collections to the prepared dataset and aggregate population/capacity to conservative documented limits.

Response shape must include:

```text
schema_version, dataset_version, scenario_id
input: level_m, closed_edge_ids, shelter_overrides
hazard: overlay_url, image_coordinates, unavailable_edge_ids, unknown_edge_ids
origins: id, assumed_population, status, allocated, unmet
shelters: id, open, usable, capacity, allocated, remaining
allocations: origin_id, shelter_id, people, travel_seconds, edge_ids, geometry
totals: population, allocated, isolated, capacity_unserved, unknown_or_unavailable_origin
baseline: allocations and matching totals
comparison: actual deltas and interpretation
assumptions: short product-readable statements
```

Categories must be disjoint: `population = allocated + isolated + capacity_unserved + unknown_or_unavailable_origin`. Define “isolated” precisely as no feasible path under the current scenario/cutoff. Keep population bookkeeping true in every edge case.

Return only JSON-serialisable native types, not NumPy scalars/NaN. Keep runtime data read-only. Copy scenario graph state before changing it. One user's custom request must not alter another request or the default scenario. Caches, if used, must include the dataset version and every input that changes the result; correctness cannot depend on cache persistence.

Use same-origin requests and relative URLs. No wildcard CORS is needed. Add bounded request duration and small JSON payload limits. Avoid logging request bodies unnecessarily.

## 10. Sleek UI/UX specification

Aim for the discipline of Vercel's product interfaces and the restrained typography/spacing of Anthropic, expressed through a flood-planning identity. Do not reproduce their logos, page layouts, or marketing copy. The app should open directly into the working tool.

### Visual system

| Token | Value / use |
|---|---|
| Page background | `#0B1117`, deep blue-black |
| Surface | `#111B24` |
| Raised surface | `#172530` |
| Borders | `#273A47`, subtle 1 px rules |
| Primary text | `#EDF3F4` |
| Secondary text | `#B5C2CA` |
| Primary action | `#55D6BE`, with dark text |
| Flood overlay | `#3D9CE8`, translucent |
| Allocated / available | `#74C991` |
| Capacity warning | `#F2B766` |
| Closure / unavailable | `#EE7F7F` |

Check actual contrast on all backgrounds; adjust tokens if necessary. Meaning cannot depend solely on colour. Use explicit status labels and icons/line patterns. Create a simple original SVG mark of a waterline and route. Avoid generated bitmap hero imagery.

Use a system sans-serif stack with excellent macOS rendering; a restrained serif can appear only in the brief mission sentence if it looks cohesive. Numeric metrics use tabular figures. Body text should generally be 14–16 px, not tiny dashboard text. Use an 8 px spacing system, 10–12 px corner radii, minimal shadows, and no excessive gradients, glass effects or ornamental motion.

### Desktop layout

- Header, about 64 px: mark + JALREKHA at left; “Pune · Scenario planner”; methods/data button, reset and export controls at right; “Team Advantage” unobtrusively in about/footer.
- Left control panel, roughly 300 px: scenario level, baseline/optimised comparison, road-closure tool, candidate shelter controls and scenario assumptions. Explain metres as a relative scenario parameter.
- Main map: largest region, occupying at least half the desktop width. Water is visually legible; closures are coral/dashed; selected allocation routes are teal or light yellow. Never render every route at full intensity if unreadable; show selected origins clearly.
- Compact summary strip: scenario population, allocated people, unallocated people, usable shelter capacity. Show comparison deltas only after a valid result exists.
- Right inspector or bottom drawer: selected origin/shelter, allocation table, route explanation, current capacity and input provenance.
- Persistent subtle label: “Planning simulation · Assumed population and capacities”. An expandable Methods panel provides the full limitation statement without interrupting ordinary use.

No long landing page before the map. No empty “coming soon” buttons. A control that cannot work must be disabled with a concise reason. Buttons should name their action: “Recalculate plan”, “Open candidate shelter”, “Export scenario”, “Reset”.

### Interaction rules

Store inputs in one state object. Debounce slider requests (~250 ms), use AbortController and/or a monotonically increasing request ID, and discard stale responses. Apply the overlay, routes and metrics as one consistent result. Never show a new water level with old allocation numbers without a clear recalculating state.

While updating, keep the previous map visible with “Updating scenario”; do not replace the entire interface with a spinner. Provide proper empty, error, offline-result and no-route states. Keep a selected shelter or origin selected across updates if it still exists.

Provide keyboard-operable slider, controls, visible focus, labelled inputs, accessible table alternatives, reduced-motion support and at least 44 px touch targets where practical. On mobile, show the map with a collapsible controls sheet and stacked metrics; keep the allocation table scrollable inside its own container. Test at about 1440×900, 1024×768, and 390×844.

Use MapLibre data layers with real prepared geometries and attribution. Version-pin the library. Prefer vendoring its necessary JS/CSS/worker assets with notices so a CDN script outage does not break the tool. Handle unavailable basemap tiles with the local road/waterway layers against a plain background. Full map/offline availability must not be claimed merely because scenario JSON is cached.

3D terrain is a finishing enhancement only after a working 2D view and deployment. Provide a 2D mode. Real computation and clear results have higher priority than animated water.

## 11. Resilience and honest fallback behaviour

Precompute the default scenarios and a small set of demonstrable interventions through the **same engine** used by the API. Export results under deterministic scenario IDs, with the data version and full applied inputs embedded. Pair each result with its correct flood overlay.

If the API is unavailable, offer the exact saved matching scenario when available, labelled “Saved scenario”. Do not return the default scenario while leaving custom shelter or road edits selected. If an edited combination has no saved result, retain the last valid result, explain that this edit requires computation, and offer explicit reset to a saved scenario. A fallback must never pretend to have recomputed.

Do not claim that precomputed results are fake; they are genuine earlier computations when produced by the same engine. Do not claim they are live either. Preload a few demonstration assets after the interface becomes responsive. Avoid a service worker in the first release unless needed and tested; stale versioned data is worse than an explicit network error.

The runtime does not require a weather API. Remove the guide's arbitrary `8 × (discharge − median)/(max − median)` forecast-to-metres mapping. A forecast panel is deferred. This removes an unvalidated scientific claim and a network dependency while preserving the core product.

## 12. Verification that matters

Write focused tests for the high-impact algorithm and integration risks. Do not spend the build window pursuing an arbitrary coverage percentage.

### Algorithm and data tests

1. A directed edge cannot be traversed backwards.
2. Closing an edge removes every returned route that uses that edge.
3. A flooded/closed shelter receives no allocation.
4. No shelter exceeds its capacity; zero capacity is handled.
5. Population conservation holds and unmet categories do not overlap.
6. A disconnected origin is reported with no fabricated path.
7. Increasing capacity cannot reduce the maximum possible allocation when all else is fixed.
8. The optimiser assigns at least as many people as the feasible greedy baseline; when assigned totals tie, its person-second cost is no worse.
9. One custom request does not mutate the next default request.
10. Route edge geometry is continuous, starts/ends at the expected nodes, and matches the graph path.
11. NaN/infinity, unknown IDs, invalid levels and negative capacities produce 4xx responses.
12. API and exported fallback results agree for identical inputs and dataset version.

Use a tiny handcrafted graph with known answers in unit tests. On at least one very small allocation example, cross-check against enumerated feasible assignments or a known optimum so tests do more than mirror the implementation. Real-data validation checks coordinate ranges, raster alignment, positive edge weights, stable IDs, and connections for selected assembly/candidate nodes.

### Integration and visual checks

Run API tests locally, then perform the same essential checks against the deployed preview. Load the actual homepage, move the slider, close a road, edit a capacity, export, reset, and force an API failure to inspect saved-result behaviour. Test rapid slider changes to expose race conditions.

Use browser automation if available; otherwise run the strongest available browser checks and explicitly report anything unverified. Capture screenshots at the target viewport sizes and inspect them. Fix clipped labels, overlapping panels, invisible routes, blocked map controls, missing attribution, broken fonts, and poor contrast. Read console/network errors. Verify both local and deployed static asset paths.

Record actual latency and payload size for several scenarios without claiming production scale. Target a responsive warm interaction (ideally around 1–2 seconds or less for this small case); measure rather than promise. If computation is slow, reduce graph scope/visual payload or use a matching precomputed default, preserving correctness. Keep the function within its configured duration.

## 13. Git: authentic commits throughout the build

Work in `shivam-core/jalrekha`. Commit completed, coherent changes regularly, roughly every 20–40 minutes or at the milestones below. Push after each milestone when authentication permits. Do not manufacture empty commits, split existing work to pretend it happened earlier, or backdate anything.

Suggested milestone messages, only when the described work exists:

1. `chore: establish build specification and deployment scaffold`
2. `feat: deploy FastAPI health endpoint and static interface`
3. `data: prepare attributed Pune corridor terrain and roads`
4. `feat: implement directed routing and constrained shelter allocation`
5. `test: verify allocation invariants and scenario isolation`
6. `feat: add flood scenarios and interactive planning interface`
7. `feat: add exact saved scenarios and allocation exports`
8. `fix: resolve deployed integration and responsive layout issues`
9. `docs: add methods limitations AI disclosure and demo guide`
10. `release: prepare verified hackathon prototype`

Before each commit, inspect staged files and `git diff --cached --check`. Stage intended project files explicitly. Check for accidental secrets, raw downloads, huge files, environment folders and unrelated edits. Use the actual author identity. If teammates push to `main`, fetch and integrate safely; resolve only understood conflicts. Never force-push. Do not squash away the development history before submission.

A final `v1.0-demo` tag is appropriate only after verification. Do not move or overwrite an existing tag. Record the final code commit, tag and deployment identifier. If a later documentation-only commit changes the head, clearly distinguish it from the tested application commit; do not falsely claim the production deployment corresponds to a different SHA.

## 14. Vercel deployment, step by step

1. Authenticate in the owner's personal Hobby scope. Check the plan and do not enable a trial or paid upgrade.
2. Inspect `.vercel/project.json` if already linked; confirm project ownership/name before reusing it. Keep `.vercel/` out of Git.
3. Ensure root `app.py` exposes `app`, Python is 3.12, runtime requirements are slim, and `public/index.html` exists.
4. Confirm `.vercelignore` excludes raw/cache data, local environments, tests' bulky outputs and secrets, while retaining `public/**`, `engine/**`, and compact `data/processed/**`. Do not exclude runtime files accidentally with a broad pattern.
5. Run the local health/static/scenario smoke test using the same relative `/api` paths.
6. Deploy a preview with the installed Vercel CLI (`vercel` / `vercel deploy` as supported). Use repository root as Root Directory and the FastAPI preset. There should be no heavy geospatial build command and no required frontend build.
7. Inspect build logs and returned preview URL. Check `/`, `/index.html`, `/styles.css`, `/js/main.js`, `/api/health`, `/api/meta`, one default scenario, one custom POST, and an overlay PNG. Confirm API JSON is not being replaced by an HTML catch-all page.
8. Inspect function imports and bundled file paths if anything fails. Fix the actual error. Avoid introducing multiple competing routing configurations. Keep the standard Python bundle within the provider limit; no large-function upgrade is needed for this scope.
9. Connect the Vercel project to `shivam-core/jalrekha` through the supported Git integration if possible, with `main` as the intended production branch. Verify the association. If account permissions block automatic Git deployment, use the authenticated CLI as an explicit fallback and record the manual deployment procedure; do not claim pushes deploy automatically when they do not.
10. Once preview validation passes, deploy the verified commit to production (`vercel --prod` or supported equivalent). This production deployment is authorised by the handoff, subject to actual platform permissions. Read the resulting URL and deployment ID from the tool output.
11. Open the production URL in a logged-out/private session. Judges must not need a Vercel or GitHub login. Adjust protection only for this intended public demo if authorised by the account UI. Do not publish credentials or private documents to make it accessible.
12. Verify the same essential interactions on production. Record the actual code SHA/data version and deployment URL in the handoff/status documentation. If Git integration creates additional deployments, check which deployment is actually production.

Use only the default free project domain; no purchased domain is required. Vercel Hobby is for eligible personal, non-commercial use and has resource caps. A small hackathon prototype should be engineered to fit those caps, not promised unlimited hosting. If a paid feature is unexpectedly required, stop that path and use the public static saved-scenario mode on Vercel while reporting the exact limitation.

### Troubleshooting boundaries

| Failure | Correct first response |
|---|---|
| Frontend 404 | Check root/public paths and preset; avoid broad API-swallowing rewrites |
| API returns HTML | Fix route precedence and any static-only/catch-all configuration |
| Missing prepared JSON | Correct include/ignore rules and paths based on `__file__` |
| Native library build fails on Vercel | Remove preparation-only imports/dependencies from runtime |
| Function timeout | Reduce graph/payload, inspect algorithm, use exact saved defaults |
| Wrong overlay after quick slider movement | Abort/discard stale requests and apply one result atomically |
| No route after closure | Treat it as valid if graph checks confirm it; do not invent a route |
| Tile service unavailable | Use prepared roads/waterway on plain background with source label |
| Auth/permissions block push/deploy | Ask for the specific browser authorisation; continue local work |

## 15. Time-boxed execution plan

Treat times as working budgets, not guarantees. Adapt to actual remaining competition time.

| Elapsed target | Deliverable and exit criterion |
|---|---|
| 0–20 min | Inspect repo, authenticate, scope/time check, scaffold, first meaningful commit |
| 20–40 min | Local and preview health + static page + synthetic contract fixture working |
| 40–90 min | Real-data feasibility gate; usable terrain/roads or explicit reduced-scope decision |
| 90–140 min | Routing/allocation/API, known-answer tests, precomputed defaults |
| 140–195 min | Designed interface, closures/capacity edits, map and consistent result updates |
| 195–220 min | Exports/fallbacks, deployed smoke tests, responsive and visual corrections |
| 220–240 min | Production verification, truthful documentation, demo/submission handoff |

If only two hours remain, use 2D, fewer origins/shelters and a few valid saved flood scenarios; preserve real routing/allocation, authentication, Git provenance, and deployment checks. If real HAND is blocked, deliver the labelled road-closure exercise rather than claim a working flood model. Do not cut correctness, assumption labels, or public-link verification to add decoration.

Provide short progress updates focused on what works, the next milestone, and actual risks. Persist status after each milestone. Do not finish with “I can implement this next” while authorised work remains.

## 16. README, presentation and demonstration

The README must include the actual live URL, product purpose, AI-05 mapping, Team Advantage credit, setup commands, architecture, data provenance, limitations, verification commands/results, deployment procedure, and AI-use disclosure. Name contributors only when their identities and contributions are known.

Use a disclosure such as: “AI tools assisted with ideation, planning, code generation, debugging and documentation. The team reviewed and tested the submitted implementation.” List the tools actually used. Do not claim validation that did not occur.

The original PDF lists a companion `jalrekha_starter.zip`; it was not supplied with this handoff. Do not wait for it or claim to have used it. Reimplement from this specification. If the PDF/code is available, reuse permitted helpful portions with attribution and test them, applying the corrections above.

Prepare `docs/presentation-content.md` mapped into the organisers' exact template structure once accessible. The template link extracted from the supplied problem-statement PDF is:

https://docs.google.com/presentation/d/1TqGAM5d53rcmuvWlFzIE5fuVaZYr61M8/edit

Fetch/copy through an available authorised method. Preserve the required template rather than invent a substitute and call it compliant. If accessible and the necessary presentation tools exist, populate a local PPTX with verified screenshots/results. If not accessible, prepare the complete slide text and figures, explicitly flag that the required PPTX still needs the template, and ask the user to supply it while continuing the software work. Do not edit the organiser's shared original. A text outline alone is not the mandatory PPT submission.

Content to cover in the template: problem/user, proposed solution, scenario workflow, architecture, real versus assumed data, algorithms and baseline, actual validation/result example, limitations, future validation/pilot, team and AI disclosure. All percentages/numbers must be computed or sourced; no claimed real-world impact without evidence.

### 75–90 second demo

1. Show the actual corridor and explain “This is a planning simulation with assumed population and shelter capacity.”
2. Start at a tested scenario and show the baseline allocation.
3. Increase the scenario level and identify a modelled accessibility change.
4. Apply one real graph-edge closure; show a rerouted or unreachable origin.
5. Show the constrained plan and open the additional candidate shelter.
6. Explain the measured change in allocated/unallocated people, including ties or infeasibility honestly.
7. Open one route/capacity explanation and export the scenario.
8. End with the method and the next validation need, not a claim of operational readiness.

Choose a demonstrable scenario by inspecting actual computed results. Record a short screen capture if available and authorised by the local tools; otherwise provide exact recording steps and a rehearsed script. Do not spend the last available minutes building a video editing pipeline.

`docs/submission.md` must list the repository, actual public URL, tested commit/tag, required PPT status, optional demo status, and the deadline. No external submission is made without a separate explicit instruction.

## 17. Definition of done and final response

The prototype is complete only when:

- The repository preserves any pre-existing work and contains genuine incremental commits pushed to the correct remote.
- The core interface works on a real small geographic area, with any fallback/synthetic mode explicitly identified.
- Slider/closures/capacity edits produce consistent engine-backed results, or unavailable modes are clearly identified without fabricated outputs.
- No returned route uses a closed edge, no shelter exceeds capacity, and population bookkeeping holds.
- Baseline and optimiser use identical constraints and measured results.
- Runtime deployment excludes geospatial preparation work and secrets.
- The public Vercel URL loads without login, with working API and static assets, or is explicitly delivered as a limited saved-scenario deployment.
- Focused algorithm, API, browser, and deployed checks have been performed, with remaining failures disclosed.
- The README, limitations, data credits, AI disclosure, demo script and submission checklist are present.
- The required PPT is either produced in the organisers' template or explicitly reported as outstanding; never hide this gap behind “all done.”

Finish with a concise factual report: live URL; repository URL; branch and tested commit/tag; implemented features; validation passed; remaining limitations; PPT/demo status; and any exact user action still required. Do not claim a deploy, push, test, or data validation succeeded unless you observed it.

## 18. Source notes and decisions superseding the Claude guide

The uploaded **JALREKHA Complete Build Guide.pdf** supplied the HAND/roads/routing/allocation concept and Colab/Pages/Spaces reference implementation. It explicitly reported synthetic-only sandbox testing and unverified external data downloads. This handoff is a new implementation specification, not a verified copy of that code.

Changes made deliberately: local Codex instead of Colab as primary editor; Vercel for both static interface and FastAPI; Python 3.12 runtime; slim prepared data; preserved road directions/geometry; fixed assembly-point semantics; honest unknown terrain; feasible baseline; lexicographic allocation; explicit fallback state; no uncalibrated discharge-to-metres forecast; real-data-first verification.

Official references checked while preparing this handoff (17 September 2026; recheck only if deployment behaviour differs):

- [Vercel FastAPI deployment, entrypoints and static assets](https://vercel.com/docs/frameworks/backend/fastapi)
- [Vercel Python runtime, supported versions and bundle controls](https://vercel.com/docs/functions/runtimes/python)
- [Vercel Hobby plan](https://vercel.com/docs/plans/hobby)
- [Vercel GitHub integration](https://vercel.com/docs/git/vercel-for-github)
- [Codex authentication](https://learn.chatgpt.com/docs/auth)
- [Codex subscription limits](https://learn.chatgpt.com/docs/pricing)
- [Copernicus public elevation dataset registry](https://registry.opendata.aws/copernicus-dem/)
- [HAND method documentation](https://grass.osgeo.org/grass84/manuals/addons/r.hand.html)
- [Open-Meteo Flood API: discharge, not street-level inundation](https://open-meteo.com/en/docs/flood-api)
- [Hugging Face Spaces current creation/compute requirements](https://huggingface.co/docs/hub/spaces-overview)

The hosted app requires no paid LLM API. Existing ChatGPT Plus usage is still limited, and no completion guarantee is made about the owner's remaining quota. Free hosting is subject to provider eligibility and caps. Initial preview deployment and real-data checks are the evidence gates; a document by itself cannot guarantee compatibility or scientific validity.

**Begin execution now with repository inspection, actual deadline check, and authentication status.**
