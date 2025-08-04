#!/usr/bin/env python3
"""
Categorize Q&A with Comprehensive Taxonomy
Uses the comprehensive taxonomy based on actual Q&A analysis to categorize content
into the correct product, category, and subcategory folders.
"""

import os
import re
from pathlib import Path
from typing import Tuple, Dict, List
from collections import Counter

class TaxonomyCategorizer:
    def __init__(self, base_output_dir="output"):
        self.base_output_dir = Path(base_output_dir)
        self.taxonomy_dir = self.base_output_dir / "taxonomy_structure"
        
        # Load comprehensive taxonomy based on our analysis
        self.taxonomy = self._load_comprehensive_taxonomy()
        
        # Words to filter out from questions (instructor names, common non-technical words)
        self.filter_words = {
            "aaron", "instructor", "teacher", "presenter", "speaker", "demonstrator",
            "shows", "demonstrates", "explains", "describes", "mentions", "notes",
            "emphasizes", "concludes", "says", "states", "tells", "indicates",
            "this", "that", "these", "those", "here", "there", "now", "then",
            "very", "really", "quite", "rather", "somewhat", "kind", "sort"
        }
        
    def _load_comprehensive_taxonomy(self) -> Dict[str, Dict[str, List[str]]]:
        """Load the comprehensive taxonomy based on our analysis"""
        return {
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
            "SketchUp_(iPad_Mobile)": {
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
    
    def filter_question_text(self, text: str) -> str:
        """Filter out instructor names and non-technical words from question text"""
        # Convert to lowercase for filtering
        text_lower = text.lower()
        
        # Remove instructor names and common non-technical words
        for word in self.filter_words:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(word) + r'\b'
            text_lower = re.sub(pattern, '', text_lower)
        
        # Clean up extra whitespace
        text_lower = re.sub(r'\s+', ' ', text_lower).strip()
        
        return text_lower
    
    def extract_qa_pairs(self, content: str) -> List[Tuple[str, str]]:
        """Extract individual Q&A pairs from content preserving original format"""
        qa_pairs = []
        
        # Pattern for ### Question format with **A:** answer format (most common in our files)
        header_pattern = r'###\s*([^\n]+)\n\n\*\*A:\*\*\s*([\s\S]*?)(?=\n###|$)'
        header_matches = re.findall(header_pattern, content)
        
        if header_matches:
            for question, answer in header_matches:
                question = question.strip()
                answer = answer.strip()
                if question and answer:
                    qa_pairs.append((question, answer))
            return qa_pairs
        
        # Pattern for numbered questions with "Answer:" format
        numbered_pattern = r'(\d+\.\s*[^\n]+)\nAnswer:\n([\s\S]*?)(?=\n\d+\.|$)'
        numbered_matches = re.findall(numbered_pattern, content)
        
        if numbered_matches:
            for question, answer in numbered_matches:
                question = question.strip()
                answer = answer.strip()
                if question and answer:
                    qa_pairs.append((question, f"Answer:\n{answer}"))
            return qa_pairs
        
        # Pattern for ### Question format with **Answer:** format
        header_pattern2 = r'###\s*([^\n]+)\n\*\*Answer:\*\*\s*([\s\S]*?)(?=\n###|$)'
        header_matches2 = re.findall(header_pattern2, content)
        
        if header_matches2:
            for question, answer in header_matches2:
                question = question.strip()
                answer = answer.strip()
                if question and answer:
                    qa_pairs.append((question, f"**Answer:** {answer}"))
            return qa_pairs
        
        # Pattern for **Q:** format
        q_pattern = r'\*\*Q:\*\*\s*([^\n]+)\n\*\*Answer:\*\*\s*([\s\S]*?)(?=\n\*\*Q:\*\*|$)'
        q_matches = re.findall(q_pattern, content)
        
        if q_matches:
            for question, answer in q_matches:
                question = question.strip()
                answer = answer.strip()
                if question and answer:
                    qa_pairs.append((question, f"**Answer:** {answer}"))
            return qa_pairs
        
        return qa_pairs
    
    def determine_product(self, text: str) -> str:
        """Determine which SketchUp product the Q&A is about"""
        text_lower = text.lower()
        
        # Product-specific keywords with scoring
        product_keywords = {
            "SketchUp_Pro_(Desktop)": [
                "sketchup pro", "desktop", "pro", "professional", "3d modeling",
                "modeling", "design", "architecture", "construction", "interior design"
            ],
            "LayOut": [
                "layout", "lay out", "documentation", "presentation", "drawing", "plan",
                "section", "elevation", "detail", "annotation", "dimension", "construction document"
            ],
            "SketchUp_Web": [
                "sketchup web", "web", "browser", "online", "cloud", "web-based", "sketchup.com"
            ],
            "SketchUp_(iPad_Mobile)": [
                "sketchup go", "mobile", "ipad", "tablet", "touch", "ar", "augmented reality", "vr", "virtual reality"
            ],
            "SketchUp_Shop": [
                "sketchup shop", "shop", "premium", "online store", "e-commerce"
            ],
            "SketchUp_Studio": [
                "sketchup studio", "studio", "scan to design", "point cloud", "v-ray", "sustainability"
            ],
            "SketchUp_Mobile_Viewer": [
                "mobile viewer", "viewer app", "ios", "android", "view model"
            ]
        }
        
        best_product = None
        best_score = 0
        
        for product, keywords in product_keywords.items():
            current_score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    # Higher score for exact product name matches
                    if keyword in ["sketchup pro", "layout", "sketchup web", "sketchup go", "sketchup shop", "sketchup studio", "sketchup mobile viewer"]:
                        current_score += 10
                    else:
                        current_score += len(keyword.split()) * 2
            
            if current_score > best_score:
                best_score = current_score
                best_product = product
        
        # Fallback to SketchUp_Pro_(Desktop) if no clear match but contains general SketchUp content
        if not best_product and "sketchup" in text_lower:
            return "SketchUp_Pro_(Desktop)"
        
        return best_product
    
    def categorize_qa(self, question: str, answer: str) -> Tuple[str, str, str]:
        """Categorize Q&A based on comprehensive taxonomy"""
        # Filter the question text to remove instructor names and non-technical words
        filtered_question = self.filter_question_text(question)
        
        # Determine product first
        combined_text = f"{filtered_question} {answer}"
        product = self.determine_product(combined_text)
        
        if not product or product not in self.taxonomy:
            return None, None, None
        
        # Find best matching category and subcategory
        best_category = None
        best_subcategory = None
        best_score = 0
        
        for category, subcategories in self.taxonomy[product].items():
            category_score = self._calculate_category_score(category, combined_text, filtered_question)
            
            for subcategory in subcategories:
                subcategory_score = self._calculate_subcategory_score(subcategory, combined_text, filtered_question)
                total_score = category_score + subcategory_score
                
                if total_score > best_score:
                    best_score = total_score
                    best_category = category
                    best_subcategory = subcategory
        
        # Only return if we have a reasonable match
        if best_score >= 1:  # Lowered threshold for better categorization
            return product, best_category, best_subcategory
        
        return None, None, None
    
    def _calculate_category_score(self, category: str, combined_text: str, question: str) -> int:
        """Calculate score for category matching"""
        category_keywords = self._get_category_keywords(category)
        score = 0
        
        question_lower = question.lower()
        combined_lower = combined_text.lower()
        
        for keyword in category_keywords:
            if keyword in question_lower:
                score += len(keyword.split()) * 3  # Higher score for question matches
            elif keyword in combined_lower:
                score += len(keyword.split()) * 2
        
        return score
    
    def _calculate_subcategory_score(self, subcategory: str, combined_text: str, question: str) -> int:
        """Calculate score for subcategory matching"""
        search_terms = self._get_subcategory_search_terms(subcategory)
        score = 0
        
        question_lower = question.lower()
        combined_lower = combined_text.lower()
        
        for term in search_terms:
            if term in question_lower:
                score += len(term.split()) * 4  # Very high score for question matches
            elif term in combined_lower:
                score += len(term.split()) * 2
        
        return score
    
    def _get_category_keywords(self, category: str) -> List[str]:
        """Get keywords for category matching"""
        category_keywords = {
            "Installation_&_Setup": ["install", "installation", "setup", "download", "activate", "license", "subscription"],
            "Updates_&_Versioning": ["update", "upgrade", "version", "new version", "changelog", "migration"],
            "Getting_Started_&_Basics": ["getting started", "beginner", "basic", "tutorial", "introduction", "overview"],
            "Drawing_&_Modeling_Tools": ["draw", "drawing", "model", "modeling", "tool", "tools", "create"],
            "Components_and_Groups": ["component", "components", "group", "groups", "instance", "library"],
            "Materials_and_Textures": ["material", "materials", "texture", "textures", "color", "paint"],
            "Styles_and_Display": ["style", "styles", "display", "appearance", "visual", "render"],
            "Scenes_and_Animation": ["scene", "scenes", "animation", "animate", "camera", "walkthrough"],
            "Import_and_Export": ["import", "export", "file", "format", "save", "load"],
            "Extensions_and_Plugins": ["extension", "extensions", "plugin", "plugins", "add-on", "warehouse"],
            "LayOut_Integration": ["layout", "lay out", "document", "presentation", "drawing"],
            "Rendering_and_Visualization": ["render", "rendering", "visualization", "lighting", "shadows"],
            "Troubleshooting_and_Support": ["problem", "error", "issue", "troubleshoot", "fix", "crash"],
            "Advanced_Techniques": ["advanced", "complex", "scripting", "automation", "parametric"],
            "Collaboration_and_Sharing": ["collaboration", "sharing", "team", "cloud", "connect"],
            "Licensing_and_Subscription": ["license", "licensing", "subscription", "billing", "account"],
            "Hardware_and_Software_Compatibility": ["hardware", "software", "compatibility", "gpu", "driver"],
            "Customization_and_Workflows": ["customize", "customization", "workflow", "shortcut", "template"],
            "Educational_Resources": ["tutorial", "course", "learning", "education", "guide"],
            "Feature_Specific": ["feature", "specific", "live components", "warehouse", "scan"]
        }
        
        return category_keywords.get(category, [category.lower().replace('_', ' ')])
    
    def _get_subcategory_search_terms(self, subcategory: str) -> List[str]:
        """Get search terms for subcategory matching"""
        # Convert underscore to space and create variations
        base_term = subcategory.replace('_', ' ')
        search_terms = [base_term, subcategory]
        
        # Add common variations
        if 'tool' in subcategory:
            search_terms.extend(['tool', 'tools'])
        if 'component' in subcategory:
            search_terms.extend(['component', 'components'])
        if 'material' in subcategory:
            search_terms.extend(['material', 'materials'])
        if 'extension' in subcategory:
            search_terms.extend(['extension', 'extensions'])
        if 'import' in subcategory:
            search_terms.extend(['import', 'importing'])
        if 'export' in subcategory:
            search_terms.extend(['export', 'exporting'])
        if 'layout' in subcategory:
            search_terms.extend(['layout', 'lay out'])
        
        return search_terms
    
    def write_qa_to_category(self, product: str, category: str, subcategory: str, question: str, answer: str, qa_number: int):
        """Write Q&A to the appropriate category folder"""
        target_dir = self.taxonomy_dir / product / category / subcategory
        target_file = target_dir / f"qa_content.md"
        
        # Create directory if it doesn't exist
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Format the Q&A content
        formatted_content = f"\n## Q&A #{qa_number}\n\n"
        formatted_content += f"**Question:** {question}\n\n"
        formatted_content += f"**Answer:** {answer}\n\n"
        formatted_content += "---\n"
        
        # Append to file
        with open(target_file, 'a', encoding='utf-8') as f:
            f.write(formatted_content)
    
    def categorize_all_playlists(self):
        """Categorize all Q&A from playlist files using comprehensive taxonomy"""
        print("🚀 Starting comprehensive Q&A categorization with improved filtering...")
        print(f"📁 Using taxonomy structure: {self.taxonomy_dir}")
        
        # Find all playlist directories
        playlist_dirs = [d for d in self.base_output_dir.iterdir() if d.is_dir() and d.name.startswith('PL-')]
        
        total_qa_pairs = 0
        categorized_pairs = 0
        skipped_pairs = 0
        categorization_stats = Counter()
        
        for playlist_dir in playlist_dirs:
            print(f"\n📁 Processing playlist: {playlist_dir.name}")
            
            # Find all Q&A files in the playlist
            qa_files = list(playlist_dir.glob("*_QnA.md"))
            
            for qa_file in qa_files:
                try:
                    with open(qa_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Extract Q&A pairs
                    qa_pairs = self.extract_qa_pairs(content)
                    total_qa_pairs += len(qa_pairs)
                    
                    for i, (question, answer) in enumerate(qa_pairs, 1):
                        # Categorize the Q&A pair
                        product, category, subcategory = self.categorize_qa(question, answer)
                        
                        if product and category and subcategory:
                            # Write to appropriate category
                            self.write_qa_to_category(product, category, subcategory, question, answer, i)
                            categorized_pairs += 1
                            categorization_stats[f"{product}/{category}/{subcategory}"] += 1
                            
                            if categorized_pairs <= 10:  # Show first 10 categorizations
                                print(f"  ✅ Categorized: {question[:50]}... -> {product}/{category}/{subcategory}")
                        else:
                            skipped_pairs += 1
                            if skipped_pairs <= 5:  # Show first 5 skips
                                print(f"  ❌ Skipped: {question[:50]}... (no match)")
                
                except Exception as e:
                    print(f"Error processing {qa_file}: {e}")
        
        # Generate summary report
        self.generate_categorization_report(total_qa_pairs, categorized_pairs, skipped_pairs, categorization_stats)
    
    def generate_categorization_report(self, total_qa_pairs: int, categorized_pairs: int, skipped_pairs: int, categorization_stats: Counter):
        """Generate comprehensive categorization report"""
        print(f"\n{'='*80}")
        print(f"📊 COMPREHENSIVE CATEGORIZATION REPORT")
        print(f"{'='*80}")
        
        print(f"\n📈 SUMMARY:")
        print(f"  • Total Q&A pairs processed: {total_qa_pairs}")
        print(f"  • Successfully categorized: {categorized_pairs}")
        print(f"  • Skipped (no match): {skipped_pairs}")
        print(f"  • Categorization rate: {(categorized_pairs/total_qa_pairs)*100:.1f}%")
        
        print(f"\n🏆 TOP CATEGORIES (by Q&A count):")
        for category_path, count in categorization_stats.most_common(15):
            print(f"  • {category_path}: {count} Q&A pairs")
        
        print(f"\n📁 Categorized content location: {self.taxonomy_dir}")
        print(f"✅ Categorization completed successfully!")

def main():
    categorizer = TaxonomyCategorizer()
    categorizer.categorize_all_playlists()

if __name__ == "__main__":
    main() 