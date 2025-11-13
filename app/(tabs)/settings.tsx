import { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Switch, Alert } from 'react-native';
import { Volume2, VolumeX, Type, Trash2, Info, ExternalLink, User, Crown, Sparkles, Mail, ChevronRight, CheckCircle2 } from 'lucide-react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { supabase } from '@/lib/supabase';

type SubscriptionType = 'trial' | 'monthly' | 'annual' | null;

export default function ProfileTab() {
  const [user, setUser] = useState<any>(null);
  const [subscription, setSubscription] = useState<any>(null);
  const [voiceEnabled, setVoiceEnabled] = useState(true);
  const [autoSpeak, setAutoSpeak] = useState(true);
  const [fontSize, setFontSize] = useState<'small' | 'medium' | 'large'>('medium');
  const [daysRemaining, setDaysRemaining] = useState<number>(0);

  useEffect(() => {
    loadUserData();
  }, []);

  const loadUserData = async () => {
    try {
      const { data: { user: authUser } } = await supabase.auth.getUser();
      setUser(authUser);

      if (authUser) {
        const { data: subData } = await supabase
          .from('user_subscriptions')
          .select('*')
          .eq('user_id', authUser.id)
          .maybeSingle();

        if (subData) {
          setSubscription(subData);

          if (subData.trial_end_date) {
            const endDate = new Date(subData.trial_end_date);
            const now = new Date();
            const diffTime = endDate.getTime() - now.getTime();
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
            setDaysRemaining(Math.max(0, diffDays));
          }
        }
      }
    } catch (error) {
      console.error('Error loading user data:', error);
    }
  };

  const signInWithGoogle = async () => {
    try {
      const { error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
          redirectTo: window.location.origin,
        },
      });

      if (error) throw error;
    } catch (error: any) {
      Alert.alert('Error', error.message || 'Failed to sign in with Google');
    }
  };

  const signOut = async () => {
    try {
      const { error } = await supabase.auth.signOut();
      if (error) throw error;
      setUser(null);
      setSubscription(null);
    } catch (error: any) {
      Alert.alert('Error', error.message || 'Failed to sign out');
    }
  };

  const clearAllHistory = async () => {
    Alert.alert(
      'Clear All History',
      'Are you sure you want to delete all history? This cannot be undone.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Delete All',
          style: 'destructive',
          onPress: async () => {
            try {
              const { error } = await supabase
                .from('recognition_history')
                .delete()
                .neq('id', '00000000-0000-0000-0000-000000000000');

              if (error) throw error;

              Alert.alert('Success', 'All history has been cleared');
            } catch (error) {
              console.error('Error clearing history:', error);
              Alert.alert('Error', 'Failed to clear history');
            }
          },
        },
      ]
    );
  };

  const handleSubscribe = (type: 'monthly' | 'annual') => {
    Alert.alert(
      'Coming Soon',
      `${type === 'monthly' ? 'Monthly' : 'Annual'} subscription will be available soon!`,
      [{ text: 'OK' }]
    );
  };

  const isTrialActive = subscription?.subscription_type === 'trial' && subscription?.status === 'active';
  const isPro = subscription?.subscription_type !== 'trial' && subscription?.status === 'active';

  return (
    <ScrollView style={styles.container}>
      <LinearGradient
        colors={['#6366f1', '#8b5cf6', '#a855f7']}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
        style={styles.headerGradient}
      >
        <View style={styles.header}>
          <Text style={styles.title}>Profile</Text>
        </View>
      </LinearGradient>

      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <User size={20} color="#6b7280" strokeWidth={2.5} />
          <Text style={styles.sectionTitle}>ACCOUNT</Text>
        </View>

        {!user ? (
          <TouchableOpacity style={styles.card} onPress={signInWithGoogle}>
            <LinearGradient
              colors={['#4285F4', '#34A853']}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 0 }}
              style={styles.signInGradient}
            >
              <View style={styles.signInContent}>
                <Mail size={24} color="#ffffff" strokeWidth={2.5} />
                <View style={styles.signInText}>
                  <Text style={styles.signInTitle}>Sign In with Google</Text>
                  <Text style={styles.signInSubtitle}>Securely sync your data across devices</Text>
                </View>
              </View>
            </LinearGradient>
          </TouchableOpacity>
        ) : (
          <View style={styles.card}>
            <View style={styles.userInfo}>
              <View style={styles.avatarContainer}>
                <LinearGradient
                  colors={['#6366f1', '#a855f7']}
                  style={styles.avatar}
                >
                  <Text style={styles.avatarText}>
                    {user.email?.charAt(0).toUpperCase() || 'U'}
                  </Text>
                </LinearGradient>
              </View>
              <View style={styles.userDetails}>
                <Text style={styles.userName}>{user.user_metadata?.full_name || 'User'}</Text>
                <Text style={styles.userEmail}>{user.email}</Text>
              </View>
            </View>
            <TouchableOpacity style={styles.manageButton} onPress={signOut}>
              <Text style={styles.manageButtonText}>Sign Out</Text>
              <ChevronRight size={20} color="#8b5cf6" strokeWidth={2.5} />
            </TouchableOpacity>
          </View>
        )}
      </View>

      {isTrialActive && (
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Sparkles size={20} color="#FF9F00" strokeWidth={2.5} />
            <Text style={styles.sectionTitle}>MEMBERSHIP</Text>
            <View style={styles.trialBadge}>
              <Text style={styles.trialBadgeText}>• TRIAL ACTIVE</Text>
            </View>
          </View>

          <View style={styles.card}>
            <LinearGradient
              colors={['#fef3c7', '#fde68a']}
              style={styles.trialCard}
            >
              <Text style={styles.trialTitle}>Your 3-Day Free Trial is active!</Text>
              <Text style={styles.trialDescription}>
                Experience unlimited identifications and premium features. Trial ends in {daysRemaining} {daysRemaining === 1 ? 'day' : 'days'}.
              </Text>
              <TouchableOpacity style={styles.trialButton}>
                <LinearGradient
                  colors={['#f59e0b', '#d97706']}
                  style={styles.trialButtonGradient}
                >
                  <Text style={styles.trialButtonText}>Subscribe Now</Text>
                </LinearGradient>
              </TouchableOpacity>
              <Text style={styles.trialFooter}>Unlock all features before your trial ends.</Text>
            </LinearGradient>
          </View>
        </View>
      )}

      {isPro && (
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Crown size={20} color="#f59e0b" strokeWidth={2.5} />
            <Text style={styles.sectionTitle}>MEMBERSHIP</Text>
          </View>

          <View style={styles.card}>
            <LinearGradient
              colors={['#fef3c7', '#fde68a']}
              style={styles.proCard}
            >
              <View style={styles.proHeader}>
                <Crown size={32} color="#f59e0b" strokeWidth={2.5} />
                <Text style={styles.proTitle}>✨ You're a Pro Member!</Text>
              </View>
              <Text style={styles.proDescription}>
                Your subscription is active. Next billing date: {subscription.next_billing_date ? new Date(subscription.next_billing_date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : 'N/A'}
              </Text>
              <TouchableOpacity style={styles.manageSubButton}>
                <Text style={styles.manageSubButtonText}>Manage Subscription</Text>
                <ChevronRight size={20} color="#f59e0b" strokeWidth={2.5} />
              </TouchableOpacity>
            </LinearGradient>
          </View>
        </View>
      )}

      {!isPro && (
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Crown size={20} color="#f59e0b" strokeWidth={2.5} />
            <Text style={styles.sectionTitle}>UPGRADE TO PRO</Text>
          </View>

          <View style={styles.card}>
            <Text style={styles.upgradeTitle}>Unlock Unlimited AI Identifications & Premium Features</Text>

            <View style={styles.pricingCard}>
              <View style={styles.pricingHeader}>
                <Text style={styles.pricingPlan}>Monthly Plan</Text>
                <View style={styles.pricingPrice}>
                  <Text style={styles.pricingAmount}>$9.99</Text>
                  <Text style={styles.pricingPeriod}> / month</Text>
                </View>
              </View>
              <TouchableOpacity
                style={styles.subscribeButton}
                onPress={() => handleSubscribe('monthly')}
              >
                <LinearGradient
                  colors={['#6366f1', '#8b5cf6']}
                  start={{ x: 0, y: 0 }}
                  end={{ x: 1, y: 0 }}
                  style={styles.subscribeButtonGradient}
                >
                  <Text style={styles.subscribeButtonText}>Subscribe Monthly</Text>
                </LinearGradient>
              </TouchableOpacity>
            </View>

            <View style={[styles.pricingCard, styles.bestValueCard]}>
              <View style={styles.bestValueBadge}>
                <Text style={styles.bestValueText}>BEST VALUE</Text>
              </View>
              <View style={styles.pricingHeader}>
                <Text style={styles.pricingPlan}>Annual Plan</Text>
                <View style={styles.pricingPrice}>
                  <Text style={styles.pricingAmount}>$59.99</Text>
                  <Text style={styles.pricingPeriod}> / year</Text>
                </View>
                <Text style={styles.savingsText}>Save 50%</Text>
              </View>
              <TouchableOpacity
                style={styles.subscribeButton}
                onPress={() => handleSubscribe('annual')}
              >
                <LinearGradient
                  colors={['#10b981', '#059669']}
                  start={{ x: 0, y: 0 }}
                  end={{ x: 1, y: 0 }}
                  style={styles.subscribeButtonGradient}
                >
                  <Text style={styles.subscribeButtonText}>Subscribe Annually</Text>
                </LinearGradient>
              </TouchableOpacity>
            </View>

            <Text style={styles.paymentDisclaimer}>
              Payment will be charged to your Apple/Google ID account upon confirmation. Subscriptions auto-renew unless canceled at least 24 hours before the end of the current period.
            </Text>
          </View>
        </View>
      )}

      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>♿ ACCESSIBILITY</Text>
        </View>

        <View style={styles.card}>
          <View style={styles.settingRow}>
            <View style={styles.settingInfo}>
              <Volume2 size={24} color="#6366f1" strokeWidth={2.5} />
              <View style={styles.settingText}>
                <Text style={styles.settingLabel}>Voice Output</Text>
                <Text style={styles.settingDescription}>
                  Enable text-to-speech for AI responses
                </Text>
              </View>
            </View>
            <Switch
              value={voiceEnabled}
              onValueChange={setVoiceEnabled}
              trackColor={{ false: '#e5e7eb', true: '#c7d2fe' }}
              thumbColor={voiceEnabled ? '#6366f1' : '#f3f4f6'}
            />
          </View>
        </View>

        <View style={styles.card}>
          <View style={styles.settingRow}>
            <View style={styles.settingInfo}>
              <VolumeX size={24} color="#6366f1" strokeWidth={2.5} />
              <View style={styles.settingText}>
                <Text style={styles.settingLabel}>Auto-Speak</Text>
                <Text style={styles.settingDescription}>
                  Automatically read AI responses aloud
                </Text>
              </View>
            </View>
            <Switch
              value={autoSpeak}
              onValueChange={setAutoSpeak}
              trackColor={{ false: '#e5e7eb', true: '#c7d2fe' }}
              thumbColor={autoSpeak ? '#6366f1' : '#f3f4f6'}
            />
          </View>
        </View>

        <View style={styles.card}>
          <View style={styles.settingColumn}>
            <View style={styles.settingRow}>
              <Type size={24} color="#6366f1" strokeWidth={2.5} />
              <View style={styles.settingText}>
                <Text style={styles.settingLabel}>Text Size</Text>
                <Text style={styles.settingDescription}>
                  Choose a comfortable reading size
                </Text>
              </View>
            </View>

            <View style={styles.fontSizeOptions}>
              {(['small', 'medium', 'large'] as const).map((size) => (
                <TouchableOpacity
                  key={size}
                  style={[
                    styles.fontSizeButton,
                    fontSize === size && styles.fontSizeButtonActive,
                  ]}
                  onPress={() => setFontSize(size)}
                >
                  <Text
                    style={[
                      styles.fontSizeButtonText,
                      fontSize === size && styles.fontSizeButtonTextActive,
                    ]}
                  >
                    {size.charAt(0).toUpperCase() + size.slice(1)}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>
        </View>
      </View>

      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>🗃️ DATA & PRIVACY</Text>
        </View>

        <TouchableOpacity style={[styles.card, styles.dangerCard]} onPress={clearAllHistory}>
          <View style={styles.settingRow}>
            <View style={styles.settingInfo}>
              <Trash2 size={24} color="#ef4444" strokeWidth={2.5} />
              <View style={styles.settingText}>
                <Text style={[styles.settingLabel, styles.dangerText]}>
                  Clear Conversation History
                </Text>
                <Text style={styles.settingDescription}>
                  Delete all saved recognitions and chats
                </Text>
              </View>
            </View>
            <ChevronRight size={24} color="#ef4444" strokeWidth={2.5} />
          </View>
        </TouchableOpacity>
      </View>

      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>ℹ️ ABOUT</Text>
        </View>

        <View style={styles.card}>
          <View style={styles.aboutRow}>
            <Text style={styles.aboutLabel}>App Version</Text>
            <Text style={styles.aboutValue}>Version 1.2.0 (Build 42)</Text>
          </View>
        </View>

        <TouchableOpacity style={styles.linkCard}>
          <ExternalLink size={20} color="#6366f1" strokeWidth={2.5} />
          <Text style={styles.linkText}>Privacy Policy</Text>
          <ChevronRight size={20} color="#6366f1" strokeWidth={2.5} />
        </TouchableOpacity>

        <TouchableOpacity style={styles.linkCard}>
          <ExternalLink size={20} color="#6366f1" strokeWidth={2.5} />
          <Text style={styles.linkText}>Terms of Service</Text>
          <ChevronRight size={20} color="#6366f1" strokeWidth={2.5} />
        </TouchableOpacity>

        <TouchableOpacity style={styles.linkCard}>
          <ExternalLink size={20} color="#6366f1" strokeWidth={2.5} />
          <Text style={styles.linkText}>Contact Support</Text>
          <ChevronRight size={20} color="#6366f1" strokeWidth={2.5} />
        </TouchableOpacity>
      </View>

      <View style={styles.footer}>
        <Text style={styles.footerText}>Made with care for everyone</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc',
  },
  headerGradient: {
    paddingTop: 60,
    paddingBottom: 24,
    paddingHorizontal: 24,
    borderBottomLeftRadius: 32,
    borderBottomRightRadius: 32,
  },
  header: {
    alignItems: 'center',
  },
  title: {
    fontSize: 36,
    fontWeight: '800',
    color: '#ffffff',
    letterSpacing: -1,
  },
  section: {
    marginTop: 24,
    paddingHorizontal: 20,
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 12,
    paddingHorizontal: 4,
  },
  sectionTitle: {
    fontSize: 13,
    fontWeight: '700',
    color: '#6b7280',
    letterSpacing: 0.5,
  },
  trialBadge: {
    backgroundColor: '#FF9F00',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
    marginLeft: 8,
  },
  trialBadgeText: {
    fontSize: 11,
    fontWeight: '800',
    color: '#ffffff',
    letterSpacing: 0.5,
  },
  card: {
    backgroundColor: '#ffffff',
    borderRadius: 20,
    padding: 20,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 8,
    elevation: 3,
  },
  signInGradient: {
    borderRadius: 16,
    padding: 20,
    margin: -20,
  },
  signInContent: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 16,
  },
  signInText: {
    flex: 1,
  },
  signInTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#ffffff',
    marginBottom: 4,
  },
  signInSubtitle: {
    fontSize: 14,
    color: '#ffffff',
    opacity: 0.9,
  },
  userInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 16,
    marginBottom: 16,
  },
  avatarContainer: {
    shadowColor: '#6366f1',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 5,
  },
  avatar: {
    width: 64,
    height: 64,
    borderRadius: 32,
    justifyContent: 'center',
    alignItems: 'center',
  },
  avatarText: {
    fontSize: 28,
    fontWeight: '800',
    color: '#ffffff',
  },
  userDetails: {
    flex: 1,
  },
  userName: {
    fontSize: 20,
    fontWeight: '700',
    color: '#1e293b',
    marginBottom: 4,
  },
  userEmail: {
    fontSize: 14,
    color: '#64748b',
  },
  manageButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#f8fafc',
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderRadius: 12,
  },
  manageButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#8b5cf6',
  },
  trialCard: {
    borderRadius: 16,
    padding: 24,
    margin: -20,
  },
  trialTitle: {
    fontSize: 20,
    fontWeight: '800',
    color: '#92400e',
    marginBottom: 12,
  },
  trialDescription: {
    fontSize: 15,
    color: '#78350f',
    lineHeight: 22,
    marginBottom: 20,
  },
  trialButton: {
    borderRadius: 16,
    overflow: 'hidden',
    marginBottom: 12,
    shadowColor: '#f59e0b',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 5,
  },
  trialButtonGradient: {
    paddingVertical: 16,
    alignItems: 'center',
  },
  trialButtonText: {
    fontSize: 18,
    fontWeight: '800',
    color: '#ffffff',
    letterSpacing: 0.5,
  },
  trialFooter: {
    fontSize: 13,
    color: '#92400e',
    textAlign: 'center',
    fontWeight: '600',
  },
  proCard: {
    borderRadius: 16,
    padding: 24,
    margin: -20,
  },
  proHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    marginBottom: 12,
  },
  proTitle: {
    fontSize: 20,
    fontWeight: '800',
    color: '#92400e',
  },
  proDescription: {
    fontSize: 15,
    color: '#78350f',
    lineHeight: 22,
    marginBottom: 16,
  },
  manageSubButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#ffffff',
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderRadius: 12,
  },
  manageSubButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#f59e0b',
  },
  upgradeTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#1e293b',
    marginBottom: 20,
    textAlign: 'center',
  },
  pricingCard: {
    backgroundColor: '#f8fafc',
    borderRadius: 16,
    padding: 20,
    marginBottom: 16,
    borderWidth: 2,
    borderColor: '#e2e8f0',
  },
  bestValueCard: {
    borderColor: '#10b981',
    position: 'relative',
  },
  bestValueBadge: {
    position: 'absolute',
    top: -10,
    right: 16,
    backgroundColor: '#10b981',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
    zIndex: 1,
  },
  bestValueText: {
    fontSize: 11,
    fontWeight: '800',
    color: '#ffffff',
    letterSpacing: 0.5,
  },
  pricingHeader: {
    marginBottom: 16,
  },
  pricingPlan: {
    fontSize: 16,
    fontWeight: '700',
    color: '#475569',
    marginBottom: 8,
  },
  pricingPrice: {
    flexDirection: 'row',
    alignItems: 'baseline',
  },
  pricingAmount: {
    fontSize: 32,
    fontWeight: '800',
    color: '#1e293b',
  },
  pricingPeriod: {
    fontSize: 16,
    color: '#64748b',
    fontWeight: '600',
  },
  savingsText: {
    fontSize: 14,
    fontWeight: '700',
    color: '#10b981',
    marginTop: 4,
  },
  subscribeButton: {
    borderRadius: 12,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 8,
    elevation: 5,
  },
  subscribeButtonGradient: {
    paddingVertical: 14,
    alignItems: 'center',
  },
  subscribeButtonText: {
    fontSize: 16,
    fontWeight: '800',
    color: '#ffffff',
    letterSpacing: 0.5,
  },
  paymentDisclaimer: {
    fontSize: 11,
    color: '#94a3b8',
    lineHeight: 16,
    textAlign: 'center',
    marginTop: 8,
  },
  settingRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  settingColumn: {
    gap: 16,
  },
  settingInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
    gap: 12,
  },
  settingText: {
    flex: 1,
  },
  settingLabel: {
    fontSize: 17,
    fontWeight: '600',
    color: '#1e293b',
    marginBottom: 4,
  },
  settingDescription: {
    fontSize: 14,
    color: '#64748b',
    lineHeight: 20,
  },
  dangerCard: {
    borderWidth: 1,
    borderColor: '#fee2e2',
  },
  dangerText: {
    color: '#ef4444',
  },
  fontSizeOptions: {
    flexDirection: 'row',
    gap: 10,
  },
  fontSizeButton: {
    flex: 1,
    paddingVertical: 14,
    borderRadius: 12,
    backgroundColor: '#f1f5f9',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: 'transparent',
  },
  fontSizeButtonActive: {
    backgroundColor: '#eef2ff',
    borderColor: '#6366f1',
  },
  fontSizeButtonText: {
    fontSize: 15,
    fontWeight: '600',
    color: '#64748b',
  },
  fontSizeButtonTextActive: {
    color: '#6366f1',
    fontWeight: '700',
  },
  aboutRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  aboutLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#475569',
  },
  aboutValue: {
    fontSize: 15,
    color: '#64748b',
  },
  linkCard: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    backgroundColor: '#ffffff',
    borderRadius: 16,
    padding: 18,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 8,
    elevation: 2,
  },
  linkText: {
    flex: 1,
    fontSize: 16,
    fontWeight: '600',
    color: '#1e293b',
  },
  footer: {
    alignItems: 'center',
    paddingVertical: 40,
    paddingHorizontal: 40,
  },
  footerText: {
    fontSize: 14,
    color: '#94a3b8',
    textAlign: 'center',
  },
});
