import 'react-native-url-polyfill/auto';
import { createClient } from '@supabase/supabase-js';
import Constants from 'expo-constants';

const supabaseUrl = Constants.expoConfig?.extra?.EXPO_PUBLIC_SUPABASE_URL || process.env.EXPO_PUBLIC_SUPABASE_URL;
const supabaseAnonKey = Constants.expoConfig?.extra?.EXPO_PUBLIC_SUPABASE_ANON_KEY || process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Missing Supabase environment variables');
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    persistSession: false,
  },
});

export type RecognitionHistory = {
  id: string;
  user_id: string | null;
  image_url: string;
  object_name: string;
  explanation: string;
  video_url: string | null;
  is_favorite: boolean;
  rating: number | null;
  created_at: string;
  updated_at: string;
};

export type ConversationMessage = {
  id: string;
  recognition_id: string;
  role: 'user' | 'assistant';
  content: string;
  is_voice: boolean;
  created_at: string;
};
