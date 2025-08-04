# Q&A for Import and Cleanup CAD Files in SketchUp

### 1. What is the main focus of this tutorial and what does Eric plan to cover?

**A:** Eric plans to go **"Beyond SketchUp desktop"** to work with imported CAD files and look at extensions that make working with CAD files easier. He acknowledges that CAD file quality depends on how well they were drafted, and there's always some work needed in SketchUp to get them working efficiently. The tutorial covers both importing/organizing CAD files and making the 2D to 3D transition more efficient.

### 2. What does Eric say about the best approach for CAD files and when this might not be possible?

**A:** Eric normally says that **"the best thing you can do is get all your drafting done perfectly in CAD before you import it into SketchUp"**, but he acknowledges that if the CAD file comes from somebody else like a consultant or team member, that may be outside of your hands. This is why he focuses on techniques to work with imperfect CAD files.

### 3. What is the first step Eric takes after importing the CAD file?

**A:** Eric starts by **creating a drafting environment that mimics CAD**. He sets the standard view to top and switches to parallel projection, just like in CAD where you're drafting straight down. He also turns off the axis and changes the style to better see what he's working with.

### 4. How does Eric use the Styles panel to better understand the imported CAD file?

**A:** Eric uses the **"Color by Material"** option in the Styles panel to see the original CAD colors. This shows him that the road would be yellow and road center lines would be blue, revealing the color information that came from CAD. He also uses "Color by Tag Override" so that any faces created will also change to the same color.

### 5. What does Eric do to create a CAD-like working environment?

**A:** Eric creates a **new style called "CAD"** and saves it as a scene. He turns off the sky and changes the background color to charcoal gray or black, something you would expect to see in a CAD drafting environment. This makes it feel like he's still working in CAD and helps him see the line work better.

### 6. Why does Eric explode everything that came in from the CAD file?

**A:** Eric explodes everything because he **doesn't know how it was organized** - there were some groups but no blocks or components. He needs to reorganize it himself. He's careful to note that he's doing this intentionally and reminds viewers to be cautious when exploding things, but in this case it's necessary for reorganization.

### 7. How does Eric use the tag information from the CAD file to his advantage?

**A:** Eric uses the fact that **the raw geometry retains the layer information** from AutoCAD - the AutoCAD layer is translated to a SketchUp tag. So "L-site" was basically the drafting layer. Even though lines may be overlapping, they retain their tag information, which Eric uses to select all geometry on the same tag and group it together.

### 8. What is Eric's approach to organizing the exploded CAD geometry?

**A:** Eric **selects all geometry on the same tag** and makes it a group. This protects that geometry so he can start filling in faces and extruding without affecting other elements. He then moves all the geometry inside the group from the original tag (like "L-site") to "Untagged" and puts the group itself on a new SketchUp tag.

### 9. What naming convention does Eric use for his SketchUp tags and why?

**A:** Eric uses an **"S" prefix** (like "S-Building" instead of "L-site") as a reminder that he's moving from CAD to SketchUp. The "S" prefix means he's transitioning from 2D CAD to 3D SketchUp. He notes you don't have to use this convention, but it helps him remember which elements are ready to go 3D.

### 10. What shortcut does Eric show for dealing with tags after grouping?

**A:** Eric shows a **shortcut** where you can just delete the original tag (like "L-Contour") after you've grouped everything, and it will automatically assign all the geometry inside the group to "Untagged." This is faster than going into the group and manually selecting all the geometry to move it to Untagged.

### 11. What are the two extensions Eric introduces for working with CAD files?

**A:** Eric introduces two extensions by **ThomThom**: **"Flatten to Plane"** and **"Face Creator"**. Flatten to Plane takes everything that may be at different elevations and brings it back down to the same elevation. Face Creator automatically creates faces from the geometry.

### 12. Why is the Flatten to Plane extension important when working with CAD files?

**A:** **Flatten to Plane** is important because CAD files often have geometry at different elevations (like contours from engineers that come in 3D space). If you accidentally snap a line to a contour, it might look perfect in plan view but won't create faces properly. Flatten to Plane brings everything to the same elevation so faces can be created correctly.

### 13. How does Eric demonstrate the problem with elevation differences in CAD files?

