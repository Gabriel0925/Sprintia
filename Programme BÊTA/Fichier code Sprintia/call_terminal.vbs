' Script VBS pour lancer Sprintia.bat sans afficher la console
Set WshShell = CreateObject("WScript.Shell")
' Le ", 0" permet de lancer la commande en mode caché
WshShell.Run """" & WScript.ScriptFullName & "\..\launch_app.bat" & """", 0
