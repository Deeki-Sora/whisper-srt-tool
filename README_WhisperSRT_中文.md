# WhisperX 閫愯瘝瀛楀箷宸ュ叿

杩欏鑴氭湰鎶婃湰鏈洪煶棰戞垨瑙嗛杞崲涓虹編寮忚嫳璇€愯瘝鏃堕棿鎴?SRT銆傚瓧骞曡緭鍑哄湪婧愭枃浠跺悓鐩綍锛屽懡鍚嶄负锛?
    鍘熸枃浠跺悕.word_whisperx.srt

## 棣栨瀹夎

鍙屽嚮 install_whisper_srt.bat銆傝剼鏈細鍏堟鏌ュ綋鍓嶇郴缁熺殑 Python 鐜锛?
1. 濡傛灉绯荤粺 Python 宸插畨瑁?WhisperX銆乫aster-whisper銆丳yTorch 鍜?ctranslate2锛屽垯鐩存帴浣跨敤绯荤粺鐜锛屼笉鍒涘缓铏氭嫙鐜锛屼篃涓嶄細閲嶅瀹夎銆?2. 濡傛灉绯荤粺鐜缂哄皯渚濊禆锛岃剼鏈墠浼氬湪鏈洰褰曞垱寤?.venv锛屽苟鎶婁緷璧栧畨瑁呭埌璇ヨ櫄鎷熺幆澧冦€?
CUDA PyTorch 瀹夎鍖呰緝澶э紝寤鸿棰勭暀鑷冲皯 8 GB 纾佺洏绌洪棿銆?
## 浣跨敤鏂瑰紡

鍙屽嚮 run_whisper_srt.bat 鍚庢寜涓枃鎻愮ず杈撳叆鏂囦欢鎴栫洰褰曪紱涔熷彲浠ユ妸涓€涓垨澶氫釜鏂囦欢/鐩綍鎷栧埌 bat 鏂囦欢涓娿€傚惎鍔ㄨ剼鏈悓鏍蜂細浼樺厛閫夋嫨宸插叿澶囦緷璧栫殑绯荤粺 Python锛屽彧鏈夌郴缁熺幆澧冧笉鍙敤鏃舵墠閫夋嫨 .venv銆?
鍛戒护琛岀ず渚嬶細

    run_whisper_srt.bat "E:\Games\lol_guide\璁茶В.mp4"
    run_whisper_srt.bat "E:\Games\lol_guide\褰曢煶鐩綍" --recursive
    run_whisper_srt.bat "E:\Games\lol_guide\褰曢煶.flac" --overwrite

鏀寔甯歌鐨?wav銆乫lac銆乵p3銆乵4a銆乵p4銆乵kv銆乵ov銆亀ebm銆乷gg銆乷pus 绛夋牸寮忋€傞粯璁や娇鐢?RTX GPU 鍋?Whisper 杞綍锛屼娇鐢?CPU 鍋氬己鍒跺榻愪互闄嶄綆鏄惧瓨宄板€硷紱濡傛灉鏄惧瓨鍏呰冻锛屽彲浠ュ鍔?--align-device cuda銆傛樉瀛樹笉瓒虫椂灏?--batch-size 2 鎴?--batch-size 1銆?
绋嬪簭鍥哄畾浣跨敤 en 璇嗗埆锛屽苟鍦ㄦ彁绀鸿瘝涓姹?American English spelling銆傞€愯瘝鏃堕棿鎴虫潵鑷?WhisperX 鐨?forced alignment锛岀簿搴︿細鏄庢樉浼樹簬 Whisper 鍘熺敓浼拌锛屼絾浠嶅睘浜庢ā鍨嬪榻愮粨鏋滐紝涓嶆槸浜哄伐閫愬抚鏍囨敞銆?
