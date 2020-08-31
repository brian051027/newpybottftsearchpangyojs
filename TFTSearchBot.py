import discord
import asyncio
import os
from discord.ext import commands
import urllib
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.request import urlopen
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib.parse import quote
import re # Regex for youtube link
import warnings
import requests
import unicodedata
import time
client = discord.Client()
token = "NzQ4MzYwOTQ2NDk3NDg2OTQy.X0cTcQ.uJmCtOxHCV3CRUAuhNm_pedoy0o"

def returnStatsTFT(bs):
    # 통계 정보
    InfoText = []
    statsInfo = bs.findAll('span', {'class': 'profile__tier__stat__value float-right'})
    for sI in statsInfo:
        InfoText.append(sI.text.strip())

    InfoText = InfoText[:5]
    # InfoText List value in place order
    # [Number of win,Win Rate,Top 4,Top4 Rate, Total Game,Average place]
    return InfoText

def returnStatsPercentage(bs):
    InfoText = []
    statsPercentage = bs.findAll('span',{'class' : 'profile__tier__stat__text'})
    for sP in statsPercentage:
        InfoText.append(sP.text.strip())
    return InfoText



@client.event # Use these decorator to register an event.
async def on_ready(): # on_ready() event : when the bot has finised logging in and setting things up
    await client.change_presence(status=discord.Status.online, activity=discord.Game("나는야 따까리이자 롤검색이 ㅋ"))
    print("New log in as {0.user}".format(client))

