from flask import Flask, request, jsonify
from flask_cors import CORS
#from my_agents import orchestrate_case  # import your agent setup
import tempfile
import os

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
# allow requests from React frontend
CORS(app)  
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/api/process", methods=["POST"])
def process():
    """
    Accepts text or files, sends them to orchestrate_case(),
    and returns the response or actionable task summary.
    """
    try:
        uploaded_files = request.files.getlist("files")
        uploaded_file_paths = []


        for f in uploaded_files:
            if f:
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], f.filename)
                f.save(file_path)
                uploaded_file_paths.append(file_path)

        # Handle optional user text prompt
        prompt = request.form.get("prompt", "")

        ai_response = f"Received prompt: {prompt}\n"
        if uploaded_file_paths:
            ai_response += f"Uploaded files: {', '.join(uploaded_file_paths)}"
        else:
            ai_response += "No files uploaded."

                # Example: Call OpenAI API
        # response = openai.Completion.create(
        #     engine="text-davinci-003",
        #     prompt=prompt,
        #     max_tokens=500
        # )
        # ai_response = response.choices[0].text
        # Run your orchestration
        
        #result = orchestrate_case(file_paths, prompt)

        return jsonify({"status": "success", "result": str(ai_response)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
