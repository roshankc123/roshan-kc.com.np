# roshan-kc.com.np

**Personal site and blog of [Roshan Kc](https://roshan-kc.com.np/) — Cofounder & CTO of [MarginTop Solutions](https://www.margintopsolutions.com/), Kathmandu, Nepal.**

[![Live Site](https://img.shields.io/badge/Live%20Site-roshan--kc.com.np-0A66C2?style=flat-square)](https://roshan-kc.com.np/)
[![Blog](https://img.shields.io/badge/Blog-Founder%20%26%20CTO%20Notes-4B5563?style=flat-square)](https://roshan-kc.com.np/blog/)
[![RSS](https://img.shields.io/badge/RSS-Feed-F97316?style=flat-square&logo=rss)](https://roshan-kc.com.np/feed.xml)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Roshan%20Kc-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/roshan-kc-12892b25a)
[![GitHub](https://img.shields.io/badge/GitHub-roshankc123-181717?style=flat-square&logo=github)](https://github.com/roshankc123)
[![Medium](https://img.shields.io/badge/Medium-@kcroshan566-000000?style=flat-square&logo=medium)](https://medium.com/@kcroshan566)

---

## About

This is the source for [roshan-kc.com.np](https://roshan-kc.com.np/) — a static site that serves as my personal presence, founder notes, and technical blog. The site is hosted on GitHub Pages.

I'm Roshan Kc — I cofounded [MarginTop Solutions](https://www.margintopsolutions.com/) and serve as its CTO, leading a growing engineering team in Kathmandu that builds scalable SaaS products and client systems. Before that I taught higher secondary students, which is where I learned to explain hard things simply. I write here about building companies, leading engineering teams, and the technical decisions that actually matter in production.

---

## What's on the site

### 🔗 Live pages

| Page | URL |
|---|---|
| Home | [roshan-kc.com.np](https://roshan-kc.com.np/) |
| Blog index | [roshan-kc.com.np/blog/](https://roshan-kc.com.np/blog/) |
| RSS feed | [roshan-kc.com.np/feed.xml](https://roshan-kc.com.np/feed.xml) |
| Sitemap | [roshan-kc.com.np/sitemap.xml](https://roshan-kc.com.np/sitemap.xml) |
| LLMs.txt | [roshan-kc.com.np/llms.txt](https://roshan-kc.com.np/llms.txt) |

---

## Blog posts

Practical writing on engineering leadership, startup decisions, and technical craft. All posts are data-backed where possible — benchmarks, research references, and real examples from what we've built at MarginTop.

### Docker & Infrastructure
- **[Optimized Laravel Docker Image: PHP 8.5 + Swoole + io_uring (ARM64 Preferred)](https://roshan-kc.com.np/blog/optimized-laravel-docker-swoole-iouring.html)** — How I built a public Docker image that compiles Swoole 6.2.2 with `--enable-iouring`, what io_uring is and why it matters for Laravel Octane concurrency, and why ARM64/Graviton is the preferred deployment target. Multi-arch (amd64 + arm64). Free on [Docker Hub](https://hub.docker.com/r/roshankc1234/optimized-laravel-runtime).

### Laravel & PHP Performance
- **[How We Use Laravel Octane + Swoole to Handle Concurrent Load](https://roshan-kc.com.np/blog/laravel-octane-swoole-concurrent-load.html)** — What Octane actually changes in the request model, community benchmark data (3–10× RPS gains), `Octane::concurrently` for parallel I/O, and the ops caveats nobody puts in the tutorial.
- **[What TypePHP Means for the Future of PHP Performance](https://roshan-kc.com.np/blog/what-typephp-means-for-php-performance.html)** — PHP performance history from PHP 5 to 8.x JIT, what Swoole's AOT compiler is doing, and why HHVM's story is the right frame for evaluating it.
- **[Why We Chose Laravel Over Node.js for Our Stack](https://roshan-kc.com.np/blog/why-we-chose-laravel-over-nodejs.html)** — Ecosystem comparison table, hiring pool reality in Nepal, and honest cases where Node genuinely wins.

### Architecture & Engineering
- **[The Hidden Cost of Premature Microservices](https://roshan-kc.com.np/blog/hidden-cost-premature-microservices-monolith.html)** — Why we're still a modular Laravel monolith, with a cost table (distributed debugging, contract churn, duplicated auth) and the signals we watch before extracting a service.
- **[Business Logic First: Why We Don't Worry About the Perfect Tech Stack](https://roshan-kc.com.np/blog/business-logic-first-not-perfect-tech-stack.html)** — Stack migration costs 2–6 weeks. Domain model migration costs 6–18 months. Why AI tools make the argument for business-logic-first even stronger.
- **[Our Engineering Principles: How We Decide What NOT to Build](https://roshan-kc.com.np/blog/engineering-principles-what-not-to-build.html)** — The five principles we apply, with a concrete table of things we said no to and what we did instead.
- **[Build vs. Buy: The Framework We Use](https://roshan-kc.com.np/blog/build-vs-buy-framework-what-to-build-in-house.html)** — Decision matrix with 7 real examples. When the maintenance tax of commodity code exceeds the license fee.

### Security
- **[Security Basics Every Early-Stage Startup Should Get Right Before Fundraising](https://roshan-kc.com.np/blog/security-basics-startups-before-fundraising.html)** — IBM 2024 breach data ($4.88M average cost), an 8-control pre-fundraise checklist table, and the correct SOC 2 sequencing.

### AI & Velocity
- **[How AI Coding Tools Changed Our Engineering Velocity (Without Changing Our Standards)](https://roshan-kc.com.np/blog/how-ai-coding-tools-changed-engineering-velocity.html)** — GitHub/Microsoft (55.8% faster), McKinsey (35–45%), and METR (2025) study results. Task-type impact table. Where AI doesn't help.

### Startups & Cloud
- **[How to Run Your Startup Tech Stack for Free Until You're Funded](https://roshan-kc.com.np/blog/how-to-run-startup-tech-stack-free-until-funded.html)** — Cloud credits comparison table: AWS Activate, Microsoft for Startups (up to $150K no-VC tier), Google Cloud for Startups. Billing guardrails and billing alert strategy.
- **[Ship Fast Without Losing Client Trust](https://roshan-kc.com.np/blog/ship-fast-without-losing-client-trust.html)** — Milestone-based delivery, scope cuts in the open, quality floors, and why hustle ≠ thrash.

### Team & Leadership
- **[Building a Software Team in Kathmandu From Zero](https://roshan-kc.com.np/blog/building-a-software-team-in-kathmandu.html)** — Nepal tech market context, hiring quality table, and why culture investment is the multiplier.
- **[What I Look for When Hiring Engineers as a First-Time CTO](https://roshan-kc.com.np/blog/hiring-engineers-as-first-time-cto.html)** — Ownership over ticket theater, trade-off judgment probing table, and what I explicitly deprioritize (prestigious past employers, whiteboard algorithms).
- **[What a First-Time CTO Actually Does (Beyond the Title)](https://roshan-kc.com.np/blog/what-a-first-time-cto-actually-does.html)** — Weekly time breakdown table, the hero-to-leader transition, and habits that compound.

### Founder Story
- **[Why I Left Teaching to Build a Company in Kathmandu](https://roshan-kc.com.np/blog/why-i-left-teaching-to-build-a-company.html)** — The quiet tipping point, what the first year actually felt like, and advice for founders in Nepal.

---

## How the site works

### Architecture

```
roshan-kc.com.np/          ← Static HTML/CSS/JS — this repo
      │
      ├── index.html        ← Home page
      ├── blog/             ← Individual blog posts (static HTML)
      ├── css/site.css      ← Single stylesheet
      ├── js/shell.js       ← Sidebar, deck navigation, mobile menu
      ├── feed.xml          ← RSS feed
      ├── sitemap.xml       ← Sitemap for search engines
      ├── llms.txt          ← Machine-readable identity for AI assistants
      └── images/           ← Profile and asset images
```

The **Projects** section on the home page auto-fetches my public GitHub repositories and displays them dynamically. To avoid hitting GitHub API rate limits (60 unauthenticated requests/hour), this fetch goes through a private Python/Flask backend that caches responses and holds the authenticated API token. The frontend calls the backend; the backend calls GitHub. This also keeps the auth token out of client-side code.

### Tech stack

| Layer | Technology |
|---|---|
| Hosting | GitHub Pages |
| Frontend | Vanilla HTML, CSS, JavaScript (no framework) |
| Fonts | Atkinson Hyperlegible + JetBrains Mono (Google Fonts) |
| Projects API | Python / Flask (private backend, not in this repo) |
| DNS | Custom domain `roshan-kc.com.np` via CNAME |

---

## Public Docker image

I publish and maintain a free Docker image for Laravel Octane with io_uring support:

**[`roshankc1234/optimized-laravel-runtime`](https://hub.docker.com/r/roshankc1234/optimized-laravel-runtime)**

```bash
docker pull roshankc1234/optimized-laravel-runtime:php8.5-swoole6.2.2-iouring
```

- PHP 8.5 + Swoole 6.2.2 compiled with `--enable-iouring`
- Nginx + Supervisor included
- Multi-arch: `linux/amd64` + `linux/arm64` — **ARM64/Graviton recommended**
- ~78MB compressed Alpine base

See the full writeup: [Optimized Laravel Docker Image blog post](https://roshan-kc.com.np/blog/optimized-laravel-docker-swoole-iouring.html)

---

## Connect

| Platform | Link |
|---|---|
| 🌐 Website | [roshan-kc.com.np](https://roshan-kc.com.np/) |
| 🏢 Company | [margintopsolutions.com](https://www.margintopsolutions.com/) |
| 💼 LinkedIn | [linkedin.com/in/roshan-kc-12892b25a](https://www.linkedin.com/in/roshan-kc-12892b25a) |
| 🐙 GitHub | [github.com/roshankc123](https://github.com/roshankc123) |
| ✍️ Medium | [medium.com/@kcroshan566](https://medium.com/@kcroshan566) |
| 📘 Facebook | [facebook.com/roshan.kc.3557440](https://www.facebook.com/roshan.kc.3557440) |
| 📱 WhatsApp | [wa.me/qr/4VJJDHCT4HNUC1](https://wa.me/qr/4VJJDHCT4HNUC1) |
| 📧 Email | [kcroshan566@gmail.com](mailto:kcroshan566@gmail.com) |

---

## License

Source code in this repository is released under the [MIT License](LICENSE).  
Blog content and writing are © Roshan Kc. All rights reserved.

---

*Built and maintained by [Roshan Kc](https://roshan-kc.com.np/) · Kathmandu, Nepal*
