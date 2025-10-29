# GitHub Repository Setup Guide

## Prepare Repository for Publishing

Follow these steps to publish your Foxess V2 HACS integration to GitHub:

### Step 1: Initialize Git Repository

```bash
cd /app
git init
git add .
git commit -m "Initial commit: Foxess V2 Home Assistant Integration"
```

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `foxess-v2-hacs` (or your preferred name)
3. Description: "Home Assistant custom component for Foxess V2 solar inverters"
4. Choose: **Public** (required for HACS)
5. **Do NOT** initialize with README (we already have one)
6. Click "Create repository"

### Step 3: Push to GitHub

```bash
# Replace with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/foxess-v2-hacs.git
git branch -M main
git push -u origin main
```

### Step 4: Update Repository URLs

After creating the repository, update these files with your actual GitHub URL:

1. **manifest.json**
   ```json
   "documentation": "https://github.com/YOUR_USERNAME/foxess-v2-hacs",
   "issue_tracker": "https://github.com/YOUR_USERNAME/foxess-v2-hacs/issues",
   ```

2. **README.md**
   - Update all GitHub links
   - Replace `yourusername` with your actual username

3. Commit the changes:
   ```bash
   git add .
   git commit -m "Update repository URLs"
   git push
   ```

### Step 5: Create a Release

1. Go to your repository on GitHub
2. Click "Releases" → "Create a new release"
3. Tag: `v1.0.0`
4. Release title: `v1.0.0 - Initial Release`
5. Description:
   ```markdown
   ## Foxess V2 Integration v1.0.0
   
   Initial release of the Home Assistant integration for Foxess V2 solar systems.
   
   ### Features
   - Username/password authentication
   - Real-time power monitoring
   - Daily energy statistics
   - 12 comprehensive sensors
   - HACS compatible
   
   ### Installation
   See [README.md](README.md) and [INSTALLATION.md](INSTALLATION.md)
   
   ### Known Issues
   - Authentication requires testing with live Foxess V2 accounts
   - May need adjustments based on actual API responses
   
   Please report issues and successes!
   ```
6. Click "Publish release"

### Step 6: Add to HACS (Optional - for wider distribution)

To make your integration discoverable in HACS:

1. Fork the HACS default repository: https://github.com/hacs/default
2. Add your repository to `custom_components.json`:
   ```json
   {
     "foxess_v2": {
       "name": "Foxess V2",
       "description": "Home Assistant integration for Foxess V2 solar inverters",
       "domain": "foxess_v2",
       "documentation": "https://github.com/YOUR_USERNAME/foxess-v2-hacs",
       "release_stage": "experimental"
     }
   }
   ```
3. Create a pull request

**Note**: HACS inclusion requires:
- ✅ Public GitHub repository
- ✅ At least one release
- ✅ Valid HACS metadata (hacs.json)
- ✅ Working integration (needs testing!)

### Step 7: Test Installation

Test the HACS custom repository method:

1. In Home Assistant, open HACS
2. Go to Integrations
3. Click ⋮ → Custom repositories
4. Add: `https://github.com/YOUR_USERNAME/foxess-v2-hacs`
5. Category: Integration
6. Install and test

### Step 8: Documentation

Create these additional files (optional but recommended):

1. **CONTRIBUTING.md** - Guidelines for contributors
2. **CHANGELOG.md** - Version history
3. **SECURITY.md** - Security policy
4. **.github/ISSUE_TEMPLATE/** - Issue templates
5. **.github/workflows/** - CI/CD automation

## Repository Structure Checklist

Before publishing, ensure you have:

- [x] `custom_components/foxess_v2/` - Integration files
- [x] `README.md` - Main documentation
- [x] `INSTALLATION.md` - Detailed setup guide
- [x] `LICENSE` - MIT License
- [x] `hacs.json` - HACS metadata
- [x] `.gitignore` - Git ignore rules
- [ ] GitHub repository created
- [ ] First release published
- [ ] URLs updated in manifest.json
- [ ] Tested installation via HACS

## Files to Update with Your Info

**Before publishing**, replace placeholders:

| File | Placeholder | Replace With |
|------|-------------|--------------|
| manifest.json | `@yourusername` | Your GitHub username |
| manifest.json | documentation URL | Your repo URL |
| README.md | `yourusername` | Your GitHub username |
| README.md | All GitHub links | Your repo links |

## Post-Publication

After publishing:

1. ✅ Test installation from HACS
2. ✅ Test with your Foxess V2 credentials
3. ✅ Document any issues found
4. ✅ Update README with actual test results
5. ✅ Create issues for known problems
6. ✅ Share in Home Assistant community

## Getting Help

If you need help:
- **HACS**: https://hacs.xyz/docs/publish/start
- **HA Integration**: https://developers.home-assistant.io/
- **Community**: https://community.home-assistant.io/

## Quick Checklist

```bash
# 1. Initialize git
git init
git add .
git commit -m "Initial commit"

# 2. Create GitHub repo (via web interface)

# 3. Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/foxess-v2-hacs.git
git push -u origin main

# 4. Update URLs in files
# (edit manifest.json and README.md)
git add .
git commit -m "Update repository URLs"
git push

# 5. Create release v1.0.0 (via web interface)

# 6. Test in HACS
```

## Next Steps

1. **Test Thoroughly**: The integration needs testing with real Foxess V2 accounts
2. **Fix Issues**: Update the API client based on actual responses
3. **Iterate**: Release new versions as you improve the integration
4. **Community**: Share with other Foxess users!

---

Good luck with your integration! 🚀