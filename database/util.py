import database


def record_message(m):
    """Adds a message to the database"""
    s = database.session()
    message2add = database.Message(channel=m.channel.id, author=m.author.id, content=m.content, timestamp=m.created_at)
    s.add(message2add)

    s.flush()

    attachments = []
    for a in m.attachments:
        att = database.Attachment(file_link=a.url, message_id=message2add.id)
        attachments.append(att)
    s.add_all(attachments)
    s.commit()
    s.close()


def clear_outdated_messages():
    s = database.session()


def group_message_results(query_result):
    """Takes a query resul"""
    unique_channel_msgs = {}
    unique_channels = []
    for i in query_result:
        # separating query results by channel
        channel_author = str(i.channel) + "_" + str(i.author)
        if channel_author not in unique_channels:
            unique_channels.append(channel_author)
            unique_channel_msgs[channel_author] = []

        unique_channel_msgs[channel_author].append(i)
    current_channel_groups = []
    for channel in unique_channels:
        cci = len(current_channel_groups) - 1
        current_groups = [[]]
        msg_channel = unique_channel_msgs[channel]
        last_msg = None
        for msg in msg_channel:
            if len(current_groups[cci]) == 0:
                last_msg = msg
                current_groups[cci].append(msg)
            else:
                if (msg.timestamp - last_msg.timestamp).total_seconds() / 60.0 < 5:
                    current_groups[cci].append(msg)
                else:
                    last_msg = msg
                    current_groups.append([msg])
        current_channel_groups.append(current_groups)
    return current_channel_groups
