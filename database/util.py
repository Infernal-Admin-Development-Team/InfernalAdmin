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


def add_report(category, poster_id, offender_id, content, timestamp, offending_messages):
    s = database.session()
    report2add = database.Report(category=category, poster_id=poster_id, offender_id=offender_id, status=0,
                                 content=content, timestamp=timestamp)
    s.add(report2add)
    s.flush()
    report_id = report2add.id
    refrences = []
    for msg in offending_messages:
        refrences.append(database.Reference(message_id=msg.id, report_id=report2add.id))
    s.add_all(refrences)
    s.commit()
    s.close()

    return report_id

def clear_outdated_messages():
    s = database.session()


def group_message_results(query_result):
    """Takes a query result (or list of messages)
     and splits them into groups depending on channel, author or timestamp"""
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

        current_groups = [[]]
        msg_channel = unique_channel_msgs[channel]
        last_msg = None
        for msg in msg_channel:

            if len(current_groups[-1]) == 0:
                last_msg = msg
                current_groups[-1].append(msg)
            else:
                if (msg.timestamp - last_msg.timestamp).total_seconds() / 60.0 < 5:
                    current_groups[-1].append(msg)
                else:
                    last_msg = msg
                    current_groups.append([msg])
        current_channel_groups.append(current_groups)
    return current_channel_groups


def get_messages_above(msg, count):
    """Grabs the N messages above the message in the same channel"""
    s = database.session()
    timestamp = str(msg.timestamp)
    channel = str(msg.channel)
    results = s.execute(
        "WITH R AS (SELECT * FROM message WHERE message.timestamp<'" + timestamp + "' AND message.channel=" + channel +
        " ORDER BY timestamp DESC LIMIT " + str(count) + ") SELECT * FROM R ORDER BY timestamp;")
    s.close()
    return results


def get_messages_below(msg, count):
    """Grabs the N messages below the message in the same channel"""
    s = database.session()
    timestamp = str(msg.timestamp)
    channel = str(msg.channel)
    results = s.execute(
        "SELECT * FROM message WHERE message.timestamp>'" + timestamp + "' AND message.channel=" + channel +
        " ORDER BY timestamp LIMIT " + str(count) + ";")
    s.close()
    return results


def get_message_attachments(msg):
    s = database.session()
    results = s.execute("SELECT * FROM message_attachment WHERE message_id=" + str(msg.id))
    s.close()
    return results
