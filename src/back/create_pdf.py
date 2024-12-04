from fpdf import FPDF
import matplotlib.pyplot as plt
import requests
from collections import defaultdict
from back.plot_maker import create_wakatime_plot
from io import BytesIO

base_url = 'http://api:8000'
#base_url = 'http://0.0.0.0:8000'


def create_pdf():
    create_wakatime_plot()
    gitlab_data = requests.get(f'{base_url}/stats/gitlab').json()
    github_data = requests.get(f'{base_url}/stats/github').json()
    wakahours = requests.get(f'{base_url}/stats/wakatime/hours').json()
    waka_stats = requests.get(f'{base_url}/stats/wakatime').json()
    skills = requests.get(f'{base_url}/skills').json()
    systems = waka_stats['systems']
    editors = waka_stats['editors']
    daily_avg = waka_stats['daily average']

    skills_by_category = defaultdict(list)
    for skill in skills:
        skills_by_category[skill["category"]].append(skill)
    #print(skills_by_category)
    total = {
        'commits':gitlab_data['commits'] + github_data['total commits'],
        'created issues': github_data['created issues']+ gitlab_data['created issues'],
        'Hours coded': wakahours['time coded'],
        'closed issues': github_data['closed issues'] + gitlab_data['closed issues'],
        'total contributions': sum(github_data.values()) + sum(gitlab_data.values()),
        'Daily coding time avg':daily_avg
    }
    TITLE = 'Codestats'

    def create_pie():
        # Data for the inner pie chart (System usage)
        
        labels_1 = list(systems.keys())
        sizes_1 = [systems[system]["percent"] for system in labels_1]
        #text_1 = [systems[system]["text"] for system in labels_1]
        #colors_1 = ['#66b3ff', '#99ff99']  # Colors for the slices
        explode_1 = [0.1] + [0] * (len(labels_1) - 1)
        explode_1 = tuple(explode_1)  # Convert to tuple

        # Data for the outer pie chart (Editor usage)

        labels_2 = list(editors.keys())
        sizes_2 = [editors[editor]["hours numeral"] for editor in labels_2]
        explode_2 = [0.1] + [0] * (len(labels_2) - 1)
        explode_2 = tuple(explode_2)  # Convert to tuple

        # Create a figure with two subplots (side by side)
        fig, axes = plt.subplots(1, 2, figsize=(16, 8))  # 1 row, 2 columns

        # Inner pie chart (System usage) on the first subplot
        axes[0].pie(sizes_1, explode=explode_1, labels=labels_1,
                    autopct='%1.1f%%', shadow=True, startangle=90, pctdistance=0.85,
                    textprops={'fontsize': 14})  # Increase font size
        axes[0].axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle
        axes[0].set_title('Systems', fontsize=16)



        # Outer pie chart (Editor usage) on the second subplot
        axes[1].pie(sizes_2, explode=explode_2, labels=labels_2,
                    autopct='%1.1f%%', shadow=True, startangle=90, pctdistance=0.85,
                    textprops={'fontsize': 14})  # Increase font size
        axes[1].axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle
        axes[1].set_title('Editors', fontsize=16)

        # Adjust layout to prevent overlap
        plt.tight_layout()

        # Save the figure as a PNG image
        plt.savefig('pie.png')
        plt.close()

    # Call the function to create and save the pie charts
    create_pie()
    # Create a PDF instance
    pdf = FPDF('P', 'mm', 'A4')
    pdf.set_draw_color(200)
    #pdf.fill_color(127,126,126)
    pdf.add_page()
    pdf.set_margins(10, 10, 10)

    # Title Section
    pdf.set_font('Arial', 'B', 24)
    pdf.set_text_color(33, 37, 41)
    pdf.cell(0, 10, 'Coding Stats and Contributions', border=0, ln=1, align='C')
    pdf.line(0, 21, 300, 21)
    pdf.ln(10)

    pdf.set_font('Arial', 'B', 16)

    # Box Styling Parameters
    box_width = 55
    box_height = 25
    box_margin = 15

    # Data for Metrics (Split into Two Rows)
    row1_data = {
        'Contributions': total['total contributions'],
        'Commits': total['commits'],
        'Hours coded': total['Hours coded']
    }
    row2_data = {
        'Issues Created': total['created issues'],
        'Issues Closed': total['closed issues'],
        'Daily average':total['Daily coding time avg']
    }

    # Calculate total width for each row
    def get_x_start(data, box_width, box_margin, page_width):
        num_cols = len(data)
        table_width = num_cols * box_width + (num_cols - 1) * box_margin
        return (page_width - table_width) / 2

    # Page width
    page_width = pdf.w


    # Draw first row
    x_start = get_x_start(row1_data, box_width, box_margin, page_width)
    y_start = pdf.get_y() + 10
    x = x_start
    y = y_start

    for key, value in row1_data.items():
        pdf.rect(x, y, box_width, box_height,round_corners=True,style='D')  # Draw the box
        pdf.set_xy(x, y + 5)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(box_width, 5, key, border=0, align='C')  # Label
        pdf.set_xy(x, y + 15)
        pdf.set_font('Arial', '', 12)
        pdf.cell(box_width, 5, str(value), border=0, align='C')  # Value
        x += box_width + box_margin

    # Draw second row
    x_start = get_x_start(row2_data, box_width, box_margin, page_width)
    y_start += box_height + box_margin  # Move down for the second row
    x = x_start
    y = y_start
    for key, value in row2_data.items():
        pdf.rect(x, y, box_width, box_height,round_corners=True,style='D')  # Draw the box
        pdf.set_xy(x, y + 5)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(box_width, 5, key, border=0, align='C')  # Label
        pdf.set_xy(x, y + 15)
        pdf.set_font('Arial', '', 12)
        pdf.cell(box_width, 5, str(value), border=0, align='C')  # Value
        x += box_width + box_margin

    pdf.set_font('Arial', 'B', 16)

    pdf.ln(15)
    pdf.cell(0,10, 'Programming overview',ln=2,align='C')

    pdf.image('wakatime_plot.png', x=5, y=120, w=200)
    pdf.line(65, 120, 146, 120)
    pdf.add_page()
    pdf.image('pie.png',x=0,y=10,w=210)
    pdf.ln(100)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Skills:', ln=1,align='C')
    # Skills Section

    pdf.ln(10)

        # Set header font and size
    pdf.set_font('Arial', 'B', 12)

    categories = sorted(set(skill["category"] for skill in skills))  # Extract and sort categories

    # Define constants
    column_width = 63  # Width of each column (190 page width divided by 3, minus some margin)
    line_height = 5   # Height for each row
    spacing = 5       # Space between categories and rows

    # Initialize position trackers
    y_positions = [pdf.get_y()] * 3  # Track Y positions for three columns
    x_positions = [10, 73, 136]  # X positions for the three columns

    for i, category in enumerate(categories):
        # Determine the current column index (0, 1, or 2)
        col_index = i % 3

        # Set X and Y position for the column
        pdf.set_xy(x_positions[col_index], y_positions[col_index])
        pdf.set_font('Arial', 'B', 12)

        # Add the category header
        pdf.cell(column_width, line_height, category, 0, 1, 'C')  # Category header, centered

        # Set font for skill details (normal size)
        pdf.set_font('Arial', '', 12)

        # Render skills for the category
        for skill in skills:
            if skill["category"] == category:
                pdf.set_x(x_positions[col_index])  # Ensure correct column alignment
                pdf.cell(column_width, line_height, skill["value"], 0, 1, 'C')  # Skill value

        # Update the vertical position tracker for the current column
        y_positions[col_index] = pdf.get_y()

        # After processing all columns, align to the maximum Y position of the row if all columns are used
        if col_index == 2:
            new_row_y = max(y_positions) + spacing
            y_positions = [new_row_y] * 3  # Reset all columns to the new row's starting position
            pdf.set_y(new_row_y)


    # Save PDF
    #pdf.output('coding_stats_resume.pdf', 'F')
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()
