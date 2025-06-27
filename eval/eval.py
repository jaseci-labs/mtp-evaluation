import os
import sys
import json
import argparse
import time
import importlib.util
from pathlib import Path
from pyinstrument import Profiler
from pyinstrument.renderers import JSONRenderer
from cProfile import Profile
from loguru import logger

# Add the parent directory to the path so we can import jaclang
sys.path.insert(0, str(Path(__file__).parent.parent / "jaseci" / "jac"))

from jaclang import JacMachineInterface as Jac


def run_dspy_program(program_name, program_path, profiler_type, output_dir):
    """Run a DSPy program with profiling."""
    os.makedirs(f"{output_dir}/{program_name}/dspy", exist_ok=True)
    
    # Get absolute path to the program
    program_path = os.path.abspath(program_path)
    
    # Create a results file to capture output
    results_file = open(f"{output_dir}/{program_name}/dspy/results.txt", "w")
    sys.stdout = results_file

    # Set up profiler
    if profiler_type == "cProfile":
        pr = Profile()
        pr.enable()
    else:
        profiler = Profiler()
        profiler.start()

    try:
        # Load the module directly using importlib
        spec = importlib.util.spec_from_file_location("dspy_module", program_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["dspy_module"] = module
        spec.loader.exec_module(module)
    except Exception as e:
        logger.error(f"Error while running {program_path}: {e}")

    # Save profiling results
    if profiler_type == "cProfile":
        pr.disable()
        pr.dump_stats(f"{output_dir}/{program_name}/dspy/profile.prof")
    else:
        profiler.stop()
        with open(f"{output_dir}/{program_name}/dspy/profile.html", "w") as f:
            f.write(profiler.output_html())
        with open(f"{output_dir}/{program_name}/dspy/profile.json", "w") as f:
            json.dump(json.loads(profiler.output(JSONRenderer())), f, indent=4)

    # Restore stdout
    sys.stdout = sys.__stdout__
    results_file.close()


def run_jac_program(program_name, program_path, profiler_type, output_dir):
    """Run a JAC program with profiling."""
    os.makedirs(f"{output_dir}/{program_name}/jac", exist_ok=True)
    
    # Get absolute path and split into directory and filename
    program_path = os.path.abspath(program_path)
    program_dir, program_file = os.path.split(program_path)
    module_name = program_file.replace(".jac", "")

    # Create a results file to capture output
    results_file = open(f"{output_dir}/{program_name}/jac/results.txt", "w")
    sys.stdout = results_file

    # Set up profiler
    if profiler_type == "cProfile":
        pr = Profile()
        pr.enable()
    else:
        profiler = Profiler()
        profiler.start()

    try:
        # Use the JAC import system
        Jac.jac_import(target=module_name, base_path=program_dir)
    except Exception as e:
        logger.error(f"Error while running {program_path}: {e}")

    # Save profiling results
    if profiler_type == "cProfile":
        pr.disable()
        pr.dump_stats(f"{output_dir}/{program_name}/jac/profile.prof")
    else:
        profiler.stop()
        with open(f"{output_dir}/{program_name}/jac/profile.html", "w") as f:
            f.write(profiler.output_html())
        with open(f"{output_dir}/{program_name}/jac/profile.json", "w") as f:
            json.dump(json.loads(profiler.output(JSONRenderer())), f, indent=4)

    # Restore stdout
    sys.stdout = sys.__stdout__
    results_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate JAC and DSPy implementations")
    parser.add_argument(
        "--profiler",
        help="Which profiler to use",
        default="cProfile",
        type=str,
        choices=["cProfile", "pyinstrument"],
    )
    parser.add_argument(
        "--config",
        help="Location to the Eval config",
        default="eval.config.json",
        type=str,
    )
    parser.add_argument(
        "--output_dir",
        help="Output Directory Location",
        default="output",
        type=str,
    )
    parser.add_argument(
        "--impl",
        help="Implementation to use",
        default="both",
        type=str,
        choices=["both", "dspy", "jac"],
    )
    parser.add_argument(
        "-y",
        help="Skip confirmation",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--delay",
        help="Delay between runs in seconds",
        default=60,
        type=int,
    )
    
    args = parser.parse_args()
    logger.info(f"Using {args.profiler} as the profiler.")
    
    # Load the evaluation configuration
    config_path = os.path.abspath(args.config)
    if not os.path.exists(config_path):
        logger.error(f"Config file not found: {config_path}")
        sys.exit(1)
        
    with open(config_path) as f:
        EVAL_PROBLEMS = json.load(f)
    
    # Check if output directory exists
    if os.path.exists(args.output_dir) and not args.y:
        logger.info(f"Output directory exists. Do you want to overwrite it? (y/n)")
        if input().lower() != "y":
            logger.info("Exiting...")
            sys.exit(0)
    
    # Run evaluations
    for difficulty, PROBLEM_SET in EVAL_PROBLEMS.items():
        logger.info(f"Running {difficulty} difficulty problems...")
        
        for problem_name, paths in PROBLEM_SET.items():
            if os.path.exists(f"{args.output_dir}/{problem_name}") and not args.y:
                logger.info(f"Output directory for {problem_name} exists.")
                logger.info(f"Do you want to overwrite it? (y/n)")
                if input().lower() != "y":
                    logger.info("Skipping...")
                    continue

            logger.info(f"Running {problem_name} problem from {difficulty} difficulty.")

            # Run JAC implementation
            if args.impl == "jac" or args.impl == "both":
                if "jac" in paths:
                    jac_path = os.path.abspath(paths["jac"])
                    if os.path.exists(jac_path):
                        logger.info(f"Running JAC program: {jac_path}")
                        run_jac_program(
                            problem_name, jac_path, args.profiler, args.output_dir
                        )
                        time.sleep(args.delay)
                    else:
                        logger.warning(f"JAC file not found: {jac_path}")

            # Run DSPy implementation
            if args.impl == "dspy" or args.impl == "both":
                if "dspy" in paths:
                    dspy_path = os.path.abspath(paths["dspy"])
                    if os.path.exists(dspy_path):
                        logger.info(f"Running DSPy program: {dspy_path}")
                        run_dspy_program(
                            problem_name, dspy_path, args.profiler, args.output_dir
                        )
                        time.sleep(args.delay)
                    else:
                        logger.warning(f"DSPy file not found: {dspy_path}")
    
    logger.info("Evaluation completed!")
