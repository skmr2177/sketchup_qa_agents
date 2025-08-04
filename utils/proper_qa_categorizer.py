#!/usr/bin/env python3
"""
Proper SketchUp Q&A Categorization System
Analyzes actual Q&A content to determine correct categorization using:
1. 28 Core Question Intent Types from sample_category.md
2. Product Platform determination
3. Specific category and subcategory mapping
"""

import os
import shutil
import re
from pathlib import Path
from typing import Tuple, Optional, List

class ProperQACategorizer:
    def __init__(self, base_output_dir="output"):
        self.base_output_dir = Path(base_output_dir)
        self.categorized_dir = self.base_output_dir / "categorized"
        
        # 28 Core Question Intent Types from sample_category.md
        self.core_question_types = [
            "bug_report", "crash_issue", "how_to_guide", "troubleshooting", 
            "feature_inquiry", "performance_issue", "compatibility_issue", 
            "installation_issue", "export_issue", "import_issue", "sync_issue",
            "account_issue", "workflow_optimization", "advanced_technique",
            "beginner_guidance", "configuration_help", "integration_help",
            "limitation_explanation", "best_practices", "concept_explanation",
            "ui_feedback", "update_inquiry", "data_loss", "licensing_issues",
            "recommendation_help"
        ]
        
        self.taxonomy = self._load_complete_taxonomy()
    
    def _load_complete_taxonomy(self):
        """Load complete 7-platform taxonomy structure"""
        return {
            "SketchUp_Pro_Desktop": {
                "Installation_Setup": ["initial_installation", "license_activation", "subscription_management", "system_requirements", "network_configuration", "trimble_id_setup", "offline_installation", "pro_features_activation"],
                "Updates_Versioning": ["changelog_review", "version_migration", "feature_deprecation", "new_feature_use", "backward_compatibility", "update_installation"],
                "Getting_Started_Basics": ["interface_overview", "workspace_setup", "basic_navigation", "tool_introduction", "menu_navigation", "panel_management", "preference_settings", "template_selection", "units_setup"],
                "Drawing_Modeling_Tools": ["line_tool", "rectangle_tool", "circle_tool", "push_pull_tool", "follow_me_tool", "offset_tool", "move_tool", "rotate_tool", "scale_tool", "tape_measure", "protractor", "text_tool", "dimension_tool", "section_plane"],
                "Selection_Navigation": ["selection_methods", "multi_selection", "orbit_navigation", "pan_navigation", "zoom_controls", "walk_through", "camera_positioning", "view_controls", "standard_views"],
                "Geometry_Modeling": ["edges_faces", "groups_components", "solid_modeling", "boolean_operations", "intersect_operations", "geometry_repair", "face_orientation", "smoothing_softening"],
                "Groups_Components": ["creating_groups", "editing_groups", "component_creation", "dynamic_components", "component_browser", "nested_components", "component_outliner", "unique_components", "component_reload", "component_sync"],
                "Materials_Textures": ["material_browser", "applying_materials", "creating_materials", "texture_positioning", "material_sampling", "transparency_settings", "custom_textures", "photo_textures"],
                "Layers_Tags": ["tag_management", "visibility_control", "layer_organization", "tag_assignment", "scene_layers", "layer_colors", "layer_export", "tag_migration"],
                "Scenes_Animation": ["scene_creation", "scene_management", "scene_transitions", "animation_settings", "camera_scenes", "walkthrough_animation", "scene_export"],
                "Styles_Display": ["edge_styles", "face_styles", "background_settings", "watermarks", "style_creation", "style_editing", "sketch_styles", "photorealistic_styles"],
                "Shadows_Lighting": ["shadow_settings", "sun_positioning", "geographic_location", "time_date_settings", "shadow_accuracy", "interior_lighting", "shadow_analysis"],
                "Import_Export": ["cad_import", "image_import", "3d_import", "2d_export", "3d_export", "pdf_export", "image_export", "animation_export", "file_optimization"],
                "Extensions_Plugins": ["extension_installation", "extension_management", "ruby_scripting", "api_development", "extension_updates", "custom_tools", "extension_compatibility", "extension_review", "extension_discovery"],
                "LayOut_Integration": ["layout_references", "model_updates", "viewport_management", "layout_sync", "layout_export", "layout_templates"],
                "Performance_Stability": ["model_optimization", "file_size_reduction", "graphics_settings", "large_model_handling", "performance_monitoring", "render_optimization", "memory_management"],
                "Data_Management_Recovery": ["file_backups", "auto_recovery", "data_corruption", "version_control", "file_organization", "cloud_sync"],
                "Troubleshooting_System_Issues": ["crash_issues", "startup_problems", "display_issues", "file_corruption", "licensing_issues", "graphics_problems", "memory_issues", "tool_failures"],
                "AI_Integration": ["ai_prompts", "automation_tools", "ai_assisted_modeling"],
                "Architectural_Workflows": ["structural_modeling", "construction_documentation", "engineering_integration"],
                "Creative_Modeling": ["artistic_techniques", "creative_projects", "decorative_elements"],
                "Professional_Workflows": ["business_modeling", "commercial_projects", "client_presentations"]
            },
            "SketchUp_Web": {
                "Account_Access": ["trimble_id_login", "subscription_access", "web_browser_compatibility", "account_management", "offline_limitations", "sync_issues"],
                "Updates_Releases": ["web_feature_rollout", "mobile_feature_gaps", "browser_updates_impact", "feature_parity", "rollback_issues"],
                "Web_Interface": ["browser_interface", "toolbar_layout", "panel_management", "touch_interface", "keyboard_shortcuts", "web_navigation", "responsive_design"],
                "Basic_Drawing_Tools": ["line_tool", "rectangle_tool", "circle_tool", "push_pull_tool", "move_tool", "rotate_tool", "scale_tool", "eraser_tool", "paint_bucket"],
                "Web_Specific_Features": ["auto_save", "cloud_storage", "web_performance", "browser_limitations", "feature_differences", "mobile_browser_support", "version_differences", "cloud_processing_limits"],
                "File_Management": ["cloud_save", "file_sharing", "export_limitations", "import_restrictions", "file_formats", "download_options", "storage_limits"],
                "Collaboration": ["sharing_models", "collaborative_editing", "real_time_sync", "access_permissions", "shared_projects", "team_features"],
                "Performance_Stability": ["browser_performance", "loading_issues", "lag_problems", "memory_limitations", "graphics_performance", "crash_recovery"],
                "Web_Limitations": ["missing_features", "export_restrictions", "extension_limitations", "advanced_tool_access", "professional_features"]
            },
            "SketchUp_Go": {
                "Mobile_Setup": ["app_installation", "account_login", "subscription_activation", "device_compatibility", "ios_requirements", "storage_management"],
                "App_Updates_Versions": ["app_store_versioning", "feature_delays", "ios_updates", "version_compatibility", "update_failures"],
                "Touch_Interface": ["touch_controls", "gesture_navigation", "multi_touch", "apple_pencil_support", "touch_precision", "interface_adaptation", "gesture_conflicts", "rotation_lock"],
                "Mobile_Drawing": ["touch_drawing", "precision_modeling", "mobile_tools", "simplified_interface", "tool_adaptation", "mobile_workflow"],
                "AR_Features": ["ar_mode", "object_placement", "ar_measurement", "real_world_scale", "ar_viewing", "environmental_tracking"],
                "Performance_Stability": ["app_performance", "device_heating", "battery_usage", "memory_management", "crash_issues", "app_optimization"],
                "Cloud_Sync_Data": ["model_sync", "cross_device_access", "cloud_storage", "sync_conflicts", "offline_access", "backup_recovery"],
                "Mobile_Limitations": ["feature_restrictions", "export_limitations", "complex_modeling_limits", "professional_features", "desktop_comparison"]
            },
            "SketchUp_Shop": {
                "Premium_Features": ["advanced_export", "unlimited_cloud_storage", "premium_templates", "enhanced_sharing", "priority_support", "commercial_use"],
                "Version_Differences": ["free_vs_premium_features", "legacy_vs_current_features", "upgrade_benefits", "feature_migration"],
                "Enhanced_Export": ["dwg_export", "pdf_export", "image_export", "3d_formats", "export_quality", "batch_export", "format_options"],
                "Cloud_Storage": ["unlimited_storage", "file_organization", "cloud_management", "storage_optimization", "backup_features", "version_history"],
                "Commercial_Use": ["licensing_compliance", "commercial_projects", "client_sharing", "professional_workflows", "business_features", "usage_rights"],
                "Collaboration_Features": ["team_sharing", "project_management", "client_access", "shared_folders", "collaborative_workflows", "review_processes", "client_review_access", "comment_tracking"]
            },
            "SketchUp_Studio": {
                "Studio_Suite": ["pro_desktop_access", "layout_integration", "style_builder_access", "advanced_importers", "premium_support", "enterprise_features"],
                "Rendering_Visualization_Tools": ["vray_access", "rendering_plugins", "style_builder", "photorealistic_export", "advanced_materials", "lighting_tools"],
                "Advanced_Import_Export": ["dwg_import", "3ds_import", "advanced_formats", "batch_processing", "format_conversion", "data_exchange", "cad_integration"],
                "Enterprise_Features": ["network_licensing", "deployment_tools", "admin_controls", "user_management", "security_features", "compliance_tools"],
                "Professional_Workflows": ["architectural_workflows", "engineering_integration", "construction_documentation", "design_development", "project_coordination"]
            },
            "LayOut": {
                "Layout_Basics": ["interface_overview", "page_setup", "document_creation", "workspace_organization", "tool_introduction"],
                "Template_Management": ["loading_templates", "custom_template_creation", "shared_templates", "template_organization", "template_sharing"],
                "Drawing_Annotation": ["line_drawing", "shape_creation", "text_tools", "dimensioning", "labeling", "leader_lines", "callouts", "markup_tools"],
                "SketchUp_Integration": ["model_references", "viewport_creation", "scene_management", "model_updates", "reference_linking", "view_synchronization"],
                "Layout_Formatting": ["page_layout", "master_pages", "layer_management", "style_formatting", "grid_settings", "alignment_tools", "object_arrangement"],
                "Export_Printing": ["pdf_export", "image_export", "printing_setup", "print_quality", "batch_export", "format_options", "output_optimization"],
                "Advanced_Features": ["auto_text", "scrapbooks", "shared_layers", "collaborative_editing", "custom_tools"],
                "Performance_Stability": ["layout_performance", "large_document_handling", "reference_issues", "crash_problems", "file_corruption", "memory_issues", "render_delays", "linked_model_refresh"]
            },
            "SketchUp_Mobile_Viewer": {
                "Viewer_Features": ["model_viewing", "navigation_controls", "measurement_tools", "section_viewing", "scene_navigation", "model_information"],
                "Cross_Platform_Support": ["android_support", "ios_behavior_differences", "version_sync", "platform_compatibility", "device_variations"],
                "File_Access": ["model_loading", "cloud_access", "local_files", "sharing_access", "file_formats", "download_issues"],
                "Mobile_Interface": ["touch_navigation", "gesture_controls", "interface_layout", "viewing_modes", "display_options", "screen_adaptation"],
                "Viewing_Limitations": ["viewer_restrictions", "editing_limitations", "export_restrictions", "feature_comparison", "upgrade_options"]
            }
        }
    
    def extract_qa_content(self, file_path: Path) -> Tuple[str, List[Tuple[str, str]]]:
        """Extract title and Q&A pairs from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return "", []
        
        # Extract title
        title_match = re.search(r'^# (.+)', content, re.MULTILINE)
        title = title_match.group(1) if title_match else ""
        
        # Extract Q&A pairs - look for numbered questions and answers
        qa_pairs = []
        
        # Pattern to match numbered questions and their answers
        qa_pattern = r'(\d+\.\s+.+?\?)\s*\n\s*(?:Answer:?\s*\n)?\s*(.+?)(?=\n\d+\.|$)'
        matches = re.findall(qa_pattern, content, re.DOTALL | re.IGNORECASE)
        
        for question, answer in matches:
            # Clean up question and answer
            question = re.sub(r'^\d+\.\s*', '', question.strip())
            answer = answer.strip()
            if question and answer:
                qa_pairs.append((question, answer))
        
        return title, qa_pairs
    
    def analyze_question_intent(self, questions: List[str], title: str) -> str:
        """Analyze questions to determine the core question intent type"""
        
        all_text = (title + " " + " ".join(questions)).lower()
        
        # How-to guides - step by step instructions
        if any(phrase in all_text for phrase in [
            'how to', 'how do', 'how can', 'step by step', 'tutorial', 'guide',
            'what are the steps', 'what is the process', 'walk through'
        ]):
            return "how_to_guide"
        
        # Feature inquiry - asking about capabilities
        if any(phrase in all_text for phrase in [
            'what is', 'what does', 'what are', 'can you', 'is it possible',
            'does sketchup', 'feature', 'capability', 'function'
        ]):
            return "feature_inquiry"
        
        # Troubleshooting - problem solving
        if any(phrase in all_text for phrase in [
            'why won\'t', 'why doesn\'t', 'not working', 'problem', 'issue',
            'error', 'fix', 'troubleshoot', 'won\'t work', 'can\'t'
        ]):
            return "troubleshooting"
        
        # Beginner guidance - basic learning
        if any(phrase in all_text for phrase in [
            'beginner', 'new to', 'getting started', 'basics', 'first time',
            'learning', 'introduction', 'fundamentals'
        ]):
            return "beginner_guidance"
        
        # Best practices - optimization and recommendations  
        if any(phrase in all_text for phrase in [
            'best practice', 'recommend', 'optimize', 'improve', 'better way',
            'efficient', 'tips', 'advice', 'should i'
        ]):
            return "best_practices"
        
        # Workflow optimization
        if any(phrase in all_text for phrase in [
            'workflow', 'efficiency', 'faster', 'automate', 'shortcut',
            'productivity', 'streamline'
        ]):
            return "workflow_optimization"
        
        # Advanced techniques
        if any(phrase in all_text for phrase in [
            'advanced', 'complex', 'professional', 'sophisticated'
        ]):
            return "advanced_technique"
        
        # Update inquiry
        if any(phrase in all_text for phrase in [
            'new feature', 'update', 'version', 'what\'s new', 'release'
        ]):
            return "update_inquiry"
        
        # Performance issues
        if any(phrase in all_text for phrase in [
            'slow', 'lag', 'performance', 'speed', 'optimize'
        ]):
            return "performance_issue"
        
        # Installation issues
        if any(phrase in all_text for phrase in [
            'install', 'setup', 'download', 'activate'
        ]):
            return "installation_issue"
        
        # Import/Export issues
        if any(phrase in all_text for phrase in [
            'import', 'export', 'file format', 'save', 'load'
        ]):
            if 'problem' in all_text or 'issue' in all_text or 'error' in all_text:
                return "import_issue" if 'import' in all_text else "export_issue"
            else:
                return "how_to_guide"
        
        # Default to feature inquiry for most questions
        return "feature_inquiry"
    
    def determine_platform(self, title: str, qa_pairs: List[Tuple[str, str]]) -> str:
        """Determine product platform based on content"""
        
        all_content = title + " " + " ".join([q + " " + a for q, a in qa_pairs])
        all_content = all_content.lower()
        
        # LayOut detection - ONLY if explicitly about LayOut
        if any(keyword in all_content for keyword in [
            'layout', 'clipping mask', 'scrapbook', 'viewport', 'draft mode'
        ]) and ('layout' in title.lower() or 'layout' in all_content):
            return "LayOut"
        
        # SketchUp Go (mobile/iPad) - ONLY if explicitly about iPad/mobile
        if any(keyword in all_content for keyword in [
            'ipad', 'mobile', 'touch', 'ar mode', 'apple pencil', 'gesture'
        ]) and ('ipad' in title.lower() or 'mobile' in title.lower() or 'hot dog stand on the ipad' in all_content):
            return "SketchUp_Go"
        
        # SketchUp Studio (professional/rendering) - ONLY if explicitly about V-Ray/Studio features
        if any(keyword in all_content for keyword in [
            'vray', 'v-ray', 'style builder', 'enterprise', 'studio suite'
        ]) and ('vray' in title.lower() or 'v-ray' in title.lower() or 'studio' in title.lower()):
            return "SketchUp_Studio"
        
        # SketchUp Web - ONLY if explicitly about web version
        if any(keyword in all_content for keyword in [
            'web browser', 'browser', 'web version', 'online'
        ]) and ('web' in title.lower() or 'browser' in title.lower()):
            return "SketchUp_Web"
        
        # SketchUp Shop - ONLY if explicitly about Shop features
        if any(keyword in all_content for keyword in [
            'shop', 'premium', 'commercial use', 'dwg export'
        ]) and ('shop' in title.lower() or 'premium' in title.lower()):
            return "SketchUp_Shop"
        
        # SketchUp Mobile Viewer - ONLY if explicitly about viewer
        if any(keyword in all_content for keyword in [
            'viewer', 'viewing only', 'mobile viewer'
        ]) and ('viewer' in title.lower() or 'viewing' in title.lower()):
            return "SketchUp_Mobile_Viewer"
        
        # Default to SketchUp Pro Desktop for most content
        return "SketchUp_Pro_Desktop"
    
    def determine_category_subcategory(self, platform: str, question_intent: str, 
                                     title: str, qa_pairs: List[Tuple[str, str]]) -> Tuple[str, str]:
        """Determine specific category and subcategory"""
        
        all_content = title + " " + " ".join([q + " " + a for q, a in qa_pairs])
        all_content = all_content.lower()
        
        if platform == "SketchUp_Pro_Desktop":
            return self._categorize_desktop_content(question_intent, all_content)
        elif platform == "LayOut":
            return self._categorize_layout_content(question_intent, all_content)
        elif platform == "SketchUp_Go":
            return self._categorize_go_content(question_intent, all_content)
        elif platform == "SketchUp_Studio":
            return self._categorize_studio_content(question_intent, all_content)
        else:
            return "Getting_Started_Basics", "interface_overview"
    
    def _categorize_desktop_content(self, question_intent: str, content: str) -> Tuple[str, str]:
        """Categorize SketchUp Pro Desktop content based on detailed Q&A analysis"""
        
        # 1. EXTENSIONS AND PLUGINS - Check for extension-specific content
        if any(keyword in content for keyword in [
            'extension', 'plugin', 'bezier', 'placemaker', 'round corner',
            'installing extensions', 'extension warehouse', 'extension inspection'
        ]):
            if any(keyword in content for keyword in ['installing', 'install', 'installation']):
                return "Extensions_Plugins", "extension_installation"
            else:
                return "Extensions_Plugins", "extension_review"
        
        # 2. SOLID TOOLS AND GEOMETRY - Check for solid modeling content
        if any(keyword in content for keyword in [
            'solid tool', 'union', 'outer shell', 'boolean', 'geometry', 'solid modeling'
        ]):
            return "Geometry_Modeling", "boolean_operations"
        
        # 3. MATERIALS AND RENDERING - Check for materials/visualization content
        if any(keyword in content for keyword in [
            'material', 'texture', 'look better', 'ambient occlusion', 'shadows', 'rendering',
            'pbr', 'realistic', 'visualization', 'lighting'
        ]):
            return "Materials_Textures", "applying_materials"
        
        # 4. IMPORT/EXPORT - Check for file handling content
        if any(keyword in content for keyword in [
            'import', 'export', 'cad', 'reference image', 'cleanup', 'file format',
            'linework', 'tracing'
        ]):
            return "Import_Export", "cad_import"
        
        # 5. DRAWING AND MODELING TOOLS - Check for specific tool tutorials
        # Check for rotate tool specifically first
        if any(keyword in content for keyword in [
            'rotate tool', 'rotation', 'rotating', 'rotate around', 'center handles',
            'rotation grips', 'rotation points', '2025 improvements'
        ]):
            return "Drawing_Modeling_Tools", "rotate_tool"
        
        # Check for move tool specifically
        if any(keyword in content for keyword in [
            'move tool', 'moving objects', 'translation', 'move tool operations'
        ]):
            return "Drawing_Modeling_Tools", "move_tool"
        
        # Check for other specific tools
        if any(keyword in content for keyword in [
            'modeling', 'circle tool', 'text tool', 'section plane', 'select tool',
            'hot dog', 'coffee cup', 'wine glass', 'business card', 'finger joints',
            'template', 'snowflakes', 'measurements'
        ]):
            return "Drawing_Modeling_Tools", "push_pull_tool"
        
        # 6. GROUPS AND COMPONENTS - Check for component/group content
        if any(keyword in content for keyword in [
            'component', 'group', 'door', 'window', 'live component', 'editing components'
        ]):
            return "Groups_Components", "component_creation"
        
        # 7. SCENES AND ANIMATION - Check for scene management
        if any(keyword in content for keyword in [
            'scene', 'animation', 'tags to scenes', 'scene update'
        ]):
            return "Scenes_Animation", "scene_creation"
        
        # 8. UPDATES AND VERSIONING - Check for new features
        if any(keyword in content for keyword in [
            'new features', '2025', '2024', 'everything new', 'what\'s new'
        ]):
            return "Updates_Versioning", "new_feature_use"
        
        # 9. PERFORMANCE AND OPTIMIZATION - Check for performance content
        if any(keyword in content for keyword in [
            'performance', 'optimization', 'workflow', 'efficiency', 'time-saving'
        ]):
            return "Performance_Stability", "model_optimization"
        
        # 10. INSTALLATION AND SETUP - Check for installation content
        if any(keyword in content for keyword in [
            'installation', 'install', 'setup', 'download', 'activate'
        ]):
            return "Installation_Setup", "initial_installation"
        
        # 11. AI AND AUTOMATION - Check for AI-related content
        if any(keyword in content for keyword in [
            'ai', 'artificial intelligence', 'automation', 'prompt', 'diffusion'
        ]):
            return "AI_Integration", "ai_prompts"
        
        # 12. ARCHITECTURAL WORKFLOWS - Check for professional workflows
        if any(keyword in content for keyword in [
            'architectural', 'structural', 'engineering', 'logistics', 'construction',
            'basecamp', 'firm', 'aquarium', 'retail', 'event design'
        ]):
            return "Architectural_Workflows", "structural_modeling"
        
        # 13. CREATIVE MODELING - Check for artistic/creative content
        if any(keyword in content for keyword in [
            'creative', 'artistic', 'basket', 'finger joints', 'templates', 'snowflakes'
        ]):
            return "Creative_Modeling", "artistic_techniques"
        
        # 14. PROFESSIONAL WORKFLOWS - Check for business/professional content
        if any(keyword in content for keyword in [
            'professional', 'business', 'commercial', 'practice', 'workflow'
        ]):
            return "Professional_Workflows", "business_modeling"
        
        # 15. BASIC TOOLS AND INTERFACE - Only for truly basic content
        if any(keyword in content for keyword in [
            'interface', 'basic', 'getting started', 'first time', 'beginner',
            'square one', 'fundamentals'
        ]):
            if question_intent == "beginner_guidance":
                return "Getting_Started_Basics", "basic_navigation"
            else:
                return "Getting_Started_Basics", "tool_introduction"
        
        # 16. LAYERS AND TAGS - Check for layer/tag content
        if any(keyword in content for keyword in [
            'layer', 'tag', 'visibility', 'organization'
        ]):
            return "Layers_Tags", "tag_management"
        
        # 17. STYLES AND DISPLAY - Check for style/display content
        if any(keyword in content for keyword in [
            'style', 'display', 'edge style', 'face style', 'background'
        ]):
            return "Styles_Display", "edge_styles"
        
        # 18. SHADOWS AND LIGHTING - Check for lighting content
        if any(keyword in content for keyword in [
            'shadow', 'lighting', 'sun', 'geographic', 'time date'
        ]):
            return "Shadows_Lighting", "shadow_settings"
        
        # 19. SELECTION AND NAVIGATION - Check for selection/navigation
        if any(keyword in content for keyword in [
            'selection', 'navigation', 'orbit', 'pan', 'zoom', 'walk through'
        ]):
            return "Selection_Navigation", "selection_methods"
        
        # 20. DATA MANAGEMENT - Check for file/data management
        if any(keyword in content for keyword in [
            'backup', 'recovery', 'file management', 'data', 'corruption'
        ]):
            return "Data_Management_Recovery", "file_backups"
        
        # If none of the above match, analyze the content more carefully
        # Look for specific patterns in the questions and answers
        if 'how to' in content and 'model' in content:
            return "Drawing_Modeling_Tools", "push_pull_tool"
        
        if 'tutorial' in content or 'skill builder' in content:
            # Check if it's about a specific tool or general learning
            if any(keyword in content for keyword in ['tool', 'technique', 'method']):
                return "Drawing_Modeling_Tools", "push_pull_tool"
            else:
                return "Getting_Started_Basics", "tool_introduction"
        
        # Last resort - only use Getting_Started_Basics for truly basic content
        if question_intent == "beginner_guidance":
            return "Getting_Started_Basics", "basic_navigation"
        else:
            # Default to a more specific category based on content analysis
            return "Drawing_Modeling_Tools", "push_pull_tool"
    
    def _categorize_layout_content(self, question_intent: str, content: str) -> Tuple[str, str]:
        """Categorize LayOut content"""
        
        if 'clipping mask' in content or 'scrapbook' in content:
            return "Advanced_Features", "auto_text"
        
        if 'draft mode' in content or 'performance' in content:
            return "Performance_Stability", "layout_performance"
        
        return "Layout_Basics", "interface_overview"
    
    def _categorize_go_content(self, question_intent: str, content: str) -> Tuple[str, str]:
        """Categorize SketchUp Go content"""
        
        if 'ar mode' in content or 'ar' in content:
            return "AR_Features", "ar_mode"
        
        if any(keyword in content for keyword in ['touch', 'gesture', 'apple pencil']):
            return "Touch_Interface", "touch_controls"
        
        return "Mobile_Drawing", "touch_drawing"
    
    def _categorize_studio_content(self, question_intent: str, content: str) -> Tuple[str, str]:
        """Categorize SketchUp Studio content"""
        
        if any(keyword in content for keyword in ['vray', 'v-ray', 'rendering', 'pbr']):
            return "Rendering_Visualization_Tools", "vray_access"
        
        return "Professional_Workflows", "architectural_workflows"
    
    def categorize_single_qa_file(self, qa_file_path: Path) -> bool:
        """Categorize a single Q&A file based on actual content analysis"""
        
        # Skip empty or problematic files
        try:
            file_size = qa_file_path.stat().st_size
            if file_size < 100:  # Skip very small files
                print(f"⚠️  Skipping {qa_file_path.name} - file too small ({file_size} bytes)")
                return False
        except:
            return False
        
        # Extract Q&A content
        title, qa_pairs = self.extract_qa_content(qa_file_path)
        
        if not qa_pairs:
            print(f"⚠️  Skipping {qa_file_path.name} - no Q&A pairs found")
            return False
        
        # Analyze content
        questions = [q for q, a in qa_pairs]
        question_intent = self.analyze_question_intent(questions, title)
        platform = self.determine_platform(title, qa_pairs)
        category, subcategory = self.determine_category_subcategory(
            platform, question_intent, title, qa_pairs
        )
        
        # Create target path
        target_path = self.categorized_dir / platform / category / subcategory / qa_file_path.name
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Move file to correct location (don't copy, move it)
        if qa_file_path != target_path:
            shutil.move(str(qa_file_path), str(target_path))
            print(f"📁 {qa_file_path.name}")
            print(f"   📊 Q&A Pairs: {len(qa_pairs)}")
            print(f"   🎯 Intent: {question_intent}")
            print(f"   📂 {platform}/{category}/{subcategory}")
            print()
            return True
        else:
            return False
    
    def categorize_all_qa_files(self):
        """Categorize all Q&A files using proper content analysis"""
        
        print("🧠 Starting proper Q&A content analysis and categorization...")
        print("📊 Using 28 core question intent types from sample_category.md")
        print("🔍 Analyzing actual Q&A pairs content for accurate categorization")
        print()
        
        # Create taxonomy structure
        for platform, categories in self.taxonomy.items():
            for category, subcategories in categories.items():
                for subcategory in subcategories:
                    dir_path = self.categorized_dir / platform / category / subcategory
                    dir_path.mkdir(parents=True, exist_ok=True)
        
        # Find ALL Q&A files (including those already categorized to re-categorize properly)
        all_qa_files = []
        for qa_file in self.base_output_dir.rglob("*QnA*.md"):
            all_qa_files.append(qa_file)
        
        print(f"📋 Found {len(all_qa_files)} total Q&A files to analyze")
        print()
        
        categorized_count = 0
        skipped_count = 0
        moved_count = 0
        
        for qa_file in all_qa_files:
            # Skip if already in correct location
            if self.is_file_in_correct_location(qa_file):
                continue
                
            if self.categorize_single_qa_file(qa_file):
                categorized_count += 1
                moved_count += 1
            else:
                skipped_count += 1
        
        print("🎉 Proper Q&A categorization complete!")
        print(f"✅ Successfully categorized: {categorized_count} files")
        print(f"📦 Moved to correct locations: {moved_count} files")
        print(f"⚠️  Skipped (empty/invalid): {skipped_count} files")
        print(f"📂 Files organized using actual Q&A content analysis")
    
    def is_file_in_correct_location(self, qa_file_path: Path) -> bool:
        """Check if file is already in the correct categorized location"""
        try:
            title, qa_pairs = self.extract_qa_content(qa_file_path)
            if not qa_pairs:
                return False
                
            questions = [q for q, a in qa_pairs]
            question_intent = self.analyze_question_intent(questions, title)
            platform = self.determine_platform(title, qa_pairs)
            category, subcategory = self.determine_category_subcategory(
                platform, question_intent, title, qa_pairs
            )
            
            expected_path = self.categorized_dir / platform / category / subcategory / qa_file_path.name
            return qa_file_path == expected_path
        except:
            return False

def main():
    """Main function for proper Q&A categorization"""
    categorizer = ProperQACategorizer()
    categorizer.categorize_all_qa_files()

if __name__ == "__main__":
    main() 