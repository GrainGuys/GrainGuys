# GrainGuys

Official website for **GrainGuys** — a professional handyman and carpentry service offering reliable repairs, assembly, painting, flooring, and custom woodwork for homeowners and businesses.

---

## Project Overview

GrainGuys is a static, multi-page marketing website built to showcase services, portfolio work, team information, and customer engagement features. The site presents GrainGuys as a dependable, skilled handyman brand with clear calls to action for free estimates and contact.

The repository contains the full front-end codebase, assets, and lightweight PHP handlers for form submissions.

---

## Purpose and Goals

| Goal | Description |
|------|-------------|
| **Lead generation** | Drive inquiries through contact forms, appointment booking, and prominent “Free Estimate” CTAs |
| **Service discovery** | Present eight core service categories with dedicated detail pages |
| **Trust building** | Highlight testimonials, project galleries, team profiles, and FAQs |
| **Brand presence** | Deliver a polished, responsive experience that reflects professional craftsmanship |
| **Maintainability** | Keep the codebase organized for straightforward content updates and deployment |

---

## Features

### Pages and Layouts

- **Home** — Three variants: standard (`index.html`), slider hero (`index-slider.html`), and video hero (`index-video.html`)
- **About Us** — Company story, mission, vision, and experience counters
- **Services** — Service grid with nine dedicated detail pages (`service-general-repairs.html`, `service-furniture-assembly.html`, and more)
- **Projects** — Portfolio listing and project detail pages
- **Blog** — Article listing and single post template
- **Team** — Team roster and individual member pages
- **Galleries** — Image and video gallery pages
- **Support pages** — Testimonials, FAQs, 404, and Contact

### Interactive Elements

- Responsive navigation with mobile menu (SlickNav)
- Hero sliders and carousels (Swiper)
- Scroll-triggered animations (WOW.js, GSAP, ScrollTrigger)
- Image and video lightboxes (Magnific Popup)
- Animated counters and parallax sections
- Custom cursor effects
- Contact and appointment forms with client-side validation
- PHP mail handlers for form processing (`form-process.php`, `form-appointment.php`)

### Content Management Utilities

- `update_handyman_content.py` — Batch content update script
- `translate_site.py` — Site translation utility

---

## Technology Stack

| Layer | Technologies |
|-------|--------------|
| **Markup & styling** | HTML5, CSS3, Bootstrap 5 |
| **Scripting** | JavaScript (ES5-compatible), jQuery 3.7 |
| **Animation** | GSAP, ScrollTrigger, SplitText, WOW.js, Animate.css |
| **UI components** | Swiper, SlickNav, Magnific Popup, jQuery CounterUp, Waypoints |
| **Typography** | Google Fonts — Inter |
| **Icons** | Font Awesome |
| **Backend (forms)** | PHP (`mail()` for contact and appointment submissions) |
| **Tooling** | Python 3 (optional content scripts) |

---

## Project Structure

```
GrainGuys/
├── index.html                 # Main homepage
├── index-slider.html          # Homepage with slider hero
├── index-video.html           # Homepage with video hero
├── about.html                 # About page
├── services.html              # Services listing
├── service-general-repairs.html # General repairs service detail
├── service-furniture-assembly.html
├── service-painting-decorating.html
├── service-kitchen-fitting.html
├── service-flooring-tiling.html
├── service-custom-woodwork.html
├── service-shop-counter-construction.html
├── service-bespoke-design-work.html
├── service-general-handyman.html
├── projects.html              # Project portfolio
├── project-single.html        # Project detail template
├── blog.html                  # Blog listing
├── blog-single.html           # Blog post template
├── team.html                  # Team listing
├── team-single.html           # Team member detail
├── testimonials.html          # Customer testimonials
├── image-gallery.html         # Photo gallery
├── video-gallery.html         # Video gallery
├── faqs.html                  # Frequently asked questions
├── contact.html               # Contact page
├── 404.html                   # Not found page
├── form-process.php           # Contact form handler
├── form-appointment.php       # Appointment form handler
├── css/
│   ├── bootstrap.min.css      # Bootstrap framework
│   ├── custom.css             # Project-specific styles
│   └── …                      # Plugin stylesheets
├── js/
│   ├── function.js            # Main site logic
│   ├── jquery-3.7.1.min.js    # jQuery
│   └── …                      # Plugin scripts
├── images/                    # Logos, icons, photos, SVG assets
├── update_handyman_content.py # Content update utility
├── translate_site.py          # Translation utility
└── README.md                  # This file
```

---

## Getting Started

### Prerequisites

- A modern web browser (Chrome, Firefox, Safari, or Edge)
- A local web server for full functionality (recommended)
- PHP 7.4+ with `mail()` configured (required only for form submission handlers)

