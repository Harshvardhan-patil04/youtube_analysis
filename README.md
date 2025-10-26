📊 YouTube Channel Statistics Analyzer
A comprehensive Python tool for analyzing YouTube channel statistics and understanding engagement trends by category and video length.

🎯 Features

📈 Data Analysis: Comprehensive statistical analysis of YouTube video performance
🏷️ Category Insights: Compare performance across different content categories
⏱️ Length Analysis: Understand how video duration affects engagement
📊 Visualizations: Beautiful charts and graphs using Matplotlib
🔍 Key Insights: Automated insight generation for quick decision-making
🧹 Data Cleaning: Flexible CSV parsing with automatic data type handling

📸 What You'll Get
Analysis Output:

Total videos, views, likes, and comments
Engagement rates by category and length
Average performance metrics
Distribution visualizations
Actionable insights

Visualizations:

Average views by category (Bar Chart)
Engagement rate comparison (Horizontal Bar Chart)
Video distribution (Pie Chart)
Performance by video length (Bar Chart)
Likes vs Comments analysis (Grouped Bar Chart)

🚀 Quick Start
Prerequisites
Make sure you have Python 3.7+ installed. Then install the required packages:
bashpip install pandas numpy matplotlib seaborn
Installation

Clone or Download the repository:

bashgit clone https://github.com/yourusername/youtube-analyzer.git
cd youtube-analyzer

Install Dependencies:

bashpip install -r requirements.txt

📋 CSV File Format
Your CSV file should contain the following columns (flexible naming supported):
ColumnAlternative NamesDescriptiontitleTitleVideo titlecategoryCategory, channel_title, channelTitleContent categoryviewsViews, view_count, viewCountNumber of viewslikesLikes, like_count, likeCountNumber of likescommentsComments, comment_count, commentCountNumber of commentsdurationDuration, video_length, lengthVideo durationsubscribersSubscribers, subscriber_countChannel subscribers (optional)
