import pandas as pd
import subprocess
import os
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
import ast  
import multiprocessing
from datetime import datetime, timedelta
import shutil
import cv2
import ffmpeg
import time  

start_time = time.time()  

logging.basicConfig(filename='summary_execution_yt-dlp.log', level=logging.INFO)

def check_tools_installed():
    """
    Checks if the 'ffmpeg' tool is installed and accessible in the system's PATH.

    This function tries to run the 'ffmpeg' command to check its version. If 'ffmpeg'
    is not installed or is not found in the system's PATH, it logs an error message and
    raises a RuntimeError.

    Raises:
        RuntimeError: If 'ffmpeg' is not installed or not found in PATH.
    """
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError as e:
        logging.error("ffmpeg is not installed or not found in PATH. Exiting.")
        raise RuntimeError("ffmpeg is not installed or not found in PATH.") from e

def get_available_disk_space():
    """
    Returns available disk space in bytes.

    This function calculates the available disk space in the current working directory
    by utilizing the 'os.statvfs' method. It multiplies the filesystem block size (f_frsize)
    by the number of available blocks (f_bavail) to compute the available space in bytes.

    Returns:
        int: Available disk space in bytes.
    """
    statvfs = os.statvfs('.')
    return statvfs.f_frsize * statvfs.f_bavail

