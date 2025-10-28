# GitHub Setup Guide

## ✅ Completed

1. ✅ Git repository initialized
2. ✅ All files committed with comprehensive commit message
3. ✅ CI badges added to README.md
4. ✅ .gitignore configured

## 📋 Next Steps

### Step 1: Create GitHub Repository

**Option A: Using GitHub CLI (Recommended)**

```bash
# If you have gh CLI installed
gh repo create flyberry_platform --public --source=. --remote=origin --push

# This will:
# - Create the GitHub repository
# - Set up the remote
# - Push all commits
# - Activate the CI workflow automatically
```

**Option B: Using GitHub Web Interface**

1. Go to https://github.com/new
2. Repository name: `flyberry_platform`
3. Description: "Unified, scalable platform for generating and validating the Flyberry brand framework"
4. Choose Public or Private
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

### Step 2: Add Remote and Push

After creating the repository on GitHub:

```bash
# Replace YOUR_USERNAME with your actual GitHub username
git remote add origin https://github.com/YOUR_USERNAME/flyberry_platform.git

# Or use SSH (if you have SSH keys set up)
git remote add origin git@github.com:YOUR_USERNAME/flyberry_platform.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Expected Output:**
```
Enumerating objects: 108, done.
Counting objects: 100% (108/108), done.
Delta compression using up to 8 threads
Compressing objects: 100% (95/95), done.
Writing objects: 100% (108/108), 1.2 MiB | 2.5 MiB/s, done.
Total 108 (delta 15), reused 0 (delta 0), pack-reused 0
To github.com:YOUR_USERNAME/flyberry_platform.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

### Step 3: Update README Badges

```bash
# Edit README.md and replace YOUR_USERNAME with your actual GitHub username
sed -i '' 's/YOUR_USERNAME/your-actual-username/g' README.md

# Or manually edit the file
# Change:
#   https://github.com/YOUR_USERNAME/flyberry_platform/...
# To:
#   https://github.com/your-actual-username/flyberry_platform/...

# Commit the change
git add README.md
git commit -m "docs: Update README badges with actual GitHub username"
git push origin main
```

### Step 4: Verify CI Workflow

1. Go to your repository on GitHub
2. Click the "Actions" tab
3. You should see the "Flyberry Platform CI" workflow
4. The workflow should trigger automatically on push
5. Wait for it to complete (~2-3 minutes)

**Expected CI Jobs:**
- ✅ Validate & Test Platform (Python 3.9, 3.10, 3.11)
- ✅ Lint & Format Check
- ✅ Security Scan

### Step 5: Set Up Branch Protection

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Branches**
3. Click **Add branch protection rule**
4. Branch name pattern: `main`
5. Enable the following:
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
     - Search and select: `Validate & Test Platform (3.9)`
     - Search and select: `Validate & Test Platform (3.10)`
     - Search and select: `Validate & Test Platform (3.11)`
   - ✅ Require branches to be up to date before merging
   - ✅ Do not allow bypassing the above settings
6. Click **Create**

**Result:** All pull requests must pass CI before merging.

### Step 6: Test the CI Workflow

Create a test branch and PR:

```bash
# Create a test branch
git checkout -b test/ci-workflow

# Make a small change
echo "# CI Test" >> GITHUB_SETUP.md

# Commit and push
git add GITHUB_SETUP.md
git commit -m "test: Verify CI workflow on PR"
git push origin test/ci-workflow

# Create a pull request using gh CLI
gh pr create --title "Test: Verify CI workflow" --body "Testing the CI workflow on pull requests"

# Or create PR manually on GitHub
# Go to: https://github.com/YOUR_USERNAME/flyberry_platform/pulls
# Click "New pull request"
```

**What to Expect:**
1. CI workflow will trigger automatically
2. You'll see status checks on the PR
3. If gates fail, you'll see an automated comment
4. Reports will be uploaded as artifacts

### Step 7: Add CI Status Badge (Final)

Once the first CI run completes:

1. Go to Actions tab on GitHub
2. Click on "Flyberry Platform CI" workflow
3. Click the "..." menu → "Create status badge"
4. Copy the markdown
5. Replace the existing badge in README.md

**Or use this format:**
```markdown
[![CI Status](https://github.com/YOUR_USERNAME/flyberry_platform/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/flyberry_platform/actions)
```

## 🔐 Optional: Set Up Secrets

If you want to add notifications or integrations:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add secrets like:
   - `SLACK_WEBHOOK_URL` (for Slack notifications)
   - `DISCORD_WEBHOOK_URL` (for Discord notifications)
   - `CODECOV_TOKEN` (for code coverage)

## 📊 Verify Everything Works

```bash
# Check remote
git remote -v
# Should show: origin https://github.com/YOUR_USERNAME/flyberry_platform.git

# Check current branch
git branch
# Should show: * main

# Pull latest (should be up to date)
git pull origin main

# Check CI status (if gh CLI installed)
gh workflow list
gh run list --workflow="Flyberry Platform CI"
```

## 🎉 Success Checklist

- [ ] GitHub repository created
- [ ] Remote added and code pushed
- [ ] README badges updated with actual username
- [ ] CI workflow triggered and passed
- [ ] Branch protection enabled
- [ ] Test PR created and verified
- [ ] CI status badge shows "passing"

## 🚨 Troubleshooting

### Issue: CI workflow not triggering

**Solution:**
1. Check `.github/workflows/ci.yml` exists in the repository
2. Verify the workflow file has correct YAML syntax
3. Check Actions tab → Workflows → Make sure workflow is not disabled

### Issue: CI failing on specific Python version

**Solution:**
1. Check the Actions tab for detailed logs
2. Look for the specific step that failed
3. Common issues:
   - Missing dependencies (check requirements.txt)
   - Python version compatibility (update code or remove that version from matrix)
   - File paths (ensure paths are relative to repo root)

### Issue: Gates always failing

**Solution:**
This is expected if you have failing checks in your fixtures. To fix:
1. Review the gate definitions in specs/*.yml
2. Check the actual metric values in product/runs/*/run.json
3. Adjust gate thresholds or fix the underlying issues

### Issue: Can't push to GitHub (authentication error)

**Solution:**
```bash
# Option 1: Use Personal Access Token (PAT)
# Create PAT at: https://github.com/settings/tokens
# Use PAT as password when prompted

# Option 2: Set up SSH keys
ssh-keygen -t ed25519 -C "your_email@example.com"
# Add key to GitHub: https://github.com/settings/keys

# Option 3: Use gh CLI (recommended)
gh auth login
```

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Branch Protection Rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches)
- [GitHub CLI](https://cli.github.com/)
- [Creating Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

## 🎯 Next Steps After Setup

1. **Configure notifications:**
   - Set up Slack/Discord webhooks
   - Enable email notifications for CI failures

2. **Add more CI checks:**
   - Code coverage reporting (codecov, coveralls)
   - Dependency vulnerability scanning
   - Performance benchmarks

3. **Create templates:**
   - PR template (.github/pull_request_template.md)
   - Issue templates (.github/ISSUE_TEMPLATE/)
   - Contributing guide (CONTRIBUTING.md)

4. **Set up automated releases:**
   - Semantic versioning
   - Automated changelogs
   - GitHub Releases

## ✅ You're Done!

Your platform is now fully integrated with GitHub and has:
- ✅ Automated CI/CD pipeline
- ✅ Multi-Python version testing
- ✅ Security scanning
- ✅ Automated quality gates
- ✅ Branch protection
- ✅ Status badges

Happy coding! 🚀
