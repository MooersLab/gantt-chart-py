#!/opt/local/bin/python3.12
"""
This script makes a great plot for planning manuscript assembly and submission.
The activities per manuscript are on the same line.
The activities are grouped by project name.
A named tuple had to be used to properly align the project name on the y-axis.

Blaine Mooers and the OUHSC Board of Regents

April 4, 2025
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import namedtuple

# Create a named tuple for task data to ensure immutability
Task = namedtuple('Task', ['name', 'start', 'end', 'phase'])

# Define tasks using the immutable namedtuple: project name, start date, end date, and task.
project_tasks = (
    Task("Paper A", "2025-04-05", "2025-04-30", "Research and Lit Rev"),
    Task("Paper A", "2025-05-05", "2025-05-15", "Writing Results and Slideshow"),
    Task("Paper A", "2025-05-16", "2025-05-22", "Discussion"),
    Task("Paper A", "2025-05-16", "2025-05-25", "Polishing and Submission"),
    Task("Paper A", "2025-07-15", "2025-08-25", "Revision, Resubmit, Galley Proofs"),
    
    Task("Paper B", "2025-04-05", "2025-08-30", "Research and Lit Rev"),
    Task("Paper B", "2025-08-30", "2025-10-30", "Writing Results and Slideshow"),
    Task("Paper B", "2025-10-31", "2025-12-31", "Discussion"),
    Task("Paper B", "2026-01-02", "2026-05-03", "Polishing and Submission"),
    Task("Paper B", "2026-07-15", "2026-08-25", "Revision, Resubmit, Galley Proofs"),
    
    Task("Paper C", "2025-04-05", "2025-04-13", "Research and Lit Rev"),
    Task("Paper C", "2025-04-09", "2025-04-13", "Writing Results and Slideshow"),
    Task("Paper C", "2025-04-13", "2025-04-21", "Discussion"),
    Task("Paper C", "2025-04-21", "2025-04-25", "Polishing and Submission"),
    Task("Paper C", "2025-06-25", "2025-08-25", "Revision, Resubmit, Galley Proofs"),
    
    Task("Paper D", "2025-04-05", "2025-04-13", "Research and Lit Rev"),
    Task("Paper D", "2025-04-09", "2025-04-13", "Writing Results and Slideshow"),
    Task("Paper D", "2025-04-13", "2025-04-21", "Discussion"),
    Task("Paper D", "2025-04-21", "2025-04-30", "Polishing and Submission"),
    Task("Paper D", "2025-06-05", "2025-06-30", "Revision, Resubmit, Galley Proofs"),

    Task("Paper E", "2025-04-06", "2025-05-30", "Research and Lit Rev"),
    Task("Paper E", "2025-05-01", "2025-06-30", "Writing Results and Slideshow"),
    Task("Paper E", "2025-06-30", "2025-07-31", "Discussion"),
    Task("Paper E", "2025-07-31", "2025-08-30", "Polishing and Submission"),
    Task("Paper E", "2025-10-15", "2025-10-30", "Revision, Resubmit, Galley Proofs"),
    
    Task("Paper F", "2025-08-01", "2025-08-30", "Research and Lit Rev"),
    Task("Paper F", "2025-09-01", "2025-09-30", "Writing Results and Slideshow"),
    Task("Paper F", "2025-09-30", "2025-10-31", "Discussion"),
    Task("Paper F", "2025-10-31", "2025-11-30", "Polishing and Submission"),
    Task("Paper F", "2026-02-01", "2026-02-28", "Revision, Resubmit, Galley Proofs"),

    Task("Paper G", "2025-05-01", "2025-08-30", "Research and Lit Rev"),
    Task("Paper G", "2025-08-31", "2025-10-30", "Writing Results and Slideshow"),
    Task("Paper G", "2025-10-30", "2025-11-15", "Discussion"),
    Task("Paper G", "2025-11-15", "2025-11-30", "Polishing and Submission"),
    Task("Paper G", "2026-02-01", "2026-02-28", "Revision, Resubmit, Galley Proofs"),
    
)

# Define custom phase colors with updated categories
phase_colors = {
    "Research and Lit Rev": "#39FF14",  # Bright Green
    "Writing Results and Slideshow": "#4287f5",  # Blue
    "Discussion": "#f542bb",      # Pink
    "Polishing and Submission": "#e84118",        # Red
    "Revision, Resubmit, Galley Proofs": "#ffd700"        # Gold
}

# Group tasks by name to consolidate y-axis labels
task_names_unique = sorted(set(task.name for task in project_tasks))
name_to_pos = {name: len(task_names_unique) - i - 1 for i, name in enumerate(task_names_unique)}

# Create figure and axis
fig, ax = plt.subplots(figsize=(16, 7))

# Determine overall date range for x-axis
all_starts = [pd.Timestamp(task.start) for task in project_tasks]
all_ends = [pd.Timestamp(task.end) for task in project_tasks]
min_date = min(all_starts)
max_date = max(all_ends)

# Plot the tasks
for task in project_tasks:
    # Convert dates to timestamps
    start_date = pd.Timestamp(task.start)
    end_date = pd.Timestamp(task.end)
    
    # Get y position based on task name
    y_pos = name_to_pos[task.name]
    
    # Calculate duration
    duration = (end_date - start_date).days + 1
    
    # Plot bar
    ax.barh(y_pos, 
            duration, 
            left=mdates.date2num(start_date), 
            height=0.5,
            align='center',
            color=phase_colors[task.phase],
            alpha=0.8,
            edgecolor='navy')
    
    # Add phase label inside the bar for longer bars
    if duration > 60:
        bar_middle = mdates.date2num(start_date) + duration / 2
        ax.text(bar_middle, y_pos, task.phase, 
                ha='center', va='center', color='white', 
                fontweight='bold', fontsize=9)

# Set up y-axis
ax.set_yticks(list(name_to_pos.values()))
ax.set_yticklabels(list(name_to_pos.keys()))
ax.set_ylim(-0.5, len(task_names_unique) - 0.5)

# Generate monthly date range for vertical grid lines
start_month = pd.Timestamp(min_date.year, min_date.month, 1)
end_month = pd.Timestamp(max_date.year, max_date.month, 1) + pd.DateOffset(months=1)
months = pd.date_range(start=start_month, end=end_month, freq='MS')

# Add vertical lines for each month (first of the month)
for month in months:
    ax.axvline(x=mdates.date2num(month), color='gray', linestyle='-', 
              alpha=0.2, linewidth=1)
    
# Set up x-axis with monthly ticks showing both month and year
ax.xaxis.set_major_locator(mdates.MonthLocator())  # First of each month
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))  # Month and year on separate lines
ax.tick_params(axis='x', which='major', labelsize=9, pad=2)

# Add buffer space to the x-axis
buffer_days = max(10, (max_date - min_date).days * 0.02)  # 2% buffer, minimum 10 days
ax.set_xlim(
    mdates.date2num(min_date - pd.Timedelta(days=buffer_days)),
    mdates.date2num(max_date + pd.Timedelta(days=buffer_days))
)

# Add today vertical line
today = pd.Timestamp('2025-04-03')
plt.axvline(x=mdates.date2num(today), color='red', linestyle='--', 
            alpha=0.7, label='Start Date')

# Add legend for phases
handles = [plt.Rectangle((0,0),1,1, color=color, alpha=0.8) for color in phase_colors.values()]
labels = list(phase_colors.keys())
plt.legend(handles, labels, loc='upper right', title='Manuscript Phases')

# Add title and labels
plt.title('Journal Article Writing Plan 2025-2026', fontsize=16, pad=20)
plt.xlabel('Month/Year', fontsize=12, labelpad=10)

# Style and grid
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Custom year separator lines (darker line between years)
year_starts = [pd.Timestamp(year=y, month=1, day=1) for y in range(min_date.year, max_date.year + 2)]
for year_date in year_starts:
    if year_date >= min_date and year_date <= max_date:
        ax.axvline(x=mdates.date2num(year_date), color='black', linestyle='-', 
                  alpha=0.5, linewidth=1.5)

# Adjust layout to prevent label cutoff
plt.tight_layout()


# Uncomment to save the figure
plt.savefig('writingPLan2025-2026.png', dpi=300, bbox_inches='tight')

# Display the plot
plt.show()
