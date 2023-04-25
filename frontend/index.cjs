const { app, BrowserWindow } = require('electron')
const { join } = require('path')

app.on("ready", () => {
  const mainWindow = new BrowserWindow();
  mainWindow.loadFile(join(__dirname, "index.html"));
  mainWindow.webContents.openDevTools();
});
