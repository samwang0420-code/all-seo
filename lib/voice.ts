import * as Speech from 'expo-speech';
import { Audio } from 'expo-av';
import { Platform } from 'react-native';

export const speak = async (text: string) => {
  try {
    if (Platform.OS === 'web') {
      console.log('Text-to-speech not fully supported on web');
      return;
    }

    const isSpeaking = await Speech.isSpeakingAsync();
    if (isSpeaking) {
      await Speech.stop();
    }

    await Speech.speak(text, {
      language: 'en-US',
      pitch: 1.0,
      rate: 0.85,
    });
  } catch (error) {
    console.error('Error speaking:', error);
  }
};

export const stopSpeaking = async () => {
  try {
    await Speech.stop();
  } catch (error) {
    console.error('Error stopping speech:', error);
  }
};

export const startRecording = async () => {
  try {
    if (Platform.OS === 'web') {
      console.log('Audio recording not fully supported on web');
      return null;
    }

    await Audio.requestPermissionsAsync();
    await Audio.setAudioModeAsync({
      allowsRecordingIOS: true,
      playsInSilentModeIOS: true,
    });

    const { recording } = await Audio.Recording.createAsync(
      Audio.RecordingOptionsPresets.HIGH_QUALITY
    );

    return recording;
  } catch (error) {
    console.error('Error starting recording:', error);
    return null;
  }
};

export const stopRecording = async (recording: Audio.Recording | null) => {
  try {
    if (!recording) return null;

    await recording.stopAndUnloadAsync();
    const uri = recording.getURI();
    return uri;
  } catch (error) {
    console.error('Error stopping recording:', error);
    return null;
  }
};
