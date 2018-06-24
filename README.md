# Andorid Messages for Desktop

![Andorid Messages Home Page](http://i.imgur.com/5g1VU3S.png)

A "native-like" desktop app for [Andorid Messages](https://www.allofordesktop.com/). This desktop app is supported by both [Nativefier](https://github.com/jiahaog/nativefier) and [Electron](https://github.com/electron/electron) version `^1.7.6`.

The Mac, Windows, and Linux apps can be downloaded from the [latest release](https://github.com/kelyvin/Android-Messages-Desktop-App/releases).

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
nativefier --platform "mac" --icon android-messages-logo.png --name "Android Messages" "https://messages.android.com/" --honest --disable-dev-tools --single-instance
```

### Windows
```
nativefier --platform "windows" --icon android-messages-logo.png --name "Android Messages" "https://messages.android.com/" --honest --disable-dev-tools --single-instance --tray
```

### Linux
```
nativefier --platform "linux" --icon android-messages-logo.png --name "Android Messages" "https://messages.android.com/" --honest --disable-dev-tools --single-instance
```
