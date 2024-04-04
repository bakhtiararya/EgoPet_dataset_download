# Egopet Dataset
### [Amir Bar*](https://amirbar.net), [Arya Bakhtiar*](), [Danny Tran*](), [Antonio Loquercio](https://antonilo.github.io/), [Jathushan Rajasegaran](https://people.eecs.berkeley.edu/~jathushan/), [Yann LeCun](https://engineering.nyu.edu/faculty/yann-lecun), [Trevor Darrell](https://people.eecs.berkeley.edu/~trevor/), [Amir Globerson](https://cs3801.wixsite.com/amirgloberson)

This repository contains the implementation of the EgoPet research paper. For more information about this work, please visit the [Project Page](link-to-project-page). Explore our visual prompting demo in this Jupyter notebook: [demo.ipynb](demo.ipynb).

## Dataset Download and Preparation

To download and prepare the EgoPet Dataset, follow these steps:

1. Clone the YouTube-DL repository:
2. Install yt-dlp and the required Python packages from `requirements.txt`.
3. Run the following command in the terminal. This process may take awhile (> 3 hours)

```
python download_egopet_datatset.py
```

### Input

The dataset processing scripts require an input Excel spreadsheet (`egopet_dataset_spreadsheet.xlsx`) containing video details such as URLs, availability, and segment information.

### Output

Processed videos are saved in the `edited_downloaded_videos` directory, with each video file prefixed with "edited_" in its filename.

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

 
