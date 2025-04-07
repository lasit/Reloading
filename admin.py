import streamlit as st
import utils

def main():
    st.set_page_config(
        page_title="Component List Admin",
        page_icon="🔧",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("Component List Administration")
    st.markdown("---")
    
    # Add a link back to the main app
    st.sidebar.markdown("### Navigation")
    if st.sidebar.button("Back to Main App"):
        import webbrowser
        webbrowser.open("http://localhost:8501")
    
    # Load component lists
    component_lists = utils.load_component_lists()
    
    # Create tabs for each component type
    tabs = st.tabs([
        "Calibre", 
        "Rifle", 
        "Case Brand", 
        "Powder Brand", 
        "Powder Model", 
        "Bullet Brand", 
        "Bullet Model", 
        "Primer Brand", 
        "Primer Model",
        "Brass Sizing"
    ])
    
    # Map tab indices to component list keys and names
    component_info = [
        {"key": "calibre", "name": "Calibre"},
        {"key": "rifle", "name": "Rifle"},
        {"key": "case_brand", "name": "Case Brand"},
        {"key": "powder_brand", "name": "Powder Brand"},
        {"key": "powder_model", "name": "Powder Model"},
        {"key": "bullet_brand", "name": "Bullet Brand"},
        {"key": "bullet_model", "name": "Bullet Model"},
        {"key": "primer_brand", "name": "Primer Brand"},
        {"key": "primer_model", "name": "Primer Model"},
        {"key": "brass_sizing", "name": "Brass Sizing"}
    ]
    
    # Display and edit each component list
    for i, tab in enumerate(tabs):
        with tab:
            component_key = component_info[i]["key"]
            component_name = component_info[i]["name"]
            
            st.header(f"{component_name} List")
            
            # Display current items
            st.subheader("Current Items")
            items = component_lists.get(component_key, [])
            
            # Create a container for the items
            item_container = st.container()
            
            # Add new item
            st.subheader("Add New Item")
            col1, col2 = st.columns([3, 1])
            with col1:
                new_item = st.text_input(f"New {component_name}", key=f"new_{component_key}")
            with col2:
                add_button = st.button("Add", key=f"add_{component_key}")
            
            if add_button and new_item:
                if new_item not in items:
                    items.append(new_item)
                    component_lists[component_key] = items
                    utils.save_component_lists(component_lists)
                    st.success(f"Added '{new_item}' to {component_name} list")
                else:
                    st.warning(f"'{new_item}' already exists in {component_name} list")
            
            # Display and allow editing of items
            with item_container:
                if not items:
                    st.info(f"No {component_name} items found. Add some using the form below.")
                else:
                    for j, item in enumerate(items):
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            edited_item = st.text_input(f"Item {j+1}", value=item, key=f"{component_key}_{j}")
                        with col2:
                            update_button = st.button("Update", key=f"update_{component_key}_{j}")
                        with col3:
                            delete_button = st.button("Delete", key=f"delete_{component_key}_{j}")
                        
                        if update_button and edited_item != item:
                            items[j] = edited_item
                            component_lists[component_key] = items
                            utils.save_component_lists(component_lists)
                            st.success(f"Updated '{item}' to '{edited_item}'")
                        
                        if delete_button:
                            items.remove(item)
                            component_lists[component_key] = items
                            utils.save_component_lists(component_lists)
                            st.success(f"Deleted '{item}' from {component_name} list")
                            st.experimental_rerun()

if __name__ == "__main__":
    main()
