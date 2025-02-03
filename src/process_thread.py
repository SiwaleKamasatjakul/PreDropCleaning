import os
import threading
import sys
import argparse
import queue

# Ensure the correct path to access your modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.FileManagerClass import FileMover
from tools.ProcessHandler import FileQueue
from tools.JsonManage import JsonLoader


class MainProcess:
    @staticmethod
    def run(file_mover_class, config, file_queue):
        """
        Start threads for file moving and processing.
        """
        mover_thread = threading.Thread(target=file_mover_class.move_files, args=(file_queue, config))

        processor_thread = FileQueue.file_queue_process(file_queue, config)  # Single thread for processing

        # Start both threads
        mover_thread.start()
        try:
            mover_thread.join()
            file_queue.put(None)  # Signal the processor thread to stop
            processor_thread.join()
        except KeyboardInterrupt:
            print("Stopping threads...")
            sys.exit(1)


def configure_parser():
    """
    Configures the argument parser for command-line options.
    """
    parser = argparse.ArgumentParser(description="File processing script.")
    parser.add_argument(
        "--config",
        type=str,
        help="Path to the JSON configuration file.",
        default="/home/siwale/Documents/PreCleanB4Drop/config/config.json",
    )
    return parser


def main():
    """
    Main entry point for the script.
    """
    parser = configure_parser()
    args = parser.parse_args()
    file_queue = queue.Queue()

    try:
        # Load the configuration JSON file
        config = JsonLoader().LoadJsonConfig(args.config)

        # Initialize FileMover with the configuration
        file_mover_class = FileMover

        # Run the MainProcess with static methods
        MainProcess.run(file_mover_class, config, file_queue)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
