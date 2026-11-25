# HAGRad Website

Public informational website for `hagrad.org`, served by GitHub Pages from `main:/`.
Only static website files, icons, and approved media belong here. Never publish
Viewer source, packages, DICOM files, patient data, exports, certificates, caches,
credentials, or local tooling in this repository.

Standalone QCA and the comprehensive Viewer for Apple Silicon macOS and Windows
are distributed through separate private binary-only repositories,
`mt-hagar/hagrad-qca` and `mt-hagar/hagrad-viewer-downloads`. Website links go
through GitHub sign-in directly to a DMG or EXE. GitHub checks private repository
access before serving each file. There is no
HAGRad signup or password form. Do not put a username, password, token, or signed
storage URL in HTML, JavaScript, configuration, commits, or Pages artifacts.

The website is publicly readable. Downloads are not. Keep research-use-only and
non-clinical text and unsigned macOS/Windows first-launch notes visible. DICOM stays
local. See the private Viewer repository's `docs/private-access.md` for verification.

The public QCA demonstration is `assets/hagrad-qca-demo.mp4`, a 720p web copy
of the research demo. It is not a software package or a route to private assets.
