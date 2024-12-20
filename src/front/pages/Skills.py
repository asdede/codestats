import streamlit as st
import json
from back.create_pdf import create_pdf
import uuid
import requests


base_url = 'http://api:8000'
#base_url = 'http://0.0.0.0:8000'
# JSON file name
FILENAME = "skills.json"

with st.sidebar:
    if st.button("Export"):
        pdf = create_pdf()
        st.download_button(
            label='Download PDF',
            data = pdf,
            file_name='codestats_resume.pdf',
            mime='application/pdf'
        )
skills_url = f'{base_url}/skills'
# Function to read JSON data
def read_from_file(filename):
    res = requests.get(skills_url)
    if res.status_code != 200 or len(res.json()) == 0:
        return []
    return res.json()



# Function to save data to a JSON file
def save_to_file(data, filename):
    skill_data = [{"uuid": item["uuid"], "key": item["key"],
                "value": item["value"], "category": item["category"],
                "editable": item["editable"]} for item in data]
    
    requests.post(f'{base_url}/skills/add',json=skill_data)

# Initialize session state for inputs
if "inputs" not in st.session_state:
    st.session_state.inputs = read_from_file(FILENAME)

# Extract unique categories for dropdown
if "categories" not in st.session_state:
    st.session_state.categories = list(
        {entry["category"] for entry in st.session_state.inputs if entry.get("category")} | 
        {"Data Manipulation", "Deep Learning", "Machine Learning","Databases", "Add New..."}
    )

for input_obj in st.session_state.inputs:
    if "uuid" not in input_obj:
        input_obj["uuid"] = str(uuid.uuid4())  # Assign a UUID if missing


# Track the last used category
if "last_used_category" not in st.session_state:
    st.session_state.last_used_category = st.session_state.categories[0]

# Function to add a new row
def add_new_row():
    st.session_state.inputs.insert(
        0, {
            "uuid": str(uuid.uuid4()),
            "key": f"input_{len(st.session_state.inputs) + 1}",
            "value": "",
            "category": st.session_state.last_used_category,
            "editable": True
        }
    )

# Function to delete a row
def delete_row(index):
    st.session_state.inputs.pop(index)
if st.button("💾 Save"):
    # Save and reset all rows to non-editable after saving
    for input_obj in st.session_state.inputs:
        input_obj["editable"] = False
    save_to_file(st.session_state.inputs, FILENAME)
# Add a new input field at the top
if st.button("➕ Add New"):
    add_new_row()

# Display input fields
st.subheader("Skills")
to_delete_indices = []  # Collect indices of rows to delete
for i, input_obj in enumerate(st.session_state.inputs):
    cols = st.columns([2, 1, 0.5, 0.5])  # Adjust layout for buttons
    unique_key = input_obj["uuid"]  # Use the unique UUID as the key
    with cols[0]:
        if input_obj.get("editable", False):  # Editable mode
            st.session_state.inputs[i]["value"] = st.text_input(
                label=f"Skill",
                value=input_obj["value"],
                key=f"skill_{unique_key}"
            )
        else:  # Non-editable mode
            st.text_input(
                label=f"Skill {i + 1}",
                value=input_obj["value"],
                key=f"skill_{unique_key}",
                disabled=True,
            )
    with cols[1]:
        if input_obj.get("editable", False):  # Editable mode
            category = st.selectbox(
                label=f"Category",
                options=st.session_state.categories,
                index=st.session_state.categories.index(input_obj["category"]) if input_obj["category"] else 0,
                key=f"category_{unique_key}"
            )
            st.session_state.inputs[i]["category"] = category

            # Handle "Add New..." dynamically
            if category == "Add New...":
                new_category = st.text_input(
                    f"Add New Category", 
                    key=f"new_category_{unique_key}"
                )
                if new_category and new_category not in st.session_state.categories:
                    st.session_state.categories.insert(-1, new_category)
                    st.session_state.inputs[i]["category"] = new_category
        else:  # Non-editable mode
            st.selectbox(
                label=f"Category",
                options=[input_obj["category"]],
                index=0,
                key=f"category_{unique_key}",
                disabled=True,
            )
    with cols[2]:
        # Edit button
        if not input_obj.get("editable", False):  # Show 'Edit' for non-editable rows
            if st.button(f"✏️", key=f"edit_{unique_key}"):
                st.session_state.inputs[i]["editable"] = True
        else:  # Show 'Lock' for editable rows
            if st.button(f"🔒", key=f"lock_{unique_key}"):
                st.session_state.inputs[i]["editable"] = False
                
    with cols[3]:
        # Delete button
        if st.button(f"❌", key=f"delete_{unique_key}"):
            to_delete_indices.append(i)

# Delete selected rows after iteration (to avoid index mismatch during iteration)
for index in sorted(to_delete_indices, reverse=True):
    delete_row(index)

# Save button to persist data to JSON file

