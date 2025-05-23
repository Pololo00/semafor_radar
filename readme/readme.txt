Hola, per executar aquest codi sera nessesari algunes coses especifiques.

primer de tot has de estar en una xarxa publica o privada si no esta limitada per el firewall,
hauras de instalar l'apalicacio thonny i arduino en el PC, a mes de descargarte les llibreries i el software del easOCR i un poseir un servidor de base de dades
un cop fet tot aixo hauras de posar el codi del archiu thonny.txt al software de l'aplicacio.
aquest haura de anar acompanyat de una placa ESP32 a poder ser una ESP32s si no hauras de modificarr part del thonny i colocar un led a la ESP32(si no disposes d'una ESP32s)
Amb arduino hauras de obrir el programa i anar a Archivos-->Ejemplos-->ESP32-->Camara-->WebCamaraServer
i obrir-ho aquest exemple es mes que suficient nomes hauras de fer 2 canvis, colocalr les credencials de la wifi
i habilitar el model de la camera en el meu cas una ESP32-CAM que el mes utilitzat es el AI_THINKER
un cop fet aixo i activada la camra i obtinguda la direccio ip del monitor serial d'arduino colocar-la alla on indican els comentaris del codi.

Ara amb lacamara funcionant amb una ip, i la ip de la camara colocada al seu lloc en el codi thonny i app.py
executa thonny i app.py i tambe et deixo per aqui la meva base de dades en un altre fitxer per que la puguis importar i executar ja que si no esta activa 
no es podra executar coorectament.

pd: red.txt l'hauras d'afeguir a la placa tambe, i els guardes els dos dintre de la placa per el seu us correctament.

