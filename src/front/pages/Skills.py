import streamlit as st
import json

# JSON file name
FILENAME = "inputs_with_categories.json"

# Function to read JSON data
def read_from_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []  # Return an empty list if the file does not exist
    except json.JSONDecodeError:
        return []

# Function to save data to a JSON file
def save_to_file(data, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        st.success(f"Data successfully saved to {filename}")
    except Exception as e:
        st.error(f"An error occurred while saving: {e}")

# Initialize session state for inputs
if "inputs" not in st.session_state:
    st.session_state.inputs = read_from_file(FILENAME)

# Extract unique categories for dropdown
if "categories" not in st.session_state:
    st.session_state.categories = list(
        {entry["category"] for entry in st.session_state.inputs if entry.get("category")} | 
        {"Data Manipulation", "Deep Learning", "Add New..."}
    )

# Track the last used category
if "last_used_category" not in st.session_state:
    st.session_state.last_used_category = st.session_state.categories[0]

# Function to add a new row
def add_new_row():
    st.session_state.inputs.insert(
        0, {
            "key": f"input_{len(st.session_state.inputs) + 1}",
            "value": "",
            "category": st.session_state.last_used_category,
            "editable": True
        }
    )

# Function to delete a row
def delete_row(index):
    st.session_state.inputs.pop(index)

# Add a new input field at the top
if st.button("➕ Add New"):
    add_new_row()

# Display input fields
st.subheader("Inputs")
to_delete_indices = []  # Collect indices of rows to delete
for i, input_obj in enumerate(st.session_state.inputs):
    cols = st.columns([2, 1, 0.5, 0.5])  # Adjust layout for buttons
    with cols[0]:
        if input_obj.get("editable", False):  # Editable mode
            st.session_state.inputs[i]["value"] = st.text_input(
                label=f"Skill",
                value=input_obj["value"],
                key=f"skill_{input_obj['key']}"
            )
        else:  # Non-editable mode
            st.text_input(
                label=f"Skill {i + 1}",
                value=input_obj["value"],
                key=f"skill_{input_obj['key']}",
                disabled=True,
            )
    with cols[1]:
        if input_obj.get("editable", False):  # Editable mode
            category = st.selectbox(
                label=f"Category",
                options=st.session_state.categories,
                index=st.session_state.categories.index(input_obj["category"]) if input_obj["category"] else 0,
                key=f"category_{input_obj['key']}"
            )
            st.session_state.inputs[i]["category"] = category

            # Handle "Add New..." dynamically
            if category == "Add New...":
                new_category = st.text_input(
                    f"Add New Category", 
                    key=f"new_category_{input_obj['key']}"
                )
                if new_category and new_category not in st.session_state.categories:
                    st.session_state.categories.insert(-1, new_category)
                    st.session_state.inputs[i]["category"] = new_category
        else:  # Non-editable mode
            st.selectbox(
                label=f"Category",
                options=[input_obj["category"]],
                index=0,
                key=f"category_{input_obj['key']}",
                disabled=True,
            )
    with cols[2]:
        # Edit button
        if not input_obj.get("editable", False):  # Show 'Edit' for non-editable rows
            if st.button(f"✏️", key=f"edit_{input_obj['key']}"):
                st.session_state.inputs[i]["editable"] = True
        else:  # Show 'Lock' for editable rows
            if st.button(f"🔒", key=f"lock_{input_obj['key']}"):
                st.session_state.inputs[i]["editable"] = False
                
    with cols[3]:
        # Delete button
        if st.button(f"❌", key=f"delete_{input_obj['key']}"):
            to_delete_indices.append(i)

# Delete selected rows after iteration (to avoid index mismatch during iteration)
for index in sorted(to_delete_indices, reverse=True):
    delete_row(index)

# Save button to persist data to JSON file
if st.button("💾 Save"):
    # Save and reset all rows to non-editable after saving
    for input_obj in st.session_state.inputs:
        input_obj["editable"] = False
    save_to_file(st.session_state.inputs, FILENAME)
