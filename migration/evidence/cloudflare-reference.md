# Cloudflare reference notes

Documentation was checked on 2026-07-25 before generating redirect artifacts.

- Bulk Redirect source URLs may omit the scheme. A scheme-less source matches both HTTP and HTTPS.
- Bulk Redirect CSV format is:
  `source_url,target_url,status_code,preserve_query_string,include_subdomains,subpath_matching,preserve_path_suffix`
- Free accounts support up to 10,000 Bulk Redirect URLs across lists.
- Pages `_redirects` supports 2,000 static and 100 dynamic redirects, but account-level Bulk Redirects are preferred here because they remain independent of either Pages project.
- Single Redirects execute before Bulk Redirects, so the disabled emergency `302` can override the permanent list during rollback.

Sources:

- https://developers.cloudflare.com/rules/url-forwarding/bulk-redirects/reference/parameters/
- https://developers.cloudflare.com/rules/url-forwarding/bulk-redirects/reference/csv-file-format/
- https://developers.cloudflare.com/changelog/post/2025-02-12-rules-upgraded-limits/
- https://developers.cloudflare.com/pages/platform/limits/
