from discord.ext import commands
from discord.utils import get
from discord import Member, Embed, FFmpegPCMAudio
import os
import traceback
from gtts import gTTS
from tempfile import TemporaryFile


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))
    
    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel
        # we do not want the bot to reply to itself
        if message.author == self.bot.user:
            return
        if message.content.startswith('Hello darkness'):
            embed = Embed(title='',
                              description='',
                              colour=0x000000)
            embed.set_image(url='https://i.imgur.com/OsnmPRA.jpeg')
            await channel.send(content="I've come to talk with you again", embed=embed)

    @commands.command()
    async def hello(self, ctx, *, member: Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name}~'.format(member))
        else:
            await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
        self._last_member = member
        
        
    @commands.command()
    async def hi(self, ctx, *, member: Member = None):
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send("This is a tts message", tts=True)
        else:
            tts = gTTS(text='Hello', lang='en')
            f = TemporaryFile()
            tts.write_to_fp(f)
            
            FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            await self.join(ctx, voice)
            voice = get(bot.voice_clients, guild=ctx.guild)
            voice.play(FFmpegPCMAudio(f, **FFMPEG_OPTS), after=lambda e: print('done', e))
            voice.is_playing()
            f.close()
            
        self._last_member = member
        
    
    @commands.command()
    async def join(self, ctx, voice):
        channel = ctx.author.voice.channel

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect() 

        
bot = commands.Bot(command_prefix='/')
bot.add_cog(Greetings(bot))
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')
    

bot.run(token)
