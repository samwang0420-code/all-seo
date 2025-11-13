/*
  # AskCam Database Schema

  1. New Tables
    - `recognition_history`
      - `id` (uuid, primary key) - Unique identifier
      - `user_id` (uuid) - User who made the recognition (future auth support)
      - `image_url` (text) - URL or path to the captured image
      - `object_name` (text) - Identified object name
      - `explanation` (text) - AI-generated explanation
      - `video_url` (text, nullable) - Optional how-to video link
      - `is_favorite` (boolean) - Whether user marked as favorite
      - `created_at` (timestamptz) - When recognition was made
      - `updated_at` (timestamptz) - Last update timestamp
    
    - `conversation_messages`
      - `id` (uuid, primary key) - Unique identifier
      - `recognition_id` (uuid) - Links to recognition_history
      - `role` (text) - 'user' or 'assistant'
      - `content` (text) - Message content
      - `is_voice` (boolean) - Whether message was voice input/output
      - `created_at` (timestamptz) - Message timestamp

  2. Security
    - Enable RLS on both tables
    - Add policies for authenticated users to manage their own data
    - Allow public access for demo/unauthenticated usage

  3. Indexes
    - Index on created_at for sorting history
    - Index on is_favorite for filtering favorites
    - Index on recognition_id for conversation lookups
*/

-- Create recognition_history table
CREATE TABLE IF NOT EXISTS recognition_history (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid DEFAULT NULL,
  image_url text NOT NULL,
  object_name text NOT NULL,
  explanation text NOT NULL,
  video_url text DEFAULT NULL,
  is_favorite boolean DEFAULT false,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create conversation_messages table
CREATE TABLE IF NOT EXISTS conversation_messages (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  recognition_id uuid NOT NULL REFERENCES recognition_history(id) ON DELETE CASCADE,
  role text NOT NULL CHECK (role IN ('user', 'assistant')),
  content text NOT NULL,
  is_voice boolean DEFAULT false,
  created_at timestamptz DEFAULT now()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_recognition_created_at ON recognition_history(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_recognition_favorites ON recognition_history(is_favorite) WHERE is_favorite = true;
CREATE INDEX IF NOT EXISTS idx_recognition_user ON recognition_history(user_id);
CREATE INDEX IF NOT EXISTS idx_messages_recognition ON conversation_messages(recognition_id);

-- Enable Row Level Security
ALTER TABLE recognition_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversation_messages ENABLE ROW LEVEL SECURITY;

-- Policies for recognition_history
-- Allow anyone to insert (for unauthenticated demo usage)
CREATE POLICY "Anyone can create recognition"
  ON recognition_history
  FOR INSERT
  TO public
  WITH CHECK (true);

-- Allow users to view their own records or any record without user_id
CREATE POLICY "Users can view own recognition or public"
  ON recognition_history
  FOR SELECT
  TO public
  USING (user_id IS NULL OR user_id = auth.uid());

-- Allow users to update their own records or records without user_id
CREATE POLICY "Users can update own recognition or public"
  ON recognition_history
  FOR UPDATE
  TO public
  USING (user_id IS NULL OR user_id = auth.uid())
  WITH CHECK (user_id IS NULL OR user_id = auth.uid());

-- Allow users to delete their own records or records without user_id
CREATE POLICY "Users can delete own recognition or public"
  ON recognition_history
  FOR DELETE
  TO public
  USING (user_id IS NULL OR user_id = auth.uid());

-- Policies for conversation_messages
-- Allow anyone to insert messages
CREATE POLICY "Anyone can create messages"
  ON conversation_messages
  FOR INSERT
  TO public
  WITH CHECK (true);

-- Allow users to view messages for recognitions they can access
CREATE POLICY "Users can view accessible messages"
  ON conversation_messages
  FOR SELECT
  TO public
  USING (
    EXISTS (
      SELECT 1 FROM recognition_history
      WHERE recognition_history.id = conversation_messages.recognition_id
      AND (recognition_history.user_id IS NULL OR recognition_history.user_id = auth.uid())
    )
  );

-- Allow users to update messages for recognitions they can access
CREATE POLICY "Users can update accessible messages"
  ON conversation_messages
  FOR UPDATE
  TO public
  USING (
    EXISTS (
      SELECT 1 FROM recognition_history
      WHERE recognition_history.id = conversation_messages.recognition_id
      AND (recognition_history.user_id IS NULL OR recognition_history.user_id = auth.uid())
    )
  )
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM recognition_history
      WHERE recognition_history.id = conversation_messages.recognition_id
      AND (recognition_history.user_id IS NULL OR recognition_history.user_id = auth.uid())
    )
  );

-- Allow users to delete messages for recognitions they can access
CREATE POLICY "Users can delete accessible messages"
  ON conversation_messages
  FOR DELETE
  TO public
  USING (
    EXISTS (
      SELECT 1 FROM recognition_history
      WHERE recognition_history.id = conversation_messages.recognition_id
      AND (recognition_history.user_id IS NULL OR recognition_history.user_id = auth.uid())
    )
  );