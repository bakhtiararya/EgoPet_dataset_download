# Egopet Dataset
### [Amir Bar](https://amirbar.net), [Arya Bakhtiar](), [Antonio Loquercio](https://antonilo.github.io/), [Jathushan Rajasegaran](https://people.eecs.berkeley.edu/~jathushan/), [Danny Tran](), [Yann LeCun](https://yann.lecun.com/), [Amir Globerson](http://www.cs.tau.ac.il/~gamir/), [Trevor Darrell](https://people.eecs.berkeley.edu/~trevor/)

This repository contains the implementation of the EgoPet research paper. For more information about this work, please visit the [Project Page](link-to-project-page). Explore our visual prompting demo in this Jupyter notebook: [demo.ipynb](demo.ipynb).

## Dataset Download and Preparation

To download and prepare the EgoPet Dataset, follow these steps:

1. Install all dependencies
2. Clone the YouTube-DL repository:
3. Install yt-dlp and the required Python packages from `requirements.txt`.
4. Clone this repository  
6. Run the following command in the terminal. This process may take awhile (> 3 hours)

```
python download_egopet_datatset.py
```

### Input

The dataset processing scripts require an input Excel spreadsheet (`egopet_dataset_spreadsheet.xlsx`) containing video details such as URLs, availability, and segment information.

### Output format

Processed videos are saved in the `edited_downloaded_videos` directory, with each video file prefixed with "edited_" in its filename. By the end, the folder structure should look like something below

```
edited_downloaded_videos/
│
├── train/
│   ├── cat/
│   │   ├── edited_0a47448b479faca78b65f7d39d04b77a1ee4c55ef8154fb24061038c7b381761_segment_1.mp4
│   │   ├── edited_0a81227f2f3276024e3c9ff980e917ce4cb066608d6139aca18e0a7a761b9a5b_segment_1.mp4
│   │   └── ...
│   │
│   ├── dog/
│   │   ├── edited_0e4b23e072ec674d5ece872d3558d52e5794fb27fa5e0780de58a10bad56ad5b_segment_078.mp4
│   │   ├── edited_0e4b23e072ec674d5ece872d3558d52e5794fb27fa5e0780de58a10bad56ad5b_segment_080.mp4
│   │   └── ...
│   │
│   ├── snake/
│   │   ├── edited_2c14aa00e7448d4d11799f3d58962f4b4f82efa4300e2134a04e86efa6aca8d7_segment_3.mp4
│   │   ├── edited_2c14aa00e7448d4d11799f3d58962f4b4f82efa4300e2134a04e86efa6aca8d7_segment_9.mp4
│   │   └── ...
│   │
│   └── ... (other animal folders)
│
└── validation/
    ├── cat/
    │   ├── edited_2cd4884c54a62fe9a41372412fc774f8d39afdd4f0c12c5473ad166d1b1c7b61_segment_7.mp4
    │   ├── edited_2cd4884c54a62fe9a41372412fc774f8d39afdd4f0c12c5473ad166d1b1c7b61_segment_45.mp4
    │   └── ...
    │
    ├── dog/
    │   ├── edited_3ef180ebd7674cf9e4f9dd736cc72d1cf20f978b4a70a0843e61319565774911_segment_5.mp4
    │   ├── edited_3ef180ebd7674cf9e4f9dd736cc72d1cf20f978b4a70a0843e61319565774911_segment_6.mp4
    │   └── ...
    │
    ├── eagle/
    │   ├── edited_44e62a242eeea6616cccb60f884f2ad6c141193b50ad00581fc17039b4dbf339_segment_9.mp4
    │   └── ...
    │
    └── ... (other animal folders)
```





## Abstract

Animals perceive the world to plan their actions and interact with other agents to accomplish complex tasks, demonstrating capabilities that are still unmatched by AI systems. To advance our understanding and reduce the gap between the capabilities of animals and AI systems, we introduce a dataset of pet egomotion imagery with diverse examples of simultaneous egomotion and multi-agent interaction. Current video datasets separately contain egomotion and interaction examples, but rarely both at the same time. In addition, EgoPet offers a radically distinct perspective from existing egocentric datasets of humans or vehicles.  We define two in-domain benchmark tasks that capture animal behavior, and a third benchmark to assess the utility of EgoPet as a pretraining resource to robotic quadruped locomotion, showing that models trained from EgoPet outperform those trained from prior datasets. This work provides evidence that today's pets could be a valuable resource for training future AI systems and robotic assistants.

## Introduction
The Egopet Dataset is an extensive collection of egocentric videos of animals sourced from YouTube and TikTok. It features over 84 hours of footage, including various animals such as dogs, cats, eagles, turtles, and more. Along with the dataset, this repository provides code for processing the videos and performing tasks like Visual Interaction Prediction (VIP) and Vision to Proprioception Prediction (VPP).

## Dependencies and Prerequisites

Ensure you have the following dependencies installed before running the code:

- Python 3.9
- ffmpeg (for video processing)
- yt-dlp (a youtube-dl fork for downloading videos)
- Additional Python packages as listed in `requirements.txt`

### Installation

1. Install Python 3.9.
2. Install ffmpeg: `sudo apt-get install ffmpeg`
3. Install yt-dlp and other Python dependencies:

```
pip install yt-dlp
pip install -r requirements.txt
git clone https://github.com/ytdl-org/youtube-dl.git
```

## Usage

To process the dataset, execute the `download_egopet_dataset.py` script. Ensure the input spreadsheet is correctly set up and all dependencies are installed.

**Note**: the paper sources are hosted by arXiv and download time might take 2-3 days. <br>For inquiries/questions about this please email the authors directly.  

### Reference
If you found this code useful, please cite the following paper:


```
@InProceedings{ginosar2019gestures,
  author={A. Bar, A. Bakhtiar, D. Tran, A. Loquercio, J. Rajasegaran, Y. LeCun, T. Darrell, and A. Globerson},
  title = {EgoPet: Egomotion and Interaction Data from an
Animal’s Perspective},
  booktitle = {European Conference on Computer Vision (ECCV)}
  publisher = {IEEE},
  year={2024},
  month=jun
}
```

 
