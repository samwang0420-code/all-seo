import { useState, useEffect } from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity, Image, RefreshControl, Alert } from 'react-native';
import { Star, Trash2, Clock, MessageCircle } from 'lucide-react-native';
import { supabase, RecognitionHistory } from '@/lib/supabase';
import { router } from 'expo-router';
import { LinearGradient } from 'expo-linear-gradient';

export default function HistoryTab() {
  const [history, setHistory] = useState<RecognitionHistory[]>([]);
  const [refreshing, setRefreshing] = useState(false);
  const [filter, setFilter] = useState<'all' | 'favorites'>('all');

  useEffect(() => {
    loadHistory();
  }, [filter]);

  const loadHistory = async () => {
    try {
      let query = supabase
        .from('recognition_history')
        .select('*')
        .order('created_at', { ascending: false });

      if (filter === 'favorites') {
        query = query.eq('is_favorite', true);
      }

      const { data, error } = await query;

      if (error) throw error;

      setHistory(data || []);
    } catch (error) {
      console.error('Error loading history:', error);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadHistory();
    setRefreshing(false);
  };

  const deleteItem = async (id: string) => {
    try {
      const { error } = await supabase
        .from('recognition_history')
        .delete()
        .eq('id', id);

      if (error) throw error;

      setHistory((prev) => prev.filter((item) => item.id !== id));
    } catch (error) {
      console.error('Error deleting item:', error);
    }
  };

  const toggleFavorite = async (item: RecognitionHistory) => {
    try {
      const newFavoriteStatus = !item.is_favorite;

      const { error } = await supabase
        .from('recognition_history')
        .update({ is_favorite: newFavoriteStatus })
        .eq('id', item.id);

      if (error) throw error;

      setHistory((prev) =>
        prev.map((h) =>
          h.id === item.id ? { ...h, is_favorite: newFavoriteStatus } : h
        )
      );
    } catch (error) {
      console.error('Error toggling favorite:', error);
    }
  };

  const rateResult = async (item: RecognitionHistory, rating: number) => {
    try {
      const { error } = await supabase
        .from('recognition_history')
        .update({ rating })
        .eq('id', item.id);

      if (error) throw error;

      setHistory((prev) =>
        prev.map((h) => (h.id === item.id ? { ...h, rating } : h))
      );

      Alert.alert(
        'Thank You!',
        'Your feedback helps us train the model more accurately and assist more people in need.'
      );
    } catch (error) {
      console.error('Error rating result:', error);
      Alert.alert('Error', 'Failed to save rating. Please try again.');
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;

    return date.toLocaleDateString();
  };

  const renderRatingStars = (item: RecognitionHistory) => {
    const currentRating = item.rating || 0;

    return (
      <View style={styles.ratingContainer}>
        <Text style={styles.ratingLabel}>Rate this result:</Text>
        <View style={styles.starsContainer}>
          {[1, 2, 3, 4, 5].map((star) => (
            <TouchableOpacity
              key={star}
              onPress={(e) => {
                e.stopPropagation();
                rateResult(item, star);
              }}
              style={styles.starButton}
            >
              <Star
                size={24}
                color={star <= currentRating ? '#fbbf24' : '#d1d5db'}
                fill={star <= currentRating ? '#fbbf24' : 'none'}
                strokeWidth={2}
              />
            </TouchableOpacity>
          ))}
        </View>
      </View>
    );
  };

  const renderItem = ({ item }: { item: RecognitionHistory }) => (
    <View style={styles.card}>
      <TouchableOpacity
        style={styles.cardMain}
        onPress={() => router.push({ pathname: '/chat', params: { imageUri: item.image_url } })}
        activeOpacity={0.7}
      >
        <Image source={{ uri: item.image_url }} style={styles.thumbnail} />

        <View style={styles.cardContent}>
          <View style={styles.cardHeader}>
            <Text style={styles.objectName} numberOfLines={1}>
              {item.object_name}
            </Text>
            <TouchableOpacity
              style={styles.favoriteIconButton}
              onPress={(e) => {
                e.stopPropagation();
                toggleFavorite(item);
              }}
            >
              <Star
                size={20}
                color={item.is_favorite ? '#fbbf24' : '#9ca3af'}
                fill={item.is_favorite ? '#fbbf24' : 'none'}
              />
            </TouchableOpacity>
          </View>

          <Text style={styles.explanation} numberOfLines={2}>
            {item.explanation}
          </Text>

          <View style={styles.cardFooter}>
            <View style={styles.timeContainer}>
              <Clock size={14} color="#9ca3af" />
              <Text style={styles.timeText}>{formatDate(item.created_at)}</Text>
            </View>
            <TouchableOpacity
              style={styles.deleteButton}
              onPress={(e) => {
                e.stopPropagation();
                deleteItem(item.id);
              }}
            >
              <Trash2 size={16} color="#ef4444" />
            </TouchableOpacity>
          </View>
        </View>
      </TouchableOpacity>

      {renderRatingStars(item)}
    </View>
  );

  const renderEmpty = () => (
    <View style={styles.emptyContainer}>
      <MessageCircle size={72} color="#cbd5e1" strokeWidth={1.5} />
      <Text style={styles.emptyTitle}>
        {filter === 'favorites' ? 'No Favorites Yet' : 'No History Yet'}
      </Text>
      <Text style={styles.emptyText}>
        {filter === 'favorites'
          ? 'Mark items as favorites to see them here'
          : 'Start by capturing or uploading a photo to identify objects'}
      </Text>
    </View>
  );

  const renderHeader = () => (
    <View style={styles.feedbackBanner}>
      <LinearGradient
        colors={['#3b82f6', '#8b5cf6']}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
        style={styles.bannerGradient}
      >
        <View style={styles.bannerContent}>
          <View style={styles.bannerIconContainer}>
            <Star size={28} color="#fbbf24" fill="#fbbf24" />
          </View>
          <View style={styles.bannerTextContainer}>
            <Text style={styles.bannerTitle}>Help Us Improve</Text>
            <Text style={styles.bannerText}>
              Based on your feedback, we can train the model more accurately, which will help more people in need.
            </Text>
          </View>
        </View>
      </LinearGradient>
    </View>
  );

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>History</Text>
        <View style={styles.filterContainer}>
          <TouchableOpacity
            style={[styles.filterButton, filter === 'all' && styles.filterButtonActive]}
            onPress={() => setFilter('all')}
          >
            <Text style={[styles.filterText, filter === 'all' && styles.filterTextActive]}>
              All
            </Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.filterButton, filter === 'favorites' && styles.filterButtonActive]}
            onPress={() => setFilter('favorites')}
          >
            <Star
              size={16}
              color={filter === 'favorites' ? '#ffffff' : '#6b7280'}
              fill={filter === 'favorites' ? '#ffffff' : 'none'}
            />
            <Text style={[styles.filterText, filter === 'favorites' && styles.filterTextActive]}>
              Favorites
            </Text>
          </TouchableOpacity>
        </View>
      </View>

      <FlatList
        data={history}
        renderItem={renderItem}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.listContent}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        ListHeaderComponent={history.length > 0 ? renderHeader : null}
        ListEmptyComponent={renderEmpty}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc',
  },
  header: {
    backgroundColor: '#ffffff',
    paddingHorizontal: 20,
    paddingTop: 60,
    paddingBottom: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#e5e7eb',
  },
  title: {
    fontSize: 32,
    fontWeight: '800',
    color: '#1f2937',
    marginBottom: 16,
  },
  filterContainer: {
    flexDirection: 'row',
    gap: 8,
  },
  filterButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    backgroundColor: '#f3f4f6',
  },
  filterButtonActive: {
    backgroundColor: '#3b82f6',
  },
  filterText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#6b7280',
  },
  filterTextActive: {
    color: '#ffffff',
  },
  listContent: {
    padding: 16,
    gap: 16,
  },
  feedbackBanner: {
    marginBottom: 8,
    borderRadius: 16,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 12,
    elevation: 6,
  },
  bannerGradient: {
    padding: 20,
  },
  bannerContent: {
    flexDirection: 'row',
    gap: 16,
  },
  bannerIconContainer: {
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  bannerTextContainer: {
    flex: 1,
  },
  bannerTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#ffffff',
    marginBottom: 6,
  },
  bannerText: {
    fontSize: 14,
    color: '#ffffff',
    lineHeight: 20,
    opacity: 0.95,
  },
  card: {
    backgroundColor: '#ffffff',
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#e5e7eb',
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 8,
    elevation: 3,
  },
  cardMain: {
    flexDirection: 'row',
    padding: 12,
    gap: 12,
  },
  thumbnail: {
    width: 90,
    height: 90,
    borderRadius: 12,
    backgroundColor: '#f3f4f6',
  },
  cardContent: {
    flex: 1,
    justifyContent: 'space-between',
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    justifyContent: 'space-between',
    marginBottom: 6,
  },
  objectName: {
    flex: 1,
    fontSize: 18,
    fontWeight: '700',
    color: '#1f2937',
  },
  favoriteIconButton: {
    padding: 4,
    marginLeft: 8,
  },
  explanation: {
    fontSize: 14,
    color: '#6b7280',
    lineHeight: 20,
    flex: 1,
  },
  cardFooter: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginTop: 4,
  },
  timeContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  timeText: {
    fontSize: 12,
    color: '#9ca3af',
    fontWeight: '500',
  },
  deleteButton: {
    padding: 6,
  },
  ratingContainer: {
    paddingHorizontal: 16,
    paddingVertical: 14,
    backgroundColor: '#f9fafb',
    borderTopWidth: 1,
    borderTopColor: '#e5e7eb',
  },
  ratingLabel: {
    fontSize: 13,
    fontWeight: '600',
    color: '#6b7280',
    marginBottom: 10,
    textAlign: 'center',
  },
  starsContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 8,
  },
  starButton: {
    padding: 4,
  },
  emptyContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 80,
    paddingHorizontal: 40,
  },
  emptyTitle: {
    fontSize: 22,
    fontWeight: '700',
    color: '#64748b',
    marginTop: 20,
    marginBottom: 8,
  },
  emptyText: {
    fontSize: 16,
    color: '#94a3b8',
    textAlign: 'center',
    lineHeight: 24,
  },
});
