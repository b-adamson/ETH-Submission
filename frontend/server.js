const express = require("express");
const fs = require("fs");
const cors = require("cors");
const {spawn} = require('child_process')

const app = express();
const PORT = 5500;

app.use(express.json());
app.use(cors());

// Route to save search data
app.post("/save-search", (req, res) => {
    const searchQuery = req.body.search;

    fs.readFile("frontend/data/searches.json", "utf8", (err, data) => {
        let searches = [];

        if (!err && data) {
            searches = JSON.parse(data);
        }

        searches = [];
        searches.push({name: searchQuery});

        fs.writeFile("frontend/data/searches.json", JSON.stringify(searches, null, 2), (err) => {
            if (err) {
                return res.status(500).json({ error: "Failed to save search" });
            }
            res.json({ message: "Search saved!", searches });
        });

        const pythonProcess = spawn('python', ['src/main.py']).on('close', () => {
            // if (fs.existsSync("src/data/metadata.json")) {
            // console.log("Metadata file found. Proceeding with the server setup...");
            // res.redirect("/coins");
            // res.end();
            app.get("/coins", (req, res) => {
                fs.readFile("src/data/metadata.json", "utf8", (err, data) => {
                    if (err) {
                        return res.status(500).json({ error: "Failed to load data" });
                    }
                    res.json(JSON.parse(data));
                });
            });
        });;
        pythonProcess.stdout.on('data', (data) => {
            console.log(`stdout: ${data.toString()}`);
        });
        console.log(1);
        
    });
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});