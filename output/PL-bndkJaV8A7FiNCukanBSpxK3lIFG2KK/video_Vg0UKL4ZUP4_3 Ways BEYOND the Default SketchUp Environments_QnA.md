# Q&A for 3 Ways BEYOND the Default SketchUp Environments

### 1. What are environments in SketchUp 2025 and what do they provide?

**A:** Environments were introduced in SketchUp 2025 to provide image-based lighting for PBR (physically-based rendered) materials. They offer unique looks that weren't accessible to SketchUp visualizations before, allowing users to create custom lighting and background effects for their models.

### 2. How do you access the default environments in SketchUp?

**A:** You can access default environments by going to the Environments panel and using the environments dropdown. SketchUp ships with several pre-made environments that can also be found on the 3D Warehouse. As you change between different environments, you can see how the look and color of materials changes.

### 3. What is Poly Haven and how can it be used for custom environments?

**A:** Poly Haven is a free asset library website that provides HDRIs (High Dynamic Range Images). Under the "Assets" section, you can find HDRIs that SketchUp can import as EXR and HDR files for SkyDome image-based lighting. The site offers various environments in different resolutions (2K, 4K, 8K, etc.).

### 4. What file formats does SketchUp support for custom environments?

**A:** SketchUp supports both HDR and EXR file formats for custom environments. These are high dynamic range image formats that provide the lighting information needed for realistic image-based lighting in your models.

### 5. How do you import a custom environment into SketchUp?

**A:** To import a custom environment, click the plus button in the Environments panel. This will open a file browser where you can select your downloaded environment file (HDR or EXR). Once selected, it will instantly populate and you can see the effect on your model.

### 6. What is the "Set Sun Location" feature and why is it important?

**A:** The "Set Sun Location" feature allows you to position the sun to match the lighting in your custom environment. When you check this box, you get a sun control that you can move around, and the shadows will update to match. This ensures that reflections in your model accurately reflect the sun location that will also show up in the shadows.

### 7. How can you adjust the brightness of a custom environment?

**A:** You can adjust the brightness of a custom environment using the exposure slider in the Environments panel. This allows you to make the environment brighter or darker to match your desired lighting conditions.

### 8. What is the second method for creating custom environments using stock images?

**A:** The second method involves using stock image websites to find suitable background images. You can search for terms like "HDR studio background" to find images that can be converted for use as environments. This method is useful when you want a very clean, specific look that isn't available in HDR libraries.

### 9. What is the process for converting a JPEG to an HDR file for SketchUp?

**A:** To convert a JPEG to an HDR file: 1) Open the JPEG in Photoshop (or any photo editing software), 2) Change the mode from 8-bit to 32 bits per channel, 3) Ensure the image is in RGB color (not grayscale), 4) Save as an EXR file with appropriate compression to manage file size.

### 10. Why is file size important when working with custom environments?

**A:** File size is important because large environment files can slow down your SketchUp model. Matt shows that a 256MB file is too large and not practical, while files around 4-10MB (similar to SketchUp's default environments) work well. You can use compression options like zlib to reduce file size while maintaining quality.

### 11. What is the difference between using an environment as a SkyDome versus just a background?

**A:** When used as a SkyDome, the environment provides both lighting and background. When you turn off the SkyDome option, the environment only serves as a background image. This is useful when you want the lighting effect but prefer a different background appearance.

### 12. How can you rotate a custom environment to get the desired look?

**A:** You can use the rotation angle control in the Environments panel to rotate the environment until you achieve the desired look. This allows you to position the background elements exactly where you want them in relation to your model.

### 13. What is the third method for creating custom environments?

**A:** The third method is creating your own HDR environment using specialized apps. Matt demonstrates using an app called "HDReye" on an iPad, which allows you to capture multiple exposures at different points around a circle to create a complete 360-degree environment.

### 14. How does the HDReye app work for creating custom environments?

**A:** HDReye works by having you hover over dots in a circle around your location. It takes multiple exposures at each point and then stitches all the images together to create an EXR file that can be downloaded and used in SketchUp.

### 15. What are the considerations when creating your own HDR environment?

**A:** When creating your own HDR environment, consider: 1) Choose a day with good lighting and dynamic range (sunny days with cloud variation work best), 2) The resulting file will likely be very large and may need compression, 3) You may need to adjust brightness in post-processing, 4) The perspective won't perfectly match your model since environments are infinitely far away.

### 16. How can you reduce the file size of a custom HDR environment?

**A:** You can reduce file size by: 1) Using compression options like zlib or RLE when saving as EXR, 2) Reducing the resolution of the image, 3) Using photo editing software to optimize the file before importing into SketchUp.

### 17. What is the limitation of using custom environments for perspective matching?

**A:** The limitation is that environments are backgrounds that are infinitely far away, so any perspective in your model won't line up exactly with the environment. You can try adjusting zoom and focal length, but it won't create perfect perspective matching like you might expect.

### 18. How can you align a custom environment with your model?

**A:** You can align a custom environment by using the rotation controls to match key elements. Matt shows aligning with a Calder statue in the background, though he notes it won't be perfect due to the perspective limitations. You could also determine true north and rotate accordingly for exact reflections.

### 19. What is the advantage of using stock images for environments?

**A:** Using stock images allows you to achieve very clean, specific looks that might not be available in HDR libraries. You can find exactly the type of background you want and convert it to work as an environment, giving you more control over the final appearance.

### 20. How can you use environments for animation effects?

**A:** You can animate environments by changing the rotation angle between scenes. This creates the effect of the image-based lighting moving as the camera moves, adding dynamic lighting effects to your animations.

### 21. What is the recommended file size for custom environments?

**A:** Matt recommends keeping custom environment files between 4-10MB, similar to the size of SketchUp's default environments. This provides good quality without significantly slowing down your model performance.

### 22. How do you handle environments that don't tile seamlessly?

**A:** If an environment doesn't tile seamlessly (like some stock images converted to HDR), you can turn off the SkyDome option and use it only as a background. This way you get the lighting effect without the problematic tiling issues.

### 23. What is the benefit of using 32-bit files for environments?

**A:** 32-bit files provide higher dynamic range than 8-bit files, which is essential for HDR environments. This allows for more realistic lighting with greater contrast and detail in both bright and dark areas.

### 24. How can you create a clean, modern look with custom environments?

**A:** You can create a clean, modern look by using simple stock backgrounds, turning off the SkyDome option, and adjusting the exposure and rotation to get a minimalist appearance. This works well for product visualization and architectural presentations.

### 25. What are the three main methods for creating custom environments beyond the defaults?

**A:** The three main methods are: 1) Using free HDR libraries like Poly Haven to download pre-made HDR/EXR files, 2) Converting stock images from websites by changing them from JPEG to EXR format, and 3) Creating your own HDR environments using specialized apps like HDReye to capture real-world locations.