@client.event
async def on_message(message): # on_message() event : when the bot has recieved a message
    #To user who sent message
    # await message.author.send(msg)
    print(message.content)
    if message.author == client.user:
        return

    if message.content.startswith("!롤체전적"):
        try:
            krTFTProfileURL = 'https://lolchess.gg/profile/kr/'
            playerNickname = ''.join((message.content).split(' ')[1:])
            playerNicknameShow = ' '.join((message.content).split(' ')[1:])
            playerInfoURL = krTFTProfileURL + quote(playerNickname)
            html = urlopen(playerInfoURL)
            bs = BeautifulSoup(html, 'html.parser')

            # 닉네임이 입력되지 않은 경우
            if len(message.content.split(" ")) == 1:
                embed = discord.Embed(title="닉네임이 입력되지 않았습니다", description="", color=0x5CD1E5)
                embed.add_field(name="Player nickname not entered",
                                value="To use command !롤체전적 : !롤체전적 (Nickname)", inline=False)
                embed.set_footer(text='by 설준서.',
                                     icon_url='https://attach.s.op.gg/forum/20170922204322_434504.png')
                await message.channel.send("Error : Incorrect command usage ", embed=embed)


            elif bs.find('div', {'class': 'profile__tier__icon'}).img['alt'] == 'Unranked':
                # 티어 아이콘 URL
                tierIcon = 'https:' + bs.find('div', {'class': 'profile__tier__icon'}).img[
                    'src']  # Unranked -> 배치안된경우 필터링

                # 티어 정보
                tierInfo = bs.find('div', {'class': 'profile__tier__icon'}).img['alt']

                #Most Syergy
                embedSynergy = True
                mostSyn = bs.find('div', {'class': 'profile__recent__trends__traits'})
                synergyInfo = []
                if mostSyn == None:
                    embedSynergy = False
                    pass
                else:
                    mostSyn = mostSyn.table.tbody.findAll('tr')[0].findAll('td')
                    for sf in mostSyn:
                        synergyInfo.append(sf.text.strip())


                statsli = returnStatsTFT(bs)
                embed = discord.Embed(title="Team Fight Tactics player stats from lolchess.gg", description="", color=0x5CD1E5)
                embed.add_field(name="Click on the link below to view more information",
                                value=playerInfoURL,
                                inline=False)
                embed.add_field(name="Rank Information",
                                value=tierInfo + "(Unable to find Raiting & Ranking Info)",
                                inline=False)
                if mostSyn:
                    embed.add_field(name="Most used Synergy : " + synergyInfo[0],
                                    value="Use : " + synergyInfo[4] + " time(s) | " + "1st place Ratio : " +
                                          synergyInfo[-2] + " | Top4 Ratio : " + synergyInfo[-1],
                                    inline=False)
                else:
                    pass
                embed.add_field(name="Number of Win(#1)",
                                value=statsli[0] + "/Top 0.00%",
                                inline=True)
                embed.add_field(name="Win Ratio",
                                value=statsli[1] + "/Top 0.00%",
                                inline=True)
                embed.add_field(name="Number of Top 4(#4)",
                                value=statsli[2] + "/Top 0.00%",
                                inline=True)
                embed.add_field(name="Top 4 Ratio",
                                value=statsli[3] + "/Top 0.00%",
                                inline=True)
                embed.add_field(name="Number of game",
                                value=statsli[4] + "/Top 0.00%",
                                inline=True)
                embed.add_field(name="Average Place",
                                value="NaN",
                                inline=True)
                embed.set_thumbnail(url=tierIcon)
                embed.set_footer(text='by 설준서.',
                                     icon_url='https://attach.s.op.gg/forum/20170922204322_434504.png')
                await message.channel.send("TFT player " + playerNicknameShow + "'s information search", embed=embed)


            else:
                # 티어 정보
                tierInfo = bs.find('div', {'class': 'profile__tier__icon'}).img['alt']
                # 티어 아이콘 URL
                tierIcon = 'https:' + bs.find('div', {'class': 'profile__tier__icon'}).img[
                    'src']  # Unranked -> 배치안된경우 필터링

                # 티어 정보
                tierInfo = bs.find('div', {'class': 'profile__tier__icon'}).img['alt']
                # lp
                lpInfo = bs.find('span', {'class': 'profile__tier__summary__lp'}).text
                # 상위 백분율
                toppercent = bs.find('span', {'class': 'top-percent'}).text.strip()
                # 전체 등수
                rankplace = bs.find('span', {'class': 'rank-region'}).text.strip()
                statsli = returnStatsTFT(bs)
                satatsPercentage = returnStatsPercentage(bs)

                #Most used Synergy

                mostSyn = bs.find('div',{'class' : 'profile__recent__trends__traits'}).table.tbody.findAll('tr')[0]
                synergyName = mostSyn.findAll('td')
                synergyInfo = []
                for sf in synergyName:
                    synergyInfo.append(sf.text.strip())

                #[Synergy Name , 1성조합횟수,2성조합횟수,3성조합횟수,게임수,승률(=1등),Top비율 (=Top4비율)]


                AveragePlace = bs.find('dl', {'class': re.compile('average average-[0-9]*')}).dd.text
                recentNumberofGame = bs.find('div', {'class': 'profile__placements'}).h4.text.strip()
                embed = discord.Embed(title="Team Fight Tactics player stats from lolchess.gg", description="", color=0x5CD1E5)
                embed.add_field(name="Click on the link below to view more information",
                                value=playerInfoURL,
                                inline=False)
                embed.add_field(name="Rank Information",
                                value=tierInfo + "(" + lpInfo + ")" + " | " + toppercent + " | " + "Ranking : " + rankplace,
                                inline=False)
                embed.add_field(name="Most used Synergy : "+synergyInfo[0],
                                value="Use : "+synergyInfo[4] + " time(s) | " + "1st place Ratio : " + synergyInfo[-2] + " | Top4 Ratio : " + synergyInfo[-1],
                                inline=False)
                embed.add_field(name="Number of Win(#1)",
                                value=statsli[0] + "/" + satatsPercentage[0],
                                inline=True)
                embed.add_field(name="Win Ratio",
                                value=statsli[1] + "/" + satatsPercentage[1],
                                inline=True)
                embed.add_field(name="Number of Top 4(#4)",
                                value=statsli[2] + "/" + satatsPercentage[2],
                                inline=True)
                embed.add_field(name="Top 4 Ratio",
                                value=statsli[3] + "/" + satatsPercentage[3],
                                inline=True)
                embed.add_field(name="Number of game",
                                value=statsli[4] + "/" + satatsPercentage[4],
                                inline=True)
                embed.add_field(name="Average Place",
                                value=AveragePlace,
                                inline=True)
                embed.set_thumbnail(url=tierIcon)
                embed.set_footer(text='by 설준서.',
                                     icon_url='https://attach.s.op.gg/forum/20170922204322_434504.png')
                await message.channel.send("TFT player " + playerNicknameShow + "'s information search", embed=embed)
        except AttributeError as e:
            embed = discord.Embed(title="Nick name not exist", description="", color=0x5CD1E5)
            embed.add_field(name="해당 닉네임의 플레이어가 존재하지 않습니다.",value="플레이어 이름을 확인해 주세요",inline=False)
            embed.set_footer(text='by 설준서.',
                                     icon_url='https://attach.s.op.gg/forum/20170922204322_434504.png')
            await message.channel.send("Error : Not existing nickname", embed=embed)

client.run(token)
