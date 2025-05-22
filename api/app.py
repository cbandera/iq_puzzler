from flask import Flask, request, jsonify, Response, stream_with_context
import os
import sys
import subprocess
import json
from flask_cors import CORS

# Add the parent directory to sys.path so we can import modules from the main project
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route("/api/solve-puzzle", methods=["POST"])
def solve_puzzle():
    try:
        data = request.json
        puzzleStateFile = data.get("puzzleStateFile")
        libraryFile = data.get("libraryFile")
        solutionFile = data.get("solutionFile")

        if not puzzleStateFile or not libraryFile or not solutionFile:
            return jsonify({"error": "Missing required parameters"}), 400

        # Get the paths relative to the iq_puzzler project root
        puzzleStatePath = os.path.join(
            "puzzle_vis", "public", "data", "temp", puzzleStateFile
        )
        libraryPath = os.path.join("puzzle_vis", "public", "data", libraryFile)
        solutionPath = os.path.join(
            "puzzle_vis", "public", "data", "temp", solutionFile
        )

        # Build the command arguments
        args = [
            "--initial",
            puzzleStatePath,
            "--library",
            libraryPath,
            "--mode",
            "pyramid",
            "--solver",
            "dlx",
            "--output",
            solutionPath,
        ]

        def generate():
            # Spawn the process
            process = subprocess.Popen(
                ["iq-puzzler"] + args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                cwd=os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
            )

            # Stream stdout
            for line in process.stdout:
                yield f"data: {json.dumps({'output': line})}\n\n"

            # Stream stderr
            for line in process.stderr:
                yield f"data: {json.dumps({'output': line, 'error': True})}\n\n"

            # Wait for process to complete
            exit_code = process.wait()

            # Send completion event
            completion_data = {
                "completed": True,
                "success": exit_code == 0,
                "solutionFile": solutionFile,
                "exitCode": exit_code,
            }
            yield f"data: {json.dumps(completion_data)}\n\n"

        return Response(
            stream_with_context(generate()),
            mimetype="text/event-stream",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
        )

    except Exception as e:
        return jsonify({"error": "Error running solver", "details": str(e)}), 500


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
