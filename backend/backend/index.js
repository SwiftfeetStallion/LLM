const express = require("express");
const cors = require("cors");
const app = express();
const { PythonShell } = require("python-shell");

const pyshell = new PythonShell('./scripts/main.py');

app.use(cors());
app.use(express.json());


app.post("/send", async (request, response) => {
  pyshell.send(request.body.prompt);
  pyshell.send("end");

  let result = "";

  const promise = new Promise((resolve, reject) => {
    pyshell.on('message', (message) => {
      if (message === "end") { resolve(result); } 
      else { result += (message + "\n"); }
    });
    pyshell.on('error', error => reject(error));
  });

  promise.then((result) => {
    console.log(result);
    response.json(result);
  }).catch((error) => {
    console.error(error);
    response.status(500).send("error");
  });
  
})


app.listen(3001)
