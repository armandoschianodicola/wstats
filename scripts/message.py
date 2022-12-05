import datetime
import dateutil.parser as datepars


class Message:
    """
    A class to contain info of a chat message

    Attributes
    --------------------
        self.date: str
            Contains the date on which the message was sent
        self.time: str
            Contains the time at which the message was sent
        self.author: str
            Contains the author of the message
        self.content: str
            Contains the content of the message (text or media)
        self.type: str
            Contains the type of the message (text, media or link)
        self.weekday: str
            Contains the weekday on which the day was sent
    """

    def __init__(self, chatline):
        """constructor"""
        self.date = datepars.parse(chatline.split(',')[
                                       0])  # this object is created only if the message is valid (tested before the message is created)
        self.__datelen = len(chatline.split(',')[0])
        self.time = chatline.split(',')[1][1:6]
        self.__timelen = self.__datelen + 1 + len(self.time)
        self.author = self.get_author(chatline)
        self.__authlen = self.__timelen + 3 + len(self.author) + 2  # length of string until end of author name
        self.content = self.get_content(chatline)
        self.type = self.get_type(chatline)
        self.weekday = self.weekDayMessage()

    def is_valid_message(self, line):
        """
        Determines whether a line from the file is a valid message or the continuation of the previous message.
        A message is valid if the first characters are the date and the time of the message,
        otherwise it is the continuation of the previous message.

        Parameters
        --------------------
            line: str
                Line to be analyzed

        Returns
        --------------------
            True if the message is valid, False otherwise
        """
        try:
            if datepars.parse(line.split(',')[0]):
                return True
        except Exception as e:
            return False

    def __str__(self):
        """conversion to string"""

        return 'Author: {}, Date: {}, Time: {}, Type: {} \nContent: {}'.format(
            self.author,
            self.date,
            self.time,
            self.type,
            self.content,
        )

    def get_author(self, chatline):
        """
        Determines the author of the message

        Parameters
        --------------------
            chatline: str
                Line of the chat to be analyzed

        Returns
        --------------------
            author: str
                Author of the message
        """
        authstr = chatline.split(',')[1][9:]  # string where the author name is

        return authstr.split(':')[0]

    def get_content(self, chatline):
        """
        Returns the content of the message

        Parameters
        --------------------
            chatline: str
                Line of the chat to be analyzed

        Returns
        --------------------
            Content of the message (str)
        """
        return chatline[self.__authlen:]

    def get_type(self, chatline):
        """
        Returns the type of the message

        Parameters
        --------------------
            chatline: str
                Line of the chat to be analyzed

        Returns
        --------------------
            messType: str
                Type of the message
        """
        if '<Media omitted>' in chatline[self.__authlen:]:
            messType = 'Media'
        elif 'https://' in chatline[self.__authlen:]:
            messType = 'Link'
        else:
            messType = 'Text'
        return messType

    def weekDayMessage(self):
        """
        Returns the day of the week on which the message was sent

        Returns
        --------------------
            Day of the week on which message was sent (str)
        """
        weekNum = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
        weekday = self.date.weekday()
        return weekNum[weekday]


if __name__ == '__main__':
    line = '03/07/2017, 12:34 - Joe: <Media omitted>'
    m = Message(line)
    print(m)
    print(m.date)
    print(len(str(m.date)))
    print(m.time)
    print(m.is_valid_message(line))
