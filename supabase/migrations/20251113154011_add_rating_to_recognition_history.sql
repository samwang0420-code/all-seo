/*
  # Add Rating System to Recognition History

  1. Changes
    - Add `rating` column to `recognition_history` table
      - `rating` (integer, 1-5, nullable) - User's rating of the recognition result
    - Add index on rating for analytics
    - Add check constraint to ensure rating is between 1 and 5

  2. Purpose
    - Enable users to provide feedback on recognition accuracy
    - Help train the model based on user feedback
    - Track quality metrics for improvement
*/

-- Add rating column to recognition_history
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'recognition_history' AND column_name = 'rating'
  ) THEN
    ALTER TABLE recognition_history 
    ADD COLUMN rating integer DEFAULT NULL CHECK (rating >= 1 AND rating <= 5);
  END IF;
END $$;

-- Create index on rating for analytics
CREATE INDEX IF NOT EXISTS idx_recognition_rating ON recognition_history(rating) WHERE rating IS NOT NULL;

-- Add comment to explain the column
COMMENT ON COLUMN recognition_history.rating IS 'User feedback rating (1-5 stars) for recognition accuracy';
