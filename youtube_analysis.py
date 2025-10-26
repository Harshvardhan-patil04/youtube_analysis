import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta
import re

class YouTubeAnalyzer:
    """
    A class to analyze YouTube channel statistics and visualize engagement trends
    by category and video length.
    """
    
    def __init__(self, csv_file):
        """
        Initialize the analyzer with a CSV file.
        
        Parameters:
        -----------
        csv_file : str
            Path to the CSV file containing YouTube data
        """
        self.data = None
        self.category_stats = None
        self.length_stats = None
        self.csv_file = csv_file
        
    def load_data(self):
        """
        Load and clean the CSV data with flexible column name handling.
        """
        # Read CSV with flexible handling
        df = pd.read_csv(self.csv_file)
        
        # Standardize column names (handle variations)
        column_mapping = {}
        for col in df.columns:
            col_lower = col.lower().strip()
            if col_lower in ['title']:
                column_mapping[col] = 'title'
            elif col_lower in ['category', 'channel_title', 'channeltitle']:
                column_mapping[col] = 'category'
            elif col_lower in ['views', 'view_count', 'viewcount']:
                column_mapping[col] = 'views'
            elif col_lower in ['likes', 'like_count', 'likecount']:
                column_mapping[col] = 'likes'
            elif col_lower in ['comments', 'comment_count', 'commentcount']:
                column_mapping[col] = 'comments'
            elif col_lower in ['duration', 'video_length', 'length']:
                column_mapping[col] = 'duration'
            elif col_lower in ['subscribers', 'subscriber_count']:
                column_mapping[col] = 'subscribers'
        
        # Rename columns
        df = df.rename(columns=column_mapping)
        
        # Ensure required columns exist
        required_cols = ['title', 'category', 'views', 'likes', 'comments', 'duration']
        for col in required_cols:
            if col not in df.columns:
                if col == 'category':
                    df['category'] = 'Unknown'
                else:
                    df[col] = 0
        
        # Clean and convert data types
        df['views'] = pd.to_numeric(df['views'], errors='coerce').fillna(0).astype(int)
        df['likes'] = pd.to_numeric(df['likes'], errors='coerce').fillna(0).astype(int)
        df['comments'] = pd.to_numeric(df['comments'], errors='coerce').fillna(0).astype(int)
        df['duration'] = df['duration'].apply(self._parse_duration)
        
        # Filter out invalid entries
        df = df[df['views'] > 0]
        
        # Add calculated fields
        df['engagement_rate'] = ((df['likes'] + df['comments']) / df['views'] * 100).round(2)
        df['duration_minutes'] = (df['duration'] / 60).round(2)
        
        # Categorize by length
        df['length_category'] = pd.cut(
            df['duration_minutes'],
            bins=[0, 5, 15, 30, float('inf')],
            labels=['Short (0-5 min)', 'Medium (5-15 min)', 'Long (15-30 min)', 'Very Long (30+ min)']
        )
        
        self.data = df
        print(f"✓ Data loaded successfully: {len(df)} videos")
        return self
    
    def _parse_duration(self, duration):
        """
        Parse duration from various formats to seconds.
        
        Parameters:
        -----------
        duration : str, int, or float
            Duration in various formats
            
        Returns:
        --------
        int : Duration in seconds
        """
        if pd.isna(duration):
            return 0
        
        # If already a number, return it
        if isinstance(duration, (int, float)):
            return int(duration)
        
        duration_str = str(duration).strip()
        
        # Handle HH:MM:SS or MM:SS format
        if ':' in duration_str:
            parts = duration_str.split(':')
            parts = [int(p) for p in parts]
            if len(parts) == 3:  # HH:MM:SS
                return parts[0] * 3600 + parts[1] * 60 + parts[2]
            elif len(parts) == 2:  # MM:SS
                return parts[0] * 60 + parts[1]
            else:
                return int(parts[0])
        
        # Handle YouTube API format (PT1H2M3S)
        match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
        if match:
            hours = int(match.group(1) or 0)
            minutes = int(match.group(2) or 0)
            seconds = int(match.group(3) or 0)
            return hours * 3600 + minutes * 60 + seconds
        
        # Try to parse as plain number
        try:
            return int(float(duration_str))
        except:
            return 0
    
    def analyze_by_category(self):
        """
        Analyze video performance grouped by category.
        """
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        # Group by category and calculate statistics
        category_stats = self.data.groupby('category').agg({
            'title': 'count',
            'views': ['sum', 'mean'],
            'likes': ['sum', 'mean'],
            'comments': ['sum', 'mean'],
            'engagement_rate': 'mean'
        }).round(0)
        
        # Flatten column names
        category_stats.columns = ['video_count', 'total_views', 'avg_views', 
                                   'total_likes', 'avg_likes', 'total_comments', 
                                   'avg_comments', 'avg_engagement_rate']
        
        # Sort by average views
        category_stats = category_stats.sort_values('avg_views', ascending=False)
        
        self.category_stats = category_stats
        print("\n✓ Category analysis complete")
        return self
    
    def analyze_by_length(self):
        """
        Analyze video performance grouped by video length.
        """
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        # Group by length category
        length_stats = self.data.groupby('length_category', observed=True).agg({
            'title': 'count',
            'views': ['sum', 'mean'],
            'likes': ['sum', 'mean'],
            'comments': ['sum', 'mean'],
            'engagement_rate': 'mean'
        }).round(0)
        
        # Flatten column names
        length_stats.columns = ['video_count', 'total_views', 'avg_views',
                                'total_likes', 'avg_likes', 'total_comments',
                                'avg_comments', 'avg_engagement_rate']
        
        self.length_stats = length_stats
        print("✓ Length analysis complete")
        return self
    
    def display_summary(self):
        """
        Display overall summary statistics.
        """
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        print("\n" + "="*60)
        print("📊 YOUTUBE CHANNEL ANALYTICS SUMMARY")
        print("="*60)
        print(f"\n📹 Total Videos: {len(self.data):,}")
        print(f"👁️  Total Views: {self.data['views'].sum():,}")
        print(f"👍 Total Likes: {self.data['likes'].sum():,}")
        print(f"💬 Total Comments: {self.data['comments'].sum():,}")
        print(f"📈 Avg Engagement Rate: {self.data['engagement_rate'].mean():.2f}%")
        print(f"\n🏷️  Categories: {self.data['category'].nunique()}")
        print(f"⏱️  Avg Video Duration: {self.data['duration_minutes'].mean():.1f} minutes")
        print("="*60 + "\n")
        return self
    
    def plot_category_performance(self):
        """
        Create visualizations for category performance.
        """
        if self.category_stats is None:
            raise ValueError("Category analysis not done. Call analyze_by_category() first.")
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('📊 Performance by Category', fontsize=16, fontweight='bold')
        
        # 1. Average Views by Category
        ax1 = axes[0, 0]
        self.category_stats['avg_views'].plot(kind='bar', ax=ax1, color='steelblue')
        ax1.set_title('Average Views by Category', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Category')
        ax1.set_ylabel('Average Views')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(axis='y', alpha=0.3)
        
        # 2. Engagement Rate by Category
        ax2 = axes[0, 1]
        self.category_stats['avg_engagement_rate'].plot(kind='barh', ax=ax2, color='coral')
        ax2.set_title('Engagement Rate by Category', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Engagement Rate (%)')
        ax2.set_ylabel('Category')
        ax2.grid(axis='x', alpha=0.3)
        
        # 3. Video Count Distribution
        ax3 = axes[1, 0]
        self.category_stats['video_count'].plot(kind='pie', ax=ax3, autopct='%1.1f%%')
        ax3.set_title('Video Distribution by Category', fontsize=12, fontweight='bold')
        ax3.set_ylabel('')
        
        # 4. Likes vs Comments by Category
        ax4 = axes[1, 1]
        x = np.arange(len(self.category_stats))
        width = 0.35
        ax4.bar(x - width/2, self.category_stats['avg_likes'], width, label='Avg Likes', color='#ef4444')
        ax4.bar(x + width/2, self.category_stats['avg_comments'], width, label='Avg Comments', color='#10b981')
        ax4.set_title('Average Engagement by Category', fontsize=12, fontweight='bold')
        ax4.set_xlabel('Category')
        ax4.set_ylabel('Count')
        ax4.set_xticks(x)
        ax4.set_xticklabels(self.category_stats.index, rotation=45, ha='right')
        ax4.legend()
        ax4.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        return self
    
    def plot_length_performance(self):
        """
        Create visualizations for video length performance.
        """
        if self.length_stats is None:
            raise ValueError("Length analysis not done. Call analyze_by_length() first.")
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 10))
        fig.suptitle('⏱️ Performance by Video Length', fontsize=16, fontweight='bold')
        
        # 1. Average Views by Length
        ax1 = axes[0, 0]
        self.length_stats['avg_views'].plot(kind='bar', ax=ax1, color='#3b82f6')
        ax1.set_title('Average Views by Video Length', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Video Length')
        ax1.set_ylabel('Average Views')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(axis='y', alpha=0.3)
        
        # 2. Engagement Rate by Length
        ax2 = axes[0, 1]
        self.length_stats['avg_engagement_rate'].plot(kind='bar', ax=ax2, color='#8b5cf6')
        ax2.set_title('Engagement Rate by Video Length', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Video Length')
        ax2.set_ylabel('Engagement Rate (%)')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(axis='y', alpha=0.3)
        
        # 3. Video Count by Length
        ax3 = axes[1, 0]
        self.length_stats['video_count'].plot(kind='bar', ax=ax3, color='#10b981')
        ax3.set_title('Video Count by Length Category', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Video Length')
        ax3.set_ylabel('Number of Videos')
        ax3.tick_params(axis='x', rotation=45)
        ax3.grid(axis='y', alpha=0.3)
        
        # 4. Likes vs Comments by Length
        ax4 = axes[1, 1]
        x = np.arange(len(self.length_stats))
        width = 0.35
        ax4.bar(x - width/2, self.length_stats['avg_likes'], width, label='Avg Likes', color='#ef4444')
        ax4.bar(x + width/2, self.length_stats['avg_comments'], width, label='Avg Comments', color='#f59e0b')
        ax4.set_title('Average Engagement by Video Length', fontsize=12, fontweight='bold')
        ax4.set_xlabel('Video Length')
        ax4.set_ylabel('Count')
        ax4.set_xticks(x)
        ax4.set_xticklabels(self.length_stats.index, rotation=45, ha='right')
        ax4.legend()
        ax4.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        return self
    
    def generate_insights(self):
        """
        Generate key insights from the analysis.
        """
        if self.category_stats is None or self.length_stats is None:
            raise ValueError("Complete analysis not done. Run analyze_by_category() and analyze_by_length() first.")
        
        print("\n" + "="*60)
        print("💡 KEY INSIGHTS")
        print("="*60)
        
        # Category insights
        print("\n🏆 Top Performing Category:")
        top_category = self.category_stats.index[0]
        top_views = self.category_stats.iloc[0]['avg_views']
        print(f"   {top_category}: {top_views:,.0f} avg views")
        
        # Engagement insights
        print("\n📈 Highest Engagement Rate:")
        top_engagement_cat = self.category_stats['avg_engagement_rate'].idxmax()
        top_engagement_rate = self.category_stats.loc[top_engagement_cat, 'avg_engagement_rate']
        print(f"   {top_engagement_cat}: {top_engagement_rate:.2f}%")
        
        # Length insights
        print("\n⏱️  Optimal Video Length:")
        best_length = self.length_stats['avg_views'].idxmax()
        best_length_views = self.length_stats.loc[best_length, 'avg_views']
        print(f"   {best_length}: {best_length_views:,.0f} avg views")
        
        # Engagement by length
        print("\n📊 Best Engagement by Length:")
        best_engagement_length = self.length_stats['avg_engagement_rate'].idxmax()
        best_engagement_rate_length = self.length_stats.loc[best_engagement_length, 'avg_engagement_rate']
        print(f"   {best_engagement_length}: {best_engagement_rate_length:.2f}%")
        
        print("\n" + "="*60 + "\n")
        return self

if __name__ == "__main__":
    # Initialize analyzer
    analyzer = YouTubeAnalyzer(r'C:\Users\user\Downloads\youtube_dataset.csv')
    
    # Run full analysis pipeline
    analyzer.load_data() \
           .display_summary() \
           .analyze_by_category() \
           .analyze_by_length() \
           .generate_insights() \
           .plot_category_performance() \
           .plot_length_performance()
    
    # Access the data for further analysis
    print("\n📊 Category Statistics:")
    print(analyzer.category_stats)
    
    print("\n⏱️  Length Statistics:")
    print(analyzer.length_stats)
