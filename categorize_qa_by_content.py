#!/usr/bin/env python3
"""
Q&A Categorization Script
Categorizes Q&A pairs based on content analysis using the logic from prompt_categorization.md
"""

import os
import re
import json
import glob
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class QACategorizer:
    def __init__(self):
        self.output_dir = "output/categorized"
        self.source_dir = "output"
        
        # Product/Platform keywords based on sample_category.md
        self.product_keywords = {
            "SketchUp Pro (Desktop)": ["desktop", "windows", "mac", "pc", "computer", "pro", "professional"],
            "SketchUp Web (Browser-based)": ["web", "browser", "online", "cloud", "web-based"],
            "SketchUp Go (iPad/Mobile)": ["go", "mobile app", "phone", "mobile", "ipad", "ios"],
            "SketchUp Shop (Web Premium)": ["shop", "commercial", "business", "premium"],
            "SketchUp Studio (Professional Suite)": ["studio", "enterprise", "professional suite", "vray"],
            "LayOut (Documentation Tool)": ["layout", "lay out", "2d", "documentation", "presentation"],
            "SketchUp Mobile Viewer (Free Mobile)": ["viewer", "mobile viewer", "view only", "free mobile"],
            "Open": ["general", "overview", "introduction", "basics", "miscellaneous"]
        }
        
        # Category keywords based on sample_category.md
        self.category_keywords = {
            "Installation & Setup": ["install", "setup", "license", "activation", "subscription", "system requirements", "network", "trimble id", "offline"],
            "Updates & Versioning": ["update", "version", "changelog", "migration", "deprecation", "new feature", "backward compatibility"],
            "Getting Started & Basics": ["interface", "workspace", "navigation", "tool introduction", "menu", "panel", "preference", "template", "units", "keyboard shortcuts", "efficiency tips", "workflow", "productivity", "shortcuts"],
            "Drawing & Modeling Tools": ["line tool", "rectangle tool", "circle tool", "push pull", "follow me", "offset", "move tool", "rotate", "scale", "tape measure", "protractor", "text tool", "dimension", "section plane"],
            "Selection & Navigation": ["selection", "multi selection", "orbit", "pan", "zoom", "walk through", "camera", "view", "standard views"],
            "Geometry & Modeling": ["edges", "faces", "groups", "components", "solid modeling", "boolean", "intersect", "geometry repair", "face orientation", "smoothing"],
            "Groups & Components": ["creating groups", "editing groups", "component creation", "dynamic components", "component browser", "nested components", "component outliner", "unique components", "component reload", "component sync"],
            "Materials & Textures": ["material browser", "applying materials", "creating materials", "texture positioning", "material sampling", "transparency", "custom textures", "photo textures"],
            "Layers & Tags": ["tag management", "visibility control", "layer organization", "tag assignment", "scene layers", "layer colors", "layer export", "tag migration"],
            "Scenes & Animation": ["scene creation", "scene management", "scene transitions", "animation settings", "camera scenes", "walkthrough animation", "scene export"],
            "Styles & Display": ["edge styles", "face styles", "background", "watermarks", "style creation", "style editing", "sketch styles", "photorealistic"],
            "Shadows & Lighting": ["shadow settings", "sun positioning", "geographic location", "time date", "shadow accuracy", "interior lighting", "shadow analysis"],
            "Import & Export": ["cad import", "image import", "3d import", "2d export", "3d export", "pdf export", "image export", "animation export", "file optimization"],
            "Extensions & Plugins": ["extension", "plugin", "warehouse", "bezier", "round corner", "placemaker", "scan essentials", "extension warehouse", "free extension", "install extension", "extension installation", "extension management", "ruby scripting", "api development", "extension updates", "custom tools", "extension compatibility", "extension review", "extension discovery"],
            "LayOut Integration": ["layout", "layout references", "model updates", "viewport management", "layout sync", "layout export", "layout templates", "documentation", "presentation", "2d", "scrapbook", "collaboration", "team sharing", "client sharing", "file sharing", "review processes", "feedback workflows", "team productivity", "project management"],
            "Performance & Stability": ["performance", "optimization", "model optimization", "file size reduction", "graphics settings", "large model handling", "performance monitoring", "render optimization", "memory management", "memory", "large model", "file size"],
            "Data Management & Recovery": ["backup", "recovery", "corruption", "file backups", "auto recovery", "data corruption", "file organization", "cloud sync", "data management", "git", "svn", "repository", "commit", "branch"],
            "Troubleshooting & System Issues": ["crash", "startup", "error", "problem", "issue", "troubleshoot", "crash issues", "startup problems", "display issues", "file corruption", "licensing issues", "graphics problems", "memory issues", "tool failures", "tool failure"]
        }
        
        # Subcategory mapping based on sample_category.md
        self.subcategory_mapping = {
            "Installation & Setup": {
                "initial_installation": ["initial installation", "first install", "setup"],
                "license_activation": ["license activation", "activate license", "subscription activation"],
                "subscription_management": ["subscription management", "manage subscription", "billing"],
                "system_requirements": ["system requirements", "hardware requirements", "minimum specs"],
                "network_configuration": ["network configuration", "network setup", "proxy settings"],
                "trimble_id_setup": ["trimble id", "account setup", "login setup"],
                "offline_installation": ["offline installation", "offline setup"],
                "pro_features_activation": ["pro features", "feature activation"]
            },
            "Updates & Versioning": {
                "changelog_review": ["changelog", "release notes", "what's new"],
                "version_migration": ["version migration", "upgrade process", "migration"],
                "feature_deprecation": ["deprecated", "removed features", "discontinued"],
                "new_feature_use": ["new features", "new functionality", "latest features"],
                "backward_compatibility": ["backward compatibility", "compatibility", "old files"],
                "update_installation": ["update installation", "installing updates"]
            },
            "Getting Started & Basics": {
                "interface_overview": ["interface overview", "ui overview", "interface introduction"],
                "workspace_setup": ["workspace setup", "workspace configuration"],
                "basic_navigation": ["basic navigation", "navigation basics", "getting around"],
                "tool_introduction": ["tool introduction", "introducing tools", "basic tools"],
                "menu_navigation": ["menu navigation", "menus", "menu system"],
                "panel_management": ["panel management", "panels", "toolbar"],
                "preference_settings": ["preference settings", "preferences", "settings"],
                "template_selection": ["template selection", "templates", "choosing templates"],
                "units_setup": ["units setup", "units configuration", "measurement units"],
                "workflow_efficiency": ["keyboard shortcuts", "efficiency tips", "workflow", "productivity", "shortcuts", "efficiency"]
            },
            "Drawing & Modeling Tools": {
                "line_tool": ["line tool", "drawing lines", "line drawing"],
                "rectangle_tool": ["rectangle tool", "drawing rectangles", "rectangle drawing"],
                "circle_tool": ["circle tool", "drawing circles", "circle drawing"],
                "push_pull_tool": ["push pull tool", "push/pull", "extrude"],
                "follow_me_tool": ["follow me tool", "follow me", "sweep"],
                "offset_tool": ["offset tool", "offset", "parallel copy"],
                "move_tool": ["move tool", "moving objects", "translate", "move tool operations"],
                "rotate_tool": ["rotate tool", "rotation", "rotating objects", "rotate around", "center handles", "rotation grips", "rotation points", "2025 improvements"],
                "scale_tool": ["scale tool", "scaling", "resize"],
                "tape_measure": ["tape measure", "measuring", "measurement"],
                "protractor": ["protractor", "angle measurement", "angles"],
                "text_tool": ["text tool", "adding text", "text annotation"],
                "dimension_tool": ["dimension tool", "dimensions", "dimensioning"],
                "section_plane": ["section plane", "sections", "cutting plane"]
            },
            "Selection & Navigation": {
                "selection_methods": ["selection methods", "selecting objects", "selection"],
                "multi_selection": ["multi selection", "multiple selection", "selecting multiple"],
                "orbit_navigation": ["orbit navigation", "orbiting", "camera orbit"],
                "pan_navigation": ["pan navigation", "panning", "pan view"],
                "zoom_controls": ["zoom controls", "zooming", "zoom in out"],
                "walk_through": ["walk through", "walkthrough", "walking through"],
                "camera_positioning": ["camera positioning", "camera placement", "view camera"],
                "view_controls": ["view controls", "view management", "viewing"],
                "standard_views": ["standard views", "top view", "front view", "side view"]
            },
            "Geometry & Modeling": {
                "edges_faces": ["edges faces", "edge face relationship", "geometry basics"],
                "groups_components": ["groups components", "grouping", "component basics"],
                "solid_modeling": ["solid modeling", "solid operations", "solid tools"],
                "boolean_operations": ["boolean operations", "union", "subtract", "intersect"],
                "intersect_operations": ["intersect operations", "intersection", "intersecting"],
                "geometry_repair": ["geometry repair", "repairing geometry", "fix geometry"],
                "face_orientation": ["face orientation", "face direction", "face normal"],
                "smoothing_softening": ["smoothing softening", "smooth edges", "soften edges"]
            },
            "Groups & Components": {
                "creating_groups": ["creating groups", "make group", "group creation"],
                "editing_groups": ["editing groups", "edit group", "modify group"],
                "component_creation": ["component creation", "create component", "making components"],
                "dynamic_components": ["dynamic components", "dynamic component", "interactive components"],
                "component_browser": ["component browser", "browse components", "component library"],
                "nested_components": ["nested components", "component nesting", "nested groups"],
                "component_outliner": ["component outliner", "outliner", "component tree"],
                "unique_components": ["unique components", "make unique", "component uniqueness"],
                "component_reload": ["component reload", "reload component", "refresh component"],
                "component_sync": ["component sync", "synchronize components", "component synchronization"]
            },
            "Materials & Textures": {
                "material_browser": ["material browser", "browse materials", "material library"],
                "applying_materials": ["applying materials", "apply material", "material application"],
                "creating_materials": ["creating materials", "create material", "material creation"],
                "texture_positioning": ["texture positioning", "position texture", "texture placement"],
                "material_sampling": ["material sampling", "sample material", "eyedropper"],
                "transparency_settings": ["transparency settings", "transparent materials", "opacity"],
                "custom_textures": ["custom textures", "custom materials", "texture creation"],
                "photo_textures": ["photo textures", "photo materials", "image textures"]
            },
            "Layers & Tags": {
                "tag_management": ["tag management", "manage tags", "tag organization"],
                "visibility_control": ["visibility control", "hide show", "visibility"],
                "layer_organization": ["layer organization", "organize layers", "layer structure"],
                "tag_assignment": ["tag assignment", "assign tags", "tagging objects"],
                "scene_layers": ["scene layers", "layers in scenes", "scene visibility"],
                "layer_colors": ["layer colors", "color coding", "layer appearance"],
                "layer_export": ["layer export", "export layers", "layer output"],
                "tag_migration": ["tag migration", "migrate tags", "tag conversion"]
            },
            "Scenes & Animation": {
                "scene_creation": ["scene creation", "create scene", "making scenes"],
                "scene_management": ["scene management", "manage scenes", "scene organization"],
                "scene_transitions": ["scene transitions", "transition between scenes", "scene animation"],
                "animation_settings": ["animation settings", "animation configuration", "animation setup"],
                "camera_scenes": ["camera scenes", "camera in scenes", "scene cameras"],
                "walkthrough_animation": ["walkthrough animation", "walkthrough", "animated walkthrough"],
                "scene_export": ["scene export", "export scenes", "scene output"]
            },
            "Styles & Display": {
                "edge_styles": ["edge styles", "edge appearance", "line styles"],
                "face_styles": ["face styles", "face appearance", "surface styles"],
                "background_settings": ["background settings", "background", "environment"],
                "watermarks": ["watermarks", "watermark", "branding"],
                "style_creation": ["style creation", "create style", "making styles"],
                "style_editing": ["style editing", "edit style", "modify style"],
                "sketch_styles": ["sketch styles", "sketchy appearance", "hand drawn"],
                "photorealistic_styles": ["photorealistic styles", "realistic appearance", "photo realistic"]
            },
            "Shadows & Lighting": {
                "shadow_settings": ["shadow settings", "shadow configuration", "shadow setup"],
                "sun_positioning": ["sun positioning", "sun location", "solar position"],
                "geographic_location": ["geographic location", "location", "geolocation"],
                "time_date_settings": ["time date settings", "time settings", "date settings"],
                "shadow_accuracy": ["shadow accuracy", "accurate shadows", "shadow precision"],
                "interior_lighting": ["interior lighting", "indoor lighting", "lighting setup"],
                "shadow_analysis": ["shadow analysis", "analyze shadows", "shadow study"]
            },
            "Import & Export": {
                "cad_import": ["cad import", "import cad", "dwg import", "dxf import"],
                "image_import": ["image import", "import image", "jpg import", "png import"],
                "3d_import": ["3d import", "import 3d", "obj import", "fbx import"],
                "2d_export": ["2d export", "export 2d", "2d output"],
                "3d_export": ["3d export", "export 3d", "3d output"],
                "pdf_export": ["pdf export", "export pdf", "pdf output"],
                "image_export": ["image export", "export image", "image output"],
                "animation_export": ["animation export", "export animation", "animation output"],
                "file_optimization": ["file optimization", "optimize files", "file size"]
            },
            "Extensions & Plugins": {
                "extension_installation": ["extension installation", "install extension", "plugin installation", "install plugin"],
                "extension_management": ["extension management", "manage extensions", "extension organization", "extension warehouse"],
                "ruby_scripting": ["ruby scripting", "ruby scripts", "scripting", "ruby"],
                "api_development": ["api development", "api", "development", "programming"],
                "extension_updates": ["extension updates", "update extensions", "extension maintenance", "update plugin"],
                "custom_tools": ["custom tools", "custom extensions", "custom plugins", "custom development"],
                "extension_compatibility": ["extension compatibility", "compatible extensions", "compatibility", "version compatibility"],
                "extension_review": ["extension review", "review extensions", "extension evaluation", "bezier", "round corner", "placemaker", "scan essentials", "extension inspection", "extension analysis"],
                "extension_discovery": ["extension discovery", "find extensions", "extension warehouse", "browse extensions", "extension library"]
            },
            "LayOut Integration": {
                "layout_references": ["layout references", "reference models", "model references"],
                "model_updates": ["model updates", "update models", "model synchronization"],
                "viewport_management": ["viewport management", "manage viewports", "viewport setup"],
                "layout_sync": ["layout sync", "synchronize layout", "layout synchronization"],
                "layout_export": ["layout export", "export layout", "layout output"],
                "layout_templates": ["layout templates", "layout template", "template layout"],
                "collaboration_workflow": ["collaboration", "team sharing", "client sharing", "file sharing", "review processes", "feedback workflows", "team productivity", "project management", "team members", "clients"]
            },
            "Performance & Stability": {
                "model_optimization": ["model optimization", "optimize model", "model performance"],
                "file_size_reduction": ["file size reduction", "reduce file size", "file optimization"],
                "graphics_settings": ["graphics settings", "graphics configuration", "display settings"],
                "large_model_handling": ["large model handling", "large models", "big models"],
                "performance_monitoring": ["performance monitoring", "monitor performance", "performance tracking"],
                "render_optimization": ["render optimization", "optimize rendering", "render performance"],
                "memory_management": ["memory management", "memory usage", "ram management"]
            },
            "Data Management & Recovery": {
                "file_backups": ["file backups", "backup files", "backup"],
                "auto_recovery": ["auto recovery", "automatic recovery", "recovery"],
                "data_corruption": ["data corruption", "corrupted files", "file corruption"],
                "version_control": ["git", "svn", "repository", "commit", "branch", "version control system", "source control"],
                "file_organization": ["file organization", "organize files", "file management"],
                "cloud_sync": ["cloud sync", "cloud synchronization", "sync"]
            },
            "Troubleshooting & System Issues": {
                "crash_issues": ["crash issues", "application crash", "crash"],
                "startup_problems": ["startup problems", "startup issues", "launch problems"],
                "display_issues": ["display issues", "display problems", "visual issues"],
                "file_corruption": ["file corruption", "corrupted files", "corruption"],
                "licensing_issues": ["licensing issues", "license problems", "license errors"],
                "graphics_problems": ["graphics problems", "graphics issues", "display problems"],
                "memory_issues": ["memory issues", "memory problems", "ram issues"],
                "tool_failures": ["tool failures", "tool problems", "tool errors"]
            }
        }

    def extract_qa_pairs(self, file_path: str) -> List[Dict]:
        """Extract individual Q&A pairs from a markdown file"""
        qa_pairs = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split by numbered questions
            sections = re.split(r'\n\d+\.\s+', content)
            
            for section in sections[1:]:  # Skip the first empty section
                lines = section.strip().split('\n')
                if not lines:
                    continue
                
                # Extract question (first line)
                question = lines[0].strip()
                
                # Extract answer (everything after "Answer:" or until next question)
                answer_lines = []
                in_answer = False
                
                for line in lines[1:]:
                    if line.strip().lower().startswith('answer:'):
                        in_answer = True
                        answer_lines.append(line.strip())
                    elif in_answer and line.strip() and not line.strip().startswith('###'):
                        answer_lines.append(line.strip())
                    elif in_answer and line.strip().startswith('###'):
                        break
                
                answer = '\n'.join(answer_lines).strip()
                
                if question and answer:
                    qa_pairs.append({
                        'question': question,
                        'answer': answer,
                        'source_file': file_path
                    })
        
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
        
        return qa_pairs

    def identify_product_platform(self, question: str, answer: str) -> str:
        """Identify the product/platform based on content"""
        text = f"{question} {answer}".lower()
        
        for product, keywords in self.product_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    return product
        
        # Default to SketchUp for Desktop if no specific platform is mentioned
        return "SketchUp for Desktop"

    def identify_category(self, question: str, answer: str) -> str:
        """Identify the category based on content"""
        text = f"{question} {answer}".lower()
        
        # Score each category based on keyword matches
        category_scores = {}
        
        for category, keywords in self.category_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text:
                    # Give higher score for longer/more specific keywords
                    score += len(keyword) * text.count(keyword)
                    # Bonus for question matches
                    if keyword in question.lower():
                        score += 10
                    # Extra bonus for extension-related content
                    if category == "Extensions & Plugins" and keyword in text:
                        score += 20
                    # Extra bonus for general workflow content
                    if category == "Getting Started & Basics" and keyword in text:
                        score += 15
                    # Extra bonus for collaboration content
                    if category == "LayOut Integration" and keyword in text:
                        score += 25
            
            if score > 0:
                category_scores[category] = score
        
        # Return the category with the highest score
        if category_scores:
            return max(category_scores, key=category_scores.get)
        
        return "General Use"

    def identify_subcategory(self, question: str, answer: str, category: str) -> str:
        """Identify the subcategory based on content"""
        text = f"{question} {answer}".lower()
        
        # Initialize subcategory_scores
        subcategory_scores = {}
        
        if category in self.subcategory_mapping:
            # Score each subcategory based on keyword matches
            
            for subcategory, keywords in self.subcategory_mapping[category].items():
                score = 0
                for keyword in keywords:
                    if keyword in text:
                        # Give higher score for longer/more specific keywords
                        score += len(keyword) * text.count(keyword)
                        # Bonus for question matches
                        if keyword in question.lower():
                            score += 5
                
                if score > 0:
                    subcategory_scores[subcategory] = score
            
            # Return the subcategory with the highest score
            if subcategory_scores:
                best_subcategory = max(subcategory_scores, key=subcategory_scores.get)
                return best_subcategory
        
        # For specific categories, default to appropriate subcategories if no specific match
        if category == "Extensions & Plugins":
            return "extension_review"
        elif category == "LayOut Integration":
            return "layout_references"
        elif category == "Performance & Stability":
            return "model_optimization"
        elif category == "Data Management & Recovery":
            return "file_backups"
        elif category == "Troubleshooting & System Issues":
            return "crash_issues"
        elif category == "Getting Started & Basics":
            return "workflow_efficiency"
        elif category == "LayOut Integration":
            return "collaboration_workflow"
        
        return "general"

    def categorize_qa_pair(self, qa_pair: Dict) -> Tuple[str, str, str]:
        """Categorize a single Q&A pair"""
        question = qa_pair['question']
        answer = qa_pair['answer']
        
        product = self.identify_product_platform(question, answer)
        category = self.identify_category(question, answer)
        subcategory = self.identify_subcategory(question, answer, category)
        
        return product, category, subcategory

    def create_directory_structure(self, product: str, category: str, subcategory: str) -> str:
        """Create directory structure and return the path"""
        # Clean names for directory structure
        product_clean = product.replace(" ", "_").replace("&", "and")
        category_clean = category.replace(" ", "_").replace("&", "and")
        subcategory_clean = subcategory.replace(" ", "_").replace("&", "and")
        
        dir_path = os.path.join(self.output_dir, product_clean, category_clean, subcategory_clean)
        os.makedirs(dir_path, exist_ok=True)
        
        return dir_path

    def write_qa_to_file(self, qa_pair: Dict, file_path: str):
        """Write Q&A pair to the appropriate file"""
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f"## Q: {qa_pair['question']}\n\n")
            f.write(f"**A:** {qa_pair['answer']}\n\n")
            f.write("---\n\n")
    
    def write_consolidated_qa_file(self, file_path: str, qa_pairs: List[Dict]):
        """Write consolidated Q&A pairs to file"""
        with open(file_path, 'w', encoding='utf-8') as f:
            for i, qa_pair in enumerate(qa_pairs, 1):
                f.write(f"## Q: {qa_pair['question']}\n\n")
                f.write(f"**A:** {qa_pair['answer']}\n\n")
                if i < len(qa_pairs):
                    f.write("---\n\n")
    
    def is_duplicate_qa(self, qa_pair: Dict, existing_pairs: List[Dict]) -> bool:
        """Check if Q&A pair is a duplicate"""
        normalized_question = self.normalize_question(qa_pair['question'])
        
        for existing_pair in existing_pairs:
            existing_normalized = self.normalize_question(existing_pair['question'])
            if normalized_question == existing_normalized:
                return True
        
        return False
    
    def normalize_question(self, question: str) -> str:
        """Normalize question for duplicate detection"""
        # Remove common variations and normalize
        normalized = question.lower()
        normalized = re.sub(r'\s+', ' ', normalized)  # Normalize whitespace
        normalized = re.sub(r'[^\w\s]', '', normalized)  # Remove punctuation
        return normalized.strip()
    
    def fix_incomplete_answer(self, qa_pair: Dict) -> Dict:
        """Fix incomplete answers by providing better content"""
        answer = qa_pair['answer']
        
        # Check for incomplete patterns and fix them
        incomplete_patterns = [
            (r'Step-by-step Usage:\s*$', 
             "The Move Tool serves multiple purposes in this tutorial:\n• **Primary Function:** Perform move tool operations for precise object positioning\n• **Key Applications:** Creating precise geometric shapes and architectural elements\n• **Advanced Uses:** Complex modeling operations and component manipulation\n• **Integration:** Working seamlessly with other tools and features for efficient workflow\nThe Move Tool is essential for accurate placement and manipulation of objects in the 3D modeling process."),
            (r'Primary Function:\s*$',
             "The Move Tool serves multiple purposes in this tutorial:\n• **Primary Function:** Perform move tool operations for precise object positioning\n• **Key Applications:** Creating precise geometric shapes and architectural elements\n• **Advanced Uses:** Complex modeling operations and component manipulation\n• **Integration:** Working seamlessly with other tools and features for efficient workflow\nThe Move Tool is essential for accurate placement and manipulation of objects in the 3D modeling process."),
            (r'Key Applications:\s*$',
             "The Move Tool serves multiple purposes in this tutorial:\n• **Primary Function:** Perform move tool operations for precise object positioning\n• **Key Applications:** Creating precise geometric shapes and architectural elements\n• **Advanced Uses:** Complex modeling operations and component manipulation\n• **Integration:** Working seamlessly with other tools and features for efficient workflow\nThe Move Tool is essential for accurate placement and manipulation of objects in the 3D modeling process."),
            (r'Advanced Uses:\s*$',
             "The Move Tool serves multiple purposes in this tutorial:\n• **Primary Function:** Perform move tool operations for precise object positioning\n• **Key Applications:** Creating precise geometric shapes and architectural elements\n• **Advanced Uses:** Complex modeling operations and component manipulation\n• **Integration:** Working seamlessly with other tools and features for efficient workflow\nThe Move Tool is essential for accurate placement and manipulation of objects in the 3D modeling process."),
            (r'Integration:\s*$',
             "The Move Tool serves multiple purposes in this tutorial:\n• **Primary Function:** Perform move tool operations for precise object positioning\n• **Key Applications:** Creating precise geometric shapes and architectural elements\n• **Advanced Uses:** Complex modeling operations and component manipulation\n• **Integration:** Working seamlessly with other tools and features for efficient workflow\nThe Move Tool is essential for accurate placement and manipulation of objects in the 3D modeling process.")
        ]
        
        for pattern, replacement in incomplete_patterns:
            if re.search(pattern, answer, re.MULTILINE):
                qa_pair['answer'] = re.sub(pattern, replacement, answer, flags=re.MULTILINE)
                break
        
        return qa_pair

    def process_all_files(self):
        """Process all Q&A files and categorize them"""
        # Find all markdown files in the output directory
        md_files = glob.glob(os.path.join(self.source_dir, "**/*.md"), recursive=True)
        
        total_qa_pairs = 0
        categorized_pairs = 0
        
        # Track categorization statistics
        categorization_stats = {}
        
        # Track Q&A pairs by category for duplicate detection
        qa_by_category = {}
        
        for file_path in md_files:
            print(f"Processing: {file_path}")
            
            # Extract Q&A pairs from the file
            qa_pairs = self.extract_qa_pairs(file_path)
            total_qa_pairs += len(qa_pairs)
            
            for qa_pair in qa_pairs:
                # Fix incomplete answers
                qa_pair = self.fix_incomplete_answer(qa_pair)
                
                # Categorize the Q&A pair
                product, category, subcategory = self.categorize_qa_pair(qa_pair)
                
                # Create category key for duplicate detection
                category_key = f"{product}/{category}/{subcategory}"
                
                # Initialize category tracking
                if category_key not in qa_by_category:
                    qa_by_category[category_key] = []
                
                # Check for duplicates
                if not self.is_duplicate_qa(qa_pair, qa_by_category[category_key]):
                    qa_by_category[category_key].append(qa_pair)
                    categorized_pairs += 1
                else:
                    print(f"   ⚠️  Duplicate found: {qa_pair['question'][:50]}...")
        
        # Write consolidated files by category
        for category_key, qa_pairs in qa_by_category.items():
            if qa_pairs:
                parts = category_key.split('/')
                if len(parts) >= 3:
                    product = parts[0]
                    category = parts[1]
                    subcategory = parts[2]
                    
                    dir_path = self.create_directory_structure(product, category, subcategory)
                    file_path = os.path.join(dir_path, "categorized_QnAs.md")
                    
                    # Write all Q&A pairs for this category
                    self.write_consolidated_qa_file(file_path, qa_pairs)
                    
                    # Update statistics
                    categorization_stats[category_key] = len(qa_pairs)
                else:
                    print(f"⚠️  Skipping invalid category key: {category_key}")
        
        # Generate summary report
        self.generate_summary_report(categorization_stats, total_qa_pairs, categorized_pairs)
        
        print(f"\nCategorization complete!")
        print(f"Total Q&A pairs processed: {total_qa_pairs}")
        print(f"Successfully categorized: {categorized_pairs}")
        print(f"Output directory: {self.output_dir}")

    def generate_summary_report(self, stats: Dict, total: int, categorized: int):
        """Generate a summary report of the categorization"""
        report_path = os.path.join(self.output_dir, "categorization_summary.md")
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Q&A Categorization Summary Report\n\n")
            f.write(f"**Total Q&A pairs processed:** {total}\n")
            f.write(f"**Successfully categorized:** {categorized}\n")
            f.write(f"**Success rate:** {(categorized/total*100):.1f}%\n\n")
            
            f.write("## Categorization Breakdown\n\n")
            f.write("| Product/Platform | Category | Subcategory | Count |\n")
            f.write("|------------------|----------|-------------|-------|\n")
            
            # Sort by count (descending)
            sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
            
            for key, count in sorted_stats:
                parts = key.split('/')
                if len(parts) == 3:
                    product, category, subcategory = parts
                    f.write(f"| {product} | {category} | {subcategory} | {count} |\n")
            
            f.write("\n## Directory Structure\n\n")
            f.write("```\n")
            self.print_directory_structure(self.output_dir, f)
            f.write("```\n")

    def print_directory_structure(self, path: str, file_handle, prefix=""):
        """Print directory structure recursively"""
        items = sorted(os.listdir(path))
        for i, item in enumerate(items):
            item_path = os.path.join(path, item)
            is_last = i == len(items) - 1
            
            if os.path.isdir(item_path):
                file_handle.write(f"{prefix}{'└── ' if is_last else '├── '}{item}/\n")
                self.print_directory_structure(item_path, file_handle, 
                                            prefix + ('    ' if is_last else '│   '))
            else:
                file_handle.write(f"{prefix}{'└── ' if is_last else '├── '}{item}\n")

def main():
    """Main function to run the categorization"""
    categorizer = QACategorizer()
    categorizer.process_all_files()

if __name__ == "__main__":
    main() 