import logging as puts
import random

import re
import requests
import urllib

from discord.ext import commands

from util.helpers import (
    create_discord_file_object,
    generate_image_search_url,
    RANDOM_EXCEPTION_COMEBACKS as rec,
    validate_image,
)

from .config import (
    AVAILABLE_SPOILER_ACTIONS,
    DICTIONARY_PTBR_ENDPOINT,
    IMGUR_CLIENT_ID,
    YT_RESULTS_ENDPOINT,
    YT_WATCH_ENDPOINT,
)


@commands.command()
async def imgme(ctx, search_query, spoiler=None):
    try:
        url = generate_image_search_url(search_query)
        res = requests.get(url)
        search_result = res.json()
        if "items" not in search_result:
            raise Exception("We couldn't find any images for your search")

        image_is_valid = False

        for item in search_result["items"]:
            image_link = item["link"]
            image_is_valid, file_bytes = validate_image(image_link)
            if image_is_valid:
                f = create_discord_file_object(file_bytes, ".jpg", spoiler)
                await ctx.send(file=f)
                break

    except Exception as e:
        puts.info(e)
        await ctx.send(e)


@commands.command()
async def gifme(ctx, search_query, spoiler=None):
    try:
        url = generate_image_search_url(search_query, gif=True)
        res = requests.get(url)
        search_result = res.json()
        if "items" not in search_result:
            raise Exception("We couldn't find any images for your search")

        image_is_valid = False

        for item in search_result["items"]:
            image_link = item["link"]
            image_is_valid, file_bytes = validate_image(image_link)
            if image_is_valid:
                f = create_discord_file_object(file_bytes, ".jpg", spoiler)
                await ctx.send(file=f)
                break

    except Exception as e:
        puts.info(e)
        await ctx.send(e)


@commands.command()
async def youtube(ctx, *args):
    try:
        query_string = urllib.parse.urlencode({"search_query": " ".join(args)})
        html_content = urllib.request.urlopen("{}{}".format(YT_RESULTS_ENDPOINT, query_string))
        search_results = re.findall(
            r"href=\"\/watch\?v=(.{11})", html_content.read().decode()
        )
        await ctx.send("{}{}".format(YT_WATCH_ENDPOINT, search_results[0]))
    except BaseException as e:
        await ctx.send("Are you dumb?")


@commands.command()
async def dictionary(ctx, term, *args):
    try:
        endpoint = DICTIONARY_PTBR_ENDPOINT.format(term)
        r = requests.get(endpoint)
        result = r.json()
        print(result)

    except BaseException as e:
        await ctx.send("Are you dumb?")
