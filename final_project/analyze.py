#                           ..\|||||/',//
#                        `\\`\           ///
#                      `\`        |  /    '/'
#                   -.`\      \        |   // //
#                  _- -.   \    |         /   /.
#                -                 |      /  .'.'
#               -- - `.  \            /       .'.'
#              -_  -  `  \   \     /    /   /  .'-'
#             -_  _ -` |\      |        ' '  -'-''
#             -___  '`/  `  \      /  /   _--   -'_
#             _  _/ '`  \       |    /|       _ -
#             _.__  / `.            //|  _ -   _ -_
#             _   '| \._    \ __.--// |     -  __
#            _-  '  `  \`.  .'    (/  | -  _    -
#            ' '|  \    \ `'          |\   _  _-_
#            '/          \ |      ` _   `.  _ _
#             \ |   ` `  >/        '      `-.
#            \|       .-' |_        db       `.
#           \       .'    d|        MP         \       ___      _.-
#          `  ` | .'      Vb         '   |'     \   .-'   `----'
#        `\     .'  /      \         .-' |      _\.'
#       \     .'            |       ---.___    .'       `
#            /      -        \._mm) `-._ /   .'                 _.-
#      `\   /       .         `"Y"       --.'         .--------'
#     \\   /         `.    `-._____      .'        .-'
#         /            \           `-.  /        .'
#     )  /              '.           .-'       .'
#     ` /              '  -._.-    .'        .'
#    ) '                '      `..'        .'
#    .                ' '  `   .'        .'`
#   `                   '    .'        .'  `
#   `                  ' '.-'        .'   `
#   `               _   .'         .'  .`
#    '              _`.'         .'  .`
#     '.        .-'_ `_'       .'   `
#       -      .' _  `_`    .-'  .`
#       )          `-._`  .'    `
#        '__   _.-_  `  .'   .`         
#           '.'     `' /__. `         88                                  88 
#           /         /_.-'           ""                                  88
#                                                                         88  
#   ,adPPYba,  ,adPPYb,d8 88       88 88 8b,dPPYba, 8b,dPPYba,  ,adPPYba, 88  
#   I8[    "" a8"    `Y88 88       88 88 88P'   "Y8 88P'   "Y8 a8P_____88 88  
#    `"Y8ba,  8b       88 88       88 88 88         88         8PP""""""" 88  
#   aa    ]8I "8a    ,d88 "8a,   ,a88 88 88         88         "8b,   ,aa 88  
#   `"YbbdP"'  `"YbbdP'88  `"YbbdP'Y8 88 88         88          `"Ybbd8"' 88  
#                        88                                                     
#                        88                                                     
"""
Central Park Squirrel Analysis

Description: This script analyzes data from the 2018 Central Park Squirrel Census and generates visualizations and data outputs for the following questions:
1. Squirrel sighting concentration (heatmap).
2. Fur color distribution (bar chart).
3. AM/PM movement patterns (heatmaps).
4. Common activity distribution (bar charts).
5. Unique actions performed by squirrels (CSV file).

How to use this script:
- Place raw data in the same directory as this script. Data can be sourced from this url: https://data.cityofnewyork.us/Environment/2018-Central-Park-Squirrel-Census-Squirrel-Data/vfnx-vebw/about_data
- Run the script using Python 3.x.
- Outputs will be saved in the same directory.

The script will output html interactive heatmaps, and multiple bar charts.

This script requires the following dependencies to be installed:
- Python 3.x
- Libraries: pandas, folium, seaborn, matplotlib, wordcloud
"""

# import necessary libraries
import pandas as pd
import folium
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
from matplotlib import rcParams, font_manager
import seaborn as sns

# set up fonts for plotting
font_dirs = ['/data/users/freycv9470/my_ds150/final_project/fonts']  # path to fonts folder
font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
for font_file in font_files:
    font_manager.fontManager.addfont(font_file)

# set fonts
rcParams['font.family'] = 'Playfair Display'
rcParams['font.weight'] = 'bold'

# constants for file paths
data_file = '2018_Central_Park_Squirrel_Census_-_Squirrel_Data_20241213.csv'

# load the dataset
df = pd.read_csv(data_file)

