import os
import pickle


class ScoreManager:
    """
    Top score manager. Saves and reads saved top score form data file.
    """
    __data_directory = "./data"
    __data_file = "score.data"

    def __init__(self):
        ScoreManager.init_manager()

    @staticmethod
    def init_manager(data_directory=None):
        """
        Init score manager adn prepare data structure in IO system.
        :return: True - success; False - failed to init.
        """
        if data_directory is not None:
            ScoreManager.__data_directory = data_directory

        # Create data directory if it does not exist
        if not os.path.isdir(ScoreManager.__data_directory):
            success = ScoreManager.__create_data_directory()

            if not success:
                return False

        # Create data file if it does not exist
        if not os.path.isfile(ScoreManager.__data_directory + "/" + ScoreManager.__data_file):
            success = ScoreManager.__create_data_file()

            if not success:
                return False

        return True

    @staticmethod
    def __create_data_directory():
        """
        Create CScoreManager.__data_directory if this directory does not exist.
        :return: True - succes.
        """

        try:
            os.mkdir(ScoreManager.__data_directory)
            return True
        except OSError as error:
            print(error)
            return False

    @staticmethod
    def save_score(score: int):
        """
        Save new top score value in data file.
        :param score: Score to be saved.
        :return: True - success.
        """

        data_file_path = ScoreManager.__data_directory + "/" + ScoreManager.__data_file

        # Create the file if it does not exist.
        try:
            file = open(data_file_path, "wb")
            pickle.dump(score, file)
            file.close()
            return True
        except OSError as error:
            print(error)
            return False

    @staticmethod
    def get_score():
        """
        Get top score from data file.
        :return: Top score
        """

        # Return 0 when manager cannot be initialized.
        if not ScoreManager.init_manager():
            return 0

        data_file_path = ScoreManager.__data_directory + "/" + ScoreManager.__data_file
        value = 0

        try:
            file = open(data_file_path, "rb")
            value = pickle.load(file)
            file.close()
        except OSError as error:
            print(error)

        return value

    @staticmethod
    def __create_data_file():

        """
        Create CScoreManager.__data_file if this file does not exist and fill it with integer 0 value.
        :return: True - succes.
        """

        return ScoreManager.save_score(0)
