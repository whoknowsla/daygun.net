You are an expert Software Architect and Senior Django Developer.
Your task is to generate a complete Django project with Docker for daygun.net, including:
• Blog system
• Ghost-style live markdown editor (TipTap)
• Newsletter / Subscription system
• Projects page
• About page
• Home page with short bio + last 3 blog posts
• Full multilingual support (TR + EN)
• Mobile-first responsive design
• Accessibility-focused UI (WCAG AA)
• Nginx host reverse proxy + Django+Postgres in Docker containers
• Production-ready secure architecture
No placeholders. Implement everything fully.
You must not ask questions.
Make reasonable design decisions and build the project entirely.

1) Tech Stack Requirements
ComponentTechnologyBackendDjango (LTS), Python 3.12+DatabasePostgreSQL (Docker)Web serverGunicorn inside DockerReverse proxyNginx on host (NOT a container)FrontendHTML + TailwindCSS (JIT mode)EditorTipTap + Markdown extensionEmailDjango SMTP via .envDeploymentdocker-compose up -d ready

2) Directory & Project Structure
daygun_site/
│── docker-compose.yml
│── Dockerfile
│── .env.example
│── README.md
│── requirements.txt
│── manage.py
│
├── daygun_site/                # Core settings
│   ├── settings/base.py
│   ├── settings/production.py
│   ├── __init__.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/
│   ├── blog/
│   ├── pages/
│   └── subscriptions/
│
├── static/
└── templates/


3) Internationalization (Critical)
Languages Required
LanguageCodeDefaultTurkishtrWhen browser detects TREnglishenFallback & default homepage
URL Style
/tr/                  → Homepage TR
/en/                  → Homepage EN
/tr/blog/             → Blog list TR
/en/blog/             → Blog list EN
/tr/blog/<slug>/      → Detail TR
/en/blog/<slug>/      → Detail EN

Homepage / → detect browser → redirect to /tr/ or /en/.
Templates must use language-aware fields:
Example:
post.title_tr / post.title_en
post.content_tr / post.content_en

Reader views automatically serve correct language variant.

4) Models & Features
A) Blog App – apps/blog
FieldTypetitle_tr / title_enCharFieldslugSlugField uniquesummary_tr / summary_enTextField optionalcontent_tr / content_enTextField (Markdown)is_publishedBooleanFieldpublished_atDateTimeFieldcreated_at / updated_atAuto timestamps
Rules


Markdown is sanitized → BLEACH REQUIRED


First time is_published changes to True → send newsletter emails


Emails must match subscriber language preference


Views
/tr/blog/                 → TR list
/en/blog/                 → EN list
/tr/blog/<slug>/          → TR detail
/en/blog/<slug>/          → EN detail


B) Pages App
Project Model
FieldTR/ENNotestitle_tr / title_en✓short_description_tr / _en✓description_tr / _en✓ Markdowngithub_urloptionallive_urloptionalis_featuredhomepage highlightordermanual sorting
Experience Model
Same dual-language structure.

Page Content Behavior
PageSourceHomeShort bio text + last 3 blog postsAboutExperience listProjectsProject model listBlogDynamic posts from Markdown
⚠ Home must ONLY show short about + latest 3 blog posts.

5) Subscription System – apps/subscriptions
Model:
email (unique)
language ('tr' or 'en')
is_active default=True
created_at timestamp

Behavior
✔ On subscribe:


If exists but inactive → reactivate


If new → create new subscriber


Store preferred language


✔ Newsletter sending logic:
If Post published:
  If subscriber.language == "tr" → send TR email template
  If subscriber.language == "en" → send EN email template

Must support ~1000+ subscribers.

6) Markdown Editor (Ghost-like)
Requirements
✔ TipTap + Markdown extension
✔ Live markdown preview within editor
✔ 2 editors side-by-side OR language tab switch (Recommended for accessibility)
✔ Stores raw markdown in database
Dashboard routes:
/dashboard/posts/
/dashboard/posts/new/
/dashboard/posts/<id>/edit/

Form fields:


title_tr, title_en


summary_tr, summary_en


content_tr, content_en (from TipTap → textarea sync)


slug


is_published checkbox


Accessibility Requirements


Editor must be screen-reader friendly


aria-label for TR & EN editors


"Press ctrl+shift+1 through 6 to insert heading" like shortcuts could be good for accessibility. You can also add other shortcuts as well.


JS file → static/js/editor.js.

7) Frontend / UI / Design System
General Design Principles
RequirementMustResponsiveMobile-first CSS → flex/grid layoutScreen Readerssemantic HTML + alt text + skip navigationColouraccessible contrast (AA)Typographyclean, readable, no tiny fontsLayoutcentered max-width content area
Visual Theme Guidelines


Clean developer-portfolio style


White theme default + easy dark-mode toggle ready


Headings large + clear hierarchy


Buttons accessible → visible focus ring


Components to Implement
Navbar (TR/EN switch)
Footer (Subscribe form)
Blog Card Component
Project Card Component
Layout wrapper


8) Docker + Deployment
Dockerfile
• Python slim base
• Install deps → copy code → collectstatic → run Gunicorn
• Use non-root user
docker-compose.yml
Services:
web:
  build: .
  env_file: .env
  expose: 8000
  restart: unless-stopped
  depends_on: db

db:
  image: postgres
  volumes:
    - pgdata:/var/lib/postgresql/data
  env_file: .env

Bind web on host:
127.0.0.1:8000


Nginx (Host Machine)
Create config nginx/daygun.conf:
server_name daygun.net www.daygun.net;

location / {
  proxy_pass http://127.0.0.1:8000;
}

README must include:
sudo ln -s /etc/nginx/sites-available/daygun.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx


9) README MUST TEACH USER HOW TO EDIT SITE
The README must contain human-friendly instructions:
📍 Change homepage text
📍 Add/edit projects
📍 Add/edit blog posts
📍 Where About page text lives
📍 How to edit languages separately
📍 How subscribers get TR/EN emails
📍 How to rebuild Docker
Example sections:
### How to edit About page
Open apps/pages/templates/pages/about.html
Modify {{ about_text_tr }} and {{ about_text_en }}

### Adding a new Project
1. Login admin
2. Create Project object
3. Fill Turkish & English fields

Must be crystal clear.

10) Final Output Requirements
AI must generate:


Complete Django codebase


All settings, urls, templates, static assets


Dockerfile + docker-compose.yml


.env.example with all variables


requirements.txt fully populated


TipTap editor integration


README.md fully documented


No TODO or placeholder comments — real implementation


You must deliver everything in one response.
Also, do all the tests before making it as production ready.
