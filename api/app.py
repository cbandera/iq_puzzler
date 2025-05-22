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
    try:
        data = request.json
        puzzleStateContent = data.get("puzzleStateContent")
        libraryContent = data.get("libraryContent")
        solutionFile_hint = data.get("solutionFile")

        if not puzzleStateContent or not libraryContent:
            return jsonify({"error": "Missing puzzleStateContent or libraryContent"}), 400

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json', prefix='puzzle_') as tmp_puzzle_state_file, \
             tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json', prefix='library_') as tmp_library_file, \
             tempfile.NamedTemporaryFile(mode='r', delete=False, suffix='.json', prefix='solution_') as tmp_solution_file:

            tmp_puzzle_state_file.write(puzzleStateContent)
            tmp_library_file.write(libraryContent)

            tmp_puzzle_state_path = tmp_puzzle_state_file.name
            tmp_library_path = tmp_library_file.name
            tmp_solution_path = tmp_solution_file.name

        args = [
            "--initial",
            tmp_puzzle_state_path,
            "--library",
            tmp_library_path,
            "--mode",
            "pyramid",
            "--solver",
            "dlx",
            "--output",
            tmp_solution_path,
        ]

        def generate():
            solution_content_final = None
            try:
                process = subprocess.Popen(
                    ["iq-puzzler"] + args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                    cwd=os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
                )

                for line in process.stdout:
                    yield f"data: {json.dumps({'output': line})}\n\n"

                for line in process.stderr:
                    yield f"data: {json.dumps({'output': line, 'error': True})}\n\n"

                exit_code = process.wait()

                solution_content_final = ""
                if exit_code == 0:
                    with open(tmp_solution_path, 'r') as f_sol:
                        solution_content_final = f_sol.read()

                completion_data = {
                    "completed": True,
                    "success": exit_code == 0,
                    "solutionContent": solution_content_final,
                    "solutionFileHint": solutionFile_hint,
                    "exitCode": exit_code,
                }
                yield f"data: {json.dumps(completion_data)}\n\n"
            finally:
                os.unlink(tmp_puzzle_state_path)
                os.unlink(tmp_library_path)
                os.unlink(tmp_solution_path)

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
        app.logger.error(f"Error in solve_puzzle: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
