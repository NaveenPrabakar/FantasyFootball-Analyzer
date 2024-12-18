import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [testData, setTestData] = useState("");
  const [response, setResponse] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  //On open
  const handleTrain = async () => {
    if (!file) {
      alert("Please upload a CSV file.");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://127.0.0.1:8000/train/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResponse(res.data);
    } catch (error) {
      alert("Error training model: " + error.response.data.detail);
    }
  };


  //Button
  const handleTest = async () => {
    if (!testData) {
      alert("Please enter test data.");
      return;
    }

    const features = testData.split(",").map(Number);

    try {
      const res = await axios.post("http://127.0.0.1:8000/test/", {
        features: features,
      });
      setResponse(res.data);
    } catch (error) {
      alert("Error testing model: " + error.response.data.detail);
    }
  };

  //CSS for the styling of the website
  const styles = {
    container: {
      fontFamily: "Verdana, sans-serif",
      maxWidth: "800px",
      margin: "auto",
      padding: "20px",
      borderRadius: "8px",
      backgroundColor: "#003B1F", // Dark green, like a football field
      color: "#FFFFFF",
      boxShadow: "0 4px 10px rgba(0, 0, 0, 0.2)",
    },
    header: {
      textAlign: "center",
      fontSize: "2em",
      fontWeight: "bold",
      padding: "10px",
      borderBottom: "3px solid #FFB612", // Gold, mimicking goal posts
    },
    section: {
      margin: "20px 0",
      padding: "10px",
      border: "2px solid #FFFFFF",
      borderRadius: "6px",
      backgroundColor: "#145A32", // Lighter green for contrast
    },
    input: {
      width: "100%",
      padding: "10px",
      margin: "10px 0",
      border: "2px solid #FFB612",
      borderRadius: "4px",
      backgroundColor: "#FFFFFF",
      color: "#003B1F",
    },
    button: {
      backgroundColor: "#FFB612",
      color: "#003B1F",
      border: "none",
      padding: "12px 24px",
      margin: "10px 0",
      borderRadius: "6px",
      cursor: "pointer",
      fontWeight: "bold",
    },
    buttonDisabled: {
      backgroundColor: "#666666",
      color: "#FFFFFF",
      border: "none",
      padding: "12px 24px",
      margin: "10px 0",
      borderRadius: "6px",
      cursor: "not-allowed",
      fontWeight: "bold",
    },
    responseBox: {
      padding: "10px",
      border: "2px solid #FFFFFF",
      borderRadius: "6px",
      backgroundColor: "#FFFFFF",
      color: "#003B1F",
      overflowX: "auto",
    },
    fieldLines: {
      position: "relative",
      marginBottom: "20px",
      borderBottom: "2px dashed #FFFFFF",
      paddingBottom: "10px",
    },
    titleIcon: {
      display: "inline-block",
      backgroundColor: "#FFB612",
      color: "#003B1F",
      padding: "5px 10px",
      borderRadius: "50%",
      marginRight: "10px",
      fontWeight: "bold",
    },
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.header}>🏈 NFL Player Predication 🏈</h1>

      <div style={styles.section}>
        <div style={styles.fieldLines}>
          <span style={styles.titleIcon}>1</span>
          Upload Training Data
        </div>
        <input type="file" onChange={handleFileChange} style={styles.input} />
        <button
          onClick={handleTrain}
          style={file ? styles.button : styles.buttonDisabled}
          disabled={!file}
        >
          Train Model
        </button>
      </div>

      <div style={styles.section}>
        <div style={styles.fieldLines}>
          <span style={styles.titleIcon}>2</span>
          Test the Model
        </div>
        <input
          type="text"
          placeholder="Enter features, e.g., 1.2,3.4,5.6"
          value={testData}
          onChange={(e) => setTestData(e.target.value)}
          style={styles.input}
        />
        <button
          onClick={handleTest}
          style={testData ? styles.button : styles.buttonDisabled}
          disabled={!testData}
        >
          Test Model
        </button>
      </div>

      <div style={styles.section}>
        <div style={styles.fieldLines}>
          <span style={styles.titleIcon}>3</span>
          Response
        </div>
        {response && (
          <div style={styles.responseBox}>
            <pre>{JSON.stringify(response, null, 2)}</pre>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
