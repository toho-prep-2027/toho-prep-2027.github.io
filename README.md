# とうほう まいにちアトリエ v1.2 — GitHub Pages only (public content)

Target: 東京都調布市・桐朋小学校（桐朋学園小学校とは別校）。既存分析A〜L、12活動を保持。

## Origin and publishing prerequisite

**Required:** dedicated GitHub Organization and its root Pages site at `https://<ORG>.github.io/`, using repository `<ORG>/<ORG>.github.io`. Keep this GitHub Organization exclusively for this application. Never use a path under the user's personal `github.io` site while storing family data in localStorage: a repository path is not an origin boundary. A separately verified custom domain is an alternative only if already controlled and acceptable to the user; do not silently involve a DNS provider.

Pages source: **GitHub Actions**. `.github/workflows/qa.yml` has the public schema/pattern gate and a deploy job gated by successful validation. PRs do not deploy. Inspect semantic disclosure risk before adding public files/merging; automatic pattern checks cannot guarantee semantic safety.

## Strict publication boundary

Publish only public `index.html`, `sw.js`, `offline.appcache`, `.nojekyll` and `icon.png` (home-screen icon, 180x180 RGB); the workflow enumerates these assets in `_site` rather than publishing the repository root. `content/public-data.json` is **public generic content** for validation, not a separately deployed data endpoint. This repository contains no family import, observation data, child profiles, private snapshot, private source zip or original personal HTML.

Family observations are stored only in the user's browser's localStorage key `toho2027.family-learning.v1` on the validated dedicated-origin host. It is not a secure vault. Import private family data only after verifying the host and security gates. Existing Google Sheets/Calendar/Dossier are authoritative and read-only.

## Test and release gates

1. CI schema, allowlist, secret-pattern and prohibited-value checks pass.
2. Human-readable semantic review of ALL public source and deployed files. No public data with family-specific profile, schedule, identifying context, or private values.
3. GitHub Actions Pages deploy SUCCESS; check published URL and actual SHA/content readback.
4. Confirm target is a distinct HTTPS origin from the user's other apps. Validate cross-origin read attempt blocked.
5. **Critical:** GitHub Pages does not process Netlify `_headers`. Verify `offline.appcache` served with `Content-Type: text/cache-manifest` by a live HTTP response. GitHub Pages does not allow per-repository custom MIME settings. If wrong, block iOS10/L3 acceptance; do not claim `_headers` configured it.
6. Test browser storage, snapshot fail-close/refresh, import/export, mobile UX, and actual offline behaviors. iOS 10.3.3 and L3 require real-device offline restart evidence; do not claim PASS without it.
7. Readback source, commit SHA, GitHub Actions run, published artifacts, manifest, and private Library checkpoint. Formal release is separate from provisional public-only staging.

No Netlify service, site, DNS, deploy command or Netlify artifact is part of this implementation.
