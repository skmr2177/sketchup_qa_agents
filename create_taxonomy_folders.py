#!/usr/bin/env python3
"""
Create Taxonomy Folder Structure
Creates the complete folder structure for all SketchUp products, categories, and subcategories
based on the comprehensive taxonomy analysis.
"""

import os
from pathlib import Path

def create_taxonomy_structure():
    """Create the complete taxonomy folder structure"""
    
    # Base output directory
    base_dir = Path("output")
    taxonomy_dir = base_dir / "taxonomy_structure"
    
    # Comprehensive taxonomy based on analysis
    taxonomy = {
        "SketchUp_Pro_(Desktop)": {
            "Installation_&_Setup": [
                "initial_installation", "license_activation", "subscription_management",
                "system_requirements", "network_configuration", "trimble_id_setup",
                "offline_installation", "pro_features_activation"
            ],
            "Updates_&_Versioning": [
                "changelog_review", "version_migration", "feature_deprecation",
                "new_feature_use", "backward_compatibility", "update_installation"
            ],
            "Getting_Started_&_Basics": [
                "interface_navigation", "basic_tools", "file_management",
                "template_selection", "preferences_settings", "keyboard_shortcuts",
                "troubleshooting_basics", "performance_optimization"
            ],
            "Drawing_&_Modeling_Tools": [
                "line_tool", "rectangle_tool", "circle_tool", "push_pull_tool",
                "follow_me_tool", "offset_tool", "move_tool", "rotate_tool",
                "scale_tool", "tape_measure", "protractor", "text_tool",
                "dimension_tool", "section_plane", "select_tool", "bezier_curves",
                "freehand_tool", "arc_tool", "polygon_tool"
            ],
            "Components_and_Groups": [
                "creating_components", "editing_components", "dynamic_components",
                "warehouse_integration", "grouping_objects", "component_attributes"
            ],
            "Materials_and_Textures": [
                "applying_materials", "editing_materials", "texture_mapping",
                "custom_materials", "material_library", "transparency_settings"
            ],
            "Styles_and_Display": [
                "creating_styles", "editing_styles", "edge_settings",
                "face_settings", "background_settings", "watermark_use",
                "style_builder", "display_performance"
            ],
            "Scenes_and_Animation": [
                "creating_scenes", "editing_scenes", "animation_settings",
                "camera_tools", "walkthrough_animation", "scene_transitions"
            ],
            "Import_and_Export": [
                "3d_import", "2d_import", "3d_export", "2d_export",
                "cad_import_export", "image_import_export", "file_compatibility"
            ],
            "Extensions_and_Plugins": [
                "extension_installation", "extension_management", "plugin_troubleshooting",
                "extension_warehouse", "ruby_scripting", "api_development"
            ],
            "LayOut_Integration": [
                "sending_to_layout", "layout_viewports", "layout_dimensions",
                "layout_annotations", "layout_templates", "layout_export",
                "layout_presentation"
            ],
            "Rendering_and_Visualization": [
                "rendering_basics", "render_settings", "lighting_setup",
                "material_rendering", "post_processing", "third_party_renderers"
            ],
            "Troubleshooting_and_Support": [
                "crash_recovery", "bug_reporting", "performance_issues",
                "licensing_issues", "technical_support", "community_forums"
            ],
            "Advanced_Techniques": [
                "large_model_management", "complex_geometry", "scripting_automation",
                "custom_templates", "advanced_rendering", "parametric_modeling"
            ],
            "Collaboration_and_Sharing": [
                "trimble_connect", "model_sharing", "version_control",
                "cloud_collaboration", "team_projects", "feedback_sharing"
            ],
            "Licensing_and_Subscription": [
                "license_management", "subscription_renewal", "billing_inquiries",
                "account_management", "trial_versions", "educational_licenses"
            ],
            "Hardware_and_Software_Compatibility": [
                "gpu_issues", "os_compatibility", "peripheral_support",
                "software_conflicts", "driver_updates", "system_optimization"
            ],
            "Customization_and_Workflows": [
                "toolbar_customization", "shortcut_customization", "template_creation",
                "workflow_optimization", "scripting_customization", "profile_management"
            ],
            "Educational_Resources": [
                "tutorials_courses", "documentation_guides", "webinars_workshops",
                "community_resources", "certification_programs", "learning_paths"
            ],
            "Feature_Specific": [
                "live_components", "pre_designed_objects", "3d_warehouse_integration",
                "scan_to_design", "add_location", "geolocated_models",
                "photo_matching", "solids_tools", "sandbox_tools", "match_photo"
            ]
        },
        "LayOut": {
            "Getting_Started_&_Basics": [
                "interface_overview", "document_setup", "template_use",
                "basic_tools", "file_management", "preferences"
            ],
            "SketchUp_Model_Integration": [
                "inserting_models", "viewport_settings", "scene_management",
                "rendering_options", "model_updates", "scaling_models"
            ],
            "Drawing_&_Annotation_Tools": [
                "line_tools", "shape_tools", "dimensioning", "labeling",
                "text_tools", "scrapbooks", "callouts", "autotext"
            ],
            "Page_Management": [
                "adding_pages", "page_navigation", "master_pages",
                "layer_management", "page_numbering", "document_organization"
            ],
            "Presentation_&_Export": [
                "creating_presentations", "export_options", "pdf_export",
                "image_export", "print_settings", "web_export"
            ],
            "Customization_&_Workflows": [
                "custom_templates", "scrapbook_creation", "keyboard_shortcuts",
                "workflow_tips", "api_scripting"
            ],
            "Troubleshooting_&_Performance": [
                "file_corruption", "performance_issues", "printing_problems",
                "model_linking_issues", "bug_reporting"
            ]
        },
        "SketchUp_Go": {
            "Getting_Started_&_Basics": [
                "interface_go", "basic_tools_go", "file_management_go",
                "preferences_go", "gestures_go", "offline_mode_go"
            ],
            "Modeling_Tools_Go": [
                "drawing_tools_go", "editing_tools_go", "component_use_go",
                "grouping_go", "materials_go", "styles_go"
            ],
            "AR_&_VR_Features": [
                "ar_viewing", "vr_integration", "model_overlay",
                "measurement_tools_ar", "presentation_ar"
            ],
            "Collaboration_&_Sharing_Go": [
                "trimble_connect_go", "model_sharing_go", "cloud_sync_go"
            ],
            "Troubleshooting_Go": [
                "performance_issues_go", "device_compatibility", "bug_reporting_go"
            ]
        },
        "SketchUp_Web": {
            "Getting_Started_&_Basics": [
                "interface_web", "basic_tools_web", "file_management_web",
                "template_selection_web", "preferences_web", "keyboard_shortcuts_web"
            ],
            "Modeling_Tools_Web": [
                "drawing_tools_web", "editing_tools_web", "component_use_web",
                "grouping_web", "materials_web", "styles_web"
            ],
            "Collaboration_&_Sharing_Web": [
                "trimble_connect_web", "model_sharing_web", "version_control_web",
                "cloud_collaboration_web", "team_projects_web"
            ],
            "Import_and_Export_Web": [
                "3d_import_web", "2d_import_web", "3d_export_web",
                "2d_export_web", "file_compatibility_web"
            ],
            "Troubleshooting_Web": [
                "performance_issues_web", "browser_compatibility", "bug_reporting_web"
            ]
        },
        "SketchUp_Shop": {
            "Getting_Started_&_Basics": [
                "interface_shop", "basic_tools_shop", "file_management_shop",
                "preferences_shop"
            ],
            "Modeling_Tools_Shop": [
                "drawing_tools_shop", "editing_tools_shop", "component_use_shop",
                "grouping_shop", "materials_shop", "styles_shop"
            ],
            "Advanced_Features_Shop": [
                "custom_reporting", "advanced_import_export", "nesting_optimization"
            ],
            "Troubleshooting_Shop": [
                "performance_issues_shop", "browser_compatibility_shop", "bug_reporting_shop"
            ]
        },
        "SketchUp_Studio": {
            "Getting_Started_&_Basics": [
                "interface_studio", "installation_studio", "licensing_studio",
                "file_management_studio"
            ],
            "Scan_to_Design": [
                "scan_import", "point_cloud_processing", "scan_to_model",
                "scan_data_management"
            ],
            "Advanced_Modeling_Studio": [
                "parametric_modeling_studio", "complex_geometry_studio", "optimization_studio"
            ],
            "Rendering_&_Analysis": [
                "vray_integration", "sustainability_analysis", "daylighting_analysis",
                "energy_modeling"
            ],
            "Collaboration_Studio": [
                "trimble_connect_studio", "cloud_workflows_studio", "version_control_studio"
            ],
            "Troubleshooting_Studio": [
                "installation_issues_studio", "performance_issues_studio", "licensing_issues_studio"
            ]
        },
        "SketchUp_Mobile_Viewer": {
            "Getting_Started_&_Basics": [
                "interface_mobile_viewer", "navigation_mobile_viewer", "file_access_mobile_viewer"
            ],
            "Viewing_&_Presentation": [
                "model_viewing", "layer_visibility_mobile", "scene_playback_mobile",
                "section_planes_mobile", "ar_viewing_mobile", "vr_viewing_mobile"
            ],
            "Collaboration_Mobile": [
                "trimble_connect_mobile", "model_sharing_mobile", "markup_tools_mobile"
            ],
            "Troubleshooting_Mobile": [
                "performance_issues_mobile", "device_compatibility_mobile", "file_loading_issues_mobile"
            ]
        }
    }
    
    print("🏗️  Creating comprehensive taxonomy folder structure...")
    print(f"📁 Base directory: {taxonomy_dir}")
    
    total_folders = 0
    
    # Create the main taxonomy directory
    taxonomy_dir.mkdir(parents=True, exist_ok=True)
    
    # Create structure for each product
    for product, categories in taxonomy.items():
        print(f"\n📦 Creating structure for: {product}")
        product_dir = taxonomy_dir / product
        product_dir.mkdir(exist_ok=True)
        total_folders += 1
        
        # Create categories for each product
        for category, subcategories in categories.items():
            category_dir = product_dir / category
            category_dir.mkdir(exist_ok=True)
            total_folders += 1
            
            # Create subcategories for each category
            for subcategory in subcategories:
                subcategory_dir = category_dir / subcategory
                subcategory_dir.mkdir(exist_ok=True)
                total_folders += 1
                
                # Create a placeholder README file in each subcategory
                readme_file = subcategory_dir / "README.md"
                if not readme_file.exists():
                    with open(readme_file, 'w', encoding='utf-8') as f:
                        f.write(f"# {subcategory.replace('_', ' ').title()}\n\n")
                        f.write(f"**Product:** {product}\n")
                        f.write(f"**Category:** {category.replace('_', ' ').title()}\n")
                        f.write(f"**Subcategory:** {subcategory.replace('_', ' ').title()}\n\n")
                        f.write("This directory contains Q&A content related to this specific subcategory.\n")
    
    print(f"\n✅ Taxonomy folder structure created successfully!")
    print(f"📊 Summary:")
    print(f"  • Total folders created: {total_folders}")
    print(f"  • Products: {len(taxonomy)}")
    
    # Count categories and subcategories
    total_categories = sum(len(categories) for categories in taxonomy.values())
    total_subcategories = sum(len(subcategories) for categories in taxonomy.values() for subcategories in categories.values())
    
    print(f"  • Categories: {total_categories}")
    print(f"  • Subcategories: {total_subcategories}")
    print(f"  • Location: {taxonomy_dir.absolute()}")
    
    # Show the structure
    print(f"\n📂 Folder Structure Preview:")
    for product, categories in taxonomy.items():
        print(f"  📦 {product}")
        for category, subcategories in categories.items():
            print(f"    📁 {category}")
            for subcategory in subcategories[:3]:  # Show first 3 subcategories
                print(f"      📄 {subcategory}")
            if len(subcategories) > 3:
                print(f"      ... and {len(subcategories) - 3} more subcategories")

if __name__ == "__main__":
    create_taxonomy_structure() 