### Local Development

**Option 1 — PHP built-in server (includes form handlers)**

```bash
git clone git@github.com:GrainGuys/GrainGuys.git
cd GrainGuys
php -S localhost:8000
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

**Option 2 — Static preview (HTML/CSS/JS only)**

Open any `.html` file directly in a browser, or use a simple static server:

```bash
# Using Python
python -m http.server 8000

# Using Node.js (npx)
npx serve .
```

> **Note:** Form submissions require PHP. Static preview will display pages but cannot process contact or appointment forms.

### Form Configuration

Before deploying, update the recipient email in the PHP handlers:

1. Open `form-process.php` and set `$to` to your business email address
2. Open `form-appointment.php` and configure the recipient address similarly
3. Ensure your hosting environment supports PHP `mail()` or replace with an SMTP library

### GitHub Pages (Dev & Demo)

The site is hosted free on **GitHub Pages** for development and demo previews.

| | |
|---|---|
| **Live demo** | [https://grainguys.github.io/GrainGuys/](https://grainguys.github.io/GrainGuys/) |
| **Source branch** | `master` (repository root) |
| **Cost** | Free |

Every push to `master` triggers the [Deploy to GitHub Pages](.github/workflows/pages.yml) workflow and updates the demo site automatically (usually within 1–2 minutes).

**How it works:** GitHub Actions uploads the repository as a static artifact and deploys it via the official Pages pipeline (no Jekyll, no server required).

**Demo limitations on GitHub Pages:**

- Contact and appointment forms show a demo message instead of sending email (PHP is not supported on GitHub Pages)
- For live form handling, deploy to a PHP-capable host (see Production Deployment below)

**Enable or reconfigure Pages** (org admins):

In the GitHub UI: **Settings → Pages → Source: GitHub Actions**.

Or via CLI:

```bash
gh api --method PUT /repos/GrainGuys/GrainGuys/pages -f "build_type=workflow"
```

### Production Deployment

Deploy the repository contents to any web host that supports static files. For form functionality, choose a host with PHP support (e.g., shared hosting, VPS, or a PHP-enabled platform).

Typical deployment steps:

1. Upload all files to the web root (`public_html`, `www`, or equivalent)
2. Verify `form-process.php` and `form-appointment.php` permissions and mail settings
3. Test contact and appointment forms in production
4. Point your domain DNS to the hosting provider

---

## Development Workflow

1. **Clone the repository** and create a feature branch from `main`
2. **Run locally** using the PHP or static server commands above
3. **Edit content** directly in HTML files or use the Python utilities for bulk updates
4. **Style changes** go in `css/custom.css`; avoid editing vendor/minified files under `css/` and `js/`
5. **Behavior changes** go in `js/function.js`
6. **Test responsively** across mobile, tablet, and desktop breakpoints
7. **Open a pull request** with a clear description of changes

### Branch Naming

| Prefix | Use case |
|--------|----------|
| `feature/` | New pages, sections, or functionality |
| `fix/` | Bug fixes and broken layout corrections |
| `content/` | Copy, image, and metadata updates |
| `chore/` | Dependencies, tooling, or housekeeping |

### Commit Messages

Write concise, imperative commit messages:

```
Add shop counter service to homepage grid
Fix mobile navigation overlap on contact page
Update testimonial copy on about page
```

---

## Contribution Guidelines

Contributions are welcome from team members and collaborators. Please follow these guidelines:

1. **Fork or branch** — Never commit directly to `main` for non-trivial changes
2. **Keep changes focused** — One logical change per pull request
3. **Match existing style** — Follow indentation, naming, and HTML structure conventions already in the codebase
4. **Do not modify vendor files** — Update `custom.css` and `function.js` instead of minified libraries
5. **Test before submitting** — Verify pages load, links work, and forms behave as expected
6. **Document significant changes** — Update this README when adding pages, dependencies, or deployment steps

### Pull Request Checklist

- [ ] Pages render correctly on mobile and desktop
- [ ] No broken internal links
- [ ] Custom styles are in `custom.css`, not inline (unless matching existing patterns)
- [ ] Form endpoints updated if email routing changed
- [ ] No secrets or credentials committed

---

## License

Copyright © GrainGuys. All rights reserved.

This repository and its contents are proprietary. Unauthorized copying, distribution, or use outside of the GrainGuys organization is prohibited unless explicit written permission is granted.

---

## Contact

For business inquiries, visit the [Contact page](contact.html) on the live site or call **07709 034572**.

For repository or development questions, open an issue in this GitHub repository or contact the maintainers through the GrainGuys organization.
