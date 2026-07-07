# GrainGuys — Deployment & Forms TODO

Checklist for hosting **GrainGuys.co.uk** on **Cloudflare Pages** and handling contact form submissions without PHP.

---

## Current status

| Item | Status |
|------|--------|
| Static site (HTML/CSS/JS) | Ready |
| Domain on Cloudflare (`grainguys.co.uk`) | Done (transferred from GoDaddy) |
| Contact form → Web3Forms | Implemented in code — **access key still required** |
| Appointment form (`requestquoteForm`) | Migrated to Web3Forms — **access key still required** |
| Cloudflare Pages production deploy | Not started |
| Long-term serverless form handler | Planned (optional upgrade) |

---

## 1. Contact form — Web3Forms (short-term, recommended now)

Cloudflare Pages cannot run PHP. The contact form on `contact.html` and `team-single.html` posts to [Web3Forms](https://web3forms.com) instead of `form-process.php`.

### What is already done

- Form `action` set to `https://api.web3forms.com/submit`
- Honeypot spam field (`botcheck`) added to both contact forms
- `js/function.js` sends AJAX to Web3Forms and shows success/error in `#msgSubmit`
- Works on **Cloudflare Pages** and **GitHub Pages** (no PHP needed)

### Files involved

| File | Role |
|------|------|
| `contact.html` | Main contact page form (`#contactForm`) |
| `team-single.html` | Team member page contact form (`#contactForm`) |
| `js/function.js` | Validation, Web3Forms submit, `WEB3FORMS_ACCESS_KEY` config |
| `form-process.php` | Legacy PHP handler — **not used** on Cloudflare Pages |

### TODO — finish Web3Forms setup

- [ ] Go to [https://web3forms.com](https://web3forms.com) and create a free access key
- [ ] Register the key with your business email (e.g. `info@grainguys.com`)
- [ ] Open `js/function.js` and replace the placeholder:

  ```js
  var WEB3FORMS_ACCESS_KEY = "REPLACE_WITH_YOUR_ACCESS_KEY";
  ```

- [ ] Deploy the site (see [§3 Cloudflare Pages deployment](#3-cloudflare-pages-deployment) below)
- [ ] Submit a test message from `contact.html` on the live domain
- [ ] Confirm the email arrives and reply-to / field names look correct
- [ ] (Optional) Enable Web3Forms spam filtering or reCAPTCHA in their dashboard

### Form fields sent to Web3Forms

| Field | Description |
|-------|-------------|
| `fname` | First name |
| `lname` | Last name |
| `email` | Sender email |
| `phone` | Phone number |
| `message` | Message body |

Email subject is set in JS: `New GrainGuys contact form message`.

---

## 2. Appointment / quote form — Web3Forms

The homepage (and `about.html`, `index-slider.html`, `index-video.html`) use `#requestquoteForm`, which now posts to Web3Forms via `js/function.js` (same `WEB3FORMS_ACCESS_KEY` as the contact form).

### What is already done

- Form `action` set to `https://api.web3forms.com/submit` on all four pages
- Honeypot spam field (`botcheck`) added
- `submitappointmentForm()` in `js/function.js` posts to Web3Forms
- Email subject: `New GrainGuys quote request`

### TODO — finish setup

- [ ] Set `WEB3FORMS_ACCESS_KEY` in `js/function.js` (shared with contact form)
- [ ] Test quote form on `index.html` and `about.html` on the live site

**Option B — Long-term Cloudflare Function** (see [§4](#4-long-term-option-cloudflare-pages-functions))

- [ ] Implement `/api/appointment` alongside `/api/contact` (optional upgrade)

---

## 3. Cloudflare Pages deployment

Host the static site free on **Cloudflare Pages** with custom domain **grainguys.co.uk** (domain already on Cloudflare).

### Prerequisites

- [ ] Site code in a Git repository (GitHub or GitLab)
- [ ] Cloudflare account with `grainguys.co.uk` added
- [ ] Web3Forms access key configured (for contact form)

### Create the Pages project

1. Cloudflare dashboard → **Workers & Pages** → **Create** → **Pages** → **Connect to Git**
2. Select the GrainGuys repository
3. Build settings:

   | Setting | Value |
   |---------|--------|
   | Framework preset | **None** |
   | Build command | *(leave empty)* |
   | Build output directory | `/` *(repository root)* |

4. **Save and Deploy** — you get a `*.pages.dev` preview URL

### Custom domain

1. In the Pages project → **Custom domains**
2. Add `grainguys.co.uk` and `www.grainguys.co.uk`
3. Cloudflare creates DNS records and provisions **free SSL** automatically (domain is already on Cloudflare)

### DNS (if not auto-added)

Typical records when domain is on Cloudflare:

| Type | Name | Target |
|------|------|--------|
| CNAME | `www` | `<project-name>.pages.dev` |
| CNAME or flatten | `@` (apex) | Pages (Cloudflare often uses CNAME flattening for apex) |

Use the exact records shown in the Pages **Custom domains** UI.

### Post-deploy checks

- [ ] `https://grainguys.co.uk` loads with valid HTTPS
- [ ] `https://www.grainguys.co.uk` redirects or resolves correctly
- [ ] Home, services, projects, and contact pages load without 404s
- [ ] Images, CSS, and JS load (no mixed-content or path errors)
- [ ] Mobile navigation works
- [ ] Contact form submits and email is received
- [ ] Browser console has no critical JavaScript errors

### Local preview (before deploy)

```bash
# Static preview only (forms need network access to Web3Forms)
npx serve .

# Or Python
python -m http.server 8000
```

Open `http://localhost:8000/contact.html`. Form submit requires a valid `WEB3FORMS_ACCESS_KEY` and internet access.

### GitHub Pages vs Cloudflare Pages

| | GitHub Pages | Cloudflare Pages |
|---|--------------|------------------|
| Cost | Free | Free |
| Custom domain | Yes | Yes (easier when DNS is on Cloudflare) |
| PHP | No | No |
| Contact form (Web3Forms) | Yes | Yes |
| Recommended for production | Demo | **Production (`grainguys.co.uk`)** |

GitHub Pages can stay as a demo/staging URL; point the live domain to Cloudflare Pages.

---

## 4. Long-term option — Cloudflare Pages Functions

For more control, branding, and keeping API keys off the client, replace Web3Forms with a **Cloudflare Pages Function** that sends email via an API (e.g. [Resend](https://resend.com), SendGrid, or MailChannels).

### Why upgrade later

- Email API key stays **server-side** (environment variable in Cloudflare)
- Custom HTML email templates (similar to current `form-process.php`)
- Single backend for contact **and** appointment forms
- No third-party form dashboard dependency

### High-level architecture

```
Browser → POST /api/contact → Pages Function → Resend/SendGrid → info@grainguys.com
```

### TODO — implement when ready

- [ ] Sign up for Resend (or similar) and verify `grainguys.co.uk` domain for sending
- [ ] Create `functions/api/contact.js` (or `functions/api/contact.ts`) in the repo
- [ ] Add Cloudflare environment variables (e.g. `RESEND_API_KEY`, `CONTACT_TO_EMAIL`) in Pages project settings — **never commit secrets**
- [ ] Update `contact.html` / `team-single.html`:

  ```html
  <form id="contactForm" action="/api/contact" method="POST">
  ```

- [ ] Update `submitForm()` in `js/function.js` to POST JSON or form data to `/api/contact` and handle JSON responses
- [ ] Port validation from `form-process.php` (required fields, email format, HTML email body)
- [ ] Add rate limiting / honeypot / Turnstile in the Function if needed
- [ ] Repeat for appointment form: `functions/api/appointment.js` + `#requestquoteForm`
- [ ] Test on preview `*.pages.dev`, then production domain
- [ ] Remove Web3Forms key from `js/function.js` once migrated

### Example Function sketch (reference only)

```js
// functions/api/contact.js
export async function onRequestPost(context) {
  const { request, env } = context;
  const data = await request.formData();
  // validate fields, call Resend API with env.RESEND_API_KEY
  return new Response(JSON.stringify({ success: true }), {
    headers: { "Content-Type": "application/json" },
  });
}
```

See [Cloudflare Pages Functions docs](https://developers.cloudflare.com/pages/functions/) for the exact file layout and bindings.

---

## 5. Legacy PHP handlers

`form-process.php` is **not used** on Cloudflare Pages or GitHub Pages. `form-appointment.php` has been removed; the quote form uses Web3Forms.

| File | Status on static hosting |
|------|--------------------------|
| `form-process.php` | Superseded by Web3Forms (contact) |
| `form-appointment.php` | Removed — quote form uses Web3Forms |

Keep PHP files in the repo for reference or remove after all forms are migrated.

---

## 6. Master checklist (go-live)

- [ ] Web3Forms access key set in `js/function.js`
- [ ] Cloudflare Pages project connected to Git
- [ ] `grainguys.co.uk` and `www` attached to Pages
- [ ] Contact form tested on production
- [ ] Appointment / quote form tested on production
- [ ] Footer/header emails and phone links verified
- [ ] `404.html` works for missing routes (configure in Cloudflare Pages if needed)

---

## References

- [Web3Forms](https://web3forms.com/docs)
- [Cloudflare Pages](https://developers.cloudflare.com/pages/)
- [Cloudflare Pages Functions](https://developers.cloudflare.com/pages/functions/)
- [Resend + Cloudflare Workers/Pages](https://resend.com/docs)
