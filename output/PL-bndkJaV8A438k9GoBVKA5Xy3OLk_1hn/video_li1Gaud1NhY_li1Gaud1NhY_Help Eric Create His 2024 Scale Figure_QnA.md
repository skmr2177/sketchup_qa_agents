# Q&A Generated from: video_li1Gaud1NhY_li1Gaud1NhY_Help Eric Create His 2024 Scale Figure.txt

# Enhanced Q&A Generation Agent

You are an AI agent specialized in generating complete, accurate answers to questions derived from SketchUp tutorial transcripts.

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
   - Quote the instructor when useful
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

## ✅ Output
For each question, provide:
- A full answer grounded in the tutorial transcript
- Supplemented (if helpful) with clarifying info from SketchUp Help Docs

### Example:
**Q:** How is the Follow Me tool demonstrated in this tutorial?
**A:** The instructor uses the Follow Me tool to extrude a curved profile along a circular path to create crown molding. They select the path first, then click the profile. While the tool is used efficiently, the instructor does not explain the tool in detail. According to SketchUp Help, the Follow Me tool works by extruding a face along a preselected path.

## 📌 File Output
Save your results in Markdown under `output/{original_transcript_name}_QnA.md`

## Structure Requirements

## Reference Format

##INPUT TRANSCRIPT

hey guys it's aaron welcome back to sketchup square one where we cover the basics of sketchup so this is a great spot to start if you're new to sketchup or if you're self-taught and maybe need a way to cover the official basics we're going to take a look today at one of my favorite tools which is the line tool let's hop right in okay so the line tool you get to align to a couple different ways the toolbar the default toolbar across the top does have it right here it's this little pencil icon it's also available in the large tool set which of course you can pull up by going to view tool palettes or on windows will be tool toolbars and turning on the large tool set it's right here again just the pencil icon so you can click on that and you'll get it in the default toolbar at the top you can see there's a little arrow next to if you click and hold on that you'll get the option to switch between line and freehand we'll come back to freehand in a minute right now i really want to just look at line there's also a shortcut key by default the shortcut key for the drawing align tool is the l key on your keyboard so if you're in a different command i want to real quickly switch to drawing lines you can just hit l alright so the line tool is very simple i'm going to click two points and it's going to draw a line between those two points very very easy so we're going to start with something it's a basic concept but something that you definitely want to get the the hang of and that is how to click your mouse i know this sounds silly but what i want to do is get in the habit of clicking your left mouse button and then releasing to pick a point so click and release as opposed to clicking and holding down the line and dragging it we're going to click release so right now as i move this around i'm not holding down a mouse button this is so much easier so so many times people get in trouble when they they try to drag and they accidentally release when they're not ready to this prevents you from accidentally drawing line where you don't want click and release and then move your mouse to the next point and click and release again all right so you can see this is the the basic functionality of line tool it's going to draw a line from that first point i picked to whatever the second point i pick is you can see the line following from that start point to my cursor which is currently a little pencil so one of the things you will see as i move around too see how that turned green there turn red here turn blue here what's happening is inferencing is showing me where i can trace or or stay parallel to the main axes of the model we're going to have a whole nother video on inferencing so i'm not going to dive too deep into this right now but know that that is a good thing it's supposed to be happening and it allows you to keep nice straight lines as dry your model without any modifier keys or anything like that all right so what i'm going to do is i'm going to just draw a line i'm just going to draw come over here you can see one of the things you i want you to keep an eye on is this lower right corner where it says length right now see as i put as i move my mouse around it's telling me exactly how long that is so one of the things that new users get caught up in is they try to draw exact dimensions using this and i will tell you right now that's gonna just it's just gonna cause pain heartache and pain what this does this so if i'm looking to just draw an arbitrary line because i wanna show you what the properties of a line are i can just come over here and click if i click right now it's gonna draw a line that is 11 foot three and three 8 inches so for this example that's fine i'll go back to the select command i'm going to pick it and if i look at entity info it tells me this is currently an edge edges are what we call single lines in sketchup so that is currently an edge there it is 11 foot 3 and 3 8 perfect that's what i wanted to do now let's say i want to come down the green line the green axis this way i'm going to click to this point you'll notice that if as i move my mouse close to that boom when i get on it it turns green and says endpoint if i click i don't have to click right on it so you can click a little bit away from it as long as that's green and says end point when i click it's going to start my next line at that point i'm going to come down the green axis and i want to come down exactly eight feet so i could do this game again where oh i'm going i can't get to exactly eight all i have to do is start in the direction i want to draw and then type in the direction the dimension i want to put in there don't come down and click in the length field you don't have to do that it already knows that if you type you're entering a length so i'm just move down the green axis and i'm going to type in eight foot see how it shows up down there in length and then enter now i've drawn an eight foot line along the green axis you'll notice too that after you draw a line you stay connected to the end of that line that happens automatically that's a freebie don't have to do anything to make it happen it just happens if you want to disconnect you can just hit the escape key and that will disconnect you from that point to reconnect again just get near it click on the green green end point there and i can start pulling across here so again inferencing we're not going to get too deep into this but one of the things that inferencing will let me do is draw a line along the red axis to that point on edge means i'm connecting to this point see that as i move on there right here i have a midpoint here i'm connecting to the line inferencing is great it's really easy to draw lines but the important part is that to draw a line i'm going to click release move my mouse click release or click release move my mouse into a direction and then type an exact dimension i did mention we'd look at the freehand command real quick so either in the large toolbar it's right here this little squiggle line or again you can click and hold down on the line tool and you can click the freehand tool there this operates a little differently and violates exactly the thing i was talking about because the way that the freehand tool works is you do have to click and hold down the mouse button and then you can just start drawing a squiggly line like this when you release it's going to turn it into a bunch of line segments so where i picked this this line before and we looked at the info and it told me it was an edge what happens if i click this one it tells me it's a curve it tells me how many segments it was made up of and what the exact length of those pieces was or the total line was or this shorter one right here that's going to tell me that's a 19 foot curve where this one is 101 feet so that is the basics of using the line tool like i said it's really hard to use the line tool too much without getting into inferencing but i don't want to jump in and bite off too much to begin with go ahead and use the line tool to draw some shapes it's a great way too to see how sketchup goes about creating surfaces and breaking lines and that sort of thing go in and start clicking around make some lines draw some lines don't be afraid to break anything if you're just messing around in a model you can always close it and start over right try it use it a little bit and we'll come back next time and we'll take a look at the next tool in sketchup square one hopefully like that if so click like down below and if you haven't already please subscribe we create several videos a week and you'll be notified of each and every one of them if you're a subscriber most importantly though please leave a comment down below this whole series is actually happening because of comments from viewers like you we like making these videos a lot we like it even more when they're showing something you want to see thank you you


#OUTPUT Q&A Pairs 

1. How do I access the Line Tool in SketchUp?
Steps:
Open SketchUp.


Locate the Line Tool:


On the default toolbar, look for the pencil icon.


Or go to View > Tool Palettes (Mac) or View > Toolbars (Windows), and enable Large Tool Set to access the pencil icon there.


Alternatively, press the L key on your keyboard to activate the Line Tool via shortcut.



2. How do I use the Line Tool to draw lines in SketchUp?
Steps:
Activate the Line Tool (via toolbar or by pressing L).


Click and release your left mouse button to mark the starting point.


Move your mouse to the desired end point (don’t hold the button).


Click and release again to complete the line.


Repeat the process to continue drawing connected lines.



3. What is the correct way to click when drawing lines?
Answer:
 Always click and release, instead of clicking and dragging.
 This prevents accidental misplacement and allows for cleaner, controlled line drawing.

4. How can I draw lines of exact length in SketchUp?
Steps:
Click to set your starting point.


Move your mouse in the direction you want the line to go.


Type the exact length (e.g., 8' for eight feet).


Press Enter — the line will snap to that precise length.


✅ You don't need to click into any field; just start typing after moving the mouse.

5. How does SketchUp help you align with axes while drawing?
Answer:
 SketchUp uses inferencing:
When your line is aligned with the Red, Green, or Blue axis, the line changes color (red, green, or blue).


You’ll see tooltips like "On Green Axis" or "Endpoint" to help guide you.



6. How do I view the length of a line while drawing?
Answer:
 As you move your mouse after clicking the first point, the Length is shown in the bottom-right corner of the SketchUp window.

7. How can I end or break a connected line sequence?
Steps:
After drawing a line, the next one starts from the end of the previous line by default.


Press the Escape (Esc) key to stop the sequence and start fresh.



8. How can I draw a line from a specific endpoint or along an axis?
Steps:
Hover your mouse near an existing endpoint until it shows "Endpoint" in green.


Click to start the new line from there.


Move your mouse in the desired axis direction (e.g., green for Y).


Type in a length if needed and press Enter.



9. What is inferencing in SketchUp, and why is it helpful?
Answer:
 Inferencing is SketchUp’s way of helping you snap and align lines with:
Axes (red, green, blue)


Midpoints


Other geometry


It makes drawing accurate, connected shapes easier without additional tools.

10. What is the Freehand Tool, and how is it different from the Line Tool?
Steps:
Click and hold the Line Tool icon and select Freehand (squiggly line).


Or select it from the Large Tool Set.


Click and hold your mouse and draw a wavy line.


Release the mouse to complete it.


⚠️ Unlike the Line Tool, Freehand requires click-and-drag. It creates a curve made of small segments, not a straight edge.

11. How do I check the properties of a line in SketchUp?
Steps:
Switch to the Select Tool.


Click on a line.


Open the Entity Info panel:


It will tell you whether it’s an Edge or a Curve.


You'll also see the length and segment count (for curves).



12. How can I practice using the Line Tool in SketchUp?
Answer:
 Experiment by:
Drawing random shapes.


Connecting lines along axes.


Typing dimensions as you go.


Viewing entity properties.


Don't worry — you can always start a new model!



13. Where can I get more beginner SketchUp tutorials?
Answer:
 Subscribe to the SketchUp Square One series. New videos are posted multiple times a week. You can also leave comments to suggest topics for future tutorials.

Let me know if you want these formatted for a downloadable PDF or embedded in a help guide UI!

### Content Guidelines:
- **Cover 100% of useful content** mentioned in the transcript
- **Start with basic concepts** and progress to more advanced features
- **Include practical tips** and best practices
- **Address common user mistakes** and how to avoid them
- **Provide keyboard shortcuts** and alternative methods when mentioned
- **Explain technical terms** in simple language
- **Include specific examples** and demonstrations from the transcript
- **Cover UI interactions** and step-by-step prompts when mentioned
- **Address troubleshooting scenarios** and problem-solving
- **Include workflow examples** and real-world applications

### **CRITICAL: Tutorial-Specific Answers**
- **NEVER generate generic answers** that could apply to any tutorial
- **ALWAYS base answers on specific content** from the transcript
- **Include specific examples, techniques, or demonstrations** mentioned in the video
- **Reference specific tools, features, or workflows** shown in the tutorial
- **If a tool is mentioned but not demonstrated, acknowledge this limitation**
- **Use quotes from the transcript** when relevant to provide authentic context
- **Avoid template responses** - each answer must be unique to the tutorial content
- **Ensure each answer is completely different** from other answers in the same Q&A set
- **Vary sentence structure, vocabulary, and explanation approach** for each question
- **Make each answer feel fresh and original** rather than following a repetitive pattern

### **Quality Control for Tool-Specific Questions**
When generating questions about specific tools (like "How does the Move Tool function in this tutorial"):
1. **First, verify the tool is actually demonstrated** in the transcript
2. **If demonstrated, describe the specific technique shown**
3. **If mentioned but not shown, state this clearly**
4. **If not mentioned at all, don't generate the question**
5. **Never use generic tool descriptions** - always reference the specific context

### Formatting:
- Use bullet points for step-by-step instructions
- Include visual indicators like ✅ for tips and ⚠️ for warnings
- Keep answers concise but comprehensive
- Use consistent terminology throughout
- **Use bold formatting** for key terms and important points
- **Quote specific phrases** from the transcript when relevant

## Processing Instructions

1. **Read the transcript carefully** to identify all key concepts, procedures, and examples
2. **Extract main topics** and organize them logically from basic to advanced
3. **Create questions** that users would naturally ask when learning
4. **Write clear, actionable answers** with specific steps when needed
5. **Ensure 100% completeness** - cover everything important from the transcript
6. **Maintain educational value** - focus on learning outcomes
7. **Include specific examples** and demonstrations mentioned in the transcript
8. **Address any troubleshooting** or problem-solving scenarios
9. **Cover UI interactions** and step-by-step prompts
10. **Include workflow examples** and practical applications

## Coverage Requirements

### Essential Topics to Cover:
- **Basic tool functionality** and purpose
- **Step-by-step workflow** and procedures
- **UI interactions** and prompts
- **Keyboard shortcuts** and alternative methods
- **Best practices** and tips
- **Common mistakes** and how to avoid them
- **Troubleshooting** and problem-solving
- **Advanced techniques** and features
- **Practical examples** and demonstrations
- **Integration** with other tools/features
- **Performance considerations** and limitations
- **Visual feedback** and cues
- **Cleanup and organization** processes

### Quality Standards:
- **Accuracy**: All information must be correct according to the transcript
- **Clarity**: Instructions should be easy to follow for beginners
- **Completeness**: Cover 100% of useful content from the transcript
- **Consistency**: Use consistent terminology and formatting
- **Usefulness**: Focus on practical, actionable information
- **Specificity**: Include specific examples and quotes from the transcript
- **Progressive Learning**: Structure from basic to advanced concepts
- **Tutorial-Specific**: Every answer must be unique to the tutorial content
- **Uniqueness**: Each answer must be completely different from all other answers in the set
- **Originality**: Avoid repetitive patterns and create fresh, varied explanations

## Output File Naming

Save the generated Q&A pairs to the `output` folder with the filename format:
`{original_transcript_name}_QnA.md`

For example:
- Input: `video_3JM91eeeNE8_SketchUp Extension Inspection_ Bezier Curves.txt`
- Output: `output/video_3JM91eeeNE8_SketchUp Extension Inspection_ Bezier Curves_QnA.md`

## Success Criteria

A successful Q&A generation should:
- **Cover 100% of useful content** from the transcript
- **Include comprehensive Q&A pairs**
- **Provide actionable, step-by-step instructions**
- **Address both basic and advanced topics**
- **Include specific examples and demonstrations**
- **Cover troubleshooting and problem-solving**
- **Document UI interactions and workflows**
- **Serve as a complete help guide** for the tool/concept
- **Generate tutorial-specific answers** that cannot be applied to other tutorials
- **Use transcript as primary source** with optional Help Center supplementation

Remember: Your goal is to transform raw transcript content into valuable, searchable learning resources that help users master software tools effectively. The Q&A should be comprehensive enough to serve as a complete help guide, covering everything from basic concepts to advanced techniques and practical applications. **Most importantly, every answer must be specific to the tutorial content and not generic.** 

##INPUT TRANSCRIPT

title: help create his 2024 scale figure video id: li1gaud1nhy playlist index: 5 playlist url: https://www.youtube.com/watch?v=0rn7kf4vq4m&list=pl-bndkjav8a438k9gobvka5xy3olk_1hn video url: https://www.youtube.com/watch?v=li1gaud1nhy uploader: sketchup duration: 784 seconds downloaded: 2025-07-23t11:08:03.760550 -------------------------------------------------------------------------------- everybody here and today i'm going to need your help picking out an image that i'm going to use for my 2024 scale figure so i don't always do this i've got a few scale figures here behind me from the past years but i do to refresh it um at least every couple years if not every year so for those that haven't made their own scale figure uh it's a good skill to learn how to do not just the importance of why we use scale figures but of course picking the right image for a scale figure tracing a scale figure making a component coloring all those things it's just a great way to reinforce your basic sketchup fundamental knowledge so let's go ahead and do mine now i've got a few here this is u me from 2018 i don't know if it looks uh me or not this is me from 20121 this is me from 2023 so again i'm skipping a few years but i'm going to want one to take the place uh of one that represents me this year so i'm going to go ahead and get rid of that that question was just my placeholder before i sort of look at the images that i have to choose from let's take a look at what i the decision that i made in the past so number one my very first scale fig here you can see a couple things number one is i didn't have help taking the photo so i went and took a picture of myself in the mirror so i included the phone in the picture second thing is you'll notice that i put my foot behind me and so when you have your camera up high and your looking down at your feet you're going to see that a foot behind you is going to look higher in perspective because that's how it works in a photograph now in this case it almost looks it's floating though when it's a scale figure and it is floating because your foot is smaller and therefore um backwards now i tried to remedy this here in 2020 one i don't know why i wasn't wearing shoes that day but i wasn't and so here i am i did make sure that my feet were sort of equal with each other one was not in front and not behind only thing is is when you spread your feet out this far watch what happens when you rotate your feet and your shadow kind of becomes disconnected so may or may not be something that i care about so i went ahead and tried to learn the le use the lessons learned um from 2018 and 2021 and i made one here with myself where i've got my feet together but they're not super far apart and you can see so when i move the shadow sort of stays pretty close to my feet and it looks i'm standing on the ground even though it looks i'm floating because the photo was taken from a little bit higher up but you know what doing my best here so one thing that you can see here is all my poses i to put my hands in my pockets does that make the best scale figure i'm not sure let's see what we've got now to work with for my 2024 version so i grabbed some photos here let me see if i've got those open here i am uh hands not in the pockets if you're going to take a great photo first of all i want to point out number one maybe move some furniture in this case you can see i've got a chair blocking my feet now that's probably okay i can probably guess at what that looks um number two i've got the camera placed on a counter so you can see it's right about my waist level so that's good because it's going to reduce sort of that looking down onto my feet that you would see if it was taken at eye level looking down of course you get that perspective distortion this is going to level my feet out a little bit thumbs up i don't know maybe not the best pose let's do something a little bit more energetic well maybe not that energetic uh so this one's a little bit more dynamic you can see foot in the air now when would i use this in real life if i'm going to use a scale figure in a project i probably want to have them doing something so me doing the jig or me doing maybe stepping up onto a wall or climbing something maybe that would be useful maybe not so again trying to get my hands out of my pockets here's my superman pose on the waist um a little static i don't know again now what if i still go for a walk here i'm going to walk an egyptian i don't know who walks this i was trying to do a walking pose it is a little bit it's not me standing still with my hand hands in my pockets so again there i am with my hands in my pockets and then the last one i did is i thought you i've never made a scale figure sitting down so i'm going to take a picture sitting down so here to keep this show rolling i'm going to go with that one let's go with sitting down so let's take this image here pop over to sketchup and bring that in and let's see i'm going to drag that and scale it up now i to draw flat on the ground so i'm going to go and place that flat on the ground one thing i'm also going to do is make a group i'm going to start by making this a group and i'm going to scale i already know from checking my scale figure over here that my head is about 10 inch tall so i'm just going to come over here grab my chin go to the top of my hat i'm going to type in 10 in and there we go now i'm drawing at sort of one to one scale now i'm going to set my camera to parallel projection because i want to be looking straight down then i want to go up to camera standard views and top so i'm looking sort of straight down next thing i'm going to do is open up my styles and i'm going to come over here to edit and to face style and to x-ray now i have a keyboard shortcut for that so i'm not going to do that again just showing you that um i'm going to go ahead and turn this on to xray the reason for that is because it's going to make it easier for me to trace now i'm ready to trace one last step is i'm going to place this onto its own tag and the reason why i'm going to place my image onto my own tag is just because it's easier than freezing it you'll see in a second so now if i want i can just turn that on and off and that's just i can see my progress as i go so this is where i get to kind of choose what do i want to use i can use the line tool and then i can kind of see what's a straight line and then of course it's going to try to inference so i don't know if my arm is that straight i could come over here and use the arc tool and say well there's a little bit of a curve there it's kind of a slow way to do it uh personally i think um i actually to use the freehand tool when i draw so i have you can't see it but i actually have a tablet display so i'm going to switch over to my little handy dandy pen of course if you don't have this you can freehand with a mouse freehand tool is over here looks a squiggly line you can still freehand with your mouse it's pretty good it's not quite as good as when you work with a tablet but um if you do have a pen display then definitely use the tools that you have so i'm going to start with just the outer perimeter so i'm going to ignore all these inner lines shoelaces and faal facial features and clothes and stuff i just want to start with kind of a pretty broad brush stroke of grabbing just almost as if i was doing a silhouette of just the exterior so let's turn that off and see how my profile looks you can see there's no face in there so that's okay i'm just going to go ahead and close it so sometimes there's a little air gap and i don't know where one might be but you can see just by kind of closing the line here the other thing of course i can do is um change the color of my background but i my white background so i'm going to leave it somewhere in here i must have there it is i overlapped an edge so i just need to cut that out and then when i go to close this that should give me basically my whole body so i can erase those little extras extra bits so there we go there's my profile now let's go ahead and remove my arm bits so i'm going to go ahead and switch to the freehand tool same thing come in here grab maybe some folds of the clothes a little bit and that's it that one's done and lastly that one's done so i'm going to get rid of those i don't need those right there and then here it might be easier to switch to the line tool instead of using the freehand i'm okay just doing straight sleeves that this is where i may also want to switch to the arc tool you know again i'm combining methods you don't have to do freehand the whole time just because i did it that for a little bit you know it may actually make sense to have a a little bit more accuracy by bringing in a different tool and same thing here i might want to do an arc on the chin or i might want to do a um freehand here i'm not sure doesn't really matter again whatever works for your particular scale figure and i'm going to just draw a straight line and let's see do i want to cut both ears off i'm not sure sometimes i just cut one ear off and not the other i might want to cut both of them off in this case and lastly i need to actually draw round out i'm going to freehand this part i'm going to do my cap try not to look at the my face as i'm drawing it i'm not sure what that facial expression is probably just hold still for the camera i'm just going to speed this part up just a little bit because i know it's running a bit long so i'm going to use the same thing that i've been doing just kind of maybe fast forward put some details in here close everything up make sure everything looks good make sure to erase any straight lines that i've got so that those don't show up if i want to put some folds in or if i want to put some details on the shoes i can do that and that's it now we're ready to put some color on it so i'm going to turn this off and i'm going to actually i'm not going to turn that off i'm going to turn my x-ray mode off and i'm going to move this off to the side and the reason why is because i can actually sample using the pain bucket tool from myself so sample maybe grab a skin color that's not the right color that's okay i can adjust it later that's a little dark so i might just adjust this now that's me when i'm coming back from and there we go let's go ahead and try sampling that jean color see if i can pick up a nice color jeans and sample my shirt color again i don't have to use the color that i'm wearing here i can use any color that i want but um i can change it and be more creative okay and then we'll sample my hat get something maybe that's too dark so we'll just lighten it up a little bit and we'll go with that for now okay so that looks a little bit me now i'm going to turn it into a component so i'm going to select everything i'm going to group it just for now and flip it up 90° so that he's sitting straight up make that a component right click it it's going to ask me first of all what do you want to call it i'm calling this scale fig 2024 and i'm going to say always face camera and i'm going to say set the component axis so i want to make sure that the blue is up and the red is over if i'm if you have trouble getting this to line up at all so sometimes it may help you to orient the orient the the view in elevation style so when you're kind of looking straight at it then you can go ahead and get just sort of a better way to do that so i'm going to say make a component always face camera again i'm just going to say shorten that to 2024 and set the component axis i want it in the middle and i want making sure that blue is up and red is straight across that way when i turn you can see that it's pivoting on that center point and if i turn my shadows back on you can see i'm floating in the air here but that's okay because i have a stool that i'm going to put myself on so i don't need that anymore i'm going to turn that off and i'm going to place myself right over here on the stool and let's see here if that worked and let's make a component and place myself right there with right in line with myself now just to match the skin color i matched the one from the from before but i'm going to select all um on the same material and i'm going to grab that one and i'm going to repaste it and that way that same material is basically the same for each of my scal figs so there we go so that's it that's the process again i'm going to recap shortly here make sure you've got a good image to work with think about where the camera is taken picture is taken from up high center down low think about where your foot placement is what your pose is what you're wearing if that matters you can always change it later and of course lastly you know use the tools at your disposal if you don't have a tablet you can always do it on ipad or you can do it using um extensions you can also use it using do it using native tools so if you haven't made your own scale figure yet it's 2024 it's we're a few months in get in there go make yours and um it with us add it to 3d warehouse i'm going to add mine here right after this video i'll add it to 3d warehouse put it in the description below you can go download any of me from 2018 to today so don't forget to give us that thumbs up if you learn something new if you haven't already subscribed so you can get weekly videos and announcements and what's going on especially with live streams and with that i'm going to thank you and i will see you next time

#OUTPUT Q&A Pairs

**CRITICAL: Generate comprehensive Q&A pairs covering ALL content in this transcript. Each answer must be specific to the tutorial content shown. Include specific examples, techniques, and demonstrations mentioned. Use different writing styles for each answer. Cover 100% of useful content from the transcript.**

