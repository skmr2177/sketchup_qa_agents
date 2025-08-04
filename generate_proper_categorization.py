#!/usr/bin/env python3
"""
Generate Proper Categorization following exact sample_category.md structure
7 Product files, each with Question Intent Categories and Subcategories
"""

import json
import re
from pathlib import Path
from typing import Dict, List
from collections import defaultdict

class ProperCategorizer:
    """Generate categorization following exact sample_category.md structure"""
    
    def __init__(self):
        self.output_dir = Path("output")
        self.proper_dir = self.output_dir / "proper_categorization"
        self.stats = defaultdict(int)
        
        # Core Question Types (from sample_category.md lines 3-28)
        self.core_question_types = [
            'bug_report', 'crash_issue', 'how_to_guide', 'troubleshooting', 
            'feature_inquiry', 'performance_issue', 'compatibility_issue', 
            'installation_issue', 'export_issue', 'import_issue', 'sync_issue',
            'account_issue', 'workflow_optimization', 'advanced_technique', 
            'beginner_guidance', 'configuration_help', 'integration_help',
            'limitation_explanation', 'best_practices', 'concept_explanation',
            'ui_feedback', 'update_inquiry', 'data_loss', 'licensing_issues',
            'recommendation_help'
        ]
        
        # 7 Products from sample_category.md (Tables 1-7)
        self.products = {
            'sketchup_pro_desktop': {
                'name': 'SketchUp Pro (Desktop)',
                'table_number': 1,
                'categories': {
                    'installation_setup': {
                        'name': 'Installation & Setup',
                        'subcategories': ['initial_installation', 'license_activation', 'subscription_management', 'system_requirements', 'network_configuration', 'trimble_id_setup', 'offline_installation', 'pro_features_activation']
                    },
                    'updates_versioning': {
                        'name': 'Updates & Versioning',
                        'subcategories': ['changelog_review', 'version_migration', 'feature_deprecation', 'new_feature_use', 'backward_compatibility', 'update_installation']
                    },
                    'getting_started_basics': {
                        'name': 'Getting Started & Basics',
                        'subcategories': ['interface_overview', 'workspace_setup', 'basic_navigation', 'tool_introduction', 'menu_navigation', 'panel_management', 'preference_settings', 'template_selection', 'units_setup']
                    },
                    'drawing_modeling_tools': {
                        'name': 'Drawing & Modeling Tools',
                        'subcategories': ['line_tool', 'rectangle_tool', 'circle_tool', 'push_pull_tool', 'follow_me_tool', 'offset_tool', 'move_tool', 'rotate_tool', 'scale_tool', 'tape_measure', 'protractor', 'text_tool', 'dimension_tool', 'section_plane']
                    },
                    'selection_navigation': {
                        'name': 'Selection & Navigation',
                        'subcategories': ['selection_methods', 'multi_selection', 'orbit_navigation', 'pan_navigation', 'zoom_controls', 'walk_through', 'camera_positioning', 'view_controls', 'standard_views']
                    },
                    'geometry_modeling': {
                        'name': 'Geometry & Modeling',
                        'subcategories': ['edges_faces', 'groups_components', 'solid_modeling', 'boolean_operations', 'intersect_operations', 'geometry_repair', 'face_orientation', 'smoothing_softening']
                    },
                    'groups_components': {
                        'name': 'Groups & Components',
                        'subcategories': ['creating_groups', 'editing_groups', 'component_creation', 'dynamic_components', 'component_browser', 'nested_components', 'component_outliner', 'unique_components', 'component_reload', 'component_sync']
                    },
                    'materials_textures': {
                        'name': 'Materials & Textures',
                        'subcategories': ['material_browser', 'applying_materials', 'creating_materials', 'texture_positioning', 'material_sampling', 'transparency_settings', 'custom_textures', 'photo_textures']
                    },
                    'layers_tags': {
                        'name': 'Layers & Tags',
                        'subcategories': ['tag_management', 'visibility_control', 'layer_organization', 'tag_assignment', 'scene_layers', 'layer_colors', 'layer_export', 'tag_migration']
                    },
                    'scenes_animation': {
                        'name': 'Scenes & Animation',
                        'subcategories': ['scene_creation', 'scene_management', 'scene_transitions', 'animation_settings', 'camera_scenes', 'walkthrough_animation', 'scene_export']
                    },
                    'styles_display': {
                        'name': 'Styles & Display',
                        'subcategories': ['edge_styles', 'face_styles', 'background_settings', 'watermarks', 'style_creation', 'style_editing', 'sketch_styles', 'photorealistic_styles']
                    },
                    'shadows_lighting': {
                        'name': 'Shadows & Lighting',
                        'subcategories': ['shadow_settings', 'sun_positioning', 'geographic_location', 'time_date_settings', 'shadow_accuracy', 'interior_lighting', 'shadow_analysis']
                    },
                    'import_export': {
                        'name': 'Import & Export',
                        'subcategories': ['cad_import', 'image_import', '3d_import', '2d_export', '3d_export', 'pdf_export', 'image_export', 'animation_export', 'file_optimization']
                    },
                    'extensions_plugins': {
                        'name': 'Extensions & Plugins',
                        'subcategories': ['extension_installation', 'extension_management', 'ruby_scripting', 'api_development', 'extension_updates', 'custom_tools', 'extension_compatibility', 'extension_review', 'extension_discovery']
                    },
                    'layout_integration': {
                        'name': 'LayOut Integration',
                        'subcategories': ['layout_references', 'model_updates', 'viewport_management', 'layout_sync', 'layout_export', 'layout_templates']
                    },
                    'performance_stability': {
                        'name': 'Performance & Stability',
                        'subcategories': ['model_optimization', 'file_size_reduction', 'graphics_settings', 'large_model_handling', 'performance_monitoring', 'render_optimization', 'memory_management']
                    },
                    'data_management_recovery': {
                        'name': 'Data Management & Recovery',
                        'subcategories': ['file_backups', 'auto_recovery', 'data_corruption', 'version_control', 'file_organization', 'cloud_sync']
                    },
                    'troubleshooting_system_issues': {
                        'name': 'Troubleshooting & System Issues',
                        'subcategories': ['crash_issues', 'startup_problems', 'display_issues', 'file_corruption', 'licensing_issues', 'graphics_problems', 'memory_issues', 'tool_failures']
                    }
                }
            },
            'sketchup_web': {
                'name': 'SketchUp Web (Browser-based)',
                'table_number': 2,
                'categories': {
                    'account_access': {
                        'name': 'Account & Access',
                        'subcategories': ['trimble_id_login', 'subscription_access', 'web_browser_compatibility', 'account_management', 'offline_limitations', 'sync_issues']
                    },
                    'updates_releases': {
                        'name': 'Updates & Releases',
                        'subcategories': ['web_feature_rollout', 'mobile_feature_gaps', 'browser_updates_impact', 'feature_parity', 'rollback_issues']
                    },
                    'web_interface': {
                        'name': 'Web Interface',
                        'subcategories': ['browser_interface', 'toolbar_layout', 'panel_management', 'touch_interface', 'keyboard_shortcuts', 'web_navigation', 'responsive_design']
                    },
                    'basic_drawing_tools': {
                        'name': 'Basic Drawing Tools',
                        'subcategories': ['line_tool', 'rectangle_tool', 'circle_tool', 'push_pull_tool', 'move_tool', 'rotate_tool', 'scale_tool', 'eraser_tool', 'paint_bucket']
                    },
                    'web_specific_features': {
                        'name': 'Web-Specific Features',
                        'subcategories': ['auto_save', 'cloud_storage', 'web_performance', 'browser_limitations', 'feature_differences', 'mobile_browser_support', 'version_differences', 'cloud_processing_limits']
                    },
                    'file_management': {
                        'name': 'File Management',
                        'subcategories': ['cloud_save', 'file_sharing', 'export_limitations', 'import_restrictions', 'file_formats', 'download_options', 'storage_limits']
                    },
                    'collaboration': {
                        'name': 'Collaboration',
                        'subcategories': ['sharing_models', 'collaborative_editing', 'real_time_sync', 'access_permissions', 'shared_projects', 'team_features']
                    },
                    'performance_stability': {
                        'name': 'Performance & Stability',
                        'subcategories': ['browser_performance', 'loading_issues', 'lag_problems', 'memory_limitations', 'graphics_performance', 'crash_recovery']
                    },
                    'web_limitations': {
                        'name': 'Web Limitations',
                        'subcategories': ['missing_features', 'export_restrictions', 'extension_limitations', 'advanced_tool_access', 'professional_features']
                    }
                }
            },
            'sketchup_go': {
                'name': 'SketchUp Go (iPad/Mobile)',
                'table_number': 3,
                'categories': {
                    'mobile_setup': {
                        'name': 'Mobile Setup',
                        'subcategories': ['app_installation', 'account_login', 'subscription_activation', 'device_compatibility', 'ios_requirements', 'storage_management']
                    },
                    'app_updates_versions': {
                        'name': 'App Updates & Versions',
                        'subcategories': ['app_store_versioning', 'feature_delays', 'ios_updates', 'version_compatibility', 'update_failures']
                    },
                    'touch_interface': {
                        'name': 'Touch Interface',
                        'subcategories': ['touch_controls', 'gesture_navigation', 'multi_touch', 'apple_pencil_support', 'touch_precision', 'interface_adaptation', 'gesture_conflicts', 'rotation_lock']
                    },
                    'mobile_drawing': {
                        'name': 'Mobile Drawing',
                        'subcategories': ['touch_drawing', 'precision_modeling', 'mobile_tools', 'simplified_interface', 'tool_adaptation', 'mobile_workflow']
                    },
                    'ar_features': {
                        'name': 'AR Features',
                        'subcategories': ['ar_mode', 'object_placement', 'ar_measurement', 'real_world_scale', 'ar_viewing', 'environmental_tracking']
                    },
                    'performance_stability': {
                        'name': 'Performance & Stability',
                        'subcategories': ['app_performance', 'device_heating', 'battery_usage', 'memory_management', 'crash_issues', 'app_optimization']
                    },
                    'cloud_sync_data': {
                        'name': 'Cloud Sync & Data',
                        'subcategories': ['model_sync', 'cross_device_access', 'cloud_storage', 'sync_conflicts', 'offline_access', 'backup_recovery']
                    },
                    'mobile_limitations': {
                        'name': 'Mobile Limitations',
                        'subcategories': ['feature_restrictions', 'export_limitations', 'complex_modeling_limits', 'professional_features', 'desktop_comparison']
                    }
                }
            },
            'sketchup_shop': {
                'name': 'SketchUp Shop (Web Premium)',
                'table_number': 4,
                'categories': {
                    'premium_features': {
                        'name': 'Premium Features',
                        'subcategories': ['advanced_export', 'unlimited_cloud_storage', 'premium_templates', 'enhanced_sharing', 'priority_support', 'commercial_use']
                    },
                    'version_differences': {
                        'name': 'Version Differences',
                        'subcategories': ['free_vs_premium_features', 'legacy_vs_current_features', 'upgrade_benefits', 'feature_migration']
                    },
                    'enhanced_export': {
                        'name': 'Enhanced Export',
                        'subcategories': ['dwg_export', 'pdf_export', 'image_export', '3d_formats', 'export_quality', 'batch_export', 'format_options']
                    },
                    'cloud_storage': {
                        'name': 'Cloud Storage',
                        'subcategories': ['unlimited_storage', 'file_organization', 'cloud_management', 'storage_optimization', 'backup_features', 'version_history']
                    },
                    'commercial_use': {
                        'name': 'Commercial Use',
                        'subcategories': ['licensing_compliance', 'commercial_projects', 'client_sharing', 'professional_workflows', 'business_features', 'usage_rights']
                    },
                    'collaboration_features': {
                        'name': 'Collaboration Features',
                        'subcategories': ['team_sharing', 'project_management', 'client_access', 'shared_folders', 'collaborative_workflows', 'review_processes', 'client_review_access', 'comment_tracking']
                    }
                }
            },
            'sketchup_studio': {
                'name': 'SketchUp Studio (Professional Suite)',
                'table_number': 5,
                'categories': {
                    'studio_suite': {
                        'name': 'Studio Suite',
                        'subcategories': ['pro_desktop_access', 'layout_integration', 'style_builder_access', 'advanced_importers', 'premium_support', 'enterprise_features']
                    },
                    'rendering_visualization_tools': {
                        'name': 'Rendering & Visualization Tools',
                        'subcategories': ['vray_access', 'rendering_plugins', 'style_builder', 'photorealistic_export', 'advanced_materials', 'lighting_tools']
                    },
                    'advanced_import_export': {
                        'name': 'Advanced Import/Export',
                        'subcategories': ['dwg_import', '3ds_import', 'advanced_formats', 'batch_processing', 'format_conversion', 'data_exchange', 'cad_integration']
                    },
                    'enterprise_features': {
                        'name': 'Enterprise Features',
                        'subcategories': ['network_licensing', 'deployment_tools', 'admin_controls', 'user_management', 'security_features', 'compliance_tools']
                    },
                    'professional_workflows': {
                        'name': 'Professional Workflows',
                        'subcategories': ['architectural_workflows', 'engineering_integration', 'construction_documentation', 'design_development', 'project_coordination']
                    }
                }
            },
            'layout': {
                'name': 'LayOut (Documentation Tool)',
                'table_number': 6,
                'categories': {
                    'layout_basics': {
                        'name': 'Layout Basics',
                        'subcategories': ['interface_overview', 'page_setup', 'document_creation', 'workspace_organization', 'tool_introduction']
                    },
                    'template_management': {
                        'name': 'Template Management',
                        'subcategories': ['loading_templates', 'custom_template_creation', 'shared_templates', 'template_organization', 'template_sharing']
                    },
                    'drawing_annotation': {
                        'name': 'Drawing & Annotation',
                        'subcategories': ['line_drawing', 'shape_creation', 'text_tools', 'dimensioning', 'labeling', 'leader_lines', 'callouts', 'markup_tools']
                    },
                    'sketchup_integration': {
                        'name': 'SketchUp Integration',
                        'subcategories': ['model_references', 'viewport_creation', 'scene_management', 'model_updates', 'reference_linking', 'view_synchronization']
                    },
                    'layout_formatting': {
                        'name': 'Layout & Formatting',
                        'subcategories': ['page_layout', 'master_pages', 'layer_management', 'style_formatting', 'grid_settings', 'alignment_tools', 'object_arrangement']
                    },
                    'export_printing': {
                        'name': 'Export & Printing',
                        'subcategories': ['pdf_export', 'image_export', 'printing_setup', 'print_quality', 'batch_export', 'format_options', 'output_optimization']
                    },
                    'advanced_features': {
                        'name': 'Advanced Features',
                        'subcategories': ['auto_text', 'scrapbooks', 'shared_layers', 'collaborative_editing', 'custom_tools']
                    },
                    'performance_stability': {
                        'name': 'Performance & Stability',
                        'subcategories': ['layout_performance', 'large_document_handling', 'reference_issues', 'crash_problems', 'file_corruption', 'memory_issues', 'render_delays', 'linked_model_refresh']
                    }
                }
            },
            'sketchup_mobile_viewer': {
                'name': 'SketchUp Mobile Viewer (Free Mobile)',
                'table_number': 7,
                'categories': {
                    'viewer_features': {
                        'name': 'Viewer Features',
                        'subcategories': ['model_viewing', 'navigation_controls', 'measurement_tools', 'section_viewing', 'scene_navigation', 'model_information']
                    },
                    'cross_platform_support': {
                        'name': 'Cross-Platform Support',
                        'subcategories': ['android_support', 'ios_behavior_differences', 'version_sync', 'platform_compatibility', 'device_variations']
                    },
                    'file_access': {
                        'name': 'File Access',
                        'subcategories': ['model_loading', 'cloud_access', 'local_files', 'sharing_access', 'file_formats', 'download_issues']
                    },
                    'mobile_interface': {
                        'name': 'Mobile Interface',
                        'subcategories': ['touch_navigation', 'gesture_controls', 'interface_layout', 'viewing_modes', 'display_options', 'screen_adaptation']
                    },
                    'viewing_limitations': {
                        'name': 'Viewing Limitations',
                        'subcategories': ['viewer_restrictions', 'editing_limitations', 'export_restrictions', 'feature_comparison', 'upgrade_options']
                    }
                }
            }
        }
    
    def generate_proper_categorization(self):
        """Generate proper categorization following sample_category.md structure"""
        
        print("🚀 Generating Proper Categorization following sample_category.md")
        print("📋 Structure: 7 Product Files + Core Question Types")
        print("=" * 80)
        
        # Create directory structure
        self.proper_dir.mkdir(exist_ok=True)
        
        # Generate Core Question Types file
        self._generate_core_question_types()
        
        # Generate 7 Product category files
        for product_id, product_info in self.products.items():
            self._generate_product_category_file(product_id, product_info)
        
        # Generate main index
        self._generate_main_index()
        
        print(f"\n✅ Generated proper categorization in: {self.proper_dir}")
    
    def _generate_core_question_types(self):
        """Generate core question types file"""
        
        file_path = self.proper_dir / "core_question_types.md"
        
        content = f"""# Core Question Types

Based on sample_category.md - Complete Question Type Categories

## Overview

These are the 25 core question types that can be applied to any SketchUp product category.

## Core Question Types

"""
        
        question_type_descriptions = {
            'bug_report': 'Software defects and unexpected behavior',
            'crash_issue': 'Application crashes and stability problems',
            'how_to_guide': 'Step-by-step instructions and tutorials',
            'troubleshooting': 'Problem diagnosis and resolution',
            'feature_inquiry': 'Questions about capabilities and features',
            'performance_issue': 'Speed, lag, and optimization problems',
            'compatibility_issue': 'Hardware/software compatibility problems',
            'installation_issue': 'Setup and installation problems',
            'export_issue': 'File export failures and issues',
            'import_issue': 'File import failures and issues',
            'sync_issue': 'Cloud synchronization problems',
            'account_issue': 'Login, subscription, and account problems',
            'workflow_optimization': 'Efficiency and process improvement',
            'advanced_technique': 'Complex modeling and professional methods',
            'beginner_guidance': 'New user help and basic concepts',
            'configuration_help': 'Settings and customization assistance',
            'integration_help': 'Connecting with other software/services',
            'limitation_explanation': 'Understanding software restrictions',
            'best_practices': 'Recommended approaches and methods',
            'concept_explanation': 'Understanding underlying principles',
            'ui_feedback': 'Feedback on UI/UX or design quirks',
            'update_inquiry': 'Questions about version changes, new features',
            'data_loss': 'Missing files, unsaved work, recoverability',
            'licensing_issues': 'Specific to licensing confusion/errors',
            'recommendation_help': 'Requests for tool suggestions, extensions, or workflows'
        }
        
        for i, question_type in enumerate(self.core_question_types, 1):
            description = question_type_descriptions.get(question_type, 'Question type description')
            content += f"{i}. **{question_type}** - {description}\n"
        
        content += f"""

## Usage

These question types should be used as a reference when categorizing Q&A pairs for any SketchUp product. Each Q&A pair should first be classified by question type, then by product-specific categories and subcategories.

## Example Classification

**Question:** "How do I create a component in SketchUp?"
- **Question Type:** `how_to_guide`
- **Product:** `sketchup_pro_desktop`
- **Category:** `groups_components`
- **Subcategory:** `component_creation`

"""
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Generated: core_question_types.md")
    
    def _generate_product_category_file(self, product_id: str, product_info: Dict):
        """Generate category file for each product"""
        
        file_path = self.proper_dir / f"{product_id}.md"
        
        content = f"""# {product_info['name']}

**Table {product_info['table_number']} from sample_category.md**

## Overview

This file contains the Question Intent Categories and their Subcategories for {product_info['name']}.

## Structure

**Core Question Types** → **Product** → **Question Intent Category** → **Question Intent Subcategory**

Each Q&A pair should be classified using:
1. One of the [Core Question Types](core_question_types.md)
2. This product: `{product_id}`
3. One of the categories below
4. One of the subcategories within that category

---

## Question Intent Categories & Subcategories

"""
        
        for category_id, category_info in product_info['categories'].items():
            content += f"### {category_info['name']}\n"
            content += f"**Category ID:** `{category_id}`\n\n"
            content += "**Subcategories:**\n"
            
            for subcategory in category_info['subcategories']:
                content += f"- `{subcategory}`\n"
            
            content += "\n"
        
        content += f"""---

## Usage Examples

### Example 1: Drawing Tool Question
**Question:** "How do I use the line tool in SketchUp?"
- **Question Type:** `how_to_guide` (from core types)
- **Product:** `{product_id}`
- **Category:** `drawing_modeling_tools`
- **Subcategory:** `line_tool`

### Example 2: Installation Problem
**Question:** "SketchUp won't start after installation"
- **Question Type:** `installation_issue` (from core types)
- **Product:** `{product_id}`
- **Category:** `installation_setup`
- **Subcategory:** `initial_installation`

### Example 3: Performance Question
**Question:** "My large model is running slowly"
- **Question Type:** `performance_issue` (from core types)
- **Product:** `{product_id}`
- **Category:** `performance_stability`
- **Subcategory:** `large_model_handling`

---

## Categories Summary

**Total Categories:** {len(product_info['categories'])}

"""
        
        for category_id, category_info in product_info['categories'].items():
            subcategory_count = len(category_info['subcategories'])
            content += f"- **{category_info['name']}**: {subcategory_count} subcategories\n"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Generated: {product_id}.md ({len(product_info['categories'])} categories)")
    
    def _generate_main_index(self):
        """Generate main index file"""
        
        file_path = self.proper_dir / "README.md"
        
        content = f"""# Proper SketchUp Q&A Categorization

Following the exact structure from `sample_category.md`

## Structure Overview

**4-Level Hierarchy:**
1. **Core Question Types** (25 types) - Universal across all products
2. **Products** (7 products) - SketchUp product/platform  
3. **Question Intent Categories** - Functional areas within each product
4. **Question Intent Subcategories** - Specific features/topics

## Files

### Core Question Types
- **[Core Question Types](core_question_types.md)** - 25 universal question types

### Product Categories (Tables 1-7 from sample_category.md)

"""
        
        for product_id, product_info in self.products.items():
            category_count = len(product_info['categories'])
            total_subcategories = sum(len(cat['subcategories']) for cat in product_info['categories'].values())
            
            content += f"- **[{product_info['name']}]({product_id}.md)** - Table {product_info['table_number']}\n"
            content += f"  - {category_count} categories, {total_subcategories} subcategories\n"
        
        content += f"""

## How to Use

1. **Start with Question Type** - Classify the Q&A by its type (how-to, troubleshooting, etc.)
2. **Select Product** - Choose which SketchUp product it relates to
3. **Pick Category** - Select the functional area within that product
4. **Choose Subcategory** - Pick the specific feature or topic

## Example Classification

**Q&A:** "How do I apply materials to a surface in SketchUp?"

**Classification:**
1. **Question Type:** `how_to_guide`
2. **Product:** `sketchup_pro_desktop`  
3. **Category:** `materials_textures`
4. **Subcategory:** `applying_materials`

## Statistics

- **Core Question Types:** {len(self.core_question_types)}
- **Products:** {len(self.products)}
- **Total Categories:** {sum(len(p['categories']) for p in self.products.values())}
- **Total Subcategories:** {sum(sum(len(cat['subcategories']) for cat in p['categories'].values()) for p in self.products.values())}

## Reference

This categorization system is based on the comprehensive taxonomy defined in `agents/sample_category.md`.

"""
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Generated: README.md (main index)")

def main():
    """Main function to generate proper categorization"""
    
    categorizer = ProperCategorizer()
    categorizer.generate_proper_categorization()
    
    print("\n" + "=" * 80)
    print("✅ Proper Categorization Generated!")
    print("=" * 80)
    print(f"\n📁 Location: {categorizer.proper_dir}")
    print(f"📋 Structure: Core Question Types + 7 Product Category Files")
    print(f"🎯 Following exact sample_category.md structure")

if __name__ == "__main__":
    main() 