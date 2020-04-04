"""Deals with long message sending"""


async def list_message(ctx, message: list, title: str = None,):
    """[summary]

    Arguments:
    ---
        ctx {discord.ext.commands.Context} -- Context of the command.
        message {list} -- list of items to send

    Keyword Arguments:
        title {str} -- First line of the message to send (default: {None})
    """
    msg = "{}\n".format(title.capitalize())
    print(message)
    for item in message:
        print(item)
        msg += "> - {}\n".format(item)
    if len(msg) >= 2000:
        list_of_msgs = [msg[i:i+2000] for i in range(0, len(msg), 2000)]
        for x in list_of_msgs:
            await ctx.send(x)
        return
    await ctx.send(msg)
