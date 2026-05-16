# 🚀 Quick Start Guide - Sales Intelligence AI

## Running the Application Locally

Follow these simple steps to run the application on your computer:

---

## Step 1: Set Up Supabase (5 minutes)

### 1.1 Create Supabase Account
1. Go to [supabase.com](https://supabase.com)
2. Click **"Start your project"**
3. Sign up with GitHub or email

### 1.2 Create New Project
1. Click **"New Project"**
2. Fill in:
   - **Name**: `sales-ai`
   - **Database Password**: Create a strong password (save it!)
   - **Region**: Choose closest to you
3. Click **"Create new project"**
4. Wait 2-3 minutes for setup

### 1.3 Run Database Migration
1. In Supabase dashboard, click **"SQL Editor"** (left sidebar)
2. Click **"New Query"**
3. Open the file `migrations/001_schema_update.sql` from your project
4. Copy ALL the content
5. Paste into Supabase SQL Editor
6. Click **"Run"** (or press Ctrl+Enter)
7. You should see "Success. No rows returned"

### 1.4 Create Storage Bucket
1. Click **"Storage"** in left sidebar
2. Click **"Create a new bucket"**
3. Name it: `sales_pdfs`
4. Make it **Public**
5. Click **"Create bucket"**

### 1.5 Get Your Credentials
1. Click **"Settings"** (gear icon) in left sidebar
2. Click **"API"**
3. Copy these values (you'll need them):
   - **Project URL** (looks like: `https://xxxxx.supabase.co`)
   - **anon/public key** (long string starting with `eyJ...`)
   - **service_role key** (another long string)
4. Click **"Database"** in Settings
5. Scroll to **"Connection string"**
6. Select **"URI"**
7. Copy the connection string
8. Replace `[YOUR-PASSWORD]` with your database password

---

## Step 2: Install Python Dependencies (2 minutes)

### 2.1 Check Python Version
Open terminal/command prompt and run:
```bash
python --version
```
You need Python 3.9 or higher. If not installed, download from [python.org](https://python.org)

### 2.2 Install Required Packages
In your project directory, run:
```bash
pip install -r requirements.txt
```

This will install all necessary packages. Wait for it to complete (2-3 minutes).

---

## Step 3: Configure Environment Variables (2 minutes)

### 3.1 Create .env File
1. In your project folder, create a new file named `.env` (exactly, with the dot)
2. Copy the content from `.env.example`
3. Replace the placeholder values with your Supabase credentials:

```env
# Supabase Configuration
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Database Configuration
DB_URL=postgresql://postgres.xxxxx:YOUR_PASSWORD@aws-0-region.pooler.supabase.com:6543/postgres?sslmode=require

# Application Configuration
APP_SECRET_KEY=your_random_secret_key_here
ENVIRONMENT=development
```

### 3.2 Generate Secret Key
To generate `APP_SECRET_KEY`, run this in Python:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
Copy the output and paste it as your `APP_SECRET_KEY`

---

## Step 4: Run the Application (1 minute)

### 4.1 Start Streamlit
In your project directory, run:
```bash
streamlit run app.py
```

### 4.2 Open in Browser
- Streamlit will automatically open your browser
- If not, go to: `http://localhost:8501`
- You should see the Sales Intelligence AI application!

---

## Step 5: Create Your First Account

1. Click **"Sign Up"** or navigate to the signup page
2. Fill in:
   - **Full Name**: Your name
   - **Email**: Your email address
   - **Password**: Create a strong password (follow the requirements)
3. Click **"Create Account"**
4. Check your email for verification link
5. Click the verification link
6. Go back and click **"Login"**
7. Enter your email and password
8. You're in! 🎉

---

## Step 6: Upload Your First File

1. In the sidebar, look for **"Upload Sales PDFs"**
2. Click **"Browse files"**
3. Select a PDF, Excel, or CSV file with sales data
4. Wait for processing
5. Your dashboard will update with insights!

---

## 🎯 Quick Test with Sample Data

If you don't have sales data yet, create a simple Excel file:

**sample_sales.xlsx:**
| Date       | Product      | Quantity | Price | Customer    |
|------------|--------------|----------|-------|-------------|
| 2024-01-01 | Product A    | 10       | 100   | Customer 1  |
| 2024-01-02 | Product B    | 5        | 200   | Customer 2  |
| 2024-01-03 | Product A    | 8        | 100   | Customer 1  |

Upload this file to see the dashboard in action!

---

## 🔧 Troubleshooting

### ❌ "Module not found" error
**Solution:**
```bash
pip install -r requirements.txt
```

### ❌ "Connection refused" or database error
**Solution:**
- Check your `.env` file has correct Supabase credentials
- Verify database migration ran successfully
- Check Supabase project is active (not paused)

### ❌ "Port 8501 already in use"
**Solution:**
```bash
streamlit run app.py --server.port 8502
```

### ❌ Authentication not working
**Solution:**
- Verify email confirmation is enabled in Supabase
- Check SUPABASE_URL and SUPABASE_KEY are correct
- Try password reset if you forgot password

### ❌ File upload fails
**Solution:**
- Check storage bucket `sales_pdfs` exists in Supabase
- Verify bucket is set to Public
- Ensure file is under 50MB

---

## 📱 Accessing from Other Devices

### On Same Network
1. Find your computer's IP address:
   - **Windows**: `ipconfig` (look for IPv4)
   - **Mac/Linux**: `ifconfig` or `ip addr`
2. On other device, go to: `http://YOUR_IP:8501`

### Over Internet
- Use Streamlit Cloud (see DEPLOYMENT_GUIDE.md)
- Or use ngrok for temporary access

---

## 🛑 Stopping the Application

Press `Ctrl+C` in the terminal where Streamlit is running

---

## 📚 Next Steps

- **Read the User Manual**: `USER_MANUAL.md` for detailed features
- **Deploy to Cloud**: `DEPLOYMENT_GUIDE.md` for Streamlit Cloud
- **Customize**: Modify code to fit your needs
- **Get Help**: Check README.md for support options

---

## ⚡ Quick Command Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py

# Run on different port
streamlit run app.py --server.port 8502

# Generate secret key
python -c "import secrets; print(secrets.token_hex(32))"

# Check Python version
python --version

# Update packages
pip install --upgrade -r requirements.txt
```

---

## ✅ Checklist

Before running, make sure:
- [ ] Python 3.9+ installed
- [ ] Supabase project created
- [ ] Database migration executed
- [ ] Storage bucket created
- [ ] `.env` file configured with credentials
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Ready to run `streamlit run app.py`

---

## 🎉 You're All Set!

Your Sales Intelligence AI is now running locally. Enjoy analyzing your sales data!

**Need help?** Check the other documentation files or open an issue on GitHub.

---

**Estimated Setup Time:** 10-15 minutes  
**Difficulty:** Easy (no coding required)