# daygun.net - Personal Blog & Portfolio

A fully-featured Django blog and portfolio site with multilingual support (Turkish & English), live markdown editor, newsletter system, and Docker deployment.

## 🌟 Features

- **Multilingual Support**: Full Turkish (TR) and English (EN) content
- **Live Markdown Editor**: Ghost-style editor powered by TipTap
- **Newsletter System**: Email subscribers when new posts are published
- **Blog System**: Publish articles with markdown support
- **Projects Portfolio**: Showcase your work
- **About/Experience Pages**: Tell your story
- **Mobile-First Design**: Responsive and accessible (WCAG AA)
- **Production-Ready**: Docker + PostgreSQL + Nginx

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- (Optional) Domain name configured

### Installation

1. **Clone and Setup**
```bash
cd /home/sun/Documents/Projects/daygun.net
cp .env.example .env
```

2. **Configure Environment**
Edit `.env` with your settings:
```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=daygun.net,www.daygun.net,localhost
POSTGRES_PASSWORD=your-secure-password
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

3. **Build and Run**
```bash
docker-compose up -d --build
```

4. **Initialize Database**
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --noinput
```

5. **Access the Site**
- Main site: http://localhost:8000/
- Admin panel: http://localhost:8000/admin/
- Dashboard: http://localhost:8000/dashboard/posts/

## 📝 How to Edit Your Site

### Change Homepage Bio

1. Login to admin: http://localhost:8000/admin/
2. Go to **Pages** → **About Contents**
3. Edit "About Page Content"
4. Fill in both Turkish (`bio_short_tr`) and English (`bio_short_en`) fields
5. Save

The short bio appears on the homepage. The full bio appears on the About page.

### Add/Edit Blog Posts

#### Using the Dashboard (Recommended)

1. Go to http://localhost:8000/dashboard/posts/
2. Click "Create New Post"
3. Fill in:
   - **Title (English)**: Your post title in English
   - **Title (Turkish)**: Your post title in Turkish
   - **Slug**: URL-friendly version (auto-generated from English title)
   - **Summary (optional)**: Brief description
   - **Content**: Use the markdown editor with live preview

4. **Editor Tips**:
   - Switch between EN/TR tabs to edit different languages
   - Use toolbar buttons or keyboard shortcuts:
     - `Ctrl+B`: Bold
     - `Ctrl+I`: Italic
     - `Ctrl+Shift+1-6`: Headings H1-H6
     - `Ctrl+Shift+8`: Bullet list
     - `Ctrl+Shift+7`: Numbered list

5. Check "Publish this post" to make it live (sends newsletter!)
6. Click "Create Post"

#### Using Django Admin

1. Go to http://localhost:8000/admin/
2. Navigate to **Blog** → **Blog Posts**
3. Click "Add Blog Post"
4. Fill in Turkish and English content
5. Set `is_published` to True to publish

### Add/Edit Projects

1. Login to admin: http://localhost:8000/admin/
2. Go to **Pages** → **Projects**
3. Click "Add Project"
4. Fill in:
   - **Turkish Content**: Title, short description, full description
   - **English Content**: Same fields in English
   - **GitHub URL**: Link to code repository (optional)
   - **Live URL**: Link to live demo (optional)
   - **Featured**: Check to highlight on projects page
   - **Order**: Lower numbers appear first

5. Click "Save"

### Edit About Page

#### Change Bio Text

1. Admin → **Pages** → **About Contents**
2. Edit `bio_full_tr` and `bio_full_en`
3. Save

#### Add Work Experience

1. Admin → **Pages** → **Experiences**
2. Click "Add Experience"
3. Fill in:
   - Position title (TR/EN)
   - Company name (TR/EN)
   - Description (TR/EN)
   - Start date and end date
   - Check "Current Position" if still working there
4. Save

Experiences are displayed in reverse chronological order on the About page.

### Manage Newsletter Subscribers

1. Admin → **Subscriptions** → **Subscribers**
2. View all subscribers with their language preferences
3. Activate/deactivate subscribers using bulk actions

**Important**: When you publish a new blog post (check "is_published"), the newsletter is **automatically sent** to all active subscribers in their preferred language (TR or EN).

## 🌐 Nginx Configuration (Production)

### Setup Nginx on Host Machine

1. **Copy config to Nginx**
```bash
sudo cp nginx/daygun.conf /etc/nginx/sites-available/daygun.conf
sudo ln -s /etc/nginx/sites-available/daygun.conf /etc/nginx/sites-enabled/
```

2. **Update static files path in config**
Edit `/etc/nginx/sites-available/daygun.conf` and update the static files path to match your actual deployment path.

3. **Test and reload**
```bash
sudo nginx -t
sudo systemctl reload nginx
```

### Setup SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d daygun.net -d www.daygun.net
```

After SSL setup, uncomment the HTTPS server block in the Nginx config.

## 🔄 Rebuilding After Changes

### Code Changes

```bash
docker-compose down
docker-compose up -d --build
```

### Database Changes (Migrations)

```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### Static Files Changes

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

## 📧 Email Configuration

The site uses Django's email backend for sending newsletters.

### Gmail Setup (Recommended for testing)

