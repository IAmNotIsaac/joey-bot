import tags

from command import CommandInfo, register_command
from gtts import gTTS


async def join(cmd: CommandInfo):
	pass
    # elif args[0].lower() == "join":
    #     id = 0
    #     if len(args) == 1:

    #         id = VCHANNEL_ID
    #     else:
    #         id = int(args[1])
    #     vchannel = discord.utils.get(client.get_all_channels(), id=id)
    #     await vchannel.connect()
register_command(join, tags.DEV_TODO, channel="v_channel")


    # elif args[0].lower() == "leave":
    #     if guild.voice_client:
    #         await guild.voice_client.disconnect()


    # elif args[0].lower() == "play":
    #     if guild.voice_client:
    #         voice = guild.voice_client
    #         source = discord.FFmpegPCMAudio(args[1])
    #         voice.play(source)


    # tts = gTTS(message, lang="en", tld="ca")
    # tts.save("_voice.mp3")

    # voice = guild.voice_client
    # source = discord.FFmpegPCMAudio("_voice.mp3")
    # voice.play(source)


    # elif args[0].lower() == "tts":
    #     if guild.voice_client:
    #         voice_message(" ".join(args[1:]))