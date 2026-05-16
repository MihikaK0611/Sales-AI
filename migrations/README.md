# Database Migrations

This directory contains SQL migration scripts for the Sales Intelligence AI database.

## Migration Files

### 001_schema_update.sql
**Purpose:** Initial schema update and standardization
**Changes:**
- Creates `file_metadata` table for tracking uploaded files
- Creates new `sales_data` table with standardized column names
- Migrates existing data from old schema to new schema
- Adds user_id foreign key for multi-user support
- Creates indexes for performance optimization
- Enables Row Level Security (RLS)
- Creates RLS policies for data isolation
- Adds triggers for automatic timestamp updates
- Creates analytics view

## How to Run Migrations

### Using Supabase Dashboard
1. Log in to your Supabase project dashboard
2. Navigate to SQL Editor
3. Copy the contents of the migration file
4. Paste and execute the SQL

### Using psql Command Line
```bash
psql "postgresql://postgres.iqkzzeevjtvbnijffwqp:SalesAI%40Kathmandu@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres?sslmode=require" -f migrations/001_schema_update.sql
```

### Using Python Script
```python
from sqlalchemy import create_engine, text
from config import DB_URL

engine = create_engine(DB_URL)

with open('migrations/001_schema_update.sql', 'r') as f:
    migration_sql = f.read()

with engine.connect() as conn:
    conn.execute(text(migration_sql))
    conn.commit()
    
print("Migration completed successfully!")
```

## Migration Checklist

Before running migrations:
- [ ] Backup your database
- [ ] Review the migration script
- [ ] Test in development environment first
- [ ] Verify user permissions

After running migrations:
- [ ] Verify tables were created successfully
- [ ] Check that data was migrated correctly
- [ ] Test RLS policies
- [ ] Update application code to use new schema

## Schema Changes

### Old Schema
```sql
sales_data (
    date,
    product,
    quantity,
    price,
    revenue,
    file_id
)
```

### New Schema
```sql
sales_data (
    id,
    user_id,              -- NEW: Multi-user support
    file_id,
    invoice_number,       -- NEW
    invoice_date,         -- RENAMED from 'date'
    customer_name,        -- NEW
    customer_address,     -- NEW
    customer_contact,     -- NEW
    customer_email,       -- NEW
    product_name,         -- RENAMED from 'product'
    product_description,  -- NEW
    category,
    quantity,
    unit_price,           -- RENAMED from 'price'
    discount,             -- NEW
    tax_amount,           -- NEW
    revenue,
    payment_terms,        -- NEW
    payment_status,       -- NEW
    notes,                -- NEW
    created_at,
    updated_at
)
```

## Rollback Instructions

If you need to rollback the migration:

```sql
-- Restore from backup
ALTER TABLE sales_data RENAME TO sales_data_new;
ALTER TABLE sales_data_backup RENAME TO sales_data;

-- Or drop new tables
DROP TABLE IF EXISTS sales_data CASCADE;
DROP TABLE IF EXISTS file_metadata CASCADE;
DROP VIEW IF EXISTS sales_analytics CASCADE;
```

## Notes

- The migration preserves existing data by creating a backup table
- Row Level Security ensures users can only access their own data
- Indexes are created for optimal query performance
- The analytics view simplifies reporting queries

## Support

If you encounter issues during migration:
1. Check the error message in the SQL output
2. Verify your database connection
3. Ensure you have proper permissions
4. Contact support with the error details