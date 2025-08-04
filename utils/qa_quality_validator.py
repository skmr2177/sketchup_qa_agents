#!/usr/bin/env python3
"""
QA Quality Validator
Detects and flags generic answers in Q&A files
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Tuple

class QAQualityValidator:
    def __init__(self):
        self.generic_patterns = self._load_generic_patterns()
        self.tutorial_specific_indicators = self._load_specific_indicators()
    
    def _load_generic_patterns(self) -> List[str]:
        """Load patterns that indicate generic answers"""
        return [
            r"The Move Tool serves multiple purposes in this tutorial:",
            r"• Primary Function: Perform move tool operations",
            r"• Key Applications: Creating precise geometric shapes",
            r"• Advanced Uses: Complex modeling operations",
            r"• Integration: Working with other tools and features",
            r"Step-by-step Usage:",
            r"The tool serves multiple purposes",
            r"Perform tool operations",
            r"Creating precise geometric shapes",
            r"Complex modeling operations",
            r"Working with other tools and features",
            r"The \w+ Tool serves multiple purposes",
            r"Primary Function: Perform \w+ tool operations",
            r"Key Applications: Creating precise geometric shapes",
            r"Advanced Uses: Complex modeling operations",
            r"Integration: Working with other tools and features"
        ]
    
    def _load_specific_indicators(self) -> List[str]:
        """Load patterns that indicate tutorial-specific content"""
        return [
            r"in this tutorial",
            r"the instructor",
            r"demonstrates",
            r"shows",
            r"creates",
            r"builds",
            r"uses the",
            r"applies",
            r"positions",
            r"moves",
            r"rotates",
            r"scales",
            r"specific",
            r"example",
            r"technique",
            r"method",
            r"approach",
            r"workflow",
            r"process",
            r"step by step"
        ]
    
    def analyze_qa_file(self, file_path: Path) -> Dict:
        """Analyze a single Q&A file for quality issues"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {"error": str(e)}
        
        # Extract Q&A pairs
        qa_pairs = self._extract_qa_pairs(content)
        
        analysis = {
            "file_path": str(file_path),
            "total_qa_pairs": len(qa_pairs),
            "generic_answers": [],
            "specific_answers": [],
            "quality_score": 0.0,
            "issues": []
        }
        
        for i, (question, answer) in enumerate(qa_pairs):
            qa_analysis = self._analyze_single_qa(question, answer, i+1)
            
            if qa_analysis["is_generic"]:
                analysis["generic_answers"].append(qa_analysis)
                analysis["issues"].append(f"QA #{i+1}: Generic answer detected")
            else:
                analysis["specific_answers"].append(qa_analysis)
        
        # Calculate quality score
        if analysis["total_qa_pairs"] > 0:
            analysis["quality_score"] = len(analysis["specific_answers"]) / analysis["total_qa_pairs"]
        
        return analysis
    
    def _extract_qa_pairs(self, content: str) -> List[Tuple[str, str]]:
        """Extract Q&A pairs from content"""
        qa_pairs = []
        
        # Pattern for numbered questions: "1. Question text\nAnswer:\nAnswer text"
        qa_pattern = r'(\d+)\.\s*(.+?)\nAnswer:\s*\n(.+?)(?=\n\n\d+\.|\n\n---|\n\n## Q:|$)'
        qa_matches = re.findall(qa_pattern, content, re.DOTALL)
        
        for number, question, answer in qa_matches:
            question = question.strip()
            answer = answer.strip()
            if question and answer and len(answer) > 10:
                qa_pairs.append((question, answer))
        
        # If no numbered format found, try the ## Q: format
        if not qa_pairs:
            qa_pattern = r'## Q: (.+?)\n\n\*\*A:\*\* Answer:\n(.+?)(?=\n\n---|\n\n## Q:|$)'
            qa_matches = re.findall(qa_pattern, content, re.DOTALL)
            
            for question, answer in qa_matches:
                question = question.strip()
                answer = answer.strip()
                if question and answer and len(answer) > 10:
                    qa_pairs.append((question, answer))
        
        return qa_pairs
    
    def _analyze_single_qa(self, question: str, answer: str, qa_number: int) -> Dict:
        """Analyze a single Q&A pair"""
        analysis = {
            "qa_number": qa_number,
            "question": question,
            "answer": answer,
            "is_generic": False,
            "generic_phrases_found": [],
            "specific_indicators_found": [],
            "confidence": 0.0
        }
        
        # Check for generic patterns
        answer_lower = answer.lower()
        for pattern in self.generic_patterns:
            if re.search(pattern, answer_lower):
                analysis["generic_phrases_found"].append(pattern)
        
        # Check for specific indicators
        for indicator in self.tutorial_specific_indicators:
            if re.search(indicator, answer_lower):
                analysis["specific_indicators_found"].append(indicator)
        
        # Determine if answer is generic
        generic_score = len(analysis["generic_phrases_found"])
        specific_score = len(analysis["specific_indicators_found"])
        
        # If more than 2 generic phrases and fewer than 2 specific indicators
        if generic_score >= 2 and specific_score < 2:
            analysis["is_generic"] = True
        
        # Calculate confidence (higher is better)
        analysis["confidence"] = specific_score / max(generic_score + 1, 1)
        
        return analysis
    
    def validate_all_qa_files(self, base_dir: str = "output") -> Dict:
        """Validate all Q&A files in the output directory"""
        base_path = Path(base_dir)
        all_qa_files = []
        
        # Find all Q&A files
        for qa_file in base_path.rglob("*_QnA.md"):
            all_qa_files.append(qa_file)
        
        print(f"🔍 Found {len(all_qa_files)} Q&A files to validate")
        
        results = {
            "total_files": len(all_qa_files),
            "files_with_issues": 0,
            "total_qa_pairs": 0,
            "generic_qa_pairs": 0,
            "quality_scores": [],
            "file_analyses": [],
            "summary": {}
        }
        
        for qa_file in all_qa_files:
            print(f"📄 Analyzing: {qa_file.name}")
            analysis = self.analyze_qa_file(qa_file)
            
            if "error" not in analysis:
                results["file_analyses"].append(analysis)
                results["total_qa_pairs"] += analysis["total_qa_pairs"]
                results["generic_qa_pairs"] += len(analysis["generic_answers"])
                results["quality_scores"].append(analysis["quality_score"])
                
                if analysis["issues"]:
                    results["files_with_issues"] += 1
        
        # Generate summary
        if results["quality_scores"]:
            results["summary"] = {
                "average_quality_score": sum(results["quality_scores"]) / len(results["quality_scores"]),
                "files_with_quality_issues": results["files_with_issues"],
                "percentage_generic_answers": (results["generic_qa_pairs"] / max(results["total_qa_pairs"], 1)) * 100,
                "recommendations": self._generate_recommendations(results)
            }
        
        return results
    
    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate recommendations based on analysis results"""
        recommendations = []
        
        avg_quality = results["summary"]["average_quality_score"]
        generic_percentage = results["summary"]["percentage_generic_answers"]
        
        if avg_quality < 0.7:
            recommendations.append("Quality score is low. Consider regenerating Q&A pairs with more specific prompts.")
        
        if generic_percentage > 20:
            recommendations.append("High percentage of generic answers detected. Review and regenerate affected files.")
        
        if results["files_with_issues"] > 0:
            recommendations.append(f"{results['files_with_issues']} files have quality issues that need attention.")
        
        if not recommendations:
            recommendations.append("Overall quality is good. Continue monitoring for new issues.")
        
        return recommendations
    
    def generate_validation_report(self, results: Dict, output_file: str = "qa_quality_report.md"):
        """Generate a detailed validation report"""
        report_content = f"""# Q&A Quality Validation Report