# rename columns to follow good data practices
column_renaming = {
    'X': 'longitude',
    'Y': 'latitude',
    'Unique Squirrel ID': 'unique_squirrel_id',
    'Hectare': 'hectare',
    'Shift': 'shift',
    'Date': 'date',
    'Hectare Squirrel Number': 'hectare_squirrel_number',
    'Age': 'age',
    'Primary Fur Color': 'primary_fur_color',
    'Highlight Fur Color': 'highlight_fur_color',
    'Combination of Primary and Highlight Color': 'fur_color_combination',
    'Color notes': 'color_notes',
    'Location': 'location',
    'Above Ground Sighter Measurement': 'above_ground_measurement',
    'Specific Location': 'specific_location',
    'Running': 'running',
    'Chasing': 'chasing',
    'Climbing': 'climbing',
    'Eating': 'eating',
    'Foraging': 'foraging',
    'Other Activities': 'other_activities',
    'Kuks': 'kuks',
    'Quaas': 'quaas',
    'Moans': 'moans',
    'Tail flags': 'tail_flags',
    'Tail twitches': 'tail_twitches',
    'Approaches': 'approaches',
    'Indifferent': 'indifferent',
    'Runs from': 'runs_from',
    'Lat/Long': 'lat_long'
}
df.rename(columns=column_renaming, inplace=True)

# ==============================================================================#
# question 1: squirrel sighting concentration in central park
# ==============================================================================#
"""
cleans data and generates a heatmap of squirrel locations in central park.

args:
    data (pd.DataFrame): raw data from the census.

returns:
    pd.DataFrame: cleaned data with latitude, longitude, and unique ids.
"""

def clean_squirrel_concentration_data(data):

    concentration_data = data[['latitude', 'longitude', 'unique_squirrel_id', 'date', 'lat_long']].dropna(how='any')
    concentration_data.to_csv('location.csv', index=False)

    # generate heatmap
    map_data = concentration_data[['latitude', 'longitude']].values.tolist()
    map = folium.Map(location=[40.7829, -73.9654], zoom_start=14)
    HeatMap(map_data, radius=10).add_to(map)
    map.save('squirrel_concentration_heatmap.html')

    return concentration_data

# ==============================================================================#
# question 2: fur colors
# ==============================================================================#
"""
analyzes fur color distribution and generates a bar chart.

args:
    data (pd.DataFrame): raw data from the census.

returns:
    pd.DataFrame: cleaned data with fur color information.
"""

def clean_fur_color_data(data):

    fur_data = data[['latitude', 'longitude', 'unique_squirrel_id', 'primary_fur_color', 'highlight_fur_color', 'lat_long']]
    fur_data = fur_data.dropna(subset=['primary_fur_color'])
    fur_data.to_csv('fur.csv', index=False)

    # count occurrences of each fur color
    fur_color_counts = fur_data['primary_fur_color'].value_counts()

    # define squirrel-specific colors
    fur_colors = {
        "Gray": "#a8a8a8",
        "Cinnamon": "#d2691e",
        "Black": "#000000",
    }

    # create bar chart
    plt.figure(figsize=(10, 6))
    sns.barplot(
        x=fur_color_counts.index,
        y=fur_color_counts.values,
        palette=[fur_colors.get(color, "#44444499") for color in fur_color_counts.index],
        alpha=0.7
    )
    plt.title("distribution of primary fur colors among squirrels", fontsize=16, color="#303030", weight='bold')
    plt.xlabel("primary fur color", fontsize=14, color="#303030", weight='bold')
    plt.ylabel("count", fontsize=14, color="#303030", weight='bold')
    plt.xticks(fontsize=12, color="#303030", weight='bold')
    plt.yticks(fontsize=12, color="#303030", weight='bold')

    # save chart
    plt.tight_layout()
    plt.savefig("fur_color_distribution_pretty.png", dpi=300, transparent=True)
    plt.close()

    return fur_data

# ==============================================================================
# Question 3: AM/PM Movement Patterns
# ==============================================================================

"""
cleans data for am/pm movement pattern analysis and generates heatmaps.

args:
    data (pd.DataFrame): raw data from the census.

returns:
    pd.DataFrame: cleaned data for am/pm movement patterns.
"""

