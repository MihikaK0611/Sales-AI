# 📊 Sales Intelligence AI

A powerful, production-ready sales analytics platform with AI-powered insights, built with Streamlit and Supabase.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 🌟 Features

### 🔐 Authentication & Security
- **Email/Password Authentication** with Supabase Auth
- **Email Verification** for account security
- **Password Reset** functionality
- **Row-Level Security** for data isolation
- **Secure Session Management**

### 📁 Data Extraction
- **Multi-Format Support**: PDF, Excel (.xlsx, .xls), CSV
- **Intelligent PDF Parsing**: Extracts data from various invoice formats
- **Metadata Extraction**: Invoice numbers, customer details, payment terms
- **Automatic Data Validation**: Ensures data quality
- **Error Handling**: Comprehensive error reporting

### 📈 Analytics & Insights
- **Revenue Trends**: Daily, weekly, and monthly analysis
- **Top Products**: Identify best-selling items
- **Customer Analysis**: Track top customers and segments
- **Inventory Risk**: Detect low-movement products
- **Anomaly Detection**: Spot unusual sales patterns
- **AI-Powered Insights**: Automated business recommendations
- **Sales Forecasting**: 7-day revenue predictions using XGBoost

### 📊 Visualizations
- Interactive charts with Plotly
- Revenue trend analysis
- Category contribution pie charts
- Customer segmentation
- Weekday performance analysis

### 📤 Export Capabilities
- **Excel Export**: Multi-sheet reports with analytics
- **CSV Export**: Simple data export
- **Summary Reports**: Key metrics and insights

### 👤 User Management
- Personal dashboard
- Profile management
- Usage statistics
- Secure logout

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Supabase account (free tier available)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/sales-intelligence-ai.git
   cd sales-intelligence-ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_anon_key
   SUPABASE_SERVICE_KEY=your_supabase_service_key
   DB_URL=your_postgresql_connection_string
   APP_SECRET_KEY=your_secret_key
   ENVIRONMENT=development
   ```

4. **Set up database**
   
   Run the migration script in your Supabase SQL Editor:
   ```bash
   # Copy contents of migrations/001_schema_update.sql
   # Paste and execute in Supabase SQL Editor
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open in browser**
   
   Navigate to `http://localhost:8501`

---

## 📚 Documentation

- **[User Manual](USER_MANUAL.md)** - Complete guide for end users
- **[Deployment Guide](DEPLOYMENT_GUIDE.md)** - Deploy to Streamlit Cloud
- **[Improvement Plan](IMPROVEMENT_PLAN.md)** - Technical architecture and roadmap
- **[Migration Guide](migrations/README.md)** - Database schema updates

---

## 🏗️ Project Structure

```
sales-intelligence-ai/
├── app.py                      # Main application
├── auth.py                     # Authentication module
├── database.py                 # Database operations
├── parser.py                   # PDF/Excel/CSV parsing
├── analysis.py                 # Analytics functions
├── model.py                    # ML forecasting model
├── storage.py                  # File storage
├── exports.py                  # Export functionality
├── config.py                   # Configuration
├── pages/                      # Streamlit pages
│   ├── 1_🔐_Login.py
│   ├── 2_📝_Signup.py
│   ├── 3_🔑_Reset_Password.py
│   └── 4_👤_Profile.py
├── migrations/                 # Database migrations
│   ├── 001_schema_update.sql
│   └── README.md
├── .streamlit/                 # Streamlit configuration
│   └── config.toml
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── USER_MANUAL.md             # User documentation
├── DEPLOYMENT_GUIDE.md        # Deployment instructions
├── IMPROVEMENT_PLAN.md        # Technical documentation
└── README.md                  # This file
```

---

## 🛠️ Technology Stack

### Frontend
- **Streamlit** - Web application framework
- **Plotly** - Interactive visualizations

### Backend
- **Python 3.9+** - Core language
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing

### Database & Auth
- **Supabase** - Backend as a Service
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM

### PDF Processing
- **pdfplumber** - PDF text extraction
- **Camelot** - Table extraction
- **OpenCV** - Image processing

### Machine Learning
- **XGBoost** - Sales forecasting
- **scikit-learn** - Data preprocessing

### Export
- **openpyxl** - Excel file generation

---

## 🔒 Security Features

- ✅ Environment-based configuration
- ✅ Secure password hashing
- ✅ Email verification
- ✅ Row-level security (RLS)
- ✅ SQL injection prevention
- ✅ HTTPS enforcement
- ✅ Session management
- ✅ Input validation

---

## 📊 Database Schema

### Tables

**sales_data**
- Stores all sales transactions
- User-specific data isolation
- Comprehensive product and customer information

**file_metadata**
- Tracks uploaded files
- Processing status
- Error logging

**auth.users** (Supabase managed)
- User authentication
- Email verification
- Password management

---

## 🚀 Deployment

### Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Configure secrets
4. Deploy!

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

### Other Platforms

The application can also be deployed on:
- Heroku
- AWS
- Google Cloud
- Azure

---

## 📈 Usage

### For End Users

1. **Sign Up**: Create an account with email verification
2. **Upload Data**: Upload PDF, Excel, or CSV files
3. **Analyze**: View automated insights and analytics
4. **Export**: Download reports in Excel or CSV format

See [USER_MANUAL.md](USER_MANUAL.md) for detailed instructions.

### For Developers

1. **Clone Repository**: Get the code
2. **Install Dependencies**: Set up environment
3. **Configure Database**: Run migrations
4. **Develop**: Make improvements
5. **Test**: Ensure quality
6. **Deploy**: Push to production

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🐛 Known Issues

- PDF extraction accuracy depends on invoice format quality
- Streamlit Cloud free tier has resource limitations
- Large file uploads may timeout on slow connections

---

## 🔮 Future Enhancements

- [ ] OCR support for scanned PDFs
- [ ] Multi-language support
- [ ] Advanced ML models for predictions
- [ ] Real-time collaboration features
- [ ] Mobile app
- [ ] API access
- [ ] Automated email reports
- [ ] Integration with accounting software

---

## 📞 Support

For support, please:
1. Check the [User Manual](USER_MANUAL.md)
2. Review [Deployment Guide](DEPLOYMENT_GUIDE.md)
3. Open an issue on GitHub
4. Contact the development team

---

## 👥 Authors

- **Development Team** - Initial work and ongoing maintenance

---

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- Supabase for backend infrastructure
- Open source community for various libraries

---

## 📊 Project Status

**Status**: ✅ Production Ready

**Version**: 1.0.0

**Last Updated**: May 2026

---

## 🎯 Key Metrics

- **Security**: Enterprise-grade authentication
- **Performance**: Optimized for Streamlit Cloud free tier
- **Scalability**: Supports multiple concurrent users
- **Reliability**: Comprehensive error handling
- **Usability**: Designed for non-technical users

---

**Made with ❤️ for businesses to make data-driven decisions**