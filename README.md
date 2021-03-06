# VisualizeBikeRide

![example image4](https://user-images.githubusercontent.com/30561629/39067038-45fe4c78-44a5-11e8-86a0-75503fa1c244.png)
 ---

## Parse through exported XML files from Strava to visualize recorded rides

The program will read your Strava file and run through the GPS coordinates of the route while showing the altitude, heart rate (if recorded), and speed on the right.

**Author**

Eric Yang


**Files**

* VisualizeBikeRide.py
* graphics.py
* compass.gif
* RacingSunsetFull.xml

---

**How To Use**

1. Clone the directory to your local machine. It includes `RacingSunsetFull.xml` as an example
2. To get an XML of your own ride, go online to Strava.com and find the specific activity you want to export
3. In the url, append `/export_original` to the end, and this will download the tcx file
4. To convert the TCX to XML, simply change the filetype from `.tcx` to `.xml`
5. In `main()`, change `fileName` to the **full** name of your downloaded xml file
6. (optional) You can change the size of the visualization by modifying `scale` in `main()`
7. (optional) Depending on the size of your file, you may want to go through it slower or faster. You can tweak `rfRate` and `readRate` in `main()`. **Decreasing** `rfRate` and **Increasing** `readRate` will make it faster.
8. Make sure you have all of the files in the same folder
9. Run VisualizeBikeRide.py

## Resources

The visualization uses the `graphics.py` library which can be found at http://mcsp.wartburg.edu/zelle/python/graphics.py
