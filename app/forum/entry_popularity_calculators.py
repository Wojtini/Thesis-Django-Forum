def base(popularity: float, entry, previous_entries):
    print(f"Base popularity calculated")
    return popularity + 2


def one_user_chat(threshold: float):
    def one_user_chat_inner(popularity: float, entry, previous_entries):
        previous_entries_of_the_same_user = [entry for entry in previous_entries if entry.creator == entry.creator]
        user_activity_in_thread = len(previous_entries_of_the_same_user)
        activity_in_thread = len(previous_entries) + 1
        percent = user_activity_in_thread / activity_in_thread
        if percent > threshold:
            print(f"Popularity set to 0, oneuser thread {percent*100}%")
            return 0
        return popularity
    return one_user_chat_inner


def files_bonus(popularity: float, entry, previous_entries):
    print(f"Bonus pop from files")
    return popularity + len(entry.attached_files) * 2
