# People: What's the right level of detail and style for you?

### 1. What are the three main factors Eric considers when choosing people for his models?
**Answer:**
Eric identifies three key factors: the type of person (whether they're doing an activity, standing, or sitting), level of detail (whether they're 2D or 3D), and stylistically whether they're wearing proper clothes, have the right color, and are engaging with the space appropriately. He emphasizes that "good fit is sort of up to you to determine those parameters" based on your specific project needs and desired aesthetic.

### 2. What are the different types of people available in 3D Warehouse?
**Answer:**
Eric demonstrates three main categories: 2D face-me people (which always face the camera), photographic people (actual photos of people), and fully-fledged 3D people. He shows how searching for "people" in 3D Warehouse yields a variety including silhouettes, face-me components, and 3D models with varying polygon counts. Eric notes that some 3D people can be very high-poly (400,000 polygons) while others are more reasonable (2,000 polygons), so you need to be careful about performance.

### 3. How does Eric customize the appearance of 2D face-me people?
**Answer:**
Eric shows how to customize 2D people by making a copy using the keyboard modifier with the move tool, then making them unique. He applies a charcoal gray color to create a more neutral appearance and sometimes reduces opacity (anything above 70% gives shadows). He demonstrates this by creating both colored and neutral versions of the same person, showing how the neutral version "has a little bit less detail" and creates a more subtle presence in the model.

### 4. What are the advantages and disadvantages of using 3D people versus 2D people?
**Answer:**
3D people offer the advantage of being viewable from any angle - when you rotate around them, they maintain their pose and don't always stare at the camera like 2D face-me people do. They also cast realistic shadows when rendering, with shadows moving under chins and arms as the light source changes. However, 3D people can be distracting due to facial expressions or clothing choices, and they add geometry to your model. Eric notes that 3D people engage better with the space and furniture than 2D face-me people.

### 5. How does Eric handle the issue of black lines on black lines when tracing over imported images?
**Answer:**
Eric addresses this visibility problem by using custom styles. He goes to View → Face Style → X-Ray, which fades the image back and makes faces transparent so he can see what's underneath. He also creates a custom style with hot pink lines (or any contrasting color) by going to Styles → Edit and changing the line color. He saves this as a new style using the plus icon, allowing him to switch between default and tracing styles.

### 6. What workflow does Eric demonstrate for efficiently working with reference images?
**Answer:**
Eric creates two scenes: one with the tracing style applied and one with the default style. He disables camera location for both scenes so he can work in different areas without losing his position. He also turns off the reference image in the default scene to see his progress clearly. This allows him to quickly toggle between tracing mode and review mode by clicking between scenes, maintaining focus on the area he's working on.

### 7. How does Eric set up a template for image tracing projects?
**Answer:**
Eric saves his tracing setup as a template by going to File → Save as Template, naming it "image trace." He keeps the styles, scenes, and reference tag in the model when creating the template. Later, he can access this template through File → New from Template → My Templates, which gives him all the tracing settings ready to use. He notes that you probably don't want this as your default template unless you only trace images.

### 8. What are the different import options for 2D files in SketchUp?
**Answer:**
When importing 2D files, SketchUp offers three options: import as image, as texture, or as matched photo. Eric focuses on importing as image, which creates a special image group that contains a face with the material placed on it. This keeps the image separate from your materials library and prevents it from showing up in the paint bucket tool. This is useful for posters on walls or reference images on the ground.

### 9. How does Eric differentiate between his CAD linework and new lines when tracing?
**Answer:**
Eric uses the "by material" edge color setting in the Styles panel under Edit. He selects his CAD linework group and adds a color through Entity Info. This creates visual differentiation between the original CAD base and his new lines drawn on top. He demonstrates this by showing how the CAD lines now have a different color than his new SketchUp lines, making it easier to distinguish between the reference material and his work.

### 10. What is Eric's philosophy about the purpose of adding people to models?
**Answer:**
Eric emphasizes that people serve two main purposes: creating a sense of scale and showing activity in the space. He explains that people help viewers "transport themselves into the model" and understand "what's going on in this space and how are people using it." He notes that sometimes leaving people out can also be effective, allowing viewers to picture themselves in the space. The key is that people should enhance the design narrative rather than distract from it, since "the attention as a designer is on the space, the people are just there for context."