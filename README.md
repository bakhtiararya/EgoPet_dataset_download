# Egopet Dataset
### [Amir Bar*](https://amirbar.net), [Danny Tran*](), [Arya Bakhtiar*](), [Trevor Darrell](https://people.eecs.berkeley.edu/~trevor/)

This repository contains the implementation of the EgoPet research paper. For more information about this work, please visit the [Project Page](link-to-project-page). Explore our visual prompting demo in this Jupyter notebook: [demo.ipynb](demo.ipynb).

## Abstract

Animals are intelligent agents that exhibit various cognitive and behavioral traits. They plan and act to accomplish complex tasks, and they can interact with other agents or objects. Despite remarkable progress in AI, learning to understand the world as well as a cat remains a challenge. We argue that one major limitation towards achieving this goal is the lack of data. To address this, we introduce EgoPet, a new extensive dataset featuring over 84 hours of egocentric videos of animals, including dogs, cats, eagles, turtles, and others, sourced from YouTube and TikTok.\footnote{While we did not restrict our data collection to pets, our methodology led to a dataset that primarily consists of pets, so we named it EgoPet.} Together with this dataset, we propose two tasks with annotated data: Visual Interaction Prediction (VIP) and Vision to Proprioception Prediction (VPP), aimed at both perception and action. Compared to other datasets, models pretrained on EgoPet perform better on VIP and VPP.

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

## Dataset Download and Preparation

To download and prepare the EgoPet Dataset, follow these steps:

1. Clone the YouTube-DL repository:
2. Install yt-dlp and the required Python packages from `requirements.txt`.

### Input

The dataset processing scripts require an input Excel spreadsheet (`egopet_dataset_spreadsheet.xlsx`) containing video details such as URLs, availability, and segment information.

### Output

Processed videos are saved in the `edited_downloaded_videos` directory, with each video file prefixed with "edited_" in its filename.

## Usage

To process the dataset, execute the `download_egopet_dataset.py` script. Ensure the input spreadsheet is correctly set up and all dependencies are installed.

**Note**: the paper sources are hosted by arXiv and download time might take 2-3 days. <br>For inquiries/questions about this please email the authors directly.  

## Data

1. Download the full dataset as described [here](data/dataset.md)


### Reference
If you found this code useful, please cite the following paper:


```
@InProceedings{ginosar2019gestures,
  author={A. Bar and D. Tran and A. Bakhtiar},
  title = {EgoPet: A pet’s-eye view of the world for learning animal behavior},
  booktitle = {Computer Vision and Pattern Recognition (CVPR)}
  publisher = {IEEE},
  year={2024},
  month=jun
}
```