def clean_am_pm_data(data):
    temporal_data = data[['latitude', 'longitude', 'unique_squirrel_id', 'shift', 'lat_long']].dropna(how='any')
    temporal_data.to_csv('temporal.csv', index=False)

    # filter data for am and pm
    am_data = temporal_data[temporal_data['shift'] == 'AM'][['latitude', 'longitude']]
    pm_data = temporal_data[temporal_data['shift'] == 'PM'][['latitude', 'longitude']]

    # create am heatmap
    am_map = folium.Map(location=[40.7829, -73.9654], zoom_start=14)
    HeatMap(am_data.values.tolist(), radius=10).add_to(am_map)
    am_map.save('squirrel_am_heatmap.html')

    # create pm heatmap
    pm_map = folium.Map(location=[40.7829, -73.9654], zoom_start=14)
    HeatMap(pm_data.values.tolist(), radius=10).add_to(pm_map)
    pm_map.save('squirrel_pm_heatmap.html')

    return temporal_data

# ==============================================================================
# Question 4: Common Activity Distribution
# ==============================================================================

"""
 script: activity data visualization
 purpose: this script analyzes and visualizes squirrel activity data, creating bar charts for exercise, speech, and tail movement activities.
 args:
     - data: pandas dataframe containing raw squirrel activity data.
 outputs:
     - exercise_distribution_true.png: bar chart showing exercise activity counts.
     - speech_distribution_true.png: bar chart showing speech activity counts.
     - tail_movement_distribution_true.png: bar chart showing tail movement activity counts.
"""

# helper function to set fonts
def set_fonts():
    font_dirs = ['/data/users/freycv9470/my_ds150/final_project/fonts']  # path to fonts folder
    font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)
    
    # set playfair display font (ensure it's available in the font manager)
    rcParams['font.family'] = 'Playfair Display'  # assuming 'playfair display' is in the fonts directory
    rcParams['font.weight'] = 'bold'  # add more weight to the font

# function to plot exercise (running, chasing, climbing) bar chart
def plot_exercise_data(true_data):
    # filter data for exercise categories
    exercise_data = true_data[true_data['Activity'].isin(['running', 'chasing', 'climbing'])]
    
    # define squirrel-specific colors for exercise activities
    fur_colors = ['#a8a8a8', '#d2691e', '#000000']  # gray, cinnamon, black
    
    # create a bar chart for exercise data
    plt.figure(figsize=(12, 8))
    ax1 = sns.countplot(data=exercise_data, x='Activity', palette=fur_colors, edgecolor='#2a2a2a')
    
    # set chart title, labels, and ticks
    plt.title('exercise distribution (only true values)', fontsize=16, fontweight='bold', color='#303030')
    plt.xlabel('exercise activity', fontsize=14, color='#303030', weight='bold')
    plt.ylabel('count', fontsize=14, color='#303030', weight='bold')
    plt.xticks(rotation=0, fontsize=12, color='#303030', weight='bold')  # set x-axis labels flat
    plt.yticks(fontsize=12, color='#303030', weight='bold')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # modify chart boundaries to be thicker and embossed with slightly darker color
    ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_linewidth(2.5)
        spine.set_color('#2a2a2a')

    plt.tight_layout()
    plt.savefig('exercise_distribution_true.png', dpi=300, transparent=True)
    plt.show()

# function to plot speech data bar chart
def plot_speech_data(true_data):
    # filter data for speech categories
    speech_data = true_data[true_data['Category'] == 'speech']
    
    # define squirrel-specific colors for speech activities
    fur_colors = ['#a8a8a8', '#d2691e', '#000000']  # gray, cinnamon, black
    
    # create a bar chart for speech data
    plt.figure(figsize=(12, 8))
    ax2 = sns.countplot(data=speech_data, x='Activity', palette=fur_colors, edgecolor='#2a2a2a')
    
    # set chart title, labels, and ticks
    plt.title('speech distribution (only true values)', fontsize=16, fontweight='bold', color='#303030')
    plt.xlabel('speech activity', fontsize=14, color='#303030', weight='bold')
    plt.ylabel('count', fontsize=14, color='#303030', weight='bold')
    plt.xticks(rotation=0, fontsize=12, color='#303030', weight='bold')  # set x-axis labels flat
    plt.yticks(fontsize=12, color='#303030', weight='bold')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # modify chart boundaries to be thicker and embossed with slightly darker color
    ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_linewidth(2.5)
        spine.set_color('#2a2a2a')

    plt.tight_layout()
    plt.savefig('speech_distribution_true.png', dpi=300, transparent=True)
    plt.show()

