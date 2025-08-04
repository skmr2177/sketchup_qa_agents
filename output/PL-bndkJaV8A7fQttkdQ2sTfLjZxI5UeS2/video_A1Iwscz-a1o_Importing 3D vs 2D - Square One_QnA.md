# Importing 3D vs 2D - Square One

### 1. What are the two main families of files that can be imported into SketchUp?
**Answer:**
Aaron explains that there are two different families of files: 3D files and 2D files. The 3D files include SKP, DEM, IFC, DWG, DXF, STL, DAE, DMZ, 3DS, OBJ, and STL files, which will pull in three-dimensional geometry. The 2D files are image files including BMP, JPEG, PNG, PSD, TIFF, TGA, and PDF files, which are primarily bitmap images that pull in as flat images. Aaron notes that PDFs can potentially contain vector imagery, but for this tutorial he focuses on the bitmap image imports.

### 2. How does the import process differ between 3D and 2D files?
**Answer:**
3D files import with different workflows depending on the file type, and most have a "configure button" that allows you to choose how to import them. The configuration options vary by file type because "the data that's stored in that file type is a little bit different." 2D files, however, have an additional dropdown that asks whether you want to import "as an image, as a texture, or as a matched photo." Aaron focuses on importing as image, which creates a special image group rather than a regular component.

### 3. What happens when you import a DXF file and how do you work with it?
**Answer:**
When importing a DXF file, SketchUp puts the entire thing in a group. Aaron shows that going into that group lets you interact with the DXF as it existed when it was created. Sometimes there's an "extra layer" where you need to explode once to get rid of the container that was created to put the DXF file into. Once imported, the DXF shows up inside a group that can be moved around using the move command. Aaron notes that the group structure will vary based on how the file was created and how many layers deep the groups are.

### 4. How do you import a 2D image and what controls do you have over its size?
**Answer:**
When importing a 2D image, you first choose the file type (like PNG) and select "use as image" from the dropdown. After clicking import, the image becomes connected to your cursor and asks you to pick the first point. You can then drag out to any size you want, or specify an exact height by typing in dimensions (like "10 foot") and hitting enter. Aaron demonstrates this by importing a PNG file and making it exactly 10 feet tall.

### 5. What is the difference between a regular group and an image group?
**Answer:**
Aaron explains that a 2D image import creates a "special group" that's different from a regular group. If you select a 3D file import, Entity Info shows it as a component, but if you select a 2D image import, Entity Info shows it as an image with information about the PNG file being displayed and its exact size. You can't double-click to enter an image group like you can with regular groups. The image group contains a face with the material placed on it, but as long as it's in this special image group, the texture won't show up in the paint bucket tool.

### 6. When would you use the "import as image" option versus other import methods?
**Answer:**
Aaron suggests using "import as image" when you want the image to "not be a material you're going to use as a texture anywhere in the model and you want it to stay inside its own container." Specific examples include importing a poster to put on a wall or importing an image for the ground to reference something. This keeps the image separate from your materials library and prevents it from appearing in the paint bucket tool, making it ideal for reference materials or decorative elements.

### 7. What configuration options are available for 3D file imports?
**Answer:**
Aaron explains that most 3D file types have a "configure button" that allows you to choose how to import them. The configuration options vary by file type because "the information that you can pull in and the control you have over how you pull it in is going to change depending on the file." For example, the configuration options for a DXF file will be different from an STL file because they store different types of data. Aaron notes that some file types don't have configuration options, but most do.

### 8. How does the import results summary work and what information does it provide?
**Answer:**
After importing a file, SketchUp provides an import results summary that varies by file type. Aaron explains that "the data that shows up here the import results are going to vary file type by file type" but in general it tells you whether the file imported properly or not. This summary helps you understand what was successfully imported and can alert you to any issues with the import process.

### 9. What are the potential issues that can occur during the import process?
**Answer:**
Aaron mentions that it's "possible to hit errors here where there's bad data where it can't import the file." If there are problems with the file data, SketchUp will tell you that it couldn't import the file. This can happen with corrupted files, unsupported formats, or files with problematic geometry. The import results summary will indicate whether the import was successful or if there were issues.

### 10. How does Aaron approach teaching the different file import types?
**Answer:**
Aaron takes a "super high level" approach for this tutorial, explaining that "we'll dive a little bit deeper into those specific file formats in later videos." He focuses on the fundamental differences between importing 3D versus 2D files and the basic process for each. He emphasizes that this is just "toe in the water before we dive in" and that specific file formats like DXF and DWG will get their own dedicated videos where he can explain what each configuration option means and how they affect the import.