import discord
import requests
from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands


class Welcome(commands.Cog):
    """This will contain everything relating to data"""

    def __init__(self, bot):
        self.bot = bot

    def download_image(self, url):

        temp_file = 'data/temp.png'
        with open(temp_file, 'wb') as handle:
            response = requests.get(url, stream=True)
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
        return Image.open(temp_file).convert('RGB')

    def create_welcome(self, user):
        avatar_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(user)
        avatar = self.download_image(avatar_url)

        base = Image.new('RGBA', (9120, 4000), (0, 0, 0, 255))
        backround = Image.open("data/images/backround0.jpg").convert('RGBA')
        base.paste(backround, (0, 2000))
        base = base.resize((700, 250))

        # Masking out user avatar to circle
        mask = Image.new('L', avatar.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + avatar.size, fill=255)
        mask = mask.resize(avatar.size, Image.ANTIALIAS)
        avatar.putalpha(mask)
        # adding avatar to base
        base.paste(avatar, (50, 125 - int(float(avatar.size[1]) / 2)), avatar)
        # adding text to base
        fnt = ImageFont.truetype('/data/fonts/impact.ttf', 40)
        d = ImageDraw.Draw(base)
        d.text((230, 125 - int(float(avatar.size[1]) / 2)), "Hello " + user.name + ",\nWelcome to Inferno Games!",
               font=fnt, fill=(255, 255, 255, 255))
        # saving base
        temp_file = 'data/temp.png'
        base.save(temp_file)
        return temp_file

    # @commands.command()
    async def testwelcome(self, ctx):
        member = ctx.message.author
        await ctx.message.delete()

        file = discord.File(self.create_welcome(member))
        await ctx.send(files=[file])


    @commands.Cog.listener()
    async def on_member_join(self, member):
        # TODO add rule prompt
        #TODO add handling of kicked or temp baned users re entering
        channel = member.guild.system_channel
        file = discord.File(self.create_welcome(member))
        if channel is not None:
            await channel.send(files=[file])



def setup(bot):
    bot.add_cog(Welcome(bot))