-- Add other_category field to concerns table
ALTER TABLE concerns 
ADD COLUMN IF NOT EXISTS other_category VARCHAR(100);

-- Add comment
COMMENT ON COLUMN concerns.other_category IS 'Custom category text when user selects "Other" category';
