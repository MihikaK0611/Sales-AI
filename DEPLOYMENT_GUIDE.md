# Deployment Guide - Sales Intelligence AI

## Streamlit Cloud Deployment (Free Tier)

This guide will help you deploy the Sales Intelligence AI application on Streamlit Cloud's free tier.

---

## Prerequisites

Before deploying, ensure you have:

1. ✅ A GitHub account
2. ✅ A Supabase account (free tier)
3. ✅ Your code pushed to a GitHub repository
4. ✅ All environment variables ready

---

## Step 1: Prepare Your Supabase Database

### 1.1 Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign up or log in
3. Click **"New Project"**
4. Fill in project details:
   - Name: `sales-intelligence-ai`
   - Database Password: (create a strong password)
   - Region: Choose closest to your users
5. Wait for project to be created (2-3 minutes)

### 1.2 Run Database Migration

1. In Supabase dashboard, go to **SQL Editor**
2. Click **"New Query"**
3. Copy the contents of `migrations/001_schema_update.sql`
4. Paste into the SQL editor
5. Click **"Run"**
6. Verify tables were created successfully

### 1.3 Enable Row Level Security

The migration script already enables RLS, but verify:

1. Go to **Authentication** → **Policies**
2. Check that policies exist for `sales_data` and `file_metadata` tables
3. Ensure RLS is enabled on both tables

### 1.4 Configure Storage

1. Go to **Storage** in Supabase dashboard
2. Create a new bucket named `sales_pdfs`
3. Set bucket to **Public** (for file access)
4. Configure CORS if needed

### 1.5 Get Your Credentials

1. Go to **Settings** → **API**
2. Copy the following:
   - **Project URL** (SUPABASE_URL)
   - **anon/public key** (SUPABASE_KEY)
   - **service_role key** (SUPABASE_SERVICE_KEY)
3. Go to **Settings** → **Database**
4. Copy **Connection String** (DB_URL)
   - Choose "URI" format
   - Replace `[YOUR-PASSWORD]` with your database password

---

## Step 2: Prepare GitHub Repository

### 2.1 Push Code to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Sales Intelligence AI"

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/sales-intelligence-ai.git

# Push to GitHub
git push -u origin main
```

### 2.2 Verify Required Files

Ensure these files are in your repository:

- ✅ `app.py` (main application)
- ✅ `requirements.txt` (dependencies)
- ✅ `.streamlit/config.toml` (Streamlit configuration)
- ✅ All Python modules (auth.py, database.py, parser.py, etc.)
- ✅ `pages/` directory with authentication pages
- ✅ `.gitignore` (to exclude .env file)

**Important:** Do NOT commit `.env` file with credentials!

---

## Step 3: Deploy on Streamlit Cloud

### 3.1 Sign Up for Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Authorize Streamlit to access your repositories

### 3.2 Create New App

1. Click **"New app"**
2. Select your repository: `YOUR_USERNAME/sales-intelligence-ai`
3. Choose branch: `main`
4. Main file path: `app.py`
5. Click **"Advanced settings"**

### 3.3 Configure Environment Variables

In the **Advanced settings** → **Secrets** section, add:

```toml
# Supabase Configuration
SUPABASE_URL = "your_supabase_url_here"
SUPABASE_KEY = "your_supabase_anon_key_here"
SUPABASE_SERVICE_KEY = "your_supabase_service_key_here"

# Database Configuration
DB_URL = "your_postgresql_connection_string_here"

