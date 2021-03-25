print("Running twitter_for_discord")
import os
import sys
import time
import discord
import urllib.request
import urllib.error
import time
import requests
import tweepy

#cmdでpip listを入力し、os,sys,time,discord,urllib.request,urllib.error,time,requests,tweepyがインストールされていることを確認してください。
#インストールされてない場合、pip install の後にimportの後に書いてあるものを入力し、インストールしてください。cmdは管理者権限で実行することをお勧めします。

TOKEN = '' #Discord developersサイトでアプリを作成してbotのトークンを''の中に入力してください。

client = discord.Client()

CHANNEL_ID = #Discordでチャンネルを右クリックするとIDがコピーできるので「=」の直後にペーストしてください。（開発者用の設定をオンにしてください。）

#ログイン処理
async def greet():
    channel = client.get_channel(CHANNEL_ID)
    await client.change_presence(activity=discord.Game(name='Twitter for Discord'))
    print("ログインしました。\n")
    await channel.send('ログインしました。')
#ログイン処理終了

@client.event
async def on_ready():
    await greet()

@client.event
async def on_message(message):
    if message.author.bot:
        return

    def check(msg):
        return msg.author == message.author
     
    if message.content == '/login':
        if message.author.guild_permissions.administrator:
            await message.channel.send('ログイン認証...')

            API_KEY='' #Twitter Developersで生成したアプリのapi_keyを''の中に入力してください。
            API_KEY_SECRET='' #Twitter Developersで生成したアプリのapi_key_secretを''の中に入力してください。

            def get_oauth_token(url:str)->str:
                querys = urllib.parse.urlparse(url).query
                querys_dict = urllib.parse.parse_qs(querys)
                return querys_dict["oauth_token"][0]

            auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)

            redirect_url = auth.get_authorization_url()

            oauth_token = get_oauth_token(redirect_url)
            auth.request_token['oauth_token'] = oauth_token

            auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
            api = tweepy.API(auth)
            redirect_url = auth.get_authorization_url()
            redirect_url
            print(redirect_url)

            await message.channel.send(redirect_url)

            await message.channel.send('PINを入力してください。')

            def check(msg):
                return msg.author == message.author

            verifier = await client.wait_for("message", check=check)
            print(verifier.content)

            verfire_code = await message.channel.send(verifier.content)
            await verfire_code.add_reaction('🤔')

            auth.request_token['oauth_token_secret'] = verifier.content

            try:
                auth.get_access_token(verifier.content)
            except tweepy.TweepError:
                print("アクセストークンの入手に失敗しました。")

            with open("auth_info.txt",mode="w") as file:
                text = "key:{}\nsecret:{}".format(auth.access_token,auth.access_token_secret)
                file.write(text)


            if auth.access_token is None :
                if auth.access_token_secret is None :
                    print('PINコードが間違っています。')
                    await message.channel.send('PINを入力してください。')
                    return
            else:
                auth.set_access_token(auth.access_token, auth.access_token_secret)

                print("access_token:",auth.access_token)
                print("access_token_secret",auth.access_token_secret)

                print("認証が完了しました。")
                await message.channel.send("認証が完了しました。")
                await message.channel.send("ログインが完了しました。")

                api = tweepy.API(
                    auth,
                    wait_on_rate_limit=True,
                    wait_on_rate_limit_notify=True
                )

                me = api.me()
                print('ようこそ',me.name,me.screen_name)
                
                
                img = api.get_user(me.screen_name)
                url = img.profile_image_url_https

                await message.channel.send('ようこそ')
                embed_message = discord.Embed(title=me.name,description=me.screen_name,color=0xff0000)
                embed_message.set_thumbnail(url=url)
                await message.channel.send(embed=embed_message)

                while True :

                    def check(msg):
                        return msg.author == message.author
    
                    command_discord = await client.wait_for("message", check=check)

                    if message.author.bot:
                            return
                    if command_discord.content == '/tweet':
                        await message.channel.send('ツイートする内容を送信してください。')
                        wait_message = await client.wait_for("message",check=check)
                        api.update_status(wait_message.content)
                        print("ツイートを送信しました。→"+wait_message.content)
                        await message.channel.send('ツイートを送信しました。')
                    elif command_discord.content == '/purge':
                        channel = client.get_channel(CHANNEL_ID) #CHANNEL_IDを任意のチャンネルIDに入れ替えてください。
                        await channel.purge(limit=None)
                        await message.channel.send('メッセージ履歴をすべて削除しました。(˙◁˙)ﾊﾟｱ')
                        time.sleep(1.5)
                        await channel.purge(limit=None)
                    elif command_discord.content == '/logout':
                        await message.channel.send('ログアウトしました。')
                        break
        else :
            await message.channel.send('管理者権限がない者は実行できません。')
    elif message.content == '/purge':
        if message.author.guild_permissions.administrator:
            channel = client.get_channel(CHANNEL_ID) #ここも同じくCHANNEL_IDを任意のIDに入れ替えてください。
            await message.channel.send('履歴をすべて削除しますか？y/n')
            y_n = await client.wait_for("message",check=check)
            print(y_n.content)
            if y_n.content == 'y':
                await channel.purge(limit=None)
                await message.channel.send('メッセージ履歴をすべて削除しました。(˙◁˙)ﾊﾟｱ')
                time.sleep(1.5)
                await channel.purge(limit=None)
            elif y_n.content == 'Y':
                await channel.purge(limit=None)
                await message.channel.send('メッセージ履歴をすべて削除しました。(˙◁˙)ﾊﾟｱ')
                time.sleep(1.5)
                await channel.purge(limit=None)
            elif y_n.content == 'n':
                await message.channel.send('キャンセルしました。(˙◁˙)ﾊﾟｱ')
            elif y_n.content == 'N':
                await message.channel.send('キャンセルしました。(˙◁˙)ﾊﾟｱ')
            else :
                await message.channel.send('デフォルトは「n」なのでキャンセルしました。(˙◁˙)ﾊﾟｱ')
        else :
            await message.channel.send('管理者権限がない者は実行できません。')
    elif message.content.startswith == ('/'):
        if message.author.bot:
            return
        await message.channel.send('そのコマンドは存在しません')

client.run(TOKEN)