Generated on: {Path().cwd()}

## Summary

- **Total Q&A files analyzed**: {results['total_files']}
- **Files with quality issues**: {results['files_with_issues']}
- **Total Q&A pairs**: {results['total_qa_pairs']}
- **Generic Q&A pairs detected**: {results['generic_qa_pairs']}
- **Average quality score**: {results['summary'].get('average_quality_score', 0):.2f}
- **Percentage of generic answers**: {results['summary'].get('percentage_generic_answers', 0):.1f}%

## Recommendations

"""
        
        for rec in results['summary'].get('recommendations', []):
            report_content += f"- {rec}\n"
        
        report_content += "\n## Detailed Analysis\n\n"
        
        # Files with issues
        if results['files_with_issues'] > 0:
            report_content += "### Files with Quality Issues\n\n"
            for analysis in results['file_analyses']:
                if analysis['issues']:
                    report_content += f"#### {Path(analysis['file_path']).name}\n"
                    report_content += f"- Quality Score: {analysis['quality_score']:.2f}\n"
                    report_content += f"- Issues: {len(analysis['issues'])}\n"
                    for issue in analysis['issues']:
                        report_content += f"  - {issue}\n"
                    report_content += "\n"
        
        # Top quality files
        high_quality_files = [a for a in results['file_analyses'] if a['quality_score'] > 0.8]
        if high_quality_files:
            report_content += "### High Quality Files (Score > 0.8)\n\n"
            for analysis in sorted(high_quality_files, key=lambda x: x['quality_score'], reverse=True)[:10]:
                report_content += f"- {Path(analysis['file_path']).name}: {analysis['quality_score']:.2f}\n"
            report_content += "\n"
        
        # Save report
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"📄 Quality report generated: {output_file}")
        return output_file

def main():
    """Main function to run quality validation"""
    validator = QAQualityValidator()
    results = validator.validate_all_qa_files()
    
    print(f"\n📊 Validation Results:")
    print(f"   Total files: {results['total_files']}")
    print(f"   Files with issues: {results['files_with_issues']}")
    print(f"   Total Q&A pairs: {results['total_qa_pairs']}")
    print(f"   Generic Q&A pairs: {results['generic_qa_pairs']}")
    print(f"   Average quality score: {results['summary'].get('average_quality_score', 0):.2f}")
    
    # Generate report
    validator.generate_validation_report(results)

if __name__ == "__main__":
    main() 