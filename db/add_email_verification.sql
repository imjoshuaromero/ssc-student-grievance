-- Add email verification fields to users table
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS verification_code VARCHAR(6),
ADD COLUMN IF NOT EXISTS verification_code_expires TIMESTAMP,
ADD COLUMN IF NOT EXISTS verification_token VARCHAR(255);

-- Create index for verification code lookups
CREATE INDEX IF NOT EXISTS idx_users_verification_code ON users(verification_code);
CREATE INDEX IF NOT EXISTS idx_users_verification_token ON users(verification_token);

-- Update existing users to verified
UPDATE users SET email_verified = TRUE WHERE email_verified IS NULL;
