import './App.css';
import React from 'react';
import { useState } from 'react';
import axios from "axios";

const App = () => {
  const [content,setContent] = useState("");
  const [label,setLabel] = useState("");

  const onSubmit = (event) => {
    event.preventDefault();
    getLog(label);
  }

  const getLog = async (ip) => {
    try {
        const response = await axios.post('https://m6ats01hfh.execute-api.us-east-1.amazonaws.com/log_analyzer', { "ip": ip })
        setContent(response.data.urls_count);
    }
    catch (errEx) {
        setContent("");
    }
  }

  const handleChange = (event) => {
    setLabel(event.target.value);
    setContent("")
  }

  return (
    <React.Fragment>
      <form onSubmit={onSubmit}>
        <label>
          Insert an IP address (x.x.x.x):<br/>
          <input type="text" id="ip" title='ip' value={label} onChange={handleChange}/>
        </label>
        <br/>
        <button type="submit">Try it!</button>
        <br/>
      </form>
      <br/>
      <React.Fragment>
      {
        content !== "" && Object.keys(content).length > 0 &&
          <React.Fragment>
            Results for ip {label}:<br/>
            <table border={1}>
              <thead>
                <tr>
                  <td><b>URL</b></td>
                  <td><b>Count</b></td>
                </tr>
              </thead>
              <tbody>
                {Object.keys(content).map((key, i) => (
                <tr key={i}>
                  <td>{key}</td>
                  <td> {content[key]}</td>
                </tr>))}
              </tbody>
            </table>
          </React.Fragment>
      }
      </React.Fragment>
      <React.Fragment>
      {
        content !== "" && Object.keys(content).length === 0 &&
          <React.Fragment>
            No rows found for ip {label}:<br/>
          </React.Fragment>
      }
      </React.Fragment>
    </React.Fragment>
  );
}

export default App;
