#!/usr/bin/env python3
"""
Fix Tool Categorization Script
Moves files back to their proper tool directories and cleans up the enhanced categorizer mess
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict

class ToolCategorizationFixer:
    def __init__(self, base_output_dir="output"):
        self.base_output_dir = Path(base_output_dir)
        self.categorized_dir = self.base_output_dir / "categorized"
        
        # Define tool-specific keywords
        self.tool_keywords = {
            "rotate_tool": ["rotate tool", "rotation", "rotating", "rotate around", "center handles", "rotation grips"],
            "move_tool": ["move tool", "moving objects", "translation", "move tool operations"],
            "text_tool": ["text tool", "3d text", "text annotation", "leader"],
            "line_tool": ["line tool", "drawing lines", "line segments"],
            "rectangle_tool": ["rectangle tool", "drawing rectangles"],
            "circle_tool": ["circle tool", "drawing circles"],
            "push_pull_tool": ["push pull tool", "extrude", "push/pull"],
            "scale_tool": ["scale tool", "scaling", "resize"],
            "offset_tool": ["offset tool", "offsetting", "parallel lines"],
            "tape_measure": ["tape measure", "measuring", "dimensions"],
            "section_plane": ["section plane", "section cut", "section view"]
        }
    
    def find_tool_content(self) -> Dict[str, List[Path]]:
        """Find files containing tool-specific content"""
        tool_files = {tool: [] for tool in self.tool_keywords.keys()}
        
        # Search through all categorized files
        for qa_file in self.categorized_dir.rglob("categorized_QnAs.md"):
            try:
                with open(qa_file, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                
                # Check which tool keywords are present
                for tool, keywords in self.tool_keywords.items():
                    if any(keyword in content for keyword in keywords):
                        tool_files[tool].append(qa_file)
            except Exception as e:
                print(f"Error reading {qa_file}: {e}")
        
        return tool_files
    
    def move_files_to_tool_directories(self, tool_files: Dict[str, List[Path]]):
        """Move files to their proper tool directories"""
        for tool, files in tool_files.items():
            if not files:
                continue
                
            print(f"\n🔧 Processing {tool}: {len(files)} files")
            
            for file_path in files:
                # Determine the correct platform directory
                platform_dir = self._get_platform_directory(file_path)
                if not platform_dir:
                    continue
                
                # Create target path in the proper tool directory
                target_path = platform_dir / "Drawing_and_Modeling_Tools" / tool / file_path.name
                target_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Move the file
                if file_path != target_path:
                    try:
                        shutil.move(str(file_path), str(target_path))
                        print(f"   📁 Moved: {file_path.name} -> {tool}/")
                    except Exception as e:
                        print(f"   ❌ Error moving {file_path.name}: {e}")
    
    def _get_platform_directory(self, file_path: Path) -> Path:
        """Get the platform directory from the file path"""
        parts = file_path.parts
        
        # Look for platform directories in the path
        for i, part in enumerate(parts):
            if part in ["SketchUp_Pro_(Desktop)", "SketchUp_for_Desktop", "LayOut_(Documentation_Tool)", 
                       "SketchUp_Go_(iPad", "SketchUp_Studio_Professional_Suite", "SketchUp_Web_Browser_based"]:
                return Path(*parts[:i+1])
        
        return None
    
    def cleanup_enhanced_directories(self):
        """Remove directories created by the enhanced categorizer"""
        enhanced_dirs = [
            "SketchUp_Pro_Desktop",
            "LayOut", 
            "SketchUp_Studio",
            "SketchUp_Web"
        ]
        
        print("\n🧹 Cleaning up enhanced categorizer directories...")
        
        for dir_name in enhanced_dirs:
            dir_path = self.categorized_dir / dir_name
            if dir_path.exists():
                try:
                    shutil.rmtree(dir_path)
                    print(f"   🗑️  Removed: {dir_name}")
                except Exception as e:
                    print(f"   ❌ Error removing {dir_name}: {e}")
    
    def fix_categorization(self):
        """Main function to fix tool categorization"""
        print("🔧 Starting tool categorization fix...")
        
        # Find tool-specific content
        tool_files = self.find_tool_content()
        
        # Print summary
        print("\n📊 Found tool-specific content:")
        for tool, files in tool_files.items():
            if files:
                print(f"   {tool}: {len(files)} files")
        
        # Move files to proper tool directories
        self.move_files_to_tool_directories(tool_files)
        
        # Clean up enhanced directories
        self.cleanup_enhanced_directories()
        
        print("\n✅ Tool categorization fix complete!")

def main():
    """Main function"""
    fixer = ToolCategorizationFixer()
    fixer.fix_categorization()

if __name__ == "__main__":
    main() 