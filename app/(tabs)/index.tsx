import { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image, ScrollView, Alert } from 'react-native';
import { CameraView, useCameraPermissions } from 'expo-camera';
import { Camera, Image as ImageIcon, X, Sparkles, Eye } from 'lucide-react-native';
import * as ImagePicker from 'expo-image-picker';
import { router } from 'expo-router';
import { LinearGradient } from 'expo-linear-gradient';

export default function CameraTab() {
  const [permission, requestPermission] = useCameraPermissions();
  const [showCamera, setShowCamera] = useState(false);
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [cameraRef, setCameraRef] = useState<CameraView | null>(null);

  const pickImage = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ['images'],
      allowsEditing: false,
      quality: 0.8,
    });

    if (!result.canceled && result.assets[0]) {
      setSelectedImage(result.assets[0].uri);
    }
  };

  const takePicture = async () => {
    if (cameraRef) {
      try {
        const photo = await cameraRef.takePictureAsync();
        if (photo) {
          setSelectedImage(photo.uri);
          setShowCamera(false);
        }
      } catch (error) {
        Alert.alert('Error', 'Failed to take picture');
      }
    }
  };

  const openCamera = async () => {
    if (!permission?.granted) {
      const result = await requestPermission();
      if (!result.granted) {
        Alert.alert('Permission Required', 'Camera permission is needed to take photos');
        return;
      }
    }
    setShowCamera(true);
  };

  const analyzeImage = () => {
    if (selectedImage) {
      router.push({
        pathname: '/chat',
        params: { imageUri: selectedImage },
      });
    }
  };

  if (showCamera) {
    return (
      <View style={styles.container}>
        <CameraView
          style={styles.camera}
          facing="back"
          ref={(ref) => setCameraRef(ref)}
        >
          <View style={styles.cameraControls}>
            <TouchableOpacity
              style={styles.closeButton}
              onPress={() => setShowCamera(false)}
            >
              <X size={32} color="#ffffff" />
            </TouchableOpacity>
            <TouchableOpacity
              style={styles.captureButton}
              onPress={takePicture}
            >
              <View style={styles.captureButtonInner} />
            </TouchableOpacity>
          </View>
        </CameraView>
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.content}
      showsVerticalScrollIndicator={false}
    >
      <LinearGradient
        colors={['#0ea5e9', '#8b5cf6', '#ec4899']}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
        style={styles.headerGradient}
      >
        <View style={styles.header}>
          <View style={styles.titleContainer}>
            <Text style={styles.title}>AskCam</Text>
            <Sparkles size={32} color="#fbbf24" strokeWidth={2} />
          </View>
          <Text style={styles.subtitle}>Your AI-Powered Vision Assistant</Text>
          <View style={styles.tagline}>
            <Eye size={18} color="#ffffff" strokeWidth={2} />
            <Text style={styles.taglineText}>A Tap to Grasp Life’s Essence.</Text>
          </View>
        </View>
      </LinearGradient>

      {selectedImage ? (
        <View style={styles.imagePreview}>
          <Image source={{ uri: selectedImage }} style={styles.previewImage} />
          <LinearGradient
            colors={['transparent', 'rgba(0,0,0,0.3)']}
            style={styles.imageOverlay}
          />
          <TouchableOpacity
            style={styles.removeButton}
            onPress={() => setSelectedImage(null)}
          >
            <X size={24} color="#ffffff" />
          </TouchableOpacity>
        </View>
      ) : (
        <View style={styles.placeholder}>
          <LinearGradient
            colors={['#f0f9ff', '#e0f2fe']}
            style={styles.placeholderGradient}
          >
            <Camera size={72} color="#0ea5e9" strokeWidth={1.5} />
            <Text style={styles.placeholderText}>Capture or upload a photo</Text>
            <Text style={styles.placeholderSubtext}>AI will identify what it sees</Text>
          </LinearGradient>
        </View>
      )}

      <View style={styles.buttonContainer}>
        <TouchableOpacity
          style={[styles.button, styles.primaryButton]}
          onPress={openCamera}
          activeOpacity={0.8}
        >
          <LinearGradient
            colors={['#0ea5e9', '#8b5cf6']}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 0 }}
            style={styles.buttonGradient}
          >
            <Camera size={24} color="#ffffff" strokeWidth={2.5} />
            <Text style={styles.buttonText}>Capture</Text>
          </LinearGradient>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.button, styles.secondaryButton]}
          onPress={pickImage}
          activeOpacity={0.8}
        >
          <ImageIcon size={24} color="#8b5cf6" strokeWidth={2.5} />
          <Text style={[styles.buttonText, styles.secondaryButtonText]}>Upload</Text>
        </TouchableOpacity>
      </View>

      {selectedImage && (
        <TouchableOpacity
          style={[styles.button, styles.analyzeButton]}
          onPress={analyzeImage}
          activeOpacity={0.8}
        >
          <LinearGradient
            colors={['#10b981', '#059669']}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 0 }}
            style={styles.buttonGradient}
          >
            <Sparkles size={24} color="#ffffff" strokeWidth={2.5} />
            <Text style={styles.analyzeButtonText}>Identify</Text>
          </LinearGradient>
        </TouchableOpacity>
      )}

      <View style={styles.infoSection}>
        <Text style={styles.infoTitle}>How it works</Text>
        <View style={styles.stepsContainer}>
          <View style={styles.stepCard}>
            <LinearGradient
              colors={['#dbeafe', '#bfdbfe']}
              style={styles.stepIconContainer}
            >
              <Text style={styles.stepIcon}>📸</Text>
            </LinearGradient>
            <Text style={styles.stepTitle}>Capture</Text>
            <Text style={styles.stepText}>Upload a photo</Text>
          </View>
          <View style={styles.stepCard}>
            <LinearGradient
              colors={['#e9d5ff', '#d8b4fe']}
              style={styles.stepIconContainer}
            >
              <Text style={styles.stepIcon}>🔍</Text>
            </LinearGradient>
            <Text style={styles.stepTitle}>Identify</Text>
            <Text style={styles.stepText}>AI analyzes the image</Text>
          </View>
          <View style={styles.stepCard}>
            <LinearGradient
              colors={['#d1fae5', '#a7f3d0']}
              style={styles.stepIconContainer}
            >
              <Text style={styles.stepIcon}>💡</Text>
            </LinearGradient>
            <Text style={styles.stepTitle}>Learn</Text>
            <Text style={styles.stepText}>Get instant insights</Text>
          </View>
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc',
  },
  content: {
    paddingBottom: 100,
  },
  headerGradient: {
    paddingTop: 60,
    paddingBottom: 32,
    paddingHorizontal: 24,
    marginBottom: 32,
    borderBottomLeftRadius: 32,
    borderBottomRightRadius: 32,
  },
  header: {
    alignItems: 'center',
  },
  titleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    marginBottom: 12,
  },
  title: {
    fontSize: 42,
    fontWeight: '800',
    color: '#ffffff',
    letterSpacing: -1,
  },
  subtitle: {
    fontSize: 16,
    color: '#ffffff',
    fontWeight: '500',
    marginBottom: 12,
    opacity: 0.95,
  },
  tagline: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
  },
  taglineText: {
    fontSize: 14,
    color: '#ffffff',
    fontWeight: '600',
  },
  imagePreview: {
    width: '90%',
    height: 320,
    borderRadius: 24,
    overflow: 'hidden',
    marginBottom: 24,
    alignSelf: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.15,
    shadowRadius: 16,
    elevation: 10,
  },
  previewImage: {
    width: '100%',
    height: '100%',
    resizeMode: 'contain',
  },
  imageOverlay: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    height: 100,
  },
  removeButton: {
    position: 'absolute',
    top: 16,
    right: 16,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    borderRadius: 24,
    padding: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 5,
  },
  placeholder: {
    height: 320,
    borderRadius: 24,
    overflow: 'hidden',
    marginBottom: 24,
    marginHorizontal: 20,
    shadowColor: '#0ea5e9',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 12,
    elevation: 5,
    alignSelf: 'center',
    width: '90%',
  },
  placeholderGradient: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 32,
  },
  placeholderText: {
    fontSize: 18,
    color: '#0369a1',
    fontWeight: '700',
    marginTop: 20,
    textAlign: 'center',
  },
  placeholderSubtext: {
    fontSize: 14,
    color: '#0284c7',
    marginTop: 8,
    textAlign: 'center',
    fontWeight: '500',
  },
  buttonContainer: {
    flexDirection: 'row',
    gap: 16,
    marginBottom: 20,
    paddingHorizontal: 20,
  },
  button: {
    flex: 1,
    borderRadius: 24,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 12,
    elevation: 6,
  },
  buttonGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 10,
    paddingVertical: 18,
  },
  primaryButton: {
    backgroundColor: 'transparent',
  },
  secondaryButton: {
    backgroundColor: '#ffffff',
    borderWidth: 2.5,
    borderColor: '#8b5cf6',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 10,
    paddingVertical: 18,
  },
  buttonText: {
    fontSize: 16,
    fontWeight: '700',
    color: '#ffffff',
    letterSpacing: 0.5,
  },
  secondaryButtonText: {
    color: '#8b5cf6',
  },
  analyzeButton: {
    backgroundColor: 'transparent',
    marginBottom: 32,
    marginHorizontal: 20,
  },
  analyzeButtonText: {
    fontSize: 18,
    fontWeight: '800',
    color: '#ffffff',
    letterSpacing: 0.5,
  },
  infoSection: {
    paddingHorizontal: 20,
    paddingTop: 8,
  },
  infoTitle: {
    fontSize: 22,
    fontWeight: '800',
    color: '#1e293b',
    marginBottom: 20,
    textAlign: 'center',
    letterSpacing: -0.5,
  },
  stepsContainer: {
    flexDirection: 'row',
    gap: 12,
  },
  stepCard: {
    flex: 1,
    backgroundColor: '#ffffff',
    borderRadius: 20,
    padding: 16,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 8,
    elevation: 3,
  },
  stepIconContainer: {
    width: 64,
    height: 64,
    borderRadius: 32,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
  },
  stepIcon: {
    fontSize: 32,
  },
  stepTitle: {
    fontSize: 15,
    fontWeight: '700',
    color: '#1e293b',
    marginBottom: 6,
    textAlign: 'center',
  },
  stepText: {
    fontSize: 12,
    color: '#64748b',
    textAlign: 'center',
    lineHeight: 16,
    fontWeight: '500',
  },
  camera: {
    flex: 1,
  },
  cameraControls: {
    flex: 1,
    backgroundColor: 'transparent',
    flexDirection: 'column',
    justifyContent: 'space-between',
    padding: 20,
  },
  closeButton: {
    alignSelf: 'flex-end',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    borderRadius: 30,
    padding: 10,
  },
  captureButton: {
    alignSelf: 'center',
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#ffffff',
    padding: 5,
    marginBottom: 40,
  },
  captureButtonInner: {
    flex: 1,
    borderRadius: 35,
    backgroundColor: '#2563eb',
  },
});
