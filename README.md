# VisualizeBikeRide

![example image](https://user-images.githubusercontent.com/30561629/39052853-5b118a0a-447b-11e8-936f-c7f114031971.png)
 ---

## Parse through exported XML files from Strava to visualize recorded rides

The program will read the Strava file and run through the route while showing the altitude on the left and heart rate (if included) on the right.

---
## Authors

Eric Yang

---

**Files**

* VisualizeBikeRide.py
* graphics.py
* compass.gif

---

**How To Use**

1. To get an XML of your own ride, go online to Strava.com and find the specific activity you want to export
2. In the url, append `/export_tcx` to the end, and this will download the tcx file
3. To convert the tcx to XML, simply change the filetype from `.tcx` to `.xml`
4. Make sure you have all of the files in the same folder
5. In `main()`, change `fileName` to the **full** name of your downloaded xml file
6. (optional) You can change the size of the visualization by modifying `scale` in `main()`
7. (optional) Depending on the size of your file, you may want to go through it slower or faster. You can tweak `rfRate` and `readRate` in `main()`. **Decrease** `rfRate` and **Incrase** `readRate` to make it faster.
8. Run VisualizeBikeRide.py

---

## Resources

The visualization uses the `graphics.py` library which was found at http://mcsp.wartburg.edu/zelle/python/graphics.py