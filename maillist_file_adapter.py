from maillist import MailList
import os
import sqlite3


class MailListFileAdapter():
    """docstring for MailListFileAdapter"""
    def __init__(self, db_path, mail_list=None):
        self.db_path = sqlite3.connect("maillist.db")
        self.cursor = self.db_path.cursor()
        self.mail_list = mail_list
        self._ensure_db_path()

    # (name, email) -> "<name> - <email>"
    def prepare_for_save(self):
        subscribers = self.mail_list.get_subscribers()
        subscribers = map(lambda t: "{} - {}".format(t[0], t[1]), subscribers)

        return sorted(subscribers)

    def save(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Lists(id, name)""")
        lists_query = ("""INSERT INTO Lists(id, name) VALUES(?, ?)""")
        lists_data = [self.mail_list.get_id(), self.mail_list.get_name()]
        self.cursor.execute(lists_query, lists_data)
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS
                    {}(id, name, email)""".format(self.mail_list.get_name()))
        self.db_path.commit()
        self.db_path.close()

    def load(self, file_name):
        maillist_name = file_name.replace("_", " ")

        # create a Dummy mail list, so we can call the methods
        if self.mail_list is None:
            self.mail_list = MailList(-1, maillist_name)

        file = open(self.get_file_path(), "r")
        contents = file.read()
        file.close()

        lines = contents.split("\n")
        maillist_id = int(lines[0])
        lines.pop(0)

        result = MailList(maillist_id, maillist_name)

        for unparsed_subscriber in lines:
            subscriber = unparsed_subscriber.split(" - ")
            if len(subscriber) > 1:
                result.add_subscriber(subscriber[0], subscriber[1])
            else:
                return result

        return result

    def _ensure_db_path(self):
        if not os.path.isfile("maillist.db"):
            self.db_path = sqlite3.connect("maillist.db")
