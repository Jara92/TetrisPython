import os
import sys
import pickle


class CScoreManager:
    __data_directory = "./data"
    __data_file = "score.data"

    def __init__(self):
        CScoreManager.__init_manager()

    @staticmethod
    def __init_manager():
        # Create data directory if it does not exist
        success = CScoreManager.__create_data_directory()

        if not success:
            return False

        # Create data file if it does not exist
        success = CScoreManager.__create_data_file()

        if not success:
            return False
        else:
            return True

    @staticmethod
    def __create_data_directory():
        """
        Create CScoreManager.__data_directory if this directory does not exist.
        :return: True - succes.
        """

        if not os.path.isdir(CScoreManager.__data_directory):
            try:
                os.mkdir(CScoreManager.__data_directory)
                return True
            except OSError as error:
                print(error)
                return False

        return True

    @staticmethod
    def save_score(score: int):
        """
        Save new top score value in data file.
        :param score: Score to be saved.
        :return: True - success.
        """

        # If folder cannot be created there is no option to save my data.
        if not CScoreManager.__create_data_directory():
            return False

        data_file_path = CScoreManager.__data_directory + "/" + CScoreManager.__data_file

        # Create the file if it does not exist.
        if not os.path.isfile(data_file_path):

            try:
                file = open(data_file_path, "wb")
                pickle.dump(score, file)
                file.close()
                return True
            except OSError as error:
                print(error)
                return False
        else:
            return False

    @staticmethod
    def get_score():
        # Return 0 when manager cannot be initialized.
        if not CScoreManager.__init_manager():
            return 0

        data_file_path = CScoreManager.__data_directory + "/" + CScoreManager.__data_file
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

        return CScoreManager.save_score(0)
