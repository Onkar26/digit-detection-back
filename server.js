const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { exec } = require('child_process');
const util = require('util');
const fs = require('fs');

const app = express();

// Convert exec into a promise-based function
const execPromise = util.promisify(exec);

const imageProcess = async (img) => {

  // Example text data to write to the file
  const textData = img;

  // File path where you want to create the text file
  const filePath = 'image64.txt';

  // Write the text data to the file
  fs.writeFile(filePath, textData, (err) => {
    if (err) {
      console.error('Error writing to the file:', err);
    } else {
      console.log(`Text data has been written to ${filePath}`);
    }
  });

  const script = "python output.py";

  const { stdout, stderr } = await execPromise(script);

  if (stdout) {
    console.log('Python script output:', stdout);
    return stdout;
  } else {
    console.log('Python script errors:', stderr);
    return stderr;
  }
};

app.use(cors());
app.use(bodyParser.json());

app.post('/number', async (req, res) => {
  const base64Img = req.body.digitImage;
 
  const no = await imageProcess(base64Img);
  res.status(200).json({ number: no });
});

app.listen(3001, () => {
  console.log('Listening on port 3001');
});
