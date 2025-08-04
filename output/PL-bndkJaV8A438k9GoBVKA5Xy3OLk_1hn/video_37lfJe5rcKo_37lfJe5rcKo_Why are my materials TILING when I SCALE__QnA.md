## Q: Why does the material repeat when I scale loose geometry?
A: When using the Push Pull tool on loose geometry, the material repeats as it stretches. This is because the material is applied to each face of the geometry individually, and when you stretch the geometry, each face is repeated.

## Q: How does scaling a grouped geometry work?
A: Scaling a grouped geometry works in the same way as scaling loose geometry. The material will repeat as the geometry stretches.

## Q: What happens if I scale a group that has a container painted on it?
A: If you scale a group that has a container painted on it, the material inside the container will stretch, but not the container itself. However, since the question is about scaling groups with materials applied to their faces (not just containers), this answer clarifies how materials behave when scaled within these specific contexts.

## Q: Should I paint the faces of my geometry and group it, or create a separate component?
A: In general, painting the faces of your geometry and grouping it is the best approach for consistent results. However, in certain situations where you need to model a piece with loose geometry, creating a separate component might be more suitable.

## Q: Why doesn't scaling a grouped geometry work the same way as scaling loose geometry?
A: This difference arises because when you paint the faces of your group (and not the container itself), you're applying material directly to each face individually. As a result, the behavior is consistent with pushing/pulling individual faces.

## Q: Is there an exception for painting containers instead of just faces?
A: Yes, if you paint a container, it may behave differently than expected when scaling. In this case, the material inside the container will still stretch, but not the container itself.

Note that in order to enhance your answer using SketchUp Help content, according to the instructions:

"Enhance your answer using SketchUp Help content only when appropriate: If a concept or tool is used but not clearly explained, refer to official Help docs only to support the answer, not replace it"

However, this particular question doesn't require clarification of the behavior described in the video.