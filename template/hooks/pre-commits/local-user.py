import os
import sys
import re
import logging

from git import Repo, GitConfigParser

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def check_local_user(repo):
    config = repo.config_reader()
    result = False

    if 'user' in config.sections():
        user = dict(config.items('user'))
        result = True

        if 'name' not in user:
            logging.warning("Local user.name is not set.")
            result = False
        elif 'email' not in user:
            logging.warning("Local user.email is not set.")
            result = False
    else:
        logging.warning("Local user setting not set.")

    return result


def has_remotes(repo):
    if len(repo.remotes) == 0:
        logging.warning("Repo does not have any remotes set.")
        return False
    else:
        return True


def predict_local_user(repo):
    config = GitConfigParser(
        [os.path.normpath(os.path.expanduser("~/.gitconfig"))],
        read_only=True
    )

    writer = repo.config_writer()
    sections = config.sections()

    i = 0
    is_set = False
    while i < len(sections) and not is_set:
        sec = sections[i]

        if 'multi-user' in sec:
            # name = re.findall(r'"([^"]*)"', sec)[1]
            user = dict(config.items(sec))
            logging.debug("multi-user: %s", str(user))

            if 'url' in user and 'name' in user and 'email' in user:
                for remote in repo.remotes:
                    logging.debug("remote-url: %s", remote.url)
                    prog = re.compile(user['url'])

                    if prog.match(remote.url):
                        logging.info(
                            "%s found in remote url %s",
                            user['url'], remote.url
                        )

                        logging.info(
                            "Setting local user.name to %s",
                            user["name"]
                        )
                        writer.set_value('user', 'name', user['name'])

                        logging.info(
                            "Setting local user.email to %s",
                            user["email"]
                        )
                        writer.set_value('user', 'email', user['email'])

                        writer.release()
                        is_set = True
                        break
            elif 'url' not in user:
                logging.warning('url not set for %s', sec)
            elif 'name' not in user:
                logging.warning('name not set for %s', sec)
            elif 'email' not in user:
                logging.warning('email not set for %s', sec)

        i = i + 1

    return is_set


if __name__ == '__main__':
    logging.info("Locating git repo...")
    repo = Repo(os.getcwd())
    rc = 1

    if not check_local_user(repo):
        if has_remotes(repo) and predict_local_user(repo):
            rc = 0
        else:
            logging.warning(
                "Failed to automatically set local user.name and user.email."
            )
    else:
        logging.info("Local user already set.")
        rc = 0

    sys.exit(rc)