# function to plot tail movement data bar chart
def plot_tail_movement_data(true_data):
    # filter data for tail movement categories
    tail_movement_data = true_data[true_data['Category'] == 'tail movement']
    
    # define squirrel-specific colors for tail movement activities
    fur_colors = ['#a8a8a8', '#d2691e', '#000000']  # gray, cinnamon, black
    
    # create a bar chart for tail movement data
    plt.figure(figsize=(12, 8))
    ax3 = sns.countplot(data=tail_movement_data, x='Activity', palette=fur_colors, edgecolor='#2a2a2a')
    
    # set chart title, labels, and ticks
    plt.title('tail movement distribution (only true values)', fontsize=16, fontweight='bold', color='#303030')
    plt.xlabel('tail movement activity', fontsize=14, color='#303030', weight='bold')
    plt.ylabel('count', fontsize=14, color='#303030', weight='bold')
    plt.xticks(rotation=0, fontsize=12, color='#303030', weight='bold')  # set x-axis labels flat
    plt.yticks(fontsize=12, color='#303030', weight='bold')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # modify chart boundaries to be thicker and embossed with slightly darker color
    ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_linewidth(2.5)
        spine.set_color('#2a2a2a')

    plt.tight_layout()
    plt.savefig('tail_movement_distribution_true.png', dpi=300, transparent=True)
    plt.show()

# main function to clean and process the data
def clean_activity_data(data):
    # set fonts
    set_fonts()

    # cleans data for common activity distribution analysis
    activity_data = data[['latitude', 'longitude', 'unique_squirrel_id', 'running', 'chasing', 'climbing', 'eating', 'foraging', 'kuks', 'quaas', 'moans', 'tail_flags', 'tail_twitches', 'lat_long']].dropna(how='all')
    activity_data.to_csv('activity.csv', index=False)

    # separate the binary columns into categories
    activities_columns = ['running', 'chasing', 'climbing', 'eating', 'foraging']
    speech_columns = ['kuks', 'quaas', 'moans']
    tail_movement_columns = ['tail_flags', 'tail_twitches']

    # prepare the data for plotting
    activity_data_categories = {
        'activities': activity_data[activities_columns],
        'speech': activity_data[speech_columns],
        'tail movement': activity_data[tail_movement_columns],
    }

    # create a new dataframe that will be used for seaborn plotting
    melt_data = []
    for category, columns in activity_data_categories.items():
        melted = columns.melt(var_name='Activity', value_name='Occurred')
        melted['Category'] = category
        melt_data.append(melted)

    # combine all categories into a single dataframe
    combined_data = pd.concat(melt_data, ignore_index=True)

    # filter the data to include only 'true' values
    true_data = combined_data[combined_data['Occurred'] == True]

    # plot data for each category
    plot_exercise_data(true_data)
    plot_speech_data(true_data)
    plot_tail_movement_data(true_data)

    return activity_data





# ==============================================================================
# Question 5: Unique Actions
# ==============================================================================
"""
    cleans data for analysis
"""


# define function to clean and prepare data for unique actions analysis
def clean_unique_actions_data(data):
    # cleans data for unique actions analysis
    unique_data = df[['latitude', 'longitude', 'unique_squirrel_id', 'other_activities', 'lat_long']].dropna(how='any', subset=['other_activities'])
    unique_data.to_csv('unique.csv', index=False)
    return unique_data

# ==============================================================================
# Run Functions
# ==============================================================================

# call all cleaning functions
clean_squirrel_concentration_data(df)
clean_fur_color_data(df)
clean_am_pm_data(df)
clean_activity_data(df)
clean_unique_actions_data(df)