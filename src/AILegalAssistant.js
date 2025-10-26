import React, {useState} from "react";
import axios from "axios";

function AILegalAssistant() {
  const [prompt, setPrompt] = useState("");
  const [files, setFiles] = useState([]);
  const [response, setResponse] = useState("");

  const handleFileChange = (e) => {
    setFiles(e.target.files);
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append("prompt", prompt);

    for (let i = 0; i < files.length; i++) {
      formData.append("files", files[i]);
    }

    try {
      const res = await axios.post("http://127.0.0.1:5000/api/process", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResponse(res.data.result);
    } catch (err) {
      setResponse("Error: " + err.message);
    }
  };
  return (
    <section style={styles.container}>
      <div style={styles.overlay}>
        <h1 style={styles.mainTitle}>AI Legal Assistant</h1>
        <h3 style={styles.subTitle}>Streamline your legal workflow with AI</h3>

        <div style={styles.content}>
          {/* LEFT SIDE */}
          <div style={styles.leftSide}>
            <h2 style={styles.sectionTitle}>AI Response</h2>
            <div style={styles.responseBox}>
              {/* This box will later display AI responses */}
            </div>
          </div>

          {/* RIGHT SIDE */}
          <div style={styles.rightSide}>
            <h2 style={styles.sectionTitle}>Ask Lawgic</h2>
            <textarea
              placeholder="Type your prompt here..."
              style={styles.textInput}
            ></textarea>

            <button style={styles.fileButton}>Attach File(s)</button>
            <button style={styles.submitButton}>Submit</button>
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
    backgroundImage: `url("https://www.you-fine.com/wp-content/uploads/2023/11/bronze-statue-for-sale-9.jpg")`, // <-- replace with your own image URL
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
    fontFamily: "'Arial', sans-serif",
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
};

export default AILegalAssistant;