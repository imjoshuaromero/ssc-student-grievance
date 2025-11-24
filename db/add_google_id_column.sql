-- Add google_id column to users table if it doesn't exist
-- This is for existing databases that were created before the Google OAuth feature was added

DO $$ 
BEGIN
    -- Check if google_id column exists, if not add it
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'users' 
        AND column_name = 'google_id'
    ) THEN
        ALTER TABLE users ADD COLUMN google_id VARCHAR(255) UNIQUE;
        CREATE INDEX idx_users_google_id ON users(google_id);
        
        RAISE NOTICE 'google_id column added successfully';
    ELSE
        RAISE NOTICE 'google_id column already exists';
    END IF;
END $$;

-- Verify the column was added
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'users' 
AND column_name = 'google_id';
