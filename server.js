const express = require("express");
const bodyParser = require("body-parser");
const multer = require("multer");
const { google } = require("googleapis");
const fs = require("fs");

const app = express();
app.use(bodyParser.json());

// Configure Multer for File Uploads
const upload = multer({ dest: "uploads/" });

// Google Drive Authentication
const auth = new google.auth.GoogleAuth({
  keyFile: "path/to/service-account-key.json", // Replace with your JSON key file path
  scopes: ["https://www.googleapis.com/auth/drive.file"],
});

const drive = google.drive({ version: "v3", auth });

// API Endpoint to Upload to Google Drive
app.post("/api/upload", upload.single("file"), async (req, res) => {
  try {
    const fileMetadata = {
      name: req.file.originalname,
      parents: ["your-folder-id"], // Replace with your Google Drive folder ID
    };
    const media = {
      mimeType: req.file.mimetype,
      body: fs.createReadStream(req.file.path),
    };

    const response = await drive.files.create({
      resource: fileMetadata,
      media: media,
      fields: "id",
    });

    // Clean up local file
    fs.unlinkSync(req.file.path);

    res.json({
      success: true,
      message: "File uploaded successfully!",
      fileId: response.data.id,
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ success: false, message: "Failed to upload file." });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () =>
  console.log(`Server running on http://localhost:${PORT}`)
);
