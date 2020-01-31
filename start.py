import calc_JIT_index

# import notify_and_replied_timing

import histgram_notify_and_replied_timing2


def main():
    usernames = ["arisa", "nakano", "taka", "takatoshi", "yamada", "yamamura"]
    for username in usernames:
        calc_JIT_index.username = username
        calc_JIT_index.main()
        histgram_notify_and_replied_timing2.username = username
        histgram_notify_and_replied_timing2.main()


if __name__ == '__main__':
    main()