# Application Configuration
APP_SECRET_KEY = "generate_a_random_secret_key_here"
ENVIRONMENT = "production"
```

**To generate APP_SECRET_KEY:**
```python
import secrets
print(secrets.token_hex(32))
```

### 3.4 Deploy

1. Click **"Deploy!"**
2. Wait for deployment (5-10 minutes first time)
3. Monitor the deployment logs for any errors

---

## Step 4: Post-Deployment Configuration

### 4.1 Test Authentication

1. Open your deployed app URL
2. Try creating a new account
3. Check email for verification link
4. Test login functionality

### 4.2 Test File Upload

1. Log in to your account
2. Upload a sample PDF/Excel file
3. Verify data extraction works
4. Check dashboard displays correctly

### 4.3 Verify Database Connection

1. Upload some test data
2. Check Supabase dashboard → **Table Editor**
3. Verify records appear in `sales_data` table
4. Confirm `user_id` is correctly set

---

## Step 5: Configure Custom Domain (Optional)

### 5.1 Streamlit Cloud Custom Domain

1. In Streamlit Cloud dashboard, go to app settings
2. Click **"Custom domain"**
3. Follow instructions to add your domain
4. Update DNS records as instructed

---

## Troubleshooting

### Common Issues

#### ❌ "Module not found" Error

**Solution:**
- Check `requirements.txt` includes all dependencies
- Verify package names are correct
- Try redeploying the app

#### ❌ "Database connection failed"

**Solution:**
- Verify DB_URL is correct in secrets
- Check Supabase project is active
- Ensure connection string includes password
- Verify SSL mode is set to `require`

#### ❌ "Authentication not working"

**Solution:**
- Check SUPABASE_URL and SUPABASE_KEY are correct
- Verify email confirmation is enabled in Supabase
- Check Supabase Auth settings

#### ❌ "File upload fails"

**Solution:**
- Verify storage bucket `sales_pdfs` exists
- Check bucket permissions (should be public)
- Ensure SUPABASE_KEY has storage access

#### ❌ "App is slow or times out"

**Solution:**
- Streamlit Cloud free tier has resource limits
- Optimize large file processing
- Consider upgrading to paid tier for better performance
- Reduce concurrent file uploads

---

## Streamlit Cloud Free Tier Limitations

Be aware of these limitations:

- **Resources:** 1 GB RAM, shared CPU
- **Sleep Mode:** App sleeps after inactivity (wakes on access)
- **Bandwidth:** Limited monthly bandwidth
- **Storage:** Limited to Supabase storage
- **Concurrent Users:** Limited simultaneous users

### Optimization Tips

1. **Reduce Dependencies:**
   - Only include necessary packages
   - Use lightweight alternatives where possible

2. **Optimize File Processing:**
   - Process files in batches
   - Add file size limits
   - Use efficient parsing methods

3. **Cache Data:**
   - Use `@st.cache_data` for expensive operations
   - Cache database queries when appropriate

4. **Minimize API Calls:**
   - Batch database operations
   - Reduce unnecessary queries

---

## Monitoring and Maintenance

### Monitor App Health

1. **Streamlit Cloud Dashboard:**
   - Check app status
   - View deployment logs
   - Monitor resource usage

2. **Supabase Dashboard:**
   - Monitor database size
   - Check API usage
   - Review authentication logs

### Regular Maintenance

- **Weekly:** Check error logs
- **Monthly:** Review database size and optimize
- **Quarterly:** Update dependencies in requirements.txt
- **As Needed:** Apply security patches

---

## Updating Your App

### Deploy Updates

1. Make changes to your code locally
2. Test thoroughly
3. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin main
   ```
4. Streamlit Cloud auto-deploys from GitHub
5. Monitor deployment logs

### Rollback if Needed

1. In Streamlit Cloud, go to app settings
2. Click **"Reboot app"** to restart
3. Or revert GitHub commit and redeploy

---

## Security Best Practices

### Production Checklist

- ✅ All secrets stored in Streamlit Cloud secrets (not in code)
- ✅ `.env` file in `.gitignore`
- ✅ Row Level Security enabled in Supabase
- ✅ HTTPS enabled (automatic with Streamlit Cloud)
- ✅ Strong passwords enforced
- ✅ Email verification enabled
- ✅ Regular security updates

### Ongoing Security

1. **Monitor Access:**
   - Review Supabase auth logs
   - Check for suspicious activity

2. **Update Dependencies:**
   - Keep packages up to date
   - Apply security patches promptly

3. **Backup Data:**
   - Regular Supabase backups
   - Export important data periodically

---

## Cost Considerations

### Free Tier Costs

- **Streamlit Cloud:** Free (with limitations)
- **Supabase:** Free tier includes:
  - 500 MB database
  - 1 GB file storage
  - 50,000 monthly active users
  - 2 GB bandwidth

### When to Upgrade

Consider upgrading if you need:
- More resources (RAM, CPU)
- No sleep mode
- Higher bandwidth
- More database storage
- Priority support

---

## Support and Resources

### Documentation

- [Streamlit Docs](https://docs.streamlit.io)
- [Supabase Docs](https://supabase.com/docs)
- [Application User Manual](USER_MANUAL.md)

### Community

- Streamlit Community Forum
- Supabase Discord
- GitHub Issues

---

## Conclusion

Your Sales Intelligence AI application is now deployed and ready to use!

**Next Steps:**
1. Share the app URL with users
2. Provide them with the User Manual
3. Monitor usage and performance
4. Gather feedback for improvements

**App URL Format:**
`https://your-app-name.streamlit.app`

---

**Version:** 1.0  
**Last Updated:** May 2026  
**Deployment Platform:** Streamlit Cloud (Free Tier)