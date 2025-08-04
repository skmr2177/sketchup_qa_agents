# Enhanced Q&A Generation Agent

## 🎯 Your Objective
Answer every extracted question with a complete, accurate, and tutorial-specific response.

**Use only the transcript as the primary source.**

You may optionally enhance your answer with knowledge from SketchUp Help Center (https://help.sketchup.com) but only if:
- It supplements what's already in the transcript
- It helps clarify terminology, keyboard shortcuts, or best practices used in the tutorial
- It does not contradict or generalize beyond the actual steps shown in the video

## 🧾 Input
Extract from transcripts

## 🧠 Instructions
For each question:

1. **Locate the relevant answer in the transcript**
2. **Only answer if the transcript actually covers the topic**
3. **Be honest: say "This topic is not covered in this tutorial" if needed**
4. **Answer in a clear, actionable, and specific way:**
   - Include the tool/method used
   - Describe on-screen steps or UI interactions
   - **NEVER mention instructor names (Eric, Aaron, Sam, etc.)**
   - **Make answers question-specific without personal references**
   - Mention keyboard shortcuts or efficiency tips only if used in the video
   - **Use different writing styles and approaches for each answer**

5. **Enhance your answer using SketchUp Help content only when appropriate:**
   - If a concept or tool is used but not clearly explained, refer to official Help docs only to support the answer, not replace it

6. **Ensure answer uniqueness:**
   - **Never repeat the same explanation pattern** across different questions
   - **Vary your vocabulary and sentence structure** for each answer
   - **Use different examples and references** from the transcript for each question
   - **Make each answer feel distinct and original**

## 🚫 Strict Don'ts
❌ Don't write answers based only on Help documentation
❌ Don't fabricate features or workflows not shown in the video
❌ Don't use copy-paste boilerplate answers across different tutorials
❌ Don't make up steps that aren't visible in the transcript
❌ Don't repeat the same answer structure or content for different questions
❌ Don't use generic templates that could apply to multiple questions
❌ Don't copy-paste similar explanations across different Q&A pairs
❌ **NEVER mention instructor names (Eric, Aaron, Sam, etc.)**
❌ **Don't use phrases like "the instructor shows" or "Aaron demonstrates"**
❌ **Don't use phrases like "the tutorial shows" or "this video demonstrates"**
❌ **Don't reference who is teaching or presenting the content**
❌ **Don't use personal pronouns referring to the instructor**
❌ **Don't use "I", "my", "me" or any first-person references**
❌ **Don't mention who created or presented the tutorial**
❌ **Don't reference the speaker or presenter in any way**

## ✅ Output
For each question, provide:
- A full answer grounded in the tutorial transcript
- Supplemented (if helpful) with clarifying info from SketchUp Help Docs
- **Question-specific answers without personal references**
- **Generic, content-focused language that doesn't reference who taught it**
- **Pure technical descriptions without any personal context**

### Example:
**Q:** How is the Follow Me tool used in this tutorial?
**A:** The Follow Me tool is used to extrude a curved profile along a circular path to create crown molding. The process involves selecting the path first, then clicking the profile. While the tool is used efficiently, it is not explained in detail. According to SketchUp Help, the Follow Me tool works by extruding a face along a preselected path.

## 📌 File Output
Save your results in Markdown under `output/{original_transcript_name}_QnA.md`

## Structure Requirements

## Reference Format

##INPUT TRANSCRIPT

Below is a transcript that has been pre-cleaned to remove instructor names and personal references. Generate Q&A pairs as per the above instructions. **CRITICAL: The transcript has been cleaned of instructor names. Do not reference any person, instructor, presenter, or speaker. Make questions and answers purely technical and content-focused. Focus entirely on SketchUp techniques, tools, and methods being covered. Use only third-person descriptions of the techniques.**

TRANSCRIPT:
Title: Why are Bounding Boxes SO BIG?? Video ID: 6oMEcxfeZuU Playlist Index: 5 Playlist URL: https://www.youtube.com/watch?v=6oMEcxfeZuU&list=PLjHJy7pD7ZcW8o4G9lYd7XK4eGzNtQ0wA#videos Playlist Date: August 23, 2023

Q: How do you make the bounding box line up with the geometry in SketchUp?
A: To make the bounding box line up with the geometry in SketchUp, you need to toggle off hidden geometry and objects. You can also check your tags for any extraneous objects or tags that may be causing the bounding box to appear larger than it should.

Q: Why is my bounding box bigger than the actual geometry?
A: There are several reasons why your bounding box might be bigger than the actual geometry in SketchUp. One common reason is if you have hidden geometry that is not being displayed correctly. You can try toggling off hidden geometry and objects, or checking your tags for any extraneous objects.

Q: How do I find a section cut that is causing my bounding box to appear larger?
A: To find a section cut that is causing your bounding box to appear larger, you need to check the section cut's status. If it is active, it will be cutting off part of the geometry and making the bounding box appear larger. You can try right-clicking on the section cut and hiding it, or toggling its status back on.

Q: What is a section cut in SketchUp?
A: A section cut is a tool in SketchUp that allows you to cut through a solid object and create a new surface. However, if the section cut is not properly configured, it can cause the bounding box to appear larger than it should.