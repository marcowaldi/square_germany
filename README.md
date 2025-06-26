![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

# Welcome to Germany²

This is a small side project I've started working on while searching for jobs. 

| Typical Squares | 🆚 | Most Interesting Finds |
|:---:|:---:|:---:|
| ![boring1](path/to/boring1.jpg) | | ![interesting1](path/to/interesting1.jpg) |
| ![boring2](path/to/boring2.jpg) | | ![interesting2](path/to/interesting2.jpg) |


<details>
<summary>🔍 Click to see the algorithm breakdown</summary>

### Local Outlier Factor Analysis
- **Structure Analysis**: Edge detection, texture patterns
- **Color Composition**: RGB distribution, saturation variance
- **Anomaly Detection**: Statistical outliers in feature space

</details>


# 🛰️ GermanSat Anomaly Hunter
> Discovering Germany's most visually unique landscapes, one square kilometer at a time

*What if we could automatically find the most interesting places in Germany just by looking at satellite data? This project does exactly that.*


## 📊 Project Stats
- **357,000+** satellite image squares processed
- **16** German states covered  
- **Top 1%** most interesting locations identified
- **~5TB** of satellite data analyzed


## 🧠 How It Works

🔸 **Step 1: Grid Generation** - Split Germany into 1km² squares  
🔸 **Step 2: Feature Extraction** - Analyze structure & color patterns  
🔸 **Step 3: Outlier Detection** - Apply Local Outlier Factor algorithm  
🔸 **Step 4: Ranking** - Sort by "interestingness" score


## 🏆 Most Interesting Discoveries

### 🥇 Top Find: Unique Geological Formation in Bavaria
![top-find](link-to-image)
*LOF Score: 0.97 | Coordinates: 47.8°N, 11.2°E*

### 🥈 Runner-up: Industrial Complex Pattern in NRW
![second-find](link-to-image)
*LOF Score: 0.94 | Coordinates: 51.5°N, 7.1°E*



<details>
<summary>🔬 Technical Implementation Details</summary>

### Feature Engineering
```python
def extract_features(image_square):
    # Structure features
    edges = cv2.Canny(image, 50, 150)
    texture = local_binary_pattern(image)
    
    # Color features  
    color_hist = cv2.calcHist([image], [0,1,2], None, [8,8,8], [0,256,0,256,0,256])
    saturation_var = np.var(cv2.cvtColor(image, cv2.COLOR_RGB2HSV)[:,:,1])
    
    return np.concatenate([edges.flatten(), texture.flatten(), color_hist.flatten(), [saturation_var]])
```


@software{german_sat_anomaly,
  title={GermanSat Anomaly Hunter},
  author={Your Name},
  year={2025},
  url={https://github.com/yourusername/repo}
}

# General Workflow

I am fully aware these are not proper workflows. Since this a project just for me and I'm not planning on publishing any of it it is merely a representation of the process and I am not planning on doing proper UML diagrams as the procedure is rather simple.

The chart below describes the first and rather time intensive process of getting all the images downloaded.
A few things to note:

 - I'm working with the free versions of GEE and Collab meaning I'm heavily restricted by quotas. Accounting for this the mosaic image is split up into the 16 German Bundesländer and each of them is being processed on its own. 
	 - Collab times out after ten to twelve hours so a .json progress file is created on my Google Drive in order to continue where I left of because I don't trust Collab and its runtime to not mess up. 
	 - All the images are being exported in batches in order to minimize the risk of GEE complaining about export quotas.

```mermaid
flowchart LR
n3["Sentinel 2 Data"]  -->  n2["Mosaic Composit Image"]
n2  -- Cropping & 'Gridification' -->  n1["Batch Export"]
```

 The chart below describes the  second part of the process. Since this step has not been reached yet  there's no way of telling how much time this will take. Initial testing suggests however that it should be quicker than the downloading of the images. A few considerations:
 - The images have been exported as .tif files meaning they have to be converted to .png files.
 - While steps were taken to filter for usable images there will be dirty data which needs to be processed
	 - Too much cloud coverage will be discarded
	 - broken satellite imagery will be discarded
	 - more than 50% of the square is located outside Germany will be discarded
- After processing the images will be stored in a combined folder in order to make further progress easier
- A square will receive a Feature & Colour Value based on its outlier factor which are weighed equally and a combined score is created. For a detailed explanation of the LOC and general procedure please refer to the methodology section.
-  
```mermaid
flowchart  LR
subgraph  s2["Google Drive"]
n5["Folders"]
end
s2  -- Combine & Process Images -->  n6["Combined Folder"]
n6  -->  n7["LOC Features"]  &  n8["LOC Colours"]
n8  -->  n9["Combined Score"]
n7  -->  n9
```
## Progress

```mermaid
gantt 
	title Project Development Timeline
	dateFormat YYYY-MM-DD
	
	section Downloading 
	Bremen :done, 2025-05-20, 6d
	Hamburg :done, 2025-05-26, 1d 
	Berlin :done, 2025-05-27, 1d 
	Saarland :done, 2025-05-27, 2d 
	Schleswig-Holstein :done, 2025-05-28, 2d 
	Thüringen :done, 2025-05-30, 3d 
	Sachsen :done, 2025-06-02, 5d 
	Rheinland-Pfalz :done, 2025-06-07, 2d 
	Sachsen-Anhalt : done, 2025-06-07, 2d
	Hessen :done, 2025-06-09, 2d 
	Mecklenburg-Vorpommern :done, 2025-06-11, 5d 
	Brandenburg :done, 2025-06-16, 3d 
	Nordrhein-Westfalen :done, 2025-06-19, 7d 
	Baden-Württemberg :active, task1, 2025-06-26, 7d 
	Niedersachsen : task2, after task1, 3d 
	Bayern : task3, after task2, 3d 
	
	section Processing 
	LOC Colours : task4, after task3, 7d 
	LOC Features : task5, after task4, 7d 

	section Finalisation
	Finalise GitHub: task6, after task5, 10d
	Travel to location: milestone, after task6, 1d

```

```mermaid
xychart-beta
    title "Images per Bundesland"
    x-axis ["BW", "BY", "BE", "BB", "HB", "HH", "HE", "MV", "NI", "NW", "RP", "SL", "SN", "ST", "SH", "TH"]
    y-axis "Number of Photos" 0 --> 15000
    bar [15000, 15000, 171, 6824, 135, 238, 4388, 5293, 15000, 8459, 5000, 678, 4165, 4425, 3442, 3650]
```
    "Baden-Württemberg" : 10000
    "Bayern" : 10000
    "Berlin" : 171
    "Brandenburg" : 6824
    "Bremen" : 135
    "Hamburg" : 238
    "Hessen" : 4388
    "Mecklenburg-Vorpommern" : 5293
    "Niedersachsen" : 10000
    "Nordrhein-Westfalen" : 8459
    "Rheinland-Pfalz" : 5000
    "Saarland" : 678
    "Sachsen" : 4165
    "Sachsen-Anhalt" : 4425
    "Schleswig-Holstein" : 3442
    "Thüringen" : 3650
**Gantt charts** - Project timelines:

```mermaid
gantt
    title Project Timeline
    dateFormat  YYYY-MM-DD
    section Planning
    Research    :2024-01-01, 10d
    Design      :2024-01-15, 15d
    section Development
    Backend     :2024-02-01, 30d
    Frontend    :2024-02-15, 25d
```

## Switch 
to another file

All your files and folders are presented as a tree in the file explorer. You can switch from one to another by clicking a file in the tree.

## Rename a file

You can rename the current file by clicking the file name in the navigation bar or by clicking the **Rename** button in the file explorer.

## Delete a file

You can delete the current file by clicking the **Remove** button in the file explorer. The file will be moved into the **Trash** folder and automatically deleted after 7 days of inactivity.

## Export a file

You can export the current file by clicking **Export to disk** in the menu. You can choose to export the file as plain Markdown, as HTML using a Handlebars template or as a PDF.


# Synchronization

Synchronization is one of the biggest features of StackEdit. It enables you to synchronize any file in your workspace with other files stored in your **Google Drive**, your **Dropbox** and your **GitHub** accounts. This allows you to keep writing on other devices, collaborate with people you share the file with, integrate easily into your workflow... The synchronization mechanism takes place every minute in the background, downloading, merging, and uploading file modifications.

There are two types of synchronization and they can complement each other:

- The workspace synchronization will sync all your files, folders and settings automatically. This will allow you to fetch your workspace on any other device.
	> To start syncing your workspace, just sign in with Google in the menu.

- The file synchronization will keep one file of the workspace synced with one or multiple files in **Google Drive**, **Dropbox** or **GitHub**.
	> Before starting to sync files, you must link an account in the **Synchronize** sub-menu.

## Open a file

You can open a file from **Google Drive**, **Dropbox** or **GitHub** by opening the **Synchronize** sub-menu and clicking **Open from**. Once opened in the workspace, any modification in the file will be automatically synced.

## Save a file

You can save any file of the workspace to **Google Drive**, **Dropbox** or **GitHub** by opening the **Synchronize** sub-menu and clicking **Save on**. Even if a file in the workspace is already synced, you can save it to another location. StackEdit can sync one file with multiple locations and accounts.

## Synchronize a file

Once your file is linked to a synchronized location, StackEdit will periodically synchronize it by downloading/uploading any modification. A merge will be performed if necessary and conflicts will be resolved.

If you just have modified your file and you want to force syncing, click the **Synchronize now** button in the navigation bar.

> **Note:** The **Synchronize now** button is disabled if you have no file to synchronize.

## Manage file synchronization

Since one file can be synced with multiple locations, you can list and manage synchronized locations by clicking **File synchronization** in the **Synchronize** sub-menu. This allows you to list and remove synchronized locations that are linked to your file.


# Publication

Publishing in StackEdit makes it simple for you to publish online your files. Once you're happy with a file, you can publish it to different hosting platforms like **Blogger**, **Dropbox**, **Gist**, **GitHub**, **Google Drive**, **WordPress** and **Zendesk**. With [Handlebars templates](http://handlebarsjs.com/), you have full control over what you export.

> Before starting to publish, you must link an account in the **Publish** sub-menu.

## Publish a File

You can publish your file by opening the **Publish** sub-menu and by clicking **Publish to**. For some locations, you can choose between the following formats:

- Markdown: publish the Markdown text on a website that can interpret it (**GitHub** for instance),
- HTML: publish the file converted to HTML via a Handlebars template (on a blog for example).

## Update a publication

After publishing, StackEdit keeps your file linked to that publication which makes it easy for you to re-publish it. Once you have modified your file and you want to update your publication, click on the **Publish now** button in the navigation bar.

> **Note:** The **Publish now** button is disabled if your file has not been published yet.

## Manage file publication

Since one file can be published to multiple locations, you can list and manage publish locations by clicking **File publication** in the **Publish** sub-menu. This allows you to list and remove publication locations that are linked to your file.


# Markdown extensions

StackEdit extends the standard Markdown syntax by adding extra **Markdown extensions**, providing you with some nice features.

> **ProTip:** You can disable any **Markdown extension** in the **File properties** dialog.


## SmartyPants

SmartyPants converts ASCII punctuation characters into "smart" typographic punctuation HTML entities. For example:

|                |ASCII                          |HTML                         |
|----------------|-------------------------------|-----------------------------|
|Single backticks|`'Isn't this fun?'`            |'Isn't this fun?'            |
|Quotes          |`"Isn't this fun?"`            |"Isn't this fun?"            |
|Dashes          |`-- is en-dash, --- is em-dash`|-- is en-dash, --- is em-dash|


## KaTeX

You can render LaTeX mathematical expressions using [KaTeX](https://khan.github.io/KaTeX/):

The *Gamma function* satisfying $\Gamma(n) = (n-1)!\quad\forall n\in\mathbb N$ is via the Euler integral

$$
\Gamma(z) = \int_0^\infty t^{z-1}e^{-t}dt\,.
$$

> You can find more information about **LaTeX** mathematical expressions [here](http://meta.math.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference).


## UML diagrams

You can render UML diagrams using [Mermaid](https://mermaidjs.github.io/). For example, this will produce a sequence diagram:

```mermaid
sequenceDiagram
Alice ->> Bob: Hello Bob, how are you?
Bob-->>John: How about you John?
Bob--x Alice: I am good thanks!
Bob-x John: I am good thanks!
Note right of John: Bob thinks a long<br/>long time, so long<br/>that the text does<br/>not fit on a row.

Bob-->Alice: Checking with John...
Alice->John: Yes... John, how are you?
```

And this will produce a flow chart:

```mermaid
graph LR
A[Square Rect] -- Link text --> B((Circle))
A --> C(Round Rect)
B --> D{Rhombus}
C --> D
```
