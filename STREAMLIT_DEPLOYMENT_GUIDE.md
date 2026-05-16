# Streamlit Cloud Deployment Guide

## Prerequisites
- GitHub account
- Streamlit Cloud account (free at https://streamlit.io/cloud)
- Supabase database (already set up)

## Step 1: Prepare Your Repository

### 1.1 Check Required Files
Ensure these files exist in your repository:
- ✅ `app.py` - Main application file
- ✅ `requirements.txt` - Python dependencies
- ✅ `.streamlit/config.toml` - Streamlit configuration
- ✅ `.gitignore` - Excludes sensitive files
- ✅ `README.md` - Project documentation

### 1.2 Clean Up Debug Files (Optional)
Remove test/debug files before deployment:
```bash
# These files are not needed in production
rm test_pdf.py
rm debug_pdf_structure.py
rm debug_pdf_detailed.py
rm debug_customer_detection.py
rm validate_parser.py
rm clear_database.py
rm clear_sales_data.py
```

Or keep them but add to .gitignore if you want them locally only.

## Step 2: Push to GitHub

### 2.1 Initialize Git (if not already done)
```bash
git init
git add .
git commit -m "Fixed PDF parser - now captures all voucher types"
```

### 2.2 Create GitHub Repository
1. Go to https://github.com/new
2. Create a new repository (e.g., "sales-intelligence-ai")
3. Don't initialize with README (you already have one)

### 2.3 Push Your Code
```bash
git remote add origin https://github.com/YOUR_USERNAME/sales-intelligence-ai.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy to Streamlit Cloud

### 3.1 Sign Up / Log In
1. Go to https://streamlit.io/cloud
2. Sign in with your GitHub account
3. Authorize Streamlit to access your repositories

### 3.2 Create New App
1. Click "New app" button
2. Select your repository: `YOUR_USERNAME/sales-intelligence-ai`
3. Select branch: `main`
4. Main file path: `app.py`
5. Click "Advanced settings"

### 3.3 Configure Secrets
In the "Secrets" section, add your environment variables:

```toml
# Database Configuration
DB_HOST = "your-supabase-host.supabase.co"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "your-database-password"
DB_PORT = "5432"

# Supabase Configuration
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key"

# Security
SECRET_KEY = "your-secret-key-for-sessions"

# Optional: Email Configuration (if using)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = "587"
SMTP_USERNAME = "your-email@gmail.com"
SMTP_PASSWORD = "your-app-password"
```

**Important:** Get these values from:
- Supabase Dashboard → Settings → Database
- Supabase Dashboard → Settings → API

### 3.4 Deploy
1. Click "Deploy!"
2. Wait for deployment (usually 2-5 minutes)
3. Your app will be available at: `https://your-app-name.streamlit.app`

## Step 4: Verify Deployment

### 4.1 Test the App
1. Visit your deployed URL
2. Sign up for a new account
3. Upload a PDF file
4. Verify:
   - ✅ Multiple customers appear (not just BERA COMPLEX)
   - ✅ Both B1 and ROUGH ESTIMATE voucher types
   - ✅ Category "Unknown" < 10%
   - ✅ Correct revenue calculations

### 4.2 Check Logs
If issues occur:
1. Click "Manage app" in Streamlit Cloud
2. View logs for error messages
3. Common issues:
   - Missing secrets → Add them in Advanced settings
   - Database connection → Check Supabase credentials
   - Package errors → Update requirements.txt

## Step 5: Update Deployment

### 5.1 Make Changes Locally
```bash
# Edit files
git add .
git commit -m "Description of changes"
git push
```

### 5.2 Auto-Deploy
Streamlit Cloud automatically redeploys when you push to GitHub!

## Troubleshooting

### Issue: "Module not found"
**Solution:** Add missing package to `requirements.txt`

### Issue: "Database connection failed"
**Solution:** 
1. Check secrets are correctly set
2. Verify Supabase database is running
3. Check IP allowlist in Supabase (allow all IPs for Streamlit Cloud)

### Issue: "App is slow"
**Solution:**
1. Streamlit Cloud free tier has limited resources
2. Consider upgrading to paid tier
3. Optimize database queries
4. Add caching with `@st.cache_data`

### Issue: "PDF parsing fails"
**Solution:**
1. Check PDF file format matches expected structure
2. View logs for specific error messages
3. Test locally first with `streamlit run app.py`

## Security Best Practices

### ✅ DO:
- Use Streamlit secrets for sensitive data
- Keep `.env` in `.gitignore`
- Use environment variables for all credentials
- Enable Supabase Row Level Security (RLS)
- Use HTTPS (automatic with Streamlit Cloud)

### ❌ DON'T:
- Commit `.env` file to GitHub
- Hardcode passwords in code
- Share your secrets publicly
- Disable authentication

## Monitoring

### Check App Health
1. Streamlit Cloud Dashboard → Your App
2. View metrics:
   - Active users
   - Resource usage
   - Error rate
   - Response time

### View Logs
```bash
# In Streamlit Cloud dashboard
Manage app → Logs
```

### Database Monitoring
1. Supabase Dashboard → Database
2. Check:
   - Connection count
   - Query performance
   - Storage usage

## Updating the Parser

If you need to update the parser logic:

1. **Test locally first:**
   ```bash
   python validate_parser.py
   ```

2. **Commit and push:**
   ```bash
   git add parser.py
   git commit -m "Updated parser logic"
   git push
   ```

3. **Streamlit auto-deploys** - no manual action needed!

4. **Clear old data** (if needed):
   - Users can re-upload files
   - Or run `clear_database.py` locally to clear production DB

## Cost Considerations

### Streamlit Cloud Free Tier:
- ✅ 1 private app
- ✅ Unlimited public apps
- ✅ Community support
- ⚠️ Limited resources (1 GB RAM)
- ⚠️ App sleeps after inactivity

### Streamlit Cloud Pro ($20/month):
- ✅ More resources (4 GB RAM)
- ✅ No sleeping
- ✅ Priority support
- ✅ Custom domains

### Supabase Free Tier:
- ✅ 500 MB database
- ✅ 2 GB bandwidth
- ✅ 50,000 monthly active users
- ⚠️ Pauses after 1 week inactivity

## Support

### Resources:
- Streamlit Docs: https://docs.streamlit.io
- Streamlit Community: https://discuss.streamlit.io
- Supabase Docs: https://supabase.com/docs
- GitHub Issues: Create issues in your repository

### Getting Help:
1. Check logs first
2. Search Streamlit Community forum
3. Review this deployment guide
4. Check `PARSER_FIX_DOCUMENTATION.md` for parser issues

---

## Quick Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Streamlit Cloud account created
- [ ] App created in Streamlit Cloud
- [ ] Secrets configured (database, Supabase, etc.)
- [ ] App deployed successfully
- [ ] Test upload works
- [ ] Multiple customers appear
- [ ] Both voucher types captured
- [ ] Categories classified correctly
- [ ] Revenue calculations accurate

**Your app is now live! 🎉**

Share your URL: `https://your-app-name.streamlit.app`