def process_file(video_key_id, video_file_path, index, output_folder_path, num_total_videos):
    """
    Processes a video file by resizing and re-encoding it using 'ffmpeg'.

    This function takes a video file, applies resizing and re-encoding operations with
    specific parameters using 'ffmpeg', and saves the processed file in the specified output
    folder. If the processing is successful, it removes the original file.

    Args:
        video_key_id (str): A unique identifier for the video.
        video_file_path (str): The path to the video file to be processed.
        index (int): The index of the current video being processed in the total video list.
        output_folder_path (str): The path to the folder where the processed video will be saved.
        num_total_videos (int): The total number of videos to be processed.

    Returns:
        tuple: A tuple containing a status string ('success', 'already_processed', 'error') and the filename of the processed video.
    """
    filename = os.path.basename(video_file_path)
    print(f"Processing video no. {index+1}/{num_total_videos} | key_id: {video_key_id} ...")
    
    temp_filepath = os.path.join('.', "temp_" + filename)
    output_filepath = os.path.join(output_folder_path, "edited_" + filename)
    try:
        if os.path.exists(output_filepath):
            os.remove(video_file_path)  # Remove original if edited version already exists
            return "already_processed", filename

        command_ffmpeg = [
            'ffmpeg', '-i', video_file_path,
            '-vf', "scale='if(lte(iw,ih),480,-2):if(lte(iw,ih),-2,480)',format='yuv420p'",
            '-r', '30', '-vcodec', 'libx264', '-y', temp_filepath
        ]
        
        result_ffmpeg = subprocess.run(command_ffmpeg, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result_ffmpeg.returncode != 0:
            raise Exception(f"Error! ffmpeg failed to process no. {index+1}/{num_total_videos} | key_id: {video_key_id}")
        os.rename(temp_filepath, output_filepath)
        os.remove(video_file_path)  # Remove original after successful processing
        return "success", filename

    except Exception as e:
        print()
        print(f"Error! Failed processing video no. {index+1}/{num_total_videos} | key_id: {video_key_id}")
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
        logging.error(str(e))
        return "error", filename

def extract_video_segments(video_key_id, input_path, segments_info, output_folder):
    """
    Extracts specified segments from a video file and saves them as separate files.

    This function uses 'ffmpeg' to cut out segments from a given video file according to
    the specified start and end times in 'segments_info', and saves each segment as a new
    video file in the specified output folder. It handles errors and logs success or failure
    messages.

    Args:
        video_key_id (str): A unique identifier for the video.
        input_path (str): The path to the input video file from which segments are extracted.
        segments_info (dict): A dictionary containing segment information, where each key is a
                              segment identifier and each value is a dict with 'start_time' and
                              'end_time'.
        output_folder (str): The path to the folder where extracted segments will be saved.
    """
    for segment_id, segment_data in segments_info.items():
        start_time = segment_data['start_time']
        end_time = segment_data['end_time']
        output_segment_filename = f"edited_{video_key_id}_segment_{segment_id}.mp4"
        output_segment_path = os.path.join(output_folder, output_segment_filename)

        cmd = [
            "ffmpeg",
            "-i", input_path,
            "-ss", start_time,
            "-to", end_time,
            "-c:v", "libx264",
            "-c:a", "aac",
            output_segment_path
        ]
    
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            logging.info(f"Successfully extracted segment {segment_id} from {input_path}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to extract segment {segment_id} from {input_path}: {e}")
    
check_tools_installed()

input_dataset_file = "egopet_dataset_spreadsheet.xlsx"
print(f"Reading in {input_dataset_file}...")
try:
    input_dataset_df = pd.read_excel(input_dataset_file)
except Exception as e:
    logging.error(f'Error reading Excel file {input_dataset_file}: {e}')
    raise

interest_key_ids = [
    "a876cc8a99ea779976b59d175c98c0e2e9c424ecf62c3e6dd360f9e3c4b5e3fe",
    "f26955b94ddda703ab7b08881f13d129a759593f8e29ec9b169f001995eb8c21",
    "2cd4884c54a62fe9a41372412fc774f8d39afdd4f0c12c5473ad166d1b1c7b61",
    "6a9f1e7e5faaffabc8a1a204949b043c7a67cb9a99edac51d55bca3579cb2acd",
    "4324313c51204797cdd8ca259a28fec93293a4ba65bb8ba13ef15539a79f3125",
    "5a70328f74b34e0b57cf7184cff54fe7d5710a5108744bdef16a36c6d62779c7",
    "f4a6a1b1e9941eec56352d61d31dbfc09cdb54310125c88fa58e6000b1de7ee3",
    "7db8a0603799059ff83bb5011ffa671ee3744694e5fcd547451b01fa1fd59279",
    "024ed2c11e7817cdfe6c661c9ecd2cca6e84ff0f5c0e1c3f75e481ab5aae78f0",
    "8e7e2c37855dcd28ac10388f87876314320d59f0dfdf598fd50b6e3b3ca7093e",
    "5f950cdae57a098392dc4e56416d6e57046960c54a61a7bf9aeb5532cccb06a0"
]

def validate_and_sort_timecodes(timecodes, duration):
    timecodes_dt = [datetime.strptime(tc, "%H:%M:%S.%f") for tc in timecodes] + [datetime.strptime(duration, "%H:%M:%S.%f")]
    unique_sorted_timecodes = sorted(set(timecodes_dt))
    if unique_sorted_timecodes[-1] > datetime.strptime(duration, "%H:%M:%S.%f"):
        unique_sorted_timecodes = unique_sorted_timecodes[:-1]
    return [tc.strftime("%H:%M:%S.%f")[:-3] for tc in unique_sorted_timecodes[:-1]]

def create_segment_intervals(row):
    timecodes = ast.literal_eval(row['time_jump_timecodes'])
    duration = row['duration']
    timecodes = validate_and_sort_timecodes(timecodes, duration)
    intervals = {}
    for i in range(len(timecodes)):
        start_time = timecodes[i]
        end_time = timecodes[i+1] if i+1 < len(timecodes) else duration
        segment_duration = (datetime.strptime(end_time, "%H:%M:%S.%f") - datetime.strptime(start_time, "%H:%M:%S.%f")).total_seconds()
        if segment_duration > 0:  
            intervals[i+1] = {'start_time': start_time, 'end_time': end_time, 'segment_duration': segment_duration}
    return intervals

temp_df = input_dataset_df.copy(deep=True)
temp_df = temp_df[temp_df['key_id'].isin(interest_key_ids)]
temp_df['segment_time_intervals'] = temp_df.apply(create_segment_intervals, axis=1)

correct_df = input_dataset_df[~input_dataset_df['key_id'].isin(interest_key_ids)]

input_dataset_df = pd.concat([temp_df, correct_df])
    
def safe_convert(value):
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return value

input_dataset_df['segments_to_download'] = input_dataset_df['segments_to_download'].apply(safe_convert)
input_dataset_df['segment_time_intervals'] = input_dataset_df['segment_time_intervals'].apply(safe_convert)    


output_folder_name = "edited_downloaded_videos"
output_folder_path = os.path.join('.', output_folder_name)
print("Creating the output folder if it doesn't exist...")
os.makedirs(output_folder_path, exist_ok=True)

# Counters for downloaded, already downloaded, and failed videos
num_sucessfully_downloaded_videos = 0
num_already_downloaded_videos = 0
num_failed_downloads_videos = 0
num_sucessfully_processed_videos = 0
num_already_processed_videos = 0
num_failed_processed_videos = 0
failed_videos_list = []

# Set max_workers to the number of available CPU cores
machine_max_workers = os.cpu_count()

# input_dataset_df = input_dataset_df[0:100]
num_total_videos = len(input_dataset_df)
input_dataset_df.reset_index(drop=True, inplace=True)
input_dataset_df.index = range(1, num_total_videos + 1)

# Introduce a counter for processed videos
num_processed_videos_counter = 0

with ProcessPoolExecutor(max_workers=machine_max_workers) as executor:
    future_to_row = {}
    for index, row in input_dataset_df.iterrows():
        # Check disk space
        if get_available_disk_space() < 1e9:  # Less than 1GB
            logging.warning("Running critically low on disk space! Stopping processing...")
            print("Running critically low on disk space! Stopping processing...")
            break

        video_key_id = row['key_id']
        video_url = row['video_url']
        
        video_available = row['video_available_to_download']
        
        segments_to_download = row['segments_to_download']
        segment_time_intervals = row['segment_time_intervals']

        # Check if the video is available for download
        if not video_available and (len(segments_to_download) > 0):
            continue

        segments_info = {k: segment_time_intervals[k] for k in segments_to_download if k in segment_time_intervals}
        
        print(f"Downloading video no. {index}/{num_total_videos} | key_id: {video_key_id} | URL: {video_url}")
        
        video_folder = os.path.join(output_folder_path, "edited_" + video_key_id)
        os.makedirs(video_folder, exist_ok=True)
        
        input_video_file_path = os.path.join(video_folder, "edited_" + video_key_id + ".mp4")

        if not os.path.isfile(input_video_file_path):
            command = ['yt-dlp', video_url, '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
                       '--retry-sleep', 'linear=1::2', '--no-check-certificates',
                       '--sleep-requests', '2', '--no-write-auto-subs',
                       '-o', f"{video_folder}/{video_key_id}.%(ext)s", '--write-info-json']
            future = executor.submit(subprocess.run, command, capture_output=True, text=True)
            future_to_row[future] = (video_key_id, video_url, index, segments_info, video_folder)
        else:
            num_already_downloaded_videos += 1
            already_downloaded_message = f'Video with key_id {video_key_id} from {video_url} already downloaded'
            print(already_downloaded_message)
            logging.info(already_downloaded_message)
    
    # Process futures as they complete
    for future in as_completed(future_to_row):
        video_key_id, video_url, index, segments_info, video_folder = future_to_row[future]

        process = future.result()
        print(f"Beginning to process video key_id: {video_key_id} | URL: {video_url}",)
        if process.returncode == 0:
            num_sucessfully_downloaded_videos += 1
            input_video_file_path = os.path.join(video_folder, video_key_id + ".mp4")
            
            
            result, filename = process_file(video_key_id=video_key_id, 
                                            video_file_path=input_video_file_path, 
                                            index=index, 
                                            output_folder_path=video_folder,
                                            num_total_videos=num_total_videos)
            if result == "success":
                num_sucessfully_processed_videos += 1
                success_message = f'Successfully processed video key_id: {video_key_id}'
                print(success_message)
                logging.info(success_message)
                
                # Now extract the segments for this video
                input_video_file_path = os.path.join(video_folder, "edited_" + video_key_id + ".mp4")
                extract_video_segments(video_key_id, input_video_file_path, segments_info, video_folder)
                
            elif result == "already_processed":
                num_already_processed_videos += 1
                already_processed_message = f'Already processed video key_id: {video_key_id}'
                print(already_processed_message)
                logging.info(already_processed_message)
                
                # Now extract the segments for this video
                input_video_file_path = os.path.join(video_folder, "edited_" + video_key_id + ".mp4")
                extract_video_segments(video_key_id, input_video_file_path, segments_info, video_folder)
                
            else:
                num_failed_processed_videos += 1
                error_message = f'Error processing video key_id: {video_key_id} from {video_url}'
                print()
                print(error_message)
                logging.error(error_message)
                failed_videos_list.append((video_key_id, video_url))
        else:
            num_failed_downloads_videos += 1
            error_message = f'Error downloading key_id: {video_key_id} from {video_url} :\n{process.stderr}'
            print()
            print(error_message)
            logging.error(error_message)
            failed_videos_list.append((video_key_id, video_url))
        
        # After every 25 videos, print a summary message
        if (num_processed_videos_counter % 25 == 0) and (num_processed_videos_counter != 0):
            print()
            print(f"Quick Summary after processing {num_processed_videos_counter} number of videos so far...")
            print(f"\t- Sucessfully Downloaded: {num_sucessfully_downloaded_videos}, Already Downloaded: {num_already_downloaded_videos}, Failed Downloads: {num_failed_downloads_videos}")
            print(f"\t- Sucessfully Processed: {num_sucessfully_processed_videos}, Already Processed: {num_already_processed_videos}, Failed Processed: {num_failed_processed_videos}")
            print()
            
print()
print("Summary of Execution")
print("--------------------------------------------------------------------------------------------------------------------------------------------")
print(f"- Total Number of videos attempted: {num_total_videos}")
print(f"- Sucessfully Downloaded: {num_sucessfully_downloaded_videos}, Already Downloaded: {num_already_downloaded_videos}, Failed Downloads: {num_failed_downloads_videos}")
print(f"- Sucessfully Processed: {num_sucessfully_processed_videos}, Already Processed: {num_already_processed_videos}, Failed Processed: {num_failed_processed_videos}")
print('- Failed video IDs and URLs:')
for key_id, url in failed_videos_list:
    print(f'\t-- Key ID: {key_id}, URL: {url}')
print()

logging.info("\nSummary of Execution")
logging.info("--------------------------------------------------------------------------------------------------------------------------------------------")
logging.info(f"- Total Number of videos attempted: {num_total_videos}")
logging.info(f"- Sucessfully Downloaded: {num_sucessfully_downloaded_videos}, Already Downloaded: {num_already_downloaded_videos}, Failed Downloads: {num_failed_downloads_videos}")
logging.info(f"- Sucessfully Processed: {num_sucessfully_processed_videos}, Already Processed: {num_already_processed_videos}, Failed Processed: {num_failed_processed_videos}")
logging.info('- Failed video IDs and URLs:')
for key_id, url in failed_videos_list:
    logging.info(f'\t-- Key ID: {key_id}, URL: {url}')
logging.info("\n")

# Record the end time
end_time = time.time()  

# Calculate total execution time
total_seconds = end_time - start_time

# Calculate days, hours, minutes, and seconds
days, remainder = divmod(total_seconds, 86400)  # 86400 seconds in a day
hours, remainder = divmod(remainder, 3600)      # 3600 seconds in an hour
minutes, seconds = divmod(remainder, 60)        # 60 seconds in a minute

# Print out the total execution time in days, hours, minutes, and seconds
print(f"Total execution time: {int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {seconds:.2f} seconds")
print()


"""

# finalized dataset

base_dir = 'classifier_train_and_validation_video_set'
train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'validation')

# Create base, train, and validation directories if they don't exist
os.makedirs(train_dir, exist_ok=True)
os.makedirs(validation_dir, exist_ok=True)

# Path to the original videos folder
original_videos_base_dir = 'edited_downloaded_videos'

# Iterate through the dataframe
for index, row in input_dataset_df.iterrows():
    key_id = row['key_id']
    animal = row['animal']
    is_train = row['training_set']
    is_validation = row['validation_set']

    # Determine the destination base path
    base_path = train_dir if is_train else validation_dir

    # Construct the path to the animal folder within the correct set
    animal_folder_path = os.path.join(base_path, animal)
    os.makedirs(animal_folder_path, exist_ok=True)
    
    # Path to the source video segment files
    source_video_folder = os.path.join(original_videos_base_dir, "edited_" + key_id)
    
    # Check if the source folder exists, if not skip to the next iteration
    if not os.path.exists(source_video_folder):
        continue
    
    # Iterate through files in the source folder and copy them
    for filename in os.listdir(source_video_folder):
        if filename.startswith("edited_") and ("segment" in filename) and filename.endswith(".mp4"):
            # Construct full source and destination paths
            source_file_path = os.path.join(source_video_folder, filename)
            destination_file_path = os.path.join(animal_folder_path, filename)
            
            # Copy the file to the destination
            shutil.copy(source_file_path, destination_file_path)
    
    # Delete the original folder for the key_id after copying
    shutil.rmtree(source_video_folder)

# Delete the original videos base directory after processing all entries
if os.path.exists(original_videos_base_dir):
    shutil.rmtree(original_videos_base_dir)

"""

print("Segment files have been organized and original folders have been deleted.")
print()