from rimboe_road.menu import MainMenu
from user_info.user_name import UserInput
from user_info.consent_form import UserConsent
from user_info.rate_test import TestRating
from user_info.game_explanation import GameExplanation
from user_info.end_of_practise import EndOfPractise
import os.path
import pathlib
from datetime import datetime


def start():
    user_consent_form = UserConsent()
    user_accepted = user_consent_form.get_user_accepted()

    GameExplanation()

    if user_accepted:
        print("User accepted the terms.")
    else:
        print("User declined the terms.")
        return

    user_input_form = UserInput()
    user_name = user_input_form.get_user_name()
    user_name.replace(" ", "_")

    full_report = str(datetime.now()) + "\n"
    user_result = ""
    flag = False
    while not flag:
        MainMenu("Start Practice Round", 0, "Practice Dummy")
        end = EndOfPractise()
        flag = end.get_experiment_start()

    difficulties = [5, 0, 9]
    names = ["Max", "Hidde", "Gabriel"]
    for idx in range(len(difficulties)):
        tmp = MainMenu("Start Round " + str(idx + 1), difficulties[idx],
                       names[idx])
        full_report += str(tmp.get_report())
        test_rating_form = TestRating(names[idx])
        user_result += f"{names[idx]}: {test_rating_form.test_rating} \n"

    save_path = pathlib.Path(__file__).parent.resolve() / "data"
    os.makedirs(save_path, exist_ok=True)
    report_file = open(os.path.join(save_path, user_name + "_report.txt"), "w")
    report_file.write(full_report)
    report_file.close()
    rating_file = open(os.path.join(save_path, user_name + "_rating.txt"), "w")
    rating_file.write(user_result)
    rating_file.close()


if __name__ == "__main__":
    start()
