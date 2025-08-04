#!/usr/bin/env python3
"""
SketchUp Q&A Categorization System
Categorizes Q&A files according to sample_category.md taxonomy
Can be used for existing files and future Q&A generation
"""

import os
import shutil
import re
from pathlib import Path
from typing import Tuple, Optional

class SketchUpQACategorizer:
    def __init__(self, base_output_dir="output"):
        self.base_output_dir = Path(base_output_dir)
        self.categorized_dir = self.base_output_dir / "categorized"
        
        # Platform taxonomy from sample_category.md
        self.taxonomy = self._load_taxonomy()
    
    def _load_taxonomy(self):
        """Load the complete taxonomy structure from sample_category.md"""
        return {
            "SketchUp_Pro_Desktop": {
                "Installation_Setup": [
                    "initial_installation", "license_activation", "subscription_management", 
                    "system_requirements", "network_configuration", "trimble_id_setup", 
                    "offline_installation", "pro_features_activation"
                ],
                "Updates_Versioning": [
                    "changelog_review", "version_migration", "feature_deprecation", 
                    "new_feature_use", "backward_compatibility", "update_installation"
                ],
                "Getting_Started_Basics": [
                    "interface_overview", "workspace_setup", "basic_navigation", 
                    "tool_introduction", "menu_navigation", "panel_management", 
                    "preference_settings", "template_selection", "units_setup"
                ],
                "Drawing_Modeling_Tools": [
                    "line_tool", "rectangle_tool", "circle_tool", "push_pull_tool", 
                    "follow_me_tool", "offset_tool", "move_tool", "rotate_tool", 
                    "scale_tool", "tape_measure", "protractor", "text_tool", 
                    "dimension_tool", "section_plane"
                ],
                "Selection_Navigation": [
                    "selection_methods", "multi_selection", "orbit_navigation", 
                    "pan_navigation", "zoom_controls", "walk_through", 
                    "camera_positioning", "view_controls", "standard_views"
                ],
                "Geometry_Modeling": [
                    "edges_faces", "groups_components", "solid_modeling", 
                    "boolean_operations", "intersect_operations", "geometry_repair", 
                    "face_orientation", "smoothing_softening"
                ],
                "Groups_Components": [
                    "creating_groups", "editing_groups", "component_creation", 
                    "dynamic_components", "component_browser", "nested_components", 
                    "component_outliner", "unique_components", "component_reload", 
                    "component_sync"
                ],
                "Materials_Textures": [
                    "material_browser", "applying_materials", "creating_materials", 
                    "texture_positioning", "material_sampling", "transparency_settings", 
                    "custom_textures", "photo_textures"
                ],
                "Layers_Tags": [
                    "tag_management", "visibility_control", "layer_organization", 
                    "tag_assignment", "scene_layers", "layer_colors", 
                    "layer_export", "tag_migration"
                ],
                "Scenes_Animation": [
                    "scene_creation", "scene_management", "scene_transitions", 
                    "animation_settings", "camera_scenes", "walkthrough_animation", 
                    "scene_export"
                ],
                "Styles_Display": [
                    "edge_styles", "face_styles", "background_settings", 
                    "watermarks", "style_creation", "style_editing", 
                    "sketch_styles", "photorealistic_styles"
                ],
                "Shadows_Lighting": [
                    "shadow_settings", "sun_positioning", "geographic_location", 
                    "time_date_settings", "shadow_accuracy", "interior_lighting", 
                    "shadow_analysis"
                ],
                "Import_Export": [
                    "cad_import", "image_import", "3d_import", "2d_export", 
                    "3d_export", "pdf_export", "image_export", "animation_export", 
                    "file_optimization"
                ],
                "Extensions_Plugins": [
                    "extension_installation", "extension_management", "ruby_scripting", 
                    "api_development", "extension_updates", "custom_tools", 
                    "extension_compatibility", "extension_review", "extension_discovery"
                ],
                "LayOut_Integration": [
                    "layout_references", "model_updates", "viewport_management", 
                    "layout_sync", "layout_export", "layout_templates"
                ],
                "Performance_Stability": [
                    "model_optimization", "file_size_reduction", "graphics_settings", 
                    "large_model_handling", "performance_monitoring", "render_optimization", 
                    "memory_management"
                ],
                "Data_Management_Recovery": [
                    "file_backups", "auto_recovery", "data_corruption", 
                    "version_control", "file_organization", "cloud_sync"
                ],
                "Troubleshooting_System_Issues": [
                    "crash_issues", "startup_problems", "display_issues", 
                    "file_corruption", "licensing_issues", "graphics_problems", 
                    "memory_issues", "tool_failures"
                ]
            },
            "SketchUp_Web": {
                "Account_Access": [
                    "trimble_id_login", "subscription_access", "web_browser_compatibility",
                    "account_management", "offline_limitations", "sync_issues"
                ],
                "Updates_Releases": [
                    "web_feature_rollout", "mobile_feature_gaps", "browser_updates_impact",
                    "feature_parity", "rollback_issues"
                ],
                "Web_Interface": [
                    "browser_interface", "toolbar_layout", "panel_management",
                    "touch_interface", "keyboard_shortcuts", "web_navigation", "responsive_design"
                ],
                "Basic_Drawing_Tools": [
                    "line_tool", "rectangle_tool", "circle_tool", "push_pull_tool",
                    "move_tool", "rotate_tool", "scale_tool", "eraser_tool", "paint_bucket"
                ],
                "Web_Specific_Features": [
                    "auto_save", "cloud_storage", "web_performance", "browser_limitations",
                    "feature_differences", "mobile_browser_support", "version_differences", "cloud_processing_limits"
                ],
                "File_Management": [
                    "cloud_save", "file_sharing", "export_limitations", "import_restrictions",
                    "file_formats", "download_options", "storage_limits"
                ],
                "Collaboration": [
                    "sharing_models", "collaborative_editing", "real_time_sync",
                    "access_permissions", "shared_projects", "team_features"
                ],
                "Performance_Stability": [
                    "browser_performance", "loading_issues", "lag_problems",
                    "memory_limitations", "graphics_performance", "crash_recovery"
                ],
                "Web_Limitations": [
                    "missing_features", "export_restrictions", "extension_limitations",
                    "advanced_tool_access", "professional_features"
                ]
            },
            "SketchUp_Go": {
                "Mobile_Setup": [
                    "app_installation", "account_login", "subscription_activation",
                    "device_compatibility", "ios_requirements", "storage_management"
                ],
                "App_Updates_Versions": [
                    "app_store_versioning", "feature_delays", "ios_updates",
                    "version_compatibility", "update_failures"
                ],
                "Touch_Interface": [
                    "touch_controls", "gesture_navigation", "multi_touch",
                    "apple_pencil_support", "touch_precision", "interface_adaptation",
                    "gesture_conflicts", "rotation_lock"
                ],
                "Mobile_Drawing": [
                    "touch_drawing", "precision_modeling", "mobile_tools",
                    "simplified_interface", "tool_adaptation", "mobile_workflow"
                ],
                "AR_Features": [
                    "ar_mode", "object_placement", "ar_measurement",
                    "real_world_scale", "ar_viewing", "environmental_tracking"
                ],
                "Performance_Stability": [
                    "app_performance", "device_heating", "battery_usage",
                    "memory_management", "crash_issues", "app_optimization"
                ],
                "Cloud_Sync_Data": [
                    "model_sync", "cross_device_access", "cloud_storage",
                    "sync_conflicts", "offline_access", "backup_recovery"
                ],
                "Mobile_Limitations": [
                    "feature_restrictions", "export_limitations", "complex_modeling_limits",
                    "professional_features", "desktop_comparison"
                ]
            },
            "SketchUp_Shop": {
                "Premium_Features": [
                    "advanced_export", "unlimited_cloud_storage", "premium_templates",
                    "enhanced_sharing", "priority_support", "commercial_use"
                ],
                "Version_Differences": [
                    "free_vs_premium_features", "legacy_vs_current_features",
                    "upgrade_benefits", "feature_migration"
                ],
                "Enhanced_Export": [
                    "dwg_export", "pdf_export", "image_export", "3d_formats",
                    "export_quality", "batch_export", "format_options"
                ],
                "Cloud_Storage": [
                    "unlimited_storage", "file_organization", "cloud_management",
                    "storage_optimization", "backup_features", "version_history"
                ],
                "Commercial_Use": [
                    "licensing_compliance", "commercial_projects", "client_sharing",
                    "professional_workflows", "business_features", "usage_rights"
                ],
                "Collaboration_Features": [
                    "team_sharing", "project_management", "client_access",
                    "shared_folders", "collaborative_workflows", "review_processes",
                    "client_review_access", "comment_tracking"
                ]
            },
            "SketchUp_Studio": {
                "Studio_Suite": [
                    "pro_desktop_access", "layout_integration", "style_builder_access",
                    "advanced_importers", "premium_support", "enterprise_features"
                ],
                "Rendering_Visualization_Tools": [
                    "vray_access", "rendering_plugins", "style_builder",
                    "photorealistic_export", "advanced_materials", "lighting_tools"
                ],
                "Advanced_Import_Export": [
                    "dwg_import", "3ds_import", "advanced_formats",
                    "batch_processing", "format_conversion", "data_exchange", "cad_integration"
                ],
                "Enterprise_Features": [
                    "network_licensing", "deployment_tools", "admin_controls",
                    "user_management", "security_features", "compliance_tools"
                ],
                "Professional_Workflows": [
                    "architectural_workflows", "engineering_integration", "construction_documentation",
                    "design_development", "project_coordination"
                ]
            },
            "LayOut": {
                "Layout_Basics": [
                    "interface_overview", "page_setup", "document_creation",
                    "workspace_organization", "tool_introduction"
                ],
                "Template_Management": [
                    "loading_templates", "custom_template_creation", "shared_templates",
                    "template_organization", "template_sharing"
                ],
                "Drawing_Annotation": [
                    "line_drawing", "shape_creation", "text_tools", "dimensioning",
                    "labeling", "leader_lines", "callouts", "markup_tools"
                ],
                "SketchUp_Integration": [
                    "model_references", "viewport_creation", "scene_management",
                    "model_updates", "reference_linking", "view_synchronization"
                ],
                "Layout_Formatting": [
                    "page_layout", "master_pages", "layer_management", "style_formatting",
                    "grid_settings", "alignment_tools", "object_arrangement"
                ],
                "Export_Printing": [
                    "pdf_export", "image_export", "printing_setup", "print_quality",
                    "batch_export", "format_options", "output_optimization"
                ],
                "Advanced_Features": [
                    "auto_text", "scrapbooks", "shared_layers", "collaborative_editing", "custom_tools"
                ],
                "Performance_Stability": [
                    "layout_performance", "large_document_handling", "reference_issues",
                    "crash_problems", "file_corruption", "memory_issues",
                    "render_delays", "linked_model_refresh"
                ]
            },
            "SketchUp_Mobile_Viewer": {
                "Viewer_Features": [
                    "model_viewing", "navigation_controls", "measurement_tools",
                    "section_viewing", "scene_navigation", "model_information"
                ],
                "Cross_Platform_Support": [
                    "android_support", "ios_behavior_differences", "version_sync",
                    "platform_compatibility", "device_variations"
                ],
                "File_Access": [
                    "model_loading", "cloud_access", "local_files",
                    "sharing_access", "file_formats", "download_issues"
                ],
                "Mobile_Interface": [
                    "touch_navigation", "gesture_controls", "interface_layout",
                    "viewing_modes", "display_options", "screen_adaptation"
                ],
                "Viewing_Limitations": [
                    "viewer_restrictions", "editing_limitations", "export_restrictions",
                    "feature_comparison", "upgrade_options"
                ]
            }
        }
    
    def create_taxonomy_structure(self):
        """Create the complete directory structure"""
        print("🏗️  Creating taxonomy structure...")
        
        for platform, categories in self.taxonomy.items():
            for category, subcategories in categories.items():
                for subcategory in subcategories:
                    dir_path = self.categorized_dir / platform / category / subcategory
                    dir_path.mkdir(parents=True, exist_ok=True)
        
        print("✅ Taxonomy structure created!")
    
    def analyze_qa_content(self, file_path: Path) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """Analyze Q&A content to determine correct platform and category"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
        except:
            return None, None, None
        
        filename = file_path.name.lower()
        
        # LayOut content detection (highest priority)
        if any(keyword in content or keyword in filename for keyword in [
            'layout', 'layuot', 'clipping mask', "what's new in layout", 
            'layout user guide', 'scrapbook', 'viewport', 'drawing annotation',
            'draft mode', 'floorplan', 'layout workflow'
        ]):
            return self._determine_layout_category(content, filename)
        
        # SketchUp Go (Mobile) content detection  
        if any(keyword in content or keyword in filename for keyword in [
            'ipad', 'mobile', 'touch', 'apple pencil', 'ar mode', 'device heating',
            'ios', 'app store', 'gesture', 'hot dog stand on the ipad'
        ]):
            return self._determine_go_category(content, filename)
        
        # Extension content - usually desktop
        if any(keyword in content or keyword in filename for keyword in [
            'extension inspection', 'bezier curves', 'placemaker', 'round corner',
            'mini extension', 'visual merge', 'solid tool', 'extension installation',
            'installing extensions'
        ]):
            return self._determine_desktop_extension_category(content, filename)
        
        # Studio/Enterprise features
        if any(keyword in content or keyword in filename for keyword in [
            'vray', 'v-ray', 'professional 3d practice', 'enterprise', 'studio',
            'rendering plugins', 'style builder'
        ]):
            return self._determine_studio_category(content, filename)
        
        # Web-specific features
        if any(keyword in content or keyword in filename for keyword in [
            'web browser', 'browser', 'web version', 'cloud save', 'auto save'
        ]):
            return self._determine_web_category(content, filename)
        
        # Default to desktop/pro for most content
        return self._determine_desktop_category(content, filename)
    
    def _determine_layout_category(self, content: str, filename: str) -> Tuple[str, str, str]:
        """Determine LayOut category based on content"""
        
        if any(keyword in content or keyword in filename for keyword in [
            'clipping mask', 'template', 'scrapbook', 'auto text'
        ]):
            return 'LayOut', 'Advanced_Features', 'auto_text'
        
        if any(keyword in content or keyword in filename for keyword in [
            'draft mode', 'workflow', 'turbocharge'
        ]):
            return 'LayOut', 'Performance_Stability', 'layout_performance'
        
        if any(keyword in content or keyword in filename for keyword in [
            'floorplan', 'export', 'pdf'
        ]):
            return 'LayOut', 'Export_Printing', 'pdf_export'
        
        return 'LayOut', 'Layout_Basics', 'interface_overview'
    
    def _determine_go_category(self, content: str, filename: str) -> Tuple[str, str, str]:
        """Determine SketchUp Go category based on content"""
        
        if any(keyword in content or keyword in filename for keyword in [
            'touch', 'gesture', 'apple pencil'
        ]):
            return 'SketchUp_Go', 'Touch_Interface', 'touch_controls'
        
        if any(keyword in content or keyword in filename for keyword in [
            'ar mode', 'ar'
        ]):
            return 'SketchUp_Go', 'AR_Features', 'ar_mode'
        
        return 'SketchUp_Go', 'Mobile_Drawing', 'touch_drawing'
    
    def _determine_studio_category(self, content: str, filename: str) -> Tuple[str, str, str]:
        """Determine SketchUp Studio category"""
        
        if any(keyword in content or keyword in filename for keyword in [
            'vray', 'v-ray', 'rendering'
        ]):
            return 'SketchUp_Studio', 'Rendering_Visualization_Tools', 'vray_access'
        
        return 'SketchUp_Studio', 'Professional_Workflows', 'architectural_workflows'
    
    def _determine_web_category(self, content: str, filename: str) -> Tuple[str, str, str]:
        """Determine SketchUp Web category"""
        
        if any(keyword in content or keyword in filename for keyword in [
            'browser', 'web browser'
        ]):
            return 'SketchUp_Web', 'Web_Interface', 'browser_interface'
        
        return 'SketchUp_Web', 'Web_Specific_Features', 'cloud_storage'
    
    def _determine_desktop_extension_category(self, content: str, filename: str) -> Tuple[str, str, str]:
        """Determine desktop extension category"""
        
        if any(keyword in content or keyword in filename for keyword in [
            'extension inspection', 'bezier curves', 'placemaker', 'round corner'
        ]):
            return 'SketchUp_Pro_Desktop', 'Extensions_Plugins', 'extension_review'
        
        if any(keyword in content or keyword in filename for keyword in [
            'installing extensions', 'extension installation'
        ]):
            return 'SketchUp_Pro_Desktop', 'Extensions_Plugins', 'extension_installation'
        
        return 'SketchUp_Pro_Desktop', 'Extensions_Plugins', 'extension_management'
    
    def _determine_desktop_category(self, content: str, filename: str) -> Tuple[str, str, str]:
        """Determine SketchUp Pro Desktop category based on content"""
        
        # Materials and rendering
        if any(keyword in content or keyword in filename for keyword in [
            'materials', 'texture', 'rendering', 'look better', 'pbr', 'ambient occlusion',
            'shadows', 'wine glass', 'coffee cup', 'realistic', 'diffusion'
        ]):
            return 'SketchUp_Pro_Desktop', 'Materials_Textures', 'applying_materials'
        
        # Import/Export
        if any(keyword in content or keyword in filename for keyword in [
            'import', 'export', 'cad files', 'reference images', 'cleanup cad', 'linework'
        ]):
            return 'SketchUp_Pro_Desktop', 'Import_Export', 'cad_import'
        
        # Modeling tools
        if any(keyword in content or keyword in filename for keyword in [
            'circle tool', 'text tool', 'coffee cup', 'hot dog', 'modeling',
            'business card', '3d text', 'polygon', 'section plane'
        ]):
            return 'SketchUp_Pro_Desktop', 'Drawing_Modeling_Tools', 'circle_tool'
        
        # Components/Groups  
        if any(keyword in content or keyword in filename for keyword in [
            'components', 'groups', 'door', 'window', 'live components',
            'component', 'editing components', 'temporary group'
        ]):
            return 'SketchUp_Pro_Desktop', 'Groups_Components', 'component_creation'
        
        # Scenes
        if any(keyword in content or keyword in filename for keyword in [
            'scenes', 'animation', 'forensics', 'tags to scenes', 'scene'
        ]):
            return 'SketchUp_Pro_Desktop', 'Scenes_Animation', 'scene_creation'
        
        # Performance  
        if any(keyword in content or keyword in filename for keyword in [
            'performance', 'optimization', 'better at sketchup'
        ]):
            return 'SketchUp_Pro_Desktop', 'Performance_Stability', 'model_optimization'
        
        # New features / updates
        if any(keyword in content or keyword in filename for keyword in [
            'new features', 'sketchup 2025', 'everything new', 'sketchup 2024',
            'top 5 new', '3d warehouse content'
        ]):
            return 'SketchUp_Pro_Desktop', 'Updates_Versioning', 'new_feature_use'
        
        # Styles and display
        if any(keyword in content or keyword in filename for keyword in [
            'watermark', 'environment', 'style', 'sketch', 'exploded model'
        ]):
            return 'SketchUp_Pro_Desktop', 'Styles_Display', 'style_creation'
        
        # Tools and interface
        if any(keyword in content or keyword in filename for keyword in [
            'select tool', 'hiding', 'measurements box', 'skill builder'
        ]):
            return 'SketchUp_Pro_Desktop', 'Getting_Started_Basics', 'tool_introduction'
        
        # Professional workflows
        if any(keyword in content or keyword in filename for keyword in [
            'architectural', 'structural plan', 'construction', 'basecamp', 
            'professional', 'firm', 'design', 'logistics', 'site', 'aquarium',
            'retail', 'event design'
        ]):
            return 'SketchUp_Pro_Desktop', 'Getting_Started_Basics', 'interface_overview'
        
        # Default to getting started for basic content
        return 'SketchUp_Pro_Desktop', 'Getting_Started_Basics', 'basic_navigation'
    
    def categorize_single_file(self, qa_file_path: Path) -> bool:
        """Categorize a single Q&A file"""
        
        platform, category, subcategory = self.analyze_qa_content(qa_file_path)
        
        if platform and category and subcategory:
            # Create target path
            target_path = self.categorized_dir / platform / category / subcategory / qa_file_path.name
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Move file
            shutil.copy2(qa_file_path, target_path)
            print(f"📁 {qa_file_path.name} → {platform}/{category}/{subcategory}")
            return True
        
        return False
    
    def categorize_all_existing_qa(self):
        """Find and categorize ALL existing Q&A files"""
        
        print("🔍 Finding all Q&A files...")
        
        # Create structure first
        self.create_taxonomy_structure()
        
        # Find all Q&A files in output directory
        all_qa_files = []
        for qa_file in self.base_output_dir.rglob("*QnA*.md"):
            # Skip files already in categorized folder
            if "categorized" not in str(qa_file):
                all_qa_files.append(qa_file)
        
        print(f"📊 Found {len(all_qa_files)} Q&A files to categorize")
        
        categorized_count = 0
        for qa_file in all_qa_files:
            if self.categorize_single_file(qa_file):
                categorized_count += 1
        
        print(f"\n✅ Successfully categorized {categorized_count} Q&A files!")
        return categorized_count
    
    def get_category_for_new_qa(self, qa_file_path: str) -> Tuple[str, str, str]:
        """Get the correct category for a new Q&A file (for future use)"""
        
        qa_path = Path(qa_file_path)
        platform, category, subcategory = self.analyze_qa_content(qa_path)
        
        if platform and category and subcategory:
            # Ensure directory exists
            target_dir = self.categorized_dir / platform / category / subcategory
            target_dir.mkdir(parents=True, exist_ok=True)
            
            return platform, category, subcategory
        
        # Default fallback
        return "SketchUp_Pro_Desktop", "Getting_Started_Basics", "basic_navigation"

def main():
    """Main function to categorize all existing Q&A files"""
    
    print("🚀 Starting comprehensive Q&A categorization...")
    
    categorizer = SketchUpQACategorizer()
    total_categorized = categorizer.categorize_all_existing_qa()
    
    print(f"\n🎉 Categorization complete!")
    print(f"📈 Total files categorized: {total_categorized}")
    print(f"📁 All Q&A files are now organized according to sample_category.md taxonomy")

if __name__ == "__main__":
    main() 