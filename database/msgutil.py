import database.util as dbutil


async def send_long_msg(content, ctx, in_cb=False, max_size=1500):
    tokens = []
    """Breaks long chunks of text into somthing that can be sent by a message"""
    msg_arr = content.split(" ")
    if len(msg_arr) == 0:
        msg_arr = [content]

    if in_cb:
        msg_str = "```"
    else:
        msg_str = ""

    for i in msg_arr:

        if len(msg_str + i) > max_size:
            if len(i) > max_size:
                str2 = ""
                for l in i:
                    if len(str2) >= max_size:
                        tokens.append(str2)
                        str2 = ""
                    str2 += l

            if in_cb:
                msg_str += "```"
                tokens.append(msg_str)
                msg_str = "```"
            else:
                tokens.append(msg_str)
                msg_str = ""
        else:
            msg_str += i + " "

    if len(msg_str):
        if in_cb:
            msg_str += "```"
        tokens.append(msg_str)
    for i in tokens:
        print(i)
        await ctx.send(i)


async def print_message_groups(offending_msg_groups, ctx, bot, padding=3):
    for li in offending_msg_groups:

        channel = (await bot.fetch_channel(li[0].channel)).name
        await ctx.send("**In " + channel + "** around " + str(li[0].timestamp))

        if len(li) > 5:
            msg_block1 = []
            msg_block2 = []
            for r in dbutil.get_messages_above(li[0], padding):
                msg_block1.append(r)

            msg_block1.append(li[0])

            msg_block2.append(li[-1])
            for r in dbutil.get_messages_below(li[0], padding):
                msg_block2.append(r)
            final_str = "```md\n"

            for m in msg_block1:
                att_txt = ""
                author = (await bot.fetch_user(m.author)).name
                content = m.content[:80] + (m.content[80:] and '...')
                attachments = dbutil.get_message_attachments(m)
                count = 0
                count = 0
                for r in dbutil.get_message_attachments(m):
                    count += 1
                if count:
                    att_txt = "<" + str(count) + "_Attachments>"
                if m in li:
                    final_str += "[" + author + "](" + m.content + ")\t" + att_txt + "\n"
                else:
                    final_str += "< " + author + " >:" + m.content + "\t" + att_txt + "\n"
                if len(final_str) > 1500:
                    final_str += "```"
                    await ctx.send(final_str)
                    final_str = "```md\n"
            if len(final_str) > 1500:
                final_str += "```"
                await ctx.send(final_str)
                final_str = "```md\n"

            for m in msg_block2:
                att_txt = ""
                author = (await bot.fetch_user(m.author)).name
                content = m.content[:80] + (m.content[80:] and '...')
                attachments = dbutil.get_message_attachments(m)
                count = 0
                for r in dbutil.get_message_attachments(m):
                    count += 1
                if count:
                    att_txt = "<" + str(count) + "_Attachments>"
                if m in li:
                    final_str += "[" + author + "](" + m.content + ")\t" + att_txt + "\n"
                else:
                    final_str += "< " + author + " >:" + m.content + "\t" + att_txt + "\n"
                if len(final_str) > 1500:
                    final_str += "```"
                    await ctx.send(final_str)
                    final_str = "```md\n"
        else:

            msg_block = []
            for r in dbutil.get_messages_above(li[0], padding):
                msg_block.append(r)
            for m in li:
                msg_block.append(m)
            for r in dbutil.get_messages_below(li[0], padding):
                msg_block.append(r)

            final_str = "```md\n"
            for m in msg_block:
                att_txt = ""
                author = (await bot.fetch_user(m.author)).name
                content = m.content[:80] + (m.content[80:] and '...')
                count = 0
                for r in dbutil.get_message_attachments(m):
                    count += 1
                if count:
                    att_txt = "<" + str(count) + "_Attachments>"
                if m in li:
                    final_str += "[" + author + "](" + m.content + ")\t" + att_txt + "\n"
                else:
                    final_str += "< " + author + " >:" + m.content + "\t" + att_txt + "\n"
                if len(final_str) > 1500:
                    final_str += "```"
                    await ctx.send(final_str)
                    final_str = "```md\n"

        if final_str != "```md\n":
            final_str += "```"
            await ctx.send(final_str)
