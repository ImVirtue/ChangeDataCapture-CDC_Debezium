ALTER TABLE transactions ADD COLUMN modified_by TEXT;

ALTER TABLE transactions ADD COLUMN modified_at TIMESTAMP;

-- Create function to capture modified information
CREATE OR REPLACE FUNCTION record_change_user()
RETURNS TRIGGER AS $$
BEGIN
    NEW.modified_by := current_user;
    NEW.modified_at := CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for UPDATE
CREATE TRIGGER trigger_record_user_update
BEFORE UPDATE ON transactions
FOR EACH ROW EXECUTE FUNCTION record_change_user();