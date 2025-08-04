#!/usr/bin/env python3
"""
Enhanced SketchUp Q&A Categorization System
Addresses classification issues with:
1. Refined keyword matching with context requirements
2. Content validation to ensure proper categorization
3. Improved priority order for more specific categories first
4. Manual review capabilities for uncertain classifications
"""

import os
import shutil
import re
import json
from pathlib import Path
from typing import Tuple, Optional, List, Dict, Set
from datetime import datetime

class EnhancedQACategorizer:
    def __init__(self, base_output_dir="output"):
        self.base_output_dir = Path(base_output_dir)
        self.categorized_dir = self.base_output_dir / "categorized"
        self.review_dir = self.base_output_dir / "review_needed"
        
        # Enhanced keyword patterns with context requirements
        self.keyword_patterns = self._load_enhanced_patterns()
        
        # Content validation rules
        self.validation_rules = self._load_validation_rules()
        
        # Manual review triggers
        self.review_triggers = self._load_review_triggers()
        
        self.taxonomy = self._load_complete_taxonomy()
        
    def _load_enhanced_patterns(self) -> Dict[str, Dict]:
        """Load enhanced keyword patterns with context requirements"""
        return {
            "extensions_plugins": {
                "primary_keywords": ["extension", "plugin", "warehouse"],
                "context_keywords": ["install", "install", "review", "bezier", "placemaker", "round corner"],
                "exclusion_keywords": ["extension of", "extend", "extending", "extended"],
                "min_matches": 2,
                "require_context": True
            },
            "materials_textures": {
                "primary_keywords": ["material", "texture", "pbr", "ambient occlusion"],
                "context_keywords": ["apply", "create", "edit", "realistic", "visualization"],
                "exclusion_keywords": [],
                "min_matches": 2,
                "require_context": False
            },
            "import_export": {
                "primary_keywords": ["import", "export", "cad", "file format"],
                "context_keywords": ["reference image", "cleanup", "linework", "tracing"],
                "exclusion_keywords": [],
                "min_matches": 2,
                "require_context": False
            },
            "layout_integration": {
                "primary_keywords": ["layout", "viewport", "documentation"],
                "context_keywords": ["modification tools", "move", "rotate", "scale", "inferencing"],
                "exclusion_keywords": [],
                "min_matches": 2,
                "require_context": True
            },
            "specific_tools": {
                "rotate_tool": {
                    "keywords": ["rotate tool", "rotation", "rotating", "center handles", "rotation grips"],
                    "min_matches": 2
                },
                "move_tool": {
                    "keywords": ["move tool", "moving objects", "translation"],
                    "min_matches": 2
                },
                "text_tool": {
                    "keywords": ["text tool", "3d text", "text annotation", "leader"],
                    "min_matches": 2
                },
                "section_plane": {
                    "keywords": ["section plane", "section cut", "section view"],
                    "min_matches": 2
                }
            }
        }
    
    def _load_validation_rules(self) -> Dict[str, List[str]]:
        """Load validation rules for each category"""
        return {
            "Extensions_Plugins": [
                "extension", "plugin", "warehouse", "install", "bezier", "placemaker"
            ],
            "Materials_Textures": [
                "material", "texture", "pbr", "ambient occlusion", "realistic"
            ],
            "Import_Export": [
                "import", "export", "cad", "file", "reference image"
            ],
            "LayOut_Integration": [
                "layout", "viewport", "documentation", "modification tools"
            ],
            "Drawing_Modeling_Tools": [
                "tool", "modeling", "drawing", "geometry", "shape"
            ]
        }
    
    def _load_review_triggers(self) -> List[str]:
        """Load triggers that indicate manual review is needed"""
        return [
            "uncertain", "ambiguous", "multiple categories", "edge case",
            "mixed content", "unclear intent", "conflicting keywords"
        ]
    
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
                "Troubleshooting_System_Issues": ["crash_issues", "startup_problems", "display_issues", "file_corruption", "licensing_issues", "graphics_problems", "memory_issues", "tool_failures"]
            },
            "SketchUp_Web_Browser_based": {
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
            "SketchUp_Go_iPad_Mobile": {
                "Mobile_Setup": ["app_installation", "account_login", "subscription_activation", "device_compatibility", "ios_requirements", "storage_management"],
                "App_Updates_Versions": ["app_store_versioning", "feature_delays", "ios_updates", "version_compatibility", "update_failures"],
                "Touch_Interface": ["touch_controls", "gesture_navigation", "multi_touch", "apple_pencil_support", "touch_precision", "interface_adaptation", "gesture_conflicts", "rotation_lock"],
                "Mobile_Drawing": ["touch_drawing", "precision_modeling", "mobile_tools", "simplified_interface", "tool_adaptation", "mobile_workflow"],
                "AR_Features": ["ar_mode", "object_placement", "ar_measurement", "real_world_scale", "ar_viewing", "environmental_tracking"],
                "Performance_Stability": ["app_performance", "device_heating", "battery_usage", "memory_management", "crash_issues", "app_optimization"],
                "Cloud_Sync_Data": ["model_sync", "cross_device_access", "cloud_storage", "sync_conflicts", "offline_access", "backup_recovery"],
                "Mobile_Limitations": ["feature_restrictions", "export_limitations", "complex_modeling_limits", "professional_features", "desktop_comparison"]
            },
            "SketchUp_Shop_Web_Premium": {
                "Premium_Features": ["advanced_export", "unlimited_cloud_storage", "premium_templates", "enhanced_sharing", "priority_support", "commercial_use"],
                "Version_Differences": ["free_vs_premium_features", "legacy_vs_current_features", "upgrade_benefits", "feature_migration"],
                "Enhanced_Export": ["dwg_export", "pdf_export", "image_export", "3d_formats", "export_quality", "batch_export", "format_options"],
                "Cloud_Storage": ["unlimited_storage", "file_organization", "cloud_management", "storage_optimization", "backup_features", "version_history"],
                "Commercial_Use": ["licensing_compliance", "commercial_projects", "client_sharing", "professional_workflows", "business_features", "usage_rights"],
                "Collaboration_Features": ["team_sharing", "project_management", "client_access", "shared_folders", "collaborative_workflows", "review_processes", "client_review_access", "comment_tracking"]
            },
            "SketchUp_Studio_Professional_Suite": {
                "Studio_Suite": ["pro_desktop_access", "layout_integration", "style_builder_access", "advanced_importers", "premium_support", "enterprise_features"],
                "Rendering_Visualization_Tools": ["vray_access", "rendering_plugins", "style_builder", "photorealistic_export", "advanced_materials", "lighting_tools"],
                "Advanced_Import_Export": ["dwg_import", "3ds_import", "advanced_formats", "batch_processing", "format_conversion", "data_exchange", "cad_integration"],
                "Enterprise_Features": ["network_licensing", "deployment_tools", "admin_controls", "user_management", "security_features", "compliance_tools"],
                "Professional_Workflows": ["architectural_workflows", "engineering_integration", "construction_documentation", "design_development", "project_coordination"]
            },
            "LayOut_Documentation_Tool": {
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
        """Extract Q&A content from file with improved parsing"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return "", []
        
        # Extract title from filename or content
        title = file_path.stem.replace('_QnA', '').replace('video_', '')
        
        # Extract Q&A pairs with improved regex for numbered format
        # Pattern for numbered questions: "1. Question text\nAnswer:\nAnswer text"
        qa_pattern = r'(\d+)\.\s*(.+?)\nAnswer:\s*\n(.+?)(?=\n\n\d+\.|\n\n---|\n\n## Q:|$)'
        qa_matches = re.findall(qa_pattern, content, re.DOTALL)
        
        qa_pairs = []
        for number, question, answer in qa_matches:
            question = question.strip()
            answer = answer.strip()
            if question and answer and len(answer) > 10:  # Minimum answer length
                qa_pairs.append((question, answer))
        
        # If no numbered format found, try the original ## Q: format
        if not qa_pairs:
            qa_pattern = r'## Q: (.+?)\n\n\*\*A:\*\* Answer:\n(.+?)(?=\n\n---|\n\n## Q:|$)'
            qa_matches = re.findall(qa_pattern, content, re.DOTALL)
            
            for question, answer in qa_matches:
                question = question.strip()
                answer = answer.strip()
                if question and answer and len(answer) > 10:  # Minimum answer length
                    qa_pairs.append((question, answer))
        
        return title, qa_pairs
    
    def analyze_question_intent(self, questions: List[str], title: str) -> str:
        """Analyze question intent with enhanced logic"""
        all_text = title + " " + " ".join(questions)
        all_text = all_text.lower()
        
        # Enhanced intent detection
        if any(word in all_text for word in ['how to', 'tutorial', 'guide', 'step by step']):
            return "how_to_guide"
        elif any(word in all_text for word in ['what is', 'explain', 'describe', 'define']):
            return "concept_explanation"
        elif any(word in all_text for word in ['error', 'problem', 'issue', 'fix', 'troubleshoot']):
            return "troubleshooting"
        elif any(word in all_text for word in ['new', 'update', '2025', '2024', 'feature']):
            return "feature_inquiry"
        elif any(word in all_text for word in ['performance', 'slow', 'lag', 'optimization']):
            return "performance_issue"
        elif any(word in all_text for word in ['install', 'setup', 'download', 'activate']):
            return "installation_issue"
        elif any(word in all_text for word in ['extension', 'plugin', 'warehouse']):
            return "extension_inquiry"
        else:
            return "general_inquiry"
    
    def determine_platform(self, title: str, qa_pairs: List[Tuple[str, str]]) -> str:
        """Determine platform with enhanced detection"""
        all_content = title + " " + " ".join([q + " " + a for q, a in qa_pairs])
        all_content = all_content.lower()
        
        # Enhanced platform detection
        if any(keyword in all_content for keyword in ['layout', 'viewport', 'documentation']):
            return "LayOut_Documentation_Tool"
        elif any(keyword in all_content for keyword in ['mobile viewer', 'viewer', 'mobile app']):
            return "SketchUp_Mobile_Viewer"
        elif any(keyword in all_content for keyword in ['mobile', 'ipad', 'touch', 'ar mode']):
            return "SketchUp_Go_iPad_Mobile"
        elif any(keyword in all_content for keyword in ['web', 'browser', 'online']):
            return "SketchUp_Web_Browser_based"
        elif any(keyword in all_content for keyword in ['shop', 'premium', 'commercial']):
            return "SketchUp_Shop_Web_Premium"
        elif any(keyword in all_content for keyword in ['studio', 'vray', 'rendering', 'professional suite']):
            return "SketchUp_Studio_Professional_Suite"
        else:
            return "SketchUp_Pro_Desktop"
    
    def enhanced_keyword_matching(self, content: str, pattern_name: str) -> bool:
        """Enhanced keyword matching with context requirements"""
        pattern = self.keyword_patterns.get(pattern_name)
        if not pattern:
            return False
        
        content_lower = content.lower()
        
        # Check for exclusion keywords first
        for exclusion in pattern.get("exclusion_keywords", []):
            if exclusion in content_lower:
                return False
        
        # Count primary keyword matches
        primary_matches = sum(1 for keyword in pattern["primary_keywords"] 
                            if keyword in content_lower)
        
        # Check context requirements
        if pattern.get("require_context", False):
            context_matches = sum(1 for keyword in pattern["context_keywords"] 
                                if keyword in content_lower)
            return (primary_matches >= pattern["min_matches"] and 
                   context_matches >= 1)
        else:
            return primary_matches >= pattern["min_matches"]
    
    def validate_categorization(self, category: str, subcategory: str, content: str) -> bool:
        """Validate that content matches the assigned category"""
        validation_keywords = self.validation_rules.get(category, [])
        if not validation_keywords:
            return True
        
        content_lower = content.lower()
        matches = sum(1 for keyword in validation_keywords if keyword in content_lower)
        return matches >= 2  # At least 2 validation keywords should be present
    
    def needs_manual_review(self, content: str, category: str, confidence: float) -> bool:
        """Determine if content needs manual review"""
        content_lower = content.lower()
        
        # Check for review triggers
        for trigger in self.review_triggers:
            if trigger in content_lower:
                return True
        
        # Low confidence categorization
        if confidence < 0.6:
            return True
        
        # Mixed content indicators
        mixed_indicators = ['and', 'also', 'both', 'multiple', 'various']
        if sum(1 for indicator in mixed_indicators if indicator in content_lower) >= 3:
            return True
        
        return False
    
    def determine_category_subcategory_enhanced(self, platform: str, question_intent: str, 
                                              title: str, qa_pairs: List[Tuple[str, str]]) -> Tuple[str, str, float]:
        """Enhanced category determination with confidence scoring using proper taxonomy subcategories"""
        
        all_content = title + " " + " ".join([q + " " + a for q, a in qa_pairs])
        all_content = all_content.lower()
        
        # Get the taxonomy for the platform
        platform_key = platform.replace(" ", "_").replace("(", "").replace(")", "")
        taxonomy = self.taxonomy.get(platform_key, {})
        
        # Priority order: Most specific to least specific
        categorization_attempts = []
        
        # 1. Check for specific tools first (highest priority)
        # Check for rotate tool specifically
        if any(keyword in all_content for keyword in [
            'rotate tool', 'rotation', 'rotating', 'rotate around', 'center handles',
            'rotation grips', 'rotation points', '2025 improvements'
        ]):
            category = "Drawing_Modeling_Tools"
            subcategory = "rotate_tool"
            confidence = 0.9
            categorization_attempts.append((category, subcategory, confidence))
        
        # Check for move tool specifically
        if any(keyword in all_content for keyword in [
            'move tool', 'moving objects', 'translation', 'move tool operations'
        ]):
            category = "Drawing_Modeling_Tools"
            subcategory = "move_tool"
            confidence = 0.9
            categorization_attempts.append((category, subcategory, confidence))
        
        # Check for text tool specifically
        if any(keyword in all_content for keyword in [
            'text tool', '3d text', 'text annotation', 'leader'
        ]):
            category = "Drawing_Modeling_Tools"
            subcategory = "text_tool"
            confidence = 0.9
            categorization_attempts.append((category, subcategory, confidence))
        
        # Check for line tool specifically
        if any(keyword in all_content for keyword in [
            'line tool', 'line drawing', 'straight line', 'line creation'
        ]):
            category = "Drawing_Modeling_Tools"
            subcategory = "line_tool"
            confidence = 0.9
            categorization_attempts.append((category, subcategory, confidence))
        
        # Check for rectangle tool specifically
        if any(keyword in all_content for keyword in [
            'rectangle tool', 'rectangle', 'rectangular shape'
        ]):
            category = "Drawing_Modeling_Tools"
            subcategory = "rectangle_tool"
            confidence = 0.9
            categorization_attempts.append((category, subcategory, confidence))
        
        # Check for circle tool specifically
        if any(keyword in all_content for keyword in [
            'circle tool', 'circle', 'circular shape'
        ]):
            category = "Drawing_Modeling_Tools"
            subcategory = "circle_tool"
            confidence = 0.9
            categorization_attempts.append((category, subcategory, confidence))
        
        # Check for push pull tool specifically
        if any(keyword in all_content for keyword in [
            'push pull', 'push/pull', 'extrude', 'extrusion'
        ]):
            category = "Drawing_Modeling_Tools"
            subcategory = "push_pull_tool"
            confidence = 0.9
            categorization_attempts.append((category, subcategory, confidence))
        
        # Check for offset tool specifically
        if any(keyword in all_content for keyword in [
            'offset tool', 'offset', 'parallel lines'
        ]):
            category = "Drawing_Modeling_Tools"
            subcategory = "offset_tool"
            confidence = 0.9
            categorization_attempts.append((category, subcategory, confidence))
        
        # Check for scale tool specifically
        if any(keyword in all_content for keyword in [
            'scale tool', 'scaling', 'resize', 'scale objects'
        ]):
            category = "Drawing_Modeling_Tools"
            subcategory = "scale_tool"
            confidence = 0.9
            categorization_attempts.append((category, subcategory, confidence))
        
        # Check for tape measure specifically
        if any(keyword in all_content for keyword in [
            'tape measure', 'measure tool', 'measurement'
        ]):
            category = "Drawing_Modeling_Tools"
            subcategory = "tape_measure"
            confidence = 0.9
            categorization_attempts.append((category, subcategory, confidence))
        
        # Check for dimension tool specifically
        if any(keyword in all_content for keyword in [
            'dimension tool', 'dimension', 'dimensioning'
        ]):
            category = "Drawing_Modeling_Tools"
            subcategory = "dimension_tool"
            confidence = 0.9
            categorization_attempts.append((category, subcategory, confidence))
        
        # Check for section plane specifically
        if any(keyword in all_content for keyword in [
            'section plane', 'section cut', 'section view'
        ]):
            category = "Drawing_Modeling_Tools"
            subcategory = "section_plane"
            confidence = 0.9
            categorization_attempts.append((category, subcategory, confidence))
        
        # 2. Check for LayOut integration
        if self.enhanced_keyword_matching(all_content, "layout_integration"):
            category = "LayOut_Integration"
            subcategory = "layout_references"
            confidence = 0.85
            categorization_attempts.append((category, subcategory, confidence))
        
        # 3. Check for materials and textures
        if self.enhanced_keyword_matching(all_content, "materials_textures"):
            category = "Materials_Textures"
            subcategory = "applying_materials"
            confidence = 0.8
            categorization_attempts.append((category, subcategory, confidence))
        
        # 4. Check for import/export
        if self.enhanced_keyword_matching(all_content, "import_export"):
            category = "Import_Export"
            subcategory = "cad_import"
            confidence = 0.8
            categorization_attempts.append((category, subcategory, confidence))
        
        # 5. Check for extensions (with proper subcategories)
        if self.enhanced_keyword_matching(all_content, "extensions_plugins"):
            category = "Extensions_Plugins"
            # Check for specific extension subcategories
            if any(keyword in all_content for keyword in ['install', 'installation']):
                subcategory = "extension_installation"
            elif any(keyword in all_content for keyword in ['manage', 'management']):
                subcategory = "extension_management"
            elif any(keyword in all_content for keyword in ['ruby', 'scripting']):
                subcategory = "ruby_scripting"
            elif any(keyword in all_content for keyword in ['api', 'development']):
                subcategory = "api_development"
            elif any(keyword in all_content for keyword in ['update', 'updates']):
                subcategory = "extension_updates"
            elif any(keyword in all_content for keyword in ['custom', 'tools']):
                subcategory = "custom_tools"
            elif any(keyword in all_content for keyword in ['compatibility']):
                subcategory = "extension_compatibility"
            elif any(keyword in all_content for keyword in ['review', 'inspection']):
                subcategory = "extension_review"
            elif any(keyword in all_content for keyword in ['discovery', 'find', 'warehouse']):
                subcategory = "extension_discovery"
            else:
                subcategory = "extension_installation"  # default
            confidence = 0.75
            categorization_attempts.append((category, subcategory, confidence))
        
        # 6. Check other categories with proper subcategories
        if any(keyword in all_content for keyword in ['solid tool', 'union', 'boolean']):
            categorization_attempts.append(("Geometry_Modeling", "boolean_operations", 0.7))
        
        if any(keyword in all_content for keyword in ['component', 'group']):
            categorization_attempts.append(("Groups_Components", "component_creation", 0.7))
        
        if any(keyword in all_content for keyword in ['scene', 'animation']):
            categorization_attempts.append(("Scenes_Animation", "scene_creation", 0.7))
        
        if any(keyword in all_content for keyword in ['2025', '2024', 'new features']):
            categorization_attempts.append(("Updates_Versioning", "new_feature_use", 0.7))
        
        if any(keyword in all_content for keyword in ['performance', 'optimization']):
            categorization_attempts.append(("Performance_Stability", "model_optimization", 0.7))
        
        # 7. Check for Getting Started & Basics with proper subcategories
        if question_intent == "beginner_guidance":
            if any(keyword in all_content for keyword in ['interface', 'overview']):
                subcategory = "interface_overview"
            elif any(keyword in all_content for keyword in ['workspace', 'setup']):
                subcategory = "workspace_setup"
            elif any(keyword in all_content for keyword in ['navigation', 'orbit', 'pan', 'zoom']):
                subcategory = "basic_navigation"
            elif any(keyword in all_content for keyword in ['tool', 'introduction']):
                subcategory = "tool_introduction"
            elif any(keyword in all_content for keyword in ['menu', 'navigation']):
                subcategory = "menu_navigation"
            elif any(keyword in all_content for keyword in ['panel', 'management']):
                subcategory = "panel_management"
            elif any(keyword in all_content for keyword in ['preference', 'settings']):
                subcategory = "preference_settings"
            elif any(keyword in all_content for keyword in ['template', 'selection']):
                subcategory = "template_selection"
            elif any(keyword in all_content for keyword in ['units', 'setup']):
                subcategory = "units_setup"
            else:
                subcategory = "basic_navigation"  # default for beginner guidance
            categorization_attempts.append(("Getting_Started_Basics", subcategory, 0.5))
        else:
            # Default to a specific tool subcategory instead of generic
            categorization_attempts.append(("Drawing_Modeling_Tools", "push_pull_tool", 0.5))
        
        # Return the highest confidence categorization
        if categorization_attempts:
            best_categorization = max(categorization_attempts, key=lambda x: x[2])
            return best_categorization
        
        # Fallback with proper subcategory
        return "Getting_Started_Basics", "interface_overview", 0.3
    
    def categorize_single_qa_file_enhanced(self, qa_file_path: Path) -> bool:
        """Enhanced categorization with validation and review capabilities"""
        
        # Skip empty or problematic files
        try:
            file_size = qa_file_path.stat().st_size
            if file_size < 100:
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
        category, subcategory, confidence = self.determine_category_subcategory_enhanced(
            platform, question_intent, title, qa_pairs
        )
        
        # Validate categorization
        all_content = title + " " + " ".join([q + " " + a for q, a in qa_pairs])
        is_valid = self.validate_categorization(category, subcategory, all_content)
        
        # Check if manual review is needed
        needs_review = self.needs_manual_review(all_content, category, confidence)
        
        if needs_review or not is_valid:
            # Move to review directory
            review_path = self.review_dir / f"{qa_file_path.stem}_REVIEW_NEEDED.md"
            review_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create review file with analysis
            review_content = f"""# Manual Review Required

**File:** {qa_file_path.name}
**Original Path:** {qa_file_path}

## Analysis Results
- **Platform:** {platform}
- **Question Intent:** {question_intent}
- **Proposed Category:** {category}
- **Proposed Subcategory:** {subcategory}
- **Confidence:** {confidence:.2f}
- **Validation Passed:** {is_valid}
- **Review Reason:** {'Low confidence' if confidence < 0.6 else 'Validation failed' if not is_valid else 'Mixed content detected'}

## Content Preview
{all_content[:500]}...

## Recommended Action
Please review this content and manually assign the correct category/subcategory.
"""
            
            with open(review_path, 'w', encoding='utf-8') as f:
                f.write(review_content)
            
            print(f"🔍 {qa_file_path.name} -> REVIEW NEEDED")
            print(f"   📊 Confidence: {confidence:.2f}")
            print(f"   ✅ Valid: {is_valid}")
            print()
            return True
        
        # Map platform names to existing directory structure
        platform_mapping = {
            "SketchUp_Pro_Desktop": "SketchUp_Pro_(Desktop)",
            "LayOut_Documentation_Tool": "LayOut_(Documentation_Tool)",
            "SketchUp_Go_iPad_Mobile": "SketchUp_Go_(iPad/Mobile)",
            "SketchUp_Studio_Professional_Suite": "SketchUp_Studio_Professional_Suite",
            "SketchUp_Web_Browser_based": "SketchUp_Web_Browser_based",
            "SketchUp_Shop_Web_Premium": "SketchUp_Shop_(Web_Premium)",
            "SketchUp_Mobile_Viewer": "SketchUp_Mobile_Viewer"
        }
        
        # Use existing directory structure
        actual_platform = platform_mapping.get(platform, platform)
        target_path = self.categorized_dir / actual_platform / category / subcategory / qa_file_path.name
        
        # Only create directories if they don't exist
        if not target_path.parent.exists():
            target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Move file to correct location only if it's different
        if qa_file_path != target_path:
            shutil.move(str(qa_file_path), str(target_path))
            print(f"📁 {qa_file_path.name}")
            print(f"   📊 Q&A Pairs: {len(qa_pairs)}")
            print(f"   🎯 Intent: {question_intent}")
            print(f"   📂 {platform}/{category}/{subcategory}")
            print(f"   🎯 Confidence: {confidence:.2f}")
            print()
            return True
        else:
            return False
    
    def categorize_all_qa_files_enhanced(self):
        """Enhanced categorization of all Q&A files"""
        
        print("🧠 Starting ENHANCED Q&A content analysis and categorization...")
        print("🔍 Using refined keyword matching with context requirements")
        print("✅ Implementing content validation and confidence scoring")
        print("🔍 Adding manual review capabilities for uncertain cases")
        print()
        
        # Create directories
        self.review_dir.mkdir(parents=True, exist_ok=True)
        
        # Map platform names to existing directory structure
        platform_mapping = {
            "SketchUp_Pro_Desktop": "SketchUp_Pro_(Desktop)",
            "LayOut_Documentation_Tool": "LayOut_(Documentation_Tool)",
            "SketchUp_Go_iPad_Mobile": "SketchUp_Go_(iPad/Mobile)",
            "SketchUp_Studio_Professional_Suite": "SketchUp_Studio_Professional_Suite",
            "SketchUp_Web_Browser_based": "SketchUp_Web_Browser_based",
            "SketchUp_Shop_Web_Premium": "SketchUp_Shop_(Web_Premium)",
            "SketchUp_Mobile_Viewer": "SketchUp_Mobile_Viewer"
        }
        
        # Create taxonomy structure using existing directories
        for platform, categories in self.taxonomy.items():
            actual_platform = platform_mapping.get(platform, platform)
            for category, subcategories in categories.items():
                for subcategory in subcategories:
                    dir_path = self.categorized_dir / actual_platform / category / subcategory
                    if not dir_path.exists():
                        dir_path.mkdir(parents=True, exist_ok=True)
        
        # Find all Q&A files
        all_qa_files = []
        for playlist_dir in self.base_output_dir.glob("PL-*"):
            if playlist_dir.is_dir():
                all_qa_files.extend(playlist_dir.glob("*_QnA.md"))
        
        # Also check categorized directory for re-categorization
        for qa_file in self.categorized_dir.rglob("categorized_QnAs.md"):
            all_qa_files.append(qa_file)
        
        print(f"📁 Found {len(all_qa_files)} Q&A files to process")
        print()
        
        # Process files
        processed = 0
        reviewed = 0
        
        for qa_file in all_qa_files:
            if self.categorize_single_qa_file_enhanced(qa_file):
                processed += 1
                if "REVIEW_NEEDED" in str(qa_file):
                    reviewed += 1
        
        print(f"✅ Processing complete!")
        print(f"📊 Files processed: {processed}")
        print(f"🔍 Files needing review: {reviewed}")
        print(f"📁 Review files location: {self.review_dir}")
        
        # Generate enhanced report
        self.generate_enhanced_report()
    
    def generate_enhanced_report(self):
        """Generate enhanced categorization report"""
        report_path = self.base_output_dir / "enhanced_categorization_report.md"
        
        # Count files in each category
        category_counts = {}
        review_count = len(list(self.review_dir.glob("*_REVIEW_NEEDED.md")))
        
        for qa_file in self.categorized_dir.rglob("*_QnA.md"):
            parts = qa_file.parts
            if len(parts) >= 4:
                platform = parts[-4]
                category = parts[-3]
                subcategory = parts[-2]
                
                key = f"{platform}/{category}/{subcategory}"
                category_counts[key] = category_counts.get(key, 0) + 1
        
        # Generate report
        report_content = f"""# Enhanced Q&A Categorization Report

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary

This report summarizes the ENHANCED categorization of Q&A pairs with improved accuracy and validation.

### Processing Results

- **Total Q&A files processed**: {sum(category_counts.values())}
- **Files needing manual review**: {review_count}
- **Successfully categorized**: {sum(category_counts.values()) - review_count}
- **Success rate**: {((sum(category_counts.values()) - review_count) / max(sum(category_counts.values()), 1) * 100):.1f}%

## Category Distribution

| Platform | Category | Subcategory | Count |
|----------|----------|-------------|-------|
"""
        
        for key, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            platform, category, subcategory = key.split('/', 2)
            report_content += f"| {platform} | {category} | {subcategory} | {count} |\n"
        
        report_content += f"""
## Quality Improvements

✅ **Enhanced Keyword Matching**: More specific patterns with context requirements
✅ **Content Validation**: Automatic validation of categorization accuracy
✅ **Confidence Scoring**: Confidence levels for each categorization
✅ **Manual Review**: Automatic flagging of uncertain cases
✅ **Priority Ordering**: More specific categories checked first

## Review Process

Files requiring manual review are located in: `{self.review_dir}`

Each review file contains:
- Original file location
- Analysis results and confidence scores
- Content preview
- Recommended action

## Next Steps

1. Review files in the review directory
2. Manually categorize uncertain cases
3. Validate categorization accuracy
4. Update taxonomy if needed

"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"📄 Enhanced report generated: {report_path}")

def main():
    """Main function to run enhanced categorization"""
    categorizer = EnhancedQACategorizer()
    categorizer.categorize_all_qa_files_enhanced()

if __name__ == "__main__":
    main() 