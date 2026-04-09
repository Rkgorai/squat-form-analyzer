import os
from src.main import process_video

if __name__ == "__main__":
    # Define paths based on your requested directory structure
    # INPUT_VIDEO = os.path.join('tests', 'test_videos', 'sample_squat.mp4')
    # OUTPUT_VIDEO = os.path.join('demo', 'squat_analyzed_output.mp4')

    INPUT_VIDEO = '/home/rahul/Projects/squat-form-analyzer/sample_vids/squat_demo.mp4'  # Update this path to your test video
    OUTPUT_VIDEO = '/home/rahul/Projects/squat-form-analyzer/demo/squat_demo_analyzed.mp4'  # Desired output path for the analyzed video

    # INPUT_VIDEO = '/home/rahul/Projects/squat-form-analyzer/DeepSquat.mp4'  # Update this path to your test video
    # OUTPUT_VIDEO = '/home/rahul/Projects/squat-form-analyzer/demo/DeepSquat_analyzed.mp4'  # Desired output path for the analyzed video
    
    # Ensure the demo directory exists before saving
    os.makedirs('demo', exist_ok=True)

    print("Starting Squat Form Analyzer...")
    process_video(INPUT_VIDEO, OUTPUT_VIDEO, model_asset_path='pose_landmarker_lite.task')