import express from "express";
import fetch from "node-fetch";

const app = express();

app.get("/", (req, res) => {
  res.send("✅ m3u8 Proxy server is running on Render!");
});

app.get("/proxy", async (req, res) => {
  const targetUrl = req.query.url;
  if (!targetUrl) return res.status(400).send("Missing 'url' query parameter.");
  try {
    const response = await fetch(targetUrl);
    if (!response.ok) return res.status(response.status).send("Failed to fetch target m3u8 file.");
    const data = await response.text();
    res.setHeader("Content-Type", "application/vnd.apple.mpegurl");
    res.send(data);
  } catch (err) {
    console.error("Proxy error:", err);
    res.status(500).send("Proxy failed.");
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`🚀 Server is running on port ${PORT}`));