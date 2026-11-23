# Commons Lens

A public Wikimedia Commons discovery and attribution desk at https://coolcode.ca/commonslens/. Search any subject, inspect creator and licence metadata, build attribution text, and keep a shortlist or dated receipt. No account or API key is required.

<!-- coolcode:guide -->
Search **Halifax waterfront**, then open **Inspect & credit** on a work to find its original record and reported licence. Licence and creator filters narrow the returned page, not the whole catalogue; inspect later pages or loosen a filter if a page has no matches. **Shortlist** keeps selections only in this tab. Save receipt JSON before closing; an imported receipt is processed locally. Always verify the original record before reusing a work.
<!-- /coolcode:guide -->

## What it does

- Searches arbitrary text through Wikimedia's public Action API, including audio files.
- Shows each result's title, creator, original source, reported licence, dimensions where present and source attribution wording.
- Builds plain-text attribution, including an optional statement of your changes.
- Provides a tab-local shortlist, CSV and timestamped JSON export, and validated receipt import.
- Caches up to 30 responses within the tab, spaces requests at least 1.5 seconds apart, and preserves the last result on errors. No request is made on each keystroke.

Wikimedia returns a page of search results. Media, creator and licence filters are applied locally to that page, so zero displayed matches do not establish no matching work exists. Source metadata may specify more than one licence; inspect the source for your options and obligations. No licence label is a guarantee of reuse rights.

## Sources and access

[Wikimedia Action API](https://www.mediawiki.org/wiki/API:Imageinfo) supplies file metadata. Anonymous cross-origin access uses the [documented origin=* parameter](https://www.mediawiki.org/wiki/API:Cross-site_requests), without cookies or credentials. Content keeps its individual licence: see [Commons reuse guidance](https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia).

Openverse was the initial proposed source, but its API returned a Cloudflare verification response during the deployment investigation on 23 November 2026. This app uses the separately provided Wikimedia API, which returned actual Halifax records and CORS permission. It does not proxy around Openverse's challenge. The page links Openverse as another discovery service; there are no Openverse API calls in the active workflow.

The 23 November 2026 contract check returned real Halifax waterfront media, a creator (Gordon Leggett), original source and CC licence metadata. Browser CI uses clearly synthetic intercepted responses to exercise rendering and failures independently of provider availability. Root publication review also tests a live query.

## Privacy

Only submitting a search sends query text and filters to Wikimedia. Enabled thumbnails contact their media hosts; switch previews off before searching for links only. Audio uses preload=none and loads when played. Imported receipts and shortlist choices remain in memory. No localStorage, account, tracking of search words, or hidden uploads. The shared CoolCode page counter is independent of search inputs.

## Expand or customize

Edit `web/config.json`:

```json
{
  "pageSize": 12,
  "presets": [{"label":"Halifax waterfront","query":"Halifax waterfront"}],
  "requestTimeoutMs": 20000,
  "minimumRequestIntervalMs": 1500,
  "maximumSavedItems": 100,
  "providers": {"wikimedia":"https://commons.wikimedia.org/w/api.php"}
}
```

Add any preset without changing application code. Visitors can enter any search directly. Page size is capped at 20; receipt imports at 1,000 works/5 MB; requests are capped at 30 seconds. These explicit limits control workload rather than the initial examples. The endpoint must be HTTPS and support the same MediaWiki API. Do not insert credentials into this public file. Push configuration or source edits to `main`; **Commons Lens · Check and publish** tests and deploys them. There is no collector, schedule or fixed index to refresh.

## Verification

```sh
node --test tests/*.test.mjs
python3 -m unittest discover -s tests -v
python3 scripts/build.py
```

CI additionally runs `tests/browser_smoke.py` for a real UI flow at a project subpath, exports, error preservation, safe text and mobile widths. Tests cover query encoding, correct licence matching, hostile source URLs, normalization, receipts and attribution. The build is offline.
