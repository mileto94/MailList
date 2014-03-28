from commandparser import CommandParser
from maillist_factory import MailListFactory
from maillist_file_adapter import MailListFileAdapter
from subscriber import Subscriber
import sqlite3
import sys
import os


class MailListProgram():
    """docstring for MailListProgram"""
    def __init__(self):
        self.factory = MailListFactory()
        self.cp = CommandParser()
        self.lists = []

        self._load_initial_state()
        self._init_callbacks()
        self._loop()

    def create_list_callback(self, arguments):
        name = " ".join(arguments)

        maillist = self.factory.create(name)
        maillist_adapter = MailListFileAdapter(self.db_path, maillist)
        maillist_adapter.save()

        self.lists.append(maillist.get_name())
        print(self.lists)

    def add_subscriber_callback(self, arguments):
        list_id = int("".join(arguments))
        name = input("name>")
        email = input("email>")
        subscriber = Subscriber(name, email)
        subscriber.save()
        self.db_path = sqlite3.connect("maillist.db")
        self.cursor = self.db_path.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS relations
                            (list_id, subscriber_id)""")
        query = ("""INSERT INTO relations(list_id, subscriber_id)
                    VALUES(?, ?)""")
        data = [list_id, subscriber.id]
        print(data)
        self.cursor.execute(query, data)
        self.db_path.commit()
        self.db_path.close()

    def show_lists_callback(self, arguments):
        for list_id in self.lists:
            current_list = self.lists[list_id][0]
            print("[{}] {}".format(list_id,
                                   current_list.get_name()))

    def show_list_callback(self, arguments):
        list_id = int("".join(arguments))

        if list_id in self.lists:
            subscribers = self.lists[list_id][0].get_subscribers()
            for s in subscribers:
                print("{} - {}".format(s[0], s[1]))
        else:
            print("List with id <{}> was not found".format(list_id))

    def exit_callback(self, arguments):
        sys.exit(0)

    def _load_initial_state(self):
        if os.path.isfile("maillist.db"):
            self.db_path = sqlite3.connect("maillist.db")
            self.cursor = self.db_path.cursor()
            lists_data = self.cursor.execute("""SELECT name FROM Lists""")
            for list in lists_data:
                self.lists.append(list[0])

    def _init_callbacks(self):
        self.cp.on("create", self.create_list_callback)
        self.cp.on("add", self.add_subscriber_callback)
        self.cp.on("show_lists", self.show_lists_callback)
        self.cp.on("show_list", self.show_list_callback)
        self.cp.on("exit", self.exit_callback)
        # TODO - implement the rest of the callbacks

    def _notify_save(self, list_id):
        self.lists[list_id - 1].save()

    def _loop(self):
        while True:
            command = input(">")
            self.cp.take_command(command)


if __name__ == '__main__':
    MailListProgram()