1. Enable 2-factor authentication on your Google account
2. Generate an "App Password": https://myaccount.google.com/apppasswords
3. Update `.env`:
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password-here
DEFAULT_FROM_EMAIL=noreply@daygun.net
```

### Other SMTP Providers

Update `.env` with your provider's SMTP settings:
- **Mailgun**: smtp.mailgun.org
- **SendGrid**: smtp.sendgrid.net
- **AWS SES**: email-smtp.region.amazonaws.com

## 🗂️ Project Structure

```
daygun.net/
├── apps/
│   ├── blog/              # Blog posts with markdown
│   ├── pages/             # Static pages (home, about, projects)
│   └── subscriptions/     # Newsletter system
├── daygun_site/           # Django settings
│   └── settings/
│       ├── base.py        # Base configuration
│       └── production.py  # Production overrides
├── templates/             # HTML templates
│   ├── base/
│   ├── blog/
│   ├── pages/
│   └── subscriptions/
├── static/                # CSS, JS, images
│   ├── css/
│   └── js/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env
```

## 🌍 How Multilingual Works

### URL Structure

- `/` → Redirects based on browser language
- `/en/` → English homepage
- `/tr/` → Turkish homepage
- `/en/blog/` → English blog list
- `/tr/blog/` → Turkish blog list
- `/en/blog/my-post/` → English post detail
- `/tr/blog/my-post/` → Turkish post detail

### Database Fields

All content models have dual fields:
- `title_en` / `title_tr`
- `content_en` / `content_tr`
- `description_en` / `description_tr`

When a user visits `/en/blog/post-slug/`, the English fields are displayed. When visiting `/tr/blog/post-slug/`, Turkish fields are shown.

### Newsletter Language

When users subscribe, their language preference is saved (based on which language page they subscribed from). When a new post is published:

- Turkish subscribers get email with `title_tr` and `content_tr`
- English subscribers get email with `title_en` and `content_en`

## 🧪 Testing Before Production

### Test Locally

```bash
# Check all services are running
docker-compose ps

# View logs
docker-compose logs -f web

# Test email sending (console backend for development)
docker-compose exec web python manage.py shell
>>> from apps.subscriptions.models import Subscriber
>>> Subscriber.subscribe('test@example.com', 'en')
```

### Create Test Data

```bash
docker-compose exec web python manage.py shell
```

```python
from apps.pages.models import AboutContent, Project
from apps.blog.models import BlogPost

# Create about content
about = AboutContent.objects.create(
    bio_short_en="Hi, I'm a developer",
    bio_short_tr="Merhaba, ben bir yazılımcıyım",
    bio_full_en="Full bio in English...",
    bio_full_tr="Türkçe tam biyografi..."
)

# Create a project
project = Project.objects.create(
    title_en="My Project",
    title_tr="Projem",
    short_description_en="A cool project",
    short_description_tr="Harika bir proje",
    description_en="<p>Full description</p>",
    description_tr="<p>Tam açıklama</p>",
    github_url="https://github.com/user/repo",
    is_featured=True
)

# Create a blog post
post = BlogPost.objects.create(
    title_en="My First Post",
    title_tr="İlk Yazım",
    slug="my-first-post",
    content_en="<p>Post content in English</p>",
    content_tr="<p>Türkçe yazı içeriği</p>",
    is_published=False  # Set True to send newsletter
)
```

## 🔒 Security Checklist

Before deploying to production:

- [ ] Change `SECRET_KEY` in `.env`
- [ ] Set `DEBUG=False`
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Change `POSTGRES_PASSWORD`
- [ ] Setup real email credentials
- [ ] Enable HTTPS in Nginx config
- [ ] Setup SSL certificate with certbot
- [ ] Review firewall rules (open ports 80, 443)

## 📊 Maintenance

### Backup Database

```bash
docker-compose exec db pg_dump -U daygun_user daygun_db > backup_$(date +%Y%m%d).sql
```

### Restore Database

```bash
cat backup_20240101.sql | docker-compose exec -T db psql -U daygun_user daygun_db
```

### View Logs

```bash
docker-compose logs -f web
docker-compose logs -f db
```

### Update Dependencies

```bash
# Update requirements.txt, then:
docker-compose down
docker-compose up -d --build
```

## 🐛 Troubleshooting

### Site not loading

```bash
# Check if containers are running
docker-compose ps

# Check logs
docker-compose logs web

# Restart
docker-compose restart
```

### Static files not loading

```bash
docker-compose exec web python manage.py collectstatic --noinput
sudo systemctl reload nginx
```

### Database connection errors

```bash
# Check database is healthy
docker-compose logs db

# Run migrations
docker-compose exec web python manage.py migrate
```

### Newsletter not sending

- Check email credentials in `.env`
- View logs: `docker-compose logs web`
- Test SMTP connection separately
- For Gmail: ensure App Password is used (not account password)

## 📚 Additional Resources

- Django Documentation: https://docs.djangoproject.com/
- TipTap Editor: https://tiptap.dev/
- Docker Compose: https://docs.docker.com/compose/
- Nginx: https://nginx.org/en/docs/

## 📄 License

This project is open source and available for personal use.

---

**Need help?** Check the Django admin logs or Docker logs for detailed error messages.
