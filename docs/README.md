# TerminalOS Documentation

This folder contains the GitHub Pages documentation for TerminalOS.

## Structure

```
docs/
├── _config.yml           # Jekyll configuration
├── index.md              # Homepage
├── assets/
│   └── style.css         # Custom CSS styling
└── pages/
    ├── quick-start.md    # Installation & first steps
    ├── architecture.md   # Module system deep dive
    ├── api-reference.md  # Complete API documentation
    └── development.md    # Building new features
```

## Building Locally

### Prerequisites

- Ruby 3.1+
- Bundler

### Setup

```bash
cd docs
bundle install
bundle exec jekyll serve
```

Visit `http://localhost:4000` to preview the site.

## Deployment

GitHub Actions automatically deploys the documentation to GitHub Pages when you push to `main` or `master`.

The workflow file is at `.github/workflows/pages.yml`.

### Manual Deployment

1. Push changes to `main` or `master` branch
2. GitHub Actions will build and deploy automatically
3. Site will be available at `https://username.github.io/TerminalOS`

## Editing Content

Each `.md` file is a separate page:

- **index.md** - Homepage/overview
- **pages/quick-start.md** - Getting started
- **pages/architecture.md** - Technical architecture
- **pages/api-reference.md** - API documentation
- **pages/development.md** - Development guide

Edit these files and commit to automatically update the site.

## Navigation

The `_config.yml` file controls the site theme and plugins. Update it if you need to:
- Change the theme
- Add plugins
- Update site metadata

## Styling

Custom CSS is in `assets/style.css`. Modify it to change:
- Colors
- Typography
- Layouts
- Responsive design

## GitHub Pages Setup

To enable GitHub Pages in your repository:

1. Go to Settings → Pages
2. Under "Build and deployment":
   - Source: Deploy from a branch
   - Branch: Select `main` or `master`
   - Folder: Select `/docs`
3. Click Save

Your site will be available at:
```
https://[username].github.io/TerminalOS
```

## Tips

- Use clear, concise language
- Include code examples
- Link between related pages
- Keep formatting consistent
- Test links locally before deploying
- Use headings for organization
- Include tables for reference material

## Support

For issues with the documentation:
1. Check the [GitHub Issues](https://github.com/NatBuilds/TerminalOS/issues)
2. Create a new issue with suggestions
3. Submit pull requests with improvements

