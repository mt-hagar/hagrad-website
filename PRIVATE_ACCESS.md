# HAGRad Personal Testing Access

## Policy and current status

Only GitHub account `mt-hagar` (user ID `229219657`) is authorized. Both
`mt-hagar/hagrad-viewer` and `mt-hagar/hagrad-website` are private. GitHub Pages is
disabled. Do not add collaborators, invitations, shared passwords, public ports,
service-token URLs, signup, or self-service registration. Deny by default.

On November 17, 2026 the old domain, Pages origin, and release downloads were tested
without credentials and denied access. Authenticated macOS and Windows downloads
succeeded as the owner. The authenticated website is NOT yet live or verified:
the available local credential cannot manage Codespaces. This repository prepares
that activation but does not claim an end-to-end website access test has passed.

## Why this setup

Authenticated GitHub Pages requires an organization using Enterprise Cloud, not
just a private personal repository. No existing authenticated custom-domain host
or gateway was found. A private Codespaces port uses the existing GitHub identity,
avoids another account, and is suitable for occasional personal testing. It is
not always-on hosting: the Codespace stops when idle and has usage quotas/costs.
Review your existing allowance; no paid plan or new account has been created.

- [Private Pages requirements](https://docs.github.com/en/enterprise-cloud%40latest/pages/getting-started-with-github-pages/about-privately-published-github-pages-sites)
- [Codespaces port authentication](https://docs.github.com/en/codespaces/developing-in-a-codespace/forwarding-ports-in-your-codespace)

## Remaining action: activate under your existing GitHub account

1. Sign in to GitHub as `mt-hagar`. Open the private `mt-hagar/hagrad-website`
   repository, select Code > Codespaces > Create codespace on main. Use only this
   website repository, never the Viewer repository containing the DICOM backend.
2. In the Ports panel, forward port `8088` if it is not already listed. Its Port
   Visibility must be **Private**, not Public or Organization. Leave all other
   ports unforwarded. The devcontainer does not launch an HTTP server automatically.
3. In the Codespace terminal run:

   ```sh
   python3 .devcontainer/serve_private.py
   ```

4. The launcher verifies your numeric GitHub identity, Codespace ownership, private
   website repository, and private port before listening on loopback. It sets 8088
   private explicitly. If verification fails, no site starts. Check `gh auth status`
   and the Ports panel; do not bypass the check or set the port public. If GitHub
   requests additional authorization, authorize your existing `mt-hagar` identity
   through its browser flow, never paste a token into this repository or HTML.
5. Open port 8088 using Open in Browser. Authenticate with your existing GitHub
   session. The private-port gateway, not HTML/JavaScript, enforces access. Do not
   change port visibility while serving. Stop the terminal server when finished.
6. Test the same URL in a completely signed-out browser: it must redirect to
   GitHub authentication or deny access, without returning HAGRad HTML or media.
   Test a known `/assets/` image and video URL as well. In your signed-in session,
   verify the page, media, and private release link work. Record both results before
   calling the authenticated website operational. These live tests remain pending.

The GitHub login page may offer GitHub account creation. Creating another GitHub
account grants no HAGRad access. There is no HAGRad account-creation endpoint or
allow rule for other accounts. Do not create a test account just for this check.

The static server allowlists filenames, refuses directories/symlinks and upload
requests, and sends no-store/noindex headers. It does not serve `.git`, tooling,
this document, binaries, credentials, or a DICOM backend. The gateway is the
authentication boundary; do not run this server behind a public tunnel/proxy.

## Downloads and local workflows

While signed in as `mt-hagar`, open the
[private v0.9.5 release](https://github.com/mt-hagar/hagrad-viewer/releases/tag/v0.9.5-research-preview).
Download `HAGRad-Viewer-macOS.dmg` or `HAGRad-Viewer-Windows.zip` from Assets. These
are the comprehensive Viewer packages with integrated QCA and other workflows.
They are unsigned research previews: retain Gatekeeper and SmartScreen warnings.
Run the installed application locally. Never upload DICOM, patient data, exports,
certificates, or local tooling to the website or software packages.

Standalone QCA remains local/private; it has not been published by this change.
No binaries were rebuilt or replaced. Historical source bundles can contain old
GitHub asset links; those endpoints now require repository access and were tested
anonymous-404. Do not mirror binaries, paste temporary signed storage URLs, or
embed access tokens in the website. Canonical private-repository links are not
bearer credentials; GitHub checks authorization before issuing an asset download.

## Remaining action: remove obsolete public-domain routing

`hagrad.org` currently uses Namecheap DNS (`dns1.registrar-servers.com` and
`dns2.registrar-servers.com`). The domain is offline at GitHub Pages, not served
by the private Codespace. No custom-domain gateway is configured or claimed.

In the existing Namecheap account: Domain List > hagrad.org > Manage > Advanced DNS:

1. Remove only the `@` A records pointing to `185.199.108.153`, `185.199.109.153`,
   `185.199.110.153`, and `185.199.111.153`.
2. Remove only the `www` CNAME pointing to `mt-hagar.github.io`.
3. Remove any Pages-specific AAAA or URL Redirect records if present. Preserve
   unrelated MX/TXT records, email, and domain-verification records.
4. Do not point the domain to a public host or merely CNAME it to a Codespaces URL.
   Codespaces does not provide this authenticated custom-domain configuration.
5. After DNS TTL expiry, recheck both domains; they must remain non-serving.

Dashboard DNS credentials are not available here, so these removals are pending.
Removing dangling Pages DNS also reduces domain-takeover risk. Retain any GitHub
domain verification. To restore this custom domain later requires an existing
compatible host with owner-only authentication and a closed origin, plus live
anonymous/owner tests. Do not re-enable Pages as a shortcut.

## Verification and limits

Check private visibility, only-owner collaborators, empty invitations/deploy keys,
and disabled Pages after any configuration change. Every old release asset and
source archive must deny unsigned requests; the owner must still download them.
No public account creation route may grant access. Do not upload new packages
without inspecting their file contents and scanning for secrets/data first.

Privacy changes cannot recall files already downloaded, browser caches, screenshots,
or third-party archives from the period when the site/software was public. This
setup restricts current origin access; it is not retroactive erasure.

Research use only. Not for clinical diagnosis or patient care. DICOM stays local.