**A:** Eric shows that when he switches to **elevation view**, you can see that contours and buildings are actually sitting in 3D space. It's easy to accidentally snap a line to a contour, which would make it look perfect in plan view but prevent faces from being created. This is why Flatten to Plane is necessary.

### 14. What is the workflow Eric demonstrates for creating faces from CAD geometry?

**A:** The workflow is: **1) Organize geometry by grouping elements on the same tag, 2) Use Flatten to Plane to bring everything to the same elevation, 3) Use Face Creator to automatically create faces from the geometry.** This makes the transition from 2D CAD to 3D SketchUp much more efficient.

### 15. How does Eric use scenes to switch between different working modes?

**A:** Eric creates **two scenes**: one called "CAD" for the drafting environment and another called "SketchUp" for the 3D working environment. This allows him to switch back and forth between CAD view (to check organization and tags) and SketchUp view (to see faces and work in 3D).

### 16. What does Eric say about the importance of proper organization when working with CAD files?

**A:** Eric emphasizes that **proper organization is crucial** because it protects geometry and makes it safe to start filling in faces and extruding. By grouping elements and organizing them on appropriate tags, you can work confidently without accidentally affecting other parts of the model.

### 17. How does Eric handle the visual feedback during the CAD cleanup process?

**A:** Eric uses **color coding** to provide visual feedback - he makes untagged geometry orange as a warning, and uses the original CAD colors to understand what each element represents. This helps him quickly identify what's been processed and what still needs work.

### 18. What does Eric recommend for users who want to learn more about CAD to SketchUp workflow?

**A:** Eric plugs the **SketchUp Campus course** at learn.sketchup.com, which covers "Three Ways to Boost Your CAD to SketchUp Workflow." He mentions that the course covers the tips he demonstrated more slowly, provides exercise files to follow along with, and offers much more detailed information.

### 19. What is Eric's approach to dealing with overlapping or crisscrossing geometry from CAD?

**A:** Eric explains that **overlapping geometry is okay** when working with CAD files because the tag information is preserved. Even if lines are crisscrossing or overlapping, you can select all geometry on the same tag and group it together. The tag information helps you organize the geometry properly.

### 20. How does Eric demonstrate the difference between CAD and SketchUp working environments?

**A:** Eric shows the difference by **switching between scenes** - the CAD scene has a dark background, parallel projection, and shows the original CAD colors, while the SketchUp scene has a lighter background, perspective view, and shows the faces that have been created. This helps him work efficiently in both modes.

### 21. What keyboard shortcuts does Eric mention for speeding up the process?

**A:** Eric mentions using **keyboard shortcuts** to speed up the selection and grouping process, though he doesn't specify which ones. He emphasizes that using shortcuts makes the reorganization process much faster when working with large CAD files.

### 22. How does Eric handle the transition from 2D CAD geometry to 3D SketchUp models?

**A:** Eric's approach is to **first organize and clean up the 2D geometry** by grouping elements, flattening elevations, and creating faces. Once this is done, it becomes easy to extrude the buildings and move on to the next piece of the puzzle. The key is getting the 2D foundation right before moving to 3D.

### 23. What does Eric say about the importance of checking geometry before creating faces?

**A:** Eric emphasizes **double-checking geometry** before creating faces, especially when working with CAD files that might have elevation differences. He shows how Flatten to Plane helps identify and fix these issues, ensuring that faces can be created properly.

### 24. How does Eric use the Entity Info panel in his workflow?

**A:** Eric mentions that you could use the **Entity Info panel** to look at what tag something is on, but he notes that this is time-consuming, especially if you have a lot of layers. Instead, he uses the visual approach with the Styles panel to quickly see tag information through colors.

### 25. What is Eric's final recommendation for viewers who want to improve their CAD to SketchUp workflow?

**A:** Eric recommends **enrolling in the free SketchUp Campus course** at learn.sketchup.com, which provides more detailed instruction on CAD to SketchUp workflows. He also encourages viewers to like, comment, and subscribe to help them make better videos, and asks for feedback on what they learned.

This comprehensive Q&A covers the complete CAD Import and Cleanup tutorial, including specific techniques for organizing CAD files, using extensions, and transitioning from 2D to 3D modeling in SketchUp.