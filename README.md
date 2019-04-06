# Android Messages for Desktop

![Android Messages Home Page](https://i.imgur.com/OVKBkNY.png)

A "native-like" desktop app for [Android Messages](https://www.messagesfordesktop.com/). This desktop app is supported by both [Nativefier](https://github.com/jiahaog/nativefier) and [Electron](https://github.com/electron/electron) version `^1.7.6`.

The Mac, Windows, and Linux apps can be downloaded from the [latest release](https://github.com/kelyvin/Android-Messages-For-Desktop/releases).

## Purpose
The purpose of this project is to build dedicated native-like desktop apps for Android Messages and leverage your OS's built in notification system.

This desktop app and project is not an official product of Google and I am not affiliated with Google in any way.

## Rebuilding the app
Requires `nodejs`

### Nativefier
Install nativefier and make sure to have your [optional dependencies](https://github.com/jiahaog/nativefier#optional-dependencies) set up to replace the icon.
```
npm install -g nativefier
```

### Mac
```
nativefier --platform "mac" --icon android-messages-logo.png --name "Android Messages" "https://messages.google.com/web" --honest --disable-dev-tools --single-instance
```

### Windows
```
nativefier --platform "windows" --icon android-messages-logo.png --name "Android Messages" "https://messages.google.com/web" --honest --disable-dev-tools --single-instance --tray
```

### Linux
```
nativefier --platform "linux" --icon android-messages-logo.png --name "Android Messages" "https://messages.google.com/web" --honest --disable-dev-tools --single-instance
```

## Notifications on Windows
To receive notifications on Windows, you'll need to do the following:

1. Add a shortcut of this app to the Start Menu folder
2. In the "Windows Settings" app, check if the setting for "Show notifications in action center" is on (It might be off by default)


### For developers
These instructions were the result of an active issue with electron + Windows 8/10 and is resolved by setting `app.setAppUserModelId(process.execPath)` within `resources/app/lib/main.js` during electron initialization:

Example:

```javascript
const {app, shell} = electron;

app.setAppUserModelId(process.execPath);  // Include this line

function getFilenameFromMime(name, mime) {
  const exts = extName.mime(mime);
  ...
```

## Ubuntu Shortcut
Submitted by user [FlorentLM](https://github.com/kelyvin/Android-Messages-For-Desktop/issues/8), to create a shortcut for the Ubuntu launcher, please do the following:

1. Create and open the shortcut file
```bash
nano ~/.local/share/applications/Android-Messages.desktop
```

2. Copy and paste the following entry inside the file:

```ini
[Desktop Entry]
Version=1.0.0
Name=Android Messages
Comment=Send and recieve messages from your Android Phone
Keywords=Message;Messaging;Android;SMS
Exec=/path/to/installfolder/android-messages
Icon=/path/to/installfolder/resources/app/icon.png
Terminal=false
Type=Application
Categories=Internet;Application;
StartupWMClass=android-messages-nativefier-f3cfa3
```

Be sure to replace /path/to/installfolder/ with your actual installation folder and Android Messages should appear along your other native apps.
