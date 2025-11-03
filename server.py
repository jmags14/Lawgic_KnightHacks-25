from flask import Flask, request, jsonify
from flask_cors import CORS
from my_agents import orchestrate_case, load_file  # import your agent setup
from werkzeug.utils import secure_filename
import os
import traceback 

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
CORS(app)  # allow requests from React frontend
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/api/process", methods=["POST"])
def process():
    try:
        print("Files received:", request.files)
        print("Form data received:", request.form)
        uploaded_files = request.files.getlist("files")
        print("Uploaded files list:", uploaded_files)

        file_contents = []

        for f in uploaded_files:
            if f:
                filename = secure_filename(f.filename)
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                print("Saving file to:", file_path)

                try:
                    f.save(file_path)
                except Exception as e:
                    print("Error saving file:", e)
                    raise
                # load_files_from_folder returns text content
                #file_contents.append(load_files_from_folder(file_path))
                content = load_file(file_path)
                file_contents.append(content)

        # Handle optional user text prompt
        prompt = request.form.get("prompt", "")

        # Run orchestration
        result = orchestrate_case(file_contents, optional_prompt=prompt)
        #result = pipeline.run(input_text)

        return jsonify({"status": "success", "result": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e), "trace": traceback.format_exc()}), 500

if __name__ == "__main__":
    app.run(debug=True)
