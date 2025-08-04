#!/usr/bin/env python3
"""
Intelligent SketchUp Q&A Categorization System
Analyzes Q&A content to determine:
1. Core Question Intent (28 types from sample_category.md)
2. Product Platform 
3. Specific Subcategory within platform
"""

import os
import shutil
import re
from pathlib import Path
from typing import Tuple, Optional, List

class IntelligentQACategorizer:
    def __init__(self, base_output_dir="output"):
        self.base_output_dir = Path(base_output_dir)
        self.categorized_dir = self.base_output_dir / "categorized"
        
        # Core Question Types from sample_category.md
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
        
        # Load platform taxonomy
        self.taxonomy = self._load_taxonomy()
    
    def _load_taxonomy(self):
        """Load complete taxonomy structure"""
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
                ],
                "AI_Integration": [
                    "ai_prompts", "automation_tools", "ai_assisted_modeling"
                ],
                "Architectural_Workflows": [
                    "structural_modeling", "construction_documentation", "engineering_integration"
                ],
                "Creative_Modeling": [
                    "artistic_techniques", "creative_projects", "decorative_elements"
                ],
                "Professional_Workflows": [
                    "business_modeling", "commercial_projects", "client_presentations"
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
            "SketchUp_Go": {
                "Mobile_Setup": [
                    "app_installation", "account_login", "subscription_activation",
                    "device_compatibility", "ios_requirements", "storage_management"
                ],
                "Touch_Interface": [
                    "touch_controls", "gesture_navigation", "multi_touch",
                    "apple_pencil_support", "touch_precision", "interface_adaptation"
                ],
                "Mobile_Drawing": [
                    "touch_drawing", "precision_modeling", "mobile_tools",
                    "simplified_interface", "tool_adaptation", "mobile_workflow"
                ],
                "AR_Features": [
                    "ar_mode", "object_placement", "ar_measurement",
                    "real_world_scale", "ar_viewing", "environmental_tracking"
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

    def analyze_qa_content(self, file_path: Path) -> Tuple[str, str, str, str]:
        """
        Analyze Q&A content to determine:
        - Core question intent
        - Product platform
        - Category
        - Subcategory
        """
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return "how_to_guide", "SketchUp_Pro_Desktop", "Getting_Started_Basics", "basic_navigation"
        
        # Extract title and questions for analysis
        title = self._extract_title(content)
        questions = self._extract_questions(content)
        all_text = (title + " " + " ".join(questions)).lower()
        
        # Step 1: Determine core question intent
        question_intent = self._determine_question_intent(title, questions, content)
        
        # Step 2: Determine product platform
        platform = self._determine_platform(title, content, all_text)
        
        # Step 3: Determine category and subcategory
        category, subcategory = self._determine_category_subcategory(
            platform, question_intent, title, content, all_text
        )
        
        return question_intent, platform, category, subcategory
    
    def _extract_title(self, content: str) -> str:
        """Extract the main title from Q&A content"""
        lines = content.split('\n')
        for line in lines[:10]:
            if line.startswith('# '):
                return line[2:].strip()
        return ""
    
    def _extract_questions(self, content: str) -> List[str]:
        """Extract all questions from Q&A content"""
        questions = []
        lines = content.split('\n')
        
        for line in lines:
            # Look for numbered questions or questions ending with ?
            if (re.match(r'^\d+\.', line.strip()) and '?' in line) or line.strip().endswith('?'):
                questions.append(line.strip())
        
        return questions
    
    def _determine_question_intent(self, title: str, questions: List[str], content: str) -> str:
        """Determine the core question intent type"""
        
        title_lower = title.lower()
        content_lower = content.lower()
        all_questions = " ".join(questions).lower()
        
        # How-to guides (most common for tutorials)
        if any(keyword in title_lower for keyword in [
            'how to', 'step by step', 'tutorial', 'guide', 'skill builder',
            'modeling', 'creating', 'building', 'drawing'
        ]):
            return "how_to_guide"
        
        # Feature inquiry (about tools and capabilities)
        if any(keyword in title_lower or keyword in all_questions for keyword in [
            'what is', 'what does', 'extension inspection', 'tool', 'feature',
            'capability', 'new in', 'everything new'
        ]):
            return "feature_inquiry"
        
        # Workflow optimization
        if any(keyword in title_lower for keyword in [
            'workflow', 'efficiency', 'optimization', 'turbocharge', 'better',
            'tips', 'best practices', 'quick'
        ]):
            return "workflow_optimization"
        
        # Advanced techniques
        if any(keyword in title_lower for keyword in [
            'advanced', 'professional', 'refined', 'complex', 'ai',
            'pbr', 'realistic', 'rendering'
        ]):
            return "advanced_technique"
        
        # Update inquiries
        if any(keyword in title_lower for keyword in [
            'new features', '2025', '2024', "what's new", 'update'
        ]):
            return "update_inquiry"
        
        # Troubleshooting
        if any(keyword in title_lower or keyword in all_questions for keyword in [
            'problem', 'issue', 'fix', 'won\'t', 'error', 'troubleshoot'
        ]):
            return "troubleshooting"
        
        # Beginner guidance
        if any(keyword in title_lower for keyword in [
            'beginner', 'getting started', 'basics', 'square one', 'first'
        ]):
            return "beginner_guidance"
        
        # Best practices
        if any(keyword in title_lower for keyword in [
            'best practices', 'tips', 'better', 'efficient'
        ]):
            return "best_practices"
        
        # Default to how_to_guide for most content
        return "how_to_guide"
    
    def _determine_platform(self, title: str, content: str, all_text: str) -> str:
        """Determine the product platform"""
        
        # LayOut detection (highest priority)
        if any(keyword in all_text for keyword in [
            'layout', 'draft mode', 'clipping mask', 'scrapbook', 'viewport'
        ]):
            return "LayOut"
        
        # SketchUp Go (mobile/iPad)
        if any(keyword in all_text for keyword in [
            'ipad', 'mobile', 'touch', 'ar mode', 'apple pencil', 'gesture',
            'hot dog stand on the ipad'
        ]):
            return "SketchUp_Go"
        
        # SketchUp Studio (professional/enterprise features)
        if any(keyword in all_text for keyword in [
            'vray', 'v-ray', 'professional 3d practice', 'enterprise', 'studio',
            'rendering plugins', 'style builder', 'advanced materials', 'pbr materials',
            'realistic pbr', 'rendering face-off'
        ]):
            return "SketchUp_Studio"
        
        # SketchUp Web (browser-based)
        if any(keyword in all_text for keyword in [
            'web browser', 'browser', 'web version', 'cloud save', 'auto save',
            'web interface', 'online version'
        ]):
            return "SketchUp_Web"
        
        # SketchUp Shop (premium web features)
        if any(keyword in all_text for keyword in [
            'shop', 'premium', 'commercial use', 'unlimited storage', 'dwg export'
        ]):
            return "SketchUp_Shop"
        
        # SketchUp Mobile Viewer (viewing only)
        if any(keyword in all_text for keyword in [
            'viewer', 'viewing only', 'mobile viewer', 'android viewer'
        ]):
            return "SketchUp_Mobile_Viewer"
        
        # Most content defaults to SketchUp Pro Desktop
        return "SketchUp_Pro_Desktop"
    
    def _determine_category_subcategory(self, platform: str, question_intent: str, 
                                      title: str, content: str, all_text: str) -> Tuple[str, str]:
        """Determine specific category and subcategory based on content analysis"""
        
        if platform == "LayOut":
            return self._categorize_layout_content(question_intent, title, all_text)
        elif platform == "SketchUp_Go":
            return self._categorize_go_content(question_intent, title, all_text)
        elif platform == "SketchUp_Studio":
            return self._categorize_studio_content(question_intent, title, all_text)
        elif platform == "SketchUp_Web":
            return self._categorize_web_content(question_intent, title, all_text)
        elif platform == "SketchUp_Shop":
            return self._categorize_shop_content(question_intent, title, all_text)
        elif platform == "SketchUp_Mobile_Viewer":
            return self._categorize_viewer_content(question_intent, title, all_text)
        else:  # SketchUp_Pro_Desktop
            return self._categorize_desktop_content(question_intent, title, all_text)
    
    def _categorize_layout_content(self, question_intent: str, title: str, all_text: str) -> Tuple[str, str]:
        """Categorize LayOut content"""
        
        if 'draft mode' in all_text or 'performance' in all_text:
            return "Performance_Stability", "layout_performance"
        
        if any(keyword in all_text for keyword in ['clipping mask', 'scrapbook', 'auto text']):
            return "Advanced_Features", "auto_text"
        
        if 'floorplan' in all_text or 'export' in all_text:
            return "Export_Printing", "pdf_export"
        
        return "Layout_Basics", "interface_overview"
    
    def _categorize_go_content(self, question_intent: str, title: str, all_text: str) -> Tuple[str, str]:
        """Categorize SketchUp Go content"""
        
        if 'ar' in all_text or 'ar mode' in all_text:
            return "AR_Features", "ar_mode"
        
        if any(keyword in all_text for keyword in ['touch', 'gesture', 'apple pencil']):
            return "Touch_Interface", "touch_controls"
        
        return "Mobile_Drawing", "touch_drawing"
    
    def _categorize_studio_content(self, question_intent: str, title: str, all_text: str) -> Tuple[str, str]:
        """Categorize SketchUp Studio content"""
        
        if any(keyword in all_text for keyword in ['vray', 'v-ray', 'rendering', 'pbr']):
            return "Rendering_Visualization_Tools", "vray_access"
        
        if any(keyword in all_text for keyword in ['advanced', 'professional', 'enterprise']):
            return "Professional_Workflows", "architectural_workflows"
        
        return "Studio_Suite", "pro_desktop_access"
    
    def _categorize_web_content(self, question_intent: str, title: str, all_text: str) -> Tuple[str, str]:
        """Categorize SketchUp Web content"""
        
        if 'browser' in all_text:
            return "Web_Interface", "browser_interface"
        
        if any(keyword in all_text for keyword in ['cloud', 'save', 'storage']):
            return "Web_Specific_Features", "cloud_storage"
        
        return "Basic_Drawing_Tools", "push_pull_tool"
    
    def _categorize_shop_content(self, question_intent: str, title: str, all_text: str) -> Tuple[str, str]:
        """Categorize SketchUp Shop content"""
        
        if any(keyword in all_text for keyword in ['export', 'dwg', 'pdf']):
            return "Enhanced_Export", "dwg_export"
        
        if any(keyword in all_text for keyword in ['premium', 'commercial']):
            return "Premium_Features", "commercial_use"
        
        return "Cloud_Storage", "unlimited_storage"
    
    def _categorize_viewer_content(self, question_intent: str, title: str, all_text: str) -> Tuple[str, str]:
        """Categorize SketchUp Mobile Viewer content"""
        
        if 'navigation' in all_text or 'viewing' in all_text:
            return "Viewer_Features", "model_viewing"
        
        if any(keyword in all_text for keyword in ['android', 'ios', 'mobile']):
            return "Cross_Platform_Support", "android_support"
        
        return "Mobile_Interface", "touch_navigation"
    
    def _categorize_desktop_content(self, question_intent: str, title: str, all_text: str) -> Tuple[str, str]:
        """Categorize SketchUp Pro Desktop content"""
        
        # Extensions and plugins
        if any(keyword in all_text for keyword in [
            'extension', 'bezier', 'placemaker', 'round corner', 'plugin'
        ]):
            if 'inspection' in all_text:
                return "Extensions_Plugins", "extension_review"
            else:
                return "Extensions_Plugins", "extension_installation"
        
        # Materials and textures
        if any(keyword in all_text for keyword in [
            'material', 'texture', 'pbr', 'realistic', 'rendering', 'look better',
            'ambient occlusion', 'shadows', 'diffusion'
        ]):
            return "Materials_Textures", "applying_materials"
        
        # Import/Export
        if any(keyword in all_text for keyword in [
            'import', 'export', 'cad', 'reference image', 'cleanup'
        ]):
            return "Import_Export", "cad_import"
        
        # Drawing and modeling tools
        if any(keyword in all_text for keyword in [
            'hot dog', 'coffee cup', 'wine glass', 'modeling', 'circle tool',
            'text tool', '3d model', 'section plane'
        ]):
            return "Drawing_Modeling_Tools", "push_pull_tool"
        
        # Groups and components
        if any(keyword in all_text for keyword in [
            'component', 'group', 'door', 'window', 'live component'
        ]):
            return "Groups_Components", "component_creation"
        
        # Scenes and animation
        if any(keyword in all_text for keyword in [
            'scene', 'animation', 'tags to scenes'
        ]):
            return "Scenes_Animation", "scene_creation"
        
        # Updates and versioning
        if any(keyword in all_text for keyword in [
            'new features', '2025', '2024', 'everything new', 'warehouse content'
        ]):
            return "Updates_Versioning", "new_feature_use"
        
        # Performance
        if question_intent == "workflow_optimization" or 'performance' in all_text:
            return "Performance_Stability", "model_optimization"
        
        # Tools and interface
        if any(keyword in all_text for keyword in [
            'select tool', 'hiding', 'measurements', 'skill builder', 'interface'
        ]):
            return "Getting_Started_Basics", "tool_introduction"
        
        # AI and automation features (NEW DYNAMIC CATEGORY)
        if any(keyword in all_text for keyword in [
            'ai', 'artificial intelligence', 'automation', 'prompt', 'diffusion'
        ]):
            return "AI_Integration", "ai_prompts"
        
        # Architectural workflows (NEW DYNAMIC CATEGORY)  
        if any(keyword in all_text for keyword in [
            'structural', 'engineering', 'logistics', 'construction', 'basecamp',
            'architectural', 'firm', 'aquarium', 'retail', 'event design'
        ]):
            return "Architectural_Workflows", "structural_modeling"
        
        # Creative modeling (NEW DYNAMIC CATEGORY)
        if any(keyword in all_text for keyword in [
            'creative', 'artistic', 'basket', 'finger joints', 'templates', 'snowflakes'
        ]):
            return "Creative_Modeling", "artistic_techniques"
        
        # Professional workflows (NEW DYNAMIC CATEGORY)
        if any(keyword in all_text for keyword in [
            'professional', 'business', 'commercial', 'practice'
        ]):
            return "Professional_Workflows", "business_modeling"
        
        # Default based on question intent
        if question_intent == "beginner_guidance":
            return "Getting_Started_Basics", "basic_navigation"
        elif question_intent == "advanced_technique":
            return "Geometry_Modeling", "solid_modeling"
        else:
            return "Getting_Started_Basics", "interface_overview"
    
    def create_taxonomy_structure(self):
        """Create complete directory structure"""
        print("🏗️  Creating intelligent taxonomy structure...")
        
        for platform, categories in self.taxonomy.items():
            for category, subcategories in categories.items():
                for subcategory in subcategories:
                    dir_path = self.categorized_dir / platform / category / subcategory
                    dir_path.mkdir(parents=True, exist_ok=True)
        
        print("✅ Taxonomy structure created!")
    
    def categorize_single_file(self, qa_file_path: Path) -> bool:
        """Categorize a single Q&A file with intelligent analysis"""
        
        question_intent, platform, category, subcategory = self.analyze_qa_content(qa_file_path)
        
        # Create target path
        target_path = self.categorized_dir / platform / category / subcategory / qa_file_path.name
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy file to categorized location
        shutil.copy2(qa_file_path, target_path)
        print(f"📁 {qa_file_path.name}")
        print(f"   Intent: {question_intent} → {platform}/{category}/{subcategory}")
        return True
    
    def categorize_all_qa_intelligently(self):
        """Intelligently categorize all Q&A files"""
        
        print("🧠 Starting intelligent Q&A categorization...")
        print("📊 Analyzing content for question intent and platform detection...")
        
        # Create structure (don't delete existing files)
        self.create_taxonomy_structure()
        
        # Find all Q&A files that are NOT already in categorized folder
        all_qa_files = []
        for qa_file in self.base_output_dir.rglob("*QnA*.md"):
            if "categorized" not in str(qa_file):
                all_qa_files.append(qa_file)
        
        print(f"🔍 Found {len(all_qa_files)} uncategorized Q&A files to analyze")
        
        categorized_count = 0
        for qa_file in all_qa_files:
            if self.categorize_single_file(qa_file):
                categorized_count += 1
        
        print(f"\n🎉 Intelligent categorization complete!")
        print(f"📈 Total files categorized: {categorized_count}")
        print(f"🧠 All Q&A files analyzed for question intent and properly categorized")

def main():
    """Main function for intelligent categorization"""
    
    categorizer = IntelligentQACategorizer()
    categorizer.categorize_all_qa_intelligently()

if __name__ == "__main__":
    main() 