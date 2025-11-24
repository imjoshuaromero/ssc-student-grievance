-- Drop the duplicate trigger that's causing issues
DROP TRIGGER IF EXISTS trigger_log_status_change ON concerns;

-- Drop the function if you want to remove it completely
DROP FUNCTION IF EXISTS log_status_change();

-- Verify
SELECT * FROM pg_trigger WHERE tgname = 'trigger_log_status_change';
