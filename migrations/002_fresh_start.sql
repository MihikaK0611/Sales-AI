-- Migration: Fresh Start - Create New Schema Without Data Migration
-- Description: Creates new tables with improved schema, no data migration
-- Date: 2026-05-10
-- Use this if you want to start fresh without migrating existing data

-- Step 1: Drop existing tables if you want a clean start (OPTIONAL - UNCOMMENT IF NEEDED)
-- WARNING: This will delete all existing data!
-- DROP TABLE IF EXISTS sales_data CASCADE;
-- DROP TABLE IF EXISTS file_metadata CASCADE;

-- Step 2: Create file_metadata table for tracking uploaded files
CREATE TABLE IF NOT EXISTS file_metadata (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_size INTEGER,
    upload_date TIMESTAMP DEFAULT NOW(),
    processing_status VARCHAR(50) DEFAULT 'pending',
    error_message TEXT,
    records_extracted INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Step 3: Create new sales_data table with improved schema
CREATE TABLE IF NOT EXISTS sales_data (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    file_id UUID REFERENCES file_metadata(id) ON DELETE CASCADE,
    
    -- Invoice Information
    invoice_number VARCHAR(100),
    invoice_date DATE NOT NULL,
    
    -- Customer Information
    customer_name VARCHAR(255),
    customer_address TEXT,
    customer_contact VARCHAR(100),
    customer_email VARCHAR(255),
    
    -- Product Information
    product_name VARCHAR(255) NOT NULL,
    product_description TEXT,
    category VARCHAR(100),
    
    -- Transaction Details
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0),
    discount DECIMAL(10,2) DEFAULT 0 CHECK (discount >= 0),
    tax_amount DECIMAL(10,2) DEFAULT 0 CHECK (tax_amount >= 0),
    revenue DECIMAL(10,2) NOT NULL CHECK (revenue >= 0),
    
    -- Additional Information
    payment_terms VARCHAR(100),
    payment_status VARCHAR(50),
    notes TEXT,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Step 4: Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_sales_user_id ON sales_data(user_id);
CREATE INDEX IF NOT EXISTS idx_sales_file_id ON sales_data(file_id);
CREATE INDEX IF NOT EXISTS idx_sales_invoice_date ON sales_data(invoice_date);
CREATE INDEX IF NOT EXISTS idx_sales_customer_name ON sales_data(customer_name);
CREATE INDEX IF NOT EXISTS idx_sales_product_name ON sales_data(product_name);
CREATE INDEX IF NOT EXISTS idx_sales_category ON sales_data(category);
CREATE INDEX IF NOT EXISTS idx_file_user_id ON file_metadata(user_id);
CREATE INDEX IF NOT EXISTS idx_file_upload_date ON file_metadata(upload_date);

-- Step 5: Enable Row Level Security (RLS)
ALTER TABLE sales_data ENABLE ROW LEVEL SECURITY;
ALTER TABLE file_metadata ENABLE ROW LEVEL SECURITY;

-- Step 6: Create RLS policies for sales_data
-- Drop existing policies if they exist
DROP POLICY IF EXISTS sales_data_select_policy ON sales_data;
DROP POLICY IF EXISTS sales_data_insert_policy ON sales_data;
DROP POLICY IF EXISTS sales_data_update_policy ON sales_data;
DROP POLICY IF EXISTS sales_data_delete_policy ON sales_data;

-- Users can only see their own data
CREATE POLICY sales_data_select_policy ON sales_data
    FOR SELECT
    USING (auth.uid() = user_id);

-- Users can only insert their own data
CREATE POLICY sales_data_insert_policy ON sales_data
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Users can only update their own data
CREATE POLICY sales_data_update_policy ON sales_data
    FOR UPDATE
    USING (auth.uid() = user_id);

-- Users can only delete their own data
CREATE POLICY sales_data_delete_policy ON sales_data
    FOR DELETE
    USING (auth.uid() = user_id);

-- Step 7: Create RLS policies for file_metadata
DROP POLICY IF EXISTS file_metadata_select_policy ON file_metadata;
DROP POLICY IF EXISTS file_metadata_insert_policy ON file_metadata;
DROP POLICY IF EXISTS file_metadata_update_policy ON file_metadata;
DROP POLICY IF EXISTS file_metadata_delete_policy ON file_metadata;

CREATE POLICY file_metadata_select_policy ON file_metadata
    FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY file_metadata_insert_policy ON file_metadata
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY file_metadata_update_policy ON file_metadata
    FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY file_metadata_delete_policy ON file_metadata
    FOR DELETE
    USING (auth.uid() = user_id);

-- Step 8: Create function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Step 9: Create triggers for updated_at
DROP TRIGGER IF EXISTS update_sales_data_updated_at ON sales_data;
DROP TRIGGER IF EXISTS update_file_metadata_updated_at ON file_metadata;

CREATE TRIGGER update_sales_data_updated_at
    BEFORE UPDATE ON sales_data
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_file_metadata_updated_at
    BEFORE UPDATE ON file_metadata
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Step 10: Create view for sales analytics
CREATE OR REPLACE VIEW sales_analytics AS
SELECT 
    s.user_id,
    s.invoice_date,
    s.customer_name,
    s.product_name,
    s.category,
    s.quantity,
    s.unit_price,
    s.discount,
    s.tax_amount,
    s.revenue,
    EXTRACT(YEAR FROM s.invoice_date) as year,
    EXTRACT(MONTH FROM s.invoice_date) as month,
    EXTRACT(WEEK FROM s.invoice_date) as week,
    TO_CHAR(s.invoice_date, 'Day') as day_name,
    f.filename,
    f.upload_date
FROM sales_data s
LEFT JOIN file_metadata f ON s.file_id = f.id;

-- Grant permissions on the view
GRANT SELECT ON sales_analytics TO authenticated;

-- Migration completed successfully
COMMENT ON TABLE sales_data IS 'Stores sales transaction data with improved schema';
COMMENT ON TABLE file_metadata IS 'Tracks uploaded files and their processing status';
COMMENT ON VIEW sales_analytics IS 'Provides analytics-ready view of sales data';

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'Fresh start migration completed successfully!';
    RAISE NOTICE 'New tables created: sales_data, file_metadata';
    RAISE NOTICE 'Row Level Security enabled';
    RAISE NOTICE 'Ready to use!';
END $$;

-- Made with Bob
