from flask import Flask, request, jsonify, Response, stream_with_context
import os
import sys
import subprocess
import json
from flask_cors import CORS
import tempfile

# Add the parent directory to sys.path so we can import modules from the main project
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route("/api/solve-puzzle", methods=["POST"])
def solve_puzzle():
    app.logger.info("[PythonSolver] Received request to /api/solve-puzzle. Request details: %s" % request.headers)
    try:
        data = request.json
        app.logger.info("[PythonSolver] Successfully parsed JSON data.")
        # Log a snippet of the received content for verification, be careful with large data
        # app.logger.info(f"[PythonSolver] puzzleStateContent (first 100 chars): {data.get('puzzleStateContent', '')[:100]}")
        # app.logger.info(f"[PythonSolver] libraryContent (first 100 chars): {data.get('libraryContent', '')[:100]}")

        puzzleStateContent = data.get("puzzleStateContent")
        libraryContent = data.get("libraryContent")
        solutionFile_hint = data.get("solutionFile")
        app.logger.info("[PythonSolver] solutionFile_hint: %s" % solutionFile_hint)

        if not puzzleStateContent or not libraryContent:
            app.logger.error("[PythonSolver] Missing puzzleStateContent or libraryContent in request.")
            return jsonify({"error": "Missing puzzleStateContent or libraryContent"}), 400

        app.logger.info("[PythonSolver] Creating temporary files for puzzle state, library, and solution.")
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json', prefix='puzzle_') as tmp_puzzle_state_file, \
             tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json', prefix='library_') as tmp_library_file, \
             tempfile.NamedTemporaryFile(mode='r', delete=False, suffix='.json', prefix='solution_') as tmp_solution_file:

            tmp_puzzle_state_file.write(puzzleStateContent)
            tmp_library_file.write(libraryContent)

            tmp_puzzle_state_path = tmp_puzzle_state_file.name
            tmp_library_path = tmp_library_file.name
            tmp_solution_path = tmp_solution_file.name
            app.logger.info("[PythonSolver] Temp puzzle state file: %s" % tmp_puzzle_state_path)
            app.logger.info("[PythonSolver] Temp library file: %s" % tmp_library_path)
            app.logger.info("[PythonSolver] Temp solution file: %s" % tmp_solution_path)

        args = [
            "--initial", tmp_puzzle_state_path,
            "--library", tmp_library_path,
            "--mode", "pyramid",
            "--solver", "dlx",
            "--output", tmp_solution_path,
        ]
        app.logger.info("[PythonSolver] iq-puzzler arguments: %s" % args)

        def generate():
            app.logger.info("[PythonSolver] Starting generate() for SSE.")
            solution_content_final = None
            process = None # Define process here to access in finally if Popen fails
            try:
                app.logger.info("[PythonSolver] Spawning iq-puzzler process.")
                process_cwd = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
                app.logger.info("[PythonSolver] iq-puzzler CWD: %s" % process_cwd)
                process = subprocess.Popen(
                    ["iq-puzzler"] + args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                    cwd=process_cwd,
                )
                app.logger.info("[PythonSolver] iq-puzzler process started. Streaming stdout.")
                for line in process.stdout:
                    # app.logger.debug("[PythonSolver] stdout: %s" % line.strip()) # Can be very verbose
                    yield "data: %s\n\n" % json.dumps({'output': line})
                app.logger.info("[PythonSolver] Finished streaming stdout. Streaming stderr.")
                for line in process.stderr:
                    app.logger.warning("[PythonSolver] stderr: %s" % line.strip())
                    yield "data: %s\n\n" % json.dumps({'output': line, 'error': True})

                app.logger.info("[PythonSolver] Waiting for iq-puzzler process to complete.")
                exit_code = process.wait()
                app.logger.info("[PythonSolver] iq-puzzler process completed with exit code: %s" % exit_code)

                solution_content_final = ""
                if exit_code == 0:
                    app.logger.info("[PythonSolver] Reading solution from: %s" % tmp_solution_path)
                    with open(tmp_solution_path, 'r') as f_sol:
                        solution_content_final = f_sol.read()
                    # app.logger.info("[PythonSolver] Solution content (first 100 chars): %s" % solution_content_final[:100])
                else:
                    app.logger.error("[PythonSolver] iq-puzzler exited with error code %s. No solution content to read." % exit_code)

                completion_data = {
                    "completed": True,
                    "success": exit_code == 0,
                    "solutionContent": solution_content_final,
                    "solutionFileHint": solutionFile_hint,
                    "exitCode": exit_code,
                }
                app.logger.info("[PythonSolver] Sending completion event: %s" % completion_data)
                yield "data: %s\n\n" % json.dumps(completion_data)
            except Exception as e_generate:
                app.logger.error("[PythonSolver] Exception in generate(): %s" % e_generate, exc_info=True)
                # Ensure to yield an error message to the client if possible
                error_event = {"completed": True, "success": False, "error": str(e_generate), "details": "Error during solver execution or streaming."}
                try:
                    yield "data: %s\n\n" % json.dumps(error_event)
                except Exception as e_yield_error:
                    app.logger.error("[PythonSolver] Failed to yield error event to client: %s" % e_yield_error)
            finally:
                app.logger.info("[PythonSolver] Cleaning up temporary files.")
                os.unlink(tmp_puzzle_state_path)
                os.unlink(tmp_library_path)
                os.unlink(tmp_solution_path)
                app.logger.info("[PythonSolver] Temporary files unlinked.")
                if process and process.poll() is None: # Check if process is still running
                    app.logger.warning("[PythonSolver] Process was still running in finally block. Terminating.")
                    process.terminate()
                    process.wait(timeout=5) # Wait a bit for termination
                    if process.poll() is None:
                        process.kill() # Force kill if terminate didn't work
                        app.logger.warning("[PythonSolver] Process killed.")

        app.logger.info("[PythonSolver] Returning SSE response.")
        return Response(
            stream_with_context(generate()),
            mimetype="text/event-stream",
            headers={
                "Content-Type": "text/event-stream",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            },
        )

    except Exception as e:
        app.logger.error("[PythonSolver] Unhandled exception in solve_puzzle: %s" % e, exc_info=True)
        # Attempt to clean up temp files if they were defined and an error occurred before 'finally' in generate()
        # This is a best-effort, as their creation might have failed or names not assigned.
        # For a more robust solution, consider a wrapper or more structured try/except/finally for file handling.
        return jsonify({"error": "An unexpected error occurred in the solver service.", "details": str(e)}), 500


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
