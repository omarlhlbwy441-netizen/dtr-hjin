"""
╔══════════════════════════════════════════════════════════════════╗
║  Rafeeq Kernel v2.3.0 — WebArchitect Agent                     ║
║  وكيل تصميم وبناء المواقع الإلكترونية                            ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import json
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path


class WebArchitect:
    """وكيل متخصص في تصميم وبناء المواقع الإلكترونية"""

    WEBSITE_TEMPLATES = {
        "portfolio": {
            "name": "Portfolio Website",
            "description": "موقع شخصي لعرض الأعمال",
            "sections": ["hero", "about", "projects", "skills", "contact"],
            "style": "modern",
            "colors": {"primary": "#0ea5e9", "secondary": "#8b5cf6", "accent": "#10b981"}
        },
        "landing": {
            "name": "Landing Page",
            "description": "صفحة هبوط للمنتجات والخدمات",
            "sections": ["hero", "features", "pricing", "testimonials", "cta"],
            "style": "minimal",
            "colors": {"primary": "#0f172a", "secondary": "#1e293b", "accent": "#0ea5e9"}
        },
        "blog": {
            "name": "Blog Website",
            "description": "مدونة مع نظام إدارة مقالات",
            "sections": ["header", "featured", "articles", "sidebar", "footer"],
            "style": "clean",
            "colors": {"primary": "#1e293b", "secondary": "#334155", "accent": "#f59e0b"}
        },
        "ecommerce": {
            "name": "E-Commerce Store",
            "description": "متجر إلكتروني مع سلّة مشتريات",
            "sections": ["header", "products", "cart", "checkout", "footer"],
            "style": "premium",
            "colors": {"primary": "#0f172a", "secondary": "#1e293b", "accent": "#ef4444"}
        },
        "dashboard": {
            "name": "Admin Dashboard",
            "description": "لوحة تحكم إدارية",
            "sections": ["sidebar", "header", "stats", "charts", "tables"],
            "style": "dark",
            "colors": {"primary": "#0f172a", "secondary": "#1e293b", "accent": "#0ea5e9"}
        }
    }

    def __init__(self):
        self.websites_dir = Path("websites")
        self.websites_dir.mkdir(exist_ok=True)
        self.generated_websites = []

    def list_templates(self) -> List[Dict]:
        return [{"id": k, **v} for k, v in self.WEBSITE_TEMPLATES.items()]

    def generate_website(self, template_type: str, title: str, custom_config: Optional[Dict] = None) -> Dict[str, Any]:
        if template_type not in self.WEBSITE_TEMPLATES:
            return {"status": "error", "message": f"Template '{template_type}' not found"}

        template = self.WEBSITE_TEMPLATES[template_type]
        site_id = str(uuid.uuid4())[:8]
        safe_title = title.replace(" ", "_").lower()
        site_dir = self.websites_dir / f"{safe_title}_{site_id}"
        site_dir.mkdir(parents=True, exist_ok=True)

        config = {**template, **(custom_config or {})}
        colors = config.get("colors", template["colors"])

        files_generated = []

        # HTML
        html = self._generate_html(template_type, title, config, colors)
        (site_dir / "index.html").write_text(html, encoding="utf-8")
        files_generated.append("index.html")

        # CSS
        css = self._generate_css(template_type, colors)
        (site_dir / "style.css").write_text(css, encoding="utf-8")
        files_generated.append("style.css")

        # JS
        js = self._generate_js(template_type)
        (site_dir / "script.js").write_text(js, encoding="utf-8")
        files_generated.append("script.js")

        # Config
        cfg = json.dumps({
            "site_id": site_id, "title": title, "type": template_type,
            "created_at": datetime.utcnow().isoformat(),
            "config": config, "files": files_generated
        }, indent=2, ensure_ascii=False)
        (site_dir / "site.json").write_text(cfg, encoding="utf-8")
        files_generated.append("site.json")

        site_info = {
            "status": "success", "site_id": site_id, "title": title,
            "type": template_type, "directory": str(site_dir),
            "files": files_generated,
            "preview_url": f"/websites/{safe_title}_{site_id}/index.html",
            "created_at": datetime.utcnow().isoformat()
        }
        self.generated_websites.append(site_info)
        return site_info

    def _generate_html(self, template_type, title, config, colors):
        sections = config.get("sections", [])
        html_parts = [f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Rafeeq WebArchitect</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap" rel="stylesheet">
</head>
<body>
    <nav class="navbar">
        <div class="nav-brand">🐺 {title}</div>
        <div class="nav-links">
            <a href="#home">الرئيسية</a>
            <a href="#about">عنّا</a>
            <a href="#services">الخدمات</a>
            <a href="#contact">تواصل</a>
        </div>
    </nav>
"""]

        # Generate sections based on template
        for section in sections:
            if section == "hero":
                html_parts.append(f"""
    <section id="home" class="hero">
        <div class="hero-content">
            <h1>مرحباً بك في {title}</h1>
            <p>نبني المستقبل بأيدٍ مصرية 🇪🇬</p>
            <div class="hero-buttons">
                <button class="btn-primary">ابدأ الآن</button>
                <button class="btn-secondary">تعرف أكثر</button>
            </div>
        </div>
        <div class="hero-visual">
            <div class="floating-card">
                <div class="card-icon">🚀</div>
                <div class="card-text">سرعة فائقة</div>
            </div>
            <div class="floating-card delay-1">
                <div class="card-icon">🛡️</div>
                <div class="card-text">أمان متقدم</div>
            </div>
            <div class="floating-card delay-2">
                <div class="card-icon">⚡</div>
                <div class="card-text">أداء عالي</div>
            </div>
        </div>
    </section>
""")
            elif section == "about":
                html_parts.append("""
    <section id="about" class="about">
        <div class="container">
            <h2 class="section-title">من نحن</h2>
            <div class="about-grid">
                <div class="about-card">
                    <div class="about-icon">🎯</div>
                    <h3>رؤيتنا</h3>
                    <p>بناء أقوى نظام بيئي رقمي في العالم العربي</p>
                </div>
                <div class="about-card">
                    <div class="about-icon">💡</div>
                    <h3>مهمتنا</h3>
                    <p>تمكين كل مطور عربي بأدوات الذكاء الاصطناعي</p>
                </div>
                <div class="about-card">
                    <div class="about-icon">🌍</div>
                    <h3>قيمنا</h3>
                    <p>الابتكار، الجودة، والتميز في كل شيء</p>
                </div>
            </div>
        </div>
    </section>
""")
            elif section == "features":
                html_parts.append("""
    <section id="services" class="features">
        <div class="container">
            <h2 class="section-title">خدماتنا</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">🤖</div>
                    <h3>ذكاء اصطناعي</h3>
                    <p>وكلاء ذكاء متخصصين لكل مهمة</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🎮</div>
                    <h3>تطوير ألعاب</h3>
                    <p>ألعاب HTML5 تفاعلية بجودة عالية</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🌐</div>
                    <h3>تصميم مواقع</h3>
                    <p>مواقع متجاوبة بأحدث التقنيات</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🎬</div>
                    <h3>توليد فيديو</h3>
                    <p>أفلام ومقاطع بالذكاء الاصطناعي</p>
                </div>
            </div>
        </div>
    </section>
""")
            elif section == "contact":
                html_parts.append("""
    <section id="contact" class="contact">
        <div class="container">
            <h2 class="section-title">تواصل معنا</h2>
            <form class="contact-form">
                <div class="form-group">
                    <input type="text" placeholder="الاسم" required>
                </div>
                <div class="form-group">
                    <input type="email" placeholder="البريد الإلكتروني" required>
                </div>
                <div class="form-group">
                    <textarea placeholder="رسالتك" rows="5" required></textarea>
                </div>
                <button type="submit" class="btn-primary">إرسال</button>
            </form>
        </div>
    </section>
""")

        html_parts.append("""
    <footer class="footer">
        <div class="footer-content">
            <p>🐺 بني بـ <span class="heart">❤️</span> في مصر</p>
            <p> Rafeeq Kernel v2.3.0</p>
        </div>
    </footer>
    <script src="script.js"></script>
</body>
</html>""")

        return "
