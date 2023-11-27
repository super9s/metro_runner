import discord
import os
import subprocess

TOKEN = ""

with open("token.txt") as f:
    TOKEN = f.read().strip()

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True

class BotFlags:
    def __init__(self):
        self.isPaused = False

botFlags = BotFlags()

client = discord.Client(intents=intents)

adminIdList = [
    965827889499078656, # zkr
    345342072045174795, # みなと
]

adminNames = {
    965827889499078656: "zkr",
    345342072045174795: "みなと"
}

PREFIX = "m."

@client.event
async def on_ready():
    print('ログインしました')

@client.event
async def on_message(msg):
    if msg.author.bot:
        return

    print(msg.content)

    if msg.content.strip() == "<@983328971519311923>":
        if botFlags.isPaused:
            await msg.reply(f"一時停止中だよ。\n解除するなら、オーナーもしくは権限を持つ人に `{PREFIX}.resume` をしてもらってね。\n権限保持者一覧 = `{PREFIX}.oplist`")
            return
        
        await msg.reply(f"めとろらんなーだよ。コマンドは `{PREFIX}` で使えるよ。")
        return

    if msg.content.startswith("m."):
        com = msg.content[2:]

        if com.strip() == "":
            return

        if com == "help":
            await msg.reply(
"""
めとろらんなー
23/11/27 ~  (c) aoki

コマンド一覧 (`""" + PREFIX + """` で使えるよ) ：

- update
  metro のバイナリファイルをローカルのフォルダにある最終ビルドからコピーするよ。(権限が必要)

- pause
  一部コマンドを除いて、ボットの処理を一時停止するよ。(権限が必要)

- resume
  `pause` で止めた状態を解除するよ。(権限が必要)

- oplist
  権限を持っている人の一覧を表示するよ。

- eval
  metro のスクリプトを実行するよ

- help
  このメッセージを出すよ
"""
            )

        elif com == "resume":
            if not (msg.author.id in adminIdList):
                await msg.reply("`権限が必要なコマンドだよ`")
                return

            if not botFlags.isPaused:
                await msg.reply("一時停止されてないよ")
            else:
                botFlags.isPaused = False
                await msg.reply("解除しました")

        elif com == "oplist":
            await msg.reply("\n".join(adminNames.values()))

        elif botFlags.isPaused:
            return

        elif com == "pause":
            if not (msg.author.id in adminIdList):
                await msg.reply("`権限が必要なコマンドだよ`")
                return
            
            botFlags.isPaused = True
            await msg.reply(f"一時停止しました。`{PREFIX}resume` で解除します。")
            return
        
        elif com == "update":
            if not (msg.author.id in adminIdList):
                await msg.reply("`権限が必要なコマンドだよ`")
                return
            
            os.system("./update.sh")
            await msg.reply("実行ファイルを更新しました")

        elif com.startswith("eval"):
            script = com[4:].strip()

            if script.startswith("```"):
                script = script[3:-3]

            print(script)

            with open("test.metro", mode="w") as fs:
                fs.write(script)
            
            aa = subprocess.Popen("./metro", shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            stdout, stderr = aa.communicate()
            rt = aa.returncode

            stdout = stdout.decode()

            await msg.reply(f"```{stdout}```")

        else:
            await msg.reply("そんなコマンドないよ！")

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
