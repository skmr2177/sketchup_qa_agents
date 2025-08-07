# 6Pib8cNsSEE Optimize Your SketchUp Model with One Click! - Q&A

Q1. What is the Cleanup extension and what does it do?
A1. The Cleanup extension, also known as Cleanup3, is a SketchUp extension created by TomTom that helps optimize and clean up SketchUp models with various tools and features. It can merge coplanar faces, remove hidden geometry, purge unused components and materials, repair edges, and perform other optimization tasks with a single click.

Q2. What other extension is required for Cleanup to work?
A2. The Cleanup extension requires the TT Live library extension from TomTom to be installed as well.

Q3. How can you access the Cleanup extension in SketchUp?
A3. You can access the Cleanup extension by going to Extensions > Cleanup in the SketchUp menu. Clicking "Clean..." will open the Cleanup settings dialog box.

Q4. What are the options for selecting the scope of the cleanup operation?
A4. The Cleanup extension offers three options for the scope: Clean the entire model, clean only the local context (group or component), or clean only the selected geometry.

Q5. What does the "Validate results and show statistics" option do?
A5. The "Validate results and show statistics" option displays a summary of the cleanup operations performed, including the number of edges, faces, hidden entities, and materials merged or purged.

Q6. What does the "Purge unused" option do?
A6. The "Purge unused" option removes any unused geometry, materials, or components from the SketchUp model, similar to the regular Purge command.

Q7. What does the "Erase hidden geometry" option do?
A7. The "Erase hidden geometry" option deletes any geometry that is currently hidden in the SketchUp model, regardless of whether it was intended to be used later or not.

Q8. What does the "Erase duplicate faces" option do, and what is the warning associated with it?
A8. The "Erase duplicate faces" option removes any duplicate or overlapping faces in the model. However, the warning associated with this option is that it can be a slow process, especially for complex models.

Q9. What does the "Geometry to layer zero" (or "Geometry to untagged") option do?
A9. This option moves all raw geometry (faces and edges) to the untagged layer (formerly known as layer zero), while groups and components should be on tagged layers.

Q10. What does the "Merge identical materials" option do?
A10. The "Merge identical materials" option combines any duplicate materials in the model into a single instance, reducing file size and redundancy.

Q11. What does the "Merge coplanar faces" option do, and what are the sub-options associated with it?
A11. The "Merge coplanar faces" option merges any coplanar (flat and on the same plane) faces in the model, removing the edges between them. The sub-options allow you to ignore or pay attention to materials or face normals during the merge.

Q12. What does the "Repair split edges" option do?
A12. The "Repair split edges" option fixes any edges in the model that are broken into multiple segments, merging them into a single continuous edge.

Q13. What does the "Erase stray edges" option do?
A13. The "Erase stray edges" option removes any loose or floating edges in the model that are not connected to any faces.

Q14. What does the "Remove edge materials" option do?
A14. The "Remove edge materials" option removes any materials applied to edges in the model, as edge materials are typically unnecessary and can increase file size.

Q15. What does the "Smooth edges" option do, and how can you control the angle threshold?
A15. The "Smooth edges" option automatically applies SketchUp's edge softening/smoothing to edges based on an angle threshold. You can specify the maximum angle (e.g., 30 degrees) for edges to be smoothed.

Q16. In the example model, what types of issues were intentionally introduced to demonstrate the Cleanup extension?
A16. The example model had several intentional issues, including stray edges, hidden geometry, split edges around the outside, materials applied to edges, duplicate materials, duplicate components, and geometry on the wrong layer/tag.

Q17. What happened to the duplicate materials and components after running Cleanup?
A17. After running Cleanup, the duplicate materials and components were purged, leaving only a single instance of each in the model.

Q18. What happened to the materials applied to edges after running Cleanup?
A18. The materials applied to edges were removed, as the styles were set to display all edges in black, regardless of material.

Q19. What happened to the hidden geometry and stray edges after running Cleanup?
A19. The hidden geometry and stray edges were erased from the model.

Q20. What happened to the split edges around the outside of the model after running Cleanup?
A20. The split edges around the outside were repaired and merged into a single continuous edge.

Q21. What happened to the geometry on the wrong layer/tag after running Cleanup?
A21. All geometry was moved to the untagged layer, as per the "Geometry to layer zero" option.

Q22. What is the potential downside of using the Cleanup extension, as mentioned in the video?
A22. The potential downside is that the Cleanup extension performs its operations without discrimination, potentially removing or merging geometry that you may have intended to keep separate or intact. It is described as a "wrecking ball" that does what you tell it to do without question.

Q23. What is the recommended approach if you want to preserve certain geometry or components while running Cleanup?
A23. The recommended approach is to select only the geometry you want to clean up and run Cleanup on the selected geometry, or to run Cleanup on specific groups or components individually, rather than the entire model.

Q24. How can you quickly run Cleanup with the same settings as the previous operation?
A24. If you have already set up the desired Cleanup settings, you can quickly run Cleanup with those same settings by selecting "Clean with last settings" from the Cleanup menu, without having to open the settings dialog again.

Q25. What is the overall purpose and benefit of using the Cleanup extension in SketchUp?
A25. The overall purpose and benefit of using the Cleanup extension is to quickly optimize and clean up SketchUp models by removing unnecessary geometry, materials, components, and other elements that can increase file size and clutter. It helps streamline and optimize models with a single click, improving performance and organization.

---
*Generated: 2025-08-07 15:45:40*