".join(html_parts)

    def _generate_css(self, template_type, colors):
        primary = colors.get("primary", "#0ea5e9")
        secondary = colors.get("secondary", "#1e293b")
        accent = colors.get("accent", "#10b981")

        return f"""/* Rafeeq WebArchitect — {template_type} */
* {{margin:0;padding:0;box-sizing:border-box}}
body {{font-family:'Tajawal',sans-serif;background:{secondary};color:#e2e8f0;line-height:1.6;overflow-x:hidden}}
.container {{max-width:1200px;margin:0 auto;padding:0 24px}}

/* Navbar */
.navbar {{position:fixed;top:0;left:0;right:0;z-index:1000;background:rgba(15,23,42,0.9);backdrop-filter:blur(10px);padding:16px 24px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid rgba(148,163,184,0.1)}}
.nav-brand {{font-size:1.5rem;font-weight:900;background:linear-gradient(135deg,{primary},{accent});-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.nav-links {{display:flex;gap:32px}}
.nav-links a {{color:#94a3b8;text-decoration:none;font-weight:500;transition:color 0.3s}}
.nav-links a:hover {{color:{primary}}}

/* Hero */
.hero {{min-height:100vh;display:flex;align-items:center;justify-content:space-between;padding:120px 24px 60px;max-width:1200px;margin:0 auto;gap:60px}}
.hero-content {{flex:1}}
.hero-content h1 {{font-size:4rem;font-weight:900;margin-bottom:24px;background:linear-gradient(135deg,{primary},{accent});-webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1.2}}
.hero-content p {{font-size:1.25rem;color:#94a3b8;margin-bottom:40px}}
.hero-buttons {{display:flex;gap:16px}}
.btn-primary {{padding:16px 32px;background:linear-gradient(135deg,{primary},{accent});color:white;border:none;border-radius:12px;font-size:1.1rem;font-weight:600;cursor:pointer;transition:all 0.3s}}
.btn-primary:hover {{transform:translateY(-3px);box-shadow:0 20px 40px -10px rgba(14,165,233,0.4)}}
.btn-secondary {{padding:16px 32px;background:rgba(148,163,184,0.1);color:#e2e8f0;border:1px solid rgba(148,163,184,0.2);border-radius:12px;font-size:1.1rem;font-weight:600;cursor:pointer;transition:all 0.3s}}
.btn-secondary:hover {{background:rgba(148,163,184,0.2)}}

/* Hero Visual */
.hero-visual {{flex:1;display:flex;flex-direction:column;gap:20px;position:relative}}
.floating-card {{background:rgba(30,41,59,0.8);border:1px solid rgba(148,163,184,0.1);border-radius:16px;padding:24px;display:flex;align-items:center;gap:16px;animation:float 6s ease-in-out infinite;backdrop-filter:blur(10px)}}
.floating-card.delay-1 {{animation-delay:0.5s}}
.floating-card.delay-2 {{animation-delay:1s}}
.card-icon {{font-size:2.5rem}}
.card-text {{font-size:1.1rem;font-weight:600;color:#e2e8f0}}
@keyframes float {{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-20px)}}}}

/* Sections */
section {{padding:100px 0}}
.section-title {{font-size:2.5rem;font-weight:900;text-align:center;margin-bottom:60px;background:linear-gradient(135deg,{primary},{accent});-webkit-background-clip:text;-webkit-text-fill-color:transparent}}

/* About */
.about-grid {{display:grid;grid-template-columns:repeat(3,1fr);gap:32px}}
.about-card {{background:rgba(30,41,59,0.6);border:1px solid rgba(148,163,184,0.1);border-radius:16px;padding:40px;text-align:center;transition:all 0.3s}}
.about-card:hover {{transform:translateY(-10px);border-color:{primary}}}
.about-icon {{font-size:3rem;margin-bottom:20px}}
.about-card h3 {{font-size:1.5rem;margin-bottom:12px;color:#e2e8f0}}
.about-card p {{color:#94a3b8}}

/* Features */
.features-grid {{display:grid;grid-template-columns:repeat(4,1fr);gap:24px}}
.feature-card {{background:rgba(30,41,59,0.6);border:1px solid rgba(148,163,184,0.1);border-radius:16px;padding:32px;text-align:center;transition:all 0.3s}}
.feature-card:hover {{transform:translateY(-5px);border-color:{accent}}}
.feature-icon {{font-size:2.5rem;margin-bottom:16px}}
.feature-card h3 {{font-size:1.25rem;margin-bottom:8px;color:#e2e8f0}}
.feature-card p {{color:#94a3b8;font-size:0.95rem}}

/* Contact */
.contact-form {{max-width:600px;margin:0 auto;display:flex;flex-direction:column;gap:20px}}
.form-group input, .form-group textarea {{width:100%;padding:16px;background:rgba(30,41,59,0.6);border:1px solid rgba(148,163,184,0.2);border-radius:12px;color:#e2e8f0;font-size:1rem;font-family:inherit;transition:all 0.3s}}
.form-group input:focus, .form-group textarea:focus {{outline:none;border-color:{primary};box-shadow:0 0 0 3px rgba(14,165,233,0.1)}}
.form-group input::placeholder, .form-group textarea::placeholder {{color:#64748b}}

/* Footer */
.footer {{padding:40px 24px;text-align:center;border-top:1px solid rgba(148,163,184,0.1)}}
.footer-content p {{color:#94a3b8;margin:8px 0}}
.heart {{color:#ef4444;animation:pulse 1.5s ease-in-out infinite}}
@keyframes pulse {{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.2)}}}}

/* Responsive */
@media (max-width:768px) {{
    .hero {{flex-direction:column;text-align:center;padding-top:100px}}
    .hero-content h1 {{font-size:2.5rem}}
    .about-grid {{grid-template-columns:1fr}}
    .features-grid {{grid-template-columns:repeat(2,1fr)}}
    .nav-links {{display:none}}
}}
"""

    def _generate_js(self, template_type):
        return """// Rafeeq WebArchitect — Interactive Scripts
document.addEventListener('DOMContentLoaded', () => {
    // Smooth scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) target.scrollIntoView({ behavior: 'smooth' });
        });
    });

    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(15, 23, 42, 0.95)';
        } else {
            navbar.style.background = 'rgba(15, 23, 42, 0.9)';
        }
    });

    // Form handling
    const form = document.querySelector('.contact-form');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const btn = form.querySelector('button[type="submit"]');
            const originalText = btn.textContent;
            btn.textContent = 'جاري الإرسال...';
            btn.disabled = true;

            setTimeout(() => {
                btn.textContent = '✅ تم الإرسال!';
                btn.style.background = 'linear-gradient(135deg, #10b981, #0ea5e9)';
                form.reset();

                setTimeout(() => {
                    btn.textContent = originalText;
                    btn.style.background = '';
                    btn.disabled = false;
                }, 3000);
            }, 1500);
        });
    }

    // Intersection Observer for animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.about-card, .feature-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'all 0.6s ease';
        observer.observe(card);
    });
});
"""

    def list_websites(self):
        return self.generated_websites


web_architect = WebArchitect()
def get_web_architect():
    return web_architect
