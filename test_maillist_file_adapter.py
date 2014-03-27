from maillist_factory import MailListFactory
from maillist_file_adapter import MailListFileAdapter
import unittest
import os
from subprocess import call


class MailListFileAdapterTest(unittest.TestCase):
    """docstring for MailListFileAdapterTest"""
    def setUp(self):
        self.factory = MailListFactory()
        self.m = self.factory.create("Hack Bulgaria")
        self.m.add_subscriber("Rado", "rado@rado")
        self.m.add_subscriber("Ivan", "ivan@ivan")
        self.db_path = "list_tests/"

        self.maillist_adapter = MailListFileAdapter(self.db_path, self.m)

    def test_get_file_name(self):
        self.assertEqual("Hack_Bulgaria",
                         self.maillist_adapter.get_file_name())

    def test_get_file_path(self):
        self.assertEqual(self.db_path + "Hack_Bulgaria",
                         self.maillist_adapter.get_file_path())

    def test_prepare_for_save(self):
        expected = sorted(["Rado - rado@rado", "Ivan - ivan@ivan"])
        self.assertEqual(expected, self.maillist_adapter.prepare_for_save())

    def test_save_id_on_first_line(self):
        file_name = self.maillist_adapter.get_file_name()
        self.maillist_adapter.save()

        file = open(self.db_path + file_name, "r")
        contents = file.read()
        file.close()

        lines = contents.split("\n")
        self.assertEqual("1", lines[0])

    def test_save_contents_format(self):
        file_name = self.maillist_adapter.get_file_name()
        self.maillist_adapter.save()
        file = open(self.db_path + file_name, "r")
        contents = file.read()
        lines = contents.split("\n")
        file.close()

        expected = sorted(["Rado - rado@rado", "Ivan - ivan@ivan"])
        expected = "\n".join(expected)
        lines.pop(0)  # remove the id

        self.assertEqual(expected, "\n".join(lines))

        os.remove(self.maillist_adapter.get_file_path())

    def test_load_from_file(self):
        m = self.factory.create("Hack Bulgaria")
        m.add_subscriber("Ivo", "ivo@ivo.com")
        m.add_subscriber("Maria", "maria@maria.com")
        file_adapter = MailListFileAdapter(self.db_path, m)
        file_name = file_adapter.get_file_name()

        file_adapter.save()

        loaded_mail_list = file_adapter.load(file_name)

        self.assertEqual(m.get_id(), loaded_mail_list.get_id())
        self.assertEqual(m.get_name(), loaded_mail_list.get_name())
        self.assertEqual(m.get_subscribers(),
                         loaded_mail_list.get_subscribers())

    def test_load_from_file_without_giving_maillist(self):
        m = self.factory.create("Hack Bulgaria")
        m.add_subscriber("Ivo", "ivo@ivo.com")
        m.add_subscriber("Maria", "maria@maria.com")
        file_adapter = MailListFileAdapter(self.db_path, m)
        file_adapter.save()

        load_adapter = MailListFileAdapter(self.db_path)
        loaded_mail_list = load_adapter.load(file_adapter.get_file_name())

        self.assertEqual(m.get_id(), loaded_mail_list.get_id())
        self.assertEqual(m.get_name(), loaded_mail_list.get_name())
        self.assertEqual(m.get_subscribers(),
                         loaded_mail_list.get_subscribers())

    def test_load_from_empty_list(self):
        m = self.factory.create("Hack Bulgaria")
        file_adapter = MailListFileAdapter(self.db_path, m)
        file_adapter.save()

        load_adapter = MailListFileAdapter(self.db_path)
        loaded_mail_list = load_adapter.load(file_adapter.get_file_name())

        self.assertEqual(0, loaded_mail_list.count())
        self.assertEqual([], loaded_mail_list.get_subscribers())

    def tearDown(self):
        call("rm -rf {}".format(self.db_path), shell=True)


if __name__ == '__main__':
    unittest.main()
