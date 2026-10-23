# WhisperX 閫愯瘝瀛楀箷宸ュ叿

杩欏鑴氭湰鎶婃湰鏈洪煶棰戞垨瑙嗛杞崲涓虹編寮忚嫳璇€愯瘝鏃堕棿鎴?SRT銆傚瓧骞曡緭鍑哄湪婧愭枃浠跺悓鐩綍锛屽懡鍚嶄负锛?
    鍘熸枃浠跺悕.word_whisperx.srt

## 棣栨瀹夎

鍙屽嚮 install_whisper_srt.bat銆傝剼鏈細鍏堟鏌ュ綋鍓嶇郴缁熺殑 Python 鐜锛?
1. 濡傛灉绯荤粺 Python 宸插畨瑁?WhisperX銆乫aster-whisper銆丳yTorch 鍜?ctranslate2锛屽垯鐩存帴浣跨敤绯荤粺鐜锛屼笉鍒涘缓铏氭嫙鐜锛屼篃涓嶄細閲嶅瀹夎銆?2. 濡傛灉绯荤粺鐜缂哄皯渚濊禆锛岃剼鏈墠浼氬湪鏈洰褰曞垱寤?.venv锛屽苟鎶婁緷璧栧畨瑁呭埌璇ヨ櫄鎷熺幆澧冦€?
瀹夎鑴氭湰浼氬厛妫€娴?PATH 涓殑 python锛屽叾娆℃娴?py -3.11銆乸y -3锛屾渶鍚庢娴嬪伐鍏疯嚜宸辩殑 .venv锛涙湰鏈虹幆澧冨凡鍙敤鏃朵細鐩存帴璺宠繃瀹夎锛屼篃涓嶈姹傞澶栧畨瑁?py 鍚姩鍣ㄣ€傚垱寤烘柊鐜寤鸿浣跨敤 Python 3.11銆傞娆¤浆褰曞彲鑳介渶瑕佷笅杞?Whisper 鍙婅嫳璇榻愭ā鍨嬨€?
闊抽瑙ｇ爜闇€瑕?ffmpeg.exe 鍦?PATH 涓彲鐢紱鐜鎶ュ憡浼氭樉绀烘娴嬪埌鐨?FFmpeg 璺緞銆侰UDA PyTorch 瀹夎鍖呰緝澶э紝璇烽鐣欒冻澶熺殑瀹夎涓庢ā鍨嬬紦瀛樼┖闂淬€?
## 浣跨敤鏂瑰紡

鍙屽嚮 run_whisper_srt.bat 鍚庢寜涓枃鎻愮ず杈撳叆鏂囦欢鎴栫洰褰曪紱涔熷彲浠ユ妸涓€涓垨澶氫釜鏂囦欢/鐩綍鎷栧埌 bat 鏂囦欢涓娿€傚惎鍔ㄨ剼鏈悓鏍蜂細浼樺厛閫夋嫨宸插叿澶囦緷璧栫殑绯荤粺 Python锛屽彧鏈夌郴缁熺幆澧冧笉鍙敤鏃舵墠閫夋嫨 .venv銆?
鍛戒护琛岀ず渚嬶細

    run_whisper_srt.bat "E:\Games\lol_guide\璁茶В.mp4"
    run_whisper_srt.bat "E:\Games\lol_guide\褰曢煶鐩綍" --recursive
    run_whisper_srt.bat "E:\Games\lol_guide\褰曢煶.flac" --overwrite

鏀寔甯歌鐨?wav銆乫lac銆乵p3銆乵4a銆乵p4銆乵kv銆乵ov銆亀ebm銆乷gg銆乷pus 绛夋牸寮忋€傞粯璁や娇鐢?RTX GPU 鍋?Whisper 杞綍锛屼娇鐢?CPU 鍋氬己鍒跺榻愪互闄嶄綆鏄惧瓨宄板€硷紱濡傛灉鏄惧瓨鍏呰冻锛屽彲浠ュ鍔?--align-device cuda銆傛樉瀛樹笉瓒虫椂灏?--batch-size 2 鎴?--batch-size 1銆?
绋嬪簭鍥哄畾浣跨敤 en 璇嗗埆锛屽苟鍦ㄦ彁绀鸿瘝涓姹?American English spelling銆傞€愯瘝鏃堕棿鎴虫潵鑷?WhisperX 鐨?forced alignment锛屾椂闂磋竟鐣屾槸妯″瀷浼拌鍊硷紝涓嶈兘淇濊瘉姣忎釜鍗曡瘝閮芥绉掔骇鍑嗙‘銆?
## BAT 鍚姩鏁呴殰淇

濡傛灉绐楀彛鎻愮ず errorlevel銆乸ython.exe 鐨勯儴鍒嗗瓧绗︹€滀笉鏄唴閮ㄦ垨澶栭儴鍛戒护鈥濓紝鎴栬€呬腑鏂囦贡鐮侊紝璇风敤鏈増鏂囦欢瀹屾暣鏇挎崲鏃у伐鍏凤細

- 鎵€鏈?BAT 浣跨敤绾?ASCII銆佹棤 BOM 鍜?Windows CRLF 鎹㈣锛岄伩鍏?CMD 鎷嗗垎鍛戒护锛涗腑鏂囨彁绀虹敱 UTF-8 Python 鐣岄潰鏄剧ず銆?- .gitattributes 鍥哄畾 BAT 鐨?CRLF 鎹㈣銆備娇鐢ㄧ紪杈戝櫒淇敼 BAT 鍚庤淇濇寔 CRLF锛屼笉瑕佸彟瀛樹负 UTF-16銆?- 璇峰悓鏃朵繚鐣?select_python.bat 鍜?check_environment.py锛屽畠浠笌涓や釜鍏ュ彛 BAT 鏀惧湪鍚屼竴鐩綍銆?- 鏈満宸茶濂戒緷璧栨椂鐩存帴鍙屽嚮 run_whisper_srt.bat锛屾棤闇€閲嶆柊瀹夎鎴栧垹闄ゅ師瀛楀箷銆?
鍦ㄥ懡浠よ楠岃瘉鍚姩锛堜笉浼氬姞杞借浆褰曟ā鍨嬶級锛?
    run_whisper_srt.bat --help

鑷姩鍖栬皟鐢ㄦ椂鍙厛璁剧疆 WHISPERSRT_NO_PAUSE=1 浠ヨ烦杩囩粨鏉熸椂鐨勬寜閿殏鍋溿€侭AT 鐨勫畨瑁呯姸鎬佷俊鎭娇鐢ㄨ嫳鏂囷紱瀹為檯浜や簰鐣岄潰鍙婂弬鏁拌鏄庝娇鐢ㄤ腑鏂囥€?
