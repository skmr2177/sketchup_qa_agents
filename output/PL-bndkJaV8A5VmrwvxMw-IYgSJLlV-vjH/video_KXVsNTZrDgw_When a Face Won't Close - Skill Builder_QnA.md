# Q&A for When a Face Won't Close - Skill Builder

### 1. What is the main problem this tutorial addresses?

**A:** This tutorial addresses the common issue where you have a set of lines that should form a closed face, but when you try to connect them, no face appears. Aaron explores six realistic scenarios that can cause this problem and provides solutions for each.

### 2. What is the normal behavior when lines should form a face?

**A:** When lines properly close to form a face, a face should automatically appear. Aaron demonstrates this with three lines that form a rectangle - when he draws the fourth line connecting the two ends, a face immediately shows up, which is the expected behavior.

### 3. What is the first common reason why a face won't close?

**A:** The first common reason is gaps in the lines. Even tiny gaps can prevent a face from forming. Aaron shows an example where there's a small gap in one corner that prevents the rectangle from closing, even though the lines appear to be connected.

### 4. How does SketchUp handle points that are close but not exactly connected?

**A:** SketchUp doesn't round or guess when points are close - it requires exact connections. While SketchUp does have some tolerance for very small gaps, if points are snapped to different locations and don't connect properly, the face won't close.

### 5. What is the second problem that prevents faces from closing?

**A:** The second problem is loose geometry coming into the plane. If you have any lines that come into the area but don't go back out, it prevents the formation of a closed shape. Aaron demonstrates this with a line that enters the rectangle but doesn't exit.

### 6. How can you check for loose geometry in your model?

**A:** You can check for loose geometry by doing a group select of the area. If there's loose geometry, it will show up in the Entity Info panel. Aaron shows an example where the Entity Info shows "four edges" when there should only be three, indicating there's extra geometry.

### 7. What is the third problem related to hidden geometry?

**A:** The third problem is hidden geometry that interferes with face formation. This often happens when you've worked and reworked a model, smoothed geometry, deleted parts, and drawn over that geometry. Hidden lines can prevent faces from closing even though they're not visible.

### 8. How do you access and work with hidden geometry?

**A:** You can access hidden geometry by going to View and turning on "Hidden Geometry." This will show all the hidden lines and edges that might be interfering with face formation. Aaron shows how turning on hidden geometry reveals problematic lines that need to be deleted.

### 9. What is the fourth problem related to geometry being out of plane?

**A:** The fourth problem is when geometry is slightly out of plane. Even tiny deviations in the Z-axis can prevent faces from forming. Aaron demonstrates this with a rectangle where one corner is slightly higher than the others, preventing the face from closing.

### 10. How can you identify if geometry is out of plane?

**A:** You can identify out-of-plane geometry by checking the coordinates of each point. Aaron shows how to look at the X, Y, and Z coordinates of each corner to see if they're all at the same height. If one point is at a different Z-coordinate, that's the problem.

### 11. What is a quick test to see if geometry is out of plane?

**A:** A quick test is to try "stitching" - connect corner to corner with a line. If it closes when you add the line but disappears when you delete it, that's an indicator that you have an out-of-plane problem.

### 12. How do you fix out-of-plane geometry?

**A:** To fix out-of-plane geometry, use the Move tool to grab the problematic point and move it vertically to the same height as the other points. Once all points are at the same Z-coordinate, the face should close properly.

### 13. What is the fifth problem related to hidden tags?

**A:** The fifth problem is geometry on hidden tags. Even if you can't see the geometry, if it's on a hidden tag, it can still interfere with face formation. This is different from hidden geometry - it's geometry that's hidden because its tag is turned off.

### 14. How do you check for geometry on hidden tags?

**A:** You can check for geometry on hidden tags by going to the Tags panel and looking for hidden tags. Aaron shows an example where there's a line on a hidden tag that's preventing the face from closing, even though the line isn't visible.

### 15. What is the sixth problem related to groups?

**A:** The sixth problem is when the lines you're trying to connect are inside a group. If you're trying to draw a line outside the group to connect lines that are inside the group, it won't work because you can't interact with geometry inside a container.

### 16. How can you tell if lines are inside a group?

**A:** You can tell if lines are inside a group by clicking on them - if you click one line and it all lights up, or if you see a flickering line, that's often an indicator. The Entity Info panel will also show that it's a group.

### 17. What are the two ways to fix the group problem?

**A:** The two ways to fix the group problem are: 1) Right-click and explode the group to get the lines out, or 2) Double-click to enter the group and then draw your line inside the group where the other lines are located.

### 18. Why is it important to understand these different problems?

**A:** Understanding these different problems is important because each requires a different solution. If you don't know what's causing the face not to close, you might waste time trying the wrong fixes. Aaron provides a systematic approach to diagnose and solve each type of problem.

### 19. What is the systematic approach to troubleshooting face closure issues?

**A:** The systematic approach is: 1) Check for gaps in the lines, 2) Look for loose geometry coming into the plane, 3) Check for hidden geometry, 4) Verify that all points are in the same plane, 5) Check for geometry on hidden tags, 6) Determine if the lines are inside a group.

### 20. How does Aaron demonstrate the importance of exact connections?

**A:** Aaron demonstrates this by showing that even small gaps prevent face formation. He emphasizes that SketchUp doesn't guess or round - it requires exact connections between points for faces to form properly.

### 21. What is the difference between hidden geometry and geometry on hidden tags?

**A:** Hidden geometry refers to lines and edges that are hidden because they were created during modeling operations (like smoothing) but aren't visible. Geometry on hidden tags refers to visible geometry that's hidden because its tag/layer is turned off. Both can interfere with face formation.

### 22. How does Aaron show the relationship between Entity Info and troubleshooting?

**A:** Aaron shows how the Entity Info panel can help diagnose problems. For example, if you select an area that should have three edges but Entity Info shows four edges, that indicates there's extra geometry that needs to be found and removed.

### 23. What is the significance of the "stitching" test?

**A:** The stitching test (connecting corner to corner) is a quick diagnostic tool. If adding a line makes the face appear but deleting it makes it disappear, this indicates an out-of-plane problem rather than a missing line problem.

### 24. How does Aaron emphasize the importance of checking multiple potential causes?

**A:** Aaron shows that you need to check multiple potential causes systematically. Just because one solution doesn't work doesn't mean the problem is unsolvable - you need to go through the list of possible causes to find the right one.

### 25. What is the overall lesson about SketchUp's precision requirements?

**A:** The overall lesson is that SketchUp requires precise geometry for faces to form. Whether it's exact connections, proper plane alignment, or clean geometry without interference, SketchUp doesn't make assumptions or approximations - it needs everything to be exactly right for faces to close properly.