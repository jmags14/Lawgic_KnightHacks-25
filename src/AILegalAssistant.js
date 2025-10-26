<<<<<<< HEAD
import React, {useState, useRef} from "react";
=======
import React, { useState } from "react";
>>>>>>> f73e62219f7a73237765f295b203e2df06969793
import axios from "axios";

function AILegalAssistant() {
  const [prompt, setPrompt] = useState("");
  const [files, setFiles] = useState([]);
  const [response, setResponse] = useState("");
  const fileInputRef = useRef();  


  const handleFileChange = (e) => {
    // convert FileList to array
    setFiles(Array.from(e.target.files));
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append("prompt", prompt);

    files.forEach((file) => formData.append("files", file));
    try {
      const res = await axios.post(
        "http://127.0.0.1:5000/api/process",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      setResponse(res.data.result);
    } catch (err) {
      setResponse("Error: " + err.message);
    }
  };

  return (
    <section style={styles.container}>
      <div style={styles.overlay}>
        <h1 style={styles.mainTitle}>AI Legal Assistant</h1>
        <h3 style={styles.subTitle}>Simplify legal work through intelligent automation.</h3>

        <div style={styles.content}>
          {/* LEFT SIDE */}
          <div style={styles.leftSide}>
            <h2 style={styles.sectionTitle}>AI Response</h2>
            <div style={styles.responseBox}>
<<<<<<< HEAD
              {response || "AI response will appear here..."}
=======
              {response ? response : "Awaiting input..."}
>>>>>>> f73e62219f7a73237765f295b203e2df06969793
            </div>
          </div>

          {/* RIGHT SIDE */}
          <div style={styles.rightSide}>
            <h2 style={styles.sectionTitle}>Ask Lawgic</h2>
            <textarea
              placeholder="Type your prompt here..."
              style={styles.textInput}
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
            ></textarea>

<<<<<<< HEAD
              <input
                type="file"
                multiple
                style={{ display: "none" }}
                ref={fileInputRef}
                onChange={handleFileChange}
              />

              <button
                style={styles.fileButton}
                onClick={() => fileInputRef.current.click()}
              >
                Attach File(s)
              </button>

              <button style={styles.submitButton} onClick={handleSubmit}>
                Submit
              </button>
=======
            {/* Hidden file input */}
            <input
              type="file"
              multiple
              onChange={handleFileChange}
              style={{ display: "none" }}
              id="fileInput"
            />

            {/* Custom attach button */}
            <button
              style={styles.fileButton}
              onClick={() => document.getElementById("fileInput").click()}
            >
              Attach File(s)
            </button>

            {/* Submit button */}
            <button style={styles.submitButton} onClick={handleSubmit}>
              Submit
            </button>

            {/* Display selected filenames */}
            {files.length > 0 && (
              <ul style={styles.fileList}>
                {files.map((file, i) => (
                  <li key={i}>{file.name}</li>
                ))}
              </ul>
            )}
>>>>>>> f73e62219f7a73237765f295b203e2df06969793
          </div>
        </div>
      </div>
    </section>
  );
}

const styles = {
  container: {
    position: "relative",
    height: "100vh", // same height as Home
    backgroundImage: `url("https://www.you-fine.com/wp-content/uploads/2023/11/bronze-statue-for-sale-9.jpg")`,
    backgroundSize: "cover",
    backgroundPosition: "center",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    color: "white",
  },
  overlay: {
    backgroundColor: "rgba(0, 0, 0, 0.6)",
    width: "100%",
    height: "100%",
    padding: "60px 100px",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
  },
  mainTitle: {
    fontSize: "42px",
    textAlign: "center",
    marginBottom: "10px",
    fontFamily: "'Georgia', serif",
  },
  subTitle: {
    fontSize: "20px",
    textAlign: "center",
    marginBottom: "50px",
    fontFamily: "'Georgia', serif",
  },
  content: {
    display: "flex",
    justifyContent: "space-between",
    gap: "50px",
  },
  leftSide: {
    flex: 1,
  },
  rightSide: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    alignItems: "stretch",
  },
  sectionTitle: {
    fontSize: "24px",
    marginBottom: "15px",
    fontFamily: "'Georgia', serif",
  },
  responseBox: {
    backgroundColor: "rgba(255, 255, 255, 0.1)",
    border: "1px solid rgba(255, 255, 255, 0.3)",
    borderRadius: "8px",
    height: "250px",
    padding: "15px",
    overflowY: "auto",
  },
  textInput: {
    height: "100px",
    borderRadius: "8px",
    border: "none",
    padding: "10px",
    marginBottom: "15px",
    fontSize: "16px",
  },
  fileButton: {
    backgroundColor: "#8e4848ff",
    color: "white",
    border: "none",
    borderRadius: "8px",
    padding: "10px",
    cursor: "pointer",
    marginBottom: "10px",
  },
  submitButton: {
    backgroundColor: "#1b3099ff",
    color: "white",
    border: "none",
    borderRadius: "8px",
    padding: "10px",
    cursor: "pointer",
  },
  fileList: {
    marginTop: "10px",
    fontSize: "14px",
    listStyleType: "disc",
    paddingLeft: "20px",
  },
};

export default AILegalAssistant;