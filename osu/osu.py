import discord
from redbot.core import commands, Config, checks
import aiohttp
from redbot.core.utils.menus import menu, commands, DEFAULT_CONTROLS

BaseCog = getattr(commands, "Cog", object)

OSU_MODES = {"std":0, "taiko":1, "ctb":2, "mania":3}

class Osu(BaseCog):
    """Show stats from osu! api"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def osu(self, ctx, username, mode="std"):
        """Shows an osu! user"""

        apikey = await self.bot.get_shared_api_tokens("osu")

        if apikey is None or apikey == "":
            await ctx.send("You need to set an api key to use the osu! api, please use [p]osukey")
            return

        # Queries api to get osu profile
        headers = {"content-type": "application/json", "user-key": apikey}

        mode_id = OSU_MODES[mode]

        async with aiohttp.ClientSession() as session:
            async with session.post(f"https://osu.ppy.sh/api/get_user?k={apikey}&u={username}&m={mode_id}", headers=headers) as response:
                osu = await response.json()

        if osu:
            # Build Embed
            embed = discord.Embed()
            embed.title = osu[0]["username"]
            embed.url = "https://osu.ppy.sh/u/{}".format(osu[0]["user_id"])
            embed.set_footer(text="Powered by osu!")
            embed.add_field(name="Join date", value=osu[0]["join_date"][:10])
            embed.add_field(name="Accuracy", value=osu[0]["accuracy"][:6])
            embed.add_field(name="Level", value=osu[0]["level"][:5])
            embed.add_field(name="Ranked score", value=osu[0]["ranked_score"])
            embed.add_field(name="Rank", value=osu[0]["pp_rank"])
            embed.add_field(name="Country rank ({})".format(osu[0]["country"]), value=osu[0]["pp_country_rank"])
            embed.add_field(name="Playcount", value=osu[0]["playcount"])
            embed.add_field(name="Total score", value=osu[0]["total_score"])
            embed.add_field(name="Total seconds played", value=osu[0]["total_seconds_played"])
            embed.set_thumbnail(url="https://a.ppy.sh/{}".format(osu[0]["user_id"]))
            await ctx.send(embed=embed)
        else:
            await ctx.send("No results.")

    @commands.command()
    async def taiko(self, ctx, username, mode="taiko"):
        await self.osu(ctx, username, mode=mode)

    @commands.command()
    async def ctb(self, ctx, username, mode="ctb"):
        await self.osu(ctx, username, mode=mode)

    @commands.command()
    async def mania(self, ctx, username, mode="mania"):
        await self.osu(ctx, username, mode=mode)