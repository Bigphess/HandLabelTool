## HandLabelTool
A simple hand gesture labeling tool based on OpenCV, it will record your input keypoints of the hand, connect the points and save the data into a json file

## Files
- HandAnnotationTool.py 
- README.md
- res
	- 0/1/2/3/4/5.JPG
		* photos of hands
	- KeyPoints.json
		* file of keypoints
- results
	- Samples of display of the labeling

## ``HandAnnotationTool.py``
* This part is based on OpenCV
* Please comment others in main and run ``HandAnnotation().Annotation()`` for labeling
	* There are 20 key points in one hand,in 6 parts, including
		* 1 for hand center
		* 3 for thumb
		* 4 for itemfinger
		* 4 for middlefinger
		* 4 for ringfinger
		* 4 for littlefinger
	* Use ``n`` for next image
	* Use ``space`` for changing the parts,it will tell you which part now(thumb,itemfinger...etc)
	* Please label the finger from root to finger tip
	* Use ``s`` for saving the data in **current** picture
	* Use ``c`` for deleting **all** of the data in current picture before save

* Please comment ``HandAnnotation().Annotation()`` and uncomment these part for showing the labeling result
```
with open("res/KeyPoints.json") as f:
    df = json.load(f)
HandAnnotation().Display(df)
```
	* It will show you the keypoints you labeled
	* Different parts are in different colors

## results
![](results/q1_1.jpg)
![](results/q1_2.jpg)