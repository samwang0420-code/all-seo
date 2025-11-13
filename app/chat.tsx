import { useState, useEffect, useRef } from 'react';
import { View, Text, StyleSheet, ScrollView, Image, TouchableOpacity, TextInput, ActivityIndicator, KeyboardAvoidingView, Platform, Alert } from 'react-native';
import { useLocalSearchParams, router } from 'expo-router';
import { ArrowLeft, Send, Mic, Square, Star, Volume2 } from 'lucide-react-native';
import { supabase } from '@/lib/supabase';
import { speak, stopSpeaking, startRecording, stopRecording } from '@/lib/voice';
import { Audio } from 'expo-av';

type Message = {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  is_voice: boolean;
};

export default function ChatScreen() {
  const { imageUri } = useLocalSearchParams<{ imageUri: string }>();
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [recognitionId, setRecognitionId] = useState<string | null>(null);
  const [objectName, setObjectName] = useState<string>('');
  const [isFavorite, setIsFavorite] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const recordingRef = useRef<Audio.Recording | null>(null);
  const scrollViewRef = useRef<ScrollView>(null);

  useEffect(() => {
    if (imageUri) {
      analyzeImage();
    }
  }, [imageUri]);

  const analyzeImage = async () => {
    setLoading(true);

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: 'What is this object?',
      is_voice: false,
    };

    setMessages([userMessage]);

    try {
      const mockResponse = `This is a **Rice Cooker**.

A rice cooker is a kitchen appliance that makes cooking rice very simple and convenient.

**How to use it:**

1. **Add rice**: Open the lid and put rice in the inner pot. Use the measuring cup that comes with it.

2. **Add water**: Pour water into the pot. Usually, the water level should be slightly above the rice. Many rice cookers have marks inside to guide you.

3. **Close the lid**: Make sure it's properly closed.

4. **Press the button**: Press the "Cook" or "Start" button. The light will turn on.

5. **Wait**: The rice cooker will automatically cook the rice. When it's done, it will switch to "Keep Warm" mode.

6. **Enjoy**: Open the lid carefully (hot steam will come out) and serve your rice!

**Tips:**
- Rinse the rice before cooking to remove excess starch
- Don't open the lid while cooking
- The rice cooker can also be used for steaming vegetables or cooking porridge

Would you like to see a video showing how to use it?`;

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: mockResponse,
        is_voice: false,
      };

      setMessages([userMessage, assistantMessage]);

      if (Platform.OS !== 'web') {
        await speak(mockResponse);
      }

      const { data: recognition, error } = await supabase
        .from('recognition_history')
        .insert({
          image_url: imageUri,
          object_name: 'Rice Cooker',
          explanation: mockResponse,
          video_url: 'https://www.youtube.com/watch?v=example',
          is_favorite: false,
        })
        .select()
        .single();

      if (error) throw error;

      if (recognition) {
        setRecognitionId(recognition.id);
        setObjectName(recognition.object_name);
        setIsFavorite(recognition.is_favorite);

        await supabase.from('conversation_messages').insert([
          {
            recognition_id: recognition.id,
            role: 'user',
            content: userMessage.content,
            is_voice: false,
          },
          {
            recognition_id: recognition.id,
            role: 'assistant',
            content: assistantMessage.content,
            is_voice: false,
          },
        ]);
      }
    } catch (error) {
      console.error('Error analyzing image:', error);
      const errorMessage: Message = {
        id: (Date.now() + 2).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        is_voice: false,
      };
      setMessages([userMessage, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const sendMessage = async () => {
    if (!inputText.trim() || !recognitionId) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputText.trim(),
      is_voice: false,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputText('');
    setLoading(true);

    try {
      await supabase.from('conversation_messages').insert({
        recognition_id: recognitionId,
        role: 'user',
        content: userMessage.content,
        is_voice: false,
      });

      const mockAIResponse = `That's a great question! Here's what I can tell you:

Based on your question about "${inputText.trim()}", I recommend checking the user manual that came with your rice cooker.

Most rice cookers have similar features:
- A removable inner pot for easy cleaning
- A keep-warm function that activates automatically
- Simple one-button operation

If you need more specific help, feel free to ask another question!`;

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: mockAIResponse,
        is_voice: false,
      };

      setMessages((prev) => [...prev, assistantMessage]);

      if (Platform.OS !== 'web') {
        await speak(mockAIResponse);
      }

      await supabase.from('conversation_messages').insert({
        recognition_id: recognitionId,
        role: 'assistant',
        content: assistantMessage.content,
        is_voice: false,
      });
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleFavorite = async () => {
    if (!recognitionId) return;

    try {
      const newFavoriteStatus = !isFavorite;

      const { error } = await supabase
        .from('recognition_history')
        .update({ is_favorite: newFavoriteStatus })
        .eq('id', recognitionId);

      if (error) throw error;

      setIsFavorite(newFavoriteStatus);
    } catch (error) {
      console.error('Error toggling favorite:', error);
    }
  };

  const toggleRecording = async () => {
    if (Platform.OS === 'web') {
      Alert.alert('Not Available', 'Voice recording is not available on web');
      return;
    }

    if (isRecording) {
      setIsRecording(false);
      const uri = await stopRecording(recordingRef.current);
      recordingRef.current = null;

      if (uri) {
        setInputText('How do I clean it?');
      }
    } else {
      const recording = await startRecording();
      if (recording) {
        recordingRef.current = recording;
        setIsRecording(true);
      } else {
        Alert.alert('Permission Required', 'Microphone permission is needed for voice input');
      }
    }
  };

  const readMessageAloud = async (content: string) => {
    if (Platform.OS === 'web') {
      Alert.alert('Not Available', 'Text-to-speech is not available on web');
      return;
    }

    if (isSpeaking) {
      await stopSpeaking();
      setIsSpeaking(false);
    } else {
      setIsSpeaking(true);
      await speak(content);
      setIsSpeaking(false);
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      keyboardVerticalOffset={0}
    >
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
          <ArrowLeft size={24} color="#1f2937" />
        </TouchableOpacity>
        <Text style={styles.headerTitle} numberOfLines={1}>
          {objectName || 'Analyzing...'}
        </Text>
        <TouchableOpacity onPress={toggleFavorite} style={styles.favoriteButton}>
          <Star size={24} color={isFavorite ? '#fbbf24' : '#9ca3af'} fill={isFavorite ? '#fbbf24' : 'none'} />
        </TouchableOpacity>
      </View>

      {imageUri && (
        <View style={styles.imageContainer}>
          <Image source={{ uri: imageUri }} style={styles.image} />
        </View>
      )}

      <ScrollView
        ref={scrollViewRef}
        style={styles.messagesContainer}
        contentContainerStyle={styles.messagesContent}
        onContentSizeChange={() => scrollViewRef.current?.scrollToEnd({ animated: true })}
      >
        {messages.map((message) => (
          <View key={message.id} style={styles.messageWrapper}>
            <View
              style={[
                styles.messageBubble,
                message.role === 'user' ? styles.userBubble : styles.assistantBubble,
              ]}
            >
              <Text
                style={[
                  styles.messageText,
                  message.role === 'user' ? styles.userText : styles.assistantText,
                ]}
              >
                {message.content}
              </Text>
            </View>
            {message.role === 'assistant' && Platform.OS !== 'web' && (
              <TouchableOpacity
                style={styles.speakerButton}
                onPress={() => readMessageAloud(message.content)}
              >
                <Volume2 size={20} color={isSpeaking ? '#2563eb' : '#6b7280'} />
              </TouchableOpacity>
            )}
          </View>
        ))}

        {loading && (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="small" color="#2563eb" />
            <Text style={styles.loadingText}>Thinking...</Text>
          </View>
        )}
      </ScrollView>

      <View style={styles.inputContainer}>
        <TouchableOpacity
          style={[styles.voiceButton, isRecording && styles.voiceButtonRecording]}
          onPress={toggleRecording}
        >
          {isRecording ? <Square size={20} color="#ef4444" /> : <Mic size={24} color="#6b7280" />}
        </TouchableOpacity>
        <TextInput
          style={styles.input}
          placeholder="Ask a question..."
          placeholderTextColor="#9ca3af"
          value={inputText}
          onChangeText={setInputText}
          multiline
          maxLength={500}
        />
        <TouchableOpacity
          style={[styles.sendButton, !inputText.trim() && styles.sendButtonDisabled]}
          onPress={sendMessage}
          disabled={!inputText.trim() || loading}
        >
          <Send size={20} color="#ffffff" />
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f9fafb',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingTop: 60,
    paddingBottom: 12,
    backgroundColor: '#ffffff',
    borderBottomWidth: 1,
    borderBottomColor: '#e5e7eb',
  },
  backButton: {
    padding: 8,
  },
  headerTitle: {
    flex: 1,
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1f2937',
    textAlign: 'center',
    marginHorizontal: 8,
  },
  favoriteButton: {
    padding: 8,
  },
  imageContainer: {
    width: '100%',
    height: 200,
    backgroundColor: '#000000',
  },
  image: {
    width: '100%',
    height: '100%',
    resizeMode: 'contain',
  },
  messagesContainer: {
    flex: 1,
  },
  messagesContent: {
    padding: 16,
    gap: 12,
  },
  messageWrapper: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    gap: 8,
  },
  messageBubble: {
    maxWidth: '80%',
    padding: 16,
    borderRadius: 16,
    marginVertical: 4,
  },
  userBubble: {
    alignSelf: 'flex-end',
    backgroundColor: '#2563eb',
  },
  assistantBubble: {
    alignSelf: 'flex-start',
    backgroundColor: '#ffffff',
    borderWidth: 1,
    borderColor: '#e5e7eb',
  },
  messageText: {
    fontSize: 16,
    lineHeight: 24,
  },
  userText: {
    color: '#ffffff',
  },
  assistantText: {
    color: '#1f2937',
  },
  speakerButton: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: '#f3f4f6',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 4,
  },
  loadingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    alignSelf: 'flex-start',
    backgroundColor: '#ffffff',
    padding: 12,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#e5e7eb',
    gap: 8,
  },
  loadingText: {
    fontSize: 14,
    color: '#6b7280',
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    padding: 12,
    backgroundColor: '#ffffff',
    borderTopWidth: 1,
    borderTopColor: '#e5e7eb',
    gap: 8,
  },
  voiceButton: {
    padding: 12,
    borderRadius: 24,
    backgroundColor: '#f3f4f6',
  },
  voiceButtonRecording: {
    backgroundColor: '#fee2e2',
  },
  input: {
    flex: 1,
    minHeight: 44,
    maxHeight: 120,
    backgroundColor: '#f3f4f6',
    borderRadius: 22,
    paddingHorizontal: 16,
    paddingVertical: 12,
    fontSize: 16,
    color: '#1f2937',
  },
  sendButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: '#2563eb',
    justifyContent: 'center',
    alignItems: 'center',
  },
  sendButtonDisabled: {
    backgroundColor: '#9ca3af',
  },
});
