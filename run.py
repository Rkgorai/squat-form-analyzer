import os
import argparse
from src.main import process_video

if __name__ == "__main__":
    # 1. Initialize the Argument Parser
    parser = argparse.ArgumentParser(description="Analyze squat form from a video file.")

    # 2. Add expected arguments
    parser.add_argument(
        "-i", "--input", 
        type=str, 
        required=True, 
        help="Path to the input video file."
    )
    
    parser.add_argument(
        "-o", "--output", 
        type=str, 
        required=True, 
        help="Path where the analyzed video will be saved."
    )
    
    parser.add_argument(
        "-m", "--model", 
        type=str, 
        default="pose_landmarker_lite.task",
        choices=["pose_landmarker_lite.task", "pose_landmarker_heavy.task"],
        help="Which MediaPipe model to use (default: pose_landmarker_lite.task)"
    )

    # 3. Parse the arguments provided by the user
    args = parser.parse_args()

    # 4. Extract the directory path from the output argument and ensure it exists
    output_dir = os.path.dirname(args.output)
    if output_dir:  # Only attempt to create if a directory was specified
        os.makedirs(output_dir, exist_ok=True)

    print("Starting Squat Form Analyzer...")
    print(f"Input Video: {args.input}")
    print(f"Output Video: {args.output}")
    print(f"Model: {args.model}")
    print("-" * 40)

    # 5. Run the process
    process_video(args.input, args.output, model_asset_path=args.model)