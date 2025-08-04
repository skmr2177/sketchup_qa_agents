# Q&A for SketchUp Skill Builder: Door and Window Schedule

### 1. What is the main objective of this tutorial on door and window schedules?

**A:** This tutorial demonstrates how to generate a door and window schedule using SketchUp and LayOut. It shows the complete workflow from setting up a model with proper component organization to creating a detailed schedule report and integrating it into LayOut documentation.

### 2. What type of model does Aaron use to demonstrate the door and window schedule process?

**A:** Aaron uses a model with three units - little houses or cabana-type structures. Each unit contains multiple doors and windows, and he shows how to organize these components properly in the Outliner for effective schedule generation.

### 3. How does Aaron organize the components in his model for schedule generation?

**A:** Aaron organizes components hierarchically in the Outliner: the top level contains the entire model, level two contains the main pieces (barbecue, bench, chair, fire pit, table, and the three buildings), and level three contains the doors and windows. This nesting structure is crucial for the reporting process.

### 4. What is the difference between Definition Name and Instance Name in SketchUp components?

**A:** The Definition Name is what SketchUp calls the component (like "Glass Door"), while the Instance Name is what you want to call it in your output (like "D1" or "D2"). The Instance Name is what generates the label in the schedule, and it can be different for the same component definition.

### 5. How does Aaron handle identical components that appear multiple times in the model?

**A:** For identical components that repeat throughout the model, Aaron uses the same Instance Name (like "W4" for the same small window). However, for components that are the same definition but have different orientations (like doors with opposite swings), he uses different Instance Names (like "D1" and "D2").

### 6. What are Advanced Attributes and how are they used in the schedule?

**A:** Advanced Attributes are additional information you can add to components, accessible by clicking the plus sign in the Entity Info panel. They include fields like price, size, URL, owner, status, and IFC type. For the door and window schedule, Aaron populates the size field (like "3068" for a door).

### 7. What scenes does Aaron set up in his model and why?

**A:** Aaron creates two scenes: one is a section cut looking down from above, and the other is a three-quarter view. These scenes are important because they will be referenced in LayOut to create the final documentation with the schedule.

### 8. What is the first step in generating a door and window schedule report?

**A:** The first step is to click "Generate Report" in SketchUp. This opens the report generation interface where you can create a new template and configure the reporting parameters.

### 9. What filtering options are available when generating a report?

**A:** The report generation offers several filtering options: you can report on the entire model or just selected items, and you can filter by nesting level (which level in the Outliner hierarchy to report on). For door and window schedules, Aaron filters to level three where the doors and windows are located.

### 10. How does the nesting level filtering work in report generation?

**A:** Nesting level filtering allows you to specify which level in the Outliner hierarchy to report on. Aaron's model has doors and windows at level three, so he sets the filter to only report on components at that level, automatically excluding other elements like furniture and building structures.

### 11. What information does Aaron include in his door and window schedule?

**A:** Aaron includes the Entity Name (the instance labels like "D1", "W4"), total Quantities (how many of each type), and Size (the dimensions like "3068"). This creates a comprehensive schedule showing what types of doors and windows are used and how many of each.

### 12. How does Aaron save and export the generated schedule?

**A:** After generating the report, Aaron downloads the file and saves it as "MySchedule." This creates a file that can be imported into LayOut as a table for the final documentation.

### 13. What is the workflow for integrating the schedule into LayOut?

**A:** The workflow is: 1) Save the SketchUp model, 2) Send to LayOut, 3) Change the scene to the section cut view, 4) Insert the schedule file as a table, 5) Edit the table headers if needed, 6) Add labels to the drawing by clicking on doors and windows.

### 14. How does Aaron add labels to the doors and windows in LayOut?

**A:** Aaron clicks on each door and window in the LayOut viewport and chooses what information to display. He selects the Component Instance level to show labels like "D2" or "W2". The labels automatically correspond to the schedule table because they're pulling from the same model data.

### 15. What is the advantage of using the section cut scene in LayOut?

**A:** The section cut scene provides a top-down view where you can actually see all the doors and windows clearly. This makes it easier to add labels and reference them to the schedule, as you can see the exact locations and relationships between different elements.

### 16. How does Aaron handle windows that aren't visible in the section cut?

**A:** Aaron demonstrates that you can still label windows that aren't visible in the section cut (like the L-shaped window above the cut) by clicking on their locations. The labels will still correspond to the schedule even if the windows aren't visible in that particular view.

### 17. What is the benefit of creating multiple views with the same schedule?

**A:** Aaron shows that you can create multiple views (like copying the section view and adding a 3D view) and the labels will correspond to the same schedule across all views. This allows you to show different perspectives while maintaining consistent labeling and scheduling.

### 18. How does the Generate Report feature consolidate identical components?

**A:** By filtering by Entity Name (the instance labels), the Generate Report feature consolidates all items with the same label into one line on the output. So all "W4" windows appear as a single entry with the total quantity, rather than listing each individual window separately.

### 19. What is the difference between using nesting level filtering and current selection filtering?

**A:** Nesting level filtering automatically selects all components at a specific level in the Outliner hierarchy, which is efficient if your model is well-organized. Current selection filtering requires you to manually select the items you want to report on, which is useful if your model isn't organized hierarchically or if you want to report on specific items only.

### 20. How does Aaron ensure the schedule labels match the actual components?

**A:** Aaron ensures matching by using the Component Instance names (like "D1", "D2", "W4") consistently. When he clicks on a door or window in LayOut, he selects the same Component Instance level that was used in the schedule generation, ensuring the labels correspond exactly to the schedule entries.

### 21. What is the advantage of using Advanced Attributes for schedule information?

**A:** Advanced Attributes allow you to store specific information (like size, price, status) directly with the components. This information can then be automatically pulled into the schedule, ensuring accuracy and consistency between the model and the documentation.

### 22. How does the table in LayOut relate to the generated schedule?

**A:** The table in LayOut is created by importing the generated schedule file. It shows the same information (Entity Name, Quantity, Size) and is fully editable. You can modify headers, add or remove columns, and the table maintains its connection to the model data.

### 23. What is the benefit of using the same model for both the drawing and the schedule?

**A:** Using the same model ensures that the labels in the drawing automatically correspond to the schedule table. Any changes to the model will be reflected in both the drawing and the schedule, maintaining consistency and reducing the chance of errors.

### 24. How does Aaron handle components that are the same definition but different instances?

**A:** For components that are the same definition but different instances (like doors with opposite swings), Aaron uses different Instance Names ("D1" vs "D2"). This allows the schedule to distinguish between them while still recognizing they're the same type of component.

### 25. What is the overall workflow for creating a complete door and window schedule?

**A:** The complete workflow is: 1) Set up the model with proper component organization and Advanced Attributes, 2) Create scenes for documentation, 3) Generate a report using appropriate filters, 4) Export the schedule file, 5) Send to LayOut, 6) Insert the schedule as a table, 7) Add labels to the drawing by clicking on components, 8) Create multiple views as needed, all maintaining consistency between the model, schedule, and documentation.