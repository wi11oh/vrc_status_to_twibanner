import configparser, glob, os, getpass, sys, time

from PIL import Image,ImageFont,ImageDraw
import tweepy



configfile = ".\\RVS2TB.Resources\\RVS2TB_config.ini"
config = configparser.ConfigParser()
config.read(configfile)

sendimage = ".\\RVS2TB.Resources\\sended.png"
API_KEY = config["twitter_authentication"]["API_KEY"]
API_KEY_SECRET = config["twitter_authentication"]["API_KEY_SECRET"]
ACCESS_TOKEN = config["twitter_authentication"]["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = config["twitter_authentication"]["ACCESS_TOKEN_SECRET"]

prev_CURRENT_STATUS = ""
prev_CURRENT_WORLD = ""
sendcount = 0



windows_fontfile = f"C:\\Users\\{getpass.getuser()}\\AppData\\Local\\Microsoft\\Windows\\Fonts\\"
emojifont_st = ImageFont.truetype("seguiemj.ttf", size=50, layout_engine=ImageFont)
status_font = ImageFont.truetype(f"{windows_fontfile}{config['letter_font']['status_letter_font']}", size=60, layout_engine=ImageFont)
geo_font = ImageFont.truetype(f"{windows_fontfile}{config['letter_font']['world_letter_font']}", size=20, layout_engine=ImageFont)
time_font = ImageFont.truetype(f"{windows_fontfile}{config['letter_font']['time_letter_font']}", size=10, layout_engine=ImageFont)




def main():
    global prev_CURRENT_STATUS
    global prev_CURRENT_WORLD
    global banner_base



    #画像読み込み
    banner_base = Image.open(".\\banner.png").convert("RGBA").resize((1500,500))
    img_clear = Image.new("RGBA", banner_base.size, (255, 255, 255, 0))
    fukidashi = Image.open(".\\RVS2TB.Resources\\fukidashi.png").convert("RGBA")



    #ログファイルのパスを取得
    file_list=glob.glob(f"C:\\Users\\{getpass.getuser()}\\AppData\\LocalLow\\VRChat\\VRChat\\output_log_*.txt")
    logfile = sorted(file_list, key=lambda f: os.stat(f).st_mtime, reverse=True)[0]
    print("ログファイル:" , logfile)



    #ログファイルをパース
    with open(logfile, "r" , encoding="utf-8") as f:
        lines = f.readlines()
    lines_strip = [line.strip() for line in lines ]



    #VRChatが終了しているか確認
    if len([i for i, line_s in enumerate(lines_strip) if "VRCApplication: OnApplicationQuit" in line_s ]) != 0:
        auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)#なんか怖いから中に入れてる
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        ImageDraw.Draw(fukidashi).text((178, 59), "⚪", embedded_color=True, font=emojifont_st)
        ImageDraw.Draw(fukidashi).text((265, 39), "offline", font=status_font, fill="black")
        img_clear.paste(fukidashi, (int(config["fukidashi_location"]["fukidashi_X"]), int(config["fukidashi_location"]["fukidashi_Y"])))
        banner_base = Image.alpha_composite(banner_base, img_clear)
        banner_base.save(sendimage)
        api.update_profile_banner(sendimage)
        print("VRCが終了しているので、Twitterのバナーをofflineにしました")
        sys.exit()



    #パースからステータスを抽出
    try:
        list_rownum = [i for i, line_s in enumerate(lines_strip) if "Update Status success status" in line_s ]
        CURRENT_STATUS = lines_strip[list_rownum[-1]].split(":")[-1]
        config["please_do_not_touch"]["prev_status"] = CURRENT_STATUS
        with open(configfile, "w") as f:
            config.write(f)
    except:
        CURRENT_STATUS = config["please_do_not_touch"]["prev_status"]



    #パースからワールド名を抽出
    try:
        list_rownum = [i for i, line_s in enumerate(lines_strip) if "Joining or Creating Room" in line_s ]
        if CURRENT_STATUS == "ask me":
            CURRENT_WORLD = "User is Online in a Private World (status)"
        elif CURRENT_STATUS == "busy":#なんか気分でaskとbusy分けちゃった
            CURRENT_WORLD = "User is Online in a Private World (status)"
        elif str(lines_strip[list_rownum[-1] - 3]).split("~")[1].split("(")[0] == "private":
            CURRENT_WORLD = "User is Online in a Private World (instance)"
        else:
            CURRENT_WORLD = str(lines_strip[list_rownum[-1]].split(":")[-1])[1:]
    except:#握りつぶし
        CURRENT_WORLD = "User is Online in a Private World (loading)"



    #ステータスとワールド名をデバッグ用に表示
    print("")
    print(nowtime:= time.strftime("%Y/%m/%d %H:%M ~"))
    print("ステータス　:" , CURRENT_STATUS)
    print("ワールド　　:" , CURRENT_WORLD)



    #PILで画像編集
    if CURRENT_STATUS == "active":
        STATUS_ICON = "🟢"#こういう指定の仕方多分良くない気がする
    elif CURRENT_STATUS == "busy":
        STATUS_ICON = "🔴"
        CURRENT_STATUS = "do not disturb"
    elif CURRENT_STATUS == "ask me":
        STATUS_ICON = "🟠"
    elif CURRENT_STATUS == "join me":
        STATUS_ICON = "🔵"
    else:
        STATUS_ICON = "⚪"

    ImageDraw.Draw(fukidashi).text((int(config["letter_location"]["status_icon_X"]), int(config["letter_location"]["status_icon_Y"])), STATUS_ICON, embedded_color=True, font=emojifont_st)
    ImageDraw.Draw(fukidashi).text((int(config["letter_location"]["status_letter_X"]), int(config["letter_location"]["status_letter_Y"])), CURRENT_STATUS, font=status_font, fill="black")
    ImageDraw.Draw(fukidashi).text((int(config["letter_location"]["world_letter_X"]), int(config["letter_location"]["world_letter_Y"])), CURRENT_WORLD, font=geo_font, fill="black")
    ImageDraw.Draw(fukidashi).text((int(config["letter_location"]["time_letter_X"]), int(config["letter_location"]["time_letter_Y"])), nowtime, font=time_font, fill="black")
    img_clear.paste(fukidashi, (100, 130))#なんかbanner_baseに透過貼ると突き抜けるからクリアのレイヤー入れてる
    banner_base = Image.alpha_composite(banner_base, img_clear)
    banner_base.save(sendimage)



    #画像をTwitterのバナーに設定
    def send2twitter():
        global prev_CURRENT_STATUS
        global prev_CURRENT_WORLD
        global sendcount
        auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        api.update_profile_banner(sendimage)

        prev_CURRENT_WORLD = CURRENT_WORLD
        prev_CURRENT_STATUS = CURRENT_STATUS
        sendcount += 1
        print("バナーを更新しました" , sendcount )

    if prev_CURRENT_STATUS == "":
        send2twitter()
    elif prev_CURRENT_WORLD == "": #要るか要らないか考えるのめんどいから入れてる
        send2twitter()
    elif prev_CURRENT_STATUS != CURRENT_STATUS or prev_CURRENT_WORLD != CURRENT_WORLD:
        send2twitter()
    else:
        print("前回更新と同じ内容っぽいので更新しないよ" , sendcount)
        pass




time.sleep(5)
while True:
    main()
    time.sleep(int(config["waittime"]["cycle